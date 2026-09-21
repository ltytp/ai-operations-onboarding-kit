# AI-Ready Operations Repository / Codex App
## 04. Design Principles

**File Name:** `04_DESIGN_PRINCIPLES.md`  
**Status:** Draft  
**Document Role:** Design Principles / Architecture Guardrails  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、以下で整理した背景・Vision・要件を実装へ落とす際に、設計判断の基準となる原則を定義する。

- `AI-Ready Operations Repository - Codex App_01_BACKGROUND_AND_PROBLEM.md`
- `AI-Ready Operations Repository - Codex App_02_VISION_AND_GOALS.md`
- `AI-Ready Operations Repository - Codex App_03_REQUIREMENTS.md`

本ドキュメントの目的は、特定の技術製品やDirectory構成を確定することではない。

後続でRepository構成、Knowledge Model、Graph、Document変換、Agent、Runtime Storage、UI等を設計する際に、

> 何を優先し、何を避けるべきか

を一貫させるためのArchitecture Guardrailとして利用する。

---

# 2. Principle 1: Existing Repository First

[DECIDED]

本PoCは、AI向けに理想化した新Repositoryを先に作るのではなく、既存の運用保守Repositoryを理解することから開始する。

対象Repositoryにはすでに、問い合わせ調査、テスト項目書、Source Code、運用保守資料等の既存資産と運用方法が存在する。

そのため設計順序は以下とする。

1. 現在のRepository構造を確認する
2. Directoryごとの意味と人間の運用を理解する
3. 維持すべき既存構造を特定する
4. AI-Ready化に不足する能力のみ追加する

AIにとって扱いやすいという理由だけで、既存Repositoryを全面再編しない。

---

# 3. Principle 2: Human Workflowを壊さない

[DECIDED]

AI-Ready化のために、人間の通常業務へ大きな追加作業を要求しない。

特に以下を避ける。

- 同じ内容をOriginal DocumentとAI用Documentへ二重入力する
- AIのためだけに既存の問い合わせ管理方法を全面変更する
- AIのためだけにOffice Documentを手作業でMarkdownへ変換する
- AIのためだけに大量のMetadataを人間が毎回入力する

理想的には、人間が通常どおり資料やコードを更新すると、その変更からAI向け情報が派生する構造とする。

PoCでは完全自動化を必須としないが、将来の自動化を阻害する構造にはしない。

---

# 4. Principle 3: GitをHistorical Source of Truthとして扱う

[DECIDED]

Gitは、Source Codeだけではなく、Repository内で管理可能なKnowledgeの変更履歴を追跡する重要な基盤として扱う。

Gitから確認したい情報には、以下が含まれる。

- いつ変更されたか
- 何が変更されたか
- どの資料とコードが同時に変更されたか
- どのReleaseに関連する変更か
- 過去状態から現在状態へどのように変化したか

ただし、すべてのOriginal DocumentをGit管理できるとは限らない。

議事録等のセンシティブな情報については、組織・Security上の確認結果に従う。

---

# 5. Principle 4: OriginalとDerived Knowledgeを分離する

[DECIDED]

人間が作成・利用するOriginal Documentと、AIが探索しやすいように生成するAI-Ready Knowledgeは別物として扱う。

Originalは、人間の業務上の正式資料・Evidenceである。

Derived Knowledgeは、検索、Relation探索、要約、Graph生成、Index生成等を目的とした派生情報である。

AI-Ready化のためにOriginalを置き換えることを目的としない。

---

# 6. Principle 5: Derived Dataは再生成可能にする

[DECIDED]

AI向けに生成する以下の情報は、可能な限り再生成可能にする。

- Markdown
- Metadata
- Relation
- Graph
- Search Index
- Vector Index
- HTML View
- Coverage View
- Runtime Knowledge Database

重要情報を、再生成不能なRuntime Databaseにのみ保持しない。

理想的には、Original、Config、Transformer、Git Historyから再構築可能とする。

---

# 7. Principle 6: Provenanceを失わない

[DECIDED]

AI-Ready Knowledgeは、必ず可能な範囲でOriginal Sourceへ戻れるようにする。

AIが生成したSummaryやRelationだけを残し、どの資料から生成されたか分からなくなる状態を避ける。

Provenanceとして後続設計で検討する情報には、以下がある。

- Source File
- Repository Path
- Git Commit
- Document Version
- Sheet
- Row / Range
- Page / Slide
- External Source
- Transformer Version
- Extraction Date
- Review Status

問い合わせ対応では、AIの結論よりもEvidenceへの追跡可能性を重視する。

---

# 8. Principle 7: RetrievalをLLM Memoryより重視する

[DECIDED]

本プロジェクトでは、LLMがRepository全体を常に記憶している状態を目標にしない。

目標は、

> 問い合わせに応じて、必要なKnowledgeへ正しく到達できること

である。

そのため、以下を重視する。

- Retrieval
- Relation
- Index
- Graph
- Provenance
- Coverage
- Context Selection

長いSessionやAgent Memoryだけに依存しない。

---

# 9. Principle 8: Work Itemを作業Contextの中心単位とする

[DECIDED]

AI-Ready Repository全体を一度に理解させるのではなく、現在のWork Itemを中心に必要なKnowledgeを集める。

Work Item Type候補には以下がある。

- Inquiry
- Incident
- Bug
- Change Request
- Release
- Investigation
- Operation Task
- System Discovery
- Impact Analysis
- Estimation
- Knowledge Maintenance

PoCでは問い合わせをPrimary Objectiveとして扱う。`Case`はInquiry / Incident subtypeまたは既存互換用語として残す。

Work ItemはPrimary ObjectiveとSecondary Objectivesを持ち、目的変更時もShared Context、Evidence、Coverage、Findingsを失わない。

ただし、既存Repositoryにすでに問い合わせ単位のフォルダ構造があるため、新しい`cases/` Directoryを必須とはしない。

既存管理方法を確認した上で、Case ConceptをどのようにMappingするか決定する。

---

# 10. Principle 9: 業務プロセスと調査対象を混同しない

[DECIDED]

問い合わせ対応の業務プロセスと、その工程で確認する技術対象・Evidenceを別概念として扱う。

問い合わせ対応の大きな業務プロセスは、以下である。

1. 問い合わせを受ける
2. 発生事象・期待動作を理解する
3. 原因を調査する
4. 現行仕様・過去合意と照合する
5. バグ / 仕様 / 責任範囲の判断材料を整理する
6. 人間がReviewする
7. 利用者・顧客へ説明する

一方、API、Batch、Database、Source Code等は原因調査の対象である。

議事録、Design、Test、過去問い合わせ等は、原因や仕様・合意内容を評価するEvidenceである。

これらを単一の直列フローとして設計しない。

---

# 11. Principle 10: Technical CauseとAssessmentを分離する

[DECIDED]

技術的原因が判明したことと、その事象がバグであることを同一視しない。

少なくとも以下を分けて扱う。

- Observed Fact
- Technical Cause
- Current Specification
- Historical Evidence
- Historical Agreement
- Difference / Deviation
- Responsibility Assessment Material
- Human Decision

例えば、「対象レコードが生成されていない」はTechnical Causeになり得るが、それだけでは実装バグか現行仕様かは判断できない。

---

# 12. Principle 11: AI推論と確認済み事実を区別する

[DECIDED]

AIが抽出・推論した情報と、人間またはOriginal Evidenceで確認済みの情報を混同しない。

Knowledge Stateとして、後続設計では以下のような区別を検討する。

- Human Verified
- Human Reviewed
- AI Extracted
- AI Inferred
- Needs Review
- Conflicting
- Deprecated
- Unknown

責任範囲や仕様判断にAI推論を使用する場合、その状態が人間から見えること。

---

# 13. Principle 12: Missing Knowledgeを一級情報として扱う

[DECIDED]

AIが確認できなかった情報を失敗として隠さない。

以下を明示できる構造とする。

- Sources Checked
- Sources Not Checked
- Missing Knowledge
- Open Questions
- Conflicts
- Access Restricted Sources

問い合わせに必要な議事録がCodexから参照できない場合は、「未確認」であること自体が重要な調査結果となる。

不明情報をもっともらしい推論で埋めない。

---

# 14. Principle 13: CoverageをAI Memoryの代わりに可視化する

[DECIDED]

人間が確認したいのは「AIが何を覚えているか」ではなく、

> 今回のCaseについて、どのKnowledge領域を実際に確認したか

である。

将来的には、例えば以下のCoverageを表示できることが望ましい。

- Business
- Function
- System
- Implementation
- Test
- Historical Evidence
- Stakeholder / Responsibility

Coverageは、回答の信頼性と未確認領域を人間が判断するために利用する。

---

# 15. Principle 14: GraphはRelation Modelとして使う

[DECIDED]

Graph導入の目的は、巨大なGraphを可視化することではない。

目的は、

> 問い合わせから必要なKnowledgeへ関係を辿って到達できること

である。

GraphはStorage製品ではなく、まずRelation Modelとして設計する。

そのため、Graph Database採用前に以下を明確にする。

- 何をNodeとするか
- 何をEdgeとするか
- Relationが何を意味するか
- RelationのEvidenceは何か
- RelationのVersionをどう扱うか

---

# 16. Principle 15: 1つのRelation Modelを層別ViewへProjectionする

[DECIDED]

Graph Viewごとに別のKnowledge Storeを作らず、1つのCanonical Relation Modelから以下を概念的に区別してProjectionする。

- Case
- Domain / Business
- Function
- System / Architecture
- Data Flow
- Code
- Test
- Evidence / History

各ViewをStable IDとBridge Relationで接続し、BusinessからImplementation、Test、Historical Evidenceへ縦に辿れるようにする。

PoCでは必要な範囲のみ実装し、全Graph生成を必須としない。

---

# 17. Principle 16: Data Flowを重要視する

[PROVISIONAL]

運用保守ではCall GraphだけでなくData Flowが原因調査に重要となる場合が多い。

例えば「データが画面に表示されない」という問い合わせでは、

- 入力File
- Batch
- Database
- 集計処理
- API
- Screen

というデータの流れが原因調査経路になる。

したがってCode Graphを導入する場合でも、Code Structureだけに偏らずData Flowを考慮する。

---

# 18. Principle 17: TimeはKnowledge Layerではなく横断Dimensionとする

[DECIDED]

本システムでは複数種類の時間が存在する。

例：

- Business Date
- Input File Date
- Data Creation Time
- Batch Execution Time
- Release Date
- Requirement Decision Date
- Meeting Date
- Inquiry Date
- Investigation Date

これらを単一のTimelineへ無理に統合せず、各Knowledgeに関連する時間属性として扱う。

必要に応じてCase単位で複数時間軸を重ねて表示する。

---

# 19. Principle 18: Repository内外のKnowledgeを区別する

[DECIDED]

現時点では、Repository外にNotebookLMで管理されている過去議事録・仕様情報が存在する。

したがってKnowledge Modelは、SourceがRepository内にあることを前提としない。

最低限、以下を区別可能にする。

- Repository Source
- External Source
- External Source / Checked
- External Source / Not Checked
- Access Restricted Source

将来的に議事録をRepositoryへ一元化できても、Domain Modelを大きく変更しなくて済む構造を目指す。

---

# 20. Principle 19: SecurityはIngestion時点から考える

[DECIDED]

Office DocumentをMarkdownへ変換しただけではSecurity対策にならない。

AIへ情報を渡す前に、必要に応じて以下を適用できる設計とする。

- Classification
- Masking
- Redaction
- Access Policy
- Customer Data Handling
- Personal Information Handling
- Credential Detection
- Contract / Responsibility Information Handling

特に議事録等については、Codex直接参照可否・Git管理可否を上司等へ確認するまで無条件にRepositoryへ追加しない。

PoCでは利用者へ資料ごとのSecurity分類やMasking判断を要求しない。対象Dataを事前にAI利用承認済み範囲へ限定し、許可されていないSourceはIngestしない。Masking、Token Vault、Detokenization、原本復元UIはProduction検討事項とする。

---

# 21. Principle 20: Original AccessとAI-Ready Accessを分離できるようにする

[PROVISIONAL]

Security上必要であれば、

- AIはAI-Ready Summaryのみ参照可能
- 人間はOriginalを参照可能

といった権限分離を可能にする。

OriginalをAIへ直接渡せない場合でも、Metadataや許可済みSummaryをKnowledgeとして利用できる構造を検討する。

---

# 22. Principle 21: Document FormatとDocument Meaningを分離する

[DECIDED]

Excel、Word、PowerPoint、PDF等は物理Formatであり、Knowledge上の意味ではない。

同じExcelでも、

- Requirement
- Test Specification
- Inquiry
- Release Management
- Operation Manual

など意味が異なる。

そのためDocument処理では、

> Physical Format

と

> Business Document Type

を分離して扱う。

---

# 23. Principle 22: Officeから直接Markdownへ落とすだけにしない

[PROVISIONAL]

Document変換では、Office / PDF等からMarkdownへ直接変換するだけの実装に固定しない。

将来的には、

1. OriginalをParseする
2. 共通のNormalized Intermediate Representationへ変換する
3. Security / Maskingを適用する
4. Domain Knowledgeへ変換する
5. Metadata / Relation / Indexを生成する

というPipelineを検討する。

これにより、Excel / PowerPoint / Word等のParser差異をDomain処理から分離する。

---

# 24. Principle 23: Stable IDをPathだけに依存させない

[PROVISIONAL]

File MoveやRenameによってKnowledge Identityが失われないよう、PathだけをIdentifierとして扱わないことを検討する。

特に以下を関連付ける場合に重要である。

- Original Document
- AI-Ready Knowledge
- Graph Node
- Case
- Evidence
- Historical Version

具体的なStable ID方式は後続設計で決定する。

---

# 25. Principle 24: Change DetectionはIncrementalを基本とする

[PROVISIONAL]

Repository起動時に全Fileを毎回再解析する方式より、Git Diff等を利用したIncremental Updateを優先する。

基本思想は以下である。

1. 最後に処理したRevisionを確認する
2. Added / Modified / Deletedを取得する
3. 影響するKnowledgeのみ再生成する
4. 関連Index / Graphを更新する

PoCでは完全実装を必須としない。

---

# 26. Principle 25: Generated ViewをSource of Truthにしない

[DECIDED]

HTML、Graph View、Coverage Report、Dashboard等は人間が理解しやすくするためのGenerated Viewとして扱う。

Generated Viewを直接編集して正式情報を更新する設計にはしない。

---

# 27. Principle 26: AgentはDirectoryではなく責務で分ける

[DECIDED]

将来的にAgentを分割する場合、Repository Directory単位でAgentを定義しない。

Directory構成は変更され得るため、Agentは以下のような責務で分ける。

- Business Analysis
- System Analysis
- Code Investigation
- Evidence Investigation
- Timeline Analysis
- Responsibility Assessment Support
- Stakeholder Communication
- Review

具体的Agent数やMulti-Agent採用はPoCでは未決定。

---

# 28. Principle 27: AgentとSkillを分離する

[PROVISIONAL]

Agentは「誰が責任を持つか」、Skillは「何ができるか」として分離する。

例えばEvidence Agentが、

- Find Evidence
- Trace Decision
- Build Timeline

等のSkillを利用する構造を検討する。

これによりAgent編成を変更してもSkillを再利用できる。

---

# 29. Principle 28: Main AgentはすべてのFileを直接読む役割にしない

[PROVISIONAL]

将来的なOrchestratorは、Repository全体を毎回読み込むのではなく、

- Caseを理解する
- 必要な調査領域を決める
- 適切なSkill / Agentへ委譲する
- Evidenceを統合する
- Conflictを確認する
- Missing Knowledgeを整理する

役割とする。

これはLLM Context肥大化を避けるためでもある。

---

# 30. Principle 29: Agent Executionを追跡可能にする

[PROVISIONAL]

Agent / Skillを利用する場合、その実行結果だけでなく、

- Task
- Sources Checked
- Evidence
- Sources Not Checked
- Open Questions
- Result
- Review Status

を記録できることが望ましい。

長いSessionでも、どの情報を根拠にしたかを後から確認可能にする。

---

# 31. Principle 30: Responsibility / Contract判断はHuman Approvalを必須とする

[DECIDED]

AIは、責任範囲の判断材料を整理することはできる。

しかし、

- 契約上の責任
- 費用負担
- 顧客への正式な責任表明

をAIだけで確定しない。

AIの役割は、Observed Fact、Technical Cause、Current Specification、Historical Agreement、Differenceを整理することまでとする。

最終判断は人間が行う。

---

# 32. Principle 31: StakeholderによってOutputを変える

[DECIDED]

同じ調査結果でも、説明相手によって必要な情報は異なる。

End Userには業務影響や回避方法を中心に説明する。

Customer System / Managementには、原因、仕様、過去合意、改修要否、責任範囲の判断材料を説明する。

Developerには、Reproduction、Code、SQL、Data Flow、Root Cause、Impact、Test Scopeを提示する。

Knowledge自体とPresentationを分離する。

---

# 33. Principle 32: Config-Driven Designを優先する

[DECIDED]

Project固有ルールをApplication Codeへ直接Hard Codingしない。

Config化候補には以下がある。

- Document Types
- Repository Policy
- Masking
- Classification
- Stakeholders
- Graph Schema
- Transformer Rules
- Agent Policy
- Access Policy

これにより別Projectへ横展開できる構造を目指す。

---

# 34. Principle 33: 特定TechnologyへDomainを従属させない

[DECIDED]

Semantica、Neo4j、Vector DB等の採用可否より先に、運用保守として必要なDomain Modelを定義する。

設計順序は以下とする。

1. 運用保守で何を判断する必要があるか
2. そのためにどのKnowledgeが必要か
3. Knowledge間にどのRelationが必要か
4. そのModelをどのTechnologyで実装するか

特定製品のData Modelに業務要件を合わせない。

---

# 35. Principle 34: Semantica等はInfrastructure候補として扱う

[PROVISIONAL]

Semantica等のKnowledge Infrastructureを採用する場合、

- Ingest
- Parse
- Normalize
- Knowledge Graph
- Temporal
- Conflict
- Provenance
- Decision
- MCP

等の汎用Infrastructureとして評価する。

一方、以下は本Project固有のDomainとして自ら設計する。

- Maintenance Ontology
- Case Workflow
- Responsibility Model
- Stakeholder Model
- Repository Policy
- Human Review
- Coverage
- Inquiry Investigation Logic

---

# 36. Principle 35: PoCはEnd-to-Endを優先する

[DECIDED]

PoC初期から以下を全面実装することを目的としない。

- Full Knowledge Graph
- Full Multi-Agent
- Neo4j
- Vector Database
- Production UI
- 全Document変換
- 全Repository再構築

最初に優先するのは、一件の実運用に近い問い合わせについて、

1. 問い合わせメールを入力する
2. Repositoryを調査する
3. Code / Documentへ到達する
4. 技術的原因を整理する
5. Current Specificationを確認する
6. Evidenceを提示する
7. Missing Knowledgeを示す
8. Human Reviewする
9. 結果を再利用可能に残す

というEnd-to-Endの流れを成立させることである。

---

# 37. Principle 36: Golden Sampleを基準に設計する

[PROVISIONAL]

Document IngestやKnowledge Modelを抽象論だけで設計しない。

PoCでは、実Repositoryから代表的な資料・問い合わせを選び、

> このOriginalから最終的にどのAI-Ready情報が生成されれば調査に役立つか

を手作業で定義するGolden Sample方式を優先する。

そのOutputを基にParser、Schema、Relationを設計する。

---

# 38. Principle 37: Repositoryを利用するほどKnowledgeが改善する

[DECIDED]

問い合わせ対応を一回限りのAI Sessionとして終わらせない。

調査によって判明した、

- Fact
- Evidence
- Cause
- Relation
- Review結果

を、Human Review後に次の問い合わせへ再利用可能なKnowledgeとして蓄積できる構造を目指す。

AI推論を自動的に確定Knowledgeへ昇格させない。

---

# 39. Principle 38: Conflictを隠さない

[DECIDED]

Design、Test、Code、Meeting等で内容が食い違う場合、AIが勝手に一つを正しい情報として統合しない。

Conflictとして残し、

- 何と何が矛盾しているか
- Versionはどう違うか
- どちらがCurrentか
- Human Reviewが必要か

を示す。

運用保守では矛盾自体が重要な調査材料になる。

---

# 40. Principle 39: Repository PolicyはGuardrailとして使う

[PROVISIONAL]

将来的にRepository整理を支援する場合、AIは人間を過度に制約しない。

通常の違反は、

- Warning
- Recommendation
- Suggested Location
- Naming Suggestion

を中心とする。

一方、Credential、禁止データ、明確なSecurity違反等はBlocking対象として検討する。

意図的な例外を認める場合は、ReasonやApproverを残せることが望ましい。

---

# 41. Principle 40: 設計判断にはDecision Statusを付ける

[DECIDED]

本Projectでは、確定事項と仮説を混同しない。

重要事項には以下の状態を付ける。

- `[DECIDED]`
- `[PROVISIONAL]`
- `[UNDER_REVIEW]`
- `[OPEN]`
- `[OUT_OF_SCOPE]`

CodexやDeveloperは、`[PROVISIONAL]`や`[OPEN]`を確定事項として実装しない。

## 41.1 追加Design Principles（2026-08-30）

[DECIDED]

- UIはPurpose Firstとし、Graph LayerやRepository構造から開始しない
- Objectiveの追加・切替は同一Work Item内で行い、調査Contextを保持する
- Graph Viewは固定個数を目的化せず、Domain / Function / System / Data / Code / Test / EvidenceにOperationとStakeholderを加える
- Work Item ViewはKnowledge Layerではなく、現在作業に関係するNodeを横断するContext Projectionとする
- Estimationは独立した正本Graphではなく、Changeから影響・Test・Operation・Stakeholder・Evidenceを集約する分析結果とする
- Original Source、Normalized Intermediate、Persistent Knowledge、Runtime Index、System-generated Artifactを分離する
- DeleteはUnlink、Archive、Runtime除外、Permanent Deleteを区別し、影響を事前表示する
- User Action、Execution、Artifactを分け、業務上意味のあるEventだけをKnowledge Graphへ接続する
- System-generated ArtifactはReference / Metadataを基本とし、必要なものだけHuman Review後にEvidenceへ昇格する

---

# 42. Current Critical Open Decisions

以下は本設計原則作成時点でも未確定である。

## Existing Repository Structure

[OPEN]

対象Repositoryを実査した後にArchitectureを確定する。

## Meeting Minutes Access

[OPEN]

CodexからOriginal議事録を直接参照してよいか。

## Meeting Minutes Git Storage

[OPEN]

議事録をRepository / Git Historyへ保存してよいか。

## AI-Ready Canonical Format

[OPEN]

`content.md` / `metadata.yaml` / `relations.json` 等を正式形式とするか。

## Normalized Intermediate Representation

[OPEN]

共通Intermediate ModelのSchema。

## Graph Runtime

[OPEN]

JSON / SQLite / NetworkX / Graph DB等の選択。

## Semantica Adoption Scope

[OPEN]

どこまでInfrastructureとして利用するか。

## Agent Architecture

[OPEN]

PoCでAgent分離をどこまで行うか。

---

# 43. Anti-Patterns

後続設計・実装では、以下を避ける。

## Anti-Pattern 1

既存Repositoryを確認する前に、新Directory構成へ全面移行する。

## Anti-Pattern 2

Office Documentを大量にMarkdown化するだけでAI-Ready化完了とみなす。

## Anti-Pattern 3

Graph DBを導入すること自体を目的にする。

## Anti-Pattern 4

Semantica等のFramework Data Modelへ業務Modelを無理に合わせる。

## Anti-Pattern 5

AI回答の根拠Sourceが分からない。

## Anti-Pattern 6

AI推論と確認済み仕様を同じKnowledgeとして保存する。

## Anti-Pattern 7

重要資料が未確認なのに責任範囲を断定する。

## Anti-Pattern 8

AI-Ready情報を人間がOriginalとは別に手管理する。

## Anti-Pattern 9

すべてをMain AgentのContextへ詰め込む。

## Anti-Pattern 10

PoC初期からProduction規模のInfrastructureを構築する。

---

# 44. 設計判断時の優先順位

技術方式に迷った場合、原則として以下の優先順位で判断する。

1. Evidence Traceability
2. Existing Repository Compatibility
3. Human Verifiability
4. Security
5. Investigation Usefulness
6. Maintainability
7. Rebuildability
8. Simplicity
9. Extensibility
10. Technology Sophistication

高度なTechnologyを導入することより、運用保守の調査がEvidence付きで成立することを優先する。

---

# 45. 後続ドキュメントへの引き継ぎ

本設計原則を、以下の後続設計で具体化する。

## `05_REPOSITORY_ARCHITECTURE.md`

- Existing Repository First
- Overlay vs Existing Structure
- Original / Derived / Runtimeの配置
- Git管理範囲

## `06_KNOWLEDGE_MODEL.md`

- Case
- Knowledge State
- Provenance
- Missing Knowledge
- Stakeholder
- Evidence

## `07_GRAPH_AND_CODEGRAPH.md`

- Domain Graph
- Code Graph
- Data Flow
- Node / Edge / Relation
- Graph Storage Independence

## `08_DOCUMENT_INGEST_AND_TRANSFORM.md`

- Original / Derived separation
- Intermediate Representation
- Security / Masking
- Provenance
- Incremental Update

## `09_CASE_INVESTIGATION_WORKFLOW.md`

- Inquiry Intake
- Technical Cause
- Specification Check
- Historical Evidence
- Responsibility Assessment
- Coverage
- Human Review

## `10_AGENT_AND_SKILL_ARCHITECTURE.md`

- Responsibility-based Agents
- Skill reuse
- Orchestration
- Agent Execution Record

## `11_SECURITY_AND_GOVERNANCE.md`

- Meeting Minutes
- Git History
- Codex Access
- Classification
- Masking
- Human Approval

## `12_RUNTIME_AND_STORAGE.md`

- Git vs Runtime DB
- Rebuildability
- SQLite / Graph / Index
- Incremental Update

---

# 46. Design Principles Statement

> 本Projectでは、既存の運用保守Repositoryと人間の業務を尊重し、Original Evidenceを正しく追跡できる再生成可能なAI-Ready Knowledgeを追加する。問い合わせ、障害、System理解、Operation、Change、Impact Analysis、Estimation等を複数Objectiveを持つWork Itemとして扱い、目的変更時も共通Contextを保持する。Purpose-First UI、Canonical Relation Model、Operation / Stakeholder Projection、Source / Artifact Lifecycleを共通原則とし、特定Graph DBや高度なSecurity運用をPoCの目的にしない。PoCはAI利用承認済みDataへ限定し、Evidence Traceability、Human Verifiability、既存運用との互換性を最優先する。

## 46.1 Graph Presentation and Infrastructure Principles（2026-08-30）

[DECIDED]

1. Functionは提供Capability、SystemはFunctionを実現・稼働する技術境界として分離する。
2. Infrastructure / IaCはSystemとは別Projectionとし、Terraform Module / Resource / State Metadata / DriftをSourceへ戻れる形で表す。
3. Secret値やTerraform State内の機密PropertyをGraphへ複製しない。
4. 平面GraphはRelationの精査、Vertical Stackは層横断の理解に使用し、自由回転する3D表現を目的化しない。
5. Vertical StackはPresentation Modelであり、Canonical Relation ModelやStorage Schemaを階層固定しない。
