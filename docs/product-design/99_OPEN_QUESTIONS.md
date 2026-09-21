# AI-Ready Operations Repository / Codex App
## 99. Open Questions

**File Name:** `99_OPEN_QUESTIONS.md`  
**Status:** Active Decision Backlog  
**Document Role:** Open Questions / Decision Gates / PoC Decision Backlog  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、本Projectでまだ確定していない事項を一箇所に集約し、

> 何が未決定で、いつ、何を確認して、誰が判断すべきか

を管理するためのDecision Backlogである。

各設計Documentには`[OPEN]`、`[PROVISIONAL]`、`[DECIDED]`が存在する。

本Fileでは特に、

- PoC開始前に決める必要があること
- Existing Repository実査後に決めること
- Golden Case / Golden Document実行後に決めること
- Security / Management確認が必要なこと
- Technology Evaluation後に決めること
- Production化まで保留できること

を区別する。

---

# 2. Canonical Open Questions File

[DECIDED]

本ProjectのOpen Questions集約Fileは、

`AI-Ready_Operations_Repository-Codex_App_99_OPEN_QUESTIONS.md`

とする。

一部の既存Document内に、

`16_OPEN_QUESTIONS_AND_DECISION_LOG.md`

という参照が残っている場合、それは本Fileを指すものとして読み替える。

後続Repository実装時に必要であれば参照を一括修正する。

---

# 3. Open Questionの扱い

[DECIDED]

`[OPEN]`は、

> 実装者が自由に決めてよい

という意味ではない。

以下のいずれかを意味する。

- Existing Repository確認が必要
- Golden Caseで実測が必要
- Security / Management判断が必要
- User / Project Owner判断が必要
- Technology PoCが必要
- Production Requirementsが未確定

Codexは`[OPEN]`を勝手にArchitecture Decisionへ昇格させない。

---

# 4. Decision Priority

[DECIDED]

本Fileでは未決事項を以下のPriorityに分ける。

## P0 — PoC開始前に確認必須

Securityや対象Repository等、誤るとPoC自体が不適切になる事項。

## P1 — PoC初期で決定

Golden Caseを成立させるために必要な事項。

## P2 — Golden Case実測後に決定

Graph、Storage、Semantica等、先に固定しない方がよい事項。

## P3 — Production化前に決定

Multi-user、Retention、Enterprise Access等。

---

# 5. Decision Owner Category

[PROVISIONAL]

Decision Ownerは実名ではなくRoleで管理する。

候補：

- Project Owner
- Maintenance Lead
- Repository Owner
- Security / Manager
- Customer Communication Approver
- PoC Developer
- Human Reviewer

実際の担当者名は対象Project側で設定する。

---

# 6. Decision記録Template

[PROVISIONAL]

重要Decisionを確定する際は最低限以下を記録する。

- Question
- Decision
- Status
- Decided By
- Decided At
- Evidence / Reason
- Affected Documents
- Follow-up Action

Architectureへ大きな影響がある場合はADR化も検討する。

---

# 7. P0 — Existing Repository Access

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Repository Owner / PoC Developer

## Question

PoC対象となる実Repositoryはどれか。

## 確認事項

- Repository Root
- Branch
- Main Source Code
- Inquiry Folder
- Test Specification
- Design / Operation Documents
- Git History
- Existing AI / Codex Files

## Decision Trigger

PoC開始時のRepository Discovery。

## Default

Repositoryを確認する前にArchitectureを物理Directoryへ固定しない。

---

# 8. P0 — Existing Repository Structure

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Repository Owner / PoC Developer

## Question

現在のRepository構造のうち、どこをそのまま利用し、どこへAI-Ready Overlayを追加するか。

## Candidate

- Keep As-Is
- In-Place Metadata
- Overlay
- Central Index
- Hybrid

## Decision Trigger

Existing Repository実査後。

## Default

全面再編しない。

---

# 9. P0 — Existing Inquiry Folder Mapping

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Question

既存問い合わせFolderをLogical Caseとしてどう扱うか。

## Candidate

- Existing Folder = Case Root
- Existing Folder + Metadata
- Central Case IndexからReference
- New Investigation Summaryのみ追加

## 確認事項

- 問い合わせ本文が残っているか
- 調査内容が残っているか
- Final Responseが残っているか
- Related Code / SQLが残っているか
- Folder命名規則が安定しているか

## Default

既存Folderを先に移動しない。

---

# 10. P0 — Existing Codex Resume / Session Availability

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** PoC Developer

## Question

対象Repositoryに関連するPast Codex Resume / Sessionをどこまで参照可能か。

## 確認事項

- 過去Sessionを開けるか
- Repositoryごとに関連Sessionを判別できるか
- Search可能か
- CaseとのReferenceを残せるか
- Inquiry Folderより詳細なInvestigation Historyがあるか

## Default

利用可能なら引き継ぎSourceとして確認するが、正本にはしない。

---

# 11. P0 — Meeting Minutes: Codex Direct Access

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Security / Manager

## Question

開発時のMeeting Minutes OriginalをCodexへ直接参照させてよいか。

## Why Important

Historical AgreementとResponsibility Assessmentの重要Evidenceになるため。

## Decision Options

- Allowed
- Allowed with Masking
- Human Only
- Prohibited

## Default

確認完了まで直接参照しない。

---

# 12. P0 — Meeting Minutes: Repository Storage

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Security / Manager

## Question

Meeting Minutes Originalを対象Repositoryへ保存してよいか。

## Options

- Original Allowed
- Local Repository Only
- Approved Summary Only
- Reference Only
- Not Allowed

## Default

確認完了まで追加しない。

---

# 13. P0 — Meeting Minutes: Git Storage

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Security / Manager

## Question

Meeting MinutesをGit Historyへ残してよいか。

## 確認事項

- Full Text
- Summary
- Customer Name
- Personal Name
- Email
- Contract / Responsibility Discussion

## Default

未承認Meeting MinutesをGit Commitしない。

---

# 14. P0 — Personal / Customer Information

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Security / Manager

## Question

以下をRepository / Codex / Gitで扱える条件は何か。

- Customer Name
- Personal Name
- Email Address
- Internal System Name
- Customer Identifier

## Candidate Controls

- Masking
- Role Replacement
- Restricted Storage
- Human Only

---

# 15. P0 — Contract / Responsibility Information

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Security / Manager / Maintenance Lead

## Question

Contract、Responsibility、Cost Discussionを、

- Codexへ渡せるか
- Repositoryへ保存できるか
- Gitへ保存できるか

## Default

Human Approval必須。

---

# 16. P0 — Production Data Access

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Security / Manager

## Question

Production DataをCodexへ渡せる条件は何か。

## 確認事項

- Raw Data
- SQL Result
- Masked Record
- Aggregated Summary
- Record IDのみ

## Default

必要最小限、可能ならMasked / Summarized。

---

# 17. P0 — Security Classification

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Security / Manager

## Question

Projectで正式に利用するClassificationは何か。

Candidate：

- public
- internal
- confidential
- restricted
- ai_restricted
- ai_not_allowed

## Default

Organization Policyへ合わせる。

---

# 18. P0 — AI Access Policy

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Security / Manager

## Question

Source Classificationごとに、

- Human Read
- Codex Read
- Agent Read
- Repository Store
- Git Store
- Export

をどう制御するか。

---

# 19. P0 — Golden Case Selection

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Question

PoCで使用する実運用に近い問い合わせはどれか。

## Desired Characteristics

- Raw Inquiryがある
- Code Investigationが必要
- Test Evidenceがある
- Current Specification確認が必要
- 過去CaseとのRelationがある
- 可能ならHistorical Evidenceも関係する
- Security上PoC利用可能

---

# 20. P0 — Golden Document Selection

**Status:** `[OPEN]`  
**Priority:** `P0`  
**Decision Owner:** PoC Developer / Maintenance Lead

## Question

最初にAI-Ready Conversion Contractを作るDocumentはどれか。

## First Candidate

Golden Caseに関連するTest Specification。

## Alternative

- Design Document
- Existing Inquiry Record
- Release Document

---

# 21. P1 — Persistent Investigation Knowledge Location

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** Repository Owner / PoC Developer

## Question

Human ReviewedなCase Knowledgeを物理的にどこへ保存するか。

## Candidate

- Existing Inquiry Folder
- AI-Ready Overlay
- Central Case Directory
- Approved External Storage

## Default

Existing Repositoryを最小限変更する方式を優先する。

---

# 22. P1 — Persistent Case Format

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer

## Question

Caseの正式保存Formatを何にするか。

## Candidate

- Single Markdown
- Markdown + YAML
- Markdown + JSON
- Existing File + Metadata

## Required Properties

- Human Readable
- Machine Searchable
- Git Diff Friendly
- Evidence Reference
- Human Review State

---

# 23. P1 — Canonical AI-Ready Format

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer

## Question

Document Derived KnowledgeのCanonical Physical Formatをどうするか。

Candidate：

- `content.md`
- `metadata.yaml`
- `relations.json`

## Important

Logical Knowledge ModelをPhysical Formatへ従属させない。

---

# 24. P1 — Normalized Intermediate Representation Schema

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer

## Question

Excel / Word / PPT / PDFを共通Domain Transformationへ渡すIntermediate Schemaをどう定義するか。

## Decision Trigger

Golden Document Conversion Contract作成時。

## Default

Golden Documentに必要なPrimitiveだけ実装する。

---

# 25. P1 — Stable ID Strategy

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer

## Question

Knowledge Node / Case / RelationにどのStable ID方式を使うか。

## Candidate

- Existing Business ID
- Requirement ID
- Test Case ID
- Deterministic ID
- UUID + Mapping
- Composite Key

## Requirement

File Rename / MoveだけでIdentityが変わらないこと。

---

# 26. P1 — Current Specification Detection

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Question

複数Document / VersionからCurrent Specificationをどう判定するか。

## Candidate Evidence

- Release
- Document Version
- Effective Date
- Git History
- Test
- Human Review

## Default

Modified DateだけでCurrent判定しない。

---

# 27. P1 — TestCase Granularity

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Question

Existing Test Specificationをどの粒度でKnowledge化するか。

## Candidate

- Sheet
- Scenario
- Test Case
- Row
- Section

## Decision Trigger

Golden Test Specification実査。

---

# 28. P1 — Excel Formatting Semantics

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer / Human Reviewer

## Question

色、Border、Merge、Hidden等をMeaningful Metadataとして保持する必要があるか。

## Decision Trigger

Golden Excel実査。

---

# 29. P1 — Design Document Structure

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer

## Question

Existing Designの主Formatと構造は何か。

- Excel
- Word
- PowerPoint
- PDF
- Markdown

## Impact

Parser / Chunking / Provenance。

---

# 30. P1 — PowerPoint Diagram Extraction

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer

## Question

Diagramの、

- Shape
- Connector
- Position

まで構造化する必要があるか。

## Default

PoCでは重要Diagramだけ必要性を評価する。

---

# 31. P1 — PDF / OCR Requirement

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer

## Question

Scanned PDF / OCRがPoC対象に必要か。

## Default

Golden Caseに不要なら後回し。

---

# 32. P1 — Inquiry / Case Migration Rule

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Question

既存InquiryをどこまでPersistent Case ModelへMigrationするか。

## Candidate

- Golden Caseのみ
- Important Casesのみ
- New Casesのみ
- 全Case

## Default

PoCではGolden Case + 必要なPast Caseだけ。

---

# 33. P1 — Codex Resume to Persistent Knowledge

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer / Human Reviewer

## Question

Past Resumeから何を抽出・保存するか。

Candidate：

- Sources Checked
- Major Investigation Steps
- Technical Cause
- Missing Knowledge
- Open Questions
- Final Result

## Default

Session全文を保存しない。

---

# 34. P1 — Relation Type Minimal Set

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer

## Question

Golden Caseで必要なRelation Typeは何か。

First Candidate：

- AFFECTS
- IMPLEMENTED_BY
- READS
- WRITES
- TESTED_BY
- EVIDENCED_BY
- SIMILAR_TO
- DEFINED_BY

---

# 35. P1 — Graph Node Minimal Set

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer

## First Candidate

- Case
- Function
- Code Function
- Table
- TestCase
- Evidence
- PastInquiry

Historical Evidence利用可能時：

- Decision

---

# 36. P1 — Data Flow Granularity

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer / Maintenance Lead

## Question

Data Flowをどこまで細かく扱うか。

Candidate：

- System
- Component
- Table
- Column
- Field

## Default

PoCではTable Levelを第一候補とする。

---

# 37. P1 — Column Level Lineage

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer

## Question

Column / Field Level RelationがGolden Caseで必要か。

## Default

必要性が実証されるまで実装しない。

---

# 38. P1 — Human Review UX

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Question

Human ReviewをどのInterfaceで行うか。

Candidate：

- Markdown Review
- CLI
- Local Web UI
- VS Code View

## Required

責任・仕様・Customer Responseを明示的に承認可能。

---

# 39. P1 — Case Status Schema

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** PoC Developer

## Candidate

- received
- investigating
- awaiting_external_evidence
- assessing
- needs_human_review
- reviewed
- resolved
- blocked

Golden Caseで必要なものだけ採用する。

---

# 40. P1 — Coverage Schema

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Candidate Areas

- Business
- Function
- System
- Data
- Implementation
- Test
- Current Design
- Historical Evidence
- Responsibility

## Candidate States

- checked
- partial
- not_checked
- restricted
- not_applicable

---

# 41. P1 — External Evidence Recording

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Question

NotebookLM等をHumanが確認した結果をCaseへどの粒度で残すか。

Candidate：

- Source ID
- Date
- Topic
- Approved Summary
- Human Checked
- Access State

---

# 42. P1 — Knowledge Promotion Rule

**Status:** `[OPEN]`  
**Priority:** `P1`  
**Decision Owner:** Human Reviewer / PoC Developer

## Question

Case固有KnowledgeからGeneral Knowledgeへ何を昇格させるか。

## Requirement

- Evidenceあり
- Human Review済み
- Existing KnowledgeとのConflict確認済み

---

# 43. P2 — Runtime Storage

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Question

PoC Runtime Storeを何にするか。

Candidate：

- JSON
- SQLite
- NetworkX
- Semantica
- Graph DB

## Current Leaning

SQLiteまたは軽量File-based Runtime。

## Decision Trigger

Golden CaseのQuery要件確認後。

---

# 44. P2 — SQLite Adoption

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Question

SQLiteを以下へ使うか。

- Knowledge Index
- Relation
- Processing State
- Case Index
- Runtime Metadata

## Default

有力候補だが固定しない。

---

# 45. P2 — Runtime Directory

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer / Security

## Question

Runtimeを、

- Repository内Ignored Directory
- Repository外Local App Data

のどちらへ置くか。

## Decision Factors

- Security
- Portability
- Developer Debug
- Repository Cleanliness

---

# 46. P2 — Derived Knowledge Git Management

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** Repository Owner / Security / PoC Developer

## Question

AI-Ready Derived KnowledgeをGit Commitするか。

## Benefits

- Diff Review
- History
- Audit

## Risks

- Noise
- Sensitive Derived Data
- Repository Size

---

# 47. P2 — Persistent Case Git Management

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** Repository Owner / Security

## Question

Persistent Investigation KnowledgeをGit管理するか。

Security Classificationごとに異なる可能性がある。

---

# 48. P2 — Graph Storage

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Candidate

- JSON
- SQLite
- NetworkX
- Semantica
- Neo4j
- Other Graph DB

## Default

Dedicated Graph DBをPoC必須にしない。

---

# 49. P2 — Graph DB Adoption

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Adopt Only If

- Multi-hop Queryが頻繁
- Relation数が大きい
- Reverse Impact Analysisが重要
- Lightweight Storeでは不足

---

# 50. P2 — Vector Search

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Question

Vector SearchがGolden Case / Similar Inquiryで必要か。

## Default

Full Text / Metadata / Graphで不足する場合に追加する。

---

# 51. P2 — Search Architecture

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Candidate Combination

- Repository Search
- Full Text
- Metadata
- Code Search
- Graph
- Vector

Golden Caseで必要な最小構成を選ぶ。

---

# 52. P2 — Code Graph Tool

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Question

Code Graph生成に何を使うか。

Candidate：

- Semantica CodeParser
- Language-native Parser
- Custom Static Analysis
- Existing Code Graph Tool

## Requirement

Project Logical GraphへAdapterできること。

---

# 53. P2 — Data Flow Extraction Tool

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Question

以下をどこまで自動抽出できるか。

- SQL Table Access
- File IO
- API
- Batch
- Configuration

不足部分はHuman / Document Knowledgeで補う。

---

# 54. P2 — Graph Visualization

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer / Maintenance Lead

## Question

PoC UIにGraph Visualizationを含めるか。含める場合、目的別Viewを共通Projection Contractから表示するために、どのLibrary / Layout / Interactionを採用するか。

## Default

Work Item Subgraphが調査時間を短縮する場合のみ追加する。追加時は`Work Item`を初期表示し、Golden Objectiveで価値の高い2 View以上を切り替えて評価する。目的別Viewすべての完全実装はPoC必須としない。

---

# 55. P2 — Timeline UI

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Question

Golden Caseで、

- Runtime Timeline
- Historical Decision Timeline

のViewが有用か。

---

# 56. P2 — UI Technology

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Candidate

- VS Code Extension / Webview
- Local Web App
- CLI
- Hybrid

## Default

PoCで最も軽量な方法を選ぶ。

---

# 57. P2 — Git Diff UI Integration

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Question

Persistent Knowledge Review時にUIからGit Diffを見せる価値があるか。

PoC必須ではない。

---

# 58. P2 — Review Agent

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Question

PoCでReview Agentを分離するか。

## Default

まずSingle Main Agent + Validation Skillで開始可能。

---

# 59. P2 — Multi-Agent Adoption

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Adopt Only If

- Main Contextが肥大化
- Specialist Promptで品質改善
- 並列調査価値が高い
- Execution Trace分離が有効

## Default

PoCでは必須にしない。

---

# 60. P2 — Skill Definition Format

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Candidate

- Markdown
- YAML
- Code
- Codex-native mechanism

Logical Skill Contractを先に定義する。

---

# 61. P2 — Agent Execution Record Persistence

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer / Security

## Question

詳細Execution Logをどこまで保存するか。

## Default

Detailed LogはRuntime、重要SummaryはPersistent Case。

---

# 62. P2 — Context Package Schema

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Question

Main OrchestratorからSkill / Specialistへ渡す構造を正式化するか。

Golden Caseで必要になった場合に定義する。

---

# 63. P2 — Semantica Version

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Question

PoC評価時点のSemantica Current Versionは何か。

## Required

Version Pinning。

---

# 64. P2 — Semantica Adoption Scope

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Candidate Decision

- Adopt
- Partially Adopt
- Defer
- Reject

## Current Evaluation Priority

1. Parse / Normalize
2. Provenance
3. Graph / Relation
4. Context Query
5. Temporal
6. Conflict
7. MCP

---

# 65. P2 — Semantica AgentContext API

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Verify

- Constructor
- Required `vector_store`
- Query API
- Current Source Code
- Plugin Exampleとの差

Documentationだけで判断しない。

---

# 66. P2 — Semantica RepoIngestor

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Verify

- Ignore
- Incremental
- Rename
- Delete
- Large Binary
- Repository Metadata

---

# 67. P2 — Semantica CodeParser

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Verify

- Supported Language
- Module / Function
- CALLS
- Dependency
- Data Access
- Provenance

---

# 68. P2 — Semantica Excel / PPT / PDF Parsing

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Verify

Golden Documentに対して、

- Structure Preservation
- Source Mapping
- Table
- Sheet / Slide / Page
- Diagram

が十分か。

---

# 69. P2 — Semantica MCP

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Verify

- Local MCP Server
- Codex Integration
- Query
- Provenance
- Security
- Large Result Handling

---

# 70. P2 — Semantica Adapter Boundary

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Candidate

- Parser Adapter
- Graph Adapter
- Provenance Adapter
- Search Adapter
- Context Adapter

一つの巨大Adapterを作る必要はない。

---

# 71. P2 — Semantic Diff

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Question

Document変更で、

- Requirement変更
- Expected Result変更
- Decision変更

を意味的に検出する機能が必要か。

## Default

PoCではGit Diff + Rebuildで開始可能。

---

# 72. P2 — Current / Historical Graph Schema

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Question

Current / Historical / Supersededを、

- Node Attribute
- Edge
- Version Object

のどれで表現するか。

Golden Caseで必要な最小方式を選ぶ。

---

# 73. P2 — Human Curated Relation Format

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Question

Human ReviewedなRelationをどのPersistent Formatへ保存するか。

Runtime Graphだけに保存しない。

---

# 74. P2 — Conflict Representation

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** PoC Developer

## Candidate

- `CONFLICTS_WITH` Relation
- Conflict Object
- Knowledge State

Golden Caseで扱いやすい方式を選ぶ。

---

# 75. P2 — Similar Case Logic

**Status:** `[OPEN]`  
**Priority:** `P2`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Question

Similar Caseを何で判断するか。

Candidate：

- Same Function
- Same Table
- Same Batch
- Same Error
- Same Cause
- Semantic Similarity

Embeddingだけに依存しない。

---

# 76. P3 — Runtime Encryption

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Security

## Question

SQLite / Runtime FileのEncryptionが必要か。

Data Classificationに依存する。

---

# 77. P3 — Runtime Log Retention

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Security / Repository Owner

## Question

以下の保持期間はどの程度か。

- Agent Execution Log
- Transformation Log
- Cache
- Session
- Derived Index

---

# 78. P3 — Persistent Case Retention

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Security / Maintenance Lead

## Question

Inquiry / Investigation Knowledgeの保存期間と削除Ruleは何か。

Git Historyも考慮する。

---

# 79. P3 — Audit Requirement

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Security / Manager

## Question

何をAudit対象とするか。

Candidate：

- Sensitive Source Access
- Human Approval
- Customer Output
- Security Exception
- Policy Version
- AI-generated Decision Material

---

# 80. P3 — Agent RBAC / Access Control

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Security / PoC Developer

## Question

Agent RoleごとのFine-Grained Access Controlが必要か。

PoCではLogical Access Scopeで開始可能。

---

# 81. P3 — Multi-User Runtime

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Project Owner / PoC Developer

## Question

複数Developerが同時利用するArchitectureが必要か。

必要になった場合、

- Shared DB
- Authentication
- Concurrency
- Central Index

を再評価する。

---

# 82. P3 — Multi-Branch Knowledge

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Repository Owner / PoC Developer

## Question

複数BranchのKnowledge / Indexを同時管理する必要があるか。

## Default

PoCではCurrent Checkoutのみ。

---

# 83. P3 — Historical Repository Query

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Maintenance Lead / PoC Developer

## Question

「Release X時点の仕様」を直接Queryする必要があるか。

PoCではGit HistoryからHuman / Toolで追えることを優先する。

---

# 84. P3 — Shared Knowledge Server

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Project Owner / Security

## Question

Local-Firstから中央Knowledge Serviceへ移行する必要があるか。

PoC終了後の利用人数・Repository数で判断する。

---

# 85. P3 — Backup Strategy

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Repository Owner

## Principle

Runtime Backupより、

- Git
- Original
- Persistent Knowledge

のBackupを優先する。

---

# 86. P3 — Production Monitoring

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Project Owner / PoC Developer

## Candidate

- Ingest Failure
- Stale Runtime
- Graph Failure
- Security Block
- Index Lag

Production化時に定義する。

---

# 87. P3 — Setup Assistant / Project Template

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Project Owner

## Question

他Project展開用に、

- Maintenance
- Waterfall
- Agile
- Hybrid

等のTemplate / Setup Assistantを作るか。

PoC対象外。

---

# 88. P3 — Multiple Repository Support

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Project Owner

## Question

将来的に一つのCaseから複数Repositoryを横断する必要があるか。

現PoCではSingle Target Repositoryを基本とする。

---

# 89. P3 — Customer-specific Configuration

**Status:** `[OPEN]`  
**Priority:** `P3`  
**Decision Owner:** Project Owner / Security

## Question

Projectごとの差異をどこまでConfig化するか。

Candidate：

- Document Type
- Security
- Stakeholder
- Agent Policy
- Graph Schema
- Transformer
- Responsibility Vocabulary

---

# 90. PoC開始時の最小Decision Set

[DECIDED]

PoC開始時にすべてのOpen Questionを解決する必要はない。

最初に解決すべき最小Setは以下。

1. Target Repository
2. Golden Case
3. Golden Document
4. Allowed / Restricted Source
5. Meeting Minutes Access Level
6. Production Data利用条件
7. Existing Inquiry Mappingの暫定方針
8. Persistent Caseの暫定保存先
9. Persistent Caseの暫定Format

これ以外はGolden Caseを進めながら決めてよい。

---

# 91. PoC中に意図的に保留する事項

[DECIDED]

以下はGolden Case実測前に確定しないことを推奨する。

- Neo4j採用
- Vector DB採用
- Full Multi-Agent
- Full Graph Visualization
- Full Ontology
- Full Office Conversion
- Semantica全面採用
- Enterprise RBAC

---

# 92. Decision Gate Summary

## Gate A — Repository Discovery

決めるもの：

- Physical Architecture
- Existing Inquiry Mapping
- Golden Case候補
- Golden Document候補

## Gate B — Security / Management

決めるもの：

- Meeting Minutes
- PII
- Contract / Responsibility
- Production Data
- Git Storage

## Gate C — Golden Document

決めるもの：

- NIR
- Canonical Format
- Provenance粒度
- TestCase粒度
- Stable ID暫定方式

## Gate D — Golden Case

決めるもの：

- Minimal Graph
- Search構成
- Persistent Case Format
- Coverage
- Human Review UX

## Gate E — Technology Evaluation

決めるもの：

- SQLite
- Graph DB
- Vector
- Multi-Agent
- Semantica

## Gate F — Production Readiness

決めるもの：

- Retention
- Audit
- Encryption
- Multi-user
- Central Runtime
- Monitoring

---

# 93. Decision Log

以下は、このDocument作成時点で確定している主要DecisionのSummaryである。

## D-001 Existing Repository First

**Status:** `[DECIDED]`

対象Repositoryを実査する前に全面再編しない。

## D-002 Git as Historical Source of Truth

**Status:** `[DECIDED]`

Security上許可されたOriginal / Persistent Knowledge / Config等の履歴管理にGitを利用する。

## D-003 Case-Centered Investigation

**Status:** `[DECIDED]`

File中心ではなくInquiry / Case中心でKnowledgeを取得する。

## D-004 Technical Cause ≠ Responsibility

**Status:** `[DECIDED]`

Technical CauseとSpecification / Responsibility Assessmentを分離する。

## D-005 Human Review Required

**Status:** `[DECIDED]`

Responsibility、Contract、Cost、Customer CommitmentはHuman Approval必須。

## D-006 Codex Resume Is Working History

**Status:** `[DECIDED]`

Codex Resume / Sessionは重要なInvestigation SourceだがPersistent Source of Truthではない。

## D-007 Persist Important Investigation Outside Session

**Status:** `[DECIDED]`

Human Review後の重要な調査成果をCodex Session外へ保存する。

## D-008 Graph Is Relation Model

**Status:** `[DECIDED]`

Graph DBやVisualizationではなくRelation Modelを本質とする。

## D-009 Data Flow Is First-Class

**Status:** `[DECIDED]`

Call GraphだけでなくData Flow Graphを重視する。

## D-010 Runtime Is Rebuildable

**Status:** `[DECIDED]`

SQLite、Graph、Index、Vector等は原則再生成可能にする。

## D-011 Original ≠ Derived

**Status:** `[DECIDED]`

AI-Ready KnowledgeはOriginalの代替ではない。

## D-012 Provenance Required

**Status:** `[DECIDED]`

重要Knowledge / RelationからOriginal Evidenceへ戻れること。

## D-013 Missing Knowledge Is First-Class

**Status:** `[DECIDED]`

不足情報をAI推論で隠さない。

## D-014 Retrieval over Memory

**Status:** `[DECIDED]`

長いSessionやAgent MemoryよりRetrievalを重視する。

## D-015 Agent ≠ Skill

**Status:** `[DECIDED]`

Agentは責務、Skillは再利用可能な能力として分離する。

## D-016 Multi-Agent Is Not PoC Requirement

**Status:** `[DECIDED]`

Golden Case成立前にMulti-Agentを目的化しない。

## D-017 Security Before AI Access

**Status:** `[DECIDED]`

Classification / Masking等をAI利用後ではなく前に適用する。

## D-018 Repository / Git / AI Access Are Separate Decisions

**Status:** `[DECIDED]`

Repositoryへ置けること、Gitへ残せること、Codexが読めることを別判断とする。

## D-019 Semantica Is Evaluation Candidate

**Status:** `[DECIDED]`

SemanticaをProject全体の正本Architectureとして固定しない。

## D-020 Golden Case First

**Status:** `[DECIDED]`

一件の代表問い合わせをEnd-to-Endで成立させてから拡張する。

---

# 94. Decisions To Record During PoC

[DECIDED]

PoC中に最低限以下をDecisionとして記録する。

- Golden Case
- Golden Document
- Physical Repository Strategy
- Persistent Case Format
- Persistent Case Location
- Stable ID暫定方式
- Minimal Node / Relation
- Runtime Storage
- Search Strategy
- Meeting Minutes Access Level
- Semantica Evaluation Result

---

# 95. Open Question Update Rule

[DECIDED]

Open Questionを解決したら、

1. `[OPEN]`をDecisionへ昇格
2. Decision Reasonを記録
3. Affected Documentを更新
4. 必要ならADR作成
5. 本FileのStatusを更新

する。

---

# 96. Provisional Decision Update Rule

[DECIDED]

`[PROVISIONAL]`は実装済みでも確定とは限らない。

Golden Caseで検証し、

- Keep
- Modify
- Reject

を判断する。

---

# 97. Codex Handoff Rule

[DECIDED]

別PC / Account / Sessionで本Projectを再開するCodexは、最初に以下を行う。

1. Handoff Documentを読む
2. 01〜15の関連Documentを読む
3. 本`99_OPEN_QUESTIONS.md`を読む
4. Existing Repositoryを実査する
5. `[OPEN]`を勝手に確定しない
6. 実Repositoryとの差異を報告する
7. Golden Caseに必要な最小Decisionだけ先に解決する

---

# 98. PoC開始時にCodexが最初に報告すべきこと

[PROVISIONAL]

実Repository確認後、Codexは以下をSummaryする。

- Existing Repository Structure
- Inquiry Folder Pattern
- Test Specification Pattern
- Design Document Pattern
- Available Past Codex Resume
- Security Risk
- HandoffとのMismatch
- Recommended Golden Case
- Recommended Golden Document
- P0 / P1 Open Questions
- Proposed Minimal Changes

---

# 99. Project Completion Perspective

本Open Questions Fileが空になることをProject Completion条件にはしない。

成熟した運用保守Repositoryでも、

- New Security Rule
- New Document Type
- New System
- New Stakeholder
- New Technology

によってOpen Questionは発生する。

重要なのは、

> 未決定であることが見えること

と、

> Decisionの根拠と履歴が残ること

である。

---

# 100. Open Questions Statement

> 本Projectでは、未決事項を実装者の暗黙判断へ委ねず、Existing Repository、Security / Management、Golden Document、Golden Case、Technology Evaluation、Production ReadinessのDecision Gateごとに管理する。PoC開始時にすべてを決めるのではなく、Golden Case成立に必要な最小Decisionだけを先に確定し、Graph DB、Vector Search、Multi-Agent、Semantica等は実測結果に基づいて判断する。Codexは`[OPEN]`を自由な実装判断として扱わず、Evidence・Decision Owner・Decision Triggerを確認したうえでHumanとArchitecture Decisionを確定する。

## 100.1 2026-08-30 Decision Log Addendum

[DECIDED]

- D-021: Case中心をWork Item中心へ一般化し、CaseはInquiry / Incident Subtypeとする。
- D-022: Primary Objectiveは1つ、Secondary Objectivesは複数とし、途中切替でも調査Contextを保持する。
- D-023: UIはPurpose-First、Graphは補助導線とする。
- D-024: Canonical Relation ModelへOperation / RunbookとStakeholder / Responsibility Projectionを追加し、View数は固定しない。
- D-025: Original、Intermediate、Persistent Knowledge、Runtime Index、System-generated Artifactを区別し、単一の曖昧なDeleteを設けない。
- D-026: PoCはAI利用承認済みSourceだけを対象とし、利用者向け分類、Masking、Token Vault、Detokenization、原本復元UIは実装しない。

[OPEN / PRODUCTION]

- ProductionでMasking / Tokenizationが必要となるData範囲、運用Owner、Recovery / Display方式
- Permanent DeleteのApproval、Retention、Legal Hold、Backup連携
- Stakeholder Relationの更新Ownerと、保守担当・契約範囲・承認者・最終責任を別管理するSchema

## 100.2 Graph / IaC Decision Addendum（2026-08-30）

[DECIDED]

- D-027: Functionは提供Capability、Systemはその実現・稼働境界として分離し、Relationで接続する。
- D-028: Terraform等を対象とするInfrastructure / IaC GraphをCanonical Relation ModelのProjectionへ追加する。
- D-029: 平面GraphとVertical Stackを併用し、StackはPresentation Modelとして扱う。
- D-030: Vertical Stackは`Inquiry / Work Item → Objective → Domain / Function → System / Infrastructure → Code / Data Flow / Test → Evidence`を基本順序とする。

[OPEN / PRODUCTION]

- Terraform State / Planへ安全にAccessする実行Identityと最小権限
- DriftのSource of TruthをTerraform refresh、Cloud Inventory、Deployment Recordのどれに置くか
- ProviderごとのResource Type正規化とMulti-Cloud / On-Premise表現
- Vertical Stackの層を案件種別に応じて追加・省略するRule
