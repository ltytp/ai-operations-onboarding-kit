# AI-Ready Operations Repository / Codex App
## 03. Requirements

**File Name:** `03_REQUIREMENTS.md`  
**Status:** Draft  
**Document Role:** Functional / Non-Functional Requirements  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、以下の文書で整理した内容を、PoCおよび将来実装へつなげるための要件として定義する。

- `AI-Ready Operations Repository - Codex App_01_BACKGROUND_AND_PROBLEM.md`
- `AI-Ready Operations Repository - Codex App_02_VISION_AND_GOALS.md`

`01` では「なぜ必要なのか」を定義し、`02` では「どのような状態を目指すのか」を定義した。

本ドキュメントでは、そのVisionを実現するために、

> システムとして何ができる必要があるか

を整理する。

本ドキュメントでは、原則として特定製品・特定Database・特定Frameworkの採用を確定しない。

例えば、

- Neo4j
- SQLite
- Semantica
- NetworkX
- Vector Database
- 特定Agent Framework
- 特定UI Framework

などは要件を満たすための実装候補であり、要件そのものではない。

---

# 2. 要件の扱い

本ドキュメントでは、要件の優先度を以下で表す。

## `[POC-MUST]`

今回のPoCで成立性を確認する必要がある。

## `[POC-SHOULD]`

PoCで可能な範囲まで確認したいが、PoC成立の必須条件ではない。

## `[FUTURE]`

PoC後の拡張対象。

また、設計上の確定状況は以下で表す。

## `[DECIDED]`

現時点で方針として決定している。

## `[PROVISIONAL]`

現時点では有力だが、対象Repository確認やPoC結果によって変更可能性がある。

## `[OPEN]`

未決定。後続設計・組織確認・実Repository確認が必要。

---

# 3. 要件定義上の重要な前提

## 3.1 対象Repositoryは既存Repositoryである

[DECIDED]

本PoCの対象は、新規に作成する空のRepositoryではない。

すでに運用保守で利用されているRepositoryがあり、その中には少なくとも以下のような資産が存在すると認識している。

- Source Code
- 問い合わせごとの調査結果
- テスト項目書
- 運用保守関連資料
- その他既存資料

ただし、**本要件作成時点では対象Repository全体の実構成をまだ詳細に確認していない。**

したがって、本要件では既存Directory名や配置を固定しない。

---

## 3.2 既存Repositoryを理解してから追加構成を決める

[DECIDED]

PoC実装開始時には、対象Repositoryを解析し、

- Directory構成
- Directoryごとの用途
- 問い合わせ管理方法
- テスト項目書の配置
- 設計資料の配置
- Source Code構成
- Git運用
- 過去資料と現行資料の区別
- 現在の人間の運用方法

を確認する必要がある。

その上で、

```text
Existing Repository
        ↓
Understand Current Structure
        ↓
Preserve Useful Structure
        ↓
Add AI-Ready Capability
```

という順序で構築する。

---

## 3.3 問い合わせメールをそのまま調査開始Inputにできること

[DECIDED]

現在の運用では、問い合わせメール本文をそのままCodexへ貼り付けて調査を開始している。

PoCでもこの運用を維持し、

> 人間が事前に専用フォームへ問い合わせ内容を再入力・再構造化しないと調査を開始できない

設計にはしない。

---

## 3.4 Repository外にも重要なEvidenceが存在する

[DECIDED]

過去の仕様検討・設計打ち合わせ・議事録等は、現時点では主にNotebookLMで参照している。

したがって、PoCでは、

```text
Repository Knowledge
+
External Knowledge
```

の両方が存在することを前提にする。

---

## 3.5 議事録のRepository統合可否は未決定

[OPEN]

以下は上司・組織ルール等への確認が必要である。

- Codexが議事録Originalを直接参照してよいか
- 議事録をRepositoryへ格納してよいか
- Git管理してよいか
- Git履歴に本文・差分を残してよいか
- Masking / Redactionが必要か
- Repository権限をどう設定するか

そのため、PoCの基本設計は、

> 議事録がRepository内にある場合と、Repository外にある場合の両方を扱えること

が望ましい。

---

# 4. Primary Use Case

本PoCで最優先するObjectiveは問い合わせ対応である。ただしProduct全体の作業単位を問い合わせ専用のCaseへ固定しない。

基本フローは以下とする。

```text
問い合わせメール受信
        ↓
メール本文をCodexへ入力
        ↓
発生事象・期待動作を整理
        ↓
Repository内の関連情報を調査
        ↓
技術的原因を整理
        ↓
現行仕様と比較
        ↓
必要に応じて過去Evidenceを確認
        ↓
バグ / 仕様 / 責任範囲の判断材料を整理
        ↓
Human Review
        ↓
利用者・顧客向け回答を作成
        ↓
今回の調査結果を再利用可能なKnowledgeとして残す
```

CodexによるRepository調査とNotebookLM等による過去Evidence確認は、必ずしも直列ではない。

必要に応じて並行・往復して実施できることを前提とする。

## 4.1 Product全体のWork Item

[DECIDED]

Product全体では、以下を共通の`Work Item`として扱う。

- Inquiry Investigation
- Incident Investigation
- System Discovery
- Operation Task
- Change Request
- Impact Analysis
- Estimation
- Knowledge Maintenance

`Case`は問い合わせ・障害調査を表すWork Item subtypeまたは既存互換用語として残す。一つのWork ItemはPrimary Objectiveと複数のSecondary Objectiveを持ち、作業途中でObjectiveを追加・切替できる。切替時もEvidence、Sources Checked / Not Checked、Missing Knowledge、選択中のFunction / System / Data / Code、調査結果を保持する。

---

# 5. Functional Requirements

---

# FR-01. Existing Repository Discovery

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

PoC開始時に、既存Repositoryの構造を把握できる必要がある。

少なくとも以下を確認可能にする。

- Directory / File構成
- Source Code領域
- 問い合わせ関連領域
- Test関連領域
- Design / Document関連領域
- Release関連領域
- 既存Config
- Git管理対象
- Git管理対象外
- 既存の命名・配置パターン

## Requirement

AIまたは補助処理は、Repositoryを解析した結果から、

- 現在どのような情報が存在するか
- 各Directoryが何のために使われている可能性が高いか
- 既存運用を維持すべき領域
- AI-Ready化のために不足している領域

を整理できること。

## Constraint

Repository実査前に、新しい標準Directoryへ全面移行することを前提にしてはならない。

---

# FR-02. Repository Structure Assessment

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

既存Repositoryを確認した後、

- そのまま利用する
- Metadataを追加する
- Overlay構造を追加する
- 一部のみ整理する

といった選択肢を比較できること。

PoCでは、既存構造を不必要に破壊しない方式を優先する。

---

# FR-03. Inquiry Intake from Raw Text

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

問い合わせメール本文等の非構造化テキストを、そのまま調査開始Inputとして利用できること。

AIはInputから、可能な範囲で以下を整理する。

- 発生事象
- 利用者の期待動作
- 対象業務候補
- 対象機能候補
- 発生日時・対象日等
- 対象データ
- エラー内容
- 不足している確認情報
- 調査開始候補

入力内容が不足している場合、推測だけで補完せず、不足情報として扱う。

---

# FR-04. Work Item / Investigation Unit

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

問い合わせ、障害、運用作業、変更要求、見積もり、System理解等を共通のWork Itemとして継続管理できること。

論理的には以下の情報を保持できることが望ましい。

- Work Item ID
- Work Item Type
- Primary Objective
- Secondary Objectives
- Inquiry Original
- Summary
- Symptom
- Expected Behavior
- Investigation Status
- Related Functions
- Related Systems
- Related Code
- Related Documents
- Evidence
- Timeline
- Cause
- Assessment
- Open Questions
- Missing Knowledge
- Review Status
- Output

既存Repositoryにすでに問い合わせ単位のフォルダ構造がある場合は、それを活用できることを優先する。

新しい`cases/` Directoryの作成を必須要件とはしない。

既存Repositoryで`Case`という単位を使用している場合、その構造をWork ItemのInquiry / Incident subtypeとして再利用する。

---

# FR-05. Investigation Planning

**Priority:** `[POC-MUST]`  
**Status:** `[PROVISIONAL]`

問い合わせ内容に応じて、

> 何を確認すべきか

の候補を整理できること。

例えば、

- Screen確認
- API確認
- Batch確認
- Database / Table確認
- Source Code確認
- Test確認
- Design確認
- Past Inquiry確認
- Historical Evidence確認

などである。

これは固定Checklistをすべて実行するという意味ではない。

問い合わせ内容に応じて必要な範囲を選択すること。

---

# FR-06. Code Investigation

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

Codexの強みを利用し、Repository内のSource Codeを調査できること。

少なくともPoCでは、

- 関連コード候補の特定
- 処理の流れ
- 条件分岐
- SQL / Query
- Data Access
- Configuration
- Error Handling

等を問い合わせ事象と関連付けて確認できること。

---

# FR-07. Code Relationship Discovery

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

Source Codeについて、全文検索だけでなく、コード間の関係を構造的に利用できることを検討する。

候補となるRelationは、

- Module contains Function
- Class contains Method
- Function CALLS Function
- Module IMPORTS Module
- Component DEPENDS_ON Component

などである。

具体的なCode Graph実装方式は後続設計で決定する。

---

# FR-08. Data Flow Investigation

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

問い合わせによってはCall GraphよりもData Flowが重要になる。

例えば、

```text
Input File
→ Batch
→ Table
→ Aggregation
→ API
→ Screen
```

のような処理経路を追跡できることを検討する。

候補となるEntityは、

- File
- Batch
- API
- Table
- Column
- Report
- External System

Relation候補は、

- READS
- WRITES
- GENERATES
- TRANSFORMS
- SENDS_TO
- RECEIVES_FROM

などである。

---

# FR-09. Current Specification Retrieval

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

技術的原因が判明した後、

> 現在の仕様として正しい動作なのか

を評価するため、関連する現行資料へ到達できること。

対象候補は、

- Design
- Test Specification
- Operation Manual
- Existing Inquiry
- Source Code
- Configuration

など。

「実装がそうなっている」という事実だけを、現行仕様確定の唯一の根拠として扱わない。

---

# FR-10. Test Evidence Retrieval

**Priority:** `[POC-MUST]`  
**Status:** `[PROVISIONAL]`

既存テスト項目書から、問い合わせ事象に関連するTest Evidenceを探索できること。

少なくとも、

- どの機能に関するテストか
- どの条件を確認しているか
- 期待結果
- 実施時期・版
- 現行仕様との関係

を確認できることが望ましい。

Excel等からどの粒度でTestCaseを抽出するかは後続設計で決定する。

---

# FR-11. Historical Evidence Retrieval

**Priority:** `[POC-SHOULD]`  
**Status:** `[OPEN]`

開発当時の仕様・設計打ち合わせ・合意内容を、今回事象の評価Evidenceとして利用できること。

現時点では主にNotebookLMを利用しているため、PoCでは以下のいずれかで成立すればよい。

1. Codexから直接参照可能な形にする
2. 許可されたAI-Ready情報のみRepositoryへ持つ
3. 外部Evidenceとして人間が確認し、その参照・要約をCaseへ関連付ける

どの方式を採用するかはSecurity / Governance判断後に決定する。

---

# FR-12. Multi-Source Knowledge Awareness

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

AIは、

> Repository内だけを確認すれば調査完了

と無条件に判断してはならない。

Repository外に重要なEvidenceが存在する可能性を認識し、

- Repositoryで確認済み
- External Sourceで確認済み
- External Sourceに存在するが未確認
- Source自体が不明

を区別できることが望ましい。

---

# FR-13. Technical Cause Identification

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

調査した技術情報から、

> なぜ事象が発生したのか

を整理できること。

ただし、Technical CauseとResponsibility Assessmentを混同しない。

例：

```text
Technical Cause:
対象レコードが月次集計テーブルへ生成されていない
```

と、

```text
Assessment:
現行仕様どおり / 実装バグ / 仕様漏れ / 追加要望
```

は別情報として扱う。

---

# FR-14. Specification / Bug Classification Support

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

技術的原因とEvidenceをもとに、以下の分類候補を整理できること。

- Current Specification
- Implementation Bug
- Specification Omission
- New / Additional Requirement
- Operation Cause
- Data Cause
- Historical SE / Individual Handling Cause
- Unknown / Insufficient Evidence

AIが分類する場合は、その根拠を併記すること。

---

# FR-15. Responsibility Assessment Support

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

以下を整理し、人間が責任範囲を判断するための材料を提示できること。

```text
Observed Fact
↓
Technical Cause
↓
Current Specification
↓
Historical Design / Agreement
↓
Difference / Deviation
↓
Assessment Material
```

AIのみで契約上・法的な責任を確定してはならない。

---

# FR-16. Evidence-Based Assessment

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

重要な判断には、可能な限りEvidenceを紐付けること。

例えば、

```text
Assessment:
開発時に合意済みの仕様である可能性が高い

Evidence:
- Design document X
- Test item Y
- Meeting record Z
```

のように、判断とEvidenceを分離して保持する。

---

# FR-17. Provenance

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

AI-Ready化されたKnowledgeやEvidenceについて、可能な限りOriginalへ戻れること。

Provenanceとして候補となる情報は、

- Source File
- Repository Path
- Git Commit
- Document Version
- Sheet
- Row / Range
- Page / Slide
- Original URL / External Source
- Transformer Version
- Extraction Date
- Review Status

など。

具体的Schemaは後続設計で決定する。

---

# FR-18. Source Checked / Not Checked Tracking

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

一つの調査について、AIが何を確認したかを記録できること。

例：

```text
Sources Checked
- Source Code
- Current Test Specification
- Past Inquiry #123

Sources Not Checked
- Historical Design Meeting Minutes

Reason
- Original is currently outside Codex-accessible repository
```

これにより、回答だけでなく調査Coverageを人間が確認できるようにする。

---

# FR-19. Missing Knowledge Detection

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

調査に必要な情報が不足している場合、

> 不足していること自体

をOutputできること。

例：

- 過去の設計打ち合わせを未確認
- 該当機能の旧版Designが見つからない
- Test Evidenceが存在するか不明
- 責任判断に必要な合意記録が見つからない

不明点をAI推論で無理に埋めない。

---

# FR-20. Confidence / Knowledge State Separation

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

Knowledgeや判断について、

- Human Verified
- Human Reviewed
- AI Extracted
- AI Inferred
- Needs Review
- Conflicting
- Deprecated
- Unknown

などの状態を区別できることが望ましい。

これにより、

> 資料に書いてある事実

と

> AIが推論した結論

を混同しない。

---

# FR-21. Past Inquiry Search and Reuse

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

既存Repositoryにある過去問い合わせを検索し、現在の問い合わせ調査へ再利用できること。

類似性候補として、

- Same Function
- Same Error
- Same Table
- Same Batch
- Same Business Process
- Same Cause
- Same Stakeholder
- Text Similarity

などが考えられる。

具体的な検索方式は後続設計で決定する。

---

# FR-22. Investigation Result Persistence

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

今回実施した問い合わせ調査について、

- 何を確認したか
- 原因
- Evidence
- 判断材料
- 未確認事項
- Human Review
- 最終回答

を後から再利用できる形で残せること。

既存問い合わせフォルダへ追記するのか、新しい形式へ変換するのかはRepository確認後に決定する。

---

# FR-23. Knowledge Feedback Loop

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

問い合わせ対応後、新たに確認された内容を次回調査へ利用できるKnowledgeとして更新できること。

```text
Existing Knowledge
↓
Investigation
↓
New Fact / Evidence
↓
Human Review
↓
Knowledge Update
↓
Next Inquiry
```

AIの推論を無条件に確定Knowledgeへ昇格させない。

---

# FR-24. AI-Ready Document Conversion

**Priority:** `[POC-MUST]`  
**Status:** `[PROVISIONAL]`

既存Documentのうち、PoCで必要なものについてAIが扱いやすい形へ変換できること。

対象候補：

- Excel
- Word
- PowerPoint
- PDF
- CSV
- Markdown
- Text

ただし、

> Office → Markdown

だけを変換方式として固定しない。

---

# FR-25. Normalized Intermediate Representation

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

異なるDocument形式を共通処理するため、

```text
Original
↓
Parser
↓
Normalized Intermediate Representation
↓
Security / Masking
↓
Knowledge Transformation
```

のような中間表現を設けることを検討する。

具体的Schemaは未決定。

---

# FR-26. Document Type Classification

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

Documentを拡張子だけでなく、業務上のDocument Typeとして分類できることが望ましい。

例：

- Requirement
- Design
- Test Specification
- Meeting
- Inquiry
- Release
- Operation Manual
- Contract / Responsibility Material

同じExcelでも意味が異なるため、物理Formatと業務Document Typeを分離する。

---

# FR-27. Source-to-Derived Mapping

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

Originalから生成したAI-Ready Knowledgeについて、

> どのOriginalから生成されたか

を常に追跡できること。

Originalが変更・移動・削除された場合、Derived側が古い状態のまま残らない仕組みを検討する。

---

# FR-28. Incremental Update

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

Repository全体を毎回再処理するのではなく、Git等を利用して変更された対象だけを再処理できることが望ましい。

候補フロー：

```text
Last Indexed Commit
↓
Git Diff
↓
Added / Modified / Deleted
↓
Reprocess Affected Knowledge
↓
Update Index / Graph
```

PoCでは完全実装を必須としないが、将来実装可能な構造にする。

---

# FR-29. Delete / Move / Rename Handling

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

Original Fileが、

- Delete
- Move
- Rename

された場合に、AI-Ready KnowledgeやIndexが孤立・重複しないこと。

Pathだけに依存しないStable IDの必要性を後続設計で検討する。

---

# FR-30. Git History Utilization

**Priority:** `[POC-SHOULD]`  
**Status:** `[DECIDED]`

Git履歴を、単なるSource Code履歴ではなくKnowledgeの変更履歴として利用できることを検討する。

例えば、

- Design変更
- Test変更
- Source Code変更
- Inquiry更新
- Release変更

が同一Commitで変更された場合、その関係を把握できることが望ましい。

ただしGit管理不可の資料については適用しない。

---

# FR-31. Graph Relation Model

**Priority:** `[POC-SHOULD]`  
**Status:** `[DECIDED]`

Knowledge間の関係を、必要に応じてGraphとして表現できること。

Graphは可視化だけではなく、

> 調査経路を探索するためのRelation Model

として扱う。

1つのCanonical Relation Modelを正本となる論理構造として持ち、少なくとも以下のGraph ViewへProjectionできること。

- Work Item / Case
- Domain / Business
- Function
- System / Architecture
- Infrastructure / IaC
- Data Flow
- Code
- Test
- Evidence / History
- Operation / Runbook
- Stakeholder / Responsibility

各Viewは別々のKnowledge Storeではなく、共通のNode / Edgeを用途別に抽出したProjectionとして扱う。

Viewをまたいで、`Work Item / Objective → Business → Function → System / Infrastructure → Data / Implementation → Test → Evidence / History`を辿れること。

Functionは「業務・利用者へ何を提供するか」、Systemは「そのFunctionをどの技術構成で実現・稼働するか」と定義し、`Function --IMPLEMENTED_BY--> System`等のRelationで接続する。同一Node Typeとして扱わない。

Graph Databaseの採用は要件としない。

---

# FR-32. Work Item-Centered Subgraph

**Priority:** `[POC-SHOULD]`  
**Status:** `[DECIDED]`

Graph全体を常時表示するのではなく、現在のWork ItemとObjectiveに関連するNode / Edgeのみ抽出できることが望ましい。

既定値は`Current Work Item + Current Objective + Current only + Depth 2`とし、利用者が必要な場合にのみ、

- Layer View
- Current / Historical
- Related to current Work Item / Entire project
- Depth 1 / 2 / 3

を切り替えて探索範囲を広げられること。

例：

```text
Inquiry
→ Function
→ API
→ Table
→ Batch
→ Test
→ Design
→ Meeting
```

---

# FR-33. Timeline Construction

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

問い合わせ調査で必要となる複数の時間軸を整理できること。

例：

- Business Date
- Data Creation Time
- File Arrival Time
- Batch Execution Time
- Release Date
- Requirement Decision Date
- Meeting Date
- Inquiry Date
- Investigation Date

Timeを単一のKnowledge Layerとしてではなく、各Knowledgeを横断するDimensionとして扱う。

---

# FR-34. Contradiction Detection

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

複数Evidence間で内容が一致しない場合、その矛盾を検出・提示できることが望ましい。

例：

```text
Design:
月末のみ実行

Current Code:
毎営業日実行
```

AIがどちらかを無条件に正しいものとして扱わず、Conflictとして提示する。

---

# FR-35. Stakeholder-Aware Output

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

同一の調査結果から、説明相手に応じたOutputを作成できること。

## End User

- 発生事象
- 業務影響
- 必要な操作
- 回避方法

## Customer System / Management

- 発生事象
- 原因
- 現行仕様
- 過去の合意
- 責任範囲の判断材料
- 改修要否

## Developer

- Reproduction
- Source Code
- SQL
- Data Flow
- Root Cause
- Impact
- Test Scope

---

# FR-36. Human Review Workflow

**Priority:** `[POC-MUST]`  
**Status:** `[DECIDED]`

以下についてHuman Review可能であること。

- AIが整理した事象
- Technical Cause
- Evidence
- Missing Knowledge
- Responsibility Assessment Material
- Customer Response Draft

特に、責任・契約・費用に関する最終判断はHuman Approvalを必要とする。

---

# FR-37. Review Agent / Review Function

**Priority:** `[FUTURE]`  
**Status:** `[PROVISIONAL]`

将来的には、回答や資料生成前に別のReview処理を行い、

- Evidence不足
- Source未確認
- Contradiction
- 古い仕様参照
- 過剰な責任断定
- Stakeholderに不適切な表現

などを検出できることが望ましい。

Multi-Agent必須とはしない。

---

# FR-38. Repository Navigation Support

**Priority:** `[FUTURE]`  
**Status:** `[PROVISIONAL]`

新しい資料を追加する際に、

> この資料はどこへ置くべきか

をAIへ質問し、

- 推奨Directory
- 推奨File Name
- Related Existing Document
- Metadata候補

を案内できることが望ましい。

ただし、人間を過剰に制約しない。

---

# FR-39. Repository Policy Validation

**Priority:** `[FUTURE]`  
**Status:** `[PROVISIONAL]`

Repository内で、

- 明らかに不適切な配置
- Naming Rule違反
- Current / Historical Document混在
- Missing Metadata

などを警告できることが望ましい。

通常はWarning / Recommendationを中心とする。

Security違反等のみBlockingを検討する。

---

# FR-40. Exception Recording

**Priority:** `[FUTURE]`  
**Status:** `[PROVISIONAL]`

Repository標準から意図的に外れる場合、

- Reason
- Approver
- Date
- Related Commit

などを記録できることが望ましい。

---

# FR-41. Generated Human-Readable Views

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

Repositoryの状態やCase調査結果を、人間が確認しやすいViewとして生成できることが望ましい。

候補：

- HTML Index
- Case Report
- Coverage Report
- Graph View
- Timeline View
- Update Summary

Generated ViewはSource of Truthにしない。

---

# FR-42. Context / Coverage Visualization

**Priority:** `[POC-SHOULD]`  
**Status:** `[PROVISIONAL]`

AIが「覚えている量」ではなく、

> 今回の調査でどのKnowledge Layerを確認したか

を示せることが望ましい。

例：

```text
Business        Checked
Function        Checked
System          Checked
Implementation  Checked
Evidence        Partial
Stakeholder     Checked

Missing:
- Historical design decision
```

---

# FR-43. Agent Execution Record

**Priority:** `[FUTURE]`  
**Status:** `[PROVISIONAL]`

Agent / Skillを利用する場合、実行ごとに、

- Agent / Role
- Task
- Sources Checked
- Result
- Open Questions
- Evidence
- Review Status

などを記録できることが望ましい。

長いSessionでも、

> 何を根拠に実行されたか

を後から確認可能にする。

---

# FR-44. Config-Driven Project Customization

**Priority:** `[POC-SHOULD]`  
**Status:** `[DECIDED]`

Project固有ルールを可能な限りHard Codingしない。

将来的にConfig化する候補は、

- Document Type
- Security Policy（Production / Future）
- Repository Policy
- Stakeholder
- Graph Schema
- Transformer
- Agent Policy

など。

別案件への横展開可能性を残す。

---

# FR-45. Technology Abstraction

**Priority:** `[POC-SHOULD]`  
**Status:** `[DECIDED]`

Domain Modelを特定のKnowledge Graph製品やFrameworkへ直接依存させない。

例えばSemanticaを利用する場合でも、

```text
Maintenance Domain
↓
Adapter
↓
Semantica
```

のように、交換可能な境界を設けることを検討する。

---

# FR-46. Purpose-First Workspace

**Priority:** `[POC-SHOULD]`  
**Status:** `[DECIDED]`

UIはGraph LayerやRepository構造から開始せず、「何をしたいか」を最初に選択できること。Objectiveに応じて、必要な入力、View、Checklist、完了条件、成果物を切り替える。

Objective変更は破壊的なMode変更ではなく、同じWork ItemへObjectiveを追加・切替する操作とする。

---

# FR-47. Operation / Stakeholder / Infrastructure Projection

**Priority:** `[POC-SHOULD]`  
**Status:** `[DECIDED]`

Canonical Relation Modelから、Operation / Runbook、Stakeholder / Responsibility、Infrastructure / IaCのProjectionを生成できること。Infrastructure / IaCはTerraform等の定義、Module、Resource、Network、Compute、Database、IAM、State、Monitoringを対象とし、System / ArchitectureとBridge Relationで接続する。

Technical Cause、System Maintenance、Contract Scope、Approval、Responsibility Assessmentを同一意味として扱わない。責任・契約・費用の最終判断はHuman Reviewを必須とする。

Graph UIは、各Projectionを詳しく読む平面Viewに加え、`Inquiry / Work Item → Objective → Domain / Function → System / Infrastructure → Code / Data Flow / Test → Evidence`を上下に示す縦断Stack Viewを提供できること。これはStorage階層ではなく探索・説明用の意味階層である。

---

# FR-48. Data Registration and Lifecycle

**Priority:** `[POC-SHOULD]`  
**Status:** `[DECIDED]`

最低限、以下のデータ操作を区別して扱えること。

- Uploadして管理領域へ保存
- Existing Repository Fileをコピーせず登録
- External SourceをReferenceとして登録
- Metadata / Relation更新
- Version追加・置換
- Move / Rename追跡
- Work ItemとのLink / Unlink
- Archive / Restore
- Runtime Indexから除外・再構築
- Permanent Delete候補と影響確認

曖昧な単一の`Delete`操作でOriginal、Persistent Knowledge、Human Curated Relation、Runtime Indexを一括削除しない。

---

# FR-49. User Action / Execution / Artifact

**Priority:** `[POC-SHOULD]`  
**Status:** `[DECIDED]`

業務上意味のあるユーザー操作とSystem処理・生成物を、以下の概念で追跡できること。

```text
User --PERFORMED--> UserAction
UserAction --TRIGGERED--> Execution
Execution --CONSUMED--> InputArtifact
Execution --GENERATED--> OutputArtifact
Execution --READS / WRITES--> Data
```

Upload、Execute、Approve、Export、Delete、Reprocess等は追跡対象候補とする。Tab切替、Sort、Graph Zoom等の細かなUI操作はKnowledge Graphへ入れず、必要な場合のみAccess / Audit Logへ記録する。

System生成Fileは本体を無条件に複製せず、Storage Location、Checksum、Generated By、Input、Status、Retention等のMetadata / Referenceを基本とし、調査上重要なものだけHuman Review後にEvidenceへ昇格させる。

---

# 6. Non-Functional Requirements

---

# NFR-01. Traceability

**Priority:** `[POC-MUST]`

重要なAI回答・判断材料からOriginal Evidenceまで追跡できること。

---

# NFR-02. Explainability

**Priority:** `[POC-MUST]`

AIは可能な限り、

- 何を確認したか
- 何を根拠にしたか
- どこから推論したか
- 何が不明か

を説明可能であること。

---

# NFR-03. Human Verifiability

**Priority:** `[POC-MUST]`

AIのOutputを、人間がRepositoryやEvidenceと照合して検証できること。

「AIがそう回答した」という理由だけで判断を確定しない。

---

# NFR-04. Security

**Priority:** `[POC-MUST]`

AIへ提供する情報について、

- Customer Information
- Personal Information
- Credentials
- Production Data
- Contract Information
- Responsibility Information

等の扱いを制御できること。

具体的Security Policyは後続文書で決定する。

---

# NFR-05. Original Access Control

**Priority:** `[POC-MUST]`

AI-Ready情報へのアクセス可否と、Original Documentへのアクセス可否を分けられることが望ましい。

特に議事録等については、OriginalをCodexへ直接渡さず、許可されたSummary / Metadataのみ利用する構成も可能にする。

---

# NFR-06. Git History Safety

**Priority:** `[POC-MUST]`

Gitへ一度保存すると履歴へ残り続ける性質を考慮する。

Security確認前のセンシティブ資料を、PoC都合でGitへ追加しない。

---

# NFR-07. Rebuildability

**Priority:** `[POC-SHOULD]`

AI-Ready Knowledge、Graph、Index等は、可能な限りOriginal + Config + Transformerから再生成できること。

Runtime DBのみを唯一の正本にしない。

---

# NFR-08. Maintainability

**Priority:** `[POC-MUST]`

AI-Ready化を維持するために、人間へ過大な追加作業を要求しない。

理想的には通常のDocument / Code更新から派生情報を更新する。

---

# NFR-09. Existing Workflow Compatibility

**Priority:** `[POC-MUST]`

現在の運用保守業務を大きく変更しない。

特にPoCのために既存問い合わせ・テスト・コード管理を全面移行させない。

---

# NFR-10. Portability

**Priority:** `[POC-SHOULD]`

特定Project専用実装を最小化し、ConfigやSchema差し替えによって他Repositoryへ適用可能な構成を目指す。

---

# NFR-11. Incremental Scalability

**Priority:** `[POC-SHOULD]`

PoCでは小規模な実装を許容するが、Repository拡大時に、

- Incremental Index
- Graph DB
- Vector Search
- External Storage

等へ拡張可能な構造を保つ。

---

# NFR-12. Technology Independence

**Priority:** `[POC-SHOULD]`

PoCで採用した特定技術を、将来交換不能なSource of Truthにしない。

---

# NFR-13. Failure Visibility

**Priority:** `[POC-MUST]`

Document変換・Index生成・Graph生成等に失敗した場合、黙って欠落させない。

少なくとも、

- Failure
- Affected Source
- Reason
- Retry / Review Needed

を確認できること。

---

# NFR-14. Conflict Visibility

**Priority:** `[POC-SHOULD]`

複数Knowledge間に矛盾がある場合、最新情報と推測して自動解決するだけでなく、Conflictとして人間へ提示できること。

---

# NFR-15. Auditability

**Priority:** `[POC-SHOULD]`

重要なKnowledge更新やHuman Reviewについて、

- 誰が
- いつ
- 何を
- 何を根拠に

変更・承認したか確認できることが望ましい。

Git Commitを利用できる範囲では活用する。

---

# 7. PoC Scope

現時点では、PoC Scopeを以下のように考える。

## `[POC-MUST]`

### Existing Repository Understanding

対象Repositoryを実査し、既存構造を把握する。

### One Realistic Inquiry

実運用に近い問い合わせメール一件をInputとする。

### Raw Inquiry → Investigation

メール本文から関連する調査を開始する。

### Code Investigation

関連Source Codeを特定・確認する。

### Existing Document Retrieval

テスト項目書等、Repository内の既存資料を参照する。

### Technical Cause

技術的原因を整理する。

### Current Specification Assessment

現行仕様との整合を整理する。

### Evidence

判断根拠となるSourceを示す。

### Missing Knowledge

確認できなかった情報を示す。

### Human Review

最終判断前に人間が結果を確認する。

### Persistence

今回の調査内容を次回再利用可能な形で残す。

---

# 8. PoC Conditional Scope

以下は、組織確認や対象Repositoryの実態によってPoC Scopeを決定する。

## Meeting Minutes / Historical Agreements

[OPEN]

議事録をCodexから直接確認できるか。

## Git Storage of Meeting Minutes

[OPEN]

議事録をRepository / Gitへ格納可能か。

## AI-Ready Meeting Knowledge

[OPEN]

Originalを格納できない場合、Summary / MetadataをAI-Ready Knowledgeとして保持できるか。

## Code Graph

[PROVISIONAL]

PoC問い合わせで有効性が高い場合、限定範囲で生成する。

## Data Flow Graph

[PROVISIONAL]

PoC問い合わせがデータ処理系の場合、優先度を上げる。

---

# 9. PoC Out of Scope

PoC初期では以下を必須としない。

- 全Repository DocumentのAI-Ready化
- 全Source Codeの完全Graph化
- Neo4j導入
- Vector Database導入
- Semantica全面導入
- Multi-Agent全面実装
- Production Cloud Deployment
- 全案件対応可能な汎用UI
- AIによる責任判断の完全自動化
- AIによる顧客回答の無人送信
- AIによる自動改修・自動Release
- Existing Repositoryの全面再編
- ユーザーによる機密区分の都度分類UI
- Masking / Token Vault / Detokenization
- アプリ内での原本復元表示
- 項目単位の機密情報Access Control

PoC対象データは、事前に組織・管理者がAI利用を承認した範囲に限定する。許可されていない資料を取り込み、PoC内で分類・Maskingして利用可能にすることはScope外とする。

---

# 10. Representative PoC Scenario

PoCでは、実運用に近い問い合わせを用いる。

例：

> ある対象データが画面に表示されない。

## Step 1: Inquiry Intake

問い合わせメール本文をそのままCodexへ入力する。

## Step 2: Symptom Understanding

- 何が表示されないか
- 何が期待されていたか
- 対象年月等
- 対象機能

を整理する。

## Step 3: Technical Investigation

必要に応じて、

```text
Screen
→ API
→ SQL
→ Database
```

または、

```text
Input File
→ Batch
→ Table
→ Aggregation
→ API
→ Screen
```

等を調査する。

## Step 4: Current Specification

Design / Test / Existing Inquiry等を確認する。

## Step 5: Historical Evidence

必要であれば、NotebookLM等で過去の設計打ち合わせ・合意内容を確認する。

## Step 6: Assessment Material

以下を分離して整理する。

- Observed Fact
- Technical Cause
- Current Specification
- Historical Agreement
- Missing Knowledge
- Responsibility Assessment Material

## Step 7: Human Review

担当者がEvidenceを確認する。

## Step 8: Stakeholder Output

利用者・顧客向け回答案を作成する。

## Step 9: Knowledge Reuse

今回の調査結果を次回利用可能な状態で残す。

---

# 11. Requirement Acceptance View

PoC終了時には、少なくとも以下の質問へ答えられる必要がある。

## Repository

- 対象Repositoryの現在構造を把握できたか。
- 既存運用を維持したままAI-Ready機能を追加できそうか。

## Inquiry

- 問い合わせメール本文から調査を開始できたか。
- 人間が最初から対象Fileを指定しなくても探索できたか。

## Investigation

- 関連Codeへ到達できたか。
- 必要なDocumentへ到達できたか。
- 技術的原因を整理できたか。

## Specification

- 原因とCurrent Specificationを分離して整理できたか。
- Test Evidenceを利用できたか。

## Historical Evidence

- Repository外Evidenceが必要であることを認識できたか。
- 未確認の場合、それをMissing / Not Checkedとして表現できたか。

## Assessment

- バグ / 仕様 / 仕様漏れ / 追加要望等の判断材料を整理できたか。
- AIが責任を断定せず、人間が確認できる形にできたか。

## Traceability

- 回答のEvidenceへ戻れたか。
- AIが何を見たか確認できたか。

## Reuse

- 調査結果を次のCaseで再利用可能な形にできたか。

---

# 12. Requirements Pending Existing Repository Review

以下は、対象RepositoryをCodex作業環境で確認した後に必ず再評価する。

1. Existing Inquiry FolderをCaseとしてそのまま利用できるか
2. Test Documentの実Format
3. Design Documentの実Format
4. Source Codeの構成
5. Release関連資料の構成
6. 現在のNaming Convention
7. Git Historyの品質
8. Historical / Current Documentの区別方法
9. Repository Size
10. AI-Ready変換対象とすべきDocument
11. Code Graphの必要範囲
12. Data Flow Graphの必要範囲
13. 新規Directory追加の必要性
14. Runtime / Generated Dataの配置
15. Repository Policyの必要性

これらを確認する前に、Directory ArchitectureやDocument変換方式を確定しない。

---

# 13. Requirements Pending Management / Security Confirmation

以下は上司または関連責任者への確認が必要である。

1. Codexから議事録を直接参照可能か
2. 議事録OriginalをRepositoryへ格納可能か
3. Git管理可能か
4. Git履歴に議事録本文を残してよいか
5. 顧客名・個人名等の扱い
6. Masking / Redaction要否
7. 責任・契約情報のAI利用可否
8. Repository Access Control
9. AI-Ready Summaryの保存可否
10. NotebookLMからRepositoryへ情報を移管できるか

これらの回答によって、Historical EvidenceのArchitectureを決定する。

---

# 14. 後続ドキュメントへの引き継ぎ

本要件を基に、以下の後続文書で具体化する。

```text
04_DESIGN_PRINCIPLES.md
→ 要件を満たすために守る設計原則

05_REPOSITORY_ARCHITECTURE.md
→ Existing RepositoryとAI-Ready機能をどう共存させるか

06_KNOWLEDGE_MODEL.md
→ Inquiry / Function / Test / Evidence等をどう表現するか

07_GRAPH_AND_CODEGRAPH.md
→ Relation / Code Graph / Data Flowをどう表現するか

08_DOCUMENT_INGEST_AND_TRANSFORM.md
→ Existing Documentをどう解析・変換するか

09_CASE_INVESTIGATION_WORKFLOW.md
→ 問い合わせ調査のState / Input / Output / Completion Condition

10_AGENT_AND_SKILL_ARCHITECTURE.md
→ Codex / Agent / Skillの責務分離

11_SECURITY_AND_GOVERNANCE.md
→ Meeting Minutes / Git / Codex / Masking / Access Policy

12_RUNTIME_AND_STORAGE.md
→ Runtime DB / Graph / Index / Rebuild

13_UI_AND_DEVELOPER_EXPERIENCE.md
→ Case / Evidence / Coverage等をどう表示するか

15_POC_PLAN_AND_ACCEPTANCE_CRITERIA.md
→ どの要件をどのSampleで検証するか
```

---

# 15. この要件定義で最も重要なこと

本PoCでは、

> AIへ大量の資料を読ませること

自体を要件としない。

重要なのは、

```text
問い合わせメール
↓
必要な情報を探す
↓
技術的原因を確認する
↓
仕様・Evidenceを確認する
↓
不足情報を認識する
↓
人間が判断する
↓
結果を次回へ再利用する
```

という運用保守の実際の調査プロセスを、既存Repositoryを活かしながら支援できることである。

---

# 16. Requirements Statement

> 本PoCは、既存の運用保守Repositoryを実査・尊重した上で、まず問い合わせ対応をGolden ObjectiveとしてEnd-to-Endの成立性を確認する。Product全体ではInquiry、Incident、System理解、Operation、Change、Impact Analysis、Estimation、Knowledge Maintenanceを複数Objectiveを持つWork Itemとして管理し、目的変更時も共通ContextとEvidenceを保持する。Canonical Relation Model、目的別Workspace、Operation / Stakeholder Projection、Source / Artifact Lifecycleを共通基盤とし、PoC対象データは事前にAI利用承認済みの範囲へ限定する。高度な分類・Masking・原本復元UIはPoC Scope外とし、Evidence Traceability、Human Review、Knowledge Reuseを優先する。
