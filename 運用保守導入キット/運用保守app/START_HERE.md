# Codespaces / Local Workspace 導入開始

## 推奨配置

Repository / CodespaceのWorkspace rootへ2つのFolderを置きます。Folder名が異なっていてもMarker fileから探索できます。

```text
<workspace-root>/
├─ 既存のSource・Document・Infrastructure
├─ 導入前診断/
│  ├─ AGENTS.md
│  ├─ diagnose.py
│  └─ profiles/default-profile.json
└─ 運用保守app/
   ├─ AGENTS.md
   ├─ START_HERE.md
   ├─ workspace_onboard.py
   └─ bootstrap/
```

2つのTool FolderをWorkspace rootへ置いた場合、診断時に両方を自動除外します。同じ親Folderに`導入準備完了.md`がある場合はその案内Fileも除外します。したがって、診断後にToolが生成したPackageやImport結果によって対象SystemのFingerprintが変化しません。

## 最初の2 Command

Codespaces terminalで運用保守Folderへ移動します。

```bash
cd ./運用保守app
python3 workspace_onboard.py doctor
python3 workspace_onboard.py start
```

またはWrapperを使います。

```bash
bash onboard.sh doctor
bash onboard.sh start
```

Windowsでは次を使用できます。

```powershell
.\onboard.ps1 doctor
.\onboard.ps1 start
```

PathはScript自身の位置から解決します。固定の`C:\Users\...`や`/workspaces/...`は設定しません。

## PromptだけでAgentへ依頼する場合

次のPromptを使用できます。

```text
Workspace直下に「導入前診断」と「運用保守app」を配置しました。
両FolderのAGENTS.md、README.md、START_HERE.mdを読んでください。
最初にworkspace_onboard.py doctorで配置と実行環境を確認し、問題がなければstartで読取専用診断を実行してください。
Tool用の2 Folderは診断対象から除外してください。
診断Report、Open Questions、Golden Work Item候補を説明し、承認者名やReview結果は推測せず、必要なGateで私に確認してください。
ONBOARDING_APPROVEDになるまでImportせず、承認後はSource fingerprintを再照合してBootstrap Importを実行し、Import receiptを報告してください。
```

このPromptなら、絶対Pathを利用者が指定する必要はありません。

## 状態確認

```bash
python3 workspace_onboard.py status
```

現在のPackage、Source照合、Golden Work Item、Sign-off、次に必要な操作を表示します。Session情報は`運用保守app/.onboarding/session.json`に保存されます。

## Golden Work Item

```bash
python3 workspace_onboard.py golden \
  --id CASE-001 \
  --title '代表的な問い合わせ' \
  --evidence-path 'docs/example-case.md' \
  --criterion '根拠資料へ到達できる' \
  --criterion '回答が根拠を引用する' \
  --actor '担当者名'
```

## Sign-off

```bash
python3 workspace_onboard.py signoff \
  --state SCANNER_VALIDATED \
  --actor '担当者名' \
  --role scanner-operator \
  --evidence 'Checksumと診断Reportを確認'
```

状態は`SCANNER_VALIDATED → OWNER_REVIEWED → SECURITY_REVIEWED → ONBOARDING_APPROVED`の順番です。

## Import

```bash
python3 workspace_onboard.py status
python3 workspace_onboard.py import
```

未承認、Checksum不一致、Source変更、重複Scan IDの場合はImport前に停止します。

## 例外的な配置

2つのFolderが兄弟でない場合だけ、次のように指定します。

```bash
python3 workspace_onboard.py doctor \
  --workspace-root /workspaces/example \
  --diagnosis-root /opt/preinstall-diagnosis \
  --operations-root /workspaces/example/operations
```
