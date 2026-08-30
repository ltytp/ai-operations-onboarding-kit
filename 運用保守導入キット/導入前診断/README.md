# 導入前診断Pipeline

既存Systemへ運用保守Repositoryを導入する前に、Document・Code・Infrastructure・既存Skill/Agent・生成物候補を読取専用で棚卸しし、合意形成とBootstrap Importに使うVersioned Packageを作ります。

Codespacesで2つのTool FolderをWorkspaceへ置く場合は、兄弟の運用保守Folderにある`START_HERE.md`と`workspace_onboard.py`を最初の入口にしてください。ScriptがWorkspace、診断Folder、運用保守Folderを自動発見し、固定Pathを要求しません。

## 安全性の境界

- 診断対象へは書き込みません。出力先はこのFolderの`runs/`です。
- 検出したScript、Skill、Agent、CI、Terraformは実行しません。
- DefaultはMetadata-onlyです。既知の`AGENTS.md`と`SKILL.md`は見出し・限定Metadataだけを読みます。
- Symlink / Reparse pointは追跡しません。
- `.git`、Dependency、Build cache等はProfileで除外し、除外した事実をPackageへ記録します。
- 機密らしいFile名は本文を読まずにReview対象として記録します。秘密情報の本文Scanは別工程です。

## 1. 診断を実行

PowerShellで次を実行します。

```powershell
Set-Location -LiteralPath '<導入前診断Folder>'
.\run-diagnosis.ps1 -TargetPath '<対象System Folder>' -SystemName '対象System名'
```

`PACKAGE_PATH=...`として出たFolderが1回分の不変な診断Packageです。

## 2. ReportをReview

最初に`reports/readiness-report.html`を開き、その後に以下を確認します。

- `scope.json`: 対象範囲と除外
- `inventory/`: Repository、Document、Code、Infrastructure、Skill/Agent、生成物候補
- `proposals/`: Source catalog、Directory role、導入Architecture、Golden Work Item
- `decisions/open-questions.json`: 未確定事項
- `checks/`: Quality GateとSecurity finding

分類はすべてCandidateです。利用者が全Fileを3分類して管理する設計ではありません。OwnerはScope、重要な例外、Golden Work Item、導入可否だけをReviewします。

## 3. Packageを検証

```powershell
.\validate-package.ps1 -PackagePath 'C:\...\runs\package-folder'
```

Checksum不一致、必須File不足、安全性契約違反があると失敗します。`DRAFT`の間はValidでもImport不可というWarningが出ます。

## 4. 合意形成を記録

状態は順序を飛ばせません。

```text
DRAFT
  -> SCANNER_VALIDATED     (scanner-operator)
  -> OWNER_REVIEWED        (system-owner)
  -> SECURITY_REVIEWED     (security-reviewer)
  -> ONBOARDING_APPROVED   (onboarding-approver)
```

`OWNER_REVIEWED`へ進む前に、代表的な問い合わせ・障害・改修をGolden Work Itemとして登録します。

```powershell
.\set-golden-work-item.ps1 `
  -PackagePath 'C:\...\package' `
  -Id 'CASE-001' `
  -Title '代表的な問い合わせ' `
  -EvidencePath 'cases\CASE-001.md' `
  -AcceptanceCriteria @('根拠資料へ到達できる','回答が根拠を引用する') `
  -Actor '担当者名'
```

Golden Work Itemと受入条件がないPackageは`ONBOARDING_APPROVED`にできません。

例:

```powershell
.\advance-signoff.ps1 -PackagePath 'C:\...\package' -State SCANNER_VALIDATED -Actor '担当者名' -Role scanner-operator -Evidence 'ChecksumとReportを確認'
```

各更新はActor、Role、Evidence、時刻を履歴に残し、Manifest、Handoff、Checksumを一括更新します。`ONBOARDING_APPROVED`になった時だけ`handoff/bootstrap-import.json`の`import_allowed`が`true`になります。

## 5. 運用保守Repositoryへ引き継ぐ

導入側は次の4条件を満たす場合だけImportします。

1. Checksum検証成功
2. Sign-offが`ONBOARDING_APPROVED`
3. Import直前のSource fingerprintが承認時と同一
4. Golden Work Itemと受入条件が決定済み

Sourceが変わっていれば旧Packageを`SUPERSEDED`扱いにし、再診断します。自由記述Reportを直接Importせず、`handoff/bootstrap-import.json`とVersioned JSONを契約にすることで、診断者が変わっても同じQuality Gateを通します。

Import前のSource再照合だけを実行する場合:

```powershell
.\verify-source.ps1 -PackagePath 'C:\...\package'
```

承認完了後は、運用保守Repository側で次を実行します。

```powershell
Set-Location -LiteralPath '<運用保守Folder>\bootstrap'
.\preflight-import.ps1 -PackagePath 'C:\...\package'
.\bootstrap-import.ps1 -PackagePath 'C:\...\package'
```

## Package構造

```text
manifest.json / scope.json / source-snapshot.json
inventory/   repositories, directories, documents, code, infrastructure,
             skills-and-agents, generated-artifacts, unknown, duplicates
proposals/   source-catalog, directory-roles, exclusions,
             architecture-pattern, golden-work-item
decisions/   decision-log, open-questions, missing-knowledge
approvals/   signoff
checks/      quality-gates, security-findings
reports/     readiness-report.md, readiness-report.html
handoff/     bootstrap-import.json
checksums.json
```

## Test

```powershell
python -m unittest discover -s .\tests -v
```

Profileは`profiles/default-profile.json`、Machine contractは`schemas/onboarding-package.schema.json`です。Versionを変えずに判定Ruleを変更しないでください。
