# AI Operations Onboarding Kit

既存System Repositoryを読取専用で診断し、Owner/Security reviewを経たVersioned Packageを運用保守領域へ引き継ぐための導入Kitです。

問い合わせ対応、System理解、運用調査、改修見積り、Infrastructure把握などに必要な基礎InventoryとGraph seedを、既存Sourceを移動せずに構築します。

## 主な安全性

- 対象Repositoryへ書き込まないMetadata中心の診断
- 検出したScript、Skill、Agent、CI、Terraformを実行しない
- Package全FileのSHA-256検証
- 診断時とImport直前のSource fingerprint照合
- Golden Work Itemと受入条件の必須化
- 順序付きSign-off
- 未承認Package、Source変更、Checksum不一致、重複Importの拒否

## Repository構造

```text
.
├─ README.md
├─ LICENSE
├─ SECURITY.md
├─ .gitignore
├─ .gitattributes
├─ docs/
│  └─ product-design/
│     ├─ 00_HANDOFF_INDEX.md
│     ├─ 01_BACKGROUND_AND_PROBLEM.md
│     ├─ ...
│     └─ 99_OPEN_QUESTIONS.md
└─ 運用保守導入キット/
   ├─ 導入前診断/
   ├─ 運用保守app/
   └─ 導入準備完了.md
```

`運用保守導入キット/導入準備完了.md`が導入担当者とAgentの開始点です。

## Product design documents

背景、要件、Knowledge Model、Graph、UI、Security、PoC計画などの設計書17種類は、[`docs/product-design/`](docs/product-design/)にあります。

Repository全体のKnowledge整理・可視化を検討するときは、同Folderの[`README.md`](docs/product-design/README.md)を入口にしてください。設計書は設計基準と判断履歴であり、現在実装済みの機能一覧ではありません。

## Requirements

- Python 3.10以上
- Git
- GitHub Codespaces、Linux、macOS、またはWindows PowerShell
- 対象Repositoryの読取権限

追加のPython Packageは必要ありません。

## Codespacesへの導入

対象RepositoryのCodespaces terminalで実行します。

```bash
cd /workspaces/<target-repository>

git clone --depth 1 \
  https://github.com/ltytp/ai-operations-onboarding-kit.git \
  .tools/ai-operations-onboarding-kit
```

Release後は、再現性のため承認済みTagを固定してください。

```bash
git clone --depth 1 \
  --branch <release-tag> \
  https://github.com/ltytp/ai-operations-onboarding-kit.git \
  .tools/ai-operations-onboarding-kit
```

配置確認と診断開始:

```bash
python3 \
  .tools/ai-operations-onboarding-kit/運用保守導入キット/運用保守app/workspace_onboard.py \
  doctor

python3 \
  .tools/ai-operations-onboarding-kit/運用保守導入キット/運用保守app/workspace_onboard.py \
  start
```

Scriptは最も近い`.git`からWorkspace rootを検出します。導入Kit自身と案内Documentは診断対象から相対Path単位で除外されます。

## Agentへ渡すPrompt

```text
Repository内にAI Operations Onboarding KitをCloneしました。
運用保守導入キット/導入準備完了.mdを最初に読み、2つのTool FolderのAGENTS.md、START_HERE.md、README.mdを確認してください。

workspace_onboard.py doctorでGit Workspace、診断Folder、運用保守Folder、Targetを確認し、問題がなければstartで読取専用診断を実行してください。
導入Kitは診断対象から除外してください。

診断Report、Open Questions、Golden Work Item候補を説明してください。承認者名、Review evidence、Security判断は推測せず、必要なGateで私に確認してください。
ONBOARDING_APPROVEDになるまではImportしないでください。
承認後はSource fingerprintを再照合し、Bootstrap Importを実行してImport receiptを報告してください。
```

## Onboarding flow

```text
Doctor
  → Read-only diagnosis
  → Readiness report
  → Golden Work Item
  → SCANNER_VALIDATED
  → OWNER_REVIEWED
  → SECURITY_REVIEWED
  → ONBOARDING_APPROVED
  → Source re-verification
  → Bootstrap Import
  → Inventory / Graph seeds / Import receipt
```

状態確認:

```bash
python3 <path-to-kit>/運用保守app/workspace_onboard.py status
```

承認完了後のImport:

```bash
python3 <path-to-kit>/運用保守app/workspace_onboard.py import
```

## Generated data

診断後はKit内に次のDataが生成されます。

```text
導入前診断/runs/<package>/
運用保守app/.onboarding/session.json
運用保守app/systems/<system-id>/
運用保守app/import-receipts/<scan-id>.json
```

これらは対象RepositoryのFile名、Hash、構造、判断履歴を含む可能性があります。`.gitignore`で除外していますが、Public RepositoryへCommitしないでください。

## Public distribution scope

このRepositoryに含めるもの:

- 診断とBootstrap Importに必要なRuntime
- Versioned Profile / Schema
- Agent向けの安全な実行手順
- 導入Document
- 公開可能性を確認したProduct design Markdown

含めないもの:

- Graph説明HTML
- 顧客固有・未Reviewの内部設計資料
- Test cache
- 過去の診断Package
- System Inventory、Graph seed、Import receipt
- Credential、Secret、顧客固有情報

## License

Licensed under the [MIT License](LICENSE).

## Security

脆弱性報告と公開してはいけないDataについては[SECURITY.md](SECURITY.md)を参照してください。
