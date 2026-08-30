from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any


SUPPORTED_SCHEMA = "1.1.0"
SUPPORTED_CONTRACT = "1.1.0"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def validate_package_files(package: Path) -> dict[str, Any]:
    errors: list[str] = []
    required = [
        "manifest.json", "profile-snapshot.json", "checksums.json", "approvals/signoff.json",
        "handoff/bootstrap-import.json", "proposals/golden-work-item.json",
        "inventory/all-files.json", "inventory/repositories.json", "inventory/documents.json",
        "inventory/code.json", "inventory/infrastructure.json", "inventory/skills-and-agents.json",
    ]
    for relative in required:
        if not (package / relative).is_file():
            errors.append(f"missing required file: {relative}")
    if errors:
        return {"valid": False, "errors": errors, "verified_files": 0}
    checksums = load_json(package / "checksums.json")
    rows = checksums.get("files", [])
    expected = {row.get("path") for row in rows if isinstance(row, dict)}
    actual = {
        path.relative_to(package).as_posix()
        for path in package.rglob("*")
        if path.is_file() and path.name != "checksums.json"
    }
    for relative in sorted(actual - expected):
        errors.append(f"file is not covered by checksums: {relative}")
    for relative in sorted(expected - actual):
        errors.append(f"checksummed file missing: {relative}")
    verified = 0
    for row in rows:
        relative = row.get("path")
        if not isinstance(relative, str):
            errors.append("checksum entry has no path")
            continue
        candidate = (package / relative).resolve()
        try:
            candidate.relative_to(package)
        except ValueError:
            errors.append(f"checksum path escapes package: {relative}")
            continue
        if not candidate.is_file():
            continue
        if sha256(candidate.read_bytes()).hexdigest() != row.get("sha256"):
            errors.append(f"checksum mismatch: {relative}")
        else:
            verified += 1
    return {"valid": not errors, "errors": errors, "verified_files": verified}


def verify_source(package: Path, diagnosis_root: Path, target_override: Path | None = None) -> dict[str, Any]:
    diagnosis_entry = diagnosis_root.resolve() / "diagnose.py"
    if not diagnosis_entry.is_file():
        raise ValueError(f"diagnosis entry point not found: {diagnosis_entry}")
    command = [sys.executable, str(diagnosis_entry), "verify-source", "--package", str(package)]
    if target_override is not None:
        command.extend(["--target", str(target_override.resolve())])
    process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120, check=False)
    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"source verifier returned invalid output: {process.stdout or process.stderr}") from exc
    if process.returncode != 0 or not result.get("match"):
        raise ValueError(
            "source fingerprint mismatch; rerun diagnosis and approval before import: "
            f"package={result.get('package_fingerprint')} current={result.get('current_fingerprint')}"
        )
    return result


def preflight(package: Path, diagnosis_root: Path, target_override: Path | None = None) -> dict[str, Any]:
    package = package.resolve()
    file_check = validate_package_files(package)
    if not file_check["valid"]:
        raise ValueError("package validation failed: " + "; ".join(file_check["errors"]))
    manifest = load_json(package / "manifest.json")
    signoff = load_json(package / "approvals" / "signoff.json")
    handoff = load_json(package / "handoff" / "bootstrap-import.json")
    golden = load_json(package / "proposals" / "golden-work-item.json")
    if manifest.get("schema_version") != SUPPORTED_SCHEMA:
        raise ValueError(f"unsupported package schema: {manifest.get('schema_version')}")
    if handoff.get("contract_version") != SUPPORTED_CONTRACT:
        raise ValueError(f"unsupported handoff contract: {handoff.get('contract_version')}")
    if manifest.get("status") != "ONBOARDING_APPROVED" or signoff.get("state") != "ONBOARDING_APPROVED":
        raise ValueError("package is not ONBOARDING_APPROVED")
    if handoff.get("import_allowed") is not True:
        raise ValueError("handoff import_allowed is not true")
    if golden.get("status") != "selected" or not golden.get("acceptance_criteria"):
        raise ValueError("Golden Work Item is not complete")
    if handoff.get("scan_id") != manifest.get("scan_id"):
        raise ValueError("scan_id mismatch between manifest and handoff")
    if handoff.get("source_fingerprint") != manifest.get("source", {}).get("fingerprint"):
        raise ValueError("source fingerprint mismatch inside package")
    source_check = verify_source(package, diagnosis_root, target_override)
    return {
        "ready": True,
        "package": str(package),
        "scan_id": manifest["scan_id"],
        "system": manifest["system"],
        "source": manifest["source"],
        "verified_checksum_files": file_check["verified_files"],
        "source_verification": source_check,
        "golden_work_item": golden,
    }


def safe_system_id(value: str) -> str:
    if not re.fullmatch(r"[0-9a-z][0-9a-z_-]{0,99}", value):
        raise ValueError(f"unsafe system id: {value}")
    return value


def graph_seeds(manifest: dict[str, Any], files: list[dict[str, Any]], repositories: list[dict[str, Any]], golden: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    scan_id = manifest["scan_id"]
    system_node = f"system:{manifest['system']['id']}"
    nodes = [{"id": system_node, "type": "System", "name": manifest["system"]["name"], "source_scan_id": scan_id}]
    edges = []
    for repo in repositories:
        node_id = "repository:" + sha256((scan_id + ":" + repo["relative_path"]).encode("utf-8")).hexdigest()[:20]
        nodes.append({"id": node_id, "type": "Repository", "name": repo["relative_path"], "properties": repo, "source_scan_id": scan_id})
        edges.append({"from": system_node, "to": node_id, "type": "HAS_REPOSITORY", "confidence": "observed", "source_scan_id": scan_id})
    for item in files:
        node_id = "asset:" + sha256((scan_id + ":" + item["path"]).encode("utf-8")).hexdigest()[:20]
        nodes.append({
            "id": node_id,
            "type": "Asset",
            "name": item["name"],
            "properties": {"path": item["path"], "role_candidate": item["role_candidate"], "sha256": item["sha256"]},
            "source_scan_id": scan_id,
        })
        edges.append({"from": system_node, "to": node_id, "type": "HAS_ASSET_CANDIDATE", "confidence": "observed", "source_scan_id": scan_id})
    golden_id = "work-item:" + re.sub(r"[^0-9A-Za-z_-]+", "-", golden["id"])
    nodes.append({"id": golden_id, "type": "GoldenWorkItem", "name": golden["title"], "properties": golden, "source_scan_id": scan_id})
    edges.append({"from": system_node, "to": golden_id, "type": "VALIDATED_BY", "confidence": "approved", "source_scan_id": scan_id})
    return ({"schema_version": "1.0.0", "nodes": nodes}, {"schema_version": "1.0.0", "edges": edges})


def import_package(package: Path, diagnosis_root: Path, operations_root: Path, target_override: Path | None = None) -> dict[str, Any]:
    operations_root = operations_root.resolve()
    assessment = preflight(package, diagnosis_root, target_override)
    package = package.resolve()
    manifest = load_json(package / "manifest.json")
    system_id = safe_system_id(manifest["system"]["id"])
    scan_id = manifest["scan_id"]
    system_root = operations_root / "systems" / system_id
    package_destination = system_root / "onboarding" / "packages" / scan_id
    receipt_path = operations_root / "import-receipts" / f"{scan_id}.json"
    if package_destination.exists() or receipt_path.exists():
        raise ValueError(f"scan_id is already imported: {scan_id}")

    staging_parent = operations_root / ".import-staging"
    staging_parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f"{system_id}-{scan_id[:8]}-", dir=staging_parent))
    try:
        staged_package = staging / "package"
        shutil.copytree(package, staged_package)
        copied_check = validate_package_files(staged_package)
        if not copied_check["valid"]:
            raise ValueError("copied package failed checksum validation: " + "; ".join(copied_check["errors"]))
        files = load_json(staged_package / "inventory" / "all-files.json")
        repositories = load_json(staged_package / "inventory" / "repositories.json")
        golden = load_json(staged_package / "proposals" / "golden-work-item.json")
        nodes, edges = graph_seeds(manifest, files, repositories, golden)

        package_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(staged_package), str(package_destination))
        write_json(system_root / "config" / "system.json", {
            "system": manifest["system"],
            "source_root": manifest["source"]["root"],
            "current_scan_id": scan_id,
            "source_fingerprint": manifest["source"]["fingerprint"],
            "updated_at": now_utc(),
        })
        write_json(system_root / "onboarding" / "current.json", {
            "scan_id": scan_id,
            "package_path": package_destination.relative_to(operations_root).as_posix(),
            "signoff_state": "ONBOARDING_APPROVED",
        })
        inventory_destination = system_root / "inventory"
        inventory_destination.mkdir(parents=True, exist_ok=True)
        for name in ("repositories.json", "documents.json", "code.json", "infrastructure.json", "skills-and-agents.json", "generated-artifacts.json"):
            source = package_destination / "inventory" / name
            if source.is_file():
                shutil.copy2(source, inventory_destination / name)
        write_json(system_root / "graph-seeds" / "nodes.json", nodes)
        write_json(system_root / "graph-seeds" / "edges.json", edges)
        write_json(system_root / "decisions" / "golden-work-item.json", golden)
        receipt = {
            "receipt_version": "1.0.0",
            "imported_at": now_utc(),
            "scan_id": scan_id,
            "system": manifest["system"],
            "source_fingerprint": manifest["source"]["fingerprint"],
            "package_source": str(package),
            "package_destination": str(package_destination),
            "verified_checksum_files": copied_check["verified_files"],
            "source_verification": assessment["source_verification"],
            "graph_seed_counts": {"nodes": len(nodes["nodes"]), "edges": len(edges["edges"])},
            "status": "IMPORTED",
        }
        write_json(receipt_path, receipt)
        return receipt
    finally:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bootstrap importer for approved onboarding packages")
    parser.add_argument("command", choices=["preflight", "import-package"])
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--diagnosis-root", required=True, type=Path)
    parser.add_argument("--operations-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--target", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "preflight":
            result = preflight(args.package, args.diagnosis_root, args.target)
        else:
            result = import_package(args.package, args.diagnosis_root, args.operations_root, args.target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
