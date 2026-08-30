# 導入前診断 Agent Instructions

このFolderは対象Systemを読取専用で診断し、Versioned Onboarding Packageを生成します。

## 必須Rule

- 検出したScript、Skill、Agent、CI、Terraformを自動実行しない。
- 診断対象へ書き込まない。生成物はこのFolderの`runs/`だけに置く。
- Workspace内にこのFolderと運用保守Folderが置かれている場合、両Tool Folderを診断対象から除外する。
- 自由記述Reportだけを引き継がず、Schema、Manifest、Checksum、Sign-offを含むPackageを使用する。
- Actor、承認Evidence、Golden Work Itemを推測しない。利用者から得られない場合は該当Gateで停止する。
- `ONBOARDING_APPROVED`前にImportを試みない。

## Workspace導入時

兄弟の運用保守Folderに`workspace_onboard.py`がある場合は、個別Scriptより先にその`doctor`と`start`を使う。詳細は運用保守Folderの`START_HERE.md`を読む。
