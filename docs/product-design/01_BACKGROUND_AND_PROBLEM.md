# AI-Ready Operations Repository / Codex App
## 01. Background and Problem Definition

**Document:** `01_BACKGROUND_AND_PROBLEM.md`  
**Status:** Draft  
**Document Role:** Background / Problem Definition  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、AI-Readyな運用保守RepositoryおよびCodex AppのPoCを検討するに至った背景と、現在解決したい問題を整理するためのものである。

本ドキュメントでは、

> なぜこの仕組みが必要なのか

を明確にすることを主目的とする。

そのため、以下のような具体的な技術方式は本ドキュメントでは確定しない。

- Repositoryの最終Directory構成
- Graph Databaseの採用有無
- SQLite / Neo4j等のStorage選定
- Semanticaの採用範囲
- Agent Framework
- AI-Readyファイル形式
- Document Parserの実装方式
- UI Framework
- Vector Databaseの利用有無

これらは後続の要件・設計ドキュメントで検討する。

---

# 2. 現在の業務背景

対象は、すでに稼働しているシステムの運用保守である。

運用保守では、日常的に以下のような作業が発生する。

- 顧客・利用者からの問い合わせ対応
- システム仕様確認
- 不具合調査
- データ調査
- Source Code調査
- テスト
- リリース対応
- 手順書作成
- リリース資料作成
- 顧客説明資料作成
- 定例会資料作成
- 追加改修検討
- 責任範囲確認

単にシステムが動作しているかを確認するだけではなく、

> 現在なぜこの動作になっているのか

を説明できることが重要な業務となっている。

---

# 3. 現在感じている中心的な問題

現在の運用保守では、システムの開発当時の背景・要件・設計上の判断・顧客との合意内容を十分に把握できていない状態で、問い合わせや調査を行う必要がある。

そのため、問い合わせが発生した際に、

- どこから確認を始めるべきか
- どこまで調査すべきか
- 何が現行仕様なのか
- 現在の挙動が正常なのか
- 実装上のバグなのか
- 開発時の仕様漏れなのか
- 顧客との合意済み仕様なのか
- 追加要望として扱うべきなのか
- 誰の責任範囲なのか

を判断することが難しい。

情報が全く存在しないというより、

> 必要な情報が複数の場所・資料・コード・履歴に分散し、それぞれの関係が明示されていない

ことが大きな問題となっている。

---

# 4. 問い合わせ対応の実態

問い合わせ対応では、単純に技術的な原因を調査して終わるわけではない。

大きな業務プロセスとしては、以下のようになる。

```text id="vhwwna"
問い合わせ受信
    ↓
発生事象・期待動作の確認
    ↓
原因調査
    ↓
現行仕様・開発時の合意内容との照合
    ↓
バグ / 仕様 / 責任範囲の整理
    ↓
利用者・顧客への説明
```

この中で、

- API
- Batch
- Database
- Table
- File
- Source Code
- SQL

などは、主に原因調査時に確認する技術的な範囲である。

一方、

- 要件定義
- 設計資料
- テスト項目書
- 過去問い合わせ
- 議事録
- QA
- 改修履歴

などは、原因・仕様・開発時の合意内容を評価するためのEvidenceとなる。

これらを問い合わせ対応の工程そのものと同列に扱わず、

> 業務プロセス

と

> その工程で利用する調査対象・Evidence

を分けて考える必要がある。

---

# 5. 発生事象・期待動作の確認

問い合わせを受けた直後は、まず、

> 利用者に実際に何が起きたのか

を整理する必要がある。

問い合わせ文だけでは、

- 実際の事象
- 利用者が期待していた動作
- 対象となる業務
- 対象機能
- 発生条件

が明確でない場合がある。

現在は必要に応じて、

- Codex
- Repository内の関連資料
- NotebookLM
- Source Code
- データ

などを使って確認を行っている。

この段階の目的は原因を確定することではなく、

- 何が起きたか
- 何が期待されていたか
- どの業務・機能に関係するか
- どこから原因調査を開始するか

を整理することである。

---

# 6. 原因調査

次に、

> なぜその事象が発生したのか

を技術的に調査する。

確認範囲は問い合わせによって異なる。

例えば、

- Screen
- API
- Batch
- Database
- Table
- File
- Source Code
- SQL
- Configuration
- Data
- External System

などを確認する場合がある。

例えば、画面に対象データが表示されない場合でも、

```text id="xuipgw"
画面条件
→ API
→ SQL
→ Database
```

までで原因へ到達する場合もあれば、

```text id="mhz2ar"
入力File
→ Batch
→ Database
→ 集計処理
→ API
→ 画面
```

まで追跡する必要がある場合もある。

現在の問題は、

> 今回の問い合わせでは、どの範囲をどこまで確認すれば十分なのか

を担当者自身が毎回判断しなければならないことである。

---

# 7. 原因と現行仕様の照合

技術的な原因が判明しても、それだけでは問い合わせ対応は完了しない。

次に、

> その原因・挙動が現行仕様として正しいものなのか

を確認する必要がある。

例えば、同じ「期待した結果にならない」という事象でも、

- 現行仕様どおりの動作
- 実装上のバグ
- 開発時に漏れていた仕様
- 開発時に想定されていなかったケース
- 顧客と合意済みの制約
- 過去の追加要望による仕様
- 開発側のSE対応・個別対応によって発生した不具合
- 新たな追加要望

など、背景が異なる。

そのため、

```text id="9jkyvm"
発生事象
+
技術的原因
+
現行仕様
+
開発時の設計内容
+
当時の合意内容
```

を照合する必要がある。

---

# 8. 開発時の設計打ち合わせ・議事録の確認

過去の議事録等は、現時点では主にNotebookLM側で管理・参照している。

議事録を確認する主な目的は、

> 開発当時、顧客側と開発側の間でどのような設計上の話し合い・合意が行われていたかを確認し、今回発生した事象の責任範囲を整理すること

である。

例えば、

```text id="lz0xs2"
当時の顧客要望
↓
設計打ち合わせ
↓
合意された仕様
↓
実際の設計・実装
↓
今回発生した事象
```

を辿る。

その結果、

### 開発時に顧客と合意されていた仕様である

場合は、現在の挙動が仕様どおりであり、新たな要望として扱う可能性がある。

### 顧客から必要条件が提示され、対応が合意されていたにもかかわらず実装されていない

場合は、開発側の不備である可能性がある。

### 必要な観点自体が設計検討から漏れていた

場合は、要件整理・設計責任を含めて評価する必要がある。

このように議事録は単なる仕様資料ではなく、

> 開発当時の合意形成まで遡って、今回事象の責任範囲を評価するための重要なEvidence

として利用している。

ただし、議事録だけを根拠として契約上の責任をAIが自動確定することは目的としていない。

---

# 9. バグ・仕様・責任範囲の整理

技術的原因と過去Evidenceを確認した後、

> 今回事象をどのように扱うべきか

を整理する。

代表的な分類として、以下が考えられる。

- 現行仕様
- 開発側の実装バグ
- 開発時の仕様漏れ
- 新規・追加要望
- 運用起因
- データ起因
- 過去のSE対応・個別対応起因

評価の流れは概ね、

```text id="v59o8c"
発生事象
↓
技術的原因
↓
現行仕様との比較
↓
当時の顧客・開発間の設計合意
↓
実際の設計・実装
↓
責任範囲の評価
```

となる。

この判断には技術情報だけでなく、開発時の背景・合意・Evidenceが必要である。

---

# 10. 利用者・顧客への説明

調査後は、利用者または顧客へ結果を説明する。

回答では必要に応じて、

- 何が起きたのか
- なぜ起きたのか
- 現在の仕様はどうなっているか
- システム上の問題なのか
- 運用上の問題なのか
- 対応が必要か
- 回避方法があるか
- 改修が必要か

を整理する。

説明相手によって必要な粒度は異なる。

実際の利用者には、

- 業務への影響
- 必要な操作
- 回避方法

が重要になる。

一方、顧客側のシステム担当者や管理者には、

- 原因
- 現行仕様
- 過去の合意
- 責任範囲
- 追加改修の必要性

などまで説明する必要がある。

---

# 11. 現在利用しているCodexとNotebookLM

現在も問い合わせ調査にはAIツールを利用している。

例えばCodexでは、

- Repository内のSource Code確認
- 現行実装の確認
- 関連機能の調査
- 再現確認
- データ状態確認

などを支援させている。

一方、過去の設計打ち合わせや議事録等については、NotebookLMを利用して確認している。

現状は、

```text id="b48qg3"
Codex
→ Repository / Code中心

NotebookLM
→ 議事録・過去の設計打ち合わせ中心
```

という形で情報源が分かれている。

そのため、問い合わせ一件の調査でも、

> Code上の原因

と

> 開発当時の設計・合意内容

を担当者自身が複数ツールを横断して結び付ける必要がある。

---

# 12. 対象Repositoryは既存資産を持っている

[DECIDED]

本PoCを適用予定のRepositoryは、完全な新規Repositoryではない。

すでに運用保守で利用されており、一定のフォルダ構成・資料管理方法が存在している。

これまでの認識では、例えば、

- 問い合わせごとの調査結果
- テスト項目書
- Source Code
- 運用保守関連資料

などが存在する。

ただし、**PoC設計時点では対象Repository全体のDirectory構成・格納資料・管理ルールをまだ詳細に確認できていない。**

したがって、現時点の設計案を前提に既存Repositoryを再編することはしない。

---

# 13. 既存Repositoryを踏襲しながらPoCを構築する

[DECIDED]

PoC実装開始時には、まず対象Repositoryを確認する。

確認対象として、少なくとも以下を想定する。

- 現在のDirectory構成
- Directoryごとの目的
- 問い合わせ調査の保存方法
- テスト項目書の保存方法
- 設計資料の保存方法
- Source Codeとの位置関係
- 過去資料と現行資料の区別
- Git上の運用方法
- 人間が現在どのようにRepositoryを利用しているか

その上で、

```text id="06etpm"
Existing Repository
↓
Understand Current Structure
↓
Preserve Useful Structure
↓
Add AI-Ready Capability
```

という順序でPoCを構築する。

AIにとって都合がよいという理由だけで、既存Repositoryを新しいDirectory構造へ強制的に移行しない。

---

# 14. 既存問い合わせ調査は重要な資産である

[PROVISIONAL]

既存Repositoryに保存されている問い合わせごとの調査結果は、本PoCにおいて重要なKnowledge候補となる。

過去問い合わせには、

- 問い合わせ事象
- 調査方法
- 確認したコード
- SQL
- データ確認
- 原因
- 回答案
- 関連テスト
- 修正内容

などが含まれている可能性がある。

これらを将来的に、

```text id="icukf6"
Current Inquiry
↓
Similar Past Inquiry
↓
Past Investigation
↓
Past Cause / Decision
```

として再利用できれば、調査効率を高められる可能性がある。

ただし、既存問い合わせフォルダを新しいCase Modelへどのように対応付けるかは未確定である。

---

# 15. テスト項目書も重要なEvidenceである

[PROVISIONAL]

既存のテスト項目書は単なる補足資料ではなく、

- 期待動作
- 前提条件
- 入力条件
- 出力結果
- 過去に確認された仕様

を示すEvidenceとして利用できる可能性がある。

例えば、

```text id="p3bg91"
Function
↓ TESTED_BY
TestCase
```

のように関連付けることが考えられる。

ただし、

- ExcelのSheet単位
- Test Scenario単位
- Row単位

など、どの粒度でKnowledge化するかは後続設計で検討する。

---

# 16. Repository外にも重要なKnowledgeが存在する

[DECIDED]

運用保守で必要となるKnowledgeが、すべてRepository内に存在するわけではない。

現時点の代表例が、NotebookLMで管理している過去議事録・設計打ち合わせ記録である。

そのため現状は、

```text id="jc9fhm"
Repository Knowledge
+
External Knowledge
```

の両方を利用して問い合わせ調査を行っている。

---

# 17. 議事録等をRepositoryへ一元管理できるかは未確定

[OPEN]

将来的には、Security・組織ルール上問題がなければ、議事録等もRepository内で一元管理したい。

そうすることで、

```text id="6m133b"
Requirement
Design
Test
Meeting
Inquiry
Release
Source Code
```

を同じKnowledge体系の中で関連付けられる可能性がある。

一方、議事録には、

- 顧客情報
- 個人名
- 発言者情報
- メールアドレス
- 契約・責任分界に関する記述
- プロジェクト上のセンシティブな情報

が含まれる可能性がある。

そのため以下について、上司等への確認が必要である。

- Codexから議事録を直接参照してよいか
- 議事録OriginalをRepositoryへ格納してよいか
- Git管理対象としてよいか
- Git履歴に本文や差分を残してよいか
- Masking / Redactionが必要か
- Repositoryのアクセス権限をどこまで制限する必要があるか
- AI-Ready化した派生情報のみ保存すべきか

この確認が完了するまで、議事録のRepository統合方式は確定しない。

---

# 18. 議事録をRepositoryへ格納できない場合も考慮する

[PROVISIONAL]

議事録OriginalをRepositoryへ保存できない場合でも、

- Meeting ID
- Meeting Date
- Topic
- Related Function
- Related Requirement
- Decision Summary
- Source Location
- Access Policy

などのMetadataや許可されたSummaryのみをRepository側へ保持する方式を検討できる。

重要なのは、

> OriginalをRepositoryへ保存できるかどうか

と

> Knowledgeとして関連付けできるかどうか

を別問題として扱うことである。

---

# 19. OriginalとAI-Ready Knowledgeは同一ではない

[DECIDED]

本PoCでは、人間が利用するOriginal DocumentとAI向けKnowledgeを分けて考える。

```text id="n8iabu"
Original
=
Human Source / Evidence
```

```text id="88qc3n"
AI-Ready Knowledge
=
Derived Knowledge
```

AI-Ready化のために、既存のExcel、PowerPoint、Word等をすべてMarkdownへ置き換えることは目的としない。

人間が現在利用している資料を可能な限り維持しながら、AIが探索しやすいKnowledgeを追加する方向を検討する。

---

# 20. AI-Ready Knowledgeは可能な限り再生成可能にする

[DECIDED]

AI向けに生成する、

- Markdown
- Metadata
- Relation
- Graph
- Index
- HTML
- Vector Index

等は、可能な限りOriginalと設定から再生成可能とする。

AI用情報を人間が別途手管理することでOriginalとの乖離が発生することを避ける。

---

# 21. Gitを重要な履歴情報として扱う

[DECIDED]

GitはSource Code管理だけではなく、

- いつ変更されたか
- 何が変更されたか
- どの資料とコードが同時に変更されたか
- どのReleaseに関連するか

を確認するための重要な履歴情報として扱う。

ただし、すべての業務資料をGit管理してよいかは資料種別によって異なるため、Security / Governance上の確認を行う。

---

# 22. AIがRepository全体を覚えることを目標にしない

[DECIDED]

LLMのContextやMemoryへRepository全体を保持することは現実的ではない。

目標は、

> AIがすべてを知っている状態

ではなく、

> 問い合わせに応じて必要な情報へ正しく到達できる状態

である。

そのため、今後の設計では、

- Retrieval
- Relation
- Provenance
- Coverage
- Missing Knowledge

を重要な概念として扱う。

---

# 23. AIが何を確認したのかを人間が確認できる必要がある

現在のAI利用では、回答だけを見ると、

> どの資料まで確認してこの判断をしたのか

が分かりにくい場合がある。

特に責任範囲を含む問い合わせでは、

- Source Codeを確認したか
- テスト項目書を確認したか
- 設計資料を確認したか
- 過去問い合わせを確認したか
- 議事録を確認したか
- 未確認の情報は何か

を人間が把握できることが重要である。

そのため本PoCでは、

```text id="gcm53z"
Sources Checked
Evidence
Sources Not Checked
Coverage
Open Questions
Missing Knowledge
```

などを調査結果とともに確認できる仕組みを検討する。

---

# 24. AIが分からないことも明示できる必要がある

[DECIDED]

必要なEvidenceが存在しない、またはAIから参照できない場合に、推測のみで回答を確定させることは望ましくない。

例えば、

```text id="0rf0kz"
Missing Knowledge:

- 当時の設計打ち合わせ記録を未確認
- 旧版テスト項目書が存在するか不明
```

のように、不足情報を明示する。

本PoCでは、

> AIが何を知っているか

だけではなく、

> AIが何を確認できなかったか

も重要なOutputとして扱う。

---

# 25. 問い合わせ対応を次の問い合わせへ再利用したい

現在の問い合わせ調査では、一度調査した内容が次の問い合わせで十分に再利用されない可能性がある。

本PoCでは、

```text id="xggic6"
Existing Knowledge
↓
Investigation
↓
Cause / Assessment
↓
Answer
↓
New Knowledge
↓
Next Investigation
```

という循環を作ることを目指す。

問い合わせ対応そのものを、

> Repositoryを改善するKnowledge生成活動

として扱える状態が望ましい。

---

# 26. 本PoCで検証したい中心仮説

本PoCでは、

> 運用保守に必要な情報を単なるファイル群として扱うのではなく、業務・仕様・コード・データ・テスト・過去問い合わせ・設計合意などの関係とEvidenceを持つKnowledgeとして整理することで、Codexによる問い合わせ調査の再現性・網羅性・説明可能性を向上できる

という仮説を検証する。

主に以下を確認したい。

1. 問い合わせから必要な調査対象へ辿れるか
2. CodeとDocumentを関連付けられるか
3. 過去問い合わせを再利用できるか
4. 技術的原因と開発時の合意内容を接続できるか
5. Evidence付きで責任範囲の判断材料を整理できるか
6. Missing Knowledgeを明示できるか
7. AIが何を確認したか人間が追跡できるか
8. 既存Repositoryの運用を大きく壊さずにAI-Ready化できるか

---

# 27. 現時点で未確定の重要事項

[OPEN]

以下は後続設計で検討する。

## Existing Repository

- 実際のDirectory構成
- 現在の資料配置
- 問い合わせフォルダの形式
- テスト項目書の形式
- 既存運用ルール

## Repository Integration

- 現行構造をそのまま利用するか
- Overlay構造を追加するか
- 一部のみ整理するか
- Metadataを追加するだけにするか

## Meeting Minutes

- Codex直接参照可否
- Repositoryへの格納可否
- Git管理可否
- Git履歴保持可否
- Masking / Redaction要件

## AI-Ready Knowledge

- Canonical Format
- Metadata Schema
- Relation Schema
- Intermediate Model
- Stable ID

## Graph

- Canonical Relation Model
- Case / Domain / Function / System / Data Flow / Code / Test / Evidence-History View
- Layer間のBridge Relation
- Projection / Filter契約
- Graph Storage方式

## Storage

- JSON
- SQLite
- NetworkX
- Graph Database

## Semantica

- 採用するか
- どの機能まで利用するか

## Agent Architecture

- PoCで必要なAgent
- AgentとSkillの責務
- Codexとの接続方式

---

# 28. この段階では決定しない事項

本Background Documentを根拠に、以下を確定してはならない。

- Neo4jを採用する
- Semanticaを全面採用する
- Vector Databaseを必須とする
- Multi-Agentを必須とする
- 既存Repositoryを全面再編する
- 全Office DocumentをMarkdown化する
- 議事録をGitへ格納する
- 議事録をCodexから直接参照させる
- すべての情報をGraph化する

これらは、対象Repository確認・組織ルール確認・PoC検証を行った上で決定する。

---

# 29. 本PoCの問題定義

現在の運用保守では、

> 必要な情報が存在しないこと

だけが問題ではない。

より大きな問題は、

> 業務・仕様・システム・コード・データ・テスト・問い合わせ・開発時の設計合意・責任範囲に関する情報が分散し、その関係を担当者が毎回頭の中で接続して調査していること

である。

CodexやNotebookLMを利用することで個別の調査は支援できるが、

> 問い合わせ一件について、必要な技術調査・過去Evidence確認・責任範囲整理を一貫して行い、その根拠と未確認事項まで管理する仕組み

はまだ存在していない。

本PoCでは、既存Repositoryの構造・運用を可能な限り踏襲しながら、この調査プロセスを支えるKnowledge構造とCodex利用環境を構築できるかを検証する。

---

# 30. 後続ドキュメントへ引き継ぐ事項

本ドキュメントで定義した背景・問題を基に、後続では以下を具体化する。

```text id="vdb7jw"
02_VISION_AND_GOALS.md
→ この問題に対してどこまで実現するか

03_REQUIREMENTS.md
→ PoCとして何ができればよいか

04_DESIGN_PRINCIPLES.md
→ どの原則を守って設計するか

05_REPOSITORY_ARCHITECTURE.md
→ 既存Repositoryと新しい仕組みをどう共存させるか

06_KNOWLEDGE_MODEL.md
→ どの情報をどのようなKnowledgeとして扱うか

07_GRAPH_AND_CODEGRAPH.md
→ Knowledge間のRelationをどう扱うか

08_DOCUMENT_INGEST_AND_TRANSFORM.md
→ Excel等の既存資料をどうAI-Ready化するか

09_CASE_INVESTIGATION_WORKFLOW.md
→ 問い合わせ調査をどのような工程・状態として管理するか

11_SECURITY_AND_GOVERNANCE.md
→ 議事録、Git、Codex参照、Masking等をどう管理するか
```

---

# 31. このPoCを一文で表した問題意識

> 既存の運用保守RepositoryやNotebookLM等には問い合わせ調査に必要な情報が一定量存在しているが、技術的原因、現行仕様、過去の設計合意、テスト、問い合わせ履歴、責任範囲が体系的に接続されておらず、担当者が複数ツールと資料を横断して毎回手作業で判断しているため、その調査をCodexで再現可能・追跡可能・EvidenceベースにできるRepositoryと仕組みを構築したい。

## 31.1 2026-08-30 Problem Scope Refinement

[DECIDED]

問題は問い合わせ回答だけではない。同じ分散Knowledgeを、システム構造の理解、運用手順の確認、障害調査、追加改修の影響分析・見積り、案件関係者・承認者の把握、Knowledge整備にも再利用できないことが本質である。また、目的ごとに別管理するとContextが分断され、File分類や複雑なMasking運用を利用者へ求めると利用継続が難しくなる。したがってWork Itemと可変Objective、共通Relation Model、単純な承認済みData境界を前提に解く。

## 31.2 Graph理解上の追加課題（2026-08-30）

[DECIDED]

現行資料では、Function（提供Capability）とSystem（実現・稼働する技術境界）が混同されやすく、Terraform等に記述されたInfrastructure ResourceとSystemの対応も辿りにくい。また、個別Graphを平面表示するだけでは、問い合わせからFunction、System / Infrastructure、Code / Data Flow / Test、Evidenceへ下る意味階層が伝わりにくい。これを、Function / System分離、Infrastructure / IaC Graph、平面ProjectionとVertical Stackの併用で解決する。
