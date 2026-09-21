# AI-Ready Operations Repository / Codex App
## 13. UI and Developer Experience

**File Name:** `13_UI_AND_DEVELOPER_EXPERIENCE.md`  
**Status:** Draft  
**Document Role:** Developer UI / Investigation UX / Layered Graph Navigation / Evidence Visibility  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、運用保守担当DeveloperがCodex Appを利用して問い合わせ調査を行う際の、

- UI
- Developer Experience
- Case Navigation
- Evidence確認
- Coverage確認
- Missing Knowledge確認
- Graph利用
- Timeline利用
- Human Review
- Persistent Investigation Knowledge保存
- Runtime / Ingest状態確認

の設計方針を定義する。

本ProjectのUIは、AI Chatを綺麗に見せることを目的としない。

目的は、

> 調査の現在地、確認済みEvidence、未確認領域、判断根拠をDeveloperが短時間で把握できること

である。

---

# 2. UIの基本原則

[DECIDED]

本UIでは以下を優先する。

1. Current Caseが分かる
2. AIが何を確認したか分かる
3. Evidenceへ戻れる
4. 何を確認していないか分かる
5. AI推論とHuman Reviewed Factを区別できる
6. Graph / Timelineを調査に必要な範囲だけ見せる
7. Human Reviewが明確
8. Existing Repository Workflowを邪魔しない
9. VS Code / Codexとの往復が少ない
10. UIなしでもRepository上のKnowledgeを利用できる

---

# 3. UIをSource of Truthにしない

[DECIDED]

UIで編集・表示される情報の正本は、

- Repository
- Persistent Investigation Knowledge
- Approved Storage
- Runtime Index

に置く。

UI内部だけに重要な調査結果を保存しない。

UIを使わなくてもKnowledgeを復元できることを前提とする。

---

# 4. Developer-First UI

[DECIDED]

Primary Userは運用保守を担当するDeveloper / Engineerである。

そのため、一般利用者向けの単純Chat UIではなく、

- Code
- File
- Test
- SQL
- Evidence
- Git
- Graph
- Timeline
- Case Status

へすぐ移動できるDeveloper Toolとして設計する。

---

# 5. VS Code / Codexとの関係

[PROVISIONAL]

PoCでは以下の利用形態を第一候補とする。

- VS Code
- Codex
- Local Lightweight App / Panel
- Repository Files

UIがCodexを置き換えるのではなく、Codexによる調査を補助する。

---

# 6. Chatだけに依存しない

[DECIDED]

問い合わせ調査をChat履歴だけで理解する設計にしない。

Chatには、

- 調査依頼
- Additional Context
- Human Correction

等を入力できる。

一方で重要情報は別Viewとして表示する。

例：

- Case Summary
- Evidence
- Sources Checked
- Coverage
- Missing Knowledge
- Timeline
- Graph
- Review State

---

# 7. Main Screenの考え方

[PROVISIONAL]

Main Screenでは最低限以下を確認できることを目指す。

- Current Case
- Inquiry
- Investigation Status
- Findings
- Evidence
- Coverage
- Missing Knowledge
- Current Assessment
- Human Review State

PoC初期では1画面にすべて詰め込まず、Panel / Tabで分けてもよい。

---

# 8. Case Header

[PROVISIONAL]

Case Header候補：

- Case ID
- Title
- Status
- Inquiry Date
- Related Function
- Current Owner
- Human Review Status
- Last Updated

Caseを切り替えた際、現在どの問い合わせを調査しているか明確にする。

---

# 9. Raw Inquiry View

[DECIDED]

Original Inquiryを確認できるViewを持つ。

AI Summaryだけを表示しない。

候補表示：

- Original Email / Text
- Structured Summary
- Extracted Symptom
- Expected Behavior
- Missing Initial Information

---

# 10. Investigation Summary View

[DECIDED]

現在までの調査結果を短くまとめる。

候補：

- Symptom
- Technical Cause
- Current Specification
- Historical Evidence
- Assessment
- Next Action

各項目からEvidenceへ遷移できることが望ましい。

---

# 11. Evidence Panel

[DECIDED]

Caseに関連するEvidenceを一覧化する。

候補：

- Source Type
- Title
- Path / Location
- Version
- Current / Historical
- Checked / Not Checked
- Knowledge State
- Access State

---

# 12. EvidenceからOriginalへ戻る

[DECIDED]

Evidence SummaryからOriginal Sourceへ戻れることを重視する。

例：

- Source Code File / Symbol
- Excel Sheet / Row
- PowerPoint Slide
- PDF Page
- Git Commit
- External Source Reference

AI要約しか見えないUIにしない。

---

# 13. Sources Checked View

[DECIDED]

今回のCaseで実際に確認したSourceを明示する。

例：

- Source Code: Checked
- Test Specification: Checked
- Past Inquiry: Checked
- Historical Meeting: Not Checked
- Release History: Partial

---

# 14. Sources Not Checked View

[DECIDED]

確認していないSourceも明示する。

理由候補：

- Restricted
- Not Found
- Not Required
- Pending
- Tool Error
- Unknown Location

未確認領域を隠さない。

---

# 15. Coverage View

[DECIDED]

AIが何を覚えているかではなく、

> 今回どのKnowledge領域を確認したか

を表示する。

候補：

- Business
- Function
- System
- Data
- Implementation
- Test
- Current Design
- Historical Evidence
- Responsibility

---

# 16. Coverage State

[PROVISIONAL]

State候補：

- checked
- partial
- not_checked
- restricted
- not_applicable

単純なPercentageだけにしない。

---

# 17. Coverage UI例

[PROVISIONAL]

概念的には以下のような表示を想定する。

- Business: Checked
- Function: Checked
- System: Checked
- Implementation: Checked
- Test: Checked
- Historical Evidence: Partial
- Responsibility: Partial

そして、

`Missing: Historical design decision`

のように不足を明示する。

---

# 18. Missing Knowledge Panel

[DECIDED]

Missing Knowledgeを独立Viewとして扱う。

候補：

- Missing Historical Meeting
- Old Design Not Found
- Test Evidence Unknown
- Release Reason Unknown
- Responsibility Evidence Missing

AIが補完推論で隠さない。

---

# 19. Open Questions Panel

[DECIDED]

未解決Questionを表示する。

例：

- この条件は開発時に顧客と合意されたか
- このCode変更はどのReleaseで入ったか
- このSE対応の目的は何か

Open Questionを次の調査Actionへ繋げる。

---

# 20. Suggested Next Actions

[PROVISIONAL]

AIはMissing Knowledge / Coverageから次のAction候補を提示できる。

例：

- Search Past Inquiry
- Inspect Batch Code
- Check Test Specification
- Ask Human to Check NotebookLM
- Review Git History

自動実行とSuggestionを区別する。

---

# 21. Investigation Progress

[PROVISIONAL]

Workflow上の現在地を表示する。

候補：

1. Intake
2. Technical Investigation
3. Current Specification
4. Historical Evidence
5. Assessment
6. Human Review
7. Response
8. Persisted

直列完了率として扱わず、戻り作業を許容する。

---

# 22. Technical Cause View

[DECIDED]

Technical Causeを独立して表示する。

表示候補：

- Cause Summary
- Evidence
- Confidence / Knowledge State
- Related Code
- Related Data
- Related Test

Technical CauseとResponsibilityを混ぜない。

---

# 23. Current Specification View

[DECIDED]

Current Specification確認結果を独立表示する。

候補：

- Specification Summary
- Evidence Sources
- Current / Historical
- Human Review State
- Conflicts

Code BehaviorだけをSpecificationとして表示しない。

---

# 24. Historical Evidence View

[DECIDED]

過去Requirement / Meeting / Design / Release等をまとめる。

候補：

- Date
- Source
- Topic
- Decision
- Agreement
- Access State
- Human Checked

NotebookLM等のExternal Evidenceも表示できる構造にする。

---

# 25. Responsibility Assessment View

[DECIDED]

このViewでは最終責任をAIが確定表示しない。

表示候補：

- Observed Fact
- Technical Cause
- Current Specification
- Historical Agreement
- Difference
- Missing Evidence
- AI Assessment Candidate
- Human Decision

---

# 26. AI AssessmentとHuman Decisionを分ける

[DECIDED]

UI上でも、

**AI Assessment**

と

**Human Approved Decision**

を視覚的・構造的に区別する。

Human Decisionが未入力の場合、AI Assessmentだけで確定表示しない。

---

# 27. Review Status

[DECIDED]

Human Review状態を明示する。

候補：

- Not Reviewed
- Review Required
- Approved
- Approved with Changes
- More Investigation Required
- Blocked

---

# 28. Human Review Screen

[PROVISIONAL]

Humanが以下を確認・修正できることを目指す。

- Technical Cause
- Evidence
- Current Specification
- Historical Evidence
- Missing Knowledge
- Assessment
- Final Response

修正内容は可能な範囲でPersistent Knowledgeへ反映する。

---

# 29. Review Diff

[FUTURE]

AI DraftとHuman Finalの差分を確認できることを検討する。

目的：

- AI品質改善
- Knowledge Correction
- Audit

PoC初期では必須ではない。

---

# 30. Graph View

[DECIDED]

Graph ViewではRepository全体Graphを初期表示しない。

Current Work ItemとCurrent Objectiveに関連するSubgraphを表示する。

Graph Viewは独立したDashboardではなく、Work Item Workspaceから開く調査面として扱う。

## 30.1 Layer View Switcher

[DECIDED]

以下のViewを同じGraph領域で切り替えられることを設計上の標準とする。

```text
[ Work Item ] [ Domain ] [ Function ] [ System ] [ Infrastructure / IaC ]
[ Data Flow ] [ Code ] [ Test ] [ Evidence / History ] [ Operation ] [ Stakeholder ]
```

初期表示は`Work Item`とし、選択したNodeから関連Layerへ移動できる`Open in ...`操作を提供する。

## 30.2 Graph Filter

[DECIDED]

標準Filterは以下とする。

- Time: `Current only` / `Current + Historical`
- Scope: `Related to current Work Item` / `Entire project`
- Depth: `1 / 2 / 3`

通常利用の既定値は`Current only + Related to current Work Item + Depth 2`とする。

## 30.3 Context Preservation

[DECIDED]

View切替時にCurrent Work ItemとCurrent Objectiveを失わない。選択Nodeが次のViewにも含まれる場合は選択を維持し、Bridge Relationで接続される場合は遷移元をBreadcrumbとして残す。

## 30.4 Projection Result State

[DECIDED]

Viewごとに以下を表示する。

- 表示中のView / Scope / Time / Depth
- Node / Edge件数
- Sources Checked / Not Checked
- Missing Relation
- Stale / Restricted / Needs Review

0件の場合も空白にせず、`No relation found`、`Not ingested`、`Restricted`、`Filter excluded`を区別する。

## 30.5 Layer Viewの責務

| View | 主要な問い |
|---|---|
| Work Item / Case | この作業・問い合わせに何が関係するか |
| Domain | 業務上どこに位置するか |
| Function | 業務・利用者へ何を提供するか |
| System | FunctionをどのComponentで実現・稼働するか |
| Infrastructure / IaC | 実環境ResourceはどのTerraform等の定義から作られるか |
| Data Flow | この値はどこから来たか |
| Code | どの実装が処理するか |
| Test | 仕様はどのTestで検証されたか |
| Evidence / History | なぜ現在の仕様になったか |
| Operation / Runbook | 誰が何をどの順序で実行するか |
| Stakeholder / Responsibility | 誰が保守・運用・承認・相談を担うか |

## 30.6 Flat ProjectionとVertical Stack

[DECIDED]

Graph UIは2つの表現を使い分ける。

- Flat Projection: 同一観点のNode / Edgeを詳しく探索する
- Vertical Stack: `Inquiry / Work Item → Objective → Domain / Function → System / Infrastructure → Code / Data Flow / Test → Evidence`を上下の意味階層として把握する

Vertical Stackは実際の3D空間を自由回転させるUIを必須としない。疑似立体の層表示または整列した階層表示を優先し、文字・Relation・Accessibilityを保つ。両表現の切替時もStable ID、Work Item、Objective、選択Node、Evidenceを保持する。

---

# 31. Work Item Subgraph

[PROVISIONAL]

初期Node候補：

- Case
- Function
- Code
- Table
- Test
- Past Inquiry
- Design
- Meeting Decision

必要に応じて展開する。

---

# 32. Graph Expand

[PROVISIONAL]

Nodeを選択した際に、

- Related Code
- Related Test
- Historical Evidence
- Data Flow

等を段階的にExpandできることが望ましい。

---

# 33. Graph Node Detail

[PROVISIONAL]

Node選択時に表示する候補：

- Type
- Name
- Summary
- Knowledge State
- Current / Historical
- Provenance
- Source
- Related Case

---

# 34. Graph Edge Detail

[PROVISIONAL]

Edge選択時：

- Relation Type
- Evidence
- Extraction Method
- Review State
- Effective Date

を確認できることが望ましい。

---

# 35. GraphのColor依存を避ける

[DECIDED]

StatusやNode TypeをColorだけで表現しない。

Label / Icon / Text等も併用する。

AccessibilityとDeveloper Debuggabilityを考慮する。

---

# 36. Data Flow View

[PROVISIONAL]

Data起因問い合わせでは、Graphとは別にLinearなData Flow表示が有効な可能性がある。

例：

Input File  
→ Batch  
→ Table  
→ API  
→ Screen

このViewからCode / Evidenceへ遷移できることが望ましい。

---

# 37. Code Navigation

[DECIDED]

Code EvidenceからVS Codeの該当File / Symbolへ移動しやすくする。

DeveloperがUI内でCodeを再実装閲覧する必要はない。

既存IDEを活用する。

---

# 38. Test Navigation

[PROVISIONAL]

Test Evidenceから、

- Original Excel
- Sheet
- Row / Scenario

へ遷移できることを目標とする。

---

# 39. Timeline View

[PROVISIONAL]

複数種類のTimelineを表示できることを検討する。

## Runtime Timeline

事象発生時のData / Batch / User Operation。

## Historical Decision Timeline

Requirement / Meeting / Design / Release。

---

# 40. Timelineを一つに混ぜない

[DECIDED]

Business DateとMeeting Date等を同一Timelineに無条件で並べない。

目的に応じてTimeline Typeを分ける。

---

# 41. Past Case Search

[DECIDED]

UIから類似Past Caseを検索できることを目指す。

検索候補：

- Function
- Error
- Technical Cause
- Table
- Batch
- Similar Text
- Related Decision

---

# 42. Past Case Result

[PROVISIONAL]

表示候補：

- Case Title
- Date
- Function
- Cause
- Resolution
- Similarity Reason
- Human Review State

Embedding Scoreだけを表示しない。

---

# 43. Past Case比較

[FUTURE]

Current CaseとPast Caseを並べ、

- Same
- Different
- Unknown

を比較できるViewを検討する。

---

# 44. Codex Resume Reference

[PROVISIONAL]

既存Caseで関連Codex Resume / Sessionが利用可能な場合、Referenceを表示できることが望ましい。

ただしUIの主要KnowledgeはPersistent Investigation Knowledgeを優先する。

---

# 45. ResumeをMain Viewにしない

[DECIDED]

Codex Session全文をCase UIの中心にしない。

必要な場合にWorking Historyとして参照する。

---

# 46. Agent Execution View

[PROVISIONAL]

Multi-Agent / Skillを利用する場合、現在実行中のTaskを表示する可能性がある。

候補：

- Agent / Skill
- Task
- Status
- Sources Checked
- Result
- Error

---

# 47. Agent人格を前面に出しすぎない

[DECIDED]

UIで、

- Code Agent
- Evidence Agent

等をキャラクターのように強調するより、

> 何の調査が行われているか

を優先表示する。

---

# 48. Execution History

[PROVISIONAL]

重要な実行履歴だけ表示する。

例：

- Searched Code
- Checked Test
- Historical Evidence Restricted
- Human Review Requested

詳細Tool LogはDebug Viewへ分離する。

---

# 49. Developer Debug View

[PROVISIONAL]

PoCではDeveloper自身が仕組みを検証するため、Debug情報を確認できることが重要。

候補：

- Retrieved Source
- Query
- Node / Edge ID
- Provenance
- Runtime Store
- Last Processed Commit
- Transformer Version
- Skill Version

---

# 50. Retrieval Transparency

[DECIDED]

AI回答だけでなく、

> なぜこのSourceが取得されたか

をDeveloperがある程度確認できることを目指す。

候補：

- Exact Match
- Graph Relation
- Same Function
- Semantic Similarity
- Past Case Relation

---

# 51. Search UI

[PROVISIONAL]

Unified Searchを設ける場合、以下を横断検索する。

- Files
- Knowledge
- Cases
- Code
- Test
- Decisions

Search Result Typeを区別する。

---

# 52. Search Filter

[PROVISIONAL]

候補：

- Type
- Current / Historical
- Function
- Date
- Knowledge State
- Access State
- Source Type

---

# 53. Search ResultのProvenance

[DECIDED]

AI-Ready Summaryだけでなく、Original Source情報を表示する。

---

# 54. External Source Result

[DECIDED]

External Sourceの場合、

- External
- Human Only
- Restricted
- Checked

等の状態を明示する。

Repository内Fileと同じように見せない。

---

# 55. Ingest Status View

[PROVISIONAL]

AI-Ready変換状態を確認できることを検討する。

候補：

- Converted
- Pending
- Failed
- Warning
- Stale
- Needs Review
- Restricted

---

# 56. Stale Knowledge表示

[DECIDED]

Original更新後にDerivedが古い場合、

`stale`

を明示する。

古いDerivedをCurrentとして自然に見せない。

---

# 57. Runtime Health View

[PROVISIONAL]

Developer向けに以下を確認できることが望ましい。

- Current Git Commit
- Indexed Commit
- Last Build
- Runtime DB State
- Graph State
- Search State
- Stale Count
- Failed Count

---

# 58. Rebuild操作

[PROVISIONAL]

必要に応じてDeveloperが、

- Rebuild Knowledge
- Rebuild Graph
- Rebuild Search
- Full Rebuild

を実行できるようにする。

PoCではCLIでもよい。

---

# 59. Rebuildを通常操作にしない

[DECIDED]

日常利用のたびにFull Rebuildを要求しない。

Incremental Updateを基本とする。

---

# 60. Repository Validation View

[FUTURE]

Repository Qualityを確認するViewを検討する。

例：

- Missing Metadata
- Missing Test Relation
- Orphan Knowledge
- Stale Derived
- Restricted Unknown
- Conflict

---

# 61. Conflict View

[DECIDED]

Source間Conflictを明示する。

例：

- Design vs Code
- Test vs Current Behavior
- Meeting Decision vs Implementation

一方をAIが勝手に非表示にしない。

---

# 62. Conflict Resolution

[PROVISIONAL]

Human Reviewで、

- Current
- Historical
- Incorrect
- Needs Investigation

等を設定できることを検討する。

---

# 63. Security Warning

[DECIDED]

Sensitive / Restricted操作では明確にWarningする。

例：

- External Restricted Source
- Git Prohibited
- PII Detected
- Customer Output Review Required

---

# 64. Security Warningを乱発しない

[DECIDED]

すべてを同じ赤Warningにすると無視される。

Blocking / Review / Informationalを分ける。

---

# 65. Access Restricted UI

[DECIDED]

参照不可Sourceについて、

- Exists
- Restricted
- Human Review Required

を表示する。

内容をPreviewしない。

---

# 66. Human External Check

[PROVISIONAL]

NotebookLM等のHuman-only Source確認が必要な場合、

Taskとして表示することを検討する。

例：

`Check historical design meeting for Function X`

Humanが確認後、

- Checked
- Summary
- Evidence Reference

をCaseへ追加できる。

---

# 67. Persistent Save UI

[DECIDED]

Case終了時に、

> Save Investigation Knowledge

を明示的なStepとして扱う。

ただし毎回大量のForm入力を要求しない。

CodexがDraftを生成し、HumanがReviewして保存する方式を基本候補とする。

---

# 68. Save Preview

[PROVISIONAL]

保存前に以下を確認できることが望ましい。

- What will be saved
- Where
- Security Classification
- Human Review State
- Git Commit Candidate
- External References

---

# 69. Save Location

[OPEN]

Existing Inquiry Folder / Overlay / Central Case等の保存先は実Repository確認後に決定する。

UIはStorage実装へ強く依存しないようにする。

---

# 70. Git Diff View

[PROVISIONAL]

Persistent Knowledge保存時、Git管理対象であればDiffを確認できることが望ましい。

特に、

- Human Correction
- New Relation
- Case Summary

をReviewしやすくする。

---

# 71. Git Commitは自動確定しない

[DECIDED]

Security / Human Reviewが必要なKnowledgeを、AIが無条件でCommitしない。

---

# 72. Stakeholder Output View

[DECIDED]

同じCase Knowledgeから、Audience別Draftを生成できる。

候補：

- End User
- Customer System / Management
- Developer
- Internal Review

---

# 73. Output Audienceを明示する

[DECIDED]

誰向けDraftかを明確にする。

内部向けTechnical AssessmentをCustomer向けへ誤利用しない。

---

# 74. Customer Draft Review

[DECIDED]

Customer向けDraftにはHuman Review必須状態を表示する。

---

# 75. Copy / Export

[PROVISIONAL]

Review済みOutputを、

- Clipboard
- Markdown
- Email Draft用Text

等へ出せることを検討する。

PoCではCopy可能なTextで十分。

---

# 76. UIから直接送信しない

[DECIDED]

PoCではCustomerへ自動送信しない。

正式送信は既存Communication Workflowを利用する。

---

# 77. Context Inspector

[PROVISIONAL]

Developerが、

> 今回CodexへどのContextが渡されているか

を確認できるViewを検討する。

候補：

- Current Case Summary
- Retrieved Sources
- Work Item Subgraph
- Missing Knowledge

LLM Memoryの中身を表示するのではなく、Retrieval Contextを表示する。

---

# 78. Context Coverage

[DECIDED]

「AIがRepository全体を理解済み」のような表現を避ける。

代わりに、

- Retrieved
- Checked
- Not Checked
- Restricted

を表示する。

---

# 79. Session Resume UX

[PROVISIONAL]

過去Codex Sessionを参照する場合、

- Related Resume Available
- Last Session Date
- Open Working History

等を表示する可能性がある。

Persistent Case Knowledgeがある場合はそちらを優先する。

---

# 80. New Case UX

[PROVISIONAL]

新しい問い合わせでは、

1. Email本文をPaste
2. Case Draft作成
3. Similar Past Case Search
4. Investigation Plan生成
5. Codex調査開始

という短い入口を目指す。

---

# 81. Existing Case Resume UX

[PROVISIONAL]

既存Case再開時：

1. Persistent Investigation Summary表示
2. Open Questions表示
3. Missing Knowledge表示
4. Related Resumeがあれば参照
5. New Evidence確認
6. Investigation再開

---

# 82. UI状態をSessionだけに持たない

[DECIDED]

Case Status、Review State等の重要状態はPersistentまたはRuntime Storeへ保存する。

Browser / App再起動で消えないことが望ましい。

---

# 83. User入力負荷を減らす

[DECIDED]

AI-Ready運用のために、Developerへ大量Metadata入力を要求しない。

自動抽出可能なものは自動生成し、

Humanには、

- Correction
- Approval
- Missing Context

を中心に求める。

---

# 84. Progressive Disclosure

[DECIDED]

通常利用では必要な情報だけ表示し、詳細Debug情報は展開式にする。

例：

Main：
- Cause
- Evidence
- Missing

Advanced：
- Node ID
- Transformer Version
- Raw Retrieval Score

---

# 85. Keyboard / Developer Workflow

[PROVISIONAL]

Developer向けUIでは、Mouse操作だけでなく、

- Command Palette
- Shortcut
- CLI
- File Link

等との連携を検討する。

---

# 86. CLIとの共存

[DECIDED]

UIでしか実行できない重要処理を増やしすぎない。

PoCでは、

- ingest
- validate
- rebuild
- inspect-case

等をCLIでも実行可能にする方式が望ましい。

具体CLIは未決定。

---

# 87. UIとConfig

[DECIDED]

Project固有UI項目をHard Codingしすぎない。

例：

- Stakeholder Type
- Coverage Category
- Document Type
- Security Label

はConfigから変更できることを検討する。

---

# 88. UIとTechnology Independence

[DECIDED]

UIを、

- Neo4j
- Semantica
- SQLite

等のStorage製品へ直接依存させない。

Query / Service Layerを介する。

---

# 89. Local App候補

[OPEN]

PoC実装候補：

- VS Code Extension / Webview
- Local Web App
- Terminal UI
- Simple Static HTML + Local Service

実装コストとDeveloper Workflowを見て選択する。

---

# 90. PoCではUIを作り込みすぎない

[DECIDED]

PoCの目的は調査成立性の確認。

そのため最初からProduction Dashboardを作らない。

最低限、

- Case
- Evidence
- Coverage
- Missing Knowledge
- Review
- Persistent Save

が確認できればよい。

---

# 91. PoC Minimum UI

[PROVISIONAL]

第一候補：

## Case Overview

問い合わせ・原因・Assessment。

## Evidence

Sources Checked / Source Link。

## Coverage / Missing

未確認領域。

## Review / Save

Human ReviewとPersistent Save。

Graph / Timelineは必要性が高い場合のみ追加する。

---

# 92. Graph PoC UI

[PROVISIONAL]

Graphを実装する場合も、Golden CaseのSubgraphだけ表示する。

NodeをClickしてEvidenceへ飛べることを重視する。

Graph UIをPoCへ含める場合、すべての目的別Viewを完全実装する必要はない。ただし共通Projection ContractとView Switcherを前提にし、最低限`Work Item`とGolden Objectiveで価値が高い2 Viewを切り替え、Current Work Item、Current Objective、Evidence、選択Contextが維持されることを確認する。

---

# 93. UI Acceptance Criteria

PoCでは以下を確認する。

1. Current Caseが分かる
2. Original Inquiryを確認できる
3. Technical CauseをEvidence付きで見られる
4. Current Specificationを確認できる
5. Sources Checkedが分かる
6. Sources Not Checkedが分かる
7. Missing Knowledgeが分かる
8. Human Review状態が分かる
9. Persistent Save対象が分かる
10. Original Sourceへ戻れる

---

# 94. Developer Experience Acceptance

以下を目指す。

- Fileを探し回る時間が減る
- 調査の開始地点が分かる
- 過去Caseを探しやすい
- Evidenceを確認しやすい
- 未確認情報を見落としにくい
- Codex Sessionが長くても現在地が分かる
- 別SessionでもPersistent Knowledgeから再開できる

---

# 95. UI Anti-Patterns

## Chat Only

全調査状態をChat履歴だけで表現する。

## AI Memory Badge

「AIはRepositoryを理解済み」と表示する。

## Full Graph First

Repository全体Graphを最初に表示する。

## Hidden Missing Knowledge

未確認Sourceを表示しない。

## AI Decision as Final

AI AssessmentをHuman Decisionと同じ見た目にする。

## Summary Without Source

EvidenceへのLinkがない。

## Runtime Health Hidden

Indexが古くても正常に見える。

## Dashboard Before Workflow

PoC前に大規模UIを作る。

---

# 96. Current Open Questions

[OPEN]

## UI Technology

VS Code / Web App / CLI / Hybrid。

## Graph Visualization

PoCへ含めるか。含める場合、どのLibrary / LayoutでProjection Contract、Keyboard操作、Node / Edge Detailを実現するか。

## Timeline

PoCで必要か。

## Case Editing

Markdown直接編集 / UI Form。

## Human Review UX

具体操作。

## Resume Navigation

Codex ResumeをどこまでUIから参照できるか。

## Git Diff Integration

UIへ入れるか。

## External Evidence Task

NotebookLM確認Taskの表現方法。

---

# 97. 後続ドキュメントへの引き継ぎ

## `14_SEMANTICA_EVALUATION.md`

- Graph / Context / ProvenanceをUIへどう供給できるか
- Semantica採用時のUI非依存性

## `15_POC_PLAN_AND_ACCEPTANCE_CRITERIA.md`

- PoC Minimum UI
- Golden Case UI
- Developer Experience評価
- Evidence / Coverage / Persistence確認

## `16_OPEN_QUESTIONS_AND_DECISION_LOG.md`

- UI Technology
- Graph View
- Review UX
- Resume Integration
- External Evidence UX

---

# 97.1 Purpose-First WorkspaceとData UI（2026-08-30）

[DECIDED]

LandingではGraph Layerを先に選ばせず、「何をしますか？」を最初に聞く。候補は問い合わせ調査、システム理解、運用作業、障害調査、変更・影響調査・見積り、関係者確認、Knowledge整備とする。選択したPrimary Objectiveに応じて入力項目、Checklist、推奨View、出力Templateを切り替える。

作業途中でObjectiveを追加・変更できる。切替時もCurrent Work Item、Evidence、Sources Checked / Not Checked、Missing Knowledge、選択中のFunction / System / Data / Code、Findings、Review Stateを保持する。Primary Objectiveは1つ、Secondary Objectivesは複数とし、切替による調査の作り直しを避ける。

Graphは二次導線「関係を探索」とし、1つのCanonical Relation ModelからWork Item、Domain、Function、System、Infrastructure / IaC、Data Flow、Code、Test、Evidence / History、Operation / Runbook、Stakeholder / Responsibilityを目的別にProjectionする。Functionは提供Capability、Systemは実現・稼働境界として区別する。詳細探索用の平面Graphと、Inquiry / Work ItemからEvidenceまでを上下に示す縦断Stackを併用し、View数は固定目標にしない。見積りは独立した基礎Graphではなく、影響対象、Evidence、不確実性、作業項目から導出するWorkspaceとする。

Data LibraryではUpload、既存Repository File登録、External Reference登録、Metadata / Relation更新、Version / Replace、Move / Rename、Work Item Link / Unlink、Archive / Restore、Reindex / Rebuild、影響Preview付きPermanent Delete候補を区別する。System-generated Artifactは生成元、Input、保存先、Status、Retentionを表示し、Human Review後にEvidenceへ昇格できる。PoCでは利用者向けClassification / Masking / 原本復元UIを提供しない。

# 98. UI and Developer Experience Decision Summary

## [DECIDED]

- Developer-First UIとする
- Chatだけに依存しない
- Current Work ItemとCurrent Objectiveを中心に表示する
- Original Inquiryへ戻れる
- Evidenceへ戻れる
- Sources Checked / Not Checkedを表示する
- Missing Knowledgeを独立して表示する
- CoverageをAI Memoryの代わりに利用する
- AI AssessmentとHuman Decisionを分離する
- GraphはWork Item Subgraphを基本とする
- GraphはCanonical Relation Modelの目的別Viewを同一領域で切り替え、View数を固定目標にしない
- View / Objective切替時にCurrent Work Itemと調査Contextを保持する
- Graphの既定FilterはCurrent only + Related to current Work Item + Depth 2とする
- 空Graphと未取得・Restricted・Filter除外を区別する
- Runtime Health / Stale状態を隠さない
- Persistent SaveをWorkflowとして見せる
- Customer DraftはHuman Review必須
- UIをSource of Truthにしない
- Storage / FrameworkへUIを強く依存させない
- PoCでUIを作り込みすぎない

## [PROVISIONAL]

- Main Screen Layout
- Coverage State
- Graph Visualization Library / Layout
- Timeline View
- Agent Execution View
- Context Inspector
- Review Diff
- CLI / UI併用

## [OPEN]

- UI Technology
- Graph Visualization Library
- Human Review UX
- Resume Navigation
- Git Diff UI
- External Evidence Task UI

---

# 99. UI and Developer Experience Statement

> 本ProjectのUI / Developer Experienceは、AI Chatを中心に据えるのではなく、最初に作業目的を選び、途中で目的を追加・変更できるWork Item Workspaceとして設計する。Evidence、Coverage、Missing Knowledge、Technical Cause、Current Specification、Historical Context、Operation、Stakeholder、Responsibility Assessment、Human Review、Persistent Saveを目的に応じて段階表示し、Graph、Timeline、Search、Codex Resume、Agent Execution、Runtime Healthは補助Viewとする。Data LibraryではOriginal、Derived、Runtime、System-generated Artifactの扱いと削除影響を明示し、利用者がAIの結論よりEvidenceと未確認範囲を先に確認できることを優先する。
