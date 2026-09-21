# AI-Ready Operations Repository / Codex App
## 10. Agent and Skill Architecture

**File Name:** `10_AGENT_AND_SKILL_ARCHITECTURE.md`  
**Status:** Draft  
**Document Role:** Agent Responsibility / Skill Model / Orchestration / Execution Trace  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、Codexを中心とした問い合わせ調査において、

- Agentをどの責務で分けるか
- Skillをどの単位で定義するか
- Main Agent / Orchestratorが何を担当するか
- Knowledge RetrievalとAgent Memoryをどう分離するか
- Agent実行結果をどのように追跡するか
- Human Reviewをどこに置くか

を定義する。

本Projectでは、Multi-Agent構成そのものを目的としない。

重要なのは、

> 問い合わせ調査を、再現可能・Evidence付き・Human Review可能な作業単位へ分解できること

である。

---

# 2. Agent Architectureの基本思想

[DECIDED]

Agent Architectureは、

> AIを何体作るか

から設計しない。

まず、

> 運用保守の問い合わせ調査で、どの責務と能力が必要か

を定義する。

その後、

- 一つのAgentが複数責務を担当する
- 複数Agentへ分割する
- Skillとして実装する
- Toolとして実装する

のどれが適切かを決める。

---

# 3. PoCでMulti-Agentを必須にしない

[DECIDED]

PoCの目的は、一件の問い合わせをEnd-to-Endで調査できることを確認することである。

そのためPoC初期では、

- Main Agent
- 明示的なSkill
- Repository / Search / Graph / Validation Tool

だけでもよい。

Multi-Agent化は、責務分離による効果が確認できた後に導入する。

---

# 4. AgentとSkillを分離する

[DECIDED]

本Projectでは以下のように考える。

## Agent

「誰がその判断・作業責務を担当するか」

## Skill

「何ができるか」

例えば、

**Evidence Agent**

が、

- Find Evidence
- Trace Decision
- Build Timeline

というSkillを利用できる。

Agent構成を変更してもSkillを再利用できるようにする。

---

# 5. AgentをDirectory単位で分けない

[DECIDED]

以下のような分け方を基本としない。

- src Agent
- docs Agent
- test Agent
- inquiry Folder Agent

理由は、Repository Directory構成が変化し得るためである。

Agentは、

- Business Analysis
- Code Investigation
- Evidence Investigation
- Review

等の責務で分ける。

---

# 6. Main Agent / Orchestratorの役割

[DECIDED]

Main AgentはRepository全体を毎回読み込む役割ではない。

主な責務は以下。

1. Inquiryを理解する
2. Current Caseを管理する
3. 調査領域を決める
4. 必要なSkill / Agentを選択する
5. 調査結果を統合する
6. Sources Checked / Not Checkedを整理する
7. Missing Knowledgeを管理する
8. Conflictを検出する
9. Human Reviewへ渡す
10. Persistent Investigation Knowledge作成を支援する

---

# 7. Main Agentが避けること

[DECIDED]

Main Agentは以下を前提にしない。

- Repository全Fileを一度に読む
- 全KnowledgeをContextへ入れる
- Session Memoryだけで過去調査を覚える
- すべての専門調査を自分で実行する
- EvidenceなしでAssessmentを統合する

Main AgentはOrchestrationとIntegrationを中心にする。

---

# 8. Retrieval First

[DECIDED]

Agent ArchitectureはLLM MemoryよりRetrievalを優先する。

Agentは必要に応じて、

- Repository Search
- Code Search
- Graph Traversal
- Case Search
- Full Text Search
- External Evidence Reference

を利用する。

「前のSessionで覚えているはず」という設計にしない。

---

# 9. Codex Resume / Sessionの位置付け

[DECIDED]

Codex Resume / Sessionは、過去のWorking Historyを復元する重要なInvestigation Sourceである。

引き継ぎ時には利用可能であれば参照する。

ただしAgent Memoryの代替として扱わない。

重要な調査成果はPersistent Investigation Knowledgeへ保存する。

---

# 10. Session ContextとPersistent Knowledgeを分離する

[DECIDED]

以下を明確に分ける。

## Session Context

現在のCodex Sessionで一時的に利用している情報。

## Persistent Investigation Knowledge

Human Review後にSession外へ保存された再利用対象。

## General Repository Knowledge

Function、Data Flow、Test、Decision等の継続利用Knowledge。

AgentはSession終了後も必要な情報をPersistent側から再取得できることを前提とする。

---

# 11. Candidate Agent Responsibilities

[PROVISIONAL]

将来的な責務候補として以下を想定する。

- Main Orchestrator
- Business Analyst
- System Analyst
- Code Investigation Agent
- Data Investigation Agent
- Evidence Agent
- Timeline Agent
- Responsibility Assessment Agent
- Stakeholder Communication Agent
- Review Agent

すべてを別Agentとして実装する必要はない。

---

# 12. Main Orchestrator

[PROVISIONAL]

責務候補：

- Inquiry Intake
- Case State管理
- Investigation Planning
- Skill / Agent選択
- Result Integration
- Coverage管理
- Missing Knowledge管理
- Human Review依頼
- Final Investigation Summary統合

Main Orchestrator自身が最終責任判断を確定しない。

---

# 13. Business Analyst

[PROVISIONAL]

責務候補：

- 問い合わせの業務文脈整理
- Actual / Expected Behavior整理
- Business Process特定
- Business Rule確認
- End User Impact整理
- Function候補特定

Code詳細の調査は主責務としない。

---

# 14. System Analyst

[PROVISIONAL]

責務候補：

- Screen / API / Batch / System構成確認
- Function間Relation確認
- System Boundary確認
- Data Flow候補整理
- External System影響確認

BusinessとCodeのBridgeを支援する。

---

# 15. Code Investigation Agent

[PROVISIONAL]

責務候補：

- Source Code検索
- Entry Point特定
- Call Path確認
- Conditional Logic確認
- SQL確認
- Configuration確認
- Technical Cause候補抽出
- Related Code提示

Codeの挙動だけで仕様を確定しない。

---

# 16. Data Investigation Agent

[PROVISIONAL]

責務候補：

- Data Flow確認
- Table / File Relation確認
- Batch Input / Output確認
- SQL / Query確認
- Data Missing Point特定
- Business Date / Processing Date確認

Production Dataへアクセスする場合はSecurity Policyに従う。

---

# 17. Evidence Agent

[PROVISIONAL]

責務候補：

- Current Design検索
- Test Specification検索
- Past Inquiry検索
- Historical Evidence検索
- Meeting / Decision Reference確認
- Evidence Chain作成
- Provenance確認

「Evidenceが存在しない」と「未確認」を区別する。

---

# 18. Timeline Agent

[PROVISIONAL]

責務候補：

- Runtime Timeline作成
- Historical Decision Timeline作成
- Release / Commit / Decision Date整理
- Time Conflict確認

Timeを一つの単純Timelineへ潰さない。

---

# 19. Responsibility Assessment Agent

[PROVISIONAL]

責務候補：

- Technical Cause整理
- Current Specification整理
- Historical Agreement整理
- Difference / Deviation整理
- Responsibility Assessment Material作成
- Missing Evidence明示

最終責任判断は行わない。

---

# 20. Stakeholder Communication Agent

[PROVISIONAL]

責務候補：

- End User向け説明
- Customer System / Management向け説明
- Developer向けTechnical Summary
- Internal Report

同じKnowledgeをStakeholderごとにPresentation変換する。

---

# 21. Review Agent

[PROVISIONAL]

責務候補：

- Evidence不足確認
- Sources Not Checked確認
- Conflict確認
- AI推論とFactの混在確認
- Current / Historical混同確認
- 責任断定の強さ確認
- Stakeholder Tone確認
- Security Risk確認

Review Agentの結果もHuman Approvalの代替にはしない。

---

# 22. Agent数は実装詳細

[DECIDED]

上記責務を何Agentへ分けるかはArchitectureの本質ではない。

例えばPoCでは、

- Main Agent
- Code Skill
- Evidence Skill
- Review Skill

だけでもよい。

将来的に負荷・Context・専門性を理由にAgent分割する。

---

# 23. Skillの基本原則

[DECIDED]

Skillは、

> 再利用可能な一つの作業能力

として定義する。

SkillはAgentのPersonalityではなく、Input / Output / Evidence / Failureを明確にする。

---

# 24. Candidate Skills

[PROVISIONAL]

候補：

- intake-inquiry
- understand-symptom
- plan-investigation
- search-repository
- search-past-cases
- inspect-code
- trace-code-path
- trace-data-flow
- find-test-evidence
- find-current-spec
- trace-historical-decision
- build-timeline
- classify-technical-cause
- assess-responsibility-material
- calculate-coverage
- validate-evidence
- detect-conflict
- generate-stakeholder-response
- persist-investigation
- promote-knowledge
- validate-repository

---

# 25. Skill Naming

[PROVISIONAL]

Skill名はDirectory名ではなくAction / Capabilityを表す。

避けたい例：

- docs-skill
- src-skill
- excel-agent

望ましい例：

- trace-evidence
- inspect-code
- find-related-test
- persist-investigation

---

# 26. Skill Contract

[DECIDED]

各Skillには最低限以下を定義することを検討する。

- Purpose
- Inputs
- Preconditions
- Tools / Sources
- Outputs
- Evidence
- Sources Checked
- Failure Conditions
- Review Requirement

これによりAgentから独立して再利用できる。

---

# 27. Skill Input

[PROVISIONAL]

Skill Inputには必要最小限のContextを渡す。

候補：

- Case ID
- Inquiry Summary
- Target Function
- Known Evidence
- Search Scope
- Time Range
- Security Context

Repository全体を毎回Inputにしない。

---

# 28. Skill Output

[DECIDED]

Skill Outputは単なる自然言語回答だけにしない。

可能な範囲で以下を返す。

- Result
- Evidence
- Sources Checked
- Sources Not Checked
- Confidence / Knowledge State
- Open Questions
- Suggested Next Step

---

# 29. Structured Skill Output

[PROVISIONAL]

論理的には以下のような構造を検討する。

```yaml
skill: inspect-code
status: completed
result: ...
sources_checked:
  - ...
evidence:
  - ...
open_questions:
  - ...
next_steps:
  - ...
```

これは物理Formatの確定ではない。

---

# 30. Skill Failure

[DECIDED]

Skillが結果を得られなかった場合も、明示的なOutputとする。

例：

- source_not_found
- access_restricted
- insufficient_context
- unsupported_format
- conflict_detected
- tool_error

失敗を空回答にしない。

---

# 31. ToolとSkillを分離する

[DECIDED]

Toolは技術的な操作能力。

SkillはToolを利用して一つの業務目的を達成する手順。

例えば、

Tool：
- Git Search
- Graph Query
- File Read

Skill：
- Find Current Specification

という関係。

---

# 32. Tool Candidate

[PROVISIONAL]

候補：

- Repository File Search
- Code Search
- Git Diff
- Git History
- Full Text Search
- Graph Query
- SQLite Query
- Document Parser
- Knowledge Index Search
- Case Search
- Validation Tool

---

# 33. External Source Tool

[OPEN]

NotebookLM等のExternal EvidenceをCodexから直接Toolとして参照できるかは現時点で未確定。

利用不可の場合、

- Humanが確認
- SummaryをCaseへ入力
- External Source Referenceを記録

するWorkflowを維持する。

---

# 34. Agent Execution Record

[DECIDED]

Agent / Skill実行では、結果だけでなく実行記録を残せることが望ましい。

候補：

- Execution ID
- Case ID
- Agent Role
- Skill
- Task
- Started At
- Completed At
- Sources Checked
- Sources Not Checked
- Evidence
- Result
- Open Questions
- Status
- Review State

---

# 35. Agent Execution Recordの目的

[DECIDED]

目的：

- 長いSessionで調査状況を把握する
- 引き継ぎ可能にする
- Coverageを計算する
- 誤回答原因を確認する
- 同じ調査の重複を減らす
- Reviewしやすくする

Agentの内部思考過程を保存することが目的ではない。

---

# 36. Chain of ThoughtをKnowledgeとして保存しない

[DECIDED]

AIの内部推論そのものをPersistent Knowledgeの対象としない。

保存するのは、

- Investigation Action
- Evidence
- Result
- Key Hypothesis
- Rejected Hypothesisの要点
- Open Question
- Human Review結果

等の業務上再利用可能な情報とする。

---

# 37. Sources CheckedをAgent単位でも残す

[DECIDED]

複数Agent / Skillが同じCaseで動く場合、

> 誰が何を確認したか

を統合できるようにする。

Main Orchestratorは実行Recordを基にCase全体のSources Checkedを構成する。

---

# 38. Sources Not Checked

[DECIDED]

Agentが確認できなかったSourceも記録する。

理由：

- Access Restricted
- Not Found
- Not Required
- Time Constraint
- Tool Failure
- Unsupported

未確認なのに「Evidenceなし」と結論しない。

---

# 39. Coverage Aggregation

[PROVISIONAL]

Main Orchestratorは各Skill結果を集約してCase Coverageを更新する。

例：

- Business: checked
- Function: checked
- System: partial
- Implementation: checked
- Test: checked
- Historical Evidence: not_checked
- Responsibility: partial

---

# 40. CoverageはAgent数では決まらない

[DECIDED]

Agentを多く実行したからCoverageが高いとはみなさない。

重要Sourceが未確認ならCoverageはPartialのままとする。

---

# 41. Missing Knowledge Routing

[PROVISIONAL]

AgentがMissing Knowledgeを検出した場合、Main Orchestratorが次のActionを決定する。

例：

- Repository Searchを追加
- External Evidence確認をHumanへ依頼
- CaseをBlockedにする
- Human Reviewへ進める

---

# 42. Conflict Routing

[PROVISIONAL]

Agent間で結果が矛盾した場合、Main Orchestratorが一方を自動採用しない。

Conflictとして、

- Result A
- Result B
- Evidence A
- Evidence B

を整理し、必要に応じてReview Agent / Humanへ渡す。

---

# 43. Agent間の直接会話を前提にしない

[PROVISIONAL]

複数Agentを導入する場合でも、Agent同士が無制限に会話し続ける構成は避ける。

基本は、

Main Orchestrator  
→ Task  
→ Specialist Result  
→ Main Orchestrator

とする。

これによりExecution Traceを追いやすくする。

---

# 44. Shared Context

[PROVISIONAL]

Agent間共有Contextには、必要最小限のCase情報を使用する。

候補：

- Case Summary
- Known Facts
- Known Evidence
- Missing Knowledge
- Relevant Node IDs
- Current Workflow State

全Session Conversationを毎回渡さない。

---

# 45. Context Package

[PROVISIONAL]

Main OrchestratorがSpecialistへ渡すContext Packageを定義する可能性がある。

候補：

- Case ID
- Task
- Scope
- Existing Findings
- Required Output
- Security Constraints
- Source Limits

---

# 46. Context Budget

[DECIDED]

Agent / SkillごとにContext Budgetを意識する。

大量Documentをそのまま渡すより、

- Retrieval
- Chunk
- Subgraph
- Source Snippet

を選択して渡す。

---

# 47. Case-Centered Subgraphの利用

[PROVISIONAL]

Graphが利用可能な場合、AgentにはRepository全GraphではなくCase-Centered Subgraphを提供する。

例：

- Target Function
- Related Code
- Related Table
- Related Test
- Related Past Inquiry

---

# 48. Code Investigation Skill

[PROVISIONAL]

代表的Skill Contract候補：

## Purpose

Technical Cause候補をSource Codeから調査する。

## Inputs

- Case
- Target Function
- Symptom
- Known Data

## Outputs

- Related Code
- Execution Path
- Condition
- Technical Cause Candidate
- Evidence
- Open Questions

---

# 49. Trace Data Flow Skill

[PROVISIONAL]

Purpose：

事象に関連するDataの流れを確認する。

Outputs候補：

- Upstream Source
- Processing Step
- Table
- API
- Report
- Missing Data Point
- Evidence

---

# 50. Find Current Specification Skill

[PROVISIONAL]

Purpose：

Current Specificationを示すEvidenceを集める。

Source候補：

- Current Design
- Current Test
- Operation Manual
- Release
- Code

CodeだけでCurrent Specificationを確定しない。

---

# 51. Trace Historical Decision Skill

[PROVISIONAL]

Purpose：

過去のRequirement / Meeting / Decisionから仕様成立経緯を確認する。

External Evidenceへ直接アクセス不可の場合は、

`human_external_check_required`

を返せること。

---

# 52. Search Past Cases Skill

[PROVISIONAL]

Purpose：

類似した過去Caseを探す。

検索候補：

- Function
- Technical Cause
- Error
- Table
- Batch
- Similar Text
- Historical Decision

Past Case結果を現在Caseへ自動適用しない。

---

# 53. Build Timeline Skill

[PROVISIONAL]

Purpose：

Caseに必要な時間関係を整理する。

Timeline候補：

- Runtime Timeline
- Decision Timeline
- Release Timeline

---

# 54. Assess Responsibility Material Skill

[PROVISIONAL]

Purpose：

責任判断材料を整理する。

Inputs：

- Technical Cause
- Current Specification
- Historical Agreement
- Evidence
- Missing Evidence

Output：

- Assessment Material
- Alternative Interpretations
- Missing Evidence
- Human Review Required

最終責任結論は出さない。

---

# 55. Validate Evidence Skill

[PROVISIONAL]

Purpose：

AssessmentのEvidence不足を検出する。

確認候補：

- Source Mapping
- Current / Historical
- Knowledge State
- Conflict
- Access Restricted Source
- Missing Historical Evidence

---

# 56. Generate Stakeholder Response Skill

[PROVISIONAL]

Purpose：

Human ReviewedなKnowledgeから説明Draftを生成する。

InputにHuman Approved Positionを含める。

AIが責任表現を勝手に強めない。

---

# 57. Persist Investigation Skill

[DECIDED]

Purpose：

Case終了時にHuman Reviewedな調査成果をSession外へ保存する。

保存候補：

- Investigation Summary
- Evidence
- Sources Checked
- Missing Knowledge
- Human Decision
- Final Response

保存形式・保存先は`12_RUNTIME_AND_STORAGE.md`で具体化する。

---

# 58. Promote Knowledge Skill

[PROVISIONAL]

Purpose：

Case固有の調査結果から、他Caseでも使えるGeneral Knowledgeを抽出する。

必ずEvidenceとHuman Reviewを確認する。

---

# 59. Validate Repository Skill

[PROVISIONAL]

Purpose：

Repository PolicyやAI-Ready状態を確認する。

候補：

- Missing Metadata
- Stale Derived Knowledge
- Broken Provenance
- Missing Relations
- Security Issue

PoC初期では必須ではない。

---

# 60. Human-in-the-Loop

[DECIDED]

Agent ArchitectureにHumanを明示的なActorとして含める。

Humanの責務：

- External Evidence確認
- Security判断
- Current Specificationの重要判断
- Responsibility / Contract判断
- Cost判断
- Customerへの正式Response承認
- AI Knowledge Correction

---

# 61. Human Review Point

[DECIDED]

少なくとも以下でHuman Reviewを行う。

1. Responsibility Assessment
2. Customer Response
3. Persistent Investigation Knowledgeの重要結論
4. General Knowledgeへの昇格
5. Sensitive External Evidenceの利用

---

# 62. Human Override

[DECIDED]

HumanはMain OrchestratorのInvestigation Planを変更できる。

例：

- このFileを先に確認
- Historical Meetingを確認
- この仮説は除外
- Customer Scopeの表現を修正

AgentはHuman Correctionを優先する。

---

# 63. Human Correctionの保存

[PROVISIONAL]

Human Correctionについて、

- Before
- After
- Reason
- Reviewer

を必要に応じて記録する。

Agent / Skill改善のFeedbackとして利用できる。

---

# 64. Review AgentとHuman Reviewを分ける

[DECIDED]

Review Agentは、

> Human Review前のQuality Check

として利用する。

Review AgentがApprovedでも、人間の承認が必要な事項はそのままHuman Reviewへ進める。

---

# 65. Security Guardrail

[DECIDED]

Agent / SkillごとにSecurity Policyを無視してSourceへアクセスさせない。

特に、

- Meeting Minutes
- Customer Information
- Contract
- Production Data
- Credential

はAccess Policyに従う。

---

# 66. Agent Access Scope

[PROVISIONAL]

Agent RoleごとにAccess Scopeを設定する可能性がある。

例えばStakeholder Communication Agentには、Raw CredentialやProduction Dataを渡さない。

Least Privilegeを基本とする。

---

# 67. Restricted Source

[DECIDED]

Agentが必要Sourceへアクセスできない場合、

- Access Restricted
- Human Check Required

をResultとして返す。

Access不可をSource不存在と誤認しない。

---

# 68. Agent Configuration

[DECIDED]

Project固有条件はAgent PromptへHard Codingしすぎない。

Config候補：

- Agent Policy
- Skill Registry
- Document Types
- Stakeholders
- Security Policy
- Graph Schema
- Review Rules

---

# 69. Skill Registry

[PROVISIONAL]

利用可能SkillをRegistryとして管理することを検討する。

候補情報：

- Skill ID
- Description
- Inputs
- Outputs
- Allowed Tools
- Required Policy
- Review Requirement
- Version

---

# 70. Agent Definition

[PROVISIONAL]

Agent定義候補：

- Agent ID
- Role
- Responsibilities
- Allowed Skills
- Access Scope
- Escalation Rules
- Output Contract

特定Agent Framework専用形式には固定しない。

---

# 71. AGENTS.mdとの関係

[PROVISIONAL]

Repository Root等の`AGENTS.md`には、

- Handoff Documentの場所
- Agent Architectureの概要
- Security上の禁止事項
- Human Review必須事項
- Persistent Investigation保存ルール

を記載することを検討する。

詳細Agent定義をすべてAGENTS.mdへ詰め込まない。

---

# 72. Codex Native Capabilityとの関係

[DECIDED]

本Architectureは、特定時点のCodex内部機能に強く依存しない。

Codex側で、

- Agent
- Subagent
- Skill
- Tool
- Resume

等の機能名称・実装が変わっても、

> Responsibility / Capability / Execution Record / Persistent Knowledge

というLogical Modelを維持する。

---

# 73. Agent Framework Independence

[DECIDED]

以下のFrameworkを採用する場合でも、Domain WorkflowをFrameworkへ従属させない。

候補：

- Codex native mechanisms
- Semantica integration
- Agno
- Other Agent Framework

Adapter Layerを検討する。

---

# 74. Semanticaとの関係

[PROVISIONAL]

Semanticaを利用する場合、

- Query
- Reason
- Provenance
- Decision
- Temporal
- Knowledge Graph

等をSkill / ToolのInfrastructureとして利用できる可能性がある。

Semantica付属Agentをそのまま運用保守Agent Architectureの正本にしない。

---

# 75. Agent Version

[PROVISIONAL]

Agent / Skill定義にVersionを持たせることを検討する。

Case Recordから、

> どのVersionのSkillで調査したか

を確認できるとAuditに有用である。

---

# 76. Prompt Version

[PROVISIONAL]

重要なPrompt / InstructionをRepository管理する場合、Git Historyで変更を追跡できるようにする。

ただしPromptをKnowledge Source of Truthとはしない。

---

# 77. Deterministic RuleとAgentを分ける

[DECIDED]

機械的に判定できる処理をすべてAgentへ任せない。

例：

- Schema Validation
- File Hash
- Git Diff
- ID Validation
- Security Pattern Check

はDeterministic Tool / Ruleを優先する。

---

# 78. AIを使う価値がある領域

[DECIDED]

AIを優先して利用する領域：

- Inquiry Understanding
- Semantic Retrieval
- Cross-document Interpretation
- Hypothesis Generation
- Evidence Synthesis
- Stakeholder Explanation
- Conflict Explanation

---

# 79. Agent Cost / Latency

[PROVISIONAL]

Multi-Agent化では、

- Context duplication
- Execution Time
- Cost
- Result Conflict

が増える可能性がある。

Agent分割は「専門Agentが格好良い」ことではなく、調査品質・Context管理に効果がある場合だけ行う。

---

# 80. Parallel Execution

[FUTURE]

独立性が高い調査は並列実行を検討できる。

例：

- Code Investigation
- Past Case Search
- Test Evidence Search

一方、Historical AssessmentはTechnical Cause確認後の方が効率的な場合もある。

Workflow依存関係を考慮する。

---

# 81. Execution Dependency

[PROVISIONAL]

Skill間に依存関係を定義することを検討する。

例：

`assess-responsibility-material`

は、

- Technical Cause
- Current Specification

が一定程度整理された後に実行する。

---

# 82. Retry Policy

[PROVISIONAL]

Tool FailureやInsufficient Context時にRetry可能とする。

ただし同じ検索を無限に繰り返さない。

Retry理由と結果をExecution Recordへ残す。

---

# 83. Escalation

[DECIDED]

以下ではHumanへEscalateする。

- Security判断が必要
- External Evidenceが必要
- Conflictが解消できない
- Responsibility判断
- Customer Communication承認
- ToolからEvidence取得不能

---

# 84. Investigation Stop Condition

[PROVISIONAL]

Main Agentは以下を満たした場合にHuman Reviewへ進める。

- Technical CauseまたはUnknown理由が整理済み
- Current Specification確認状況が明確
- Evidenceが存在
- Sources Checked / Not Checkedが明確
- Missing Knowledgeが明確
- Responsibility Assessment Materialが整理済み

---

# 85. Agentは調査完了を過大評価しない

[DECIDED]

「回答文を作れた」ことを調査完了とみなさない。

Coverage / Evidence / Missing Knowledgeを確認した後にHuman Reviewへ進む。

---

# 86. Persistent Execution Summary

[PROVISIONAL]

すべてのAgent実行Logを永続保存する必要はない。

Case終了時に必要なExecution SummaryだけPersistent Investigation Knowledgeへ残すことを検討する。

候補：

- Major Investigation Steps
- Sources Checked
- Significant Findings
- Rejected Major Hypotheses
- Remaining Questions

---

# 87. Runtime Execution Log

[PROVISIONAL]

詳細なAgent Execution LogはRuntime Storageへ保持する可能性がある。

永続期間・Git管理可否は`12_RUNTIME_AND_STORAGE.md`で決める。

---

# 88. Agent ResultのProvenance

[DECIDED]

Agent Resultには可能な範囲でEvidence Sourceを持たせる。

自然言語Summaryだけを次Agentへ渡さず、Source Referenceも引き継ぐ。

---

# 89. Result Compression

[PROVISIONAL]

長い調査結果を次Agentへ渡す際、

- Structured Finding
- Evidence Reference
- Open Question

へ圧縮する。

元SourceへのLinkを失わない。

---

# 90. Evidence Chain Preservation

[DECIDED]

Main Agentが複数Specialist Resultを統合した後も、

> この結論はどのEvidenceから来たか

を辿れること。

Agent間の要約を重ねてProvenanceを失わない。

---

# 91. PoC推奨Agent Architecture

[PROVISIONAL]

PoC初期は以下を第一候補とする。

## Main Codex Session

役割：

- Inquiry Intake
- Investigation Planning
- Result Integration
- Human Interaction

## Skills

- inspect-code
- trace-data-flow
- find-current-spec
- search-past-cases
- trace-evidence
- validate-investigation
- persist-investigation

必要であればReview責務のみ分離する。

---

# 92. PoCでAgent分割を追加する条件

[PROVISIONAL]

以下が発生した場合にSpecialist Agent分割を検討する。

- Main Contextが大きすぎる
- Code Investigationが長大
- Evidence調査とCode調査を並行したい
- Specialist Promptが明確に品質向上する
- Execution Traceを分けた方がReviewしやすい

---

# 93. PoCで実装しなくてよいもの

PoC初期では以下を必須としない。

- 10体以上のAgent
- 自律Agent同士の自由会話
- Agent Swarm
- Full Autonomous Workflow
- Automatic Responsibility Decision
- Agent自身によるCustomer送信
- Long-term AI Memory専用基盤

---

# 94. Golden Caseで確認するAgent Value

[DECIDED]

Golden Caseで以下を確認する。

1. Main Agentが問い合わせを正しく分解できるか
2. 必要なSkillを選べるか
3. Code / Evidence調査が混線しないか
4. Sources Checkedを統合できるか
5. Missing Knowledgeを保持できるか
6. Specialist ResultからEvidenceへ戻れるか
7. Human Reviewへ適切にEscalateできるか
8. Persistent Investigation Knowledgeを保存できるか

---

# 95. Agent Architectureの成功条件

成功とは、

> Agent数が増えた状態

ではない。

以下が成立すること。

- 調査責務が明確
- Skillが再利用可能
- Main AgentのContext肥大化を抑えられる
- Evidenceが失われない
- Sources Checkedが見える
- Missing Knowledgeが見える
- Human Reviewが明確
- Sessionを跨いでもPersistent Knowledgeから再開できる
- Framework変更に耐えられる

---

# 96. Agent Architecture Anti-Patterns

## One Agent Reads Everything

全RepositoryをMain Agentへ毎回読ませる。

## Agent = Directory

Folder単位でAgentを作る。

## Multi-Agent First

PoC成立前にAgent数を増やす。

## No Skill Contract

Agentごとに同じ処理を別実装する。

## Summary Without Evidence

Specialist ResultからSourceが消える。

## Session Memory Dependency

過去SessionをAIが覚えている前提にする。

## Agent Decision = Human Decision

責任・契約・費用をAIだけで確定する。

## Infinite Agent Discussion

Agent同士が無制限に議論し続ける。

---

# 97. Current Open Questions

[OPEN]

## PoC Agent Count

単一Agent + Skillsか、一部Specialist分割か。

## Codex Native Agent Mechanism

対象環境で利用可能な具体機能。

## Skill Definition Format

Markdown / YAML / Code等。

## Execution Record Format

Persistent / Runtimeの境界。

## Context Package Schema

具体形式。

## Agent Access Control

Roleごとの権限制御。

## Review Agent

PoCで実装するか。

## External Evidence Tool

NotebookLM等へ直接接続可能か。

## Semantica Integration

Skill / Toolとしてどこまで利用するか。

---

# 98. 後続ドキュメントへの引き継ぎ

## `11_SECURITY_AND_GOVERNANCE.md`

- Agent Access Scope
- Restricted Sources
- Human Approval
- Sensitive Knowledge
- External Evidence

## `12_RUNTIME_AND_STORAGE.md`

- Session Context
- Execution Log
- Persistent Investigation Knowledge
- Agent / Skill Version
- Rebuild

## `13_UI_AND_DEVELOPER_EXPERIENCE.md`

- Current Agent / Task
- Sources Checked
- Coverage
- Missing Knowledge
- Human Review Queue

## `14_SEMANTICA_EVALUATION.md`

- Semantica Tool / Skill Integration
- AgentContext
- MCP
- Framework Boundary

## `15_POC_PLAN_AND_ACCEPTANCE_CRITERIA.md`

- PoC Agent構成
- Golden Case
- Agent / Skill評価

---

# 99. Agent and Skill Decision Summary

## [DECIDED]

- Agentは責務で分ける
- Skillは再利用可能な能力として分ける
- Directory単位でAgentを作らない
- Main AgentはOrchestration中心
- RetrievalをSession Memoryより優先する
- PoCでMulti-Agentを必須にしない
- Skill OutputにEvidenceを含める
- Sources Checked / Not Checkedを残す
- Agent Execution Recordを持てる構造にする
- 内部思考過程をPersistent Knowledgeとして保存しない
- Human ReviewをArchitectureに含める
- Review AgentはHuman Reviewの代替ではない
- Codex Resumeを重要なWorking Sourceとして扱う
- 重要な調査成果はSession外へ永続化する
- 特定Agent FrameworkへDomain Workflowを従属させない

## [PROVISIONAL]

- Candidate Agent Roles
- Skill Registry
- Context Package
- Structured Skill Output
- Review Agent
- Agent Version
- Execution Log Storage
- Semantica Adapter

## [OPEN]

- PoC Agent数
- Codex Native機能の利用範囲
- Skill定義Format
- Agent Access Control
- External Evidence Tool
- Execution Recordの永続化範囲

---

# 100. Agent and Skill Architecture Statement

> 本ProjectのAgent Architectureは、Main Agent一体にRepository全体の理解・調査・判断・記憶を集中させず、運用保守の責務と再利用可能なSkillを分離して設計する。Main Agent / OrchestratorはInquiry理解、Investigation Planning、Skill選択、Evidence統合、Coverage・Missing Knowledge管理、Human ReviewへのEscalationを担当し、Code、Data、Evidence、Timeline、Responsibility Assessment等の専門処理は必要に応じてSkillまたはSpecialist Agentへ委譲する。すべての重要ResultはEvidenceとSources Checkedを保持し、Codex Resume / SessionはWorking Historyとして活用する一方、Human Reviewedな調査成果はPersistent Investigation KnowledgeとしてSession外へ保存する。PoCではMulti-Agent化を目的化せず、単一Main Agentと明示的なSkillから開始し、Context、品質、並列性の必要性が確認された場合にのみAgent分割を進める。

## 100.1 2026-08-30 Agent Context Refinement

[DECIDED]

Main Agentが受け取るContext PackageへWork Item Type、Primary Objective、Secondary Objectives、現在のObjectiveを追加する。Objectiveが切り替わっても既存Evidence、Coverage、Missing Knowledge、選択Node、Human Review Stateを破棄せず、目的に応じてOperation、Stakeholder、Impact、Estimation用Skillを選び直す。Agent Executionは入力Artifact、出力Artifact、使用Source、生成物の保存先とStatusを記録する。PoC Agentへ未承認SourceのMasking判断やDetokenization責務を持たせない。

## 100.2 Infrastructure and Layer Traversal Skill（2026-08-30）

[DECIDED]

Agent / SkillはFunction、System、Infrastructure / IaCを別Conceptとして返す。IaC解析SkillはTerraform HCL、Module、Provider Resource、Plan、State Metadata、Drift ResultからResource GraphとProvenanceを生成し、Secret値をResultへ含めない。Main AgentはVertical Stackを使って未確認層を判定し、詳細探索時はFunction、System、Infrastructure、Code、Data Flow等のFlat Projectionへ切り替える。Agent分割の有無にかかわらず、切替時にCurrent Work Item、Objective、Stable ID、EvidenceをContext Packageへ保持する。
