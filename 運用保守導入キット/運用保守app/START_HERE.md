# Codespaces / Local Workspace 導入開始

## 推奨配置

対象RepositoryとKit Repositoryを、同じ親Directoryの兄弟Folderとして置く方法を推奨します。

```text
/workspaces/
├─ <target-repository>/
│  └─ 既存のSource・Document・Infrastructure
└─ ai-operations-onboarding-kit/
   └─ 運用保守導入キット/
      ├─ 導入前診断/
      └─ 運用保守app/
```

この配置ではToolと生成物が対象Repositoryの外に置かれるため、対象Repositoryの`git status`やSource fingerprintへ影響しません。

## 最初の2 Command

Codespaces terminalで対象RepositoryとKitのPathを明示します。

```bash
cd /workspaces/<target-repository>
TARGET_ROOT="$(pwd -P)"
KIT_ROOT="/workspaces/ai-operations-onboarding-kit/運用保守導入キット"
DIAGNOSIS_ROOT="$KIT_ROOT/導入前診断"
OPERATIONS_ROOT="$KIT_ROOT/運用保守app"
ONBOARD="$OPERATIONS_ROOT/workspace_onboard.py"

python3 "$ONBOARD" doctor \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT"

python3 "$ONBOARD" start \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT"
```

Wrapperを使う場合も同じ引数を渡します。

```bash
bash "$OPERATIONS_ROOT/onboard.sh" doctor \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT"
```

Windowsでは次を使用できます。

```powershell
$TargetRoot = (Resolve-Path -LiteralPath "C:\path\to\target-repository").Path
$KitRoot = "C:\path\to\ai-operations-onboarding-kit\運用保守導入キット"
$DiagnosisRoot = Join-Path $KitRoot "導入前診断"
$OperationsRoot = Join-Path $KitRoot "運用保守app"

& (Join-Path $OperationsRoot "onboard.ps1") doctor `
  --workspace-root $TargetRoot `
  --target $TargetRoot `
  --diagnosis-root $DiagnosisRoot `
  --operations-root $OperationsRoot
```

Kit自身にも`.git`があるため、cloneして使う場合は自動検出だけに依存せず、対象RepositoryのPathを必ず明示してください。完全な手順はRepository rootの`docs/WORKSPACE_INSTALLATION.md`を参照してください。

## PromptだけでAgentへ依頼する場合

次のPromptを使用できます。

```text
対象RepositoryとAI Operations Onboarding Kitを別Folderとして配置しました。
KitのREADME.md、docs/WORKSPACE_INSTALLATION.md、両Tool FolderのAGENTS.mdとSTART_HERE.mdを読んでください。
対象Repository Root、Kit Root、導入前診断Root、運用保守app Rootを明示してください。
最初にworkspace_onboard.py doctorでtargetが対象Repositoryを指すことを確認し、問題がなければstartで読取専用診断を実行してください。
診断Report、Open Questions、Golden Work Item候補を説明し、承認者名やReview結果は推測せず、必要なGateで私に確認してください。
ONBOARDING_APPROVEDになるまでImportせず、承認後はSource fingerprintを再照合してBootstrap Importを実行し、Import receiptを報告してください。
```

Agentは実際の配置を確認し、対象RepositoryとKit Repositoryを混同しないよう明示的なPathを使用します。

## 状態確認

```bash
python3 "$ONBOARD" status \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT"
```

現在のPackage、Source照合、Golden Work Item、Sign-off、次に必要な操作を表示します。Session情報は`運用保守app/.onboarding/session.json`に保存されます。

## Golden Work Item

```bash
python3 "$ONBOARD" golden \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT" \
  --id CASE-001 \
  --title '代表的な問い合わせ' \
  --evidence-path 'docs/example-case.md' \
  --criterion '根拠資料へ到達できる' \
  --criterion '回答が根拠を引用する' \
  --actor '担当者名'
```

## Sign-off

```bash
python3 "$ONBOARD" signoff \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT" \
  --state SCANNER_VALIDATED \
  --actor '担当者名' \
  --role scanner-operator \
  --evidence 'Checksumと診断Reportを確認'
```

状態は`SCANNER_VALIDATED → OWNER_REVIEWED → SECURITY_REVIEWED → ONBOARDING_APPROVED`の順番です。

## Import

```bash
python3 "$ONBOARD" status \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT"

python3 "$ONBOARD" import \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT"
```

未承認、Checksum不一致、Source変更、重複Scan IDの場合はImport前に停止します。

## 例外的な配置

2つのFolderが兄弟でない場合だけ、次のように指定します。

```bash
python3 "$ONBOARD" doctor \
  --workspace-root /workspaces/example \
  --target /workspaces/example \
  --diagnosis-root /opt/preinstall-diagnosis \
  --operations-root /workspaces/example/operations
```
