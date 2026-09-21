# AI-Ready Operations Repository / Codex App
## 05. Repository Architecture

**File Name:** `05_REPOSITORY_ARCHITECTURE.md`  
**Status:** Draft  
**Document Role:** Repository Architecture / Existing Repository Integration  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、既存の運用保守RepositoryへAI-Readyな調査支援機能をどのように組み込むか、そのRepository Architectureの考え方を整理する。

前提として、本PoCの対象Repositoryはすでに運用保守で利用されており、以下のような既存資産が存在すると認識している。

- Source Code
- 問い合わせごとの調査結果
- テスト項目書
- 運用保守関連資料
- その他の既存資料

ただし、本ドキュメント作成時点では、対象Repository全体の実Directory構成、命名規則、資料配置、Git運用、各Folderの意味をまだ詳細に確認していない。

したがって本ドキュメントでは、

> 新しいDirectory構成を先に確定する

のではなく、

> 既存Repositoryをどのような考え方で理解し、どのようにAI-Ready機能を追加するか

をArchitectureとして定義する。

---

# 2. Repository Architectureの基本方針

[DECIDED]

本PoCでは、以下の順序を守る。

1. Existing Repositoryを確認する
2. 現在の人間の運用方法を理解する
3. 既存Directoryの役割を分類する
4. 既存資産を維持できる部分を特定する
5. AI-Ready化に不足する機能だけを追加する
6. 必要に応じてOverlay構造を追加する
7. PoC後に再編が必要か評価する

AIのためにRepository全体を最初から理想構造へ移動させない。

---

# 3. Repository Architectureで解決したい問題

現在の課題は、単純にDirectoryが整理されていないことではない。

Repository内外に存在する情報を、問い合わせ調査時に横断して利用しにくいことが問題である。

例えば、一件の問い合わせについて以下を確認する可能性がある。

- 問い合わせ内容
- 過去の類似問い合わせ
- Source Code
- API
- Batch
- Database
- SQL
- テスト項目書
- 現行Design
- Release情報
- Git History
- 過去仕様
- 設計打ち合わせ
- 議事録
- 顧客との合意内容

これらが物理的に同じDirectoryに存在する必要はない。

重要なのは、

> どこに存在していても、問い合わせCaseから必要なKnowledgeとして関連付けて辿れること

である。

---

# 4. Physical StructureとLogical Structureを分離する

[DECIDED]

本Repository Architectureでは、

> Fileが物理的にどこに置かれているか

と、

> そのFileがKnowledgeとして何を意味するか

を分離する。

例えば、既存Repositoryに以下のような構造があったとする。

```text
project/
├─ src/
├─ maintenance/
│  ├─ inquiry/
│  ├─ test/
│  └─ release/
└─ documents/
```

この既存構造をAIのために無理に、

```text
docs/
knowledge/
cases/
```

へ移す必要はない。

AI側ではMetadataやIndexによって、

- Inquiry
- Test
- Release
- Design
- Code

として論理的に分類できればよい。

したがってArchitecture上は、

**Physical Repository Structure**

と

**Logical Knowledge Model**

を別レイヤとして扱う。

---

# 5. Repositoryの論理レイヤ

[PROVISIONAL]

対象Repositoryの実構成に依存せず、論理的には以下のレイヤを持つことを想定する。

## 5.1 Existing Human Assets

人間が現在作成・更新・利用している資産。

例：

- Source Code
- Excel
- Word
- PowerPoint
- PDF
- CSV
- 問い合わせ調査フォルダ
- テスト項目書
- Release資料
- 運用資料

これらは原則として既存運用を維持する。

## 5.2 AI-Ready Knowledge

Existing Human Assetsから生成・整理されたAI向け派生情報。

例：

- Structured Metadata
- Summary
- Extracted Knowledge
- Relation
- Provenance
- Searchable Text

## 5.3 Codex Working Session / Resume

Codex上で問い合わせ調査・壁打ちを行ったWorking History。

ここには、最終回答だけではなく、

- 調査途中の仮説
- 実際に確認したFileやCode
- 調査順序
- 人間から追加された情報
- 見つからなかった情報
- 仮説が変更された経緯

などが残る可能性がある。

重要なInvestigation Sourceではあるが、永続Knowledgeの正本とはしない。

## 5.4 Persistent Investigation Knowledge

Codex Session等で行われた調査のうち、Human Review後に再利用すべき内容をSession外へ保存した永続調査Knowledge。

例：

- Inquiry
- Investigation Summary
- Sources Checked
- Sources Not Checked
- Technical Cause
- Evidence
- Open Questions
- Missing Knowledge
- Assessment
- Human Decision
- Final Response

## 5.5 Case / Investigation Knowledge

問い合わせ・障害・変更等の調査単位。

Persistent Investigation KnowledgeとCaseは密接に関係するが、物理的な保存形式は既存問い合わせFolderの実態を確認して決定する。

新しい物理Directoryを前提としない。

## 5.6 Graph / Relation Data

Domain、Code、Data Flow等のRelation。

## 5.7 Configuration / Policy

Project固有のルール。

## 5.8 Generated View

HTML、Report、Coverage、Graph View等。

## 5.9 Runtime State

Cache、Index、Runtime DB、Temporary Session State等。

---

# 6. Existing Human Assetsを最優先する

[DECIDED]

Original DocumentやSource Codeは、人間が業務を行うための資産である。

AI-Ready化を理由に、以下を強制しない。

- ExcelをMarkdownへ置換する
- 問い合わせFolderを新Case Folderへ移動する
- Test FolderをAI用Directoryへ移す
- Source Code Directoryを再編する

Architectureは、Existing Human Assetsを入力として扱う。

---

# 7. Original Sourceの考え方

[DECIDED]

本Projectでは、Original Sourceを以下のように考える。

Original Sourceとは、

> 人間が業務上の正式な情報源・調査Evidenceとして利用している情報

である。

Original SourceはRepository内に存在するとは限らない。

例：

## Repository内

- Source Code
- Test Specification
- Design
- Inquiry Investigation
- Release Document

## Repository外

- NotebookLMで管理している議事録
- 外部共有場所の資料
- 将来接続する可能性のある他System

したがってOriginal SourceとRepository Sourceを同一概念にしない。

また、Codex Resume / SessionはOriginal Evidenceではないが、過去の調査過程を復元するための重要なInvestigation Sourceとして別カテゴリで扱う。

---

# 8. Repository外KnowledgeをArchitecture上考慮する

[DECIDED]

現時点では、過去の議事録・設計打ち合わせ・仕様検討情報は主にNotebookLM側で確認している。

これらは今回の事象について、

- 当時何が要求されたか
- 何が設計上合意されたか
- どの仕様が顧客と開発側で共有されていたか
- 今回事象がどちら側の責任範囲として考えられるか

を確認するための重要なEvidenceである。

そのためRepository Architectureは、External Knowledge Sourceを無視しない。

---

# 9. Meeting Minutesの将来統合

[OPEN]

Security・組織ルール上問題がなければ、将来的には議事録等もRepositoryへ一元管理したい。

一元管理できれば、以下を同一のKnowledge体系で扱える可能性がある。

- Requirement
- Design
- Test
- Meeting
- Inquiry
- Release
- Code

ただし以下は未確認である。

- Codexによる直接参照可否
- Repository格納可否
- Git管理可否
- Git履歴保持可否
- Masking / Redaction要否
- Access Control要件

したがってRepository Architectureは、議事録がRepositoryにあることを必須条件としない。

---

# 10. External Source Reference

[PROVISIONAL]

OriginalをRepositoryへ保存できない場合でも、Repository側で外部Sourceの存在を表現できる構造を検討する。

例えば以下のような情報である。

- Source ID
- Source Type
- Source Location
- Title
- Date
- Related Function
- Related Requirement
- Access Policy
- Checked / Not Checked
- Summary
- Human Reviewer

これにより、

> Evidenceは存在するが、現在Codexから直接参照できない

という状態を表現できる。

# 11. Codex Resume / SessionをInvestigation Sourceとして扱う

[DECIDED]

対象Repositoryから起動して行われたCodexの過去Session / Resumeは、過去の問い合わせ調査を引き継ぐ際の重要なInvestigation Sourceとして扱う。

現在の問い合わせFolderや最終回答だけでは、調査途中の詳細が十分に残っていない場合がある。

Codex Resume / Sessionには、例えば以下が残っている可能性がある。

- 元の問い合わせメール
- 調査開始時の仮説
- 確認したDirectory / File
- 確認したSource Code
- 実行・確認したSQLやData
- 途中で否定された仮説
- 人間が追加で与えた前提情報
- NotebookLM等で確認した内容を人間がCodexへ共有した記録
- 未解決事項
- 最終的な整理に至るまでの経緯

そのため、既存問い合わせを再調査・引き継ぎする際は、利用可能であれば関連するCodex Resume / Sessionも参照候補に含める。

ただし、Codex Resume / Sessionを永続的なSource of Truthにはしない。

---

# 12. Codex Sessionを唯一の保存先にしない

[DECIDED]

今後Codexで行う問い合わせ調査・壁打ちについて、重要な調査結果をCodex Resume / Sessionのみに残す運用は避ける。

理由は以下である。

- Sessionの保持期間や利用可能性に依存する可能性がある
- 別PC・別Account・別担当者から参照できない可能性がある
- Repository上の他Knowledgeと安定してRelationを持たせにくい
- 調査結果と途中仮説が混在する
- Human Review済みの結論とWorking Historyを区別しにくい
- 将来の検索・Case再利用に適さない可能性がある

したがってArchitecture上は、

> Codex Session = Working / Investigation History

> Persistent Investigation Knowledge = 再利用する永続調査成果

として分離する。

---

# 13. Codexの壁打ち・調査結果を外部ファイルへ永続化する

[DECIDED]

今後、Codexで調査・壁打ちした重要な内容は、必要なHuman Reviewを経た上で、Codex Session外の永続ファイルまたは承認されたPersistent Storageへ保存できる構造とする。

永続化候補となる情報は以下である。

- Original Inquiry
- Investigation Summary
- Investigation Steps
- Sources Checked
- Sources Not Checked
- Technical Cause
- Current Specification
- Evidence
- Historical Evidence Reference
- Missing Knowledge
- Open Questions
- Responsibility Assessment Material
- Human Review Result
- Final Decision
- Final Response
- Related Commit / Release

具体的に、

- 一つのMarkdownへ保存するか
- YAML等のStructured Dataを併用するか
- Existing Inquiry Folderへ保存するか
- Central Case Indexへ保存するか

は、`09_CASE_INVESTIGATION_WORKFLOW.md`および`12_RUNTIME_AND_STORAGE.md`で詳細化する。

本Architectureで重要なのは、保存形式よりも、

> Sessionが失われても、重要な調査成果がRepository側または承認済みStorageに残る

ことである。

---

# 14. Investigation Knowledgeの昇格フロー

[PROVISIONAL]

Codex Session上の会話や推論を、そのまま確定Knowledgeとして保存しない。

基本的には以下の流れを想定する。

1. 問い合わせをCodexで調査する
2. Codex Session / ResumeにWorking Historyが蓄積される
3. 調査結果・Evidence・不足情報を整理する
4. Human Reviewを行う
5. 再利用すべき内容をPersistent Investigation Knowledgeとして保存する
6. 次回のCase Retrieval対象にする

これにより、

- 詳細なWorking History
- Human Reviewedな永続Knowledge

を分離できる。

過去の既存問い合わせについては、まずExisting Inquiry FolderとCodex Resume / Sessionの双方を確認し、必要に応じてPersistent Investigation Knowledgeへ整理し直すことを検討する。

---

---

# 15. Overlay Architecture

[PROVISIONAL]

対象Repositoryを実査した結果、既存構造を維持したままAI-Ready機能を追加する必要がある場合、Overlay Architectureを第一候補として検討する。

概念例：

```text
existing-project/
├─ existing-source/
├─ existing-maintenance-folders/
├─ existing-test-documents/
├─ existing-inquiry-folders/
│
└─ ops-ai/
   ├─ knowledge/
   ├─ relations/
   ├─ config/
   ├─ generated/
   └─ tooling/
```

この`ops-ai/`は現時点の仮称であり、採用決定ではない。

重要なのは、

> Existing Repositoryを大きく移動せず、AI向け機能を追加レイヤとして重ねる

という考え方である。

---

# 16. Overlay Architectureの利点

Overlay方式には以下の利点がある。

## Existing Workflowへの影響が小さい

現在のDeveloper / Maintenance担当者のFile配置や作業方法を変更しなくてよい。

## PoCを撤回しやすい

AI-Ready部分が有効でなかった場合でも既存Repositoryへの影響を最小化できる。

## PoC範囲を限定できる

最初は一部Document / InquiryだけAI-Ready化できる。

## 比較しやすい

既存方式とAI-Ready方式の差を評価しやすい。

---

# 17. Overlay Architectureの注意点

Overlay方式にも問題がある。

## Duplicate Information

OriginalとDerived Knowledgeが二重に存在して見える可能性がある。

## Stale Derived Data

Original更新後にDerivedが更新されなければ情報が古くなる。

## Path Mapping

OriginalとDerivedの対応関係を管理する必要がある。

## Human Misuse

AI-Ready KnowledgeをOriginalとして人間が直接修正してしまう可能性がある。

そのためOverlayを採用する場合は、

- Provenance
- Generated Flag
- Update Pipeline
- Validation

が重要となる。

---

# 18. In-Place Metadata Architecture

[PROVISIONAL]

もう一つの候補として、既存Folder構造を維持しながらMetadataだけを追加する方式がある。

例えば既存問い合わせFolderに、

```text
inquiry-001/
├─ existing-files...
└─ ai-metadata.yaml
```

のような補助情報を追加する方式である。

この方式が有効かどうかは、実Repository確認後に判断する。

---

# 19. Central Knowledge Index Architecture

[PROVISIONAL]

Original Fileの隣にAI用Fileを大量生成せず、中央のKnowledge IndexでMappingする方式も候補とする。

概念的には以下となる。

```text
Existing Files
      ↓
Knowledge Builder
      ↓
Central Knowledge Index
      ↓
Codex / App
```

この場合、Original DirectoryがAI用Fileで汚れにくい。

一方でOriginalとKnowledgeのMapping管理がより重要になる。

---

# 20. Architecture Patternは実Repository確認後に選択する

[DECIDED]

現時点では以下のどれかに固定しない。

- Overlay
- In-Place Metadata
- Central Knowledge Index
- Hybrid

実Repositoryを確認して、

- Folder数
- Inquiry管理方法
- Document量
- Git運用
- Human Workflow
- Security要件

を見た上で選択する。

---

# 21. Recommended Logical Architecture

[PROVISIONAL]

現時点の論理Architectureは以下の層に分ける。

## Layer 1: Original / Existing Assets

人間が利用する正式・既存情報。

## Layer 2: Ingestion / Analysis

Originalを解析する処理。

## Layer 3: AI-Ready Knowledge

検索・Relation・要約に利用する派生情報。

## Layer 4: Relation / Graph

Knowledge間の関係。

## Layer 5: Case / Investigation

問い合わせ単位の調査状態。

## Layer 6: Codex / Agent / Skill

Knowledgeを利用して調査するAI層。

## Layer 7: Developer View

Case、Evidence、Coverage、Graph、Timeline等を確認するUI。

この論理レイヤとPhysical Directory構成は一対一に対応する必要はない。

---

# 22. Proposed Physical Structureは参考案とする

[PROVISIONAL]

実Repository確認前の参考構成として、以下のようなStructureを想定できる。

```text
project-root/
├─ AGENTS.md
├─ existing-source-and-documents/
│
└─ ops-ai/
   ├─ config/
   ├─ knowledge/
   ├─ relations/
   ├─ cases/
   ├─ agents/
   ├─ skills/
   ├─ pipeline/
   └─ generated/
```

ただしこれはTarget Repositoryへそのまま適用するDirectory仕様ではない。

`existing-source-and-documents/`は既存Repository構造全体を概念的に表しただけである。

---

# 23. `knowledge/` の役割

[PROVISIONAL]

もしAI-Ready Knowledgeを物理的にRepositoryへ持つ場合、`knowledge/`相当の領域ではPhysical File Typeではなく意味で分類する。

避けたい例：

- excel/
- powerpoint/
- word/

候補となる意味分類：

- business
- functions
- systems
- implementation
- evidence
- stakeholders
- timelines

ただし、実際の分類は`06_KNOWLEDGE_MODEL.md`で定義する。

---

# 24. `cases/` の役割

[PROVISIONAL]

Case用領域を新規作成する場合、問い合わせ・Incident等の調査記録を格納する。

ただしExisting Inquiry Folderがすでに同じ役割を持っている可能性が高いため、

> 新しいcases Directoryを作る

こと自体を目的にしない。

実Repository確認後に、

- Existing Inquiry Folder = Caseとする
- Existing Inquiry FolderへMetadataを足す
- AI側だけCase Indexを作る
- New Case DirectoryへMappingする

のどれが適切か評価する。

---

# 25. `relations/` / `graph/` の役割

[PROVISIONAL]

Graph / RelationはOriginal DocumentではなくDerived Dataとして扱う。

候補として以下を分離する。

- Domain Relation
- Code Relation
- Data Flow Relation

ただし物理的に3 Directoryへ分けることは必須ではない。

重要なのはSchema上の区別である。

---

# 26. Code Graphの配置

[PROVISIONAL]

Code GraphはSource Codeそのものではない。

Source Codeから再生成可能なDerived Dataとして扱う。

したがって、

- Code Node
- Call Relation
- Dependency Relation

をGitへ保持するかRuntime生成するかはPoCで評価する。

Source CodeよりCode Graphを正本にしない。

---

# 27. Data Flowの配置

[PROVISIONAL]

Data Flow GraphもDerived Dataとして扱う。

Data Flowには、Code解析だけで抽出できない情報が存在する可能性がある。

例えば、

- Fileの業務上の意味
- Tableの意味
- Batchの実行時刻
- External Systemとの連携
- 月次 / 日次の業務周期

などである。

したがってData Flowは、

> Codeから自動抽出した情報

と

> Document / Human Knowledgeから得た情報

を区別して保持できることが望ましい。

---

# 28. `config/` の役割

[DECIDED]

Project固有ルールは可能な限りConfigとして分離する。

候補：

- Project Settings
- Document Types
- Classification
- Masking
- Repository Policy
- Stakeholders
- Graph Schema
- Transformer Rules
- Agent Policy
- Access Policy

Project固有条件をApplication Codeへ散在させない。

---

# 29. `pipeline/` / Toolingの役割

[PROVISIONAL]

AI-Ready Knowledgeを生成する処理は、Original Documentとは分離する。

候補処理：

- Discover
- Classify
- Parse
- Normalize
- Mask
- Transform
- Validate
- Index
- Build Relation
- Generate View

Semantica等を採用する場合も、このPipelineの一部として呼び出すことを検討する。

Application全体を特定Frameworkへ直接依存させない。

---

# 30. `agents/` と `skills/`

[PROVISIONAL]

Agent定義やSkill定義をRepositoryで管理する場合、Source Code / Knowledgeとは分離する。

Agentは責務を表す。

Skillは再利用可能な実行能力を表す。

具体構成は`10_AGENT_AND_SKILL_ARCHITECTURE.md`で決定する。

---

# 31. `generated/` の役割

[DECIDED]

Generated ViewはSource of Truthにしない。

候補：

- HTML
- Case Report
- Coverage Report
- Graph Visualization
- Timeline
- Repository Summary

生成物を手修正して正式情報を変更する運用にはしない。

---

# 32. Runtime Data

[DECIDED]

Runtimeでのみ必要な情報は、Original / Knowledgeから分離する。

候補：

- Cache
- Runtime DB
- Search Index
- Vector Index
- Temporary Graph
- Session
- Last Indexed Commit
- Processing Log

Runtime Dataは原則として再生成可能にする。

---

# 33. Git管理対象の考え方

[PROVISIONAL]

Git管理対象は情報の性質によって決める。

## 原則Git管理する候補

- Source Code
- Config
- Agent / Skill定義
- Schema
- Repository Policy
- Human Reviewed Knowledge
- Case結果
- Pipeline Code

## 条件付きでGit管理する候補

- AI-Ready Derived Knowledge
- Graph Relation
- Generated Reports
- Meeting Minutes

## 原則Git管理しない候補

- Cache
- Runtime Index
- Vector Index
- Temporary Files
- Local Session
- Secret
- Credential

具体的な管理方針はSecurity / Storage設計で決定する。

---

# 34. Derived KnowledgeをGit管理するか

[OPEN]

Derived Dataは再生成可能であるため、必ずしもGit管理する必要はない。

一方でGit管理すると、

- AI-Ready変換結果のDiffをReviewできる
- Parser変更による差分を確認できる
- Knowledge変更履歴を追える

という利点がある。

PoCでは、

> Human Review価値があるDerived KnowledgeだけGit管理する

方式も候補とする。

---

# 35. Runtime Databaseの位置付け

[DECIDED]

Runtime DBをSource of Truthにしない。

SQLite、Graph DB、Vector DB等を利用する場合でも、それらは、

> Retrieval / Search / Relation探索を高速化するDerived Runtime Infrastructure

として扱う。

DBを削除してもRepositoryから再構築可能なArchitectureを目標とする。

---

# 36. Stable ID

[PROVISIONAL]

Relationを安定して保持するため、File PathだけをIdentityとして使わないことを検討する。

例えばFile Rename時にRelationが全て壊れることを避ける。

Stable IDが必要になる対象候補：

- Document
- Knowledge Object
- Case
- Function
- System
- Test Case
- Meeting
- Stakeholder
- Graph Node

具体方式は`06_KNOWLEDGE_MODEL.md`で検討する。

---

# 37. Source-to-Derived Mapping

[DECIDED]

AI-Ready Knowledgeを持つ場合、OriginalとのMappingを必ず保持する。

最低限、

- Original Source
- Derived Object
- Version / Commit
- Transformer Version

を関連付ける。

Originalが更新された場合、Derivedが更新対象であることを判定できる必要がある。

---

# 38. Move / Rename / Delete

[PROVISIONAL]

Existing RepositoryではFileが移動・改名・削除される可能性がある。

AI-Ready Layerでは、

- Deleted OriginalのKnowledgeが残り続ける
- RenameをNew Documentと誤認する
- Duplicate Knowledgeが発生する

問題を避ける必要がある。

Git HistoryやStable IDを利用した対応を検討する。

---

# 39. Incremental Update

[PROVISIONAL]

全Repositoryを毎回処理する方式ではなく、変更分のみ処理することを基本方向とする。

候補：

1. Last Processed Commitを確認
2. Git Diffを取得
3. Added / Modified / Deletedを判定
4. 対象Originalを再処理
5. Related Knowledge / Relationを更新
6. Indexを更新
7. Processing Resultを記録

PoCでは最小限の実装でもよい。

---

# 40. Repository Discovery結果を保存する

[PROVISIONAL]

PoC開始時にExisting Repositoryを解析した結果は、一回限りの会話で終わらせず、Repository Architecture判断のEvidenceとして残すことを検討する。

例えば以下を記録する。

- Detected Directories
- Directory Purpose
- Existing Inquiry Pattern
- Test Document Pattern
- Design Document Pattern
- Naming Pattern
- Current / Historical Separation
- Git Usage
- Related Codex Resume / Sessionの存在と参照可能性
- 過去調査結果がFolderとSessionのどちらに詳しく残っているか
- Identified Risks
- Open Questions

これによりArchitecture判断を後から再確認できる。

---

# 41. Repository Navigator

[FUTURE]

将来的には、新しいDocumentを追加する際にAIが、

- 推奨配置先
- 推奨File Name
- 関連Document
- 必要Metadata
- Existing Patternとの整合性

を案内できることを検討する。

ただしRepository NavigatorはArchitectureの中心機能ではなく、既存Repository理解・Policy定義後の支援機能とする。

---

# 42. Repository Policy

[PROVISIONAL]

Repository整理を支援するため、将来的にPolicyを定義する可能性がある。

例：

- Naming Convention
- Current / Historical Document Separation
- Required Metadata
- Security Restrictions
- Generated File Placement

Policyは通常、Warning / Recommendationを中心とする。

AIの都合による過度な制約を避ける。

---

# 43. Existing Inquiry FolderのArchitecture上の扱い

[OPEN]

Existing Inquiry Folderは本PoCで非常に重要である。

過去問い合わせは、

- Inquiry Text
- Investigation
- SQL
- Code Reference
- Cause
- Answer
- Test
- Fix

などを含む可能性があり、実質的にPast Case Knowledgeとなり得る。

対象Repository確認後、以下を評価する。

## Option A

Existing Inquiry FolderをそのままCaseとして扱う。

## Option B

Existing Inquiry FolderへMetadataのみ追加する。

## Option C

Central Case IndexからExisting Inquiry Folderを参照する。

## Option D

AI-Ready Caseへ変換する。

現時点ではどれにも固定しない。

---

# 44. Test DocumentのArchitecture上の扱い

[OPEN]

既存テスト項目書について、実Format確認後に以下を決める。

- Originalはどこにあるか
- Excel Sheet構成
- Test Case粒度
- Version管理
- Current / Historical区別
- FunctionとのRelation
- RequirementとのRelation

Test Documentを単なる全文検索対象にするか、Test Case Knowledgeへ変換するかはPoCで評価する。

---

# 45. Current / Historical Document

[PROVISIONAL]

運用保守ではCurrent SpecificationとHistorical Specificationを混同しないことが重要である。

Repository Architectureでは、Directoryだけで区別できない場合でもMetadataで、

- Current
- Historical
- Superseded
- Draft
- Deprecated

等を表現できることが望ましい。

---

# 46. CommitをKnowledge Eventとして扱う可能性

[FUTURE]

Git Commitは変更イベントとして利用できる可能性がある。

例えば一つのCommitで、

- Design
- Test
- Code
- Release

が変更された場合、そのCommitを介して変更関係を追跡できる。

ただし全CommitをGraph Nodeにすることを初期要件とはしない。

---

# 47. Releaseとの関係

[PROVISIONAL]

運用保守では、

> いつその仕様が本番へ反映されたか

が重要になる。

将来的には、

- Change
- Commit
- Test
- Release
- Effective Date

を関連付ける。

Repository ArchitectureではRelease資料の既存配置を確認し、無理に新Directoryへ移動しない。

---

# 48. AGENTS.mdの位置付け

[PROVISIONAL]

CodexがRepositoryで作業する際の入口として、Repository Rootまたは適切なScopeに`AGENTS.md`を置くことを検討する。

AGENTS.mdには詳細なKnowledgeを詰め込まず、

- Handoff Documentsの参照先
- Repository理解ルール
- Security注意事項
- Decision Statusの扱い
- 実装前確認事項

などを記載する。

詳細設計は各MDへ分離する。

---

# 49. Handoff Documentsの配置

[PROVISIONAL]

今回作成しているHandoff Documentsは、Codexが新しいSession / PC / AccountでもDesign Contextを復元するために利用する。

配置先はExisting Repository確認後に決定する。

候補例：

```text
docs/ai-ops-design/
```

またはOverlay方式で、

```text
ops-ai/docs/
```

など。

重要なのはDirectory名ではなく、Codexが入口から順番に辿れることである。

---

# 50. Handoff DocumentsはImplementationと同期させる

[DECIDED]

Handoff Documentが設計だけ残り、実装と乖離しないようにする。

重要なArchitecture変更を行った場合は、

- Decision
- Reason
- Affected Document
- Implementation Impact

を更新する。

実装がDesign Documentと異なる場合、その差を明示する。

---

# 51. Architecture Decision Record

[FUTURE]

設計判断が増えた場合、ADRのようなDecision Recordを導入することを検討する。

特に以下の変更では有効である。

- Overlay Architecture採用
- Graph DB導入
- Semantica採用
- Meeting MinutesのRepository統合
- Stable ID方式
- AI-Ready Canonical Format

PoC初期では必須としない。

---

# 52. Repository ArchitectureにおけるSemantica

[PROVISIONAL]

Semanticaを採用する場合でも、Repository StructureをSemanticaの内部構造へ合わせない。

Semanticaは以下のInfrastructure候補として扱う。

- Parse
- Normalize
- Knowledge Graph
- Provenance
- Temporal
- Conflict
- Decision
- MCP

Repository側のDomain Structureは本Projectが所有する。

---

# 53. Repository ArchitectureにおけるGraph DB

[DECIDED]

Graph機能を採用することとGraph DBを採用することを分離する。

Graph DBなしでも、

- JSON
- SQLite
- NetworkX

等でRelationを表現可能である。

PoCではRelation Modelの有効性を先に確認し、Storage製品はその後に選択する。

---

# 54. Repository ArchitectureにおけるSQLite

[PROVISIONAL]

PoC RuntimeとしてSQLiteは候補となる。

用途候補：

- Document Index
- Knowledge Node
- Relation
- File Version
- Processing Status
- Case Index
- Provenance

ただしSQLite採用はまだ決定ではない。

重要情報はSQLiteだけに保持しない。

---

# 55. Architecture Review Gate 1: Existing Repository Review

[DECIDED]

以下を確認するまでPhysical Architectureを確定しない。

- Root Directory
- Main Source Code Directory
- Inquiry Folder
- Test Folder
- Design Document Location
- Release Document Location
- Existing AI / Codex Related Files
- Git Ignore
- Large Binary Files
- Current / Historical Document Pattern

この確認をPoC開始時の最初のArchitecture Taskとする。

---

# 56. Architecture Review Gate 2: Security / Meeting Minutes

[DECIDED]

Meeting Minutes統合方式は、以下を確認後に決定する。

- Codex Direct Access
- Repository Storage
- Git History Storage
- PII
- Customer Information
- Contract / Responsibility Information
- Masking
- Access Control

確認前に議事録OriginalをGitへ追加しない。

---

# 57. Architecture Review Gate 3: Golden Sample

[DECIDED]

Repository全体を一括AI-Ready化する前にGolden Sampleを選定する。

候補：

- 代表的問い合わせ一件
- 関連Test Document一つ
- 関連Design一つ
- 関連Code
- 必要であればHistorical Evidence

このSampleを使い、

- Original
- AI-Ready Knowledge
- Relation
- Provenance
- Case Retrieval

が成立するか確認する。

---

# 58. Architecture Review Gate 4: Derived Data Placement

[OPEN]

Golden Sample後に以下を決める。

- Derived KnowledgeをRepositoryへCommitするか
- Runtime生成のみとするか
- Hybridとするか
- GraphをRepositoryへ保存するか
- HTMLをCommitするか

PoCのReview価値とRepository Sizeを基準に判断する。

---

# 59. Architecture Review Gate 5: Runtime Storage

[OPEN]

PoCのQuery要件が見えた後に、

- JSON
- SQLite
- NetworkX
- Semantica
- Graph DB
- Vector Index

の必要性を判断する。

最初からInfrastructureを過剰に導入しない。

---

# 60. Recommended PoC Architecture

[PROVISIONAL]

現時点で最も安全なPoC Architectureは以下である。

## Step 1

Existing Repositoryを変更せず解析する。

## Step 2

Repository内の既存問い合わせ・Test・CodeのMappingを作る。

## Step 3

PoC用の小さなAI-Ready領域を追加する。

## Step 4

Golden SampleだけKnowledge化する。

## Step 5

問い合わせメールからGolden Sample Knowledgeへ到達させる。

## Step 6

不足EvidenceをNot Checked / Missingとして扱う。

## Step 7

PoC結果を見てRepository Structureを再評価する。

この順序であれば、既存Repositoryを壊さずに成立性を確認できる。

---

# 61. Physical Structureの暫定例

[PROVISIONAL]

実Repository確認後に変更する前提で、Overlayを採用する場合の最小例を以下に示す。

```text
repository-root/
├─ <existing directories remain unchanged>
│
├─ AGENTS.md
│
└─ ops-ai/
   ├─ docs/
   │  └─ handoff/
   ├─ config/
   ├─ knowledge/
   ├─ relations/
   ├─ tooling/
   └─ generated/
```

PoC初期から以下をすべて作る必要はない。

- agents/
- skills/
- graph/
- runtime/
- app/

必要になった時点で追加する。

---

# 62. 最初にDirectoryを作りすぎない

[DECIDED]

まだ用途が確定していないDirectoryを大量に作成すると、

- どこへ何を置くか分かりにくくなる
- Existing Repositoryとの重複が増える
- Codexが空Folderや類似Folderを誤解する
- 将来の再編コストが増える

可能性がある。

PoC初期では必要最小限のDirectoryだけ追加する。

---

# 63. PoC初期に必要な最小構成候補

[PROVISIONAL]

既存Repository確認後、Overlay方式が適切と判断された場合、最初は以下程度でもよい。

```text
ops-ai/
├─ docs/
├─ config/
├─ knowledge/
└─ tooling/
```

Case、Graph、Agent等はLogical Modelとして先に定義し、物理Directoryは必要になってから追加する。

---

# 64. Repository Architectureの成功条件

Repository Architectureが成功している状態は、

> 理想的に見えるFolder Treeができた状態

ではない。

以下が成立することを重視する。

- Existing Repositoryの人間運用を壊していない
- Inquiryから必要なSourceへ辿れる
- OriginalとDerivedを区別できる
- DerivedからOriginalへ戻れる
- Repository外Evidenceを表現できる
- 過去Codex Sessionを引き継ぎ時のInvestigation Sourceとして利用できる
- 今後の重要なCodex調査成果がSession外へ永続化される
- Missing Knowledgeを扱える
- Runtime DBを削除しても再構築可能
- PoC後にArchitectureを変更できる
- 特定FrameworkへRepositoryが従属していない

---

# 65. 現時点の未確定事項

[OPEN]

## Existing Repository Physical Structure

実査後に確定する。

## Overlay Directory Name

`ops-ai/`は仮称。

## Existing Inquiry Mapping

CaseへどうMappingするか。

## AI-Ready Knowledge Placement

Central / In-Place / Overlay / Runtimeのみ、のどれにするか。

## Derived Knowledge Git Management

Commitする範囲。

## Meeting Minutes Integration

Repository統合可否。

## Runtime DB

SQLite等を採用するか。

## Graph Persistence

Repository / Runtimeのどちらに置くか。

## Generated View Persistence

GitへCommitするか。

## Stable ID

具体方式。

## Persistent Investigation File Format

Codex SessionからHuman Review後に保存する調査Knowledgeの物理形式と保存先。

## Codex Resume / Session Access

過去Sessionをどの範囲まで参照・検索・引き継ぎに利用できるか。

---

# 66. Repository確認後にCodexが最初に行うべきこと

対象RepositoryでPoCを開始するCodexは、実装前に以下を行う。

1. RootからDirectory構成を確認する
2. 主要Folderの目的を推定する
3. 問い合わせFolderを確認する
4. 利用可能であれば、Repositoryに関連する過去Codex Resume / Sessionを確認する
5. 過去調査結果がInquiry FolderとCodex Sessionのどちらに詳しく残っているか整理する
6. Test Documentを確認する
7. Design / Operation資料を確認する
8. Source Code構成を確認する
9. Git History / Git Ignoreを確認する
10. Current / Historical資料の区別方法を確認する
11. Handoff Documentの想定と実Repositoryの差を整理する
12. Physical Architectureの最小変更案を提示する

この確認なしにRepository再編や大量のAI-Ready変換を開始しない。

---

# 67. Repository Architecture Decision Rule

Architecture上の判断に迷った場合は、以下の順序で優先する。

1. Existing Human Workflowを壊さない
2. Securityを守る
3. Original Evidenceを維持する
4. Provenanceを確保する
5. Inquiry Investigationに役立つ
6. Human Reviewしやすい
7. 再生成可能である
8. 単純である
9. 将来拡張できる
10. 技術的に高度である

---

# 68. Repository Architecture Statement

> 本PoCのRepository Architectureは、既存の運用保守Repositoryを正しく理解し、その人間向け構造と運用を可能な限り維持した上で、AI-Ready Knowledge、Relation、Case、Config、Runtime等の機能を必要な範囲だけ追加する。Physical DirectoryとLogical Knowledge Modelを分離し、OriginalとDerived、Repository内SourceとExternal Source、CurrentとHistoricalを区別する。過去のCodex Resume / Sessionは引き継ぎ時の重要なInvestigation Sourceとして活用する一方、今後の重要な調査・壁打ち成果はSessionのみに依存せず、Human Review後にPersistent Investigation Knowledgeとして外部ファイルまたは承認済みStorageへ保存する。新しいDirectory構成やGraph DBを先に目的化せず、問い合わせ調査のTraceability、Evidence、Missing Knowledge、Human Review、Knowledge Reuseを成立させることをArchitecture判断の中心とする。

## 68.1 2026-08-30 Repository Refinement

[DECIDED]

`cases/`は物理Directory名として即時変更を必須にせず、Logical Modelでは`work-items/`へ一般化する。Work ItemはType、Primary Objective、Secondary Objectivesを持ち、CaseはInquiry / Incident互換として扱う。Original Source、Normalized Intermediate、Persistent Knowledge、Runtime Derived Index、System-generated Artifactは保存責務を分離する。生成物は原則Metadata / Referenceだけを管理し、Human Reviewで重要なものだけEvidenceへ昇格する。Permanent Deleteは参照中Work Item、Derived Knowledge、Graph Edge、Audit要件のImpact Preview後にのみ候補化する。

## 68.2 Infrastructure / IaC Repository Refinement（2026-08-30）

[DECIDED]

Terraform等のIaC SourceはExisting Human / Machine Assetsとして保持し、Infrastructure / IaC Graphは再生成可能なDerived Relationとして管理する。Terraform HCL、Module、Provider Resource、Plan、State Metadata、Drift ResultとSource Locationの対応をStable IDで追跡するが、State内のSecret値をKnowledge StoreへCopyしない。Logical ModelではFunction、System、Infrastructureを分離し、`Function --IMPLEMENTED_BY--> System --HOSTED_ON/PROVISIONED_BY--> InfrastructureResource / IaCDefinition`として接続する。Vertical Stackは`generated/`相当の表示Projectionであり、RepositoryのPhysical Directory階層にはしない。
