from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "manifest.json",
    "profile-snapshot.json",
    "scope.json",
    "source-snapshot.json",
    "inventory/all-files.json",
    "inventory/repositories.json",
    "inventory/documents.json",
    "inventory/code.json",
    "inventory/infrastructure.json",
    "inventory/skills-and-agents.json",
    "proposals/source-catalog.json",
    "proposals/architecture-pattern.json",
    "decisions/open-questions.json",
    "approvals/signoff.json",
    "checks/quality-gates.json",
    "reports/readiness-report.md",
    "reports/readiness-report.html",
    "handoff/bootstrap-import.json",
    "checksums.json",
]


def validate_package(package: Path) -> dict[str, Any]:
    package = package.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    for name in REQUIRED_FILES:
        if not (package / name).is_file():
            errors.append(f"missing required file: {name}")
    manifest_path = package / "manifest.json"
    manifest = {}
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid manifest.json: {exc}")
    for key in ("schema_version", "scanner_version", "profile", "scan_id", "system", "source", "status", "package_contract"):
        if key not in manifest:
            errors.append(f"manifest missing key: {key}")
    contract = manifest.get("package_contract", {})
    if contract and (contract.get("target_writes") is not False or contract.get("unknown_scripts_executed") is not False):
        errors.append("unsafe package contract")
    checksum_path = package / "checksums.json"
    verified = 0
    if checksum_path.is_file():
        try:
            data = json.loads(checksum_path.read_text(encoding="utf-8"))
            checksum_rows = data.get("files", [])
            expected_paths = {row.get("path") for row in checksum_rows if isinstance(row, dict)}
            actual_paths = {
                path.relative_to(package).as_posix()
                for path in package.rglob("*")
                if path.is_file() and path.name != "checksums.json"
            }
            for unexpected in sorted(actual_paths - expected_paths):
                errors.append(f"file is not covered by checksums: {unexpected}")
            for absent in sorted(expected_paths - actual_paths):
                errors.append(f"checksummed file missing: {absent}")
            for row in checksum_rows:
                candidate = (package / row["path"]).resolve()
                try:
                    candidate.relative_to(package)
                except ValueError:
                    errors.append(f"checksum path escapes package: {row['path']}")
                    continue
                if not candidate.is_file():
                    continue
                actual = sha256(candidate.read_bytes()).hexdigest()
                if actual != row["sha256"]:
                    errors.append(f"checksum mismatch: {row['path']}")
                else:
                    verified += 1
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
            errors.append(f"invalid checksums.json: {exc}")
    signoff_path = package / "approvals" / "signoff.json"
    if signoff_path.is_file():
        signoff = json.loads(signoff_path.read_text(encoding="utf-8"))
        if signoff.get("state") != "ONBOARDING_APPROVED":
            warnings.append(f"package is not importable; signoff state is {signoff.get('state', 'UNKNOWN')}")
    return {"valid": not errors, "package": str(package), "verified_checksum_files": verified, "errors": errors, "warnings": warnings}
