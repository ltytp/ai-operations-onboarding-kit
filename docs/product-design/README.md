# Product Design Documents

このFolderには、AI-Ready Operations Repository / Codex Appの背景、要件、設計、Security、PoC計画、未決事項をまとめた17種類の設計Documentがあります。

これらは設計上の基準と判断履歴です。Documentに書かれた構成や機能が、現在のRuntimeへすべて実装済みであることを意味しません。`[DECIDED]`、`[PROVISIONAL]`、`[OPEN]`および各DocumentのStatusを区別して利用してください。

## 現在のProduct方向

最初の成果物は、問い合わせWorkflowの追加ではなく、Repository全体のKnowledgeを整理・可視化するローカルKnowledge Explorerです。

主な対象Layerは次のとおりです。

- Domain / Business
- Function
- System / Architecture
- Data Flow
- Code
- Test
- Document / Evidence
- History / Decision

一つのCanonical Knowledge Modelを基に、各LayerをGraph ViewとしてProjectionし、Layer間のRelationを辿れることを目指します。問い合わせ対応は、このKnowledge Mapを利用するConsumerの一つとして後段で扱います。

## 読む順番

### 1. 上流の事実・目的・要求

1. [`00_HANDOFF_INDEX.md`](00_HANDOFF_INDEX.md)
2. [`01_BACKGROUND_AND_PROBLEM.md`](01_BACKGROUND_AND_PROBLEM.md)
3. [`02_VISION_AND_GOALS.md`](02_VISION_AND_GOALS.md)
4. [`03_REQUIREMENTS.md`](03_REQUIREMENTS.md)

背景と要件が実態に合っているかを最優先で確認します。

### 2. Knowledge整理・可視化の中心設計

5. [`04_DESIGN_PRINCIPLES.md`](04_DESIGN_PRINCIPLES.md)
6. [`05_REPOSITORY_ARCHITECTURE.md`](05_REPOSITORY_ARCHITECTURE.md)
7. [`06_KNOWLEDGE_MODEL.md`](06_KNOWLEDGE_MODEL.md)
8. [`07_GRAPH_AND_CODEGRAPH.md`](07_GRAPH_AND_CODEGRAPH.md)
9. [`08_DOCUMENT_INGEST_AND_TRANSFORM.md`](08_DOCUMENT_INGEST_AND_TRANSFORM.md)
10. [`12_RUNTIME_AND_STORAGE.md`](12_RUNTIME_AND_STORAGE.md)
11. [`13_UI_AND_DEVELOPER_EXPERIENCE.md`](13_UI_AND_DEVELOPER_EXPERIENCE.md)
12. [`15_POC_PLAN_AND_ACCEPTANCE_CRITERIA.md`](15_POC_PLAN_AND_ACCEPTANCE_CRITERIA.md)

現在の可視化中心の方向では、このGroupが主な設計基準です。

### 3. 後段の利用WorkflowとGovernance

13. [`09_CASE_INVESTIGATION_WORKFLOW.md`](09_CASE_INVESTIGATION_WORKFLOW.md)
14. [`10_AGENT_AND_SKILL_ARCHITECTURE.md`](10_AGENT_AND_SKILL_ARCHITECTURE.md)
15. [`11_SECURITY_AND_GOVERNANCE.md`](11_SECURITY_AND_GOVERNANCE.md)

問い合わせWorkflowやAgent/Skillは、Knowledge Map構築後のConsumer・運用設計として扱います。SecurityとHuman reviewは段階にかかわらず適用します。

### 4. 評価対象と未決事項

16. [`14_SEMANTICA_EVALUATION.md`](14_SEMANTICA_EVALUATION.md)
17. [`99_OPEN_QUESTIONS.md`](99_OPEN_QUESTIONS.md)

Semanticaは採用決定ではなく評価対象です。`99_OPEN_QUESTIONS.md`の未決事項を推測で確定しないでください。

## 実Repositoryでの利用

設計DocumentをGuardrailとして利用し、対象Repositoryを最初にRead Onlyで調査します。理想構造が既に存在すると仮定せず、実際のSource Code、Document、Test、Data関連資産、System設定から抽出可能なNode、Relation、Evidence、欠落Knowledgeを報告してから実装方針を決定します。

最初からGraph DB、Vector DB、Semantica、Multi-Agentを必須にしません。最小PoCでは、JSON等のCanonical dataとローカルHTMLによるLayered Graph Visualizationから開始できます。
