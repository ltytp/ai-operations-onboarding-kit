# 作業Repositoryへの導入手順

このDocumentは、実際に調査・可視化したい既存RepositoryへAI Operations Onboarding Kitを導入する手順です。

対象RepositoryのSource、Document、Test、Infrastructure定義を移動せず、最初にRead Only診断を行います。診断後も、人による確認とSign-offが完了するまでBootstrap Importは実行しません。

## 1. 用語

- **対象Repository**: 調査・可視化したい既存SystemのGit Repository
- **Kit Repository**: `ltytp/ai-operations-onboarding-kit`
- **Workspace root**: 対象RepositoryのRoot
- **導入前診断**: 対象を変更せず、Inventoryと診断Packageを作るTool
- **運用保守app**: 診断開始、状態管理、Sign-off、Importを行うRuntime
- **診断Package**: Inventory、Report、提案、承認状態、Checksumを含む中間生成物
- **Golden Work Item**: 導入結果の品質を確認する代表案件

## 2. 前提条件

- Python 3.10以上
- Git
- 対象RepositoryのRead権限
- Kit Repositoryをcloneできること
- Codespaces、Linux、macOS、またはWindows PowerShell

追加のPython Packageは必要ありません。

## 3. 推奨配置

Kitは対象Repositoryの内部ではなく、同じ`/workspaces`配下の兄弟Folderとしてcloneすることを推奨します。

```text
/workspaces/
├─ target-repository/               # 対象Repository
└─ ai-operations-onboarding-kit/    # Kit Repository
```

この配置には次の利点があります。

- 対象RepositoryへTool Folderを作らない
- 対象Repositoryの`git status`を汚さない
- 診断PackageやImport結果を対象Repositoryの外に保持できる
- Kit自身の`.git`と対象Repositoryの`.git`を明確に区別できる

## 4. Codespacesでcloneする

対象RepositoryのCodespaces terminalで、最初に対象Rootを確定します。

```bash
cd /workspaces/<target-repository>
TARGET_ROOT="$(pwd -P)"

cd /workspaces
git clone https://github.com/ltytp/ai-operations-onboarding-kit.git
```

既にclone済みの場合は、再度cloneしないでください。

現在の`main`を使う場合:

```bash
KIT_REPO="/workspaces/ai-operations-onboarding-kit"
```

承認済みRelease tagが公開された後は、再現性のためTagを固定できます。

```bash
cd /workspaces
git clone --branch <release-tag> --depth 1 \
  https://github.com/ltytp/ai-operations-onboarding-kit.git
```

## 5. Pathを設定する

同じterminal sessionで次を実行します。

```bash
KIT_REPO="/workspaces/ai-operations-onboarding-kit"
KIT_ROOT="$KIT_REPO/運用保守導入キット"
DIAGNOSIS_ROOT="$KIT_ROOT/導入前診断"
OPERATIONS_ROOT="$KIT_ROOT/運用保守app"
ONBOARD="$OPERATIONS_ROOT/workspace_onboard.py"
```

Pathを確認します。

```bash
printf 'TARGET_ROOT=%s\nKIT_REPO=%s\n' "$TARGET_ROOT" "$KIT_REPO"
test -d "$TARGET_ROOT/.git"
test -f "$ONBOARD"
test -f "$DIAGNOSIS_ROOT/diagnose.py"
```

いずれかが失敗した場合は、`doctor`へ進まずPathを修正してください。

## 6. 配置診断（doctor）

次のCommandは環境とPathを確認するだけで、対象Repositoryを診断しません。

```bash
python3 "$ONBOARD" doctor \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT"
```

最低限、次を確認します。

- `ready`が`true`
- `target`と`workspace`が対象RepositoryのRoot
- `diagnosis`がKit内の`導入前診断`
- `operations`がKit内の`運用保守app`
- `target_scope`が`PASS`

`target`が`ai-operations-onboarding-kit`を指している場合は進めません。対象RepositoryのPathを`--workspace-root`と`--target`へ指定し直してください。

## 7. Read Only診断（start）

`doctor`が成功したら、同じPathを使って診断します。

```bash
python3 "$ONBOARD" start \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT"
```

必要ならSystem名を明示できます。

```bash
python3 "$ONBOARD" start \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT" \
  --system-name '<system-name>'
```

成功時には`PACKAGE_PATH`、`SCAN_ID`、`FILES`、`VALID`が表示されます。

診断処理は次を行います。

- File、Directory、RepositoryのInventory作成
- Document、Code、Test、Infrastructure、AI関連資産の候補分類
- SHA-256とSource fingerprintの記録
- Readiness Reportの生成
- Open QuestionsとGolden Work Item候補の生成

検出したScript、Skill、Agent、CI、Terraformは実行しません。

## 8. 診断結果を確認する

状態確認:

```bash
python3 "$ONBOARD" status \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT"
```

診断Packageは次に生成されます。

```text
<DIAGNOSIS_ROOT>/runs/<package>/
├─ reports/readiness-report.html
├─ reports/readiness-report.md
├─ inventory/
├─ proposals/
├─ decisions/
├─ approvals/
├─ checks/
├─ handoff/
└─ checksums.json
```

この時点ではまだImportしません。次を人が確認します。

- 診断対象と除外範囲が正しいか
- 機密性のあるFile名・Pathが生成物へ含まれていないか
- Inventoryの候補分類が妥当か
- Open Questionsのうち今決めるものは何か
- Golden Work Itemとして使える実案件があるか

## 9. Golden Work Itemを登録する

実在する代表案件と、確認可能な受入条件を登録します。

```bash
python3 "$ONBOARD" golden \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT" \
  --id 'CASE-001' \
  --title '代表的な問い合わせまたは改修案件' \
  --evidence-path 'docs/evidence/example.md' \
  --criterion '関連するFunctionとSystem Componentを特定できる' \
  --criterion '根拠となるDocumentとCodeを提示できる' \
  --criterion '不明点をMissing Knowledgeとして区別できる' \
  --actor '実際の確認担当者名'
```

Password、Token、個人情報、顧客秘密をCommand引数やGolden Work Itemへ記載しないでください。

## 10. Sign-offを進める

Sign-offは必ず次の順序で行います。

```text
SCANNER_VALIDATED
  → OWNER_REVIEWED
  → SECURITY_REVIEWED
  → ONBOARDING_APPROVED
```

最初の例:

```bash
python3 "$ONBOARD" signoff \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT" \
  --state SCANNER_VALIDATED \
  --actor '実際の確認担当者名' \
  --role scanner-operator \
  --evidence 'Checksumと診断Reportを確認'
```

後続Stateで必要なRole:

| State | Role |
|---|---|
| `SCANNER_VALIDATED` | `scanner-operator` |
| `OWNER_REVIEWED` | `system-owner` |
| `SECURITY_REVIEWED` | `security-reviewer` |
| `ONBOARDING_APPROVED` | `onboarding-approver` |

`actor`やReview結果をAgentに推測させないでください。各段階で実際の担当者が内容を確認します。

## 11. Bootstrap Import

`status`で次を確認します。

- Sign-offが`ONBOARDING_APPROVED`
- Golden Work Itemが登録済み
- Source fingerprintが診断時と一致
- Package checksumが一致

確認後に実行します。

```bash
python3 "$ONBOARD" import \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT"
```

Import後は次がKit側へ生成されます。

```text
<OPERATIONS_ROOT>/systems/<system-id>/
├─ config/
├─ onboarding/packages/<scan-id>/
├─ inventory/
├─ decisions/
└─ graph-seeds/

<OPERATIONS_ROOT>/import-receipts/<scan-id>.json
```

対象Repositoryの原本はコピー・移動しません。

## 12. 生成物のSecurity

次の生成物には、対象RepositoryのFile名、Path、Hash、構造、判断履歴が含まれる可能性があります。

- `導入前診断/runs/`
- `運用保守app/.onboarding/`
- `運用保守app/.import-staging/`
- `運用保守app/systems/`
- `運用保守app/import-receipts/`

これらはKit Repositoryの`.gitignore`で除外されていますが、Public Repository、Issue、Chat、メールへそのまま添付しないでください。中間生成物は自動的に機密情報をマスクしません。

## 13. 既に対象Repository内へcloneした場合

次の配置でも利用できます。

```text
target-repository/
└─ ai-operations-onboarding-kit/
```

ただしKit自身にも`.git`があるため、自動検出に任せず必ず対象Rootを明示します。

```bash
cd /workspaces/<target-repository>
TARGET_ROOT="$(pwd -P)"
KIT_REPO="$TARGET_ROOT/ai-operations-onboarding-kit"
KIT_ROOT="$KIT_REPO/運用保守導入キット"
DIAGNOSIS_ROOT="$KIT_ROOT/導入前診断"
OPERATIONS_ROOT="$KIT_ROOT/運用保守app"
ONBOARD="$OPERATIONS_ROOT/workspace_onboard.py"

python3 "$ONBOARD" doctor \
  --workspace-root "$TARGET_ROOT" \
  --target "$TARGET_ROOT" \
  --diagnosis-root "$DIAGNOSIS_ROOT" \
  --operations-root "$OPERATIONS_ROOT"
```

対象Repositoryの`git status`にはKit Folderが未追跡として表示されます。対象RepositoryへKitをcommitしない運用なら、Repositoryの共有`.gitignore`を変更せず、必要に応じてローカルの`.git/info/exclude`で除外してください。

`git clone <url> .`で、既存の対象Repository RootへKitを直接展開しないでください。

## 14. Kitを更新する

作業前に状態を確認します。

```bash
git -C "$KIT_REPO" status --short --branch
git -C "$KIT_REPO" pull --ff-only
```

診断途中でKit Versionを変更すると再現性が失われます。進行中の診断・承認・Importを完了するか破棄してから更新してください。

## 15. Agentへ渡すPrompt

```text
対象RepositoryとAI Operations Onboarding Kitを別Folderとして配置しました。
最初にKitのREADME.md、docs/WORKSPACE_INSTALLATION.md、
運用保守導入キット/導入準備完了.md、両Tool FolderのAGENTS.mdとSTART_HERE.mdを読んでください。

対象Repository Root、Kit Root、導入前診断Root、運用保守app Rootを明示し、
workspace_onboard.py doctorでtargetが対象Repositoryを指すことを確認してください。
問題がなければstartでRead Only診断を実行してください。

診断Report、Open Questions、Golden Work Item候補を説明してください。
承認者名、Review evidence、Security判断は推測せず、必要なGateで私に確認してください。
ONBOARDING_APPROVEDになるまでImportしないでください。
```

## 16. よくある停止理由

- `ready: false`: Path、Python、対象Scopeのいずれかが不正
- `target`がKitを指す: `--workspace-root`と`--target`を対象Repositoryへ変更
- 診断Folderが見つからない: `--diagnosis-root`を明示
- `package is not ONBOARDING_APPROVED`: Sign-offが未完了
- `source fingerprint mismatch`: 診断後に対象が変更されたため、再診断と再承認が必要
- `checksum mismatch`: Packageが変更されたため、内容を調査して再生成が必要
- `scan_id is already imported`: 同じ診断Packageを重複Importしようとしている

Guardを無効化して進めず、停止理由を解消してから再実行してください。
