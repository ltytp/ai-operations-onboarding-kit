# AI-Ready Operations Repository / Codex App
## 06. Knowledge Model

**File Name:** `06_KNOWLEDGE_MODEL.md`  
**Status:** Draft  
**Document Role:** Logical Knowledge Model / Domain Concepts  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、運用保守で扱う情報を、

> AIが検索・関連付け・調査・再利用できるKnowledgeとして、どのように意味付けするか

を定義する。

本ドキュメントでは、以下を主に整理する。

- Knowledgeの基本単位
- Caseの位置付け
- Knowledgeの分類
- Evidenceの扱い
- Current / Historicalの区別
- Codex Resume / Sessionの扱い
- Persistent Investigation Knowledge
- Repository外Knowledge
- Provenance
- Knowledge State
- Missing Knowledge
- Conflict
- Time
- Stakeholder / Responsibility
- Relationの基本概念

Graph DB、JSON、SQLite、Semantica等の物理実装方式は本ドキュメントでは確定しない。

---

# 2. Knowledge Modelの基本思想

[DECIDED]

本PoCでは、Repository内のFileをそのままKnowledge Modelとしない。

例えば、

- Excel File
- PowerPoint File
- Source File
- Inquiry Folder
- Codex Session

は、物理的な情報SourceまたはWorking Historyである。

Knowledge Modelでは、それらから、

- Business Process
- Function
- System
- Data
- Implementation
- Test
- Requirement
- Decision
- Inquiry
- Evidence
- Stakeholder

などの意味を抽出して扱う。

つまり、

> File Structure

と

> Knowledge Meaning

を分離する。

---

# 3. Knowledge Modelで解決したいこと

現在の問い合わせ調査では、人間が頭の中で以下を接続している。

- 問い合わせ事象
- 対象業務
- 対象機能
- Source Code
- Database
- Batch
- Test
- Current Specification
- 過去仕様
- 設計打ち合わせ
- 顧客との合意
- 過去問い合わせ
- 責任範囲

本Knowledge Modelでは、

> これらを同じFileへまとめる

ことではなく、

> それぞれを識別し、必要なRelationで接続できる状態

を目指す。

---

# 4. Work Itemを中心にKnowledgeを利用する

[DECIDED]

Repository全体を一度に理解することを前提としない。

現在のWork Itemを起点として、その目的に必要なKnowledgeだけを集める。

PoCではInquiry InvestigationをPrimary Objectiveとする。

Work Item Type候補は以下。

- Inquiry
- Incident
- Bug
- Change Request
- Release
- Investigation
- Operation Task
- System Discovery
- Impact Analysis
- Estimation
- Knowledge Maintenance

Work Itemは、単なる問い合わせ文ではなく、

> 一つ以上の目的を共有Contextの上で継続する作業単位

として扱う。

`Case`はInquiry / Incident subtypeまたは既存Repositoryとの互換用語とする。

---

# 5. Work Itemに必要な論理情報

[PROVISIONAL]

Work Itemには、論理的に以下を関連付けられることが望ましい。

- Work Item Type
- Primary Objective
- Secondary Objectives

- Original Inquiry
- Summary
- Symptom
- Expected Behavior
- Business Context
- Affected Function
- Affected System
- Affected Data
- Related Code
- Related Documents
- Related Test
- Evidence
- Timeline
- Technical Cause
- Current Specification
- Historical Evidence
- Responsibility Assessment Material
- Sources Checked
- Sources Not Checked
- Missing Knowledge
- Open Questions
- Human Review
- Final Decision
- Final Response

これらを一つの巨大Fileへ保存することを意味しない。

物理保存方式は後続設計で決める。

---

# 6. Knowledgeの主要領域

[DECIDED]

運用保守で必要なKnowledgeを、現時点では以下の6領域として考える。

1. Business / Operation
2. Function
3. System / Data
4. Implementation
5. Evidence / Decision History
6. Stakeholder / Responsibility

Timeは7番目の領域ではなく、全領域を横断するDimensionとして扱う。

---

# 7. Business / Operation Knowledge

[DECIDED]

Business / Operation Knowledgeは、

> 利用者が実際にどのような業務を行っているか

を表す。

候補Entity：

- BusinessProcess
- Operation
- BusinessEvent
- BusinessRule
- BusinessCalendar
- BusinessInput
- BusinessOutput

例：

- 日次データ受信
- 月次集計
- 利用者による検索
- 報告書作成
- 月末締め

Source Codeだけでは把握しにくいKnowledgeである。

---

# 8. Function Knowledge

[DECIDED]

Function Knowledgeは、

> システムが利用者や他Systemへ提供する機能

を表す。

候補Entity：

- Function
- Screen
- API
- Batch
- Report
- FileInterface
- OperationFunction

FunctionはImplementationより上位の意味として扱う。

例えば、複数のClass / Function Codeが一つの業務Functionを実装している場合がある。

---

# 9. System / Data Knowledge

[DECIDED]

System / Data Knowledgeは、

> システム構成とデータの流れ

を表す。

候補Entity：

- System
- Application
- Component
- Database
- Table
- Column
- File
- Queue
- ExternalSystem
- DataSet
- DataObject

運用保守では、Code Callだけでなく、

> どのDataが、どこから来て、どこへ保存され、どこで利用されるか

が重要になる。

---

# 10. Implementation Knowledge

[DECIDED]

Implementation Knowledgeは、実装そのものを表す。

候補Entity：

- Repository
- Module
- Package
- Class
- FunctionCode
- Method
- SQL
- Configuration
- JobDefinition
- Script

Implementation Knowledgeは、原則Source Codeから再生成・再解析可能な情報を中心とする。

Source CodeそのものをKnowledgeへ複製することを目的としない。

---

# 11. Evidence / Decision History Knowledge

[DECIDED]

Evidence / Decision History Knowledgeは、

> なぜ現在の仕様・実装になっているかを判断するための根拠

を表す。

候補Entity：

- Requirement
- Design
- TestCase
- TestResult
- Meeting
- MeetingDecision
- QA
- Release
- Change
- Commit
- PastInquiry
- InvestigationRecord
- Agreement

特に責任範囲を整理する際、この領域が重要となる。

---

# 12. Stakeholder / Responsibility Knowledge

[DECIDED]

Stakeholder / Responsibility Knowledgeは、

> 誰がどの立場で関与し、どの範囲を担当しているか

を表す。

候補Entity：

- Stakeholder
- Person
- Team
- Organization
- Role
- ResponsibilityScope
- ApprovalAuthority

ただし個人情報・顧客情報を含む可能性があるため、Security / Governanceの対象とする。

---

# 13. Timeは横断Dimensionとする

[DECIDED]

Timeを独立したKnowledge Layerとして扱わない。

各Knowledgeに、意味の異なる時間を関連付ける。

候補：

- EffectiveDate
- CreatedDate
- ModifiedDate
- BusinessDate
- DataDate
- FileArrivalTime
- BatchExecutionTime
- ReleaseDate
- DecisionDate
- MeetingDate
- InquiryDate
- InvestigationDate
- AnswerDate

例えば、

> Meeting Date

と

> Specification Effective Date

は同じとは限らない。

---

# 14. Knowledge Sourceの分類

[DECIDED]

Knowledgeそのものと、それを得たSourceを分離する。

現時点ではSourceを少なくとも以下に分類する。

## Repository Original

Repository内のOriginal Source。

例：

- Source Code
- Test Specification
- Design Document
- Inquiry Folder
- Release Document

## Repository Derived

Repository Originalから生成されたAI-Ready情報。

## Codex Working Session / Resume

Codex上で行われた調査・壁打ちのWorking History。

## External Original

Repository外のOriginal Source。

例：

- NotebookLMで参照している議事録
- 外部共有領域の資料

## Persistent Investigation Knowledge

Codex等での調査結果をHuman Review後にSession外へ保存したKnowledge。

---

# 15. SourceとKnowledgeを混同しない

[DECIDED]

例えば、議事録File自体はSourceである。

その議事録から、

- 顧客が要求した内容
- 開発側が回答した内容
- 合意された仕様
- 保留された事項

などをKnowledgeとして抽出できる。

同様に、Codex Resume自体はWorking Sourceであり、

- Technical Cause
- Sources Checked
- Missing Knowledge

等の永続Knowledgeとは別に扱う。

---

# 16. Codex Resume / SessionのKnowledge上の位置付け

[DECIDED]

Codex Resume / Sessionは、

> 過去の調査過程を復元するためのInvestigation Source

として扱う。

以下の情報が含まれる可能性がある。

- 問い合わせメール
- 調査仮説
- 確認File
- 確認Code
- SQL / Data確認
- 否定された仮説
- 人間の追加情報
- NotebookLM等から人間が持ち込んだ情報
- Open Questions
- 調査過程

ただし、Codex Resume / SessionをHuman Verified Knowledgeとはみなさない。

---

# 17. Persistent Investigation Knowledge

[DECIDED]

今後のCodex調査・壁打ちのうち、再利用すべき重要内容はSession外へ永続化する。

Persistent Investigation Knowledge候補：

- InvestigationSummary
- InvestigationStep
- SourceChecked
- SourceNotChecked
- TechnicalCause
- EvidenceReference
- MissingKnowledge
- OpenQuestion
- Assessment
- HumanDecision
- FinalResponse

これらは、次回問い合わせで検索・再利用可能なKnowledgeとする。

---

# 18. Working HistoryとPersistent Knowledgeを分ける

[DECIDED]

Codex Session内には、途中仮説や誤った仮説も含まれる。

そのため、

> Sessionに書かれている

ことだけを理由にKnowledgeを確定しない。

基本的には、

1. Codexで調査する
2. Working Historyが蓄積される
3. 調査結果を整理する
4. Human Reviewする
5. 再利用すべき内容だけPersistent Knowledgeへ昇格する

という流れとする。

---

# 19. Evidenceの定義

[DECIDED]

Evidenceとは、

> あるFact、Specification、Assessmentを裏付けるために参照できるSourceまたはKnowledge

とする。

Evidence候補：

- Source Code
- Test Case
- Test Result
- Requirement
- Design
- Meeting Decision
- QA
- Commit
- Release
- Past Inquiry
- Data / SQL Result

AIの説明文自体をOriginal Evidenceとして扱わない。

---

# 20. FactとEvidenceを分ける

[DECIDED]

例えば、

> 月次Batchは対象データを生成していない

というFactがある場合、

Evidenceとして、

- Source Codeの条件分岐
- SQL結果
- Batch Log
- Test Result

等が紐付く。

FactとEvidenceを同じFieldに混在させない。

---

# 21. Technical Cause

[DECIDED]

Technical Causeは、

> 事象が技術的に発生した直接または主要な原因

を表す。

例：

- 対象Recordが生成されていない
- Filter Conditionで除外されている
- Batchが未実行
- Input Fileに対象Dataがない
- APIが想定外のStatusを返している

Technical CauseだけでBug / Responsibilityを確定しない。

---

# 22. Current Specification

[DECIDED]

Current Specificationは、

> 現在有効と判断されている仕様

を表す。

Current Specificationの根拠候補：

- Current Design
- Current Test
- Current Operation Manual
- Current Code
- Release Information
- Human Confirmed Decision

Codeの挙動だけをCurrent Specificationの唯一の根拠にしない。

---

# 23. Historical Specification

[DECIDED]

Historical Specificationは、

> 過去の時点で有効だった仕様

を表す。

CurrentとHistoricalを混同しない。

Historical Source候補：

- Old Design
- Old Test
- Past Release
- Past Meeting
- Git History
- Past Inquiry

---

# 24. Agreement Knowledge

[DECIDED]

Agreement Knowledgeは、

> 顧客側と開発側等の間で、何が合意されたか

を表す。

Source候補：

- Meeting Minutes
- QA
- Requirement
- Approval Record
- Mail / Communication Record

PoC時点では議事録等のRepository統合可否が未確定であるため、Agreement KnowledgeのSourceがExternalである場合を考慮する。

---

# 25. Decision Knowledge

[DECIDED]

Decision Knowledgeは、

> ある選択肢について、どのような判断が行われたか

を表す。

候補情報：

- Decision
- Reason
- Alternatives
- DecidedBy
- DecisionDate
- Evidence
- RelatedRequirement
- RelatedFunction
- EffectiveFrom

MeetingとDecisionを同一Entityにしないことを検討する。

一つのMeetingで複数Decisionが行われる可能性があるためである。

---

# 26. Test Knowledge

[PROVISIONAL]

Test Documentを単一Documentとして扱うだけでなく、必要に応じてTest Caseへ分解する。

候補情報：

- TestCaseID
- Scenario
- Preconditions
- Input
- ExpectedResult
- ActualResult
- RelatedFunction
- RelatedRequirement
- TestVersion
- ExecutionDate

ただし実際のExcel構造確認前に粒度を確定しない。

---

# 27. Past Inquiry Knowledge

[DECIDED]

過去問い合わせは重要なKnowledge Sourceとする。

既存問い合わせFolderとCodex Resumeの双方に情報が分散している可能性がある。

Past Inquiry Knowledgeとして候補となる情報：

- InquiryText
- Symptom
- RelatedFunction
- Investigation
- TechnicalCause
- Evidence
- Assessment
- Resolution
- FinalResponse
- RelatedCode
- RelatedTest

---

# 28. Past InquiryとPersistent Investigation Knowledge

[DECIDED]

今後の問い合わせは、可能な範囲でPersistent Investigation Knowledgeを残す。

これによりPast Inquiryを、

> File Folderだけ

ではなく、

> 再利用可能な調査Knowledge

として検索できるようにする。

---

# 29. Missing Knowledge

[DECIDED]

Missing Knowledgeは正式なKnowledge状態として扱う。

例：

- Historical Meeting Minutes未確認
- Old Designが見つからない
- Test Evidenceが存在するか不明
- Responsibility判断に必要な合意記録がない
- External Sourceへアクセスできない

Missing Knowledgeを単なるError Logとして扱わない。

---

# 30. Open Question

[DECIDED]

Open Questionは、

> 調査時点で回答が確定していない問い

として扱う。

例：

- この条件は開発時に顧客と合意されたか
- このTable更新はいつReleaseされたか
- このSE対応の目的は何だったか

Open Questionが解消された場合、新しいKnowledgeとRelationを生成できる。

---

# 31. Conflict

[DECIDED]

複数Sourceで内容が一致しない場合、Conflictを明示する。

例：

- DesignとCodeが異なる
- TestとCurrent Behaviorが異なる
- Meeting Decisionと実装が異なる
- Past Inquiryの説明とCurrent Specificationが異なる

AIが無条件に一つへ統合しない。

---

# 32. Conflictに必要な情報

[PROVISIONAL]

Conflictには以下を保持できることが望ましい。

- ConflictID
- Subject
- SourceA
- StatementA
- SourceB
- StatementB
- DetectedDate
- CurrentAssessment
- ReviewStatus
- Resolution

---

# 33. Knowledge State

[PROVISIONAL]

Knowledgeには状態を持たせることを検討する。

候補：

- `human_verified`
- `human_reviewed`
- `ai_extracted`
- `ai_inferred`
- `needs_review`
- `conflicting`
- `deprecated`
- `unknown`

このStateは、Source Typeとは別概念とする。

---

# 34. Knowledge Stateの意味

## human_verified

Original Evidenceと照合して人間が確認済み。

## human_reviewed

AI生成・抽出内容を人間がReview済み。

## ai_extracted

AI / ParserがSourceから抽出したがHuman Review前。

## ai_inferred

複数情報からAIが推論した内容。

## needs_review

重要だがHuman Reviewが必要。

## conflicting

他Knowledgeと矛盾している。

## deprecated

現在は有効ではない。

## unknown

状態や正しさを判断できない。

---

# 35. Current / Historical State

[PROVISIONAL]

Knowledge Stateとは別に、時間上の有効性を表現する必要がある。

候補：

- current
- historical
- superseded
- draft
- unknown

例えば、

> human_verified + historical

という組み合わせもあり得る。

---

# 36. Provenance

[DECIDED]

すべての重要Knowledgeについて、可能な限りSourceへ戻れることを目指す。

Provenance候補：

- SourceType
- SourceID
- RepositoryPath
- ExternalLocation
- GitCommit
- DocumentVersion
- Sheet
- Row
- Range
- Page
- Slide
- CodeSymbol
- ExtractedAt
- ExtractorVersion
- ReviewedBy
- ReviewedAt

具体Schemaは`08_DOCUMENT_INGEST_AND_TRANSFORM.md`で詳細化する。

---

# 37. Provenance Chain

[PROVISIONAL]

AI-Ready Knowledgeが複数段階で生成される場合、Provenance Chainを追えることが望ましい。

例：

Original Excel  
→ Normalized Data  
→ TestCase Knowledge  
→ Case Evidence

最終KnowledgeからOriginal ExcelのSheet / Rowまで戻れる状態を目指す。

---

# 38. Stable ID

[PROVISIONAL]

Knowledge Objectには、Path変更に影響されにくいStable IDを持たせることを検討する。

対象候補：

- Case
- Function
- System
- Table
- Document
- TestCase
- Decision
- Meeting
- Stakeholder
- Knowledge Object

ID方式は未決定。

---

# 39. Knowledge Objectの最小概念Schema

[PROVISIONAL]

具体形式は未決定だが、論理的には以下を持つことを検討する。

```yaml
id: stable-id
type: Function
title: 月次集計
status: human_reviewed
temporal_status: current
summary: ...
sources:
  - ...
relations:
  - ...
created_at: ...
updated_at: ...
```

これはCanonical Formatの決定ではない。

---

# 40. Source Referenceの最小概念Schema

[PROVISIONAL]

```yaml
source_id: source-id
source_type: repository_original
location: path-or-external-reference
version: ...
access_policy: ...
checked: true
```

External Sourceの場合、Repository Pathを必須としない。

---

# 41. Relationの基本思想

[DECIDED]

Knowledgeは独立Objectとして保存するだけでなく、必要なRelationで接続する。

Relationは、

> 何と何が、どのような意味で関係しているか

を表す。

Relationの詳細Schemaは`07_GRAPH_AND_CODEGRAPH.md`で定義する。

---

# 42. Relation候補

[PROVISIONAL]

代表候補：

- USES
- CALLS
- READS
- WRITES
- GENERATES
- DEPENDS_ON
- IMPLEMENTS
- TESTED_BY
- VERIFIED_BY
- DEFINED_BY
- DECIDED_BY
- CHANGED_BY
- RELEASED_IN
- AFFECTS
- RELATED_TO
- OWNED_BY
- RESPONSIBLE_FOR
- SUPERSEDES
- DERIVED_FROM
- EVIDENCED_BY
- INVESTIGATED_IN

---

# 43. RelationにもEvidenceが必要

[DECIDED]

RelationをAIが推測しただけなのか、Original Sourceで確認できるのかを区別する。

例えば、

> Function A IMPLEMENTED_BY Code Function B

というRelationが、

- Code解析から得た
- Designから得た
- AI推論した
- Human Review済み

のどれかを確認できることが望ましい。

---

# 44. Canonical Relation ModelとGraph Projection

[DECIDED]

Graph Viewごとに別のKnowledge Modelを持たない。共通のNode / Edge / Provenance / Review State / Temporal属性を持つCanonical Relation Modelから、目的別のGraph ViewをProjectionする。

| Graph View | 主な問い | 主なNode |
|---|---|---|
| Work Item / Case | この作業・問い合わせに何が関係するか | WorkItem、Objective、Function、Data、Code、Test、Evidence |
| Domain / Business | 業務上どこに位置するか | BusinessProcess、Operation、Actor、Rule |
| Function | 業務・利用者へ何を提供するか | Function、Screen、API、Batch、Report |
| System / Architecture | Functionをどの技術構成で実現・稼働するか | System、Component、Service、Database、Queue、ExternalSystem |
| Infrastructure / IaC | 実環境Resourceはどの定義から作られ何へ依存するか | IaCRepository、Module、Resource、Network、Compute、IAM、State、Monitoring |
| Data Flow | 値はどこから来てどこへ行くか | File、Queue、Table、Column、Transform、Report |
| Code | どの実装が処理するか | Repository、Module、Class、FunctionCode、SQL、Configuration |
| Test | どの仕様・機能が検証されるか | TestCase、ExpectedBehavior、TestResult、Function |
| Evidence / History | なぜ現在の仕様になったか | Requirement、Design、Decision、Meeting、Release、Commit |
| Operation / Runbook | 誰が何をどの順序で運用するか | OperationStep、Actor、Input、Output、Control、Escalation |
| Stakeholder / Responsibility | 誰が関与し誰の確認・承認が必要か | Person、Team、Organization、Role、Approval、Scope |

Work Item Viewは現在作業に関係するNodeを横断するContext Projectionであり、他のViewは同じRelation Modelを特定のNode Type / Relation Type / Time Scopeで投影した専門Viewである。View数自体を固定目的にしない。

FunctionとSystemは分離する。FunctionはTechnologyから独立したCapability / Behavior、SystemはそのFunctionを実現するRuntime / Component境界であり、`IMPLEMENTED_BY`、`EXPOSED_BY`、`HOSTED_ON`等で接続する。Infrastructure / IaCはSystemの実行基盤と宣言元を表し、TerraformのHCL、Module、Provider Resource、Plan、State Metadata等から抽出する。Secret値やState内の機密値をGraph Propertyへ複製しない。

平面Projectionに加え、Inquiry / Work Itemを上位Context、Functionを業務Capability層、System / Infrastructureを実行層、Code / Data Flow / Testを実装・検証層、Evidenceを検証基盤として表示する縦断Stack表現を持つ。これはNodeの包含関係を固定するStorage Schemaではなく、層横断の理解を助けるPresentation Modelである。

Timeは独立したGraph Layerではなく、すべてのViewを横断する`Current / Historical / Effective Date / Version` Dimensionとして扱う。

詳細は`07_GRAPH_AND_CODEGRAPH.md`で定義する。

---

# 45. BusinessとImplementationを直接結びすぎない

[PROVISIONAL]

可能な場合、

Business  
→ Function  
→ System  
→ Implementation

という中間概念を持たせる。

例えばBusiness Processから特定Code Functionへ直接Relationだけを大量に張ると、意味が不明瞭になる可能性がある。

ただし実際のPoCで必要なRelationを優先し、過度に厳格なOntologyにはしない。

---

# 46. Work Item-Centered Retrieval

[DECIDED]

Knowledge Modelの主用途は、Work ItemとそのObjectiveから必要情報へ辿ることである。

問い合わせに対し、関連する、

- Function
- System
- Code
- Data
- Test
- Design
- Past Inquiry
- Meeting
- Decision
- Stakeholder

等を必要な範囲だけ取得する。

Repository全Knowledgeを毎回LLM Contextへ投入しない。

Objectiveを切り替えてもShared Contextは保持し、目的固有のChecklist、完了条件、成果物だけを切り替える。

---

# 47. Coverage

[DECIDED]

Work Item / Objectiveごとに、どのKnowledge領域を確認したか表現できることが望ましい。

候補：

- Business: checked / not_checked / partial
- Function: checked / not_checked / partial
- System: checked / not_checked / partial
- Implementation: checked / not_checked / partial
- Test: checked / not_checked / partial
- Historical Evidence: checked / not_checked / partial
- Responsibility: checked / not_checked / partial

---

# 48. Sources Checked

[DECIDED]

Case調査では、実際に確認したSourceを記録する。

Source Checkedは、

> Relation上つながっている

こととは別である。

Knowledge Graphに存在していても、今回のCaseで確認していなければCheckedとはしない。

---

# 49. Sources Not Checked

[DECIDED]

関連する可能性があるが確認していないSourceも記録する。

例：

- Access不可
- Time不足
- Source不存在
- Relevance低
- Human判断でScope外

理由も記録できることが望ましい。

---

# 50. Access Restricted Knowledge

[DECIDED]

Sourceが存在するが、AIまたはUserが参照権限を持たない場合を表現できること。

特に議事録・顧客情報・契約情報等を想定する。

Access RestrictedとMissingを混同しない。

---

# 51. Stakeholder KnowledgeとOutput

[DECIDED]

Stakeholder Knowledgeは調査対象だけでなく、Output生成にも利用する。

例えば同じCaseでも、

## End User

- 発生事象
- 業務影響
- 操作
- 回避策

## Customer System / Management

- Technical Cause
- Current Specification
- Historical Agreement
- Responsibility Assessment Material
- Change Requirement

## Developer

- Code
- SQL
- Data Flow
- Reproduction
- Test Scope

といった違いがある。

---

# 52. Responsibility Scope

[PROVISIONAL]

Responsibility Scopeは、単純なBooleanで表現しない。

候補として、

- Customer Scope
- Development Scope
- Maintenance Scope
- Shared / Ambiguous
- Additional Development Candidate
- Unknown

等のClassificationを検討する。

ただし契約・費用上の最終判断はHuman Decisionとする。

---

# 53. Responsibility Assessment Material

[DECIDED]

AIが保持・提示するのは、

> Responsibility Decision

そのものではなく、

> Responsibility Assessment Material

を基本とする。

含める候補：

- Observed Fact
- Technical Cause
- Current Specification
- Historical Agreement
- Requirement
- Difference
- Evidence
- Missing Evidence
- AI Assessment
- Human Review Status

---

# 54. Human Decision

[DECIDED]

Human DecisionはAI Assessmentと別Objectまたは別Stateとして扱う。

例：

- Final Classification
- Responsibility Decision
- Need for Additional Development
- Customer Response Position
- Approver
- Decision Date

AIがHuman Decisionを書き換えない。

---

# 55. Knowledgeの更新

[DECIDED]

Knowledgeは固定情報ではない。

以下により更新される。

- Document Change
- Code Change
- Release
- New Inquiry
- Investigation
- Human Review
- New Meeting / Decision
- Conflict Resolution

更新時にOriginalとVersionの関係を追跡する。

---

# 56. Knowledgeの削除

[PROVISIONAL]

Originalが削除された場合でも、過去CaseのEvidenceとしてHistorical Referenceを残す必要がある可能性がある。

したがって、

> Original削除 = Knowledge完全消去

とは限らない。

Current KnowledgeからDeprecated / Historicalへ移す等の扱いを検討する。

---

# 57. KnowledgeのVersion

[PROVISIONAL]

同一FunctionやSpecificationについて、複数Versionが存在する可能性がある。

Version管理候補：

- Git Commit
- Document Version
- Effective Date
- Release
- Valid From / To

Graph上の時間表現は`07`、Storageは`12`で詳細化する。

---

# 58. Current Knowledgeの決定

[OPEN]

複数VersionからCurrentをどのように決めるかは未確定。

候補：

- 明示Metadata
- Latest Approved Version
- ReleaseとのRelation
- Git History
- Human Review

単純にFile Modified Dateが最新のものをCurrentとみなさない。

---

# 59. Knowledge Extraction

[PROVISIONAL]

Original Sourceから以下を抽出する可能性がある。

- Entity
- Fact
- Relation
- Decision
- Requirement
- Test Case
- Data Flow
- Stakeholder
- Date
- Summary

抽出方式はDocument Typeごとに異なる。

詳細は`08_DOCUMENT_INGEST_AND_TRANSFORM.md`で定義する。

---

# 60. AI ExtractionのQuality Gate

[PROVISIONAL]

AI抽出結果を自動的にHuman Verified Knowledgeへしない。

少なくとも重要Knowledgeについて、

- Source Mapping
- Validation
- Confidence
- Review State

を持たせることを検討する。

---

# 61. Canonical Knowledge Format

[OPEN]

現時点では以下が候補としてある。

- `content.md`
- `metadata.yaml`
- `relations.json`

ただし、本Knowledge Modelをその物理形式へ固定しない。

Canonical Formatは`08_DOCUMENT_INGEST_AND_TRANSFORM.md`で決定する。

---

# 62. Knowledge ModelとSemantica

[PROVISIONAL]

Semanticaを採用する場合でも、本Knowledge ModelをSemanticaの内部Data Modelへ従属させない。

Semanticaは、

- Knowledge Graph
- Provenance
- Temporal
- Conflict
- Decision
- Context

等のInfrastructure候補として評価する。

Maintenance固有のEntity / Relation / Workflowは本Project側で定義する。

---

# 63. Knowledge ModelとCode Graph Tool

[PROVISIONAL]

Code Graph生成Toolを採用する場合でも、生成されたCode Nodeを本ProjectのKnowledgeと接続するAdapterを設けることを検討する。

例：

Function Knowledge  
→ IMPLEMENTED_BY  
→ External Code Graph Node

これによりCode Graph Toolを交換しやすくする。

---

# 64. Knowledge ModelとRuntime DB

[DECIDED]

Knowledge ModelはSQLite / Neo4j等のTable / Node Schemaそのものではない。

Logical Knowledge Modelを先に定義し、Storageは後から選択する。

Runtime DBがなくても、Repository上のSourceとDerived Dataから再構築可能な状態を目指す。

---

# 65. Knowledge ModelとExisting Repository

[DECIDED]

本Knowledge ModelはExisting RepositoryのDirectory構成を置き換えない。

既存File / Folderを、

> Knowledge ObjectへMappingする

考え方とする。

例えば既存問い合わせFolderを物理的に移動せず、Case / PastInquiryとしてLogical Model上で扱うことができる。

---

# 66. Existing Repository Review後に決める事項

[OPEN]

実Repository確認後、以下を再評価する。

- 既存問い合わせをCaseとしてそのまま扱えるか
- TestCaseの粒度
- Design Documentの種類
- Current / Historical判定方法
- Release Knowledgeの構造
- Existing NamingからStable IDを作れるか
- Source CodeとFunctionのMapping方法
- Past InquiryとCodex Resumeの対応方法

---

# 67. Codex Resume Review後に決める事項

[OPEN]

過去Codex Session / Resumeを実際に確認できる場合、以下を評価する。

- どの程度調査Sourceが残っているか
- Sources Checkedを抽出可能か
- Inquiry Folderとの重複
- Final AnswerとWorking Historyの区別
- Persistent Investigation Knowledgeへ何を昇格すべきか
- SessionとCaseをどう紐付けるか

---

# 68. Meeting Minutes確認後に決める事項

[OPEN]

上司・Security確認後に以下を決める。

- MeetingをOriginalとしてRepositoryへ持てるか
- Meeting DecisionをKnowledge化できるか
- 個人名をStakeholderとして持てるか
- Summaryのみ保存するか
- Source Locationのみ保持するか
- Codex Direct Accessを許可するか

---

# 69. Golden Sampleで確認するKnowledge

[DECIDED]

PoCでは一件の問い合わせをGolden Sampleとして、少なくとも以下をMappingできるか確認する。

- Inquiry
- Symptom
- Function
- Implementation
- Data
- Test Evidence
- Technical Cause
- Current Specification
- Past Inquiry
- Historical EvidenceまたはMissing Knowledge
- Human Assessment

すべてのKnowledge Typeを一度に実装する必要はない。

---

# 70. Golden Sampleの成功条件

Golden Sampleで以下が確認できればKnowledge Modelの初期成立と考える。

1. Inquiryから関連Functionへ辿れる
2. FunctionからCode / Dataへ辿れる
3. Current Test / Designへ辿れる
4. Past Inquiryを検索できる
5. Historical Evidenceの有無を認識できる
6. Technical CauseとAssessmentを分離できる
7. Evidence Sourceへ戻れる
8. Missing Knowledgeを表現できる
9. Human Review済み結果をPersistent Knowledgeとして残せる

---

# 70.1 Work Item・Operation・Artifact拡張

[DECIDED]

以下をCanonical Entity候補へ追加する。

## Work Management

- WorkItem
- Objective
- Finding
- Deliverable
- Review

## Operation / Stakeholder

- OperationStep
- Runbook
- Actor
- Person
- Team
- Organization
- Role
- Approval
- ResponsibilityScope

## Execution / Artifact

- UserAction
- Execution
- InputArtifact
- OutputArtifact
- GeneratedFile
- AuditEvent

代表Relation：

```text
WorkItem --HAS_OBJECTIVE--> Objective
WorkItem --INVOLVES--> Stakeholder
User --PERFORMED--> UserAction
UserAction --TRIGGERED--> Execution
Execution --CONSUMED--> InputArtifact
Execution --GENERATED--> OutputArtifact
OperationStep --PERFORMED_BY--> Actor
OperationStep --USES--> Function
```

System生成Fileは、通常の設計Documentと区別する。File本体をKnowledge Storeへ無条件に複製せず、Location、Checksum、Generated By、Input、Status、Retention等のMetadata / Referenceを基本とする。調査上重要なArtifactのみHuman Review後にEvidenceへ昇格させる。

Source / Data Stateは以下を区別する。

- Original Source
- Normalized Intermediate
- Persistent Knowledge
- Runtime Derived Index
- System-generated Artifact

DeleteはUnlink、Archive、Runtime除外、Permanent Deleteを別操作として扱う。

---

# 71. Knowledge ModelのAnti-Patterns

以下を避ける。

## File = Knowledge

File単位だけで意味を表現する。

## AI Summary = Fact

AI要約をHuman Verified Factとして扱う。

## Current = Latest Modified File

更新日時だけでCurrent Specificationを決める。

## Code = Specification

Current Codeだけで仕様を確定する。

## Resume = Source of Truth

Codex Sessionだけに調査成果を残す。

## Missing = Ignore

Evidence不足を無視して結論を出す。

## Graph = Everything

すべての情報をNode化すること自体を目的にする。

## Responsibility = AI Decision

AIが責任範囲を最終確定する。

---

# 72. 後続ドキュメントへの引き継ぎ

本Knowledge Modelを以下で具体化する。

## `07_GRAPH_AND_CODEGRAPH.md`

- Node / Edge
- Relation Schema
- Domain Graph
- Code Graph
- Data Flow Graph
- Temporal Relation
- Evidence付きRelation

## `08_DOCUMENT_INGEST_AND_TRANSFORM.md`

- Document Type
- Intermediate Representation
- Canonical Format
- Provenance
- Extraction
- Validation
- Source-to-Derived Mapping

## `09_CASE_INVESTIGATION_WORKFLOW.md`

- Inquiry State
- Investigation Step
- Sources Checked
- Missing Knowledge
- Human Review
- Codex SessionからPersistent Knowledgeへの昇格

## `11_SECURITY_AND_GOVERNANCE.md`

- Stakeholder
- Personal Information
- Meeting Minutes
- Access Policy
- Responsibility Information

## `12_RUNTIME_AND_STORAGE.md`

- Knowledge Persistence
- Runtime DB
- Index
- Version
- Rebuild
- Codex SessionとPersistent FileのStorage分離

---

# 73. Knowledge Model Decision Summary

## [DECIDED]

- Caseを調査中心とする
- 6つの主要Knowledge領域を持つ
- Timeは横断Dimension
- SourceとKnowledgeを分離する
- OriginalとDerivedを分離する
- Codex ResumeはInvestigation Source
- Codex Resumeを正本にしない
- 重要な調査成果はPersistent Investigation Knowledgeへ残す
- EvidenceとFactを分ける
- Technical CauseとAssessmentを分ける
- Missing Knowledgeを正式に扱う
- Conflictを隠さない
- Provenanceを保持する
- Human DecisionとAI Assessmentを分離する
- Storage製品よりLogical Modelを先に定義する

## [PROVISIONAL]

- Knowledge State
- Stable ID
- TestCase粒度
- Relation Type
- Responsibility Scope分類
- Canonical Knowledge Format

## [OPEN]

- Current判定方式
- Meeting Minutesの扱い
- Existing Inquiry Mapping
- Codex Sessionとの具体Mapping
- Stable ID方式
- Canonical Format
- Storage Schema

---

# 74. Knowledge Model Statement

> 本ProjectのKnowledge Modelは、運用保守に必要な情報をFile単位ではなく、Business、Function、System/Data、Implementation、Evidence/Decision History、Stakeholder/Responsibility、Operation、Execution / Artifactという意味単位で捉える。Inquiry、Incident、System理解、Operation、Change、Impact Analysis、Estimation等を複数Objectiveを持つWork Itemとして管理し、目的変更時も共通Contextを保持する。Original Source、Normalized Intermediate、Persistent Knowledge、Runtime Index、System-generated Artifactを区別し、AI推論・Human Verified Fact・Missing Knowledge・Conflictを混在させない。すべての重要Knowledgeは可能な限りEvidenceとProvenanceへ戻れることを前提とし、Logical Modelを特定Graph DB・Framework・Directory構成へ従属させない。
