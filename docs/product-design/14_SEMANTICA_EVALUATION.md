# AI-Ready Operations Repository / Codex App
## 14. Semantica Evaluation

**File Name:** `14_SEMANTICA_EVALUATION.md`  
**Status:** Draft  
**Document Role:** Semantica Fit Evaluation / Adoption Boundary / PoC Validation  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、`semantica-agi/semantica`を本Projectへ採用する価値と、採用する場合の境界を整理する。

本ProjectではSemanticaを、

> 運用保守Applicationそのもの

として採用するのではなく、

> Knowledge Infrastructure候補

として評価する。

評価対象は主に以下。

- Ingest
- Parse
- Normalize
- Knowledge Graph
- Provenance
- Temporal
- Conflict
- Deduplication
- Decision / Reasoning
- Search / Context
- Export / Visualization
- MCP
- Codex連携

一方で、Maintenance固有のDomain Model、Case Workflow、Responsibility Assessment、Human Review等は本Project側で所有する。

---

# 2. 現時点の評価結論

[PROVISIONAL]

現時点での評価は以下。

> Semanticaは、本ProjectのKnowledge Infrastructureを構築する際の有力候補である。

ただし、

> Semanticaを採用すれば本Projectの設計が不要になる

わけではない。

特に以下はProject側で設計が必要。

- Maintenance Ontology
- Case Model
- Investigation Workflow
- Responsibility Model
- Stakeholder Model
- Coverage
- Missing Knowledge
- Human Review
- Repository Policy
- Security Policy
- Persistent Investigation Knowledge
- AI-Ready Canonical Model

---

# 3. Semanticaに期待する役割

[PROVISIONAL]

Semanticaを採用する場合、主に以下のInfrastructure Roleを期待する。

1. Document / Repository Ingest
2. Parsing / Normalization
3. Entity / Relation Extraction
4. Knowledge Graph
5. Provenance
6. Temporal Knowledge
7. Conflict Detection
8. Deduplication
9. Context Retrieval
10. Decision / Reasoning Support
11. Export / Visualization
12. MCP / Tool Interface

---

# 4. Semanticaに期待しない役割

[DECIDED]

Semanticaへ以下を丸投げしない。

- 問い合わせWorkflow
- Maintenance Case管理
- Customer / Developer責任分界
- 契約判断
- Human Review
- Customer Response Policy
- Existing Repository再編
- Project固有Security判断
- Investigation Coverage
- Sources Checked / Not Checked
- Codex SessionからPersistent Knowledgeへの昇格

---

# 5. Project Architecture上の位置付け

[PROVISIONAL]

Semanticaを採用する場合の概念Architectureは以下。

Original Source  
→ Semantica / Parser Infrastructure  
→ Project Normalized Intermediate Representation  
→ Project Domain Transformer  
→ Project AI-Ready Knowledge  
→ Semantica Graph / Search / Context または別Runtime  
→ Codex / Agent / UI

重要なのは、

> Semantica内部形式をProjectの唯一のCanonical Modelにしない

ことである。

---

# 6. Why Semantica

[PROVISIONAL]

Semanticaが本Projectと相性がよい理由は、本Projectで必要とする機能領域と重なる部分が多いためである。

特に、

- Knowledge Graph
- Provenance
- Temporal
- Conflict
- Decision
- Context
- Ingest
- Code Parsing

は、本ProjectのArchitectureと方向性が近い。

---

# 7. Graph-Native Infrastructureとの適合

[PROVISIONAL]

本ProjectではGraphを、

> CaseからEvidenceへ辿るRelation Model

として利用する。

SemanticaがGraph-NativeなKnowledge Infrastructureとして利用可能であれば、

- Domain Relation
- Evidence Chain
- Temporal Relation
- Provenance
- Conflict

の実装負担を軽減できる可能性がある。

ただしDomain Ontologyは本Project側で定義する。

---

# 8. Provenanceとの適合

[PROVISIONAL]

本ProjectではProvenanceを重要要件としている。

必要なTraceability例：

- Original File
- Sheet
- Row
- Page
- Slide
- Git Commit
- Transformer Version
- Human Review

SemanticaのProvenance機能がこれらへ適用可能かPoCで確認する。

---

# 9. Temporalとの適合

[PROVISIONAL]

運用保守では、

- Business Date
- Batch Time
- Release Date
- Decision Date
- Meeting Date
- Inquiry Date

等の複数時間軸が重要。

SemanticaのTemporal機能が、

> Current / Historical Specification

や、

> Decision Timeline

に利用できるか評価する。

---

# 10. Conflictとの適合

[PROVISIONAL]

本ProjectではConflictを隠さないことを重要原則としている。

例：

- Design vs Code
- Test vs Current Behavior
- Meeting Decision vs Implementation

SemanticaのConflict関連機能が、

- Conflict Detection
- Conflict Representation
- Resolution Tracking

に利用できるか確認する。

---

# 11. Deduplicationとの適合

[PROVISIONAL]

Repositoryでは、

- 同じRequirementの複数Version
- 同じFunctionの複数呼称
- Duplicate Document
- Similar Inquiry

が存在する可能性がある。

SemanticaのDeduplication機能を利用できる可能性がある。

ただし自動MergeでHuman Knowledgeを失わないようにする。

---

# 12. Decision Intelligenceとの適合

[PROVISIONAL]

本Projectでは責任・仕様判断のため、

- Technical Cause
- Current Specification
- Historical Agreement
- Difference
- Evidence

を整理する。

SemanticaのDecision関連機能が、

> Decision Support

として利用できる可能性がある。

ただし最終責任・契約判断はHuman Decisionとする。

---

# 13. Context Retrievalとの適合

[PROVISIONAL]

本Projectでは、

> LLM MemoryよりRetrieval

を重視する。

SemanticaのContext機能が、

- Case-Centered Context
- Evidence Retrieval
- Graph Context
- Provenance付きContext

に利用できるか評価する。

---

# 14. AgentContextの評価

[PROVISIONAL]

Semanticaには`AgentContext`のようなAgent向けContext Interfaceが存在する。

ただし、確認した実装では、

> Agentそのもの

ではなく、

> Context / RetrievalのFacade

として理解する方が適切である。

本ProjectではAgent ArchitectureとSemantica Context Layerを分離する。

---

# 15. AgentContextをAgentとして扱わない

[DECIDED]

以下の構造を避ける。

Semantica AgentContext  
= Main Maintenance Agent

代わりに、

Maintenance Agent / Skill  
→ Context Adapter  
→ Semantica AgentContext

のように利用する。

---

# 16. AgentContext Constructorの実装確認

[OPEN]

以前の実装確認では、`AgentContext`利用に`vector_store`等の明示的Dependencyが必要な形が確認された。

一方でPlugin / Example側の記述と実APIが一致しない可能性があった。

そのためPoCでは、

- Current Constructor
- Required Dependencies
- Initialization Example
- Query API

を実コードで確認する。

Documentation Exampleだけで実装しない。

---

# 17. Repository Ingestとの適合

[PROVISIONAL]

SemanticaにはRepository / Code Ingestに利用可能な機能が存在するため、

- Repository Discovery
- Source Parse
- Code Extraction

の一部を代替できる可能性がある。

ただしExisting Repositoryの意味分類はProject側で行う。

---

# 18. RepoIngestorの評価

[OPEN]

PoCで確認する事項：

- Ignore Rule
- Binary File
- Large Repository
- Git Metadata
- Incremental Processing
- File Rename
- Document Type Classification
- Existing Inquiry Folder

Repository全体へいきなり適用せずGolden Sampleで確認する。

---

# 19. CodeParserの評価

[PROVISIONAL]

SemanticaのCode Parserが、

- Module
- Class
- Function
- Call
- Dependency

等を取得できる場合、Code Graph生成に利用可能性がある。

ただし本Projectではさらに、

- Function Knowledge
- Data Flow
- Test
- Business

とのBridgeが必要。

---

# 20. Code Graphの不足部分

[DECIDED]

一般的なCode Parserだけでは、

> このFunctionはどの業務機能を実現するか

は自動的に分からないことが多い。

そのため、

Code Graph  
＋  
Maintenance Domain Graph

を接続するProject固有Adapterが必要。

---

# 21. Data Flow対応

[OPEN]

SemanticaのCode / Graph機能だけで、

- SQL Table Access
- File Input / Output
- Batch Flow
- API Data Flow

をどこまで抽出できるか確認する。

Data Flowが弱い場合、Project側で追加Parser / Extractorを実装する。

---

# 22. Document Parsingとの適合

[PROVISIONAL]

Semanticaが以下のDocument Formatを扱える場合、本ProjectのIngest Layerで活用できる可能性がある。

- PDF
- DOCX
- PPTX
- Excel

ただしFormat Supportがあることと、

> Maintenance Knowledgeとして十分な構造を保持できる

ことは別である。

---

# 23. Excel評価

[OPEN]

Test Specificationで確認する。

評価項目：

- Sheet
- Row
- Cell
- Merge
- Formula
- Table
- Provenance
- Chunking

TestCase Knowledgeへ変換できる品質かを確認する。

---

# 24. PowerPoint評価

[OPEN]

Design Diagramで確認する。

評価項目：

- Slide
- Shape
- Connector
- Text
- Notes
- Provenance

Text Extractionだけで十分かをGolden Sampleで判断する。

---

# 25. PDF評価

[OPEN]

評価項目：

- Page Mapping
- Table
- Diagram
- Text Quality
- OCR Requirement
- Provenance

---

# 26. Normalized Intermediate Representationとの関係

[DECIDED]

Semantica Parser OutputをそのままDomain Knowledgeへ固定しない。

本ProjectではProject-ownedなNormalized Intermediate Representationを持つことを検討する。

これにより、

- Semantica
- Other Parser
- Custom Parser

を交換可能にする。

---

# 27. Canonical Modelの所有権

[DECIDED]

以下は本Projectが所有する。

- Entity Types
- Relation Types
- Knowledge State
- Case Model
- Provenance Contract
- Security Classification
- Persistent Investigation Model

Semanticaはこれらを実現するBackend候補。

---

# 28. Ontologyとの関係

[PROVISIONAL]

SemanticaのOntology関連機能を利用する場合も、Maintenance OntologyはProject側で定義する。

候補Entity：

- BusinessProcess
- Function
- System
- Table
- TestCase
- Requirement
- Decision
- Case
- Stakeholder

---

# 29. Ontologyを細かくしすぎない

[DECIDED]

PoC初期からEnterprise級Ontologyを作らない。

Golden Caseで必要なEntity / Relationだけから開始する。

---

# 30. Semantica Skills / Plugin

[PROVISIONAL]

確認したSemantica Pluginには、Knowledge処理関連の複数Skillが用意されていた。

候補領域：

- extract
- ingest
- query
- ontology
- validate
- deduplicate
- embed
- reason
- decision
- causal
- temporal
- provenance
- policy
- explain
- export
- change
- visualize

本ProjectのSkill ArchitectureとConcept上重なるものが多い。

---

# 31. Plugin SkillをそのままProject Skillにしない

[DECIDED]

Semantica Plugin SkillはInfrastructure Capabilityとして利用する。

本Project側のSkill例：

`trace-evidence`

が内部で、

- query
- provenance
- temporal

等のSemantica機能を利用する構造を検討する。

---

# 32. Plugin Agent

[PROVISIONAL]

確認したPluginにはDecision / Explainability / KG関連Agentが含まれていた。

ただしMaintenance固有Agentではない。

Project側Agentが必要に応じてSemantica Agent / Capabilityを呼び出す方式を検討する。

---

# 33. Plugin ExampleとLibrary APIの差異

[DECIDED]

Plugin ExampleやDocumentationはCurrent Library APIと一致しない可能性がある。

以前の確認でも、

- Constructor
- Method
- Casing
- Example Flow

等で実装との差異が疑われる箇所があった。

そのため、

> ExampleをCopyして採用決定

しない。

---

# 34. Documentation Drift

[DECIDED]

Semantica評価では、

1. Current Source Code
2. Current Package Metadata
3. Test
4. Example
5. Documentation

の順に実装事実を確認することを基本とする。

Documentationだけで判断しない。

---

# 35. Version Pinning

[PROVISIONAL]

PoCでSemanticaを利用する場合、Versionを固定する。

理由：

- API変更
- Exampleとの不一致
- Reproducibility

PoC結果には利用Versionを記録する。

---

# 36. MCPとの適合

[PROVISIONAL]

SemanticaのMCP機能は、CodexからKnowledge InfrastructureをToolとして利用する手段になり得る。

候補：

Codex  
→ MCP  
→ Semantica  
→ Knowledge / Graph / Provenance

これは本Projectと相性がよい可能性がある。

---

# 37. MCP採用の利点

[PROVISIONAL]

- Agent Frameworkから分離できる
- CodexからToolとして利用しやすい可能性
- Storage実装を隠蔽できる
- Query Interfaceを統一できる

---

# 38. MCP採用の確認事項

[OPEN]

- Current MCP Serverの機能
- Authentication
- Local起動
- Security
- Query Interface
- Provenance返却
- Large Result Handling
- Codex側Integration

---

# 39. MCPをCanonical APIにするか

[OPEN]

PoCでMCPが安定して使える場合、

> Agent → Knowledge Infrastructure

の主要Interfaceにできる可能性がある。

ただしProject内部Service APIも維持する選択肢を残す。

---

# 40. Framework Agnostic性

[PROVISIONAL]

SemanticaがFramework Agnosticであることは本Projectに有利。

本Projectでは、

- Codex
- Future Agent Framework
- Local App

から同じKnowledge Infrastructureを利用したい。

---

# 41. Agno等とのIntegration

[FUTURE]

Semantica側にAgent Framework Integrationが存在しても、PoC初期では利用を急がない。

まずCodex Workflowが成立するかを確認する。

---

# 42. Semantica Visualize

[PROVISIONAL]

Graph Visualization機能が利用可能でも、

> Semanticaの全Graph ViewerをそのままUser UIにする

ことを前提にしない。

本ProjectではCase-Centered Subgraphが必要。

---

# 43. Semantica Export

[PROVISIONAL]

Export機能は、

- Debug
- Migration
- Tool Replacement
- Review

に有用な可能性がある。

Project-ownedな中立FormatへExportできるか確認する。

---

# 44. Change / Temporal機能

[PROVISIONAL]

SemanticaのChange / Temporal Capabilityが、

- Document Version
- Current / Historical
- Release
- Git Change

へ利用できるか評価する。

---

# 45. Git Diffとの統合

[OPEN]

本ProjectではIncremental UpdateにGit Diffを利用したい。

Semanticaが、

- Changed FileのみRe-ingest
- Deleted File
- Renamed File
- Changed Relation

を扱えるか確認する。

---

# 46. Rebuildability

[DECIDED]

Semanticaを利用しても、Semantica Runtimeを削除して再構築できるArchitectureにする。

Source of Truthは、

- Original
- Git
- Persistent Knowledge
- Config
- Human Curated Relation

側に置く。

---

# 47. Semantica Storageを正本にしない

[DECIDED]

Semantica内部Graph / Vector / StoreだけにHuman Reviewed Knowledgeを保存しない。

Semanticaを外しても重要Knowledgeが残ることを目標とする。

---

# 48. Human Curated Relation

[DECIDED]

Humanが確認した、

- Business → Function
- Decision → Requirement
- Responsibility Scope

等はProject-owned Persistent Knowledgeへ保存する。

Semanticaへ同期する場合も正本はProject側に置く。

---

# 49. Securityとの関係

[DECIDED]

SemanticaへSourceを渡せるかはSemanticaの機能だけで決めない。

`11_SECURITY_AND_GOVERNANCE.md`のPolicyに従う。

---

# 50. Meeting Minutes

[OPEN]

Meeting MinutesをSemanticaへIngestするかは、Codex利用可否・Repository保存可否・Git保存可否と同じDecision Gateの対象とする。

SemanticaがParse可能でも、Security上許可されるとは限らない。

---

# 51. Sensitive Derived Graph

[DECIDED]

Sensitive Documentから生成されたGraphもSensitiveである可能性がある。

Semantica Graphへ、

- Person
- Responsibility
- Customer Decision

等を保存する場合Access Controlを検討する。

---

# 52. Provenance Security

[PROVISIONAL]

ProvenanceにOriginal Locationを保存することで、Restricted Sourceの存在・名前が露出する可能性がある。

Security ClassificationをProvenanceにも適用する。

---

# 53. Local-Firstとの適合

[PROVISIONAL]

SemanticaがLocal Environmentで軽量に動作可能であれば、PoCのLocal-First方針と相性がよい。

確認事項：

- Setup
- Dependencies
- Memory
- Startup Time
- Persistent Store
- Developer Debug

---

# 54. Dependency Cost

[OPEN]

PoCでは、

> Semanticaを入れることで減る実装量

と、

> Semantica自体を理解・保守するコスト

を比較する。

機能が多いこと自体を採用理由にしない。

---

# 55. Abstraction Cost

[DECIDED]

Semanticaを交換可能にするためAdapterを作ると一定の実装Costが発生する。

しかし本Projectは長期運用保守Repositoryを想定しているため、特定FrameworkへのLock-in回避を優先する。

---

# 56. PoC評価方針

[DECIDED]

Semanticaを全面導入してから評価しない。

Golden Case / Golden Documentで、機能ごとに小さく検証する。

---

# 57. PoC Evaluation Track A: Document Parsing

[PROVISIONAL]

Golden Documentを一つ選び、

- Parse Quality
- Structure Preservation
- Provenance
- Custom Transformation

を確認する。

---

# 58. PoC Evaluation Track B: Code Graph

[PROVISIONAL]

Golden Caseに関連するCode範囲で、

- Module
- Function
- CALLS
- Data Access

を抽出できるか確認する。

---

# 59. PoC Evaluation Track C: Knowledge Graph

[PROVISIONAL]

最低限、

- Case
- Function
- Code
- Table
- Test
- Evidence

をRelationとして保持・Queryできるか確認する。

---

# 60. PoC Evaluation Track D: Provenance

[PROVISIONAL]

Graph / KnowledgeからOriginal Sourceへ戻れるか確認する。

例：

TestCase  
→ Excel  
→ Sheet  
→ Row

---

# 61. PoC Evaluation Track E: Temporal

[PROVISIONAL]

Current / Historical Documentを最低一組用意し、

- Version
- Effective Date
- Supersedes

を扱えるか確認する。

---

# 62. PoC Evaluation Track F: Conflict

[PROVISIONAL]

意図的に、

- Design
- Code

が異なるGolden Sampleを使い、Conflictを保持できるか確認する。

---

# 63. PoC Evaluation Track G: Codex / MCP

[PROVISIONAL]

Codexから、

- Query Knowledge
- Traverse Relation
- Get Provenance

を呼び出せるか確認する。

---

# 64. PoC Evaluation Track H: Rebuild

[PROVISIONAL]

Semantica Runtimeを削除後、

- Repository
- Config
- Persistent Knowledge

から再構築できるか確認する。

---

# 65. Semanticaを採用する条件

[PROVISIONAL]

以下の複数で明確な価値がある場合、採用を前向きに検討する。

- Parser実装量削減
- Provenance管理
- Graph構築
- Temporal
- Conflict
- MCP
- Context Retrieval
- Rebuild

---

# 66. Semanticaを採用しない条件

[PROVISIONAL]

以下の場合、PoCで採用範囲を縮小または不採用とする。

- APIが不安定
- Documentationとの差異が大きい
- Golden Document Parsing品質が不足
- Project SchemaへのMappingが難しい
- Dependencyが重すぎる
- Debugが困難
- Security要件を満たしにくい
- Simple SQLite / Custom Parserの方が明確に小さい

---

# 67. Partial Adoption

[DECIDED]

SemanticaはAll-or-Nothingで評価しない。

例えば、

- Parsingだけ採用
- Graph / Provenanceだけ採用
- MCPだけ採用
- Temporalだけ採用

も許容する。

---

# 68. Replaceability

[DECIDED]

Semanticaを採用しても、将来交換できるようにする。

交換候補：

- Custom Parser
- SQLite
- NetworkX
- Neo4j
- Other Knowledge Framework

Project Domain Modelを維持できることを優先する。

---

# 69. Adapter Boundary

[PROVISIONAL]

候補Adapter：

- Parser Adapter
- Knowledge Graph Adapter
- Provenance Adapter
- Search Adapter
- Context Adapter

一つの巨大Semantica Adapterにする必要はない。

---

# 70. Testing Strategy

[DECIDED]

Semantica IntegrationにはProject側のContract Testを持つことを検討する。

例：

- Parse Golden Excel
- Expected TestCase Count
- Expected Provenance
- Expected Relation
- Rebuild Result

Library Upgrade時のRegressionを確認する。

---

# 71. Golden Sample Contract

[DECIDED]

Semantica導入判断は、

> APIが動いたか

ではなく、

> ProjectのGolden Sample Contractを満たしたか

で判断する。

---

# 72. Version Upgrade

[PROVISIONAL]

Semantica Versionを上げる際、

1. Contract Test
2. Parser Diff
3. Graph Diff
4. Provenance Diff

を確認する。

Production運用で自動Upgradeしない。

---

# 73. Observability

[PROVISIONAL]

Semanticaを利用する場合、Developerが以下を確認できることが望ましい。

- Semantica Version
- Active Capability
- Processing Result
- Error
- Generated Node / Edge Count
- Provenance
- Runtime State

---

# 74. Failure Isolation

[DECIDED]

Semanticaの一機能が失敗しても、

> Repository調査全体が停止する

構造を避ける。

例：

Graph生成失敗  
→ Direct Repository SearchへFallback

---

# 75. Fallback

[PROVISIONAL]

候補：

- Semantica Parser失敗 → Custom Parser / Original Read
- Graph失敗 → Full Text / Code Search
- MCP失敗 → Direct Local API
- Vector失敗 → Full Text Search

---

# 76. Semantica Evaluationの成功条件

PoCで以下が確認できれば有望と判断する。

1. Golden Documentを意味を壊さずParseできる
2. OriginalへProvenanceで戻れる
3. Required Node / Relationを保持できる
4. CodexからQueryできる
5. Runtimeを再構築できる
6. Project Domain Modelを独立維持できる
7. Debug可能
8. Custom実装より明確な価値がある

---

# 77. Semantica Evaluationの失敗条件

以下が複数発生する場合は採用範囲を縮小する。

- Source Mappingが不十分
- Excel / PPT構造が失われる
- API差異が頻発
- Graph SchemaをProject側で制御できない
- Errorが追跡しづらい
- Runtime StateがSource of Truth化する
- Security Policyを適用しづらい
- Codex Integrationが複雑すぎる

---

# 78. SemanticaとCustom Implementationの比較軸

[DECIDED]

比較時は以下で評価する。

- Implementation Time
- Maintenance Cost
- Debuggability
- Traceability
- Provenance
- Graph Query
- Temporal
- Conflict
- Security
- Replaceability
- Documentation Quality
- API Stability

---

# 79. 「機能数」で評価しない

[DECIDED]

Semanticaに多くの機能が存在しても、本Projectで使わなければ価値にはならない。

Golden CaseのInvestigation Time / Evidence Traceability改善を基準に評価する。

---

# 80. PoC Recommended Adoption Scope

[PROVISIONAL]

現時点の第一候補は、

## First Priority

- Parse / Normalize補助
- Provenance
- Graph / Relation
- Context Query

## Second Priority

- Temporal
- Conflict
- Deduplication
- MCP

## Later

- Advanced Reasoning
- Decision Intelligence
- Visualization
- Causal Analysis

とする。

---

# 81. Advanced Reasoningを後回しにする理由

[DECIDED]

本Projectの初期課題は、

> AIが高度に推論できないこと

より、

> 必要なEvidenceへ到達しづらく、Current / Historical / Code / Test / Meetingがつながっていないこと

である。

まずKnowledge Infrastructureを整える。

---

# 82. Decision Intelligenceを後回しにする理由

[DECIDED]

責任・契約判断はHuman Approvalが必要である。

そのため高度なDecision Engineより先に、

- Evidence
- Provenance
- Historical Agreement
- Missing Knowledge

を正しく取得できることを優先する。

---

# 83. Visualizationを後回しにする理由

[DECIDED]

Graph Visualizationは補助機能。

Case Subgraphが調査に役立つか確認してからUIを拡張する。

---

# 84. PoC Implementation Order

[PROVISIONAL]

Semanticaを試す場合、

1. Version固定
2. Minimal Install
3. Golden Document Parse
4. Provenance確認
5. Project IntermediateへMapping
6. Minimal Graph生成
7. Query
8. Codex Integration
9. Rebuild Test
10. Adoption Review

とする。

---

# 85. Adoption Review

[DECIDED]

PoC終了時に、

- Adopt
- Partially Adopt
- Defer
- Reject

のいずれかをDecisionとして残す。

理由とEvidenceを記録する。

---

# 86. 採用DecisionをADR候補にする

[PROVISIONAL]

Semantica採用範囲がArchitectureへ大きく影響するため、採用DecisionはADR等で残すことを検討する。

---

# 87. Current Open Questions

[OPEN]

## Current Semantica Version

PoC実施時に確認。

## AgentContext API

Current Constructor / Required Dependency。

## RepoIngestor

Incremental / Ignore / Rename対応。

## CodeParser

Data Access / Language Coverage。

## Excel Parser

Test Specification適合性。

## PowerPoint Parser

Diagram適合性。

## Provenance

Cell / Slide / Page粒度。

## MCP

Codexからの利用方法。

## Storage

Semantica内部Storeの構成。

## Security

Restricted Knowledge対応。

## Partial Adoption

どのCapabilityだけ採用するか。

---

# 88. PoCで記録するSemantica評価結果

[DECIDED]

最低限以下を記録する。

- Version
- Capability Tested
- Golden Sample
- Setup Time
- Parse Quality
- Provenance Quality
- Graph Quality
- Query Quality
- Error / Limitation
- Custom Code Required
- Decision

---

# 89. Evaluation Scorecard候補

[PROVISIONAL]

評価項目を5段階等で記録することを検討する。

- Fit
- Ease of Integration
- Traceability
- Debuggability
- Performance
- Security
- Replaceability
- Documentation Accuracy

数値だけで採用判断しない。

---

# 90. Semantica Risk 1: Framework Lock-in

[DECIDED]

対策：

- Project-owned Schema
- Adapter
- Persistent Knowledge outside Semantica

---

# 91. Semantica Risk 2: Documentation Drift

[DECIDED]

対策：

- Current Source確認
- Version Pin
- Contract Test

---

# 92. Semantica Risk 3: Over-Engineering

[DECIDED]

対策：

- Golden Case First
- Minimal Capability
- Advanced Feature後回し

---

# 93. Semantica Risk 4: Hidden Runtime State

[DECIDED]

対策：

- Rebuild Test
- Export
- Project-owned Persistent Knowledge

---

# 94. Semantica Risk 5: Security

[DECIDED]

対策：

- Project Security Policy優先
- Restricted Sourceを無条件Ingestしない
- Derived GraphもClassification対象

---

# 95. Semantica Risk 6: Domain Mismatch

[DECIDED]

対策：

- Maintenance OntologyをProject側で定義
- SemanticaはInfrastructure Layer

---

# 96. Handoff時の注意

[DECIDED]

別環境でPoCを開始するDeveloper / Codexは、

> Semantica採用済み

と解釈しない。

本Document時点ではEvaluation Candidateである。

---

# 97. Handoff時に最初に確認すること

1. Current Semantica Repository / Version
2. Current Installation手順
3. Current API
4. Golden Sample
5. Existing Repository
6. Security Decision
7. Minimal Evaluation Scope

---

# 98. 採用前に作らないもの

[DECIDED]

Semantica評価前に以下をSemantica依存で大量実装しない。

- Full Domain Ontology
- Full Graph Migration
- Full Agent Framework
- Full UI
- Full Document Conversion
- Production Runtime

---

# 99. 後続ドキュメントへの引き継ぎ

## `15_POC_PLAN_AND_ACCEPTANCE_CRITERIA.md`

- Semantica Evaluation Track
- Golden Sample
- Adoption Gate
- Success / Failure Criteria

## `16_OPEN_QUESTIONS_AND_DECISION_LOG.md`

- Semantica Version
- Adoption Scope
- MCP
- AgentContext
- Parser Quality
- Graph Storage
- Final Adoption Decision

---

# 100. Semantica Evaluation Decision Summary

## [DECIDED]

- SemanticaをProject全体の正本Architectureとしない
- SemanticaはKnowledge Infrastructure候補として評価する
- Maintenance Domain ModelはProject側で所有する
- Case / Responsibility / Human ReviewはProject側で設計する
- Semantica内部StorageをSource of Truthにしない
- Project-owned Intermediate / Canonical Modelを維持する
- Plugin / Exampleを実APIの代わりに信用しない
- Current SourceとContract TestでAPIを確認する
- Golden Sampleで小さく評価する
- Partial Adoptionを許容する
- Security PolicyをSemanticaより優先する
- Advanced ReasoningよりEvidence / Provenance / Graphを優先する
- Versionを固定して評価する
- Rebuild可能性を確認する

## [PROVISIONAL]

- Parse / Provenance / Graph / ContextをFirst Priorityとする
- Temporal / Conflict / MCPをSecond Priorityとする
- Adapter Layerを設ける
- Semantica MCPをCodex Tool Interface候補とする

## [OPEN]

- Current Version
- AgentContext API
- RepoIngestor品質
- CodeParser品質
- Excel / PPT Parser品質
- Data Flow対応
- MCP適合性
- Security対応
- 最終Adoption Scope

---

# 101. Semantica Evaluation Statement

> 本ProjectではSemanticaを、運用保守Applicationそのものではなく、Ingest、Parse、Knowledge Graph、Provenance、Temporal、Conflict、Context、MCP等を提供するKnowledge Infrastructure候補として評価する。Maintenance固有のCase Model、Ontology、Investigation Workflow、Responsibility Assessment、Coverage、Human Review、Persistent Investigation KnowledgeはProject側で所有し、Semantica内部Data ModelやRuntime StorageをSource of Truthにはしない。採用判断はDocumentationや機能一覧ではなく、Golden Document / Golden Caseに対してParse品質、Provenance、Relation、Codex Query、Rebuildability、Debuggabilityを実コードで検証した結果に基づいて行う。必要であれば一部Capabilityのみを採用し、Project Domain ModelとPersistent Knowledgeを維持したまま将来交換可能なArchitectureとする。

## 101.1 2026-08-30 Evaluation Scope Refinement

[DECIDED]

SemanticaがWork Item / Objective Context、Operation / Runbook、Stakeholder / Responsibility、UserAction / Execution / Artifactをそのまま表現できることは必須条件にせず、AdapterでCanonical Relation Modelへ写像できるかを評価する。固定8 ViewやCase専用Schemaへの依存は避ける。PoCでは承認済みSourceのみを入力し、Masking、Token Vault、Detokenization、原本復元をSemantica採用条件にしない。Artifact Provenance、Rebuildability、目的切替時のContext保持を評価項目へ加える。

## 101.2 Infrastructure / IaC Evaluation（2026-08-30）

[DECIDED]

Semantica評価へ、Function / System / Infrastructureを別Node Typeとして扱えるか、Terraform HCL / Module / Resource / Plan / State MetadataをAdapter経由でCanonical Relation Modelへ写像できるか、Secret値を除外しつつSource ProvenanceとDrift Stateを保持できるかを追加する。Flat ProjectionとVertical StackはProject側のPresentation契約とし、Semantica固有のVisualizationや階層Schemaを採用条件にしない。
