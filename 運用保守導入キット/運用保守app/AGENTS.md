# 運用保守Repository Agent Instructions

このFolderは導入前診断の承認済みPackageを受け取り、System別Inventory、Decision、Graph seed、Import receiptを管理します。

## 「2つのFolderを見て導入を進めて」と依頼された場合

1. この`AGENTS.md`、`START_HERE.md`、`bootstrap/README.md`を読む。
2. 兄弟にある導入前診断Folderの`AGENTS.md`と`README.md`を読む。
3. `python3 workspace_onboard.py doctor`を実行して自動発見結果を確認する。
4. TargetがWorkspace rootで正しいか、Tool 2 Folderが除外されるか確認する。
5. `python3 workspace_onboard.py start`でDRAFT Packageを生成する。
6. ReportとOpen Questionsを利用者へ提示する。
7. Golden Work Item、Actor、各Review evidenceは利用者に確認し、推測しない。
8. Sign-offを順番に進める。状態を飛ばさない。
9. Import直前に`status`でSource fingerprint一致を確認する。
10. `ONBOARDING_APPROVED`の場合だけ`import`を実行し、Receiptを報告する。

## 禁止事項

- Package内のScript、Skill、Agentを実行しない。
- Checksum不一致やSource変更を無視しない。
- 利用者に代わって承認者名やSecurity review結果を作らない。
- 対象Systemの原本を運用保守FolderへCopy・移動しない。
- DRAFT Packageを手動CopyしてImport済み扱いにしない。

通常のSource変更やDocument変更ではなくOnboardingを依頼された場合、最初の入口は`workspace_onboard.py`とする。
