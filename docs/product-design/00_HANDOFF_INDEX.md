# AI-Ready Operations Repository / Codex App
## Handoff Index

**Document:** `00_HANDOFF_INDEX.md`  
**Status:** Active Handoff Document  
**Purpose:** 本PoCの背景、要件、設計思想、検討状況を別PC・別アカウント・別Codexセッションへ正確に引き継ぐための入口。

---

# 1. このドキュメントについて

本Repositoryでは、AIを活用した運用保守支援ツールのPoCを行う。

本PoCは単なるチャットボット、RAG、全文検索ツール、Knowledge Graph Viewerを作ることが目的ではない。

目標は、

> 運用保守に必要な業務・仕様・システム・コード・データフロー・テスト・過去判断・変更履歴・ステークホルダー・責任範囲を接続し、問い合わせや障害などのCaseを起点として、Codexが必要な根拠を探索できるRepositoryを作ること。

である。

---

# 2. なぜドキュメントを分割しているか

本プロジェクトでは、背景・業務要件・Knowledge Model・Graph・Agent・Document変換・Securityなど、複数の論点が存在する。

これらを単一の巨大なHANDOFF.mdへまとめると、

- 情報が埋もれる
- 更新時にどこを変更すべきか分からなくなる
- Codexが重要事項と参考情報を区別しにくくなる
- 決定事項と未決定事項が混在する
- Context量増加により重要な設計思想が抜ける

可能性がある。

そのため、本Repositoryではテーマ別にHandoff Documentを分割する。

---

# 3. Codexへの重要指示

本Repositoryを初めて扱うCodex / Agentは、実装を始める前に本ディレクトリの設計ドキュメントを確認すること。

特に以下を守る。

1. 決定済み事項と未決定事項を区別する。
2. 未決定事項を勝手に決定済みとして扱わない。
3. PoC段階の仮説をProduction要件として扱わない。
4. 既存Repository構造をAI都合で大規模変更しない。
5. Original DocumentとAI-Ready Knowledgeを混同しない。
6. Gitを履歴上のSource of Truthとして扱う。
7. Derived Dataは可能な限り再生成可能にする。
8. AIの推論とHuman Verified Factを区別する。
9. Evidence不足時は推測で埋めず、Missing Knowledgeとして扱う。
10. Responsibility / Contract / Cost判断をAIのみで確定しない。

---

# 4. 読む順番

初めて本PoCへ参加するCodex / Developerは、原則以下の順番で読む。

## Phase 1: なぜ作るのか

### `01_BACKGROUND_AND_PROBLEM.md`

現在の運用保守で何が問題になっているのか。

主に以下を記載する。

- 運用保守担当者の現状
- 問い合わせ調査で困っていること
- システム理解不足
- 開発履歴不足
- 仕様判断の難しさ
- 責任範囲判断の難しさ
- 顧客説明の難しさ

---

### `02_VISION_AND_GOALS.md`

このPoCで最終的にどのような状態を実現したいか。

主に以下を記載する。

- Vision
- Goals
- Non-Goals
- 想定User
- 代表Use Case
- 成功状態

---

# 5. 要件

### `03_REQUIREMENTS.md`

機能要件・非機能要件を整理する。

例：

- Repository解析
- Document取込
- AI-Ready変換
- Knowledge生成
- Case生成
- 問い合わせ調査
- Evidence追跡
- Code調査
- Graph探索
- Timeline
- Responsibility Assessment
- Stakeholder別Output
- Human Review
- Git連携

PoC要件と将来要件を明確に分離する。

---

# 6. 設計原則

### `04_DESIGN_PRINCIPLES.md`

技術選定より上位にある設計思想を書く。

現時点で重要な原則：

- Git is the historical source of truth.
- AI-Ready Knowledge is derived data.
- OriginalとAI-Ready Dataを分離する。
- KnowledgeにはProvenanceを持たせる。
- Caseを調査単位とする。
- TimeはKnowledge Layerではなく横断Dimensionとする。
- Graphは可視化ではなくRelation Modelとして扱う。
- RetrievalをLLM Memoryより重視する。
- AI inferenceとHuman verified factを区別する。
- Missing Knowledgeを隠さない。
- AgentはDirectoryではなく責務で分離する。
- Project固有ルールはConfig化する。
- 特定Graph DBやFrameworkへDomain Modelを依存させない。

---

# 7. Repository Architecture

### `05_REPOSITORY_ARCHITECTURE.md`

Repositoryの物理構造を定義する。

現在検討している主要領域：

```text
source/
docs/
knowledge/
cases/
graph/
agents/
skills/
config/
pipeline/
app/
generated/
runtime/
```

既存Repositoryへ導入する場合は、大規模な移動をせず、

```text
ops-ai/
```

等を追加するOverlay方式も検討する。

---

# 8. Knowledge Model

### `06_KNOWLEDGE_MODEL.md`

AIが扱うKnowledgeの意味構造を定義する。

現時点の基本Layer：

1. Business / Operation
2. Function / UI
3. System / Data Flow
4. Implementation
5. Evidence / Decision History
6. Stakeholder / Responsibility

TimeはLayerではなく横断Dimensionとして扱う。

Knowledgeには状態を持たせることを検討する。

例：

```text
verified
human_reviewed
ai_extracted
inferred
needs_review
conflicting
deprecated
```

---

# 9. Graph / Code Graph

### `07_GRAPH_AND_CODEGRAPH.md`

Knowledge同士をどう接続するかを定義する。

Graphは1つのCanonical Relation Modelから、最低限以下のViewへProjectionして考える。

## Graph View

例：

```text
Case
Domain / Business
Function
System / Architecture
Data Flow
Code
Test
Evidence / History
```

通常の入口はCase Viewとし、`Current only + Related to current Case + Depth 2`を既定値とする。

各Viewは物理的に別Graphへ分断せず、Bridge Relationで以下を縦に辿れるようにする。

```text
Business
→ Function
→ System / Data
→ Implementation
→ Test
→ Evidence / History
```

Graph DB採用は必須条件ではない。

PoC初期ではJSON / NetworkX / SQLite等による実装も許容する。

重要なのはGraph Storage製品ではなく、

> 何をNodeとし、何と何をRelationで結ぶか

である。

---

# 10. Document Ingest / AI-Ready Conversion

### `08_DOCUMENT_INGEST_AND_TRANSFORM.md`

今後の詳細設計で特に重要な領域。

基本Pipeline：

```text
Original
↓
Classification
↓
Parser
↓
Normalized Intermediate Model
↓
Security / Masking
↓
Domain Transformation
↓
Validation
↓
AI-Ready Knowledge
↓
Graph / Index
```

Excel / PowerPoint / Word / PDF等を直接Markdownへ変換するだけの設計にはしない。

Normalized Intermediate Modelの導入を検討する。

AI-Ready Knowledge候補：

```text
content.md
metadata.yaml
relations.json
```

詳細Schemaは未決定。

---

# 11. Case Investigation

### `09_CASE_INVESTIGATION_WORKFLOW.md`

本アプリの中心となるUse Caseを定義する。

Case候補：

```text
Inquiry
Incident
Bug
Change Request
Release
Investigation
Operation Task
```

問い合わせの基本調査Flow：

```text
Inquiry
↓
Case
↓
Symptom
↓
Reproduction
↓
Business Impact
↓
Function
↓
System / Data Flow
↓
Implementation
↓
Evidence
↓
Timeline
↓
Responsibility Assessment
↓
Stakeholder Output
↓
Human Review
↓
Answer
↓
CaseをKnowledge化
```

---

# 12. Agent / Skill Architecture

### `10_AGENT_AND_SKILL_ARCHITECTURE.md`

AgentはDirectory単位ではなく責務単位にする。

候補：

```text
Main Orchestrator
Business Analyst
System Analyst
Code Investigation
Evidence
Timeline
Responsibility
Stakeholder Communication
Review
```

AgentとSkillを分離する。

Agent：

> 誰が担当するか

Skill：

> 何の仕事を実行できるか

例：

```text
investigate-case
trace-evidence
analyze-impact
build-timeline
validate-repository
build-report
```

---

# 13. Security / Governance

### `11_SECURITY_AND_GOVERNANCE.md`

以下を定義する。

- Classification
- Masking
- Redaction
- PII
- Credential
- Customer Data
- Production Data
- Original Document Access Policy
- Codex Access Policy
- Human Approval
- Repository Policy
- Exception Management

Markdown化しただけではSecurity対策にならない。

AIへ渡す前のIngestion PipelineでPolicyを適用する。

---

# 14. Runtime / Storage

### `12_RUNTIME_AND_STORAGE.md`

GitとRuntime DBの責務を整理する。

基本思想：

```text
Git
=
Historical Source of Truth
```

```text
Runtime DB / Graph / Index
=
Derived Search Infrastructure
```

重要情報をGraph DBにのみ保存しない。

Runtime DatabaseはGit + Config + Parserから再構築できることを目標とする。

PoC候補：

```text
SQLite
JSON
NetworkX
```

将来候補：

```text
Neo4j
FalkorDB
Apache AGE
Semantica Graph Store
```

---

# 15. UI / Developer Experience

### `13_UI_AND_DEVELOPER_EXPERIENCE.md`

対象Userは主にDeveloper / 運用保守担当者。

想定：

```text
VS Code
+
Codex
+
Local App
```

主要UI候補：

- Current Case
- Graph
- Timeline
- Evidence
- Agent Coverage
- Missing Knowledge
- Responsibility Assessment
- Stakeholder Output
- Repository Navigator

Graph全体を常時表示するのではなく、Case中心のSubgraphを表示する。

---

# 16. Semantica

### `14_SEMANTICA_EVALUATION.md`

Semanticaは採用決定ではなく技術選定候補として扱う。

評価対象：

- Ingest
- Parse
- Normalize
- Semantic Extraction
- Knowledge Graph
- Temporal Graph
- Conflict Detection
- Deduplication
- Provenance
- Decision Intelligence
- MCP
- Code / Repository Integration
- Visualization

Semanticaへ業務Domain Modelを合わせない。

本PoCのDomain Modelを先に設計し、

> Semanticaでどの部分を実装できるか

を評価する。

---

# 17. PoC計画

### `15_POC_PLAN_AND_ACCEPTANCE_CRITERIA.md`

PoCは巨大な完成系を作るのではなく、一つの実案件相当の問い合わせをEnd-to-Endで処理できることを重視する。

Golden Path候補：

```text
Original Document
+
Source Code
↓
Ingest
↓
AI-Ready Knowledge
↓
Code / Data Flow Graph
↓
Case
↓
Knowledge Retrieval
↓
Investigation
↓
Evidence
↓
Answer Draft
```

最初のGolden Sampleとして、実在に近いExcel設計書等を1つ選定する。

---

# 18. Open Questions

### `99_OPEN_QUESTIONS.md`

決まっていない事項は必ずここへ残す。

例：

- AI-Ready Canonical Format
- Intermediate Model Schema
- Stable ID
- Chunking
- Excel特殊情報
- PowerPoint図形
- Source Mapping
- Semantic Diff
- Graph DB採用タイミング
- Semantica採用範囲
- Codex MCP連携方式
- Vector Search必要性
- Human Review Workflow

未決定事項を設計ドキュメントの本文へ曖昧に混在させない。

---

# 19. Decision Statusの書き方

各設計ドキュメントでは、重要事項に以下の状態を可能な限り付与する。

```text
[DECIDED]
[PROVISIONAL]
[UNDER_REVIEW]
[OPEN]
[OUT_OF_SCOPE]
```

例：

```text
[DECIDED]
GitをHistorical Source of Truthとする。

[PROVISIONAL]
PoC Runtime DBとしてSQLiteを第一候補とする。

[OPEN]
Production段階でNeo4jを採用するか。
```

Codexは`[PROVISIONAL]`や`[OPEN]`を確定事項として扱ってはならない。

---

# 20. 設計変更時のルール

設計思想を変更する場合は、

1. なぜ変更するか
2. 以前の設計
3. 新しい設計
4. 影響範囲
5. Decision Status

を記録する。

可能であればGit Commitと関連付ける。

---

# 21. PoC開始時にCodexが最初に行うこと

新しいPC / Account / Sessionで開始する場合、Codexは以下を確認する。

```text
1. 00_HANDOFF_INDEX.mdを読む

2. 01〜15の存在を確認する

3. Repositoryの実際のDirectory構成を確認する

4. Handoff Documentと現在実装との差分を確認する

5. [DECIDED] / [PROVISIONAL] / [OPEN]を整理する

6. 実装済み機能を確認する

7. 未実装機能を確認する

8. PoCの次の最小実装単位を提示する
```

設計ドキュメントを読まずに大規模なコード生成を開始しない。

---

# 22. 現時点の大まかな状態

```text
Problem Definition            Drafted
Vision                        Drafted
Design Principles             Drafted
Knowledge Layers              Drafted
Case Concept                  Drafted
Repository Concept            Drafted
Agent Concept                 Drafted
Graph Concept                 Drafted
Code Graph Concept            Drafted
Semantica Evaluation          Started

Detailed Requirements         Not Yet Finalized
Knowledge Schema              Not Defined
Graph Schema                  Not Defined
Intermediate Model            Not Defined
AI-Ready Conversion Contract  Not Defined
Security Rules                Not Defined
Runtime Storage               Not Selected
Agent Implementation          Not Started
Codex App                     Not Started
PoC Implementation            Not Started
```

---

# 23. 次に作成するドキュメント

最優先は、

```text
01_BACKGROUND_AND_PROBLEM.md
```

である。

ここでは技術の話を極力入れず、

> なぜこのツールが必要になったのか

を、実際の運用保守業務と現在抱えている問題から正確に記録する。

背景を正しく固定してから、

```text
02_VISION_AND_GOALS.md
03_REQUIREMENTS.md
04_DESIGN_PRINCIPLES.md
```

へ進む。

---

# 24. このPoCの一文定義

> 運用保守に散在する業務・仕様・システム・コード・データフロー・テスト・変更履歴・意思決定・人・責任をGit上のKnowledgeとして接続し、問い合わせ等のCaseを起点にCodexが根拠を追跡しながら調査でき、その調査範囲・証拠・不足情報まで人間が検証できるAI-Ready Repository / Codex Appを構築する。

---

# 25. 2026-08-30 Design Refinement Handoff

[DECIDED]

- Productの中心単位をCaseからWork Itemへ一般化し、問い合わせ、障害、システム理解、運用、変更、影響調査、見積り、Knowledge整備を扱う。CaseはInquiry / IncidentのSubtypeとする。
- 最初に目的を聞くPurpose-First UIとし、途中のObjective追加・変更でもEvidenceや調査Contextを保持する。
- Graphは1つのCanonical Relation Modelから必要なViewをProjectionし、Operation / RunbookとStakeholder / Responsibilityを追加する。View数は固定しない。
- FileはOriginal、Intermediate、Persistent Knowledge、Runtime Index、System-generated Artifactを区別し、登録・Archive・Rebuild・Permanent Deleteを別操作にする。
- PoCはAI利用承認済みDataだけを対象とし、利用者向け分類、Masking、Token Vault、Detokenization、原本復元UIはProduction検討へ保留する。

## 25.1 Graph構造の追加引き継ぎ（2026-08-30）

[DECIDED]

- Functionは「業務・利用者へ何を提供するか」、Systemは「Functionをどの技術構成で実現・稼働するか」として分離し、`IMPLEMENTED_BY`等で接続する。
- Terraform等をSourceとするInfrastructure / IaC GraphをCanonical Relation Modelの正式Projectionへ追加する。
- 詳細なNode / Relation探索には平面Graph、`Inquiry / Work Item → Objective → Domain / Function → System / Infrastructure → Code / Data Flow / Test → Evidence`の全体理解には縦断Stackを使用する。
- Vertical StackはStorage階層ではなくPresentation Modelであり、平面Graphとの切替時もStable ID、Work Item、Objective、選択Node、Evidenceを保持する。
