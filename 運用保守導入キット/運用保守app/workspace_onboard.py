from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


SCRIPT_OPERATIONS_ROOT = Path(__file__).resolve().parent


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def is_diagnosis_root(path: Path) -> bool:
    return (path / "diagnose.py").is_file() and (path / "profiles" / "default-profile.json").is_file()


def discover_workspace_root(operations_root: Path) -> Path:
    for candidate in (operations_root, *operations_root.parents):
        if (candidate / ".git").exists():
            return candidate.resolve()
    return operations_root.parent.resolve()


def discover_diagnosis(workspace_root: Path, operations_root: Path) -> Path:
    sibling = operations_root.parent / "導入前診断"
    if is_diagnosis_root(sibling):
        return sibling.resolve()
    candidates: list[Path] = []
    excluded_names = {".git", "node_modules", ".venv", "venv", "__pycache__", "runs", "systems", "import-receipts", ".onboarding"}
    for current, dirnames, _ in os.walk(workspace_root, topdown=True, followlinks=False):
        current_path = Path(current)
        try:
            depth = len(current_path.relative_to(workspace_root).parts)
        except ValueError:
            continue
        if depth > 6:
            dirnames[:] = []
            continue
        dirnames[:] = sorted(
            [name for name in dirnames if name not in excluded_names and not (current_path / name).is_symlink()],
            key=str.casefold,
        )
        if current_path != operations_root and is_diagnosis_root(current_path):
            candidates.append(current_path.resolve())
            dirnames[:] = []
    candidates = sorted(set(candidates), key=lambda path: str(path).casefold())
    if len(candidates) == 1:
        return candidates[0].resolve()
    if not candidates:
        raise ValueError("導入前診断Folderを発見できません。--diagnosis-rootで指定してください")
    raise ValueError("導入前診断Folder候補が複数あります。--diagnosis-rootで1つ指定してください")


def resolve_context(args: argparse.Namespace, require_package: bool = False) -> dict[str, Path]:
    operations_value = args.operations_root or os.environ.get("ONBOARDING_OPERATIONS_ROOT")
    operations = Path(operations_value).resolve() if operations_value else SCRIPT_OPERATIONS_ROOT
    workspace_value = args.workspace_root or os.environ.get("ONBOARDING_WORKSPACE_ROOT")
    workspace = Path(workspace_value).resolve() if workspace_value else discover_workspace_root(operations)
    diagnosis_value = args.diagnosis_root or os.environ.get("ONBOARDING_DIAGNOSIS_ROOT")
    diagnosis = Path(diagnosis_value).resolve() if diagnosis_value else discover_diagnosis(workspace, operations)
    state_file = Path(args.state_file).resolve() if args.state_file else operations / ".onboarding" / "session.json"
    target_value = args.target or os.environ.get("ONBOARDING_TARGET_ROOT")
    target = Path(target_value).resolve() if target_value else workspace
    result = {"operations": operations, "workspace": workspace, "diagnosis": diagnosis, "state": state_file, "target": target}
    if require_package:
        if args.package:
            result["package"] = Path(args.package).resolve()
        elif state_file.is_file():
            result["package"] = Path(load_json(state_file)["current_package"]).resolve()
        else:
            raise ValueError("Current Packageがありません。先にstartを実行するか--packageを指定してください")
    return result


def run(command: list[str], allowed: set[int] | None = None) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment, check=False)
    allowed = allowed or {0}
    if process.returncode not in allowed:
        raise ValueError((process.stderr or process.stdout or f"command failed: {process.returncode}").strip())
    return process


def target_relative_path(parent: Path, child: Path) -> str | None:
    try:
        relative = child.resolve().relative_to(parent.resolve())
    except ValueError:
        return None
    return relative.as_posix() if relative.parts else None


def command_doctor(args: argparse.Namespace) -> dict[str, Any]:
    context = resolve_context(args)
    explicit_target = bool(args.target)
    repository_marker = (context["target"] / ".git").exists()
    target_is_tool = context["target"] in {context["operations"], context["diagnosis"]}
    target_scope_ok = (explicit_target or repository_marker) and not target_is_tool
    checks = {
        "python": {"status": "PASS", "version": sys.version.split()[0], "executable": sys.executable},
        "diagnosis_entry": {"status": "PASS" if (context["diagnosis"] / "diagnose.py").is_file() else "FAIL", "path": str(context["diagnosis"] / "diagnose.py")},
        "importer_entry": {"status": "PASS" if (context["operations"] / "bootstrap" / "bootstrap_import.py").is_file() else "FAIL", "path": str(context["operations"] / "bootstrap" / "bootstrap_import.py")},
        "target": {"status": "PASS" if context["target"].is_dir() else "FAIL", "path": str(context["target"])},
        "target_scope": {
            "status": "PASS" if target_scope_ok else "FAIL",
            "evidence": (
                "target cannot be one of the tool folders" if target_is_tool else
                ("explicit --target" if explicit_target else (".git marker found" if repository_marker else "no .git marker; specify --target explicitly"))
            ),
        },
        "operations_writable": {"status": "PASS" if os.access(context["operations"], os.W_OK) else "FAIL", "path": str(context["operations"])},
    }
    return {"ready": all(item["status"] == "PASS" for item in checks.values()), "paths": {key: str(value) for key, value in context.items()}, "checks": checks}


def command_start(args: argparse.Namespace) -> dict[str, Any]:
    context = resolve_context(args)
    doctor = command_doctor(args)
    if not doctor["ready"]:
        raise ValueError("Environment doctor failed")
    system_name = args.system_name or context["target"].name
    command = [
        sys.executable, str(context["diagnosis"] / "diagnose.py"), "scan",
        "--target", str(context["target"]), "--system-name", system_name,
        "--output-root", str(context["diagnosis"] / "runs"),
        "--profile", str(context["diagnosis"] / "profiles" / "default-profile.json"),
    ]
    excluded_tools: list[str] = []
    for tool_root in (context["diagnosis"], context["operations"]):
        relative = target_relative_path(context["target"], tool_root)
        if relative and relative not in excluded_tools:
            excluded_tools.append(relative)
            command.extend(["--exclude-path", relative])
    guide_candidates = {
        context["workspace"] / "導入準備完了.md",
        context["diagnosis"].parent / "導入準備完了.md",
        context["operations"].parent / "導入準備完了.md",
    }
    for guide in sorted(guide_candidates, key=lambda path: str(path).casefold()):
        relative_guide = target_relative_path(context["target"], guide) if guide.is_file() else None
        if relative_guide and relative_guide not in excluded_tools:
            excluded_tools.append(relative_guide)
            command.extend(["--exclude-path", relative_guide])
    process = run(command)
    package_line = next((line for line in process.stdout.splitlines() if line.startswith("PACKAGE_PATH=")), None)
    if not package_line:
        raise ValueError("診断は完了しましたがPackage pathを取得できません")
    package = Path(package_line.split("=", 1)[1]).resolve()
    prior_history = []
    if context["state"].is_file():
        previous = load_json(context["state"])
        prior_history = list(previous.get("package_history", []))
        if previous.get("current_package"):
            prior_history.append(previous["current_package"])
    session = {
        "session_version": "1.0.0",
        "workspace_root": str(context["workspace"]),
        "target_root": str(context["target"]),
        "diagnosis_root": str(context["diagnosis"]),
        "operations_root": str(context["operations"]),
        "current_package": str(package),
        "package_history": prior_history,
        "excluded_tool_directories": excluded_tools,
    }
    write_json(context["state"], session)
    return {"started": True, "system_name": system_name, "package": str(package), "excluded_tool_directories": excluded_tools, "state_file": str(context["state"]), "next_action": "read reports/readiness-report.html and select the Golden Work Item"}


def package_status(package: Path, diagnosis: Path, target: Path | None) -> dict[str, Any]:
    manifest = load_json(package / "manifest.json")
    signoff = load_json(package / "approvals" / "signoff.json")
    golden = load_json(package / "proposals" / "golden-work-item.json")
    verify_command = [sys.executable, str(diagnosis / "diagnose.py"), "verify-source", "--package", str(package)]
    if target:
        verify_command.extend(["--target", str(target)])
    source_process = run(verify_command, {0, 3})
    source = json.loads(source_process.stdout)
    state = signoff.get("state", "UNKNOWN")
    next_by_state = {
        "DRAFT": "set Golden Work Item, then advance to SCANNER_VALIDATED",
        "SCANNER_VALIDATED": "advance to OWNER_REVIEWED after owner review",
        "OWNER_REVIEWED": "advance to SECURITY_REVIEWED after security review",
        "SECURITY_REVIEWED": "advance to ONBOARDING_APPROVED after onboarding approval",
        "ONBOARDING_APPROVED": "run import",
    }
    return {
        "package": str(package), "scan_id": manifest["scan_id"], "system": manifest["system"],
        "signoff_state": state, "golden_work_item": golden, "source_verification": source,
        "import_allowed": load_json(package / "handoff" / "bootstrap-import.json").get("import_allowed", False),
        "next_action": next_by_state.get(state, "inspect package state"),
    }


def command_status(args: argparse.Namespace) -> dict[str, Any]:
    context = resolve_context(args, require_package=True)
    return package_status(context["package"], context["diagnosis"], context["target"] if args.target else None)


def command_golden(args: argparse.Namespace) -> dict[str, Any]:
    context = resolve_context(args, require_package=True)
    command = [
        sys.executable, str(context["diagnosis"] / "diagnose.py"), "set-golden",
        "--package", str(context["package"]), "--id", args.id, "--title", args.title,
        "--evidence-path", args.evidence_path, "--actor", args.actor,
    ]
    for criterion in args.criterion:
        command.extend(["--criterion", criterion])
    run(command)
    return command_status(args)


def command_signoff(args: argparse.Namespace) -> dict[str, Any]:
    context = resolve_context(args, require_package=True)
    run([
        sys.executable, str(context["diagnosis"] / "diagnose.py"), "signoff",
        "--package", str(context["package"]), "--state", args.state,
        "--actor", args.actor, "--role", args.role, "--evidence", args.evidence,
    ])
    return command_status(args)


def command_import(args: argparse.Namespace) -> dict[str, Any]:
    context = resolve_context(args, require_package=True)
    command = [
        sys.executable, str(context["operations"] / "bootstrap" / "bootstrap_import.py"), "import-package",
        "--package", str(context["package"]), "--diagnosis-root", str(context["diagnosis"]),
        "--operations-root", str(context["operations"]),
    ]
    if args.target:
        command.extend(["--target", str(context["target"])])
    process = run(command)
    result = json.loads(process.stdout)
    state = load_json(context["state"]) if context["state"].is_file() else {}
    state["last_import_receipt"] = str(context["operations"] / "import-receipts" / f"{result['scan_id']}.json")
    write_json(context["state"], state)
    return result


def common_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--operations-root")
    common.add_argument("--diagnosis-root")
    common.add_argument("--workspace-root")
    common.add_argument("--state-file")
    common.add_argument("--target")
    common.add_argument("--package")
    return common


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Portable workspace onboarding orchestrator")
    sub = root.add_subparsers(dest="command", required=True)
    common = common_parser()
    sub.add_parser("doctor", parents=[common], help="discover both folders and check the environment")
    start = sub.add_parser("start", parents=[common], help="scan the workspace and create a Draft package")
    start.add_argument("--system-name")
    sub.add_parser("status", parents=[common], help="show the current package and next gate")
    golden = sub.add_parser("golden", parents=[common], help="select the Golden Work Item")
    golden.add_argument("--id", required=True)
    golden.add_argument("--title", required=True)
    golden.add_argument("--evidence-path", required=True)
    golden.add_argument("--criterion", action="append", required=True)
    golden.add_argument("--actor", required=True)
    signoff = sub.add_parser("signoff", parents=[common], help="advance one approval state")
    signoff.add_argument("--state", required=True, choices=["SCANNER_VALIDATED", "OWNER_REVIEWED", "SECURITY_REVIEWED", "ONBOARDING_APPROVED"])
    signoff.add_argument("--actor", required=True)
    signoff.add_argument("--role", required=True, choices=["scanner-operator", "system-owner", "security-reviewer", "onboarding-approver"])
    signoff.add_argument("--evidence", required=True)
    sub.add_parser("import", parents=[common], help="import the approved current package")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    actions = {"doctor": command_doctor, "start": command_start, "status": command_status, "golden": command_golden, "signoff": command_signoff, "import": command_import}
    try:
        result = actions[args.command](args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
