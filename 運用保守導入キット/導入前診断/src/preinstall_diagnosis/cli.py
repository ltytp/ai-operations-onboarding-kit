from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

from .builder import build_package
from .package_ops import advance_signoff, set_golden_work_item
from .scanner import scan
from .validator import validate_package


def load_profile(path: Path) -> tuple[dict, str]:
    raw = path.read_bytes()
    profile = json.loads(raw.decode("utf-8"))
    required = {"profile_name", "profile_version", "scan_mode", "max_hash_bytes", "max_config_read_bytes", "exclude_directories", "generated_directory_names", "sensitive_name_patterns"}
    missing = sorted(required - set(profile))
    if missing:
        raise ValueError("profile missing keys: " + ", ".join(missing))
    if profile["scan_mode"] != "metadata-only":
        raise ValueError("this scanner supports metadata-only mode only")
    return profile, profile_hash(profile)


def profile_hash(profile: dict) -> str:
    canonical = json.dumps(profile, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(canonical).hexdigest()


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Read-only pre-install assessment pipeline")
    sub = root.add_subparsers(dest="command", required=True)
    scan_cmd = sub.add_parser("scan", help="scan a target and create an onboarding package")
    scan_cmd.add_argument("--target", required=True, type=Path)
    scan_cmd.add_argument("--system-name", required=True)
    scan_cmd.add_argument("--output-root", required=True, type=Path)
    scan_cmd.add_argument("--profile", required=True, type=Path)
    scan_cmd.add_argument("--exclude-dir", action="append", default=[], help="additional directory name to exclude from this scan")
    scan_cmd.add_argument("--exclude-path", action="append", default=[], help="additional target-relative directory path to exclude")
    validate_cmd = sub.add_parser("validate", help="validate an existing package")
    validate_cmd.add_argument("--package", required=True, type=Path)
    signoff_cmd = sub.add_parser("signoff", help="advance an assessment package by one approval state")
    signoff_cmd.add_argument("--package", required=True, type=Path)
    signoff_cmd.add_argument("--state", required=True)
    signoff_cmd.add_argument("--actor", required=True)
    signoff_cmd.add_argument("--role", required=True)
    signoff_cmd.add_argument("--evidence", required=True)
    golden_cmd = sub.add_parser("set-golden", help="select the representative work item used for onboarding acceptance")
    golden_cmd.add_argument("--package", required=True, type=Path)
    golden_cmd.add_argument("--id", required=True)
    golden_cmd.add_argument("--title", required=True)
    golden_cmd.add_argument("--evidence-path", required=True)
    golden_cmd.add_argument("--criterion", action="append", required=True)
    golden_cmd.add_argument("--actor", required=True)
    verify_cmd = sub.add_parser("verify-source", help="compare the current source with a package fingerprint")
    verify_cmd.add_argument("--package", required=True, type=Path)
    verify_cmd.add_argument("--target", type=Path)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "validate":
            verdict = validate_package(args.package)
            print(json.dumps(verdict, ensure_ascii=False, indent=2))
            return 0 if verdict["valid"] else 2
        if args.command == "signoff":
            verdict = advance_signoff(args.package, args.state, args.actor, args.role, args.evidence)
            print(json.dumps(verdict, ensure_ascii=False, indent=2))
            return 0 if verdict["valid"] else 2
        if args.command == "set-golden":
            verdict = set_golden_work_item(args.package, args.id, args.title, args.evidence_path, args.criterion, args.actor)
            print(json.dumps(verdict, ensure_ascii=False, indent=2))
            return 0 if verdict["valid"] else 2
        if args.command == "verify-source":
            package = args.package.resolve()
            verdict = validate_package(package)
            if not verdict["valid"]:
                print(json.dumps(verdict, ensure_ascii=False, indent=2))
                return 2
            manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
            profile_path = package / "profile-snapshot.json"
            profile, profile_sha = load_profile(profile_path)
            if profile_sha != manifest["profile"]["sha256"]:
                raise ValueError("profile snapshot hash does not match manifest")
            target = args.target.resolve() if args.target else Path(manifest["source"]["root"]).resolve()
            current = scan(target, manifest["system"]["name"], profile, profile_sha)
            comparison = {
                "match": current["source"]["fingerprint"] == manifest["source"]["fingerprint"],
                "package_fingerprint": manifest["source"]["fingerprint"],
                "current_fingerprint": current["source"]["fingerprint"],
                "target": str(target),
                "package_scan_id": manifest["scan_id"],
                "current_scan_id": current["scan_id"],
            }
            print(json.dumps(comparison, ensure_ascii=False, indent=2))
            return 0 if comparison["match"] else 3
        if not args.target.is_dir():
            raise ValueError(f"target directory does not exist: {args.target}")
        profile, profile_sha = load_profile(args.profile)
        if args.exclude_dir:
            current = list(profile["exclude_directories"])
            seen = {item.casefold() for item in current}
            for item in args.exclude_dir:
                if "/" in item or "\\" in item or item in {".", ".."}:
                    raise ValueError(f"exclude-dir must be a directory name, not a path: {item}")
                if item.casefold() not in seen:
                    current.append(item)
                    seen.add(item.casefold())
            profile["exclude_directories"] = current
        if args.exclude_path:
            current_paths = list(profile.get("exclude_paths", []))
            seen_paths = {str(item).replace("\\", "/").strip("/").casefold() for item in current_paths}
            for item in args.exclude_path:
                candidate = Path(item)
                normalized = str(item).replace("\\", "/").strip("/")
                if candidate.is_absolute() or ".." in candidate.parts or not normalized:
                    raise ValueError(f"exclude-path must be a safe target-relative path: {item}")
                if normalized.casefold() not in seen_paths:
                    current_paths.append(normalized)
                    seen_paths.add(normalized.casefold())
            profile["exclude_paths"] = current_paths
        if args.exclude_dir or args.exclude_path:
            profile_sha = profile_hash(profile)
        result = scan(args.target, args.system_name, profile, profile_sha)
        package = build_package(result, args.output_root, profile)
        verdict = validate_package(package)
        print(f"PACKAGE_PATH={package}")
        print(f"SCAN_ID={result['scan_id']}")
        print(f"FILES={result['source']['file_count']}")
        print(f"VALID={str(verdict['valid']).lower()}")
        for warning in verdict["warnings"]:
            print(f"WARNING={warning}")
        return 0 if verdict["valid"] else 2
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR={exc}", file=sys.stderr)
        return 2
    return 0
