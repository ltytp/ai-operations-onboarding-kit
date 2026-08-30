from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from fnmatch import fnmatch
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any

from . import SCANNER_VERSION, SCHEMA_VERSION


DOC_EXTENSIONS = {".md", ".mdx", ".txt", ".rst", ".adoc", ".html", ".htm", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"}
CODE_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".kt", ".go", ".rs", ".cs", ".cpp", ".cc", ".c", ".h", ".hpp", ".rb", ".php", ".swift", ".scala", ".sh", ".ps1", ".bat", ".cmd", ".sql"}
TEST_MARKERS = {"test", "tests", "spec", "specs", "__tests__"}
INFRA_EXTENSIONS = {".tf", ".tfvars", ".hcl"}
BUILD_NAMES = {"package.json", "pyproject.toml", "requirements.txt", "poetry.lock", "uv.lock", "cargo.toml", "cargo.lock", "go.mod", "go.sum", "pom.xml", "build.gradle", "settings.gradle", "makefile", "dockerfile", "docker-compose.yml", "docker-compose.yaml"}
CI_PARTS = {".github", ".gitlab", "azure-pipelines.yml", "jenkinsfile", ".circleci"}
AI_NAMES = {"agents.md", "skill.md", "mcp.json", "mcp.yaml", "mcp.yml", "claude.md", "copilot-instructions.md"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def hash_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def hash_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def system_id(name: str) -> str:
    value = re.sub(r"[^0-9A-Za-z_-]+", "-", name.strip()).strip("-").lower()
    return value or "system-" + sha256(name.encode("utf-8")).hexdigest()[:10]


def is_reparse_or_symlink(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        attrs = getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0)
        return bool(attrs & 0x400)
    except OSError:
        return True


def role_for(relative: str, name: str, suffix: str, generated_names: set[str]) -> tuple[str, list[str]]:
    lower = relative.lower().replace("\\", "/")
    parts = set(lower.split("/"))
    lname = name.lower()
    signals: list[str] = []
    if any(part in generated_names for part in parts):
        return "generated_artifact", ["generated-directory"]
    if lname == "agents.md":
        return "agent_instruction", ["AGENTS.md"]
    if lname == "skill.md":
        return "skill_definition", ["SKILL.md"]
    if lname in AI_NAMES or ".codex" in parts:
        return "ai_configuration", ["ai-asset-name"]
    if suffix in INFRA_EXTENSIONS or lname in {"dockerfile", "docker-compose.yml", "docker-compose.yaml"} or "terraform" in parts or "kubernetes" in parts or "k8s" in parts:
        return "infrastructure", ["infrastructure-pattern"]
    if any(part in CI_PARTS for part in parts) or lname in CI_PARTS:
        return "ci_configuration", ["ci-pattern"]
    if lname in BUILD_NAMES:
        return "build_configuration", ["build-manifest"]
    if suffix in CODE_EXTENSIONS:
        if parts.intersection(TEST_MARKERS) or lname.startswith("test_") or lname.endswith("_test" + suffix):
            return "test_code", ["test-pattern"]
        return "source_code", ["code-extension"]
    if suffix in DOC_EXTENSIONS:
        return "document", ["document-extension"]
    if lname.startswith("."):
        signals.append("hidden-file")
    return "unknown", signals


def safe_heading(path: Path, max_bytes: int) -> dict[str, Any]:
    result: dict[str, Any] = {"title": None, "metadata": {}}
    try:
        raw = path.read_bytes()[:max_bytes]
        text = raw.decode("utf-8", errors="replace")
    except OSError as exc:
        result["read_error"] = str(exc)
        return result
    for line in text.splitlines()[:80]:
        stripped = line.strip()
        if stripped.startswith("#"):
            result["title"] = stripped.lstrip("#").strip()[:200]
            break
    if text.startswith("---"):
        for line in text.splitlines()[1:40]:
            if line.strip() == "---":
                break
            if ":" in line:
                key, value = line.split(":", 1)
                if key.strip() in {"name", "description", "version"}:
                    result["metadata"][key.strip()] = value.strip()[:500]
    return result


def git_value(repo: Path, *args: str) -> str | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            check=False,
        )
        return proc.stdout.strip() if proc.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def repository_snapshot(root: Path, discovered: list[Path]) -> list[dict[str, Any]]:
    roots = set(discovered)
    if (root / ".git").exists():
        roots.add(root)
    rows = []
    for repo in sorted(roots, key=lambda p: str(p).lower()):
        status = git_value(repo, "status", "--porcelain=v1")
        rows.append({
            "path": str(repo),
            "relative_path": "." if repo == root else repo.relative_to(root).as_posix(),
            "head": git_value(repo, "rev-parse", "HEAD"),
            "branch": git_value(repo, "branch", "--show-current"),
            "dirty": bool(status),
            "status_entry_count": len(status.splitlines()) if status else 0,
        })
    return rows


def scan(target: Path, system_name: str, profile: dict[str, Any], profile_sha256: str) -> dict[str, Any]:
    target = target.resolve()
    excluded = {item.lower() for item in profile["exclude_directories"]}
    excluded_paths = {str(item).replace("\\", "/").strip("/").casefold() for item in profile.get("exclude_paths", [])}
    generated = {item.lower() for item in profile["generated_directory_names"]}
    max_hash = int(profile["max_hash_bytes"])
    max_read = int(profile["max_config_read_bytes"])
    sensitive_patterns = [p.lower() for p in profile["sensitive_name_patterns"]]

    files: list[dict[str, Any]] = []
    directories: list[dict[str, Any]] = []
    ai_assets: list[dict[str, Any]] = []
    generated_candidates: list[dict[str, Any]] = []
    sensitive_name_findings: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    repo_roots: list[Path] = []

    for current, dirnames, filenames in os.walk(target, topdown=True, followlinks=False):
        current_path = Path(current)
        kept_dirs = []
        for dirname in sorted(dirnames, key=str.lower):
            child = current_path / dirname
            rel = child.relative_to(target).as_posix()
            if rel.casefold() in excluded_paths:
                skipped.append({"path": rel, "reason": "profile-excluded-path"})
            elif dirname == ".git":
                repo_roots.append(current_path)
                skipped.append({"path": rel, "reason": "repository-metadata-excluded"})
            elif dirname.lower() in excluded:
                skipped.append({"path": rel, "reason": "profile-excluded-directory"})
            elif is_reparse_or_symlink(child):
                skipped.append({"path": rel, "reason": "symlink-or-reparse-point"})
            else:
                kept_dirs.append(dirname)
                directories.append({
                    "path": rel,
                    "depth": len(Path(rel).parts),
                    "role_candidate": "generated" if dirname.lower() in generated else "source",
                })
        dirnames[:] = kept_dirs

        for filename in sorted(filenames, key=str.lower):
            path = current_path / filename
            rel = path.relative_to(target).as_posix()
            if rel.casefold() in excluded_paths:
                skipped.append({"path": rel, "reason": "profile-excluded-path"})
                continue
            if is_reparse_or_symlink(path):
                skipped.append({"path": rel, "reason": "symlink-or-reparse-point"})
                continue
            try:
                stat = path.stat()
            except OSError as exc:
                skipped.append({"path": rel, "reason": "stat-error", "detail": str(exc)})
                continue
            suffix = path.suffix.lower()
            role, signals = role_for(rel, filename, suffix, generated)
            digest = None
            hash_status = "skipped-size-limit"
            if stat.st_size <= max_hash:
                try:
                    digest = hash_file(path)
                    hash_status = "hashed"
                except OSError as exc:
                    hash_status = "read-error"
                    signals.append("hash-error:" + type(exc).__name__)
            modified = datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
            record = {
                "path": rel,
                "name": filename,
                "extension": suffix,
                "size_bytes": stat.st_size,
                "modified_utc": modified,
                "sha256": digest,
                "hash_status": hash_status,
                "role_candidate": role,
                "signals": sorted(signals),
            }
            files.append(record)
            if role in {"agent_instruction", "skill_definition", "ai_configuration"}:
                info = safe_heading(path, max_read) if filename.lower() in {"agents.md", "skill.md"} else {"title": None, "metadata": {}}
                ai_assets.append({
                    "path": rel,
                    "type": role,
                    "applies_to": str(Path(rel).parent).replace("\\", "/") or ".",
                    "inspection": info,
                    "execution_policy": "detected-only-never-executed",
                })
            if role == "generated_artifact":
                generated_candidates.append({"path": rel, "reason": "generated-directory-name", "review_state": "candidate"})
            lname = filename.lower()
            if any(fnmatch(lname, pattern) for pattern in sensitive_patterns):
                sensitive_name_findings.append({"path": rel, "reason": "sensitive-name-pattern", "content_read": False})

    files.sort(key=lambda x: x["path"].lower())
    directories.sort(key=lambda x: x["path"].lower())
    ai_assets.sort(key=lambda x: x["path"].lower())
    skipped.sort(key=lambda x: x["path"].lower())
    repos = repository_snapshot(target, repo_roots)

    hash_groups: dict[str, list[str]] = defaultdict(list)
    for item in files:
        if item["sha256"]:
            hash_groups[item["sha256"]].append(item["path"])
    duplicates = [
        {"sha256": digest, "paths": sorted(paths, key=str.lower), "count": len(paths)}
        for digest, paths in sorted(hash_groups.items()) if len(paths) > 1
    ]
    role_counts = dict(sorted(Counter(item["role_candidate"] for item in files).items()))
    extension_counts = dict(sorted(Counter(item["extension"] or "[none]" for item in files).items()))
    source_basis = [{k: item[k] for k in ("path", "size_bytes", "modified_utc", "sha256", "role_candidate")} for item in files]
    fingerprint = hash_bytes(stable_json(source_basis).encode("utf-8"))
    scan_id = hash_bytes(stable_json({
        "schema": SCHEMA_VERSION,
        "scanner": SCANNER_VERSION,
        "profile": profile_sha256,
        "source": fingerprint,
        "system": system_name,
    }).encode("utf-8"))[:24]
    hashable_count = sum(1 for item in files if item["hash_status"] == "hashed")
    unknown_count = role_counts.get("unknown", 0)
    architecture = "federated-overlay" if len(repos) > 1 else "overlay-first"

    return {
        "scan_id": scan_id,
        "created_at": utc_now(),
        "system": {"name": system_name, "id": system_id(system_name)},
        "source": {"root": str(target), "fingerprint": fingerprint, "file_count": len(files), "directory_count": len(directories)},
        "profile": {"name": profile["profile_name"], "version": profile["profile_version"], "sha256": profile_sha256, "scan_mode": profile["scan_mode"]},
        "inventory": {
            "files": files,
            "directories": directories,
            "repositories": repos,
            "ai_assets": ai_assets,
            "generated_artifacts": generated_candidates,
            "duplicates": duplicates,
            "skipped": skipped,
        },
        "statistics": {
            "role_counts": role_counts,
            "extension_counts": extension_counts,
            "total_bytes": sum(item["size_bytes"] for item in files),
            "hashed_files": hashable_count,
            "hash_coverage_percent": round((hashable_count / len(files) * 100), 2) if files else 100.0,
            "unknown_files": unknown_count,
        },
        "security": {
            "sensitive_name_findings": sorted(sensitive_name_findings, key=lambda x: x["path"].lower()),
            "content_secret_scan_performed": False,
            "reason": "metadata-only profile; sensitive file contents are not inspected",
        },
        "proposals": {
            "architecture_pattern": architecture,
            "directory_roles": directories,
            "exclusions": skipped,
            "source_catalog": [{"path": f["path"], "role_candidate": f["role_candidate"], "review_state": "candidate"} for f in files],
            "golden_work_item": {"status": "not-selected", "selection_required": True},
        },
        "open_questions": [
            {"id": "Q-001", "question": "診断対象の範囲と除外候補はシステム責任者が承認したか", "owner": "system-owner", "status": "open"},
            {"id": "Q-002", "question": "代表的な問い合わせまたは改修案件（Golden Work Item）はどれか", "owner": "operations-owner", "status": "open"},
            {"id": "Q-003", "question": "生成物候補と原本の境界は正しいか", "owner": "repository-owner", "status": "open"},
        ],
        "quality_gates": [
            {"gate": "inventory", "status": "PASS" if files else "FAIL", "evidence": f"{len(files)} files inventoried"},
            {"gate": "provenance", "status": "PASS" if fingerprint else "FAIL", "evidence": "source fingerprint recorded"},
            {"gate": "security", "status": "REVIEW", "evidence": f"{len(sensitive_name_findings)} sensitive-name findings; content scan disabled"},
            {"gate": "reproducibility", "status": "PASS", "evidence": "scanner/profile/schema versions and checksums are recorded"},
            {"gate": "human_review", "status": "PENDING", "evidence": "owner and security sign-off are required before import"},
        ],
    }
