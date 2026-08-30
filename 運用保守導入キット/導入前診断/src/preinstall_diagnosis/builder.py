from __future__ import annotations

from collections import Counter
from datetime import datetime
from hashlib import sha256
from html import escape
import json
from pathlib import Path
from typing import Any

from . import SCANNER_VERSION, SCHEMA_VERSION


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def markdown_report(result: dict[str, Any]) -> str:
    stats = result["statistics"]
    inv = result["inventory"]
    gates = result["quality_gates"]
    lines = [
        f"# 導入前診断レポート: {result['system']['name']}",
        "",
        f"- Scan ID: `{result['scan_id']}`",
        f"- 実行日時 (UTC): `{result['created_at']}`",
        f"- 対象: `{result['source']['root']}`",
        f"- Source fingerprint: `{result['source']['fingerprint']}`",
        f"- Scanner / Schema / Profile: `{SCANNER_VERSION}` / `{SCHEMA_VERSION}` / `{result['profile']['version']}`",
        "- 動作契約: 読取専用、対象への書込みなし、検出したScript・Skill・Agentの自動実行なし",
        "",
        "## 総括",
        "",
        f"{stats['role_counts'].get('document', 0)}件の文書、{stats['role_counts'].get('source_code', 0)}件のSource code、{stats['role_counts'].get('infrastructure', 0)}件のInfrastructure情報、{len(inv['ai_assets'])}件のAI資産を検出しました。",
        f"提案する初期導入方式は **{result['proposals']['architecture_pattern']}** です。これは承認前の候補であり、既存Repositoryを移動しません。",
        "",
        "## Quality Gates",
        "",
        "| Gate | Status | Evidence |",
        "|---|---|---|",
    ]
    lines.extend(f"| {g['gate']} | {g['status']} | {g['evidence']} |" for g in gates)
    lines.extend([
        "",
        "## Inventory",
        "",
        f"- Files: {result['source']['file_count']}",
        f"- Directories: {result['source']['directory_count']}",
        f"- Total bytes: {stats['total_bytes']}",
        f"- Hash coverage: {stats['hash_coverage_percent']}%",
        f"- Unknown files: {stats['unknown_files']}",
        f"- Duplicate groups: {len(inv['duplicates'])}",
        f"- Generated-artifact candidates: {len(inv['generated_artifacts'])}",
        f"- Sensitive-name findings: {len(result['security']['sensitive_name_findings'])}",
        "",
        "### Role candidates",
        "",
        "| Role | Count |",
        "|---|---:|",
    ])
    lines.extend(f"| {role} | {count} |" for role, count in stats["role_counts"].items())
    lines.extend(["", "### Existing AI assets (detected only)", ""])
    if inv["ai_assets"]:
        lines.extend(f"- `{a['path']}` — {a['type']} / scope: `{a['applies_to']}`" for a in inv["ai_assets"])
    else:
        lines.append("- 検出なし")
    lines.extend(["", "## Open Questions", ""])
    lines.extend(f"- [{q['id']}] {q['question']}（Owner: {q['owner']}）" for q in result["open_questions"])
    lines.extend([
        "",
        "## 合意形成と次の操作",
        "",
        "1. `proposals/`の候補をSystem owner・Operations owner・Security reviewerが確認する。",
        "2. Golden Work Itemを1件選び、期待する調査結果と受入条件を記録する。",
        "3. `approvals/signoff.json`を更新し、Packageを再検証する。",
        "4. `ONBOARDING_APPROVED`後にだけ、`handoff/bootstrap-import.json`を運用保守Repositoryへ渡す。",
        "5. Import直前に再診断し、Source fingerprintの差分があれば承認を取り直す。",
        "",
        "## 制約",
        "",
        "このMVPはMetadata中心です。機密情報の本文検査、意味解析、推定された関係の確定は行いません。分類結果は候補であり、原本・生成物・除外範囲は人が承認します。",
        "",
    ])
    return "\n".join(lines)


def html_report(result: dict[str, Any]) -> str:
    stats = result["statistics"]
    roles = "".join(f"<tr><td>{escape(role)}</td><td>{count}</td></tr>" for role, count in stats["role_counts"].items())
    gates = "".join(
        f"<tr><td>{escape(g['gate'])}</td><td><span class='status {escape(g['status'].lower())}'>{escape(g['status'])}</span></td><td>{escape(g['evidence'])}</td></tr>"
        for g in result["quality_gates"]
    )
    questions = "".join(f"<li><b>{escape(q['id'])}</b> {escape(q['question'])}<small>{escape(q['owner'])}</small></li>" for q in result["open_questions"])
    ai = "".join(f"<li><code>{escape(a['path'])}</code><span>{escape(a['type'])} · scope {escape(a['applies_to'])}</span></li>" for a in result["inventory"]["ai_assets"]) or "<li>検出なし</li>"
    return f"""<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>導入前診断 - {escape(result['system']['name'])}</title>
<style>
:root{{--bg:#f4f7fb;--card:#fff;--ink:#17202a;--muted:#5f6b7a;--line:#dde5ee;--accent:#3157d5;--ok:#16794b;--warn:#a05b00;--pending:#6d4bc3}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font-family:"Segoe UI","Yu Gothic UI",sans-serif}}
header{{padding:42px max(28px,8vw);background:linear-gradient(125deg,#14213d,#3157d5);color:white}} h1{{margin:.2rem 0;font-size:clamp(1.8rem,4vw,3rem)}}
header p{{max-width:900px;line-height:1.7;color:#e6ecff}} main{{max-width:1180px;margin:-22px auto 70px;padding:0 24px}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;box-shadow:0 8px 24px #20305012;margin-bottom:16px}} .metric b{{display:block;font-size:2rem;color:var(--accent)}} .metric span,small{{color:var(--muted)}}
h2{{margin:0 0 16px}} table{{border-collapse:collapse;width:100%}} th,td{{text-align:left;padding:10px;border-bottom:1px solid var(--line)}} code{{overflow-wrap:anywhere}}
.status{{font-weight:700;padding:4px 9px;border-radius:999px;background:#eef1f5}} .pass{{color:var(--ok);background:#e6f6ee}} .review{{color:var(--warn);background:#fff1db}} .pending{{color:var(--pending);background:#f1ebff}}
ul{{padding-left:22px}} li{{margin:.65rem 0}} li span,li small{{display:block;margin-top:4px}} .flow{{display:flex;align-items:center;gap:8px;flex-wrap:wrap}} .step{{padding:10px 14px;border:1px solid var(--line);border-radius:10px;background:white}} .arrow{{color:var(--muted)}}
</style></head><body>
<header><div>PRE-INSTALL ASSESSMENT · {escape(result['scan_id'])}</div><h1>{escape(result['system']['name'])}</h1><p>既存資産を変更せずに、Repository・Document・Code・Infrastructure・AI資産を棚卸しし、合意形成用Packageを生成しました。検出したScript、Skill、Agentは実行していません。</p></header>
<main>
<section class="grid">
 <div class="card metric"><b>{result['source']['file_count']}</b><span>Files</span></div>
 <div class="card metric"><b>{result['source']['directory_count']}</b><span>Directories</span></div>
 <div class="card metric"><b>{stats['hash_coverage_percent']}%</b><span>Hash coverage</span></div>
 <div class="card metric"><b>{len(result['inventory']['ai_assets'])}</b><span>AI assets</span></div>
</section>
<section class="card"><h2>導入判断Flow</h2><div class="flow"><span class="step">Scan</span><span class="arrow">→</span><span class="step">Owner Review</span><span class="arrow">→</span><span class="step">Security Review</span><span class="arrow">→</span><span class="step">Approve</span><span class="arrow">→</span><span class="step">Bootstrap Import</span></div><p>現在は <b>DRAFT</b>。提案方式は <b>{escape(result['proposals']['architecture_pattern'])}</b> です。</p></section>
<section class="card"><h2>Quality Gates</h2><table><thead><tr><th>Gate</th><th>Status</th><th>Evidence</th></tr></thead><tbody>{gates}</tbody></table></section>
<section class="grid"><div class="card"><h2>Role candidates</h2><table><tbody>{roles}</tbody></table></div><div class="card"><h2>Existing AI assets</h2><ul>{ai}</ul></div></section>
<section class="card"><h2>Open Questions</h2><ul>{questions}</ul></section>
<section class="card"><h2>Source identity</h2><p><code>{escape(result['source']['root'])}</code></p><p><small>Fingerprint</small><br><code>{escape(result['source']['fingerprint'])}</code></p><p><small>Scanner / Schema / Profile</small><br>{SCANNER_VERSION} / {SCHEMA_VERSION} / {escape(result['profile']['version'])}</p></section>
</main></body></html>"""


def build_package(result: dict[str, Any], output_root: Path, profile_snapshot: dict[str, Any] | None = None) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    package = output_root.resolve() / f"{result['system']['id']}_{timestamp}_{result['scan_id'][:8]}"
    package.mkdir(parents=True, exist_ok=False)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "scanner_version": SCANNER_VERSION,
        "profile": result["profile"],
        "scan_id": result["scan_id"],
        "created_at": result["created_at"],
        "system": result["system"],
        "source": result["source"],
        "status": "DRAFT",
        "package_contract": {"metadata_only": True, "target_writes": False, "unknown_scripts_executed": False},
    }
    write_json(package / "manifest.json", manifest)
    if profile_snapshot is not None:
        write_json(package / "profile-snapshot.json", profile_snapshot)
    write_json(package / "scope.json", {"included_root": result["source"]["root"], "mode": "recursive", "excluded": result["inventory"]["skipped"], "approval_state": "pending"})
    write_json(package / "source-snapshot.json", {"source": result["source"], "repositories": result["inventory"]["repositories"], "captured_at": result["created_at"]})
    write_json(package / "inventory" / "repositories.json", result["inventory"]["repositories"])
    write_json(package / "inventory" / "directories.json", result["inventory"]["directories"])
    write_json(package / "inventory" / "documents.json", [x for x in result["inventory"]["files"] if x["role_candidate"] == "document"])
    write_json(package / "inventory" / "code.json", [x for x in result["inventory"]["files"] if x["role_candidate"] in {"source_code", "test_code", "build_configuration", "ci_configuration"}])
    write_json(package / "inventory" / "infrastructure.json", [x for x in result["inventory"]["files"] if x["role_candidate"] == "infrastructure"])
    write_json(package / "inventory" / "skills-and-agents.json", result["inventory"]["ai_assets"])
    write_json(package / "inventory" / "generated-artifacts.json", result["inventory"]["generated_artifacts"])
    write_json(package / "inventory" / "unknown.json", [x for x in result["inventory"]["files"] if x["role_candidate"] == "unknown"])
    write_json(package / "inventory" / "duplicates.json", result["inventory"]["duplicates"])
    write_json(package / "inventory" / "all-files.json", result["inventory"]["files"])
    for name in ("source_catalog", "directory_roles", "exclusions", "architecture_pattern", "golden_work_item"):
        value = result["proposals"][name]
        write_json(package / "proposals" / (name.replace("_", "-") + ".json"), value)
    write_json(package / "decisions" / "decision-log.json", {"status": "draft", "decisions": []})
    write_json(package / "decisions" / "open-questions.json", result["open_questions"])
    write_json(package / "decisions" / "missing-knowledge.json", {"items": [{"area": "golden-work-item", "status": "missing"}, {"area": "stakeholder-approval", "status": "missing"}]})
    write_json(package / "approvals" / "signoff.json", {
        "state": "DRAFT",
        "allowed_states": ["DRAFT", "SCANNER_VALIDATED", "OWNER_REVIEWED", "SECURITY_REVIEWED", "ONBOARDING_APPROVED", "IMPORTED", "SUPERSEDED"],
        "reviews": {"system_owner": None, "operations_owner": None, "security_reviewer": None},
        "source_fingerprint": result["source"]["fingerprint"],
    })
    write_json(package / "checks" / "quality-gates.json", result["quality_gates"])
    write_json(package / "checks" / "security-findings.json", result["security"])
    write_text(package / "reports" / "readiness-report.md", markdown_report(result))
    write_text(package / "reports" / "readiness-report.html", html_report(result))
    write_json(package / "handoff" / "bootstrap-import.json", {
        "contract_version": "1.1.0",
        "import_allowed": False,
        "required_signoff_state": "ONBOARDING_APPROVED",
        "scan_id": result["scan_id"],
        "source_fingerprint": result["source"]["fingerprint"],
        "architecture_pattern": result["proposals"]["architecture_pattern"],
        "inventory_paths": ["inventory/repositories.json", "inventory/documents.json", "inventory/code.json", "inventory/infrastructure.json", "inventory/skills-and-agents.json"],
        "pre_import_checks": ["validate-checksums", "compare-source-fingerprint", "verify-signoff-state", "confirm-golden-work-item"],
    })

    checksum_rows = []
    for path in sorted(package.rglob("*"), key=lambda p: p.relative_to(package).as_posix().lower()):
        if path.is_file() and path.name != "checksums.json":
            digest = sha256(path.read_bytes()).hexdigest()
            checksum_rows.append({"path": path.relative_to(package).as_posix(), "sha256": digest, "size_bytes": path.stat().st_size})
    write_json(package / "checksums.json", {"algorithm": "sha256", "files": checksum_rows})
    return package
