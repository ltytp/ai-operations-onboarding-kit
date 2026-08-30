# Bootstrap Importer

`導入前診断`が生成した承認済みOnboarding Packageを、運用保守RepositoryのSystem別領域へ安全に引き継ぎます。Package内のScriptやSkillは実行せず、Versioned JSONをDataとして取り込みます。

CodespacesやFolderを置く場所が固定されない環境では、1階層上の`START_HERE.md`と`workspace_onboard.py`を使用してください。以下の個別Scriptは詳細操作用です。

## 役割分担

```text
対象System Repository
  └─ 読取専用Scan
       ↓
導入前診断/runs/<package>
  └─ Review・Golden Work Item・Sign-off
       ↓
運用保守app/bootstrap/bootstrap-import.ps1
  └─ Preflight・Import・Receipt・Graph seed
```

## Import条件

全条件を満たさない場合は書込み前に停止します。

1. Package Schema / Handoff contractが対応Versionである
2. 全FileがChecksum対象で、SHA-256が一致する
3. ManifestとSign-offが`ONBOARDING_APPROVED`
4. `import_allowed=true`
5. Golden Work Itemと受入条件が確定済み
6. 診断時と現在のSource fingerprintが一致する
7. 同じScan IDが未Importである

## 事前検証

```powershell
Set-Location -LiteralPath '<運用保守Folder>\bootstrap'
.\preflight-import.ps1 -PackagePath '<導入前診断Folder>\runs\<package>'
```

対象Systemが移動した場合は`-TargetPath`で現在位置を指定できます。

## Import

```powershell
.\bootstrap-import.ps1 -PackagePath '<導入前診断Folder>\runs\<package>'
```

Import後は次の構造になります。

```text
運用保守app/
├─ systems/<system-id>/
│  ├─ config/system.json
│  ├─ onboarding/current.json
│  ├─ onboarding/packages/<scan-id>/   # 承認済みPackageの不変Copy
│  ├─ inventory/                       # 現行参照用Inventory
│  ├─ decisions/golden-work-item.json
│  └─ graph-seeds/
│     ├─ nodes.json
│     └─ edges.json
└─ import-receipts/<scan-id>.json
```

`graph-seeds`は確定Graphではありません。System、Repository、Asset候補、Golden Work ItemのObserved/Approvedな関係だけを初期Node・Edgeとして出力します。意味推定は後続のReview対象です。

## 失敗時

- Source fingerprint不一致: Sourceが変わっています。再診断し、再承認します。
- 未承認: Sign-offを順番に進めます。
- Golden Work Item不足: 導入前診断側の`set-golden-work-item.ps1`で設定します。
- Checksum不一致: Packageを編集せず、元の診断から再生成します。
- 既にImport済み: Receiptを確認します。同じScan IDを重複Importしません。

## Test

```powershell
python -m unittest discover -s .\tests -v
```
