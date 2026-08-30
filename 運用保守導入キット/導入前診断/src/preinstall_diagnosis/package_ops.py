from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from .validator import validate_package


STATES = ["DRAFT", "SCANNER_VALIDATED", "OWNER_REVIEWED", "SECURITY_REVIEWED", "ONBOARDING_APPROVED"]
REQUIRED_ROLE = {
    "SCANNER_VALIDATED": "scanner-operator",
    "OWNER_REVIEWED": "system-owner",
    "SECURITY_REVIEWED": "security-reviewer",
    "ONBOARDING_APPROVED": "onboarding-approver",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def refresh_checksums(package: Path) -> None:
    rows = []
    for path in sorted(package.rglob("*"), key=lambda p: p.relative_to(package).as_posix().lower()):
        if path.is_file() and path.name != "checksums.json":
            rows.append({
                "path": path.relative_to(package).as_posix(),
                "sha256": sha256(path.read_bytes()).hexdigest(),
                "size_bytes": path.stat().st_size,
            })
    write_json(package / "checksums.json", {"algorithm": "sha256", "files": rows})


def advance_signoff(package: Path, next_state: str, actor: str, role: str, evidence: str) -> dict[str, Any]:
    package = package.resolve()
    verdict = validate_package(package)
    if not verdict["valid"]:
        raise ValueError("package validation failed before sign-off: " + "; ".join(verdict["errors"]))
    if next_state not in STATES:
        raise ValueError(f"unsupported state: {next_state}")
    signoff_path = package / "approvals" / "signoff.json"
    signoff = json.loads(signoff_path.read_text(encoding="utf-8"))
    current = signoff.get("state", "DRAFT")
    expected_index = STATES.index(current) + 1
    if expected_index >= len(STATES) or STATES[expected_index] != next_state:
        expected = STATES[expected_index] if expected_index < len(STATES) else "none"
        raise ValueError(f"invalid transition {current} -> {next_state}; expected {expected}")
    required_role = REQUIRED_ROLE[next_state]
    if role != required_role:
        raise ValueError(f"state {next_state} requires role {required_role}")
    if next_state == "ONBOARDING_APPROVED":
        golden = json.loads((package / "proposals" / "golden-work-item.json").read_text(encoding="utf-8"))
        if golden.get("status") != "selected" or not golden.get("acceptance_criteria"):
            raise ValueError("ONBOARDING_APPROVED requires a selected Golden Work Item with acceptance criteria")
    entry = {"state": next_state, "actor": actor, "role": role, "evidence": evidence, "timestamp": now_utc()}
    signoff.setdefault("history", []).append(entry)
    signoff["state"] = next_state
    review_key = {
        "OWNER_REVIEWED": "system_owner",
        "SECURITY_REVIEWED": "security_reviewer",
        "ONBOARDING_APPROVED": "onboarding_approver",
    }.get(next_state)
    if review_key:
        signoff.setdefault("reviews", {})[review_key] = entry
    write_json(signoff_path, signoff)

    manifest_path = package / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["status"] = next_state
    write_json(manifest_path, manifest)

    handoff_path = package / "handoff" / "bootstrap-import.json"
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    handoff["import_allowed"] = next_state == "ONBOARDING_APPROVED"
    handoff["current_signoff_state"] = next_state
    write_json(handoff_path, handoff)
    refresh_checksums(package)
    return validate_package(package)


def set_golden_work_item(package: Path, item_id: str, title: str, evidence_path: str, acceptance_criteria: list[str], actor: str) -> dict[str, Any]:
    package = package.resolve()
    verdict = validate_package(package)
    if not verdict["valid"]:
        raise ValueError("package validation failed before Golden Work Item update: " + "; ".join(verdict["errors"]))
    signoff = json.loads((package / "approvals" / "signoff.json").read_text(encoding="utf-8"))
    if signoff.get("state") not in {"DRAFT", "SCANNER_VALIDATED"}:
        raise ValueError("Golden Work Item can be selected only in DRAFT or SCANNER_VALIDATED")
    if not acceptance_criteria or any(not item.strip() for item in acceptance_criteria):
        raise ValueError("at least one non-empty acceptance criterion is required")
    golden = {
        "status": "selected",
        "id": item_id,
        "title": title,
        "evidence_path": evidence_path,
        "acceptance_criteria": acceptance_criteria,
        "selected_by": actor,
        "selected_at": now_utc(),
    }
    write_json(package / "proposals" / "golden-work-item.json", golden)
    refresh_checksums(package)
    return validate_package(package)
