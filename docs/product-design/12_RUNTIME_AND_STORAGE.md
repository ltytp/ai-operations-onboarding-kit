# AI-Ready Operations Repository / Codex App
## 12. Runtime and Storage

**File Name:** `12_RUNTIME_AND_STORAGE.md`  
**Status:** Draft  
**Document Role:** Persistent Storage / Runtime State / Git / Index / Rebuild Architecture  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、本Projectで扱う情報を、

- Git
- Repository File
- Persistent Investigation Knowledge
- Codex Session / Resume
- Runtime Database
- Graph Store
- Search Index
- Vector Index
- Cache
- Generated View

のどこへ置くか、その役割と境界を定義する。

本Projectでは、

> Storage Productを先に選ぶ

のではなく、

> どの情報を永続化すべきか、何を再生成可能にすべきか

を先に決める。

---

# 2. Storage Architectureの基本原則

[DECIDED]

以下を基本原則とする。

1. GitはHistorical Source of Truthとして利用する
2. Original Sourceを正本として維持する
3. Human Reviewedな重要KnowledgeをRuntimeだけに置かない
4. Runtime DB / Index / Graphは原則再生成可能にする
5. Codex Session / Resumeを唯一の永続保存先にしない
6. Sensitive DataはSecurity Policyに従ってStorageを分ける
7. Storage TechnologyをLogical Knowledge Modelへ従属させる

---

# 3. Storage Layerの分類

[DECIDED]

Storageを論理的に以下へ分ける。

## Layer 1: Original / Human Source

人間が正式Evidenceとして利用するSource。

## Layer 2: Persistent Knowledge

Human Reviewedで再利用すべきKnowledge。

## Layer 3: Working / Session State

Codex Session、Temporary Investigation Context等。

## Layer 4: Derived Runtime Infrastructure

SQLite、Graph、Search Index、Vector Index等。

## Layer 5: Generated View

HTML、Report、Graph View、Coverage View等。

---

# 4. Original / Human Source

[DECIDED]

Original Source候補：

- Source Code
- Test Specification
- Design Document
- Inquiry Folder
- Release Document
- Operation Manual
- 許可されたMeeting Minutes

Originalは、人間がEvidenceとして戻る対象である。

AI-Ready KnowledgeでOriginalを置き換えない。

---

# 5. Persistent Knowledge

[DECIDED]

Persistent Knowledgeは、

> SessionやRuntimeが失われても残す必要があるHuman Reviewed Knowledge

とする。

候補：

- Case Investigation Summary
- Human Decision
- Final Response
- Human Curated Relation
- Reviewed Business Rule
- Reviewed Function Mapping
- Approved Meeting Summary
- Security / Repository Policy
- Schema
- Agent / Skill Definition

---

# 6. Persistent Investigation Knowledge

[DECIDED]

問い合わせ調査で特に重要なのはPersistent Investigation Knowledgeである。

最低候補：

- Case ID
- Original Inquiry Reference
- Investigation Summary
- Technical Cause
- Current Specification
- Evidence
- Sources Checked
- Sources Not Checked
- Missing Knowledge
- Open Questions
- Human Review
- Final Decision
- Final Response

Codex Sessionを削除しても、この情報は残る構造とする。

---

# 7. Working / Session State

[DECIDED]

Working State候補：

- Codex Session
- Resume
- Temporary Hypothesis
- Current Investigation Context
- Tool Result Cache
- Temporary Query
- Unreviewed AI Result

これらをHuman Reviewed Knowledgeとは区別する。

---

# 8. Codex Resume / Session

[DECIDED]

Codex Resume / Sessionは、

> Detailed Working History

として重要である。

過去調査の引き継ぎ時には利用可能なら参照する。

ただし、

- 保持期間
- 別環境からの参照可否
- 機械的Search可否
- Session削除

等に依存する可能性があるため、Persistent Knowledgeの正本にはしない。

---

# 9. SessionからPersistent Knowledgeへの昇格

[DECIDED]

Case終了時には、Session上の重要な調査成果を整理し、Human Review後にPersistent Storageへ保存する。

概念Flow：

1. Codexで調査
2. Working History蓄積
3. Findings整理
4. Human Review
5. Persistent Investigation Knowledge作成
6. Repository / Approved Storageへ保存
7. Runtime Indexを更新

---

# 10. Session全文を永続化しない

[DECIDED]

Codex Session全体をそのまま正式Case Recordとして保存することを基本としない。

理由：

- 誤仮説を含む
- 冗長
- Sensitive Contextを含む可能性
- AI Working HistoryとHuman Decisionが混在
- Search / Reuseしにくい

保存するのは業務上必要なInvestigation SummaryとEvidenceを中心とする。

---

# 11. Gitの位置付け

[DECIDED]

Gitは、

> Historical Source of Truth

として重要なStorage Layerである。

Gitで保持したいもの候補：

- Source Code
- Config
- Schema
- Policy
- Agent / Skill Definition
- Human Reviewed Case Knowledge
- Human Curated Relations
- Handoff Documents

ただしSecurity Policy上許可された情報に限る。

---

# 12. GitはDatabaseではない

[DECIDED]

Gitを検索・Graph Query用Databaseとして直接利用することを前提にしない。

Gitは、

- Change History
- Version
- Review
- Audit
- Rebuild Source

として利用する。

高速検索・TraversalはRuntime Indexへ委譲できる。

---

# 13. Git管理対象の分類

[PROVISIONAL]

## Git管理を優先する候補

- Source Code
- Handoff Documents
- Config
- Schema
- Policy
- Agent / Skill Definition
- Human Curated Knowledge

## 条件付き候補

- Persistent Investigation Knowledge
- AI-Ready Derived Knowledge
- Human Reviewed Relations
- Approved Meeting Summary

## 原則Git管理しない候補

- Cache
- Runtime Index
- Vector Index
- Temporary Graph
- Session Cache
- Secret
- Credential

---

# 14. Git管理可否とRepository保存可否を分ける

[DECIDED]

以下は別判断とする。

- Repository Working Treeへ置ける
- GitへCommitできる
- Codexが参照できる

例えば、

> Local Repositoryには置けるがGitへCommit禁止

という状態を許容する。

---

# 15. `.gitignore` の利用

[PROVISIONAL]

Local RuntimeやGit禁止Dataについて、`.gitignore`等を利用することを検討する。

候補：

- Runtime DB
- Cache
- Vector Index
- Temporary Extract
- Local Sensitive Source

ただしGit IgnoreだけをSecurity Controlとはみなさない。

---

# 16. Runtime Database

[DECIDED]

Runtime DBは、

> Retrieval / Query / Relation探索を高速化するためのDerived Infrastructure

として扱う。

Runtime DBが消えても、重要Knowledgeが失われない構造を目標とする。

---

# 17. SQLite

[PROVISIONAL]

PoC Runtime StorageとしてSQLiteは有力候補である。

理由：

- Localで利用可能
- Setupが軽い
- SQLで確認しやすい
- File単位で持ち運べる
- Metadata / Relation / Case Indexを扱える
- DeveloperがDebugしやすい

ただし採用決定ではない。

---

# 18. SQLiteの用途候補

[PROVISIONAL]

SQLiteへ保持する候補：

- Document Index
- Knowledge Node
- Relation
- Provenance
- Case Index
- File Version
- Processing Status
- Last Processed Commit
- Agent Execution Summary
- Search Metadata

---

# 19. SQLiteへ置かないもの

[DECIDED]

重要なHuman Decisionや唯一のEvidenceをSQLiteだけに置かない。

SQLiteを削除しても、

- Repository
- Original
- Persistent Knowledge
- Config

から再構築可能にする。

---

# 20. Runtime DBとPersistent Case File

[DECIDED]

Case Knowledgeについて、

> Persistent Case File = 正式・再利用可能なKnowledge

> Runtime DB = Retrieval用Index

という分離を基本とする。

---

# 21. Persistent Case Format

[OPEN]

候補：

- Markdown
- Markdown + YAML
- Markdown + JSON
- Existing Inquiry Folder内のFile
- Central Case Record

Existing Repository実査後に決定する。

---

# 22. Structured Metadata

[PROVISIONAL]

Human-readableなMarkdownに加えて、Machine-readable Metadataを持つ可能性がある。

候補：

- Case ID
- Status
- Related Function
- Date
- Review State
- Classification
- Knowledge State

---

# 23. Graph Storage

[OPEN]

Graph Storage候補：

- JSON
- SQLite
- NetworkX
- Semantica
- Neo4j
- Other Graph DB

Graph DBを導入すること自体を目的にしない。

---

# 24. Graph Runtimeの基本方針

[DECIDED]

Generated Code RelationやDerived GraphはRuntime Infrastructureとして再生成可能にする。

Human Curated RelationはPersistent Knowledgeとして別途保持する。

---

# 25. Human Curated Relation

[DECIDED]

以下のようなRelationは自動再生成できない可能性がある。

- Business → Function
- Function → Requirement
- Historical Decision → Function
- Responsibility Scope

Human Reviewed RelationをRuntime Graphだけに置かない。

---

# 26. Generated Relation

[DECIDED]

Code解析等から再生成可能なRelation候補：

- CALLS
- IMPORTS
- READS
- WRITES
- CONTAINS

これらはRuntimeで再生成可能とする。

---

# 27. Search Index

[DECIDED]

Search IndexはDerived Runtime Infrastructureとする。

候補：

- Full Text Index
- Metadata Index
- Code Index
- Case Index

Index削除でOriginal / Knowledgeが失われないこと。

---

# 28. Full Text Search

[PROVISIONAL]

以下の検索に有効。

- Error Message
- Requirement Keyword
- Function Name
- File Name
- Exact Term

PoCで優先度は高い。

---

# 29. Vector Index

[OPEN]

Vector Searchは以下に有効な可能性がある。

- Similar Inquiry
- Relevant Document
- Semantic Search

ただしPoC初期では必須としない。

---

# 30. Vector IndexをSource of Truthにしない

[DECIDED]

Embedding / Vector Indexは再生成可能なDerived Dataとする。

Original / Human Reviewed KnowledgeをVector DBだけに保持しない。

---

# 31. Vector Index Security

[DECIDED]

Sensitive Sourceから生成したEmbeddingもSensitive Derived Dataとして扱う。

Original削除後にVector Indexだけ残らないようにする。

---

# 32. Cache

[DECIDED]

Cacheは完全にRuntime扱いとする。

候補：

- Parsed Document Cache
- Query Cache
- Embedding Cache
- Graph Query Cache
- Temporary Agent Context

Cacheを削除しても機能的に再生成できること。

---

# 33. Generated View

[DECIDED]

Generated View候補：

- HTML
- Graph Visualization
- Coverage Report
- Timeline
- Case Report

Generated ViewはSource of Truthにしない。

---

# 34. Generated ViewのGit管理

[OPEN]

Generated ViewをGitへCommitするかは、

- Review価値
- Diff価値
- Repository Noise

を見て決める。

PoCではRuntime生成のみでもよい。

---

# 35. Rebuildability

[DECIDED]

Runtime Architectureの重要要件はRebuildabilityである。

最低限、以下からRuntimeを再構築できることを目標とする。

- Source Code
- Original Documents
- Persistent Knowledge
- Config
- Schema
- Human Curated Relations

---

# 36. Rebuild対象

[DECIDED]

再生成可能にする候補：

- SQLite Runtime DB
- Graph Index
- Full Text Index
- Vector Index
- Generated View
- AI-Ready Generated Knowledge

ただしHuman Curated Knowledgeは再生成対象ではない。

---

# 37. Rebuild Command

[PROVISIONAL]

将来的に一つの明示的なRebuild Entry Pointを持つことを検討する。

例の概念：

`rebuild all`

または、

- rebuild knowledge
- rebuild graph
- rebuild search

等。

具体CLIは未決定。

---

# 38. Incremental Update

[DECIDED]

通常運用ではFull RebuildよりIncremental Updateを優先する。

Git Diff等からChanged Sourceを検出する。

---

# 39. Last Processed Revision

[PROVISIONAL]

Runtime側に、

- Last Processed Commit
- Last Scan Time
- Transformer Version
- Schema Version

を保持することを検討する。

---

# 40. Incremental Update Flow

[PROVISIONAL]

1. Current Git Revision確認
2. Last Processed Revision確認
3. Added / Modified / Deleted / Renamed取得
4. Changed Sourceを再処理
5. Related Knowledge更新
6. Relation更新
7. Search Index更新
8. Runtime Status保存

---

# 41. Schema Change

[PROVISIONAL]

Schema Versionが変更された場合、Incremental UpdateではなくFull Rebuildが必要になる場合がある。

MigrationとRebuildを使い分ける。

---

# 42. Transformer Change

[PROVISIONAL]

Parser / Transformer Version変更時、

> どのDerived Knowledgeを再生成すべきか

を判定できるようにする。

---

# 43. Stale Runtime

[DECIDED]

Originalが更新されたがRuntime更新に失敗した場合、

`stale`

であることを明示する。

古いRuntime結果をCurrentとして無条件に利用しない。

---

# 44. Runtime Health

[PROVISIONAL]

Developerが最低限以下を確認できることが望ましい。

- Last Successful Build
- Last Processed Commit
- Stale Files
- Failed Files
- Index Status
- Graph Status
- Runtime DB Version

---

# 45. Startup Validation

[PROVISIONAL]

Codex App起動時に軽量なValidationを行う可能性がある。

候補：

- Runtime DB存在
- Schema Version
- Git Revision一致
- Stale Knowledge
- Security Policy Version

毎回Full Rebuildはしない。

---

# 46. Runtime DBが存在しない場合

[DECIDED]

Runtime DBが存在しなくても、

> Repositoryが壊れている

とはみなさない。

必要に応じて再生成可能であることを正常設計とする。

---

# 47. Git Checkout / Branch Change

[PROVISIONAL]

Branch変更時、Runtime Indexが別Revisionを指している可能性がある。

- Branch
- Commit

をRuntime Metadataへ保持し、不整合を検出することを検討する。

---

# 48. Multi-Branch

[OPEN]

複数BranchのKnowledge Indexを同時管理するかは未決定。

PoCではCurrent Checkoutだけでもよい。

---

# 49. Historical Query

[FUTURE]

将来的に、

> Release X時点のSpecification / Graph

をQueryする要求がある可能性がある。

Git Historyから再構築する方式を検討する。

PoC初期では必須ではない。

---

# 50. Runtime Data Directory

[PROVISIONAL]

Overlay Architectureを採用する場合、RuntimeをGit管理対象と分離したDirectoryへ置くことを検討する。

例：

```text
ops-ai/
├─ knowledge/
├─ config/
└─ runtime/
```

ただし実Directory名はExisting Repository確認後に決定する。

---

# 51. RuntimeをRepository外に置く選択

[PROVISIONAL]

Security / Repository Cleanlinessのため、Runtime DBをRepository Root外へ置く方式も許容する。

例：

- User Local App Data
- Project-specific Local Cache

その場合もProject / CommitとのMappingを保持する。

---

# 52. Portable Runtime

[PROVISIONAL]

Runtime DBを別PCへCopyすることを前提にしない。

可能であれば新環境でRepositoryからRebuildする。

これによりStale / Security Riskを減らす。

---

# 53. Handoff時のStorage

[DECIDED]

別PC / AccountへのHandoffでは、最低限以下があれば設計Contextを復元できることを目標とする。

- Git Repository
- Handoff Documents
- Config / Schema
- Persistent Investigation Knowledge
- Required External Source Reference

Codex SessionやRuntime DBがなくても開始可能にする。

---

# 54. Existing Codex ResumeのHandoff利用

[DECIDED]

既存Codex Resumeが利用可能なら、過去調査の詳細確認に利用する。

ただしHandoff成功条件にResumeの存在を必須としない。

---

# 55. Agent Execution Log

[PROVISIONAL]

Agent / Skillの詳細Execution LogはRuntimeへ保持する可能性がある。

候補：

- Execution ID
- Case ID
- Skill
- Started At
- Completed At
- Sources Checked
- Result Status
- Error

---

# 56. Persistent Execution Summary

[DECIDED]

全Execution LogをGitへ残す必要はない。

Case終了時に必要な、

- Major Investigation Steps
- Sources Checked
- Significant Findings
- Open Questions

だけPersistent Investigation Knowledgeへ残す。

---

# 57. Runtime Log Retention

[OPEN]

詳細Execution Logの保持期間は未決定。

Security / Disk Size / Audit要件から決定する。

---

# 58. Transformation Log

[DECIDED]

Document Ingest処理のLogを保持する。

最低候補：

- Source
- Parser
- Transformer Version
- Result
- Warning
- Error
- Generated Count
- Timestamp

---

# 59. Transformation Logの保存先

[PROVISIONAL]

Runtime DBまたはLocal Log Fileを候補とする。

重要なFailureだけPersistent Issueとして残すことも検討する。

---

# 60. Processing Queue

[FUTURE]

Document量が増えた場合、

- Pending
- Processing
- Completed
- Failed

等のQueue StateをRuntime DBへ持たせることを検討する。

PoC初期では不要。

---

# 61. StorageとSecurity Classification

[DECIDED]

Storage LocationはSecurity Classificationに応じて選択する。

例：

- Git Allowed
- Local Only
- External Only
- Human Only

Knowledge Stateとは別に管理する。

---

# 62. Sensitive Runtime

[DECIDED]

Runtime DB / Search IndexにもSensitive Dataが含まれる可能性がある。

OriginalだけをSecurity対象にしない。

---

# 63. Runtime Access Control

[PROVISIONAL]

必要に応じて、

- Local File Permission
- OS User Boundary
- Encryption

を検討する。

PoC要件はManagement / Security確認結果に依存する。

---

# 64. Encryption

[OPEN]

SQLite / Runtime FileのEncryptionが必要かは未確定。

扱うData Classificationによって決定する。

---

# 65. Backup

[PROVISIONAL]

Runtimeは再生成可能であるため、Runtime DBのBackup優先度は低い。

一方でPersistent KnowledgeはGitまたはApproved StorageでBackupされることが望ましい。

---

# 66. Disaster Recovery

[DECIDED]

重要なRecovery Pathは、

> Runtime Backupから復元する

ではなく、

> Source / Persistent KnowledgeからRuntimeを再構築する

ことを基本とする。

---

# 67. Deletion

[DECIDED]

Sensitive Sourceの削除時には以下を考慮する。

- Original
- Derived Knowledge
- Runtime DB
- Full Text Index
- Vector Index
- Graph
- Cache
- Generated View

一箇所のFile削除だけで完了としない。

---

# 68. Tombstone / Historical Reference

[PROVISIONAL]

Historical Evidenceとして存在したことだけ残す必要がある場合、

- Source Deleted
- Access Removed
- Deprecated

等のTombstoneを保持することを検討する。

---

# 69. Current / Historical Storage

[DECIDED]

CurrentとHistoricalを物理Directoryだけで分けることを前提にしない。

Metadata / Version / Effective Dateでも表現する。

---

# 70. Versioned Knowledge

[PROVISIONAL]

同一Knowledgeについて複数Versionを保持する場合、

- Stable ID
- Revision
- Valid From
- Valid To
- Release

等で管理することを検討する。

---

# 71. StorageとStable ID

[DECIDED]

Stable IDはStorage LocationやFile Pathへ強く依存させない。

Runtime DBを再生成しても同じKnowledge Identityを復元できることが望ましい。

---

# 72. Document Path変更

[PROVISIONAL]

File Rename / Move時、

- Stable ID
- Git Rename Detection
- Source Mapping

を使い、同一Documentとして扱えるようにする。

---

# 73. Runtime Query API

[FUTURE]

UI / AgentからStorageへアクセスするため、内部Query Layerを持つことを検討する。

候補：

- Search Knowledge
- Get Case
- Traverse Relation
- Get Provenance
- Get Coverage

Storage固有QueryをAgent Promptへ直接埋め込まない。

---

# 74. Storage Adapter

[PROVISIONAL]

論理的には以下のAdapterを検討する。

- Case Store
- Knowledge Store
- Relation Store
- Search Store
- Runtime State Store

これによりSQLite / Graph DB等を交換しやすくする。

---

# 75. Semanticaとの境界

[PROVISIONAL]

Semanticaを採用する場合でも、

> Semantica内部Storage = Project Source of Truth

とはしない。

Semanticaは、

- Graph
- Context
- Provenance
- Temporal
- Search

等のRuntime Infrastructure候補とする。

---

# 76. Graph DBとの境界

[DECIDED]

Neo4j等を導入しても、

- Human Curated Knowledge
- Case File
- Policy

をGraph DBだけへ保存しない。

Graph DBはQuery Infrastructureとして扱う。

---

# 77. Vector DBとの境界

[DECIDED]

Vector DBを導入しても、Embeddingしか存在しないKnowledgeを作らない。

Original / Structured Knowledgeへ戻れることを前提とする。

---

# 78. Local-First Runtime

[PROVISIONAL]

Developer向けPoCではLocal-Firstを第一候補とする。

理由：

- Setupが簡単
- Repositoryと近い
- Security Boundaryを理解しやすい
- Debugしやすい
- Infrastructure Costが小さい

Cloud化は必要性確認後とする。

---

# 79. Multi-User Runtime

[FUTURE]

複数担当者が同時利用する段階では、

- Shared DB
- Access Control
- Concurrency
- Central Index

が必要になる可能性がある。

PoC初期では対象外。

---

# 80. Runtime Concurrency

[OPEN]

PoCで同一Repositoryを複数Processから更新する必要があるかは未確定。

SQLite採用時はLockingも評価する。

---

# 81. Storage Observability

[PROVISIONAL]

Developerが以下を確認できることが望ましい。

- Runtime Store Type
- DB Path
- Current Commit
- Schema Version
- Last Build
- Index Status
- Record Count
- Stale Count
- Error Count

---

# 82. Storage Debuggability

[DECIDED]

PoCでは高度な性能よりDebugしやすさを優先する。

「なぜこのKnowledgeが検索されたか」をDeveloperが追えるStorageを選ぶ。

---

# 83. Performance

[PROVISIONAL]

Performance Optimizationは、

- Repository Size
- Query Latency
- Graph Traversal
- Index Build Time

を実測してから行う。

PoC前に分散DBへ進まない。

---

# 84. Runtime Size

[PROVISIONAL]

Index / Graphが大きくなった場合、

- Ignore
- Rebuild
- Cleanup

を簡単に行えるようにする。

Git Repository SizeをRuntime Dataで肥大化させない。

---

# 85. Cleanup

[PROVISIONAL]

Runtime Cleanup候補：

- Cache clear
- Old Execution Log clear
- Rebuild index
- Remove stale temp files

Persistent KnowledgeをCleanup対象にしない。

---

# 86. Runtime Failure

[DECIDED]

Runtime DB破損時に、

> AI調査が永久にできなくなる

構造を避ける。

最低限Repository Search等へFallbackできることが望ましい。

---

# 87. Fallback

[PROVISIONAL]

Runtime Index利用不能時のFallback候補：

1. Direct Repository Search
2. Code Search
3. Original Document Search
4. Manual Evidence Review

機能低下を明示する。

---

# 88. Degraded Mode

[FUTURE]

Runtime一部障害時、

- Graph unavailable
- Vector unavailable
- Full Text only

等のDegraded Modeを表示することを検討する。

---

# 89. PoC推奨Storage Architecture

[PROVISIONAL]

現時点では以下を第一候補とする。

## Persistent

- Existing Git Repository
- Human Reviewed Markdown / Structured Case Knowledge
- Config / Schema

## Runtime

- Local SQLiteまたは軽量Index
- Optional Graph Representation
- Temporary Search / Cache

## Working

- Codex Session / Resume

この構成でGolden Caseを成立させた後、専用Graph DBやVector DBの必要性を判断する。

---

# 90. PoCで最初にSQLiteへ入れる候補

[PROVISIONAL]

PoCでSQLiteを採用する場合、最低限候補：

- source
- knowledge_object
- relation
- case_index
- processing_state

Agent Execution詳細やVectorは後回しでよい。

---

# 91. PoCでGitへ残す候補

[PROVISIONAL]

Security上問題がなければ、

- Handoff Documents
- Config
- Schema
- Golden Case Persistent Investigation Knowledge

をGit管理候補とする。

---

# 92. PoCでRuntimeのみとする候補

[PROVISIONAL]

- Full Text Index
- Graph Index
- Cache
- Processing Log
- Temporary Agent Execution

---

# 93. PoCで必須としないもの

PoC初期では以下を必須としない。

- Neo4j
- Vector DB
- Cloud Database
- Distributed Storage
- Shared Multi-User Runtime
- Automatic Backup System
- Full Historical Query Engine
- Enterprise Encryption Platform

---

# 94. Runtime Acceptance Criteria

PoCで以下を確認する。

1. Runtime DBを削除して再生成できる
2. Persistent Case Knowledgeが失われない
3. Current Git RevisionとRuntime Revisionを確認できる
4. Stale Runtimeを検出できる
5. Search / RelationからOriginal Sourceへ戻れる
6. Codex SessionがなくてもCase結果を再利用できる
7. Sensitive DataをGitへ無条件に残さない

---

# 95. Storage Decision Gate 1: Existing Repository

[DECIDED]

実Repository確認後に、

- Existing Git Usage
- Existing Inquiry Folder
- Large Binary
- Existing DB
- Existing Tooling

を確認する。

---

# 96. Storage Decision Gate 2: Security

[DECIDED]

以下を確認後にPersistent Storage範囲を決定する。

- Meeting Minutes
- Customer Data
- PII
- Responsibility Detail
- Production Data
- Git Policy

---

# 97. Storage Decision Gate 3: Golden Case

[DECIDED]

Golden Caseを実行し、

- Required Query
- Required Relation
- Runtime Size
- Retrieval Speed

を確認してからSQLite / Graph / Vector等を決める。

---

# 98. Storage Decision Gate 4: Multi-User

[FUTURE]

複数担当者利用が必要になった時点で、

- Central Runtime
- Authentication
- Shared Index
- Concurrency

を再評価する。

---

# 99. Runtime and Storage Anti-Patterns

## Runtime DB = Source of Truth

重要KnowledgeをSQLite / Graph DBだけに保存する。

## Resume = Database

Codex Sessionだけに調査結果を残す。

## Commit Everything

Generated Index / CacheまでGit管理する。

## Git Nothing

Review価値のあるHuman KnowledgeまでRuntimeだけにする。

## Graph DB First

Relation要件前にNeo4jを導入する。

## Vector DB First

Semantic Search要件前にVector Infrastructureを増やす。

## No Rebuild Path

Runtime DBが壊れたら復旧不能。

## Security by `.gitignore`

Git IgnoreだけでSensitive Data対策が完了したと考える。

---

# 100. Current Open Questions

[OPEN]

## Persistent Case Format

Markdown / YAML / JSON。

## Persistent Case Location

Existing Inquiry Folder / Overlay / Central。

## SQLite

PoCで採用するか。

## Graph Storage

SQLite / JSON / NetworkX / Semantica / Graph DB。

## Vector Search

必要性。

## Derived Knowledge Git Management

どこまでCommitするか。

## Runtime Directory

Repository内 / Repository外。

## Encryption

必要性。

## Retention

Execution Log / Session / Derived。

## Multi-Branch

対応範囲。

---

# 101. 後続ドキュメントへの引き継ぎ

## `13_UI_AND_DEVELOPER_EXPERIENCE.md`

- Runtime Health
- Case Storage
- Search Status
- Stale Knowledge
- Rebuild操作
- Storage Error表示

## `14_SEMANTICA_EVALUATION.md`

- SemanticaをRuntime Infrastructureとして使う範囲
- Graph / Provenance / Temporal / Context
- Storage Abstraction

## `15_POC_PLAN_AND_ACCEPTANCE_CRITERIA.md`

- PoC Storage選定
- Golden Case Persistence
- Rebuild Test
- Runtime Failure Test

---

# 102. Runtime and Storage Decision Summary

## [DECIDED]

- GitをHistorical Source of Truthとして扱う
- Original Sourceを維持する
- Human Reviewedな重要KnowledgeをRuntimeだけに置かない
- Codex Resumeを唯一の永続保存先にしない
- Persistent Investigation KnowledgeをSession外へ保存する
- Runtime DB / Graph / Indexは原則再生成可能にする
- Generated ViewをSource of Truthにしない
- Human Curated RelationをRuntime再生成で失わない
- Vector / Graph DBをSource of Truthにしない
- Runtime RevisionとGit Revisionの整合性を考慮する
- Security Classificationに応じてStorageを分ける
- Local-FirstをPoC候補とする

## [PROVISIONAL]

- SQLite
- Runtime Directory
- Structured Case Metadata
- Graph Storage
- Agent Execution Log
- Startup Validation
- Storage Adapter

## [OPEN]

- Persistent Case Format
- SQLite採用
- Graph DB必要性
- Vector Search必要性
- Derived KnowledgeのGit管理
- Encryption
- Retention
- Multi-Branch対応

---

# 103. Runtime and Storage Statement

> 本ProjectのStorage Architectureでは、Original SourceとHuman ReviewedなPersistent Knowledgeを正式な再利用対象として維持し、Codex Session / Resumeは詳細なWorking History、SQLite・Graph・Search Index・Vector Index・Cacheは再生成可能なRuntime Infrastructureとして明確に分離する。GitはSource Code、Config、Schema、Human Curated Knowledge等のHistorical Source of Truthとして利用するが、Security Policy上許可された情報だけをCommitする。重要な調査成果をRuntime DBやCodex Sessionだけに残さず、Case終了時にPersistent Investigation Knowledgeとして保存する。PoCではLocal-Firstな軽量Storageから開始し、Golden Caseの実測結果を基にGraph DB、Vector DB、Shared Runtime等の必要性を判断する。

## 103.1 2026-08-30 Runtime / Artifact Refinement

[DECIDED]

RuntimeはWork ItemとObjectiveをContext Keyとして扱うが、Objective切替でIndexやEvidenceを複製しない。System-generated ArtifactはBinary内容をKnowledge Storeへ自動Copyせず、URI / Path、Checksum、Generated By、Input、Status、RetentionをArtifact Registryへ記録する。Runtime Indexの削除はRebuild可能なCache Removal、Persistent Knowledgeの削除はArchive / Restore、OriginalのPermanent DeleteはImpact Previewと権限確認を伴う別Operationにする。UserActionとExecutionを分離し、業務上重要な操作だけAuditへ残す。

## 103.2 Infrastructure Graph Runtime（2026-08-30）

[DECIDED]

Infrastructure / IaC GraphはTerraform HCLと承認済みPlan / State Metadataから再生成可能なRuntime Projectionとする。Resource Stable ID、IaC Source Revision、Environment、Last Plan / Refresh Time、Drift Stateを保持し、Secret値や完全なState PayloadをRuntime Graphへ保存しない。Function、System、Infrastructureは別Node TypeとしてIndexし、Bridge RelationでQueryする。Flat ProjectionとVertical Stackは同じRuntime Relationを異なるLayoutで返すため、Stack専用Databaseや複製Storeを作らない。
