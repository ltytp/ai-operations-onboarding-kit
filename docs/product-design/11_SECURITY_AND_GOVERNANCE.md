# AI-Ready Operations Repository / Codex App
## 11. Security and Governance

**File Name:** `11_SECURITY_AND_GOVERNANCE.md`  
**Status:** Draft  
**Document Role:** Security / Access Control / Governance / Human Approval  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、本Projectで扱うSource、Knowledge、Case、Agent、Codex、External Evidenceについて、

> 何を、誰が、どの範囲まで参照・保存・Git管理・AI利用してよいか

を定義するためのSecurity / Governance方針を整理する。

特に以下を扱う。

- Codex Access
- Repository Access
- Git History
- Meeting Minutes
- Customer Information
- Personal Information
- Contract / Responsibility Information
- Production Data
- Credential / Secret
- Masking / Redaction
- External Knowledge Source
- Persistent Investigation Knowledge
- Agent Access Scope
- Human Approval
- Auditability
- Decision Gate

本ドキュメントは、組織Security Policyや顧客契約を置き換えるものではない。

---

# 2. Securityの基本原則

[DECIDED]

本Projectでは、

> AIが扱いやすいから

という理由で情報を無条件にRepositoryへ集約しない。

情報の利便性より、以下を優先する。

1. Organization Policy
2. Customer Contract
3. Access Control
4. Confidentiality
5. Auditability
6. Human Approval

AI-Ready化はSecurity条件の範囲内で行う。

---

# 3. SecurityはIngest後ではなくIngest前から考える

[DECIDED]

OriginalをMarkdownへ変換した後でSecurityを考えるのでは遅い。

AIへ情報を渡す前に、

- Classification
- Access Check
- Masking
- Redaction
- Credential Detection
- Policy Validation

を適用できることを基本とする。

---

# 4. OriginalとDerivedでSecurityを分離しない

[DECIDED]

OriginalがSensitiveなら、Derived SummaryもSensitiveである可能性がある。

例えばOriginal Meeting MinutesをRepositoryへ保存できない場合、

> Summaryなら無条件にGitへ保存してよい

とは考えない。

Derivedから、

- Customer Name
- Personal Name
- Contract Detail
- Responsibility Discussion
- Decision

が復元できる可能性を考慮する。

---

# 5. Security Classification

[PROVISIONAL]

Project上ではSource / KnowledgeにSecurity Classificationを持たせることを検討する。

候補：

- public
- internal
- confidential
- restricted
- ai_restricted
- ai_not_allowed

具体値はOrganization Policyに合わせる。

---

# 6. ClassificationはAccess Policyと分ける

[DECIDED]

Security Classificationと、

> 誰がアクセスできるか

は別概念とする。

例えば同じ`confidential`でも、

- Humanのみ
- Codex可
- Specific Agentのみ
- Repository可 / Git不可

等の違いがあり得る。

---

# 7. Access Policyの候補

[PROVISIONAL]

Source / Knowledgeごとに以下を表現できることを検討する。

- Human Read
- Codex Read
- Agent Read
- Repository Store
- Git Store
- Derived Summary Store
- Export
- Customer Output
- Retention

---

# 8. Git Historyを特別に扱う

[DECIDED]

Gitに一度Commitした情報は、通常のFile削除より長く履歴へ残る。

そのため、

> Repositoryへ置いてよい

と

> Git Historyへ永久的に近い形で残してよい

を同一判断にしない。

特にSensitive InformationはGit Commit前に確認する。

---

# 9. Git Permanence Risk

[DECIDED]

以下の情報をGitへCommitする場合、履歴に残るRiskを考慮する。

- Personal Information
- Customer Information
- Meeting Minutes
- Contract Information
- Responsibility Discussion
- Production Data
- Credential
- Internal Cost Information

後からFileを削除しただけでは履歴から消えない可能性がある。

---

# 10. Gitに入れてはいけない情報

[DECIDED]

少なくとも以下は原則Gitへ保存しない。

- Password
- API Key
- Access Token
- Private Key
- Secret
- Production Credential

発見した場合、AI-Ready化より先にSecurity Incident / Secret Rotation等の既存手順を優先する。

---

# 11. Meeting MinutesはDecision Gate対象

[DECIDED]

Meeting Minutesは本Projectで非常に価値の高いHistorical Evidenceである。

一方で、以下を含む可能性がある。

- Customer Name
- Personal Name
- Email Address
- Business Discussion
- Contract Detail
- Responsibility Discussion
- Internal Decision
- Sensitive Requirement

そのため、Meeting MinutesのCodex利用・Repository保存・Git管理は明示的なDecision Gateとする。

---

# 12. Meeting Minutesで確認すべき事項

[OPEN]

上司・Security・必要に応じてOrganization Policyで以下を確認する。

1. CodexからOriginal Meeting Minutesを直接参照してよいか
2. Repositoryへ保存してよいか
3. Git管理してよいか
4. Git Historyへ全文を残してよいか
5. Customer Nameを保存してよいか
6. Personal Nameを保存してよいか
7. Email Addressを保存してよいか
8. Contract / Responsibility Detailを保存してよいか
9. Masking / Redactionが必要か
10. Access Controlが必要か
11. Retention Policyがあるか
12. AI-Ready Summaryのみなら保存可能か

確認前にOriginal Minutesを無条件に取り込まない。

---

# 13. Meeting Minutesの扱いを段階化する

[PROVISIONAL]

Meeting Minutesは、Policyに応じて複数の取扱Levelを持てるようにする。

## Level A: Original Allowed

OriginalをCodex / Repositoryで参照可能。

## Level B: Repository Allowed, Git Not Allowed

RepositoryまたはLocal Storageでは利用可能だがGitへCommitしない。

## Level C: Approved Summary Only

Originalは外部管理し、許可済みSummary / MetadataだけRepositoryへ保存する。

## Level D: Reference Only

Source ID / Location / Date / Topicだけ保持する。

## Level E: AI Access Not Allowed

Humanのみ確認し、Caseには「Human Checked」の結果だけ残す。

---

# 14. External Meeting Evidence

[DECIDED]

Meeting MinutesをRepositoryへ入れられない場合でも、

> Historical Evidenceは存在する

ことをKnowledge Model上表現できるようにする。

候補：

- External Source ID
- Date
- Topic
- Related Function
- Checked By
- Access Policy
- Approved Summary
- Human Review Result

---

# 15. NotebookLMのSecurity上の位置付け

[DECIDED]

現時点ではNotebookLMにHistorical Evidenceが存在する。

本ProjectではNotebookLMのSecurity Policyを独自判断で変更しない。

Codexから直接接続できない場合、

- HumanがNotebookLMで確認
- 必要なEvidenceを整理
- 許可範囲内でCaseへ反映

する。

---

# 16. External SourceからのHuman Transfer

[DECIDED]

HumanがExternal SourceからCodexへ情報を持ち込む場合も、Security Ruleを適用する。

OriginalがAI利用禁止の場合、

> Humanが全文をCopy & Pasteすればよい

とは考えない。

許可されたSummary / Factだけを渡す。

---

# 17. Personal Information

[DECIDED]

Personに関する情報は必要最小限とする。

候補：

- Name
- Email
- Role
- Organization
- Meeting Participation

Personal InformationがKnowledgeとして本当に必要かを確認する。

---

# 18. PersonよりRoleを優先する

[PROVISIONAL]

調査上個人名が不要な場合、

- Customer System Owner
- Development Lead
- Maintenance Engineer

等のRoleで表現することを優先する。

個人名がDecision Evidenceとして必要な場合のみ保持する方式を検討する。

---

# 19. Customer Information

[DECIDED]

Customer固有情報について、

- Customer Name
- Environment Name
- Internal System Name
- Business Data

等をどこまでRepository / Codexへ渡せるか確認する。

Project内で既に許可されている情報と、新たにAIへ渡す情報を区別する。

---

# 20. Contract / Responsibility Information

[DECIDED]

Contract、責任分界、費用負担等の情報は高感度情報として扱う。

AIはAssessment Materialの整理に利用できる場合があるが、

- Access Control
- Human Review
- Output Control

を必須とする。

---

# 21. Responsibility DiscussionをCustomer Outputへ直接出さない

[DECIDED]

Internal Caseに、

- 開発側責任候補
- 顧客側責任候補
- 追加費用候補

等が含まれていても、そのままCustomer Responseへ出力しない。

Human Approved Positionへ変換してから利用する。

---

# 22. Production Data

[DECIDED]

Production Dataは、Source Code / Test Documentとは別のSecurity Categoryとして扱う。

調査に必要な場合でも、

- Data Masking
- Minimum Scope
- Access Approval
- Retention

を考慮する。

---

# 23. Production DataをPersistent Knowledgeへ残しすぎない

[DECIDED]

問い合わせ調査で実Production Dataを確認しても、

> Raw Data全体

をCaseへ保存することを基本としない。

必要なEvidenceだけ、

- Masked Sample
- Query Result Summary
- Record ID Reference
- Aggregated Fact

として残す方式を検討する。

---

# 24. SQL Result

[PROVISIONAL]

SQL ResultをEvidenceにする場合、

- Sensitive Column
- Personal Data
- Production Value

を確認する。

必要に応じてMaskingして保存する。

---

# 25. Credential Detection

[DECIDED]

Ingest / Repository Validationでは、Credential候補を検出することを検討する。

対象：

- Password
- API Key
- Token
- Private Key
- Connection String
- Secret

Credentialが見つかった場合、AI Knowledge化を止めることを優先する。

---

# 26. Secret Scan

[PROVISIONAL]

Git Secret Scanや既存Toolを利用して、

- Commit前
- Ingest前
- Generated Knowledge保存前

に検査することを検討する。

---

# 27. Masking

[PROVISIONAL]

Masking対象候補：

- Personal Name
- Email Address
- Phone Number
- Customer Identifier
- Production Record
- Secret-like Value

Masking RuleはConfig Drivenとする。

---

# 28. Redaction

[PROVISIONAL]

Maskingでは不十分な場合、Section単位で削除するRedactionを利用する。

例：

- Contract Amount
- Internal Responsibility Discussion
- Personal Evaluation

---

# 29. MaskingとOriginal Mapping

[DECIDED]

Masked Derived KnowledgeからOriginalへ戻れる必要がある場合でも、AIがOriginalへ無条件アクセスできるようにはしない。

ProvenanceとAccess Permissionを分離する。

---

# 30. Access Restricted Source

[DECIDED]

Sourceの存在は分かるがAIから参照できない状態を正式に表現する。

例：

- historical-meeting-2024-01
- access: human_only

AIは、

> Sourceが存在しない

と誤認しない。

---

# 31. Restricted Knowledgeの表示

[PROVISIONAL]

UI / Caseでは必要に応じて、

- Source Exists
- Restricted
- Human Check Required
- Checked by Human

等だけ表示する。

Sensitive Contentそのものは表示しない。

---

# 32. Agent Access Control

[DECIDED]

すべてのAgent / Skillへ同じAccess権を与えることを前提にしない。

Roleごとに必要最小限のAccessを持たせることを検討する。

---

# 33. Least Privilege

[DECIDED]

Agentは、

> Task達成に必要な最小限のSource

へアクセスする。

例：

Stakeholder Communication AgentにRaw Production Dataは不要。

Review AgentにCredentialは不要。

---

# 34. Agent Access Scope候補

[PROVISIONAL]

例：

## Code Investigation

- Source Code
- Technical Documents
- Test

## Evidence Investigation

- Design
- Test
- Past Inquiry
- Approved Historical Evidence

## Stakeholder Communication

- Human Reviewed Case Summary
- Approved Position

## Review

- Case Evidence
- Security Classification
- Output Draft

---

# 35. Main Agentも無制限Accessにしない

[PROVISIONAL]

Main Orchestratorであっても、Policy上禁止されたSourceへアクセスしない。

Access Decisionを「Main Agentだから例外」としない。

---

# 36. Human Approval

[DECIDED]

以下はHuman Approvalを必須とする。

- Responsibility Decision
- Contract Interpretation
- Cost / Additional Development Position
- Customerへの正式Response
- Restricted SourceからPersistent Knowledgeへの昇格
- Sensitive Meeting SummaryのRepository保存
- Security Exception

---

# 37. Human Approval Record

[PROVISIONAL]

重要Approvalについて以下を残すことを検討する。

- Approved By
- Approved At
- Scope
- Decision
- Reason
- Related Case
- Related Source

---

# 38. Security Exception

[PROVISIONAL]

Policy上通常禁止される操作に例外を認める場合、

- Reason
- Approver
- Expiration
- Scope

を記録する。

無記録の例外を作らない。

---

# 39. Repository Policy

[PROVISIONAL]

Repository上にAI / Security PolicyをConfigとして定義する可能性がある。

候補：

- Allowed Document Types
- Restricted Paths
- Git Prohibited Data
- AI Prohibited Data
- Masking Rule
- External Source Rule
- Generated Output Rule

---

# 40. PolicyはCodeへHard Codingしない

[DECIDED]

Customer / ProjectごとのPolicyをApplication Codeへ散在させない。

Config / Policy Fileとして管理する。

---

# 41. Policy Validation

[PROVISIONAL]

Codex / ToolがRepository変更前にPolicyをValidationできることを検討する。

例：

- Sensitive FileをGitへ追加しようとしていないか
- Generated SummaryにPIIが残っていないか
- Restricted DirectoryをIndex対象にしていないか

---

# 42. Security BlockingとWarning

[DECIDED]

Security PolicyはSeverityを分ける。

## Blocking

- Credential
- AI Not Allowed Data
- Explicit Git Prohibited Data

## Warning / Review

- Unknown Classification
- Potential PII
- Sensitive Responsibility Content

すべてを同じWarningにしない。

---

# 43. Unknown Classification

[DECIDED]

Classification不明のDocumentを無条件にAIへ渡さない。

`needs_classification`

として扱うことを検討する。

---

# 44. AI OutputのSecurity

[DECIDED]

AIが生成したOutputにもSecurity Reviewが必要である。

AIはSourceのSensitive情報をSummaryへ再出力する可能性がある。

そのため、

- Generated Summary
- Case Report
- Customer Draft
- Graph Label

もSecurity対象とする。

---

# 45. Graph Security

[DECIDED]

Graph Relation自体からSensitive情報が推測できる可能性がある。

例：

Stakeholder  
APPROVED_BY  
Person

ResponsibilityScope  
APPLIES_TO  
Customer Function

Node / EdgeにもAccess Policyを持たせることを検討する。

---

# 46. Graph Visualization

[PROVISIONAL]

Restricted Nodeは、

- Hidden
- Masked
- Placeholder

等で表示する方式を検討する。

Graph全体をExportする場合もAccess Controlを適用する。

---

# 47. Vector Index Security

[DECIDED]

Sensitive DocumentをVector Indexへ登録した場合、Originalを削除してもEmbedding / Chunkが残る可能性を考慮する。

Vector IndexもDerived Sensitive Dataとして扱う。

---

# 48. Search Index Security

[DECIDED]

Full Text / Semantic Indexで、

> 検索結果からAccess禁止情報が見える

状態を避ける。

Index Retrieval時にもAccess Filterを適用できることが望ましい。

---

# 49. Runtime DB Security

[PROVISIONAL]

SQLite / Graph DB等を利用する場合、

- Local File Permission
- Encryption Requirement
- Backup
- Retention
- Deletion

を検討する。

詳細は`12_RUNTIME_AND_STORAGE.md`で扱う。

---

# 50. Codex Session Security

[DECIDED]

Codex Session / ResumeにもSensitive情報が含まれる可能性がある。

Sessionへ、

- Credential
- Prohibited Data
- Unapproved Meeting Original

を入力しない。

---

# 51. Resumeをそのまま共有しない

[PROVISIONAL]

Codex ResumeにはWorking HistoryやSensitive Contextが含まれる可能性がある。

引き継ぎ時に共有する場合、Access Scopeを確認する。

---

# 52. Persistent Investigation Knowledge

[DECIDED]

Case終了時にSession外へ保存するPersistent Investigation KnowledgeにもSecurity Policyを適用する。

特に、

- Original Inquiry
- Production Data
- Responsibility Assessment
- Customer Response
- Meeting Evidence

の保存範囲を確認する。

---

# 53. Internal InvestigationとExternal Responseを分離する

[DECIDED]

Internal Investigation Recordには、

- Technical Detail
- Responsibility Discussion
- Missing Evidence
- Internal Assessment

が含まれる可能性がある。

Customer Responseとは別Artifactとして扱う。

---

# 54. Customer ResponseのRelease Gate

[DECIDED]

Customer向けResponseはHuman Approval後にReleaseする。

AI Draftをそのまま正式回答として扱わない。

---

# 55. Persistent KnowledgeのGit管理

[OPEN]

Persistent Investigation KnowledgeをGit管理する範囲は未確定。

確認観点：

- Customer Information
- Inquiry Text
- Responsibility Assessment
- Production Evidence
- Review History

必要に応じてMetadataのみGit管理する方式も検討する。

---

# 56. Derived KnowledgeのGit管理

[OPEN]

AI-Ready Derived KnowledgeをGitへCommitするかはSource Classificationごとに判断する。

OriginalがGit禁止の場合、DerivedもGit禁止となる可能性がある。

---

# 57. Local Only Knowledge

[PROVISIONAL]

Policy上Gitへ保存できないがAI利用可能な情報について、

- Local Runtime
- Approved Secure Storage

のみへ保存する方式を許容する。

---

# 58. Storage LocationをKnowledge Stateと分離する

[DECIDED]

Knowledgeが、

- Human Reviewed
- AI Extracted

であることと、

- Git
- Local
- External

のどこへ保存されるかは別概念とする。

---

# 59. Retention

[OPEN]

以下の保持期間を確認する必要がある。

- Codex Session
- Runtime Log
- Derived Knowledge
- Production Data Evidence
- Meeting Summary
- Case Record

Organization Policyに合わせる。

---

# 60. Deletion

[PROVISIONAL]

削除要求が発生した場合、

- Repository File
- Git History
- Runtime DB
- Search Index
- Vector Index
- Cache
- Generated View

のすべてを考慮する。

File削除だけで完了としない。

---

# 61. RebuildとSecurity

[DECIDED]

Runtime Dataを再生成する場合も、現在のSecurity Policyを再適用する。

古いPolicyで生成されたSensitive Indexを無条件に復元しない。

---

# 62. Auditability

[DECIDED]

重要なSecurity / Governance判断を後から確認できることを目指す。

候補：

- Who accessed
- What was generated
- What was approved
- What was blocked
- What was masked
- Which policy version was used

ただしAudit範囲はOrganization Policyに従う。

---

# 63. Access Log

[PROVISIONAL]

Sensitive SourceについてAccess Logが必要かを検討する。

PoCでは最小限でも、

- Source
- Case
- Access Type
- Result

を記録できると望ましい。

---

# 64. Transformation Log

[DECIDED]

Document Ingestで、

- Masked
- Blocked
- Restricted
- Classified

等のSecurity結果をTransformation Logへ残す。

---

# 65. Agent Execution Log

[PROVISIONAL]

AgentがRestricted Sourceを要求した場合、

- Request
- Policy Decision
- Access Result

をExecution Recordへ残すことを検討する。

---

# 66. Policy Version

[PROVISIONAL]

Security Policy / Masking RuleへVersionを持たせる。

CaseやDerived Knowledgeから、

> どのPolicyで処理されたか

を追えることが望ましい。

---

# 67. Security Review Queue

[FUTURE]

以下をHuman Review Queueへ送ることを検討する。

- Unknown Classification
- Potential PII
- Meeting Summary
- Responsibility Knowledge
- Git Commit Candidate
- Security Exception

---

# 68. Security Scan Scope

[PROVISIONAL]

最低候補：

- New Files
- Modified Files
- Generated Knowledge
- Case Records
- Customer Draft
- Git Staged Changes

---

# 69. Pre-Commit Guard

[FUTURE]

必要であればPre-Commit等で、

- Secret
- Prohibited File
- Restricted Classification

を検出する。

PoC初期では必須としない。

---

# 70. AI Access Decision

[DECIDED]

AIがSourceを参照できるかは、

> Repositoryにあるか

では決めない。

Source ClassificationとAccess Policyで決める。

RepositoryにあるがAI参照禁止、という状態を許容する。

---

# 71. Repository Storage Decision

[DECIDED]

Repositoryへ保存できるかとCodexが参照できるかも別判断とする。

例：

- Human repository: allowed
- Codex read: prohibited

を表現可能にする。

---

# 72. Git Storage Decision

[DECIDED]

Repository Working Treeに置けるがGit Commit禁止、という状態も許容する。

`.gitignore`等で管理する可能性がある。

---

# 73. Derived Summary Decision

[PROVISIONAL]

Original禁止でもApproved SummaryならAI利用可能なケースを考慮する。

その場合、

- Summary作成者
- Approval
- Source
- Masking Rule

を追跡する。

---

# 74. Responsibility Evidence Decision

[DECIDED]

Responsibility Assessmentに利用するEvidenceは、

- Technical Evidence
- Current Specification
- Historical Agreement

を区別する。

Contract上の最終解釈をAI Knowledgeだけで確定しない。

---

# 75. Governance Role

[PROVISIONAL]

Project内のGovernance Role候補：

- Project Owner
- Maintenance Lead
- Security Approver
- Customer Communication Approver
- Knowledge Reviewer

実際の担当者はProjectごとにConfig化する。

---

# 76. Separation of Duties

[PROVISIONAL]

重要な責任・費用判断では、

> AIが調査し、AIが承認し、AIが顧客へ送る

構成を避ける。

少なくともHuman Approvalを分離する。

---

# 77. Responsibility Final Decision

[DECIDED]

AIは以下を作成できる。

- Facts
- Evidence
- Historical Agreement
- Difference
- Assessment Candidate

最終DecisionはHumanが行う。

---

# 78. Cost Decision

[DECIDED]

追加開発費用や無償対応等の判断をAIだけで確定しない。

Human / Organization ProcessへEscalateする。

---

# 79. Customer Commitment

[DECIDED]

納期・責任・費用・補償等のCustomer CommitmentをAIが自動的に確約しない。

---

# 80. Unknown Policy

[DECIDED]

Policyが分からない場合、

> おそらく大丈夫

で進めない。

`policy_unknown`

としてHuman確認を要求する。

---

# 81. Security Decision Gate 1: Meeting Minutes

[DECIDED]

Meeting Minutes利用前に管理者確認。

---

# 82. Security Decision Gate 2: Git

[DECIDED]

Sensitive KnowledgeをGitへ保存する前にPolicy確認。

---

# 83. Security Decision Gate 3: Production Data

[DECIDED]

Production DataをCodexへ渡す前にAccess / Masking条件確認。

---

# 84. Security Decision Gate 4: Responsibility Output

[DECIDED]

Responsibility / CostをCustomerへ説明する前にHuman Approval。

---

# 85. Security Decision Gate 5: External Knowledge Integration

[DECIDED]

NotebookLM等のExternal Sourceを自動Ingestする前に、

- Access
- Storage
- AI Use
- Retention

を確認する。

---

# 86. PoC Security Minimum

[DECIDED]

PoCでは最低限以下を守る。

1. AI利用承認済みSource SetだけをIngestする
2. 未承認Meeting Minutes、Credential、未承認Production DataをIngestしない
3. Existing Access Controlを迂回しない
4. Responsibility DecisionをHuman Reviewする
5. Customer ResponseをHuman Reviewする
6. Derived KnowledgeからOriginal Sourceへ戻れるようにする
7. Excluded / Access RestrictedをMissingと区別する
8. 利用者へFile分類・Masking・原本復元の運用を求めない

---

# 87. PoCで実装しなくてよいもの

PoC初期では以下を必須としない。

- Enterprise IAM
- Fine-Grained RBAC Server
- Full DLP Platform
- Central SIEM Integration
- Automated Legal Decision
- Complete Data Retention Engine
- Masking / Token Vault / Detokenization
- Field Level Confidential Data ACL
- In-app Original Reconstruction

ただし将来拡張を阻害しない。

---

# 88. PoC Security Acceptance

PoCでは以下を確認する。

## Restricted Source

参照不可Sourceを正しく`restricted`として扱える。

## Provenance

Derived KnowledgeのSourceが分かる。

## Git Safety

Git禁止情報を無条件にCommitしない。

## Human Approval

Responsibility / Customer OutputがHuman Reviewを通る。

## Persistent Knowledge

Session外保存時にもSecurity Policyを適用する。

---

# 89. Security Anti-Patterns

## Markdown = Safe

Markdown化したからSecurity上安全と考える。

## Repository = AI Allowed

RepositoryにあるからAI参照可能と考える。

## Delete File = Delete Data

Git / Index / Cacheを無視する。

## Summary = Non-Sensitive

Summaryなら無条件に公開可能と考える。

## Human Copy-Paste Bypass

AI利用禁止Sourceを人間がCopyすればよいと考える。

## AI Approval

責任・費用をAI自身が承認する。

## Main Agent Superuser

Main Agentだけは全Source参照可能とする。

---

# 90. Current Open Questions

[OPEN]

## Meeting Minutes

Codex Direct Access可否。

## Repository Storage

Meeting / Responsibility情報の保存可否。

## Git Storage

全文・SummaryのGit管理可否。

## PII

Name / Email等の保存・AI利用条件。

## Production Data

Codexへの投入条件。

## Security Classification

正式値。

## Access Policy

Role / Agentごとの権限。

## Retention

Session / Derived / Caseの保持期間。

## Audit

必要なAccess Log範囲。

## Encryption

Runtime DB等に必要か。

---

# 91. Management / Securityへ確認する質問

[DECIDED]

最低限以下を確認する。

1. Meeting MinutesをCodexへ直接読ませてよいか
2. Meeting MinutesをRepositoryへ置いてよいか
3. Git Commitしてよいか
4. Git Historyへ全文を残してよいか
5. Customer Name / Person Name / Emailを保存してよいか
6. Responsibility / Contract Detailを保存してよいか
7. Maskingが必要か
8. Production DataをCodexへ渡せる条件は何か
9. AI-Ready Summaryだけなら保存可能か
10. Access Control要件は何か
11. Retention / Deletion Ruleは何か
12. Customer向けAI Draftに必要なReview Ruleは何か

---

# 92. Decision記録

[PROVISIONAL]

上記回答を一回限りの会話で終わらせず、Project Policyとして記録する。

候補：

- policy.yaml
- security-policy.md
- ADR
- Approved Decision Record

具体形式は対象Repository確認後に決定する。

---

# 93. Policyが変わった場合

[DECIDED]

Security Policy変更時は、

- Existing Derived Knowledge
- Runtime Index
- Graph
- Case Record

への影響を確認する。

必要に応じて再生成・Masking・削除を行う。

---

# 94. SecurityとRebuildability

[DECIDED]

Rebuild可能であることと、

> いつでも全Sourceから自動再生成する

ことは同じではない。

再生成時もAccess / Policy Checkを実施する。

---

# 95. SecurityとPortability

[DECIDED]

別PC / Account / EnvironmentへProjectを移す際、Sensitive Local Dataを自動的に持ち運ばない。

Handoff DocumentsにはSensitive Originalを埋め込まない。

---

# 96. Handoff Package

[DECIDED]

Handoff DocumentsはArchitecture / Decisionを伝えるためのものとし、

- Customer Confidential Data
- Personal Data
- Meeting Original
- Credential

を直接含めない。

---

# 97. AGENTS.mdへのSecurity記載

[PROVISIONAL]

AGENTS.md等の入口には最低限、

- Restricted Sourceを無断で読まない
- Meeting Minutes Decision Gate
- Credential禁止
- Responsibility Human Approval
- Persistent Knowledge保存時のReview

を記載する。

詳細は本Documentを参照させる。

---

# 98. 後続ドキュメントへの引き継ぎ

## `12_RUNTIME_AND_STORAGE.md`

- Git / Local / Runtime Storage
- Encryption
- Retention
- Deletion
- Index Security
- Session Storage

## `13_UI_AND_DEVELOPER_EXPERIENCE.md`

- Restricted Source表示
- Human Review
- Security Warning
- Approval State

## `14_SEMANTICA_EVALUATION.md`

- SemanticaへのSensitive Data投入範囲
- Provenance / Policy機能
- External Infrastructure Risk

## `15_POC_PLAN_AND_ACCEPTANCE_CRITERIA.md`

- Security Decision Gate
- Management Confirmation
- PoC Allowed Data Scope

---

# 98.1 PoC Security Scope Override（2026-08-30）

[DECIDED]

PoCの対象Dataは、Organization / Administratorが事前にAI利用を承認した範囲に限定する。既存Source側のAccess Controlを正とし、未承認Sourceは禁止SourceとしてIngestしない。

PoCでは、利用者によるFile単位のSecurity分類UI、Masking / Redaction Pipeline、Token Vault / Detokenization、Mask済み中間生成物とSchemaを照合して原本を画面復元する仕組み、Field Levelの機密情報ACLを実装しない。

これらはProduction化のSecurity Assessmentで再検討する[FUTURE]事項である。本章のClassification / Masking詳細はProduction候補設計として保持するが、PoC Acceptanceの必須機能とはしない。PoCで必要なのはApproved Source Set、Excluded Source List、既存権限の遵守、重要なUpload / Execute / Approve / Export / Delete / ReprocessをWork ItemとExecutionへ紐づけた監査記録である。

# 99. Security and Governance Decision Summary

## [DECIDED]

- SecurityをAI利用前に適用する
- OriginalとDerivedの両方をSecurity対象とする
- Repository保存・Git保存・AI参照を別判断とする
- Git Historyの永続性を考慮する
- Meeting MinutesをDecision Gate対象とする
- Meeting Minutesを段階的Access Modelで扱えるようにする
- Access RestrictedをMissingと区別する
- CredentialをAI-Ready化しない
- Production Dataを最小限に扱う
- AgentはLeast Privilege
- Responsibility / Contract / CostはHuman Approval必須
- Customer ResponseはHuman Approval必須
- Security Unknown時は停止して確認する
- External SourceをHuman Copy-PasteでPolicy回避しない

## [PROVISIONAL]

- Security Classification
- Agent Access Scope
- Masking Rule
- Restricted Graph表示
- Local Only Knowledge
- Audit Log
- Policy Config

## [OPEN]

- Meeting Minutes利用可否
- Git保存範囲
- Personal Information条件
- Production Data条件
- Retention
- Encryption
- Formal Access Control
- Audit Requirement

---

# 100. Security and Governance Statement

> 本Projectでは、AI-Ready化の利便性よりOrganization Policy、Customer Contract、Confidentiality、Human Approvalを優先する。PoCはAI利用承認済みSourceだけを対象とし、未承認SourceをIngestしない。利用者にFile単位の分類やMaskingを運用させず、Masking、Token Vault、Detokenization、原本復元UIはProduction評価へ保留する。SourceのRepository保存、Git保存、Codex参照は別Decisionとして扱い、既存Access Controlを尊重する。AIは調査・Evidence整理・Assessment Material作成を支援するが、責任・契約・費用・Customer Commitmentの最終判断はHuman Approvalを必須とする。

## 100.1 Infrastructure / IaC Security Refinement（2026-08-30）

[DECIDED]

Infrastructure / IaC Graphは承認済みTerraform Sourceだけを対象とする。Terraform State、Plan、Variable、OutputにはCredential、Secret、Endpoint、Account情報等が含まれ得るため、GraphへはResource Address、Type、Module Path、Dependency、Source Reference、Drift State等の必要最小Metadataのみを格納し、Sensitive Valueを複製しない。Function、System、Infrastructureを分離してもAccess Controlを弱めず、Vertical StackでRestricted Nodeを内容表示せず`Restricted`状態として示す。Stack表示は新しい権限境界ではなく、既存のSource Access Decisionを継承する。
