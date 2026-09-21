# AI-Ready Operations Repository / Codex App
## 07. Graph and Code Graph

**File Name:** `07_GRAPH_AND_CODEGRAPH.md`  
**Status:** Draft  
**Document Role:** Canonical Relation Model / Layered Graph Projection / Code Graph / Data Flow Graph  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、運用保守で扱うKnowledge間のRelationを、どのようにGraphとして表現・利用するかを定義する。

本ProjectにおけるGraphの目的は、

> Knowledgeを見栄えよく可視化すること

ではない。

主目的は、

> 問い合わせCaseから、必要な業務・機能・システム・コード・データ・Test・Evidenceへ関係を辿って到達できること

である。

本ドキュメントでは以下を整理する。

- Graph導入の目的
- Node / Edgeの基本方針
- Canonical Relation Model
- Case / Domain / Function / System / Data Flow / Code / Test / Evidence-History View
- View間のBridge RelationとProjection Contract
- Case-Centered Subgraph
- Evidence付きRelation
- Temporal / Version Relation
- Current / Historicalの扱い
- Code Graphの生成と更新
- Data Flowの自動抽出とHuman Knowledgeの統合
- Graph Storageの考え方
- Graph DB導入判断
- Semantica等との境界

---

# 2. GraphはStorage製品ではなくRelation Modelとして考える

[DECIDED]

本Projectでは、

> Graphを使うこと

と

> Graph Databaseを使うこと

を分離する。

Graphの本質は、

- Node
- Edge
- Relation
- Traversal

である。

PoC初期では、JSON、YAML、SQLite、NetworkX等でRelationを表現してもよい。

Neo4j等のGraph DB採用は、Graph探索要件が明確になった後に判断する。

---

# 3. Graph導入の目的

[DECIDED]

Graphを導入する目的は、以下である。

1. Inquiryから関連Functionを辿る
2. FunctionからImplementationへ辿る
3. ImplementationからDataへ辿る
4. FunctionからTest / Designへ辿る
5. Current SpecificationからHistorical Evidenceへ辿る
6. Past Inquiryとの関連を辿る
7. Change Impactを探索する
8. Missing Relationを発見する
9. Investigation Coverageを確認する

Graph自体を完成させることを目的にしない。

---

# 4. Work Item-Centered Graphを基本とする

[DECIDED]

Repository全体のGraphを常に人間やLLMへ提示するのではなく、

> Current Work ItemとCurrent Objectiveに関連するSubgraph

を中心に利用する。

例えば問い合わせCaseから、

- Function
- Code
- Table
- Test
- Design
- Past Inquiry
- Meeting Decision

等を必要な範囲だけ抽出する。

これにより、巨大Graphの可視化やLLM Context肥大化を避ける。

---

# 5. Canonical Relation Modelと目的別Graph Projection

[DECIDED]

本ProjectではGraph Viewごとに別のGraphや別Databaseを作らない。

> 1つのCanonical Relation Modelから、利用目的に応じて複数のGraph ViewをProjectionする

ことを基本とする。

Canonical Relation ModelはNode / Edgeに加えて、Provenance、Knowledge State、Review State、Current / Historical、Versionを共通に保持する論理構造である。

## 5.1 Work Item / Case Graph

日常作業の入口。Current Work ItemとObjectiveに関係するFunction、Data、Code、Test、Evidence、Operation、Stakeholder等を横断表示する。`Case`はInquiry / Incident subtypeの表示名として残す。

## 5.2 Domain / Business Graph

BusinessProcess、Operation、Actor、Function、Ruleを中心に、問い合わせの業務上の位置を表示する。

## 5.3 Function Graph

BusinessとImplementationの中間として、Function、Screen、API、Batch、Report等の機能分解を表示する。Functionは「業務・利用者へ何を提供するか」を表し、実装Technologyや配置先が変わっても同じCapabilityとして追跡できる単位とする。

## 5.4 System / Architecture Graph

System、Component、Service、Database、Queue、ExternalSystem等の構成と接続を表示する。Systemは「Functionをどの技術構成で実現し、どこで稼働・接続するか」を表す。FunctionとSystemは同一Nodeにせず、`IMPLEMENTED_BY`、`EXPOSED_BY`、`HOSTED_ON`等で接続する。

## 5.5 Data Flow Graph

File、Batch、API、Table等を通るデータの流れ。

## 5.6 Code Graph

Source Codeの構造・Call・Dependency・Data Access等を表示する。

## 5.7 Test Graph

Function / CodeとTestCase、ExpectedBehavior、TestResultの関係を表示する。

## 5.8 Evidence / History Graph

Requirement、Design、Decision、Meeting、Release、Commitを辿り、現在の仕様がなぜ成立したかを表示する。

## 5.9 Operation / Runbook Graph

OperationStep、Actor、Input、Output、Control、Escalation、Functionを接続し、誰が何をどの順序で実行するかを表示する。

## 5.10 Infrastructure / IaC Graph

Terraform等のIaC Sourceから、IaCRepository、Module、Provider、Resource、Network、Compute、LoadBalancer、Database、IAM、State、Monitoringを表示する。代表Relationは`DECLARES`、`PROVISIONS`、`DEPENDS_ON`、`CONNECTS_TO`、`ROUTES_TO`、`ASSUMES_ROLE`、`TRACKS`、`OBSERVED_BY`とする。Terraform StateのSecret値や機密PropertyをGraphへ複製せず、Stable ID、Resource Address、Source Location、State / Plan参照、Drift Stateを管理する。

## 5.11 Stakeholder / Responsibility Graph

Person、Team、Organization、Role、System、Work Item、Approval、ResponsibilityScopeを表示する。Technical Cause、Maintenance担当、Contract Scope、最終責任判断を同一Relationにしない。

## 5.12 ViewとKnowledge Layerの関係

Graph ViewはKnowledge Layerそのものではなく、Canonical Relation Modelに対する用途別Projectionである。同じNodeが複数Viewへ現れてよく、View数自体を固定目的にしない。

重要なのは、Schema上・意味上で区別できることである。

---

# 6. Domain Graph

[DECIDED]

Domain Graphは、運用保守の意味を表すGraphである。

候補Node：

- Case
- BusinessProcess
- Operation
- Function
- Screen
- API
- Batch
- Report
- Requirement
- Design
- TestCase
- TestResult
- Meeting
- Decision
- Release
- PastInquiry
- Stakeholder
- ResponsibilityScope

Domain Graphは、運用保守固有のOntologyを中心とする。

---

# 7. Code Graph

[DECIDED]

Code Graphは、Source Codeの構造・Dependency・Call等を表す。

候補Node：

- Repository
- Module
- Package
- File
- Class
- Interface
- Method
- FunctionCode
- SQL
- Configuration
- JobDefinition

候補Relation：

- CONTAINS
- DEFINES
- IMPORTS
- CALLS
- DEPENDS_ON
- IMPLEMENTS
- OVERRIDES
- REFERENCES

---

# 8. Data Flow Graph

[DECIDED]

Data Flow Graphは、

> データがどこから来て、どこを通り、どこへ保存・出力されるか

を表す。

候補Node：

- File
- API
- Batch
- Queue
- Table
- Column
- DataSet
- Report
- ExternalSystem

候補Relation：

- READS
- WRITES
- GENERATES
- TRANSFORMS
- RECEIVES_FROM
- SENDS_TO
- LOADS
- EXPORTS
- AGGREGATES_FROM

---

# 9. Data Flow Graphを重要視する理由

[DECIDED]

運用保守では、Call Graphだけでは原因へ到達できない場合が多い。

例えば、

> 画面に対象Recordが表示されない

という問い合わせでは、

- Screen
- API
- Query
- Table

だけでなく、

- Input File
- Batch
- Aggregation
- Upstream Table

まで遡る必要がある可能性がある。

そのため、Code GraphとData Flow Graphを分けて考える。

---

# 10. Graphを一枚に潰さない

[DECIDED]

Domain、Code、Data Flowをすべて同一粒度のNodeとして扱うと、Graphが意味的に分かりにくくなる可能性がある。

そのため、例えば、

Business Process  
→ Function  
→ API  
→ Code Function  
→ Table

のように、意味階層を持たせる。

Business ProcessからCode Functionへ大量の直接Edgeを張ることを基本としない。

## 10.1 Projection Contract

[DECIDED]

すべてのGraph Viewは、少なくとも以下の共通入力を受け取れるQuery / Service契約を持つ。

```yaml
work_item_id: optional
objective: optional
view: work_item | domain | function | system | infrastructure | data | code | test | evidence | operation | stakeholder
scope: related_to_work_item | entire_project
time_scope: current | current_and_historical
depth: 1 | 2 | 3
selected_node_id: optional
```

出力Node / Edgeには、最低限以下を含める。

- Stable ID
- Type / Relation Type
- Display Label
- Knowledge State / Review State
- Current / Historical
- Provenance / Evidence Reference
- Source Access State

UIやAgentは特定Graph DBへ直接Queryせず、このProjection Contractを介する。

---

# 11. Nodeの基本原則

[DECIDED]

Node化する対象は、

> 調査時に識別・再利用・関係探索する価値があるもの

とする。

すべてのText FragmentをNode化しない。

Node化候補の判断基準：

- 一意に識別したいか
- 複数Caseから再利用するか
- Relation探索に利用するか
- Version管理する必要があるか
- Evidenceと紐付ける価値があるか

---

# 12. Node候補の初期セット

[PROVISIONAL]

PoCでは以下から必要なものだけ採用する。

## Case / Business

- Case
- BusinessProcess
- Function

## System / Data

- Screen
- API
- Batch
- File
- Database
- Table
- Report
- ExternalSystem

## Code

- Module
- Class
- FunctionCode
- SQL
- Configuration

## Evidence

- Requirement
- Design
- TestCase
- MeetingDecision
- PastInquiry
- Release
- Commit

## Stakeholder

- Stakeholder
- Organization
- ResponsibilityScope

---

# 13. Edgeの基本原則

[DECIDED]

Edgeは、

> 2つのNodeがどう関係するか

を意味的に表す。

単なる「RELATED_TO」を大量に使う設計は避ける。

可能な限り具体的なRelationを使用する。

---

# 14. 代表Relation候補

[PROVISIONAL]

## Domain

- USES
- AFFECTS
- DEFINED_BY
- DECIDED_BY
- TESTED_BY
- VERIFIED_BY
- RELATED_TO
- SUPERSEDES
- RELEASED_IN
- CHANGED_BY

## Implementation

- IMPLEMENTED_BY
- CALLS
- IMPORTS
- DEPENDS_ON
- CONTAINS

## Data

- READS
- WRITES
- GENERATES
- TRANSFORMS
- SENDS_TO
- RECEIVES_FROM
- AGGREGATES_FROM

## Investigation

- INVESTIGATED_IN
- EVIDENCED_BY
- SIMILAR_TO
- CAUSED_BY
- OBSERVED_IN
- CHECKED_IN

## Responsibility

- OWNED_BY
- RESPONSIBLE_FOR
- APPROVED_BY

---

# 15. `RELATED_TO`はFallbackとする

[DECIDED]

明確な意味を持つRelationが定義できる場合、`RELATED_TO`を使用しない。

例えば、

Function A  
RELATED_TO  
TestCase B

ではなく、

Function A  
TESTED_BY  
TestCase B

とする。

ただしAI抽出段階でRelation意味が不明な場合、一時的にGeneric Relationを持つことは許容する。

その場合は`needs_review`等の状態を持たせる。

---

# 16. RelationにもProvenanceを持たせる

[DECIDED]

RelationそのものにもEvidenceが必要である。

例えば、

Function A  
IMPLEMENTED_BY  
Code Function B

というRelationについて、

- Code解析で確認した
- Design Documentで確認した
- Humanが設定した
- AIが推論した

を区別する。

---

# 17. Relationの概念Schema

[PROVISIONAL]

論理的には以下のような情報を持つことを検討する。

```yaml
source: function:monthly-summary
relation: IMPLEMENTED_BY
target: code:monthly_summary
status: ai_extracted
provenance:
  source_type: code_analysis
  source_reference: ...
```

物理Formatは未決定。

---

# 18. Relation Confidence

[PROVISIONAL]

自動抽出Relationについて、必要に応じてConfidenceまたはReview Stateを持たせる。

候補：

- human_verified
- human_reviewed
- ai_extracted
- ai_inferred
- needs_review
- conflicting

数値Confidenceだけに依存しない。

---

# 19. Graph NodeとOriginal Fileを分離する

[DECIDED]

Original Fileそのものと、Fileから抽出されたKnowledge Nodeを別に考える。

例えば一つのExcel Design Documentから、

- Function A
- Function B
- Business Rule C

が抽出される場合がある。

File Nodeを持つことは可能だが、FileだけでDomain Knowledgeを表現しない。

---

# 20. Document Nodeの位置付け

[PROVISIONAL]

Requirement、Design、Test Specification等について、

- Document Node
- Document内部のKnowledge Node

を必要に応じて分ける。

例えば、

DesignDocument X  
DEFINES  
Function A

のようなRelationを持つ。

---

# 21. Code GraphはSource Codeから再生成可能にする

[DECIDED]

Code Graphを正本にしない。

基本的には、

Source Code  
→ Code Parser / Analyzer  
→ Code Graph

として生成する。

Source Code変更後にCode Graphだけを手修正しない。

---

# 22. Code Graphの生成範囲

[PROVISIONAL]

PoC初期から全Repositoryの全SymbolをGraph化する必要はない。

まず問い合わせCaseに関連する範囲で、

- Module
- Class
- Function
- Call
- SQL
- Table Access

等を抽出する方式も許容する。

---

# 23. Code Graphの3レベル

[PROVISIONAL]

Code Graphは少なくとも以下を概念的に分ける。

## Structure Graph

- Module
- Class
- Function
- Contains

## Dependency / Call Graph

- CALLS
- IMPORTS
- DEPENDS_ON

## Data Access Graph

- Function READS Table
- Function WRITES Table
- Function EXECUTES SQL

Data Access GraphはData Flow GraphへのBridgeとなる。

---

# 24. Code GraphとDomain Functionを接続する

[DECIDED]

Code Graph単独では運用保守Knowledgeとして不十分である。

必要に応じて、

Function  
IMPLEMENTED_BY  
Code Function

というBridge Relationを持つ。

このRelationによって、

> このCodeは何の業務機能を実現しているのか

を追跡できる。

---

# 25. Code GraphとTestを接続する

[PROVISIONAL]

可能であれば、

Code Function  
COVERED_BY  
TestCase

または、

Function  
TESTED_BY  
TestCase

等のRelationを持たせる。

Test Coverage Toolと業務Test Caseは別概念であるため、命名・Schemaは後続検討する。

---

# 26. Data Flowの自動抽出

[PROVISIONAL]

Data Flowの一部はSource Codeから自動抽出できる可能性がある。

例：

- SQLからREADS / WRITES Table
- File IOからREADS File
- API ClientからCALLS External API
- ORM MappingからTable Relation
- Batch定義からJob Dependency

ただし、Codeだけでは意味が取れない情報も多い。

---

# 27. Data FlowのHuman / Document Knowledge

[DECIDED]

Data FlowにはDocumentやHuman Knowledgeから得る情報も必要になる。

例：

- Fileの業務上の意味
- 日次 / 月次処理
- External System名
- Business Date
- 手動Operation
- 集計目的

したがってData Flow RelationにはSource Typeを持たせる。

---

# 28. Data Flowの粒度

[OPEN]

PoCでは、どこまで細かくData Flowを表現するかは未確定。

候補：

- System Level
- Component Level
- Table Level
- Column Level
- Field Level

Column / Field LevelはGraph量が急増するため、実問い合わせで必要性を確認してから採用する。

---

# 29. Table / Column Relation

[PROVISIONAL]

Column Levelが必要な場合、

Table  
CONTAINS  
Column

Function  
READS  
Column

等を表現できる。

ただしPoCではTable Levelを基本候補とする。

---

# 30. Case Graph

[DECIDED]

Case自体もNodeとして扱うことを検討する。

例：

Case  
AFFECTS  
Function

Case  
INVESTIGATED_IN  
Code Function

Case  
EVIDENCED_BY  
TestCase

Case  
SIMILAR_TO  
PastInquiry

これにより過去Caseとの再利用が可能になる。

---

# 31. Case GraphとSources Checked

[DECIDED]

Graph上にRelationが存在することと、今回のCaseで確認したことを区別する。

例えば、

Case  
CHECKED_SOURCE  
DesignDocument

等の調査実績Relationを別に持つことを検討する。

---

# 32. Work Item-Centered Subgraphの生成

[PROVISIONAL]

Current Work ItemとCurrent Objectiveに対して、

- 1 hop
- 2 hop
- Relation Type filter
- Knowledge Layer filter
- Time filter

等でSubgraphを生成できることが望ましい。

既定値は以下とする。

```text
View: Work Item
Scope: Related to current Work Item
Time: Current only
Depth: 2
```

利用者が明示的に操作した場合のみ、Entire project、Historical、Depth 3へ広げる。

---

# 33. Graph Traversal例

[PROVISIONAL]

問い合わせ：

> 月次画面に対象データが表示されない

場合、以下のようなTraversalが考えられる。

1. Case → AFFECTS → Screen
2. Screen → USES → API
3. API → IMPLEMENTED_BY → Code Function
4. Code Function → READS → Table
5. Table → WRITTEN_BY → Batch
6. Batch → READS → Input File
7. Function → TESTED_BY → TestCase
8. Function → DEFINED_BY → Design
9. Function → DECIDED_BY → MeetingDecision

すべてのCaseで同じTraversalを実行する必要はない。

## 33.1 Viewをまたぐ縦方向Traversal

[DECIDED]

各Viewを分断しない。Node選択または`Open in ...`操作により、同じStable IDまたはBridge Relationを起点に別Viewへ移動できることを目指す。

```text
Business: 出荷実績登録
    ↓ PART_OF / PROVIDES
Function: CSVアップロード
    ↓ EXPOSED_BY / IMPLEMENTED_BY
System: Upload API
    ↓ READS / WRITES
Data: shipment_raw
    ↓ ACCESSED_BY
Code: upload_service.py::save()
    ↓ COVERED_BY / TESTED_BY
Test: TEST-034
    ↓ EVIDENCED_BY / DECIDED_BY
History: 2024/05/20 設計会議
```

ViewまたはObjectiveの切替後もCurrent Work Item、Evidence、Sources Checked / Not Checked、Missing Knowledge、選択Node、Time Scope、Depthを可能な範囲で保持する。

## 33.2 Test Graph

[DECIDED]

Test GraphはCode Coverageだけではなく、業務期待値を追跡する。

```text
Function
  ├─ TESTED_BY → TestCase
  └─ EXPECTS → ExpectedBehavior

TestCase
  ├─ VERIFIES → ExpectedBehavior
  └─ PRODUCED → TestResult
```

「この仕様はTestされていたか」「どのExpected Behaviorを確認したか」をEvidenceへ戻って判断できることを重視する。

## 33.3 Graph Coverage

[PROVISIONAL]

各ViewのNode数だけでなく、Case調査に必要なBridge Relationの有無をCoverageとして扱う。

候補：

- Case → Function
- Function → System
- Function → Code
- Code → Data
- Function → Test
- Current Specification → Historical Decision

CoverageはAIがRepository全体を理解したという意味ではなく、取得・確認済みRelationの範囲を示す。

---

# 34. Reverse Traversal

[DECIDED]

Graphは原因調査だけでなく影響分析にも利用する。

例えばTable変更時に、

Table  
← READS  
Code Function  
← IMPLEMENTED_BY  
Function  
← USES  
Business Process

と逆方向へ辿り、

> このTable変更がどの業務へ影響するか

を確認する。

---

# 35. Impact Analysis

[FUTURE]

将来的にはChange RequestやRelease時に、

- Affected Code
- Affected Table
- Affected Function
- Affected Test
- Affected Business
- Affected Stakeholder

をGraph探索で取得することを検討する。

---

# 36. Similar Case探索

[PROVISIONAL]

Past Inquiry / Case間にRelationを持たせることで、類似Case探索に利用する。

類似性候補：

- Same Function
- Same Table
- Same Batch
- Same Error
- Same Technical Cause
- Same Historical Decision

Text Embeddingのみで類似性を決めない方式も検討する。

---

# 37. Historical Evidence Graph

[DECIDED]

Historical EvidenceはCurrent KnowledgeとRelationで接続する。

例：

Current Function  
DEFINED_BY  
Current Design

Current Design  
SUPERSEDES  
Old Design

Old Design  
DECIDED_BY  
Meeting Decision

これによりCurrentからHistorical Decisionへ遡れる。

---

# 38. Current / Historical Relation

[PROVISIONAL]

候補Relation：

- SUPERSEDES
- REPLACED_BY
- VALID_FROM
- VALID_UNTIL
- RELEASED_IN
- CHANGED_BY

時間属性だけでなくVersion Relationを持つことを検討する。

---

# 39. Commit Relation

[PROVISIONAL]

Git CommitをGraph Nodeとして利用する場合、

Design  
CHANGED_BY  
Commit

Code Function  
CHANGED_BY  
Commit

TestCase  
CHANGED_BY  
Commit

Release  
INCLUDES  
Commit

のようなRelationを持てる。

PoC初期では全Commit Graph化を必須としない。

---

# 40. Release Relation

[PROVISIONAL]

ReleaseをSpecificationのEffective Timingと接続する。

候補：

Change  
RELEASED_IN  
Release

Release  
AFFECTS  
Function

Release  
INCLUDES  
Commit

Current / Historical判定にも利用できる可能性がある。

---

# 41. Meeting / Decision Relation

[PROVISIONAL]

MeetingとDecisionを分離する場合、

Meeting  
CONTAINS_DECISION  
Decision

Decision  
DEFINES  
Requirement

Decision  
AFFECTS  
Function

等を表現する。

Meeting Minutes自体をRepositoryへ保存できない場合でも、許可済みDecision SummaryのみNode化する方式を検討する。

---

# 42. Responsibility Relation

[PROVISIONAL]

Responsibilityは単純なEdgeだけでは表現しにくい可能性がある。

候補：

Function  
OWNED_BY  
Team

Requirement  
APPROVED_BY  
Stakeholder

ResponsibilityScope  
APPLIES_TO  
Function

ただし契約・責任判断はHuman Review対象とする。

---

# 43. Graphから責任を自動決定しない

[DECIDED]

Graph Relationが存在しても、

> この問題は開発側責任

と自動確定しない。

Graphは、

- Technical Cause
- Current Specification
- Historical Agreement
- Responsibility Scope

等のEvidenceを辿るために利用する。

最終AssessmentはCase WorkflowとHuman Reviewで行う。

---

# 44. Missing Relation

[PROVISIONAL]

Knowledgeは存在するがRelationがない場合、それ自体をKnowledge Gapとして扱えることが望ましい。

例：

- FunctionとTestのRelationがない
- CodeとDesignのRelationがない
- Current SpecとHistorical Decisionが接続されていない

Missing RelationをRepository改善に利用する。

---

# 45. Conflict Relation

[PROVISIONAL]

ConflictをGraph上で表現することも検討する。

例：

Design A  
CONFLICTS_WITH  
Code Behavior B

ただしConflict専用Objectを持つ方式も候補であり、実装は未決定。

---

# 46. GraphとKnowledge State

[DECIDED]

Node / Edgeには、必要に応じてKnowledge Stateを持たせる。

例：

- human_verified
- human_reviewed
- ai_extracted
- ai_inferred
- conflicting
- deprecated

AI推論Edgeを確定Relationとして扱わない。

---

# 47. Stable ID

[DECIDED]

Graph NodeはPathだけでIdentityを持たせない。

File RenameやDirectory変更でGraph Relationが壊れないよう、Stable IDを検討する。

具体方式は未決定。

---

# 48. ID Namespace

[PROVISIONAL]

Node TypeごとにNamespaceを持つ方式を検討する。

例：

- `case:...`
- `function:...`
- `table:...`
- `code:...`
- `test:...`
- `decision:...`

Canonical ID設計は後続で確定する。

---

# 49. Duplicate Detection

[PROVISIONAL]

異なるDocumentから同じFunction / Table / Requirementが抽出される可能性がある。

Graph生成時に、

- Same Name
- Alias
- Same Code Symbol
- Same Provenance
- Human Mapping

等を使いDuplicateを検出することを検討する。

自動Mergeは慎重に行う。

---

# 50. Alias

[PROVISIONAL]

業務名、画面名、Code名が異なる場合がある。

NodeにAliasを持たせることを検討する。

例：

- Business Name
- UI Name
- Technical Name
- Legacy Name

---

# 51. Graph Update

[DECIDED]

GraphはOriginal / Code / Knowledge変更に応じて更新する。

更新契機候補：

- Git Diff
- Document Change
- Code Change
- Human Review
- New Case
- New Decision

---

# 52. Incremental Graph Update

[PROVISIONAL]

PoC後は、変更されたNode / Edgeだけ更新するIncremental方式を基本とする。

例えば、

1. Git Diff取得
2. Changed Source特定
3. Affected Node抽出
4. Relation再生成
5. Stale Relation削除
6. Graph Index更新

を想定する。

---

# 53. Deleted Source

[PROVISIONAL]

Source Fileが削除された場合、関連Node / Edgeを単純消去するかは状況による。

Historical Evidenceとして残す必要がある場合、

- deprecated
- historical
- source_deleted

等で状態を保持することを検討する。

---

# 54. Graph Storageの候補

[OPEN]

PoCでGraphをどこに保持するかは未決定。

候補：

- JSON
- YAML
- SQLite
- NetworkX
- Semantica ContextGraph
- Neo4j
- FalkorDB
- Apache AGE

StorageはLogical Graph Modelに従う。

---

# 55. PoC初期の推奨Storage方針

[PROVISIONAL]

PoC初期では、専用Graph DBを必須としない。

まず、

- Node / Edge Schema
- Retrieval
- Traversal
- Case-Centered Subgraph

の有効性を検証する。

小規模であればJSON / SQLite / NetworkX等でもよい。

---

# 56. Graph DB導入判断

[DECIDED]

以下の要求が強くなった場合にGraph DBを検討する。

- 多段Traversalが頻繁
- Node / Edge数が大規模
- Reverse Impact Analysisが頻繁
- Path Queryが複雑
- Multi-User Query
- Graph Analytics
- Persistent Graph Queryが重要

PoC成功前にGraph DB導入を目的化しない。

---

# 57. Vector Searchとの役割分担

[PROVISIONAL]

Vector SearchとGraph Searchは別の役割を持つ。

## Vector Search

- Text Similarity
- Similar Inquiry
- Relevant Document候補

## Graph Search

- Known Relation
- Dependency
- Impact
- Evidence Chain
- Multi-hop Traversal

Hybrid Retrievalを将来検討する。

---

# 58. Full Text Searchとの役割分担

[DECIDED]

Graphだけですべての検索を行わない。

Full Text Searchは、

- Error Message
- File Name
- Requirement Keyword
- Exact Term

等に有効である。

Graph、Full Text、Code Search、Semantic Searchを用途に応じて組み合わせる。

---

# 59. GraphRAGの位置付け

[FUTURE]

GraphRAGを採用する場合でも、GraphRAG自体を目的にしない。

Caseに必要なSubgraphとEvidenceをLLM Contextへ提供する手段として評価する。

---

# 60. Semanticaの利用候補

[PROVISIONAL]

Semanticaは以下のGraph Infrastructure候補として評価できる。

- Knowledge Graph
- Provenance
- Temporal Graph
- Conflict Detection
- Deduplication
- Context Graph
- Decision
- MCP

ただし本ProjectのNode / Edge / Domain OntologyをSemanticaの内部Schemaへ従属させない。

---

# 61. Semantica Adapter

[PROVISIONAL]

Semanticaを採用する場合、概念的には以下の境界を持たせる。

Maintenance Domain Graph  
→ Adapter  
→ Semantica Graph Infrastructure

これによりSemanticaを交換可能にする。

---

# 62. Code Graph Toolの利用候補

[PROVISIONAL]

既存Code Graph ToolやParserを利用する場合も、生成結果を直接本Projectの正本Schemaにしない。

Code Graph Adapterを介して、

- Module
- Class
- Function
- Call
- Table Access

等を本ProjectのLogical Node / EdgeへMappingする。

---

# 63. Graph Schema Versioning

[PROVISIONAL]

Node TypeやRelation Typeが変更される可能性があるため、Graph SchemaにVersionを持たせることを検討する。

例：

- schema_version
- generated_by
- generated_at

---

# 64. Graph Validation

[PROVISIONAL]

Graph生成後に以下をValidateすることを検討する。

- Node ID重複
- Unknown Relation Type
- Dangling Edge
- Missing Provenance
- Invalid Type Combination
- Deprecated Source Reference

---

# 65. Relation Type Validation

[PROVISIONAL]

例えば、

Function TESTED_BY TestCase

は妥当だが、

Stakeholder READS Table

は通常不自然である。

Relation TypeごとにSource Type / Target Type制約を持たせることを検討する。

---

# 66. Human Reviewが必要なRelation

[PROVISIONAL]

特に以下はHuman Review優先度を上げる。

- Business ↔ Function
- Requirement ↔ Function
- Meeting Decision ↔ Requirement
- Responsibility Scope
- Current / Historical
- AI推論Relation

Code CALLS等の機械的Relationより業務意味Relationの方がReview価値が高い。

---

# 67. Graph Visualization

[POC-SHOULD]

Graph可視化は調査支援として利用する。

ただし、Repository全体の巨大Graphを表示することを基本としない。

Current CaseのSubgraphを表示する。

---

# 68. Graph UIで見せたい情報

[PROVISIONAL]

Node選択時に以下を確認できることが望ましい。

- Type
- Title
- Summary
- Source
- Provenance
- Version
- Knowledge State
- Related Nodes
- Related Case
- Last Updated

---

# 69. Edge UIで見せたい情報

[PROVISIONAL]

Edge選択時に以下を確認できることが望ましい。

- Relation Type
- Source Node
- Target Node
- Evidence
- Extraction Method
- Review State
- Effective Date

---

# 70. Case GraphとCoverage

[PROVISIONAL]

Case GraphをCoverage表示にも利用できる。

例えば、

- Functionまでは確認済み
- Codeまで確認済み
- Testは未確認
- Historical DecisionはAccess不可

等をGraph上で表現することを検討する。

---

# 71. Graphから「調査完了」を自動判定しない

[DECIDED]

Graphに一定数Nodeが存在することを理由に、調査完了と判断しない。

調査完了条件はCase Workflowで定義する。

GraphはEvidence探索・Coverage確認の補助とする。

---

# 72. GraphとCodex Session

[PROVISIONAL]

Codex Session内で確認したSourceやRelationを、一時的なInvestigation Graphとして扱うことを検討する。

ただし、Session内の仮説RelationをそのままPersistent Graphへ保存しない。

Human ReviewまたはEvidence確認後に昇格する。

---

# 73. Investigation Graph

[PROVISIONAL]

一つのCaseについて、

- What was checked
- What was found
- What is still unknown
- Which hypothesis was rejected

を表すInvestigation Graphを持つ可能性がある。

これはDomain Graphの正本Relationとは別に扱うことを検討する。

---

# 74. Persistent Relationへの昇格

[PROVISIONAL]

Codex調査中に発見したRelationは、

1. Sessionで候補Relationとして生成
2. EvidenceへLink
3. Human / RuleでReview
4. Persistent Relationへ保存

というFlowを検討する。

---

# 75. GraphによるMissing Knowledge検出

[PROVISIONAL]

Expected RelationがないことからKnowledge Gapを検出できる可能性がある。

例：

Functionに、

- Design
- Test
- Implementation

のいずれかが存在しない。

ただし、すべてのFunctionに同じRelationが必須とは限らないため、Project Ruleとして定義する。

---

# 76. GraphによるRepository Quality評価

[FUTURE]

将来的に、

- Orphan Node
- Missing Test
- Missing Design
- Unlinked Past Inquiry
- Conflicting Current Specs

等をRepository Quality指標として利用することを検討する。

---

# 77. GraphのSecurity

[DECIDED]

OriginalをMaskしても、Graph Relationからセンシティブ情報が推測できる可能性がある。

そのためGraph Node / Edgeにも、

- Security Classification
- Access Policy

を持たせることを検討する。

---

# 78. Restricted Node

[PROVISIONAL]

Codexから参照不可のMeeting等について、

Nodeの存在だけ表示する

または

Summaryのみ表示する

といった制御を可能にする。

例えば、

Historical Meeting Decision  
[Access Restricted]

という存在だけCaseに示すことも考えられる。

---

# 79. Graph Export

[FUTURE]

GraphをJSON等でExportできることを検討する。

目的：

- Debug
- Review
- Migration
- Tool Replacement
- Backup

特定Graph DB専用Formatだけにしない。

---

# 80. Graph Rebuild

[DECIDED]

Persistent Runtime Graphを削除しても、可能な限り以下から再生成できることを目標とする。

- Source Code
- Original Documents
- AI-Ready Knowledge
- Config
- Schema
- Human Reviewed Relations

---

# 81. Human Reviewed Relationの扱い

[PROVISIONAL]

Humanが明示的に設定したDomain Relationは、Codeから再生成できない場合がある。

そのため、

> Pure Derived Relation

と

> Human Curated Relation

を区別する。

Human Curated RelationはRepository上のPersistent Knowledgeとして保持することを検討する。

---

# 82. Graph Dataの分類

[PROVISIONAL]

Graph Relationを以下に分けることを検討する。

## Generated

Code / Parserから再生成可能。

## Extracted

DocumentからAI / Parserが抽出。

## Inferred

AI推論。

## Curated

Humanが確認・設定。

これにより再生成時の扱いを変えられる。

---

# 83. Rebuild時のHuman Relation

[DECIDED]

Graph全体を再生成してもHuman Curated Relationを失わない構造にする。

Generated Relationだけを再生成対象とする方式を検討する。

---

# 84. PoCで実装すべき最小Graph

[PROVISIONAL]

Golden Sample Inquiryで必要な範囲だけ実装する。

最低候補：

- Case
- Function
- Code Function
- Table
- Test
- Past Inquiry
- Evidence

Relation候補：

- AFFECTS
- IMPLEMENTED_BY
- READS / WRITES
- TESTED_BY
- EVIDENCED_BY
- SIMILAR_TO

Historical Meetingを利用可能な場合はDecision Relationを追加する。

---

# 85. PoCで実装しなくてよいもの

PoC初期では以下を必須としない。

- 全Source Codeの完全AST Graph
- 全Column Level Data Lineage
- 全Commit Graph
- 全MeetingのKnowledge Graph
- Full Ontology Reasoning
- Graph DB Cluster
- Graph Analytics Dashboard
- GNN
- Automatic Responsibility Decision

---

# 86. Golden Sampleで確認するGraph Value

[DECIDED]

Golden Sampleで以下を確認する。

1. InquiryからFunctionへ到達できるか
2. FunctionからCodeへ到達できるか
3. CodeからDataへ到達できるか
4. FunctionからTestへ到達できるか
5. Past Inquiryへ到達できるか
6. Historical Evidenceが必要であることを示せるか
7. Evidence Sourceへ戻れるか
8. Missing Relation / Missing Knowledgeを認識できるか

---

# 87. Graph導入の成功条件

Graph導入が成功した状態とは、

> Graphが大きくなった状態

ではない。

以下が成立することを重視する。

- Inquiry調査経路を短縮できる
- Evidenceへ戻れる
- Codeと業務を接続できる
- Data Flowを追える
- Past Inquiryを再利用できる
- Impact Analysisへ拡張可能
- Missing Knowledgeを発見できる

---

# 88. Graph導入の失敗パターン

以下を避ける。

## Everything is a Node

すべてのFile / Paragraph / Variableを無目的にNode化する。

## Generic Relations Only

`RELATED_TO`だけでGraphを作る。

## No Provenance

Edgeがなぜ存在するか分からない。

## Code Graph Only

Code構造は分かるが業務・仕様と接続されない。

## Domain Graph Only

業務・資料は分かるが実装へ到達できない。

## No Data Flow

Call Graphだけでデータ起因調査ができない。

## Graph DB First

Query要件前にGraph DB導入が目的になる。

## AI Inference as Fact

推論EdgeをHuman Verifiedとして扱う。

---

# 89. Graph実装前に決めるべきこと

[DECIDED]

Storage選定前に以下を決める。

1. Golden Sampleで必要なNode Type
2. Golden Sampleで必要なRelation Type
3. Stable ID
4. Provenance
5. Review State
6. Current / Historical
7. CaseとのRelation
8. Graph Update方法

---

# 90. Current Open Questions

[OPEN]

## Code Graph Tool

どのParser / Toolを利用するか。

## Data Flow Extraction

Code解析だけでどこまで抽出できるか。

## Column Level

必要か。

## Stable ID

具体方式。

## Relation Storage

JSON / SQLite / NetworkX / Semantica / Graph DB。

## Graph Schema Format

YAML / JSON等。

## Human Curated Relations

物理保存方式。

## Current / Historical Version Graph

具体Schema。

## Graph Visualization Library

目的別Viewと共通Projection Contractを実現できるLibrary候補、Layout、性能、Accessibilityをどう評価するか。Graph UI自体のPoC実装要否とは分けて判断する。

---

# 91. 後続ドキュメントへの引き継ぎ

## `08_DOCUMENT_INGEST_AND_TRANSFORM.md`

- DocumentからNode / Edgeをどう抽出するか
- Provenance
- Source Mapping
- Relation Extraction
- Validation

## `09_CASE_INVESTIGATION_WORKFLOW.md`

- Case Graphをいつ作るか
- Sources Checked
- Investigation Graph
- RelationのHuman Review

## `10_AGENT_AND_SKILL_ARCHITECTURE.md`

- Code Graph探索Skill
- Evidence Traversal Skill
- Impact Analysis Skill
- Graph Query Toolの利用責務

## `11_SECURITY_AND_GOVERNANCE.md`

- Restricted Node / Edge
- Sensitive Relation
- Meeting Decision Access

## `12_RUNTIME_AND_STORAGE.md`

- JSON / SQLite / NetworkX / Graph DB
- Graph Rebuild
- Incremental Update
- Runtime Persistence

## `13_UI_AND_DEVELOPER_EXPERIENCE.md`

- Work Item-Centered Graph
- Node / Edge Detail
- Coverage View
- Timelineとの連携

---

# 91.1 User Action・Execution・Artifact Relation

[DECIDED]

ユーザー操作とシステム実行、生成ファイルを同じNodeとして混同しない。

```text
User --PERFORMED--> UserAction --TRIGGERED--> Execution
Execution --CONSUMED--> InputArtifact
Execution --GENERATED--> OutputArtifact
Execution --READS/WRITES--> Data
```

Graphへ残すUserActionは、Upload、Execute、Approve、Export、Delete、Reprocessなど業務上意味のある操作に限定する。画面遷移や展開・折りたたみなどの細かな操作は、必要な場合のみAudit / Access Logへ記録する。OutputArtifactは既定では保存場所、Checksum、生成元Execution、Input、Status、Retentionを参照し、Human Review後に重要なものだけEvidenceへ昇格する。

Operation / Runbookでは `Operation --HAS_STEP--> OperationStep --USES--> System/Data/Artifact`、Stakeholderでは `Stakeholder --MAINTAINS/OPERATES/APPROVES/CONSULTED_FOR--> 対象` を用いる。Technical Cause、Maintenance Ownership、Contract Scope、Approval、Final Responsibilityは別Relationとして保持し、自動的に同一視しない。

---

# 92. Graph Design Decision Summary

## [DECIDED]

- GraphはRelation Modelとして利用する
- Graph DB採用とは分離する
- Work Item-Centered Subgraphを基本とする。CaseはInquiry / Incident用の互換Subtypeとする
- 1つのCanonical Relation Modelから目的別Graph ViewをProjectionし、View数自体を固定目標にしない
- Work Item / Domain / Function / System / Infrastructure-IaC / Data Flow / Code / Test / Evidence-History / Operation-Runbook / Stakeholder-Responsibilityを意味上分ける
- Functionは提供Capability、Systemは実現・稼働する技術境界、Infrastructure / IaCはSystemを配置するResourceと宣言元として分離する
- 詳細探索用Flat Projectionと層横断理解用Vertical Stackを併用する
- View間をBridge Relationで縦方向に移動できるようにする
- Graph Viewの既定値はCurrent Work Item + Current Objective + Current only + Depth 2とする
- Data Flowを重要視する
- RelationにProvenanceを持たせる
- Code GraphはSource Codeから再生成可能にする
- Code GraphとDomain Functionを接続する
- Technical RelationとResponsibility Decisionを分離する
- Graphから責任を自動確定しない
- Stable IDをPathだけに依存させない
- Human Curated Relationを再生成で失わない
- Graph StorageよりLogical Schemaを先に定義する

## [PROVISIONAL]

- Node Type
- Relation Type
- Code Graph Tool
- Column Level
- Investigation Graph
- Relation Confidence
- Graph Schema Versioning
- Projection Contractの物理API
- Graph Coverage計算方式
- Semantica Adapter
- SQLite / NetworkX等のPoC Storage

## [OPEN]

- Stable ID方式
- Graph Storage
- Code Parser
- Data Flow抽出方式
- Current / Historical Graph Schema
- Human Curated Relationの保存形式

---

# 93. Graph Design Statement

> 本ProjectのGraphは、運用保守Knowledgeを可視化するための装飾ではなく、Work Itemの目的からBusiness、Function、System、Infrastructure / IaC、Data、Implementation、Test、Operation、Stakeholder、Historical Evidenceへ辿るためのRelation Modelとして設計する。Functionは提供Capability、Systemはその実現・稼働境界、Infrastructure / IaCはSystemを配置するResourceと宣言元として分離する。1つのCanonical Relation Modelから必要なViewをProjectionし、詳細Relation用Flat Viewと層横断理解用Vertical Stackを併用する。Current Work Item + Current Objective + Current only + Depth 2を既定値として必要なときだけ範囲を広げる。Work Item ViewはKnowledge Layerではなく各層を横断する作業Contextであり、見積りは基礎Graphではなく関係情報から導出する分析Workspaceとする。各ViewはBridge RelationとStable IDで接続し、すべての重要Node / EdgeにProvenance、Knowledge State、Versionを持たせる。
