# AI-Ready Operations Repository / Codex App
## 15. PoC Plan and Acceptance Criteria

**File Name:** `15_POC_PLAN_AND_ACCEPTANCE_CRITERIA.md`  
**Status:** Draft  
**Document Role:** PoC Execution Plan / Validation Scope / Acceptance Criteria  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、本ProjectのPoCを別PC・別Account・対象Repository上で開始する際に、

- 何から確認するか
- どこまで実装するか
- 何をGolden Sample / Golden Caseとするか
- 何をPoC成功とみなすか
- 何をPoCではやらないか
- Semantica等をどの段階で評価するか
- Security / Human Reviewをどこで確認するか

を具体的な実行計画として定義する。

本PoCの目的は、

> 完成したAI運用保守Platformを作ること

ではない。

目的は、

> 一件の実運用に近い問い合わせについて、問い合わせメールから開始し、Repository内外のEvidenceを辿り、Technical Cause・Current Specification・Historical Context・Missing Knowledgeを整理し、Human Review後に再利用可能なPersistent Investigation Knowledgeとして残せることを確認する

ことである。

---

# 2. PoCの基本原則

[DECIDED]

PoCでは以下を守る。

1. Existing Repositoryを先に確認する
2. Repositoryを確認する前にDirectory再編しない
3. 一件のGolden Caseから開始する
4. 一つまたは少数のGolden Documentから開始する
5. Originalを置き換えない
6. Codex Resume / Sessionを過去調査の参考Sourceとして確認する
7. 今後の重要な調査成果はSession外へ保存する
8. EvidenceとProvenanceを重視する
9. Missing Knowledgeを隠さない
10. Human Reviewを必須とする
11. Graph DB / Vector DB / Multi-Agentを先に目的化しない
12. Semanticaは評価対象であり採用前提としない

---

# 3. PoC Successの定義

[DECIDED]

PoC成功とは、

> AIが問い合わせに正解したこと

だけではない。

最低限以下が成立することを成功とする。

- Raw Inquiryから調査を開始できる
- Related Code / Data / Test / Documentへ到達できる
- Technical CauseをEvidence付きで整理できる
- Current Specification確認状況を説明できる
- Historical Evidenceの必要性を判断できる
- Sources Checked / Not Checkedが分かる
- Missing Knowledgeを明示できる
- HumanがAssessmentをReviewできる
- Persistent Investigation Knowledgeとして保存できる
- 次回Caseから再利用可能な状態にできる

---

# 4. PoCを段階的に進める

[DECIDED]

PoCは以下のPhaseで進める。

1. Phase 0: Environment / Repository Discovery
2. Phase 1: Security / Decision Gate
3. Phase 2: Golden Case / Golden Document Selection
4. Phase 3: Minimal Knowledge Model
5. Phase 4: Minimal Ingest / Retrieval
6. Phase 5: Case Investigation
7. Phase 6: Persistent Investigation Save
8. Phase 7: Minimal UI / DX
9. Phase 8: Semantica Evaluation
10. Phase 9: Acceptance Review
11. Phase 10: Next Architecture Decision

すべてを同時実装しない。

---

# 5. Phase 0: Environment / Repository Discovery

[POC-MUST]

最初に対象Repositoryを実査する。

このPhaseでは大きな変更を行わない。

---

# 6. Phase 0で確認する対象

[POC-MUST]

最低限以下を確認する。

- Repository Root
- Main Source Code
- Inquiry / Investigation Folder
- Test Specification
- Design Document
- Release Document
- Operation Document
- Existing AI / Codex Related Files
- `AGENTS.md`
- Git History
- `.gitignore`
- Large Binary
- Current / Historical Document Pattern
- Existing Scripts / Tooling

---

# 7. Existing Inquiryの確認

[POC-MUST]

既存の問い合わせFolderを複数件確認し、

- Folder単位
- Naming
- Input Inquiry
- Investigation Result
- SQL
- Code Reference
- Final Response
- Test
- Fix

がどの程度残っているか確認する。

既存構造をCase ModelへどうMappingするか判断する材料とする。

---

# 8. Existing Codex Resume / Sessionの確認

[POC-MUST]

利用可能であれば、対象Repositoryから起動して過去に行われたCodex Resume / Sessionも確認する。

特に以下を見る。

- Inquiry Folderより詳細な調査履歴が残っているか
- Sources Checkedが分かるか
- Code Investigation経路が分かるか
- Final Resultに至るまでの情報が残っているか
- 人間が追加したContextが残っているか
- Open Questionsが残っているか

Resumeを正本にはしない。

既存Knowledgeを復元するための参考Sourceとして利用する。

---

# 9. Phase 0 Deliverable

[POC-MUST]

Repository Discovery結果を一回限りのChatで終わらせない。

最低限以下を記録する。

- Repository Structure Summary
- Existing Inquiry Pattern
- Test Document Pattern
- Design Document Pattern
- Git Usage
- Existing Codex Sessionの利用可能性
- Current / Historical管理方法
- Security Risk候補
- Architecture Assumptionとの差
- Open Questions

---

# 10. Repositoryを最初に再編しない

[DECIDED]

Phase 0では以下を行わない。

- Existing Inquiry Folderの一括移動
- Test Folderの移動
- 全Document Markdown化
- 新しい巨大Directory Tree作成
- Full Graph生成

まず理解する。

---

# 11. Phase 1: Security / Decision Gate

[POC-MUST]

PoCで利用するData範囲を確認する。

特にMeeting Minutes等は、実装前にPolicy確認する。

---

# 12. Management / Security確認

[POC-MUST]

最低限以下を確認する。

1. PoCでAI利用承認済みのSource Setはどれか
2. 明示的にExcludedとするSourceはどれか
3. Existing Access Controlと閲覧権限をどう引き継ぐか
4. Repository / Gitへ保存できる範囲はどこまでか
5. Responsibility / Contract Detailを扱える範囲はどこまでか
6. Production DataをCodexへ渡せる条件は何か
7. Retention / Archive / Permanent DeleteのRuleは何か

利用者によるFile単位の分類・Masking判断はPoC運用に含めない。Masking等が必要なSourceは承認済みSetへ入れず、Production Security Assessmentへ送る。

---

# 13. Security Decisionが未確定の場合

[DECIDED]

Meeting Minutes利用可否等が未確定でもPoCは進められる。

その場合、

- Historical Evidence: Not Checked
- Access Restricted
- Human Check Required

を正しく表現する。

Security確認のためにPoC全体を停止する必要はないが、禁止Sourceを勝手に利用しない。

---

# 14. Phase 1 Deliverable

[POC-MUST]

最低限以下を記録する。

- Allowed Source
- Restricted Source
- Git Allowed / Prohibited
- AI Allowed / Prohibited
- Human Only Source
- Open Security Decisions

---

# 15. Phase 2: Golden Case Selection

[POC-MUST]

実運用に近い問い合わせを一件選ぶ。

理想的なGolden Caseは、

- Raw Inquiry Emailがある
- Code Investigationが必要
- Data / SQL確認が関係する
- Test Specificationが関係する
- Current Specification確認が必要
- Past Inquiryを利用できる
- 可能であればHistorical Evidenceが関係する

Caseとする。

---

# 16. Golden Caseを複雑にしすぎない

[DECIDED]

PoC最初のCaseとして、

- 複数System跨ぎ
- 大規模Incident
- Customer Contract紛争
- 大量Production Data

等の最難関Caseを選ぶ必要はない。

ただし単純すぎてRepository横断調査が不要なCaseも避ける。

---

# 17. Golden Case Selection Record

[POC-MUST]

選んだ理由を記録する。

候補：

- Representative
- Existing Evidence Available
- Code Path Understandable
- Test Available
- Historical Context Available / Missing
- Security Safe

---

# 18. Golden Document Selection

[POC-MUST]

Golden Caseに関連するDocumentを少数選ぶ。

候補：

- Test Specification
- Design Document
- Existing Inquiry Folder
- Release Document

---

# 19. Golden Documentの第一候補

[PROVISIONAL]

実Repository確認前の第一候補は、

> Golden Caseに関連するTest Specification

とする。

理由：

- 現行仕様Evidenceとして重要
- Excel等の構造変換評価ができる
- FunctionとのRelationを作りやすい
- Provenance粒度を評価できる

ただし実File確認後に変更可能。

---

# 20. Phase 2 Deliverable

[POC-MUST]

- Golden Case
- Golden Document
- Related Code Scope
- Related Test
- Related Historical Evidence
- Expected Investigation Outcome

を定義する。

---

# 21. Phase 3: Minimal Knowledge Model

[POC-MUST]

Golden Caseに必要なEntity / Relationだけを実装する。

---

# 22. Minimal Entity候補

[PROVISIONAL]

最低候補：

- Case
- Function
- Code Function
- Table / Data Source
- TestCase
- Document / Evidence
- PastInquiry

Historical Evidenceが利用可能なら、

- Decision

を追加する。

---

# 23. Minimal Relation候補

[PROVISIONAL]

- AFFECTS
- IMPLEMENTED_BY
- READS
- WRITES
- TESTED_BY
- EVIDENCED_BY
- SIMILAR_TO
- DEFINED_BY

必要性が確認できないRelationは作らない。

---

# 24. Knowledge State

[POC-MUST]

最低限以下を区別する。

- human_reviewed
- ai_extracted
- ai_inferred
- needs_review
- unknown

---

# 25. Current / Historical

[POC-MUST]

最低限、

- current
- historical
- unknown

を区別できる構造を持つ。

---

# 26. Provenance

[POC-MUST]

Golden KnowledgeからOriginalへ戻れること。

最低候補：

- File
- Git CommitまたはVersion
- Sheet / Page / Slide / Symbol
- Extraction Method
- Review State

---

# 27. Phase 3 Deliverable

[POC-MUST]

Golden Caseに必要な、

- Entity List
- Relation List
- Minimal Metadata
- Provenance Rule
- Knowledge State

を確定する。

Full Ontologyは作らない。

---

# 28. Phase 4: Minimal Ingest / Retrieval

[POC-MUST]

Golden DocumentをAI-Readyに変換する。

---

# 29. Minimal Ingest Flow

[POC-MUST]

1. Original Source取得
2. Document Type判定
3. Parse
4. Normalized Representation生成
5. Security Check
6. Knowledge抽出
7. Provenance付与
8. Validation
9. Search / Relationへ登録

---

# 30. Golden Document Outputを先に手設計する

[DECIDED]

Parserを作る前に、

> このDocumentから何が出れば問い合わせ調査に役立つか

を手作業で定義する。

例えば、

- content
- metadata
- relation
- provenance

の期待Outputを作る。

---

# 31. Minimal Search

[POC-MUST]

PoCでは最低限以下のどれかで必要Sourceへ到達できること。

- Repository Search
- Full Text Search
- Metadata Search
- Graph Relation

Vector Searchは必須ではない。

---

# 32. Code Retrieval

[POC-MUST]

Inquiry / FunctionからRelated Codeへ到達できること。

最初から全Repository Code Graphを作る必要はない。

---

# 33. Data Flow Retrieval

[POC-SHOULD]

Golden CaseでData Flowが重要なら、

- Code
- Table
- Batch
- File

の最低限Relationを作る。

---

# 34. Test Retrieval

[POC-MUST]

Golden Caseに関連するTest Evidenceへ到達できること。

---

# 35. Past Case Retrieval

[POC-MUST]

類似する既存問い合わせまたはPersistent Caseを最低一件検索できることが望ましい。

---

# 36. Phase 4 Deliverable

[POC-MUST]

- Golden Document AI-Ready Output
- Searchable Knowledge
- Provenance
- Minimal Relation
- Retrieval Demo

---

# 37. Phase 5: Golden Case Investigation

[POC-MUST]

Raw Inquiry EmailをCodexへ入力して調査を開始する。

人間が最初から全File Pathを指示しないことを基本とする。

---

# 38. Golden Case Investigation Flow

[POC-MUST]

1. Inquiry Intake
2. Symptom Understanding
3. Investigation Planning
4. Repository Investigation
5. Code / Data Investigation
6. Technical Cause
7. Current Specification
8. Test Evidence
9. Past Inquiry
10. Historical Evidence
11. Coverage / Missing Knowledge
12. Assessment Material

---

# 39. Historical Evidenceの扱い

[POC-MUST]

Meeting Minutes等を利用できる場合は実際に確認する。

利用不可の場合は、

> Historical Evidence未確認

という結果を正しく扱う。

PoC成功条件をHistorical Evidenceの直接利用だけに依存させない。

---

# 40. Codex Resume利用

[POC-SHOULD]

Golden Caseが過去問い合わせと関係する場合、利用可能なら過去Codex Resumeを確認する。

その結果、

- Existing Folderだけでは不足する情報
- Resumeにしかない調査経路
- Persistent化すべきKnowledge

を確認する。

---

# 41. Sources Checked

[POC-MUST]

Caseで実際に確認したSourceを記録する。

---

# 42. Sources Not Checked

[POC-MUST]

確認していないSourceと理由を記録する。

---

# 43. Missing Knowledge

[POC-MUST]

判断に必要だが不足している情報を明示する。

---

# 44. Technical Cause

[POC-MUST]

Evidence付きでTechnical Causeを特定する。

特定できない場合は、

- Unknown
- Reason
- Next Investigation

を明示する。

---

# 45. Current Specification

[POC-MUST]

Current BehaviorとCurrent Specificationを分離して整理する。

Codeだけで仕様確定しない。

---

# 46. Classification

[POC-SHOULD]

Golden Caseを以下等の候補へ整理する。

- Current Specification
- Implementation Bug
- Specification Omission
- Additional Requirement
- Operation Cause
- Data Cause
- Unknown

最終責任とは分離する。

---

# 47. Responsibility Assessment Material

[POC-SHOULD]

必要な場合、

- Technical Cause
- Current Specification
- Historical Agreement
- Difference
- Evidence
- Missing Evidence

をHuman Review用にまとめる。

---

# 48. Phase 5 Deliverable

[POC-MUST]

Golden Caseの、

- Investigation Summary
- Technical Cause
- Evidence
- Current Specification
- Sources Checked
- Sources Not Checked
- Missing Knowledge
- Assessment Candidate

を作成する。

---

# 49. Phase 6: Human Review

[POC-MUST]

AI調査結果をHumanがReviewする。

---

# 50. Human Review対象

[POC-MUST]

- Symptom
- Technical Cause
- Evidence
- Current Specification
- Historical Evidence
- Missing Knowledge
- Classification
- Responsibility Assessment Material
- Customer Draft

---

# 51. Human Correction

[POC-SHOULD]

AI結果を修正した場合、重要なCorrectionを記録する。

目的：

- Knowledge改善
- Prompt / Skill改善
- PoC評価

---

# 52. Responsibility / Cost

[DECIDED]

責任・契約・費用はPoCでもAIだけで確定しない。

---

# 53. Phase 6 Deliverable

[POC-MUST]

Human Reviewedな、

- Final Investigation Summary
- Final Classification
- Approved Assessment Position
- Response Draft

を作成する。

---

# 54. Phase 7: Persistent Investigation Save

[POC-MUST]

Human Review後の調査結果をCodex Session外へ保存する。

このPhaseはPoC成功の必須条件とする。

---

# 55. 保存候補

[PROVISIONAL]

最低候補：

- Case ID
- Inquiry Reference
- Investigation Summary
- Technical Cause
- Evidence
- Current Specification
- Sources Checked
- Sources Not Checked
- Missing Knowledge
- Human Review
- Final Response

---

# 56. Save Location

[OPEN]

実Repository確認後に、

- Existing Inquiry Folder
- Overlay
- Central Case

等から選ぶ。

PoCでは最小変更を優先する。

---

# 57. Save Format

[OPEN]

候補：

- Markdown
- Markdown + YAML
- Markdown + JSON

Human ReadabilityとMachine Retrievalの両方を確認する。

---

# 58. Related Codex Resume

[POC-SHOULD]

Persistent Caseから関連ResumeをReference可能なら保存する。

ただしResumeがなくても重要内容は残るようにする。

---

# 59. Phase 7 Deliverable

[POC-MUST]

Codex Sessionを終了しても、

> Golden Caseの重要調査結果を次Sessionから再取得できる

ことを確認する。

---

# 60. Phase 8: Knowledge Reuse

[POC-MUST]

新しいCodex Sessionまたは新しいQueryからGolden Caseを検索する。

---

# 61. Reuse Test

[POC-MUST]

最低限以下を確認する。

- FunctionからGolden Caseが見つかる
- Similar InquiryからGolden Caseが見つかる
- Technical Causeを再利用できる
- Evidenceへ戻れる
- Human Reviewed Stateが分かる

---

# 62. Session Independence Test

[POC-MUST]

元のCodex Session Contextなしで、Persistent Knowledgeから必要情報を取得できることを確認する。

---

# 63. Phase 8 Deliverable

[POC-MUST]

> 一度調べたことが、次の調査で再利用できる

ことをDemoする。

---

# 64. Phase 9: Minimal UI / DX

[POC-SHOULD]

Production UIではなく、Developerが調査状態を確認できる最小Viewを作る。

CLI / Markdown / Local Web / VS Code等、形式は問わない。

---

# 65. Minimum UI Information

[POC-SHOULD]

- Current Case
- Original Inquiry
- Technical Cause
- Evidence
- Sources Checked
- Sources Not Checked
- Missing Knowledge
- Human Review State
- Persistent Save State

---

# 66. Graph UI

[OPTIONAL]

Golden ObjectiveでGraphが明確に有用なら、Work Item Subgraphを表示する。

Repository全Graph表示は不要。

Graph UIを採用する場合は、目的別Viewを最初からすべて実装しない。共通Projection Contractを使い、最低限以下を確認する。

1. `Case` Viewを初期表示できる
2. Golden Caseで価値の高い2 View以上を切り替えられる
3. `Current only + Related to current Case + Depth 2`が既定値になる
4. View切替後もCurrent Caseと選択Contextが維持される
5. Node / EdgeからEvidence Sourceへ戻れる
6. Missing Relation / Not Checked / Restrictedを0件と区別できる

PoCで未実装のViewも、同じCanonical Relation Modelから追加できる設計であることを確認する。

---

# 67. Timeline UI

[OPTIONAL]

Golden Caseで時間関係が重要なら追加する。

---

# 68. Runtime Health

[POC-SHOULD]

最低限、

- Current Git Commit
- Indexed Commit
- Stale State
- Last Build

を確認できることが望ましい。

---

# 69. Phase 10: Semantica Evaluation

[POC-SHOULD]

SemanticaはGolden Case / Golden Documentを使って部分評価する。

全面採用は行わない。

---

# 70. Semantica Evaluation Track

[PROVISIONAL]

優先順：

1. Parse / Normalize
2. Provenance
3. Graph / Relation
4. Context Query
5. Temporal
6. Conflict
7. MCP

---

# 71. Semantica Version

[POC-MUST if evaluated]

利用Versionを固定して記録する。

---

# 72. Documentationではなく実APIを確認する

[DECIDED]

Semantica評価では、

- Current Source
- Current API
- Contract Test

を優先する。

Plugin Exampleだけで評価しない。

---

# 73. Semantica Adoption Gate

[POC-SHOULD]

PoC後に以下のいずれかを決める。

- Adopt
- Partially Adopt
- Defer
- Reject

理由を記録する。

---

# 74. Semantica採用評価軸

[PROVISIONAL]

- Implementation Time
- Parse Quality
- Provenance
- Graph Quality
- Debuggability
- API Stability
- Security
- Rebuildability
- Replaceability

---

# 75. Semantica評価で確認しないもの

PoC初期では以下を後回しにする。

- Advanced Reasoning
- Causal Analysis
- Full Decision Engine
- Production Visualization
- Full Multi-Agent Integration

---

# 76. Runtime Storage Evaluation

[POC-SHOULD]

PoC実測後にRuntime Storageを評価する。

候補：

- JSON
- SQLite
- NetworkX
- Semantica
- Graph DB

---

# 77. SQLite Evaluation

[PROVISIONAL]

必要なら以下を確認する。

- Setup
- Query
- Relation
- Rebuild
- Debug
- Locking

---

# 78. Graph DB Gate

[DECIDED]

Graph DBは以下が必要になった場合のみ検討する。

- Multi-hop Queryが頻繁
- Relation数が大きい
- Reverse Impactが重要
- SQLite / JSONで不足

---

# 79. Vector Search Gate

[DECIDED]

Vector Searchは、

- Similar Inquiry
- Semantic Document Search

で明確な価値がある場合のみ追加する。

---

# 80. Multi-Agent Gate

[DECIDED]

Multi-Agentは、

- Main Context肥大化
- 並列調査価値
- Specialist分離による品質向上

が確認できた場合のみ追加する。

---

# 81. PoCでは作らないもの

[DECIDED]

初期PoCでは以下を原則作らない。

- Full Repository Restructure
- Full Knowledge Graph
- Full Document Conversion
- Full Multi-Agent
- Production Dashboard
- Enterprise IAM
- Full Graph DB Infrastructure
- Full Vector DB
- Automatic Responsibility Decision
- Automatic Customer Send
- All Past Case Migration
- All Meeting Minutes Migration

---

# 82. PoC Acceptance Category

[DECIDED]

Acceptanceを以下に分ける。

1. Repository Compatibility
2. Investigation
3. Evidence / Traceability
4. Knowledge Model
5. Persistence / Reuse
6. Human Review
7. Security
8. Runtime / Rebuild
9. Developer Experience
10. Technology Evaluation

---

# 83. Acceptance: Repository Compatibility

[POC-MUST]

合格条件：

- Existing Repositoryを実査した
- Existing Inquiry / Test構造を理解した
- PoCのために全面再編していない
- 追加構造が最小限
- Existing Workflowを壊していない

---

# 84. Acceptance: Inquiry Intake

[POC-MUST]

合格条件：

- Raw Inquiry Emailから開始できる
- AIがOriginal Inquiryへ戻れる
- Symptom / Expected Behaviorを区別できる

---

# 85. Acceptance: Investigation

[POC-MUST]

合格条件：

- Related Functionを特定できる
- Related Codeへ到達できる
- 必要なData / SQLへ到達できる
- Related Test / Documentへ到達できる

---

# 86. Acceptance: Technical Cause

[POC-MUST]

合格条件：

- Technical CauseをEvidence付きで整理できる

または、

- 原因未確定の理由を明示できる

---

# 87. Acceptance: Current Specification

[POC-MUST]

合格条件：

- Current BehaviorとCurrent Specificationを分離できる
- Current SpecificationのEvidenceを示せる
- 不明な場合は不明と表示できる

---

# 88. Acceptance: Historical Evidence

[POC-MUST]

合格条件：

- Historical Evidenceの必要性を判断できる
- 利用可能なら確認できる
- 利用不可ならRestricted / Not Checkedを明示できる

---

# 89. Acceptance: Sources Checked

[POC-MUST]

合格条件：

- AI / Humanが実際に確認したSourceが分かる

---

# 90. Acceptance: Sources Not Checked

[POC-MUST]

合格条件：

- 未確認Sourceと理由が分かる

---

# 91. Acceptance: Missing Knowledge

[POC-MUST]

合格条件：

- 判断に必要な不足Knowledgeを隠さない

---

# 92. Acceptance: Evidence Traceability

[POC-MUST]

合格条件：

- AssessmentからOriginal Evidenceへ戻れる

例：

- Code Symbol
- Excel Sheet / Row
- Document Page
- External Reference

---

# 93. Acceptance: Knowledge State

[POC-MUST]

合格条件：

- AI Extracted / AI Inferred / Human Reviewed等を区別できる

---

# 94. Acceptance: Conflict

[POC-SHOULD]

合格条件：

- Design / Test / Code等が異なる場合、一方を勝手に消さずConflictとして扱える

---

# 95. Acceptance: Human Review

[POC-MUST]

合格条件：

- HumanがTechnical Cause / Specification / AssessmentをReviewできる
- Responsibility / CostをAIだけで確定しない

---

# 96. Acceptance: Stakeholder Output

[POC-SHOULD]

合格条件：

- Human Reviewed KnowledgeからCustomer向けDraftを作れる
- Internal InvestigationとCustomer Responseを分離できる

---

# 97. Acceptance: Persistent Knowledge

[POC-MUST]

合格条件：

- Case終了時にSession外へ調査成果を保存できる
- Codex Resumeだけに依存しない

---

# 98. Acceptance: Reuse

[POC-MUST]

合格条件：

- 新Sessionから過去Caseを検索できる
- Evidenceへ再度辿れる
- Human Reviewed状態が分かる

---

# 99. Acceptance: Codex Resume

[POC-SHOULD]

合格条件：

- 既存Resumeが利用可能なら引き継ぎSourceとして参照できる
- ResumeがなくてもPersistent Knowledgeから再開できる

---

# 100. Acceptance: Runtime Rebuild

[POC-MUST]

合格条件：

- Runtime DB / Indexを削除して再構築できる
- Persistent Knowledgeが失われない

---

# 101. Acceptance: Stale Detection

[POC-SHOULD]

合格条件：

- OriginalとRuntime Revisionの不一致を検出できる

---

# 102. Acceptance: Security

[POC-MUST]

合格条件：

- 未承認Meeting Minutesを勝手にIngestしない
- Credentialを保存しない
- Restricted SourceをMissingと区別する
- Customer OutputにHuman Reviewがある
- Approved Source Set以外をIngestしない
- 利用者向け分類・Masking・原本復元UIがPoC必須操作になっていない

---

# 103. Acceptance: Developer Experience

[POC-SHOULD]

合格条件：

Developerが短時間で以下を把握できる。

- Current Case
- Evidence
- Coverage
- Missing Knowledge
- Review State
- Save State

---

# 104. Acceptance: Technology Independence

[POC-SHOULD]

合格条件：

- Graph DB / Semantica / Vector DBなしでもLogical Modelが維持される
- Technologyを交換可能な境界がある

---

# 105. Quantitative Metrics

[PROVISIONAL]

PoCでは必要に応じて以下を測定する。

- Inquiryから最初のRelevant Code到達時間
- Relevant Test到達時間
- Past Case発見時間
- Evidence数
- Missing Knowledge検出数
- Human Correction数
- Persistent Saveに必要な追加手作業
- Runtime Rebuild時間

数値目標はGolden Case実測後に設定する。

---

# 106. Qualitative Metrics

[POC-MUST]

Human評価として以下を確認する。

- 調査開始地点が分かりやすいか
- 根拠を信頼できるか
- 未確認情報が分かりやすいか
- 過去Caseを再利用しやすいか
- 現在の手作業より認知負荷が減るか
- Double Entryが増えていないか
- Codex Sessionが長くても現在地が分かるか

---

# 107. Baseline Comparison

[PROVISIONAL]

可能であれば現在のWorkflowと比較する。

Current：

- Raw Inquiry
- Codex
- NotebookLM
- Human Manual Integration

PoC：

- Raw Inquiry
- Case
- Retrieval
- Evidence / Coverage
- Human Review
- Persistent Knowledge

比較は「AI回答精度」だけにしない。

---

# 108. PoC Failureとして扱う状態

[DECIDED]

以下が発生する場合、Architecture再検討対象とする。

- AI-Ready化の人間作業が大きすぎる
- Originalへ戻れない
- Case保存が二重入力になる
- Graphを作っても調査に役立たない
- Runtime依存でKnowledgeが失われる
- Existing Repositoryを大きく壊す必要がある
- Security上主要Evidenceを扱えず代替もできない
- Semantica等のFramework保守が本体開発より重い

---

# 109. PoC終了時Decision

[DECIDED]

PoC終了時に以下をDecisionとして残す。

## Repository Architecture

- Overlay
- In-Place
- Central Index
- Hybrid

## Persistent Case Format

採用方式。

## Runtime Storage

SQLite等。

## Graph

採用範囲。

## Vector Search

必要性。

## Agent Architecture

Single + Skills / Multi-Agent。

## Semantica

Adopt / Partial / Defer / Reject。

## Meeting Minutes

Allowed Integration Level。

---

# 110. PoC Exit Criteria

[DECIDED]

以下が揃ったらPoC終了判断を行う。

1. Golden Case End-to-End完了
2. Human Review完了
3. Persistent Investigation保存完了
4. Reuse Test完了
5. Runtime Rebuild確認
6. Security Decisionの未解決事項整理
7. Semantica評価結果または未評価理由
8. Next Architecture Decision作成

---

# 111. PoC後にすぐProduction化しない

[DECIDED]

PoC成功後も、

- Security
- Multi-User
- Backup
- Performance
- Governance
- Operational Ownership

を確認してProduction Architectureを設計する。

---

# 112. Recommended First Execution Order

[DECIDED]

別PC / Account / Repositoryで最初に行う順序は以下。

1. Handoff Documentsを読む
2. Existing Repositoryを確認する
3. Existing Inquiry / Testを確認する
4. 利用可能ならPast Codex Resumeを確認する
5. Security Decisionを確認する
6. Golden Caseを選ぶ
7. Golden Documentを選ぶ
8. Minimal Knowledge Modelを作る
9. Minimal Ingestを作る
10. Golden CaseをCodexで調査する
11. Human Reviewする
12. Persistent Investigation Knowledgeを保存する
13. New SessionからReuse Testする
14. Semantica等を必要範囲だけ評価する
15. Architecture Decisionを更新する

---

# 113. CodexへのPoC実装指示原則

[DECIDED]

CodexはHandoff Document中の、

- `[DECIDED]`
- `[PROVISIONAL]`
- `[OPEN]`

を区別する。

`[OPEN]`を勝手に確定して大規模実装しない。

---

# 114. 実装前にCodexが提示すべきもの

[POC-SHOULD]

大きな変更前に、

- Existing Repository Findings
- Proposed Minimal Change
- Files to Add / Change
- Open Decision
- Security Concern

を提示する。

---

# 115. PoC Evidence Package

[PROVISIONAL]

PoC終了時に以下をまとめることを検討する。

- Golden Case
- Investigation Result
- Persistent Case File
- Screenshots / UI
- Runtime Rebuild Result
- Semantica Evaluation
- Open Questions
- Decision Log

---

# 116. 後続ドキュメントへの引き継ぎ

## `16_OPEN_QUESTIONS_AND_DECISION_LOG.md`

PoC開始前・実行中・終了時に残る、

- Open Question
- Decision
- Decision Owner
- Evidence
- Status

を集約する。

## `00_HANDOFF_INDEX.md`

全DocumentのReading Order、Status、PoC開始手順をまとめる。

---

# 116.1 2026-08-30 PoC Scope Refinement

[DECIDED]

PoCは問い合わせ調査をGolden ObjectiveとしてEnd-to-Endで検証するが、Domain ModelはWork Itemを中心にし、CaseはInquiry / IncidentのSubtypeとして扱う。少なくとも途中でSecondary Objective（例: Impact AnalysisまたはEstimation）を追加してもEvidence、確認済みSource、Missing Knowledge、選択Context、Review Stateが維持されることを確認する。

開始画面はPurpose-Firstとし、問い合わせ、システム理解、運用、障害、変更・見積り、関係者、Knowledge整備の入口を示す。PoCで全目的の専用画面を完成させる必要はなく、Golden Objectiveの実装とObjective切替契約を優先する。Graphは補助導線とし、固定8 Viewの完全実装をAcceptanceにしない。

PoC対象はAI利用承認済みSource Setに限定し、Excluded SourceをIngestしない。利用者向けFile分類、Masking、Token Vault、Detokenization、原本復元UI、Field Level ACLはPoC Out of Scopeとする。File / Dataについては登録方式、Work Item Link / Unlink、Archive / Restore、Runtime Rebuild、生成ArtifactのProvenance、削除前の影響Previewを最小限検証する。

# 117. PoC Decision Summary

## [DECIDED]

- PoCは一件のGolden CaseをEnd-to-Endで確認する
- Existing Repository Discoveryから開始する
- Existing Codex Resumeを利用可能なら確認する
- Security Decision Gateを先に確認する
- Golden Documentを少数に限定する
- Minimal Knowledge Modelから開始する
- Raw Inquiry EmailをInputにする
- Technical CauseとSpecificationを分ける
- Sources Checked / Not Checkedを必須とする
- Missing Knowledgeを必須とする
- Human Reviewを必須とする
- Persistent Investigation SaveをPoC必須とする
- New SessionからReuse Testする
- Runtime Rebuildを確認する
- Graph DB / Vector DB / Multi-Agentを先に導入しない
- Semanticaは部分評価する
- PoC成功後にArchitecture Decisionを更新する

## [PROVISIONAL]

- Golden Document第一候補はTest Specification
- SQLiteを軽量Runtime候補とする
- Minimal UIを作る
- Minimal GraphをGolden Caseへ適用する
- SemanticaはParse / Provenance / Graph / Contextを優先評価する

## [OPEN]

- Golden Case
- Golden Document
- Existing Inquiry Mapping
- Persistent Case Format
- Persistent Case Location
- Runtime Storage
- Graph Storage
- Vector Search
- Multi-Agent
- Semantica Adoption
- Meeting Minutes Integration

---

# 118. PoC Plan Statement

> 本ProjectのPoCは、一件の実運用に近い問い合わせをGolden ObjectiveとするWork Itemで、Raw InquiryからTechnical Investigation、Current Specification、Historical Evidence、Coverage、Missing Knowledge、Human Review、Persistent Knowledge保存、次Sessionでの再利用までをEnd-to-Endで成立させる。途中のObjective追加でも調査Contextが維持され、Purpose-First UIと最小Data Lifecycleが機能することを確認する。対象はAI利用承認済みSourceだけとし、利用者向け分類・Masking・原本復元はPoC範囲外とする。Runtime DB、Graph DB、Vector Search、Multi-Agent、Semanticaは実測結果に基づいて必要性を判断し、成功はEvidence Traceability、Investigation Reproducibility、Knowledge Reuse、Human Verifiability、Existing Workflow Compatibilityによって評価する。

## 118.1 Graph / IaC PoC Refinement（2026-08-30）

[DECIDED]

PoC Acceptanceへ、FunctionとSystemが別Node / Relationで説明できること、承認済みTerraform Golden SampleからInfrastructure / IaC Graphを生成できること、平面GraphとVertical Stackで同じStable ID / Evidenceを保持できることを追加する。IaC対象がGolden Caseに存在しない場合は小さな承認済みFixtureで、Module、Resource、Dependency、Source Location、Drift Stateの抽出を確認する。Secret値やState Payloadの取り込みはAcceptance対象外かつ禁止とする。自由回転3D UIはPoC必須とせず、読みやすい疑似立体Stackまたは整列階層表示で層横断理解を評価する。
