# AI-Ready Operations Repository / Codex App
## 08. Document Ingest and Transform

**File Name:** `08_DOCUMENT_INGEST_AND_TRANSFORM.md`  
**Status:** Draft  
**Document Role:** Document Ingestion / Normalization / AI-Ready Transformation / Provenance  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、既存Repositoryや許可された外部Sourceに存在するDocumentを、

> Originalの意味・Evidence価値・人間の運用を維持したまま、Codexが検索・関連付け・調査しやすいAI-Ready Knowledgeへ変換する方法

を定義する。

対象候補には以下が含まれる。

- Excel
- Word
- PowerPoint
- PDF
- CSV
- Markdown
- Text
- 問い合わせ調査Folder内の各種File
- Test Specification
- Design Document
- Release Document
- Operation Document
- 将来Repositoryへ統合可能なMeeting Minutes

本ドキュメントでは、特定Parser LibraryやSemantica採用を確定しない。

---

# 2. Document Ingestの目的

[DECIDED]

Document Ingestの目的は、

> Office FileをMarkdownへ変換すること

ではない。

本来の目的は、

- Documentの意味を理解する
- 必要な情報を構造化する
- Originalへ戻れるようにする
- 検索可能にする
- Knowledge Relationを作れるようにする
- Security Policyを適用する
- Current / Historicalを区別できるようにする
- Case調査で必要部分だけ取得できるようにする

ことである。

---

# 3. Original Documentを置き換えない

[DECIDED]

AI-Ready化のために、人間が利用しているOriginal Documentを別Formatへ移行することを要求しない。

例えば、

- Excel Test Specification
- PowerPoint Design
- Word Manual

はOriginalのまま維持する。

AI向け情報はDerived Knowledgeとして生成する。

---

# 4. 基本Pipeline

[DECIDED]

Document Ingestの基本Pipelineは以下とする。

1. Source Discovery
2. Classification
3. Parsing
4. Normalization
5. Security / Masking
6. Domain Transformation
7. Relation Extraction
8. Validation
9. Persistence
10. Index / Graph Update
11. Human Review

この順序は論理構造であり、実装上すべて別Processにする必要はない。

---

# 5. Officeから直接Markdownへ変換しない

[DECIDED]

以下の単純Pipelineに固定しない。

`Excel / Word / PowerPoint → Markdown`

理由：

- Table構造が失われる
- Sheet / Cell位置が失われる
- Slide上の図形関係が失われる
- CommentやNoteが失われる
- 色や強調が意味を持つ場合がある
- Merge Cellが意味を持つ場合がある
- Formulaと表示値の違いが失われる
- OriginalへのSource Mappingが難しくなる

そのため共通のNormalized Intermediate Representationを間に置くことを検討する。

---

# 6. Normalized Intermediate Representation

[PROVISIONAL]

異なるFile Formatを共通のDomain Transformationへ渡すため、中間表現を導入する。

論理的には、

Original  
→ Format-Specific Parser  
→ Normalized Intermediate Representation  
→ Domain Transformer

とする。

このIntermediate Representationは最終Knowledgeではない。

---

# 7. Intermediate Representationの目的

[DECIDED]

中間表現を導入する目的は以下。

- Excel / Word / PowerPoint / PDF差異を吸収する
- Security処理を共通化する
- Provenanceを維持する
- Domain Transformationを再利用する
- Parser交換を容易にする
- Semantica等の外部Infrastructureを交換しやすくする

---

# 8. Intermediate Representation候補

[PROVISIONAL]

以下のようなPrimitiveを持つことを検討する。

- Document
- Section
- Paragraph
- Table
- Row
- Cell
- List
- ImageReference
- Shape
- Note
- Comment
- Heading
- Metadata
- SourceLocation

Format固有情報を完全に捨てず、必要な情報を保持できる構造とする。

---

# 9. Source Discovery

[DECIDED]

PoC開始時には、既存Repository内のDocumentをまず発見・分類する。

確認対象：

- File Path
- Extension
- Size
- Updated Date
- Git Status
- Directory Context
- Naming Pattern
- Duplicate候補
- Historical候補
- Current候補
- Security Risk候補

対象Repository実査前に全Documentを変換対象と決めない。

---

# 10. Document Classification

[DECIDED]

Documentは拡張子と業務上の意味を分けて分類する。

## Physical Format

- xlsx
- docx
- pptx
- pdf
- csv
- md
- txt

## Business Document Type

候補：

- Requirement
- Design
- Test Specification
- Test Result
- Inquiry
- Investigation
- Meeting
- Release
- Operation Manual
- Responsibility / Contract Material
- Unknown

同じExcelでもDocument Typeは異なる。

---

# 11. Classification Source

[PROVISIONAL]

Business Document Type判定には以下を利用できる。

- Directory
- File Name
- Sheet Name
- Document Title
- Content
- Existing Metadata
- Human Rule
- AI Classification

AI Classificationのみを確定値としない。

---

# 12. Unknown Document Type

[DECIDED]

分類できないDocumentを無理に既存Typeへ当てはめない。

`unknown`または`needs_review`として扱う。

PoCではUnknownが存在することを正常状態として扱う。

---

# 13. Document TypeごとのParser

[PROVISIONAL]

Physical FormatごとにParserを分ける。

例：

- Excel Parser
- Word Parser
- PowerPoint Parser
- PDF Parser
- Text Parser
- Source Code Parser

ただしDomain Transformationは可能な限り共通化する。

---

# 14. Excel Parsing

[PROVISIONAL]

Excelでは単純なCell Textだけでなく、必要に応じて以下を保持する。

- Workbook
- Sheet Name
- Cell Address
- Row / Column
- Cell Value
- Formula
- Displayed Value
- Merge Range
- Comment
- Hyperlink
- Hidden Row / Column
- Named Range
- Table Structure
- Formatting Signal

すべてをKnowledge化するわけではない。

---

# 15. Excel Formattingの意味

[OPEN]

色、Bold、Border等が業務上の意味を持つ場合がある。

例えば、

- 赤色 = NG
- 黄色 = 未確認
- Gray = 対象外

等。

対象Repositoryの実Fileを確認して、Formattingを意味情報として保持する必要性を判断する。

---

# 16. Excel Test Specification

[PROVISIONAL]

Test Specificationについては、以下のKnowledge抽出を検討する。

- Test Case ID
- Scenario
- Preconditions
- Input
- Expected Result
- Actual Result
- Result
- Related Function
- Related Requirement
- Version

ただしRow単位で機械的にTestCase化することを前提にしない。

Golden Sampleで実Sheetを確認して粒度を決める。

---

# 17. Word Parsing

[PROVISIONAL]

Wordでは以下を保持することを検討する。

- Heading Hierarchy
- Paragraph
- List
- Table
- Footnote
- Comment
- Hyperlink
- Page Reference
- Image Reference

Heading構造をSection Knowledgeの候補として利用する。

---

# 18. PowerPoint Parsing

[PROVISIONAL]

PowerPointでは以下を検討する。

- Slide Number
- Slide Title
- Text Box
- Shape
- Connector
- Table
- Speaker Note
- Image Reference

単純にTextだけ抜き出すと、図形間の関係が失われる可能性がある。

---

# 19. PowerPoint Diagram

[OPEN]

Architecture Diagram、Data Flow Diagram等について、

- Shape Relation
- Connector
- Position

をどこまで構造化するかは未決定。

PoCでは重要DiagramのみHuman Review付きで扱う方式も候補とする。

---

# 20. PDF Parsing

[PROVISIONAL]

PDFはSourceの性質によって品質が異なる。

候補：

- Text PDF
- Scanned PDF
- Office Export PDF
- Diagram-heavy PDF

Parserで十分な構造を取得できない場合、Source Qualityを記録する。

---

# 21. OCR

[PROVISIONAL]

OCRが必要なDocumentについては、変換品質が低下する可能性を明示する。

OCR結果をHuman Verified Knowledgeとして自動登録しない。

---

# 22. CSV / Data File

[PROVISIONAL]

CSV等はDocumentとしてだけでなくData Sourceとして扱う場合がある。

特に、

- Input File
- Output File
- Sample Data
- Test Data

の区別が必要となる。

Production DataをそのままAIへ渡すことはSecurity判断対象とする。

---

# 23. Markdown / Text

[DECIDED]

既存Markdown / Textは比較的直接利用しやすいが、

- Document Type
- Version
- Provenance
- Current / Historical

等のMetadataは別途必要となる可能性がある。

---

# 24. Source CodeはDocument Parserと分離する

[DECIDED]

Source Code解析は通常Document Ingestとは異なるParserを利用する。

Source Codeからは、

- Symbol
- Call
- Dependency
- Data Access

等を抽出し、Code Graphへ渡す。

ただしDocument Ingest PipelineとProvenance / Index等は共通化できる。

---

# 25. Security / MaskingはAI利用前に行う

[DECIDED]

Markdownへ変換してからSecurityを考えるのではなく、AIへ渡す前のPipelineにSecurity処理を含める。

対象候補：

- Personal Information
- Customer Information
- Credential
- Token
- Secret
- Production Data
- Contract Information
- Responsibility Information

---

# 26. ClassificationとAccess Policy

[PROVISIONAL]

SourceまたはKnowledgeにSecurity Classificationを持たせる。

候補：

- public
- internal
- confidential
- restricted
- ai_not_allowed

具体Classificationは組織ルールに合わせる。

---

# 27. Meeting Minutes

[OPEN]

Meeting Minutesは、本Projectで非常に重要なHistorical Evidenceである。

一方で以下は未確定。

- Codex Direct Access
- Repository Storage
- Git Storage
- Git History Storage
- Personal Information
- Customer Information
- Responsibility / Contract Information

上司等の確認前にOriginal Meeting MinutesをRepositoryへ取り込まない。

---

# 28. Meeting Minutesが利用可能な場合

[PROVISIONAL]

許可された場合、Meeting Minutesから以下を抽出することを検討する。

- Meeting Date
- Topic
- Requirement
- Question
- Customer Request
- Development Response
- Decision
- Agreement
- Open Item
- Related Function

特にDecision / Agreementを責任範囲評価Evidenceとして利用する。

---

# 29. Meeting MinutesをRepositoryへ置けない場合

[PROVISIONAL]

OriginalをRepositoryへ保存できない場合でも、

- Source ID
- Source Location
- Date
- Topic
- Allowed Summary
- Decision Summary
- Access Policy

のみRepository側で管理する方式を検討する。

---

# 30. NotebookLMとの関係

[DECIDED]

現時点ではNotebookLMがHistorical Meeting / Specificationの重要な参照手段である。

PoCではNotebookLMを無条件に廃止しない。

Repository統合可否が決まるまでは、

> External Evidence Source

として扱う。

---

# 31. Codex SessionはDocument Ingest対象ではない

[DECIDED]

Codex Resume / Sessionは通常のOriginal Documentとは異なる。

SessionはWorking Historyであり、

-途中仮説
- 質問
- 調査経路
- AI推論

を含む。

そのため、Document Ingest PipelineでそのままKnowledge化しない。

---

# 32. Codex SessionからPersistent Investigation Knowledgeへ

[DECIDED]

Codex調査終了時に、再利用すべき情報を整理してPersistent Investigation Knowledgeへ保存する。

候補：

- Investigation Summary
- Sources Checked
- Sources Not Checked
- Technical Cause
- Evidence
- Missing Knowledge
- Open Questions
- Human Decision
- Final Response

この保存処理の詳細は`09_CASE_INVESTIGATION_WORKFLOW.md`で定義する。

---

# 33. Domain Transformation

[DECIDED]

Normalized Dataから、本ProjectのKnowledge Modelへ変換する。

候補：

- Document → Requirement
- Document → Function
- Test Table → TestCase
- Meeting Text → Decision
- Inquiry Folder → PastInquiry
- Design Table → Data Flow
- Release Sheet → Release

すべてを自動抽出することを前提にしない。

---

# 34. Knowledge Extraction

[PROVISIONAL]

AI / Rule / Parserを組み合わせて以下を抽出する。

- Entity
- Fact
- Relation
- Requirement
- Business Rule
- Test Case
- Decision
- Agreement
- Stakeholder
- Date
- Data Flow

---

# 35. Extraction Methodを記録する

[DECIDED]

Knowledgeがどの方法で生成されたかを記録する。

候補：

- parser
- deterministic_rule
- ai_extraction
- ai_inference
- human_curated

Human CuratedとAI Inferredを区別する。

---

# 36. AI Extractionは確定Knowledgeではない

[DECIDED]

AI抽出結果は原則、

`ai_extracted`

または

`needs_review`

として扱う。

重要な仕様・責任EvidenceはHuman Reviewを経て昇格させる。

---

# 37. Relation Extraction

[PROVISIONAL]

DocumentからKnowledgeだけでなくRelationも抽出する。

例：

- Function TESTED_BY TestCase
- Requirement DEFINED_BY Design
- Decision AFFECTS Function
- Release INCLUDES Change
- Design DEFINES Table

RelationにもProvenanceを付与する。

---

# 38. AI-Ready Output

[PROVISIONAL]

AI-Ready Knowledgeの物理形式候補として以下を検討する。

- `content.md`
- `metadata.yaml`
- `relations.json`

ただし正式決定ではない。

---

# 39. `content.md` の役割

[PROVISIONAL]

HumanとLLMが読みやすいNarrative / Structured Textを保持する。

候補：

- Document Summary
- Section
- Extracted Facts
- Notes
- Human Review Comment

MetadataやRelationの正本をすべてMarkdown本文に埋め込まない。

---

# 40. `metadata.yaml` の役割

[PROVISIONAL]

Structured Metadataを保持する。

候補：

- ID
- Document Type
- Title
- Source
- Version
- Effective Date
- Security Class
- Knowledge State
- Related Function
- Review Status

---

# 41. `relations.json` の役割

[PROVISIONAL]

Node / Edge等のProgrammatic Relationを保持する候補。

ただしGraph RuntimeがSQLite等になる場合、JSONを永続Formatにするかは未決定。

---

# 42. Canonical Formatを特定Frameworkに合わせない

[DECIDED]

Canonical AI-Ready FormatをSemanticaやNeo4j専用Schemaにしない。

Projectが所有する中立Schemaを持ち、必要に応じてAdapterで変換する。

---

# 43. Provenanceは必須

[DECIDED]

Derived Knowledgeには可能な限りOriginal Source Mappingを持たせる。

最低候補：

- Source Path / Location
- Source Version
- Git Commit
- Sheet / Page / Slide
- Row / Cell / Range
- Extraction Method
- Transformer Version
- Extracted Date

---

# 44. Excel Provenance

[PROVISIONAL]

Excelでは必要に応じて、

- Workbook
- Sheet
- Row
- Column
- Cell Range

まで戻れることを目標とする。

TestCase等では特に重要。

---

# 45. PowerPoint Provenance

[PROVISIONAL]

PowerPointでは、

- File
- Slide Number
- Shape IDまたはText Region

等をSource Mapping候補とする。

---

# 46. PDF Provenance

[PROVISIONAL]

PDFでは、

- File
- Page
- Text Region

等をSource Mapping候補とする。

---

# 47. Source-to-Derived Mapping

[DECIDED]

OriginalとDerivedの対応関係を明示的に管理する。

DerivedからOriginalへ戻れるだけでなく、

Originalから、

> どのDerived Knowledgeへ影響するか

も追えることが望ましい。

---

# 48. One Source to Many Knowledge

[DECIDED]

一つのDocumentから複数Knowledge Objectが生成されることを前提にする。

例：

一つのDesign Excel  
→ Function A  
→ Function B  
→ Table C  
→ Business Rule D

Source FileとKnowledge Objectを一対一にしない。

---

# 49. Many Sources to One Knowledge

[DECIDED]

一つのKnowledgeが複数Sourceによって裏付けられる場合もある。

例：

Current Specification  
← Design  
← Test  
← Code  
← Release

複数Evidenceを持てる構造にする。

---

# 50. Current / Historical

[DECIDED]

Document Ingest時にCurrent / Historical判定に利用できる情報を抽出する。

候補：

- Version
- Release
- Effective Date
- File Name
- Directory
- Git History
- Approval State

単純に更新日時だけでCurrentを決めない。

---

# 51. Current判定

[OPEN]

Current判定の最終Ruleは対象Repository確認後に定義する。

AIが推測だけでCurrentを確定しない。

---

# 52. Document Version

[PROVISIONAL]

Document VersionのSource候補：

- File Name
- Internal Version
- Git Commit
- Sheet Metadata
- Release Number

複数Version Sourceが矛盾する場合、Conflictとして扱う。

---

# 53. Conflict Detection

[PROVISIONAL]

Ingest時に、既存KnowledgeとのConflictを検出する。

例：

- 同一Functionに異なる仕様
- DesignとTestのExpected Resultが異なる
- Current CodeとCurrent Designが異なる

自動的に最新情報へ上書きしない。

---

# 54. Duplicate Detection

[PROVISIONAL]

異なるFileが同一内容・同一Knowledgeを表す場合がある。

Duplicate候補判定：

- File Hash
- Title
- Content Similarity
- Stable ID
- Same Requirement ID
- Human Mapping

自動Mergeは慎重に行う。

---

# 55. Stable ID

[PROVISIONAL]

Derived KnowledgeはFile Pathだけに依存しないStable IDを持つことを検討する。

Rename / Moveで別Knowledgeとして再生成されることを避ける。

---

# 56. ID生成

[OPEN]

候補：

- Existing Business ID
- Requirement ID
- Test Case ID
- Deterministic Hash
- UUID + Mapping
- Composite Key

Document Typeごとに方式が異なる可能性がある。

---

# 57. Transform Version

[DECIDED]

AI-Ready Knowledgeには、どのTransformer Versionで生成されたかを残す。

Parser / Extraction Rule変更時に再生成対象を判断できるようにする。

---

# 58. Schema Version

[PROVISIONAL]

Intermediate RepresentationやCanonical Knowledge FormatにSchema Versionを持たせる。

Schema変更時のMigration / Rebuildを可能にする。

---

# 59. Incremental Processing

[DECIDED]

全Documentを毎回再処理するのではなく、Git Diff等を利用したIncremental Processingを基本方向とする。

---

# 60. Incremental Processingの候補Flow

[PROVISIONAL]

1. Last Indexed Commitを取得
2. Git Diffを取得
3. Added / Modified / Deleted / Renamedを分類
4. Document Typeを判定
5. 対象だけParse / Transform
6. Related Knowledgeを更新
7. Graph / Indexを更新
8. Processing Logを保存

---

# 61. New File

[DECIDED]

New Fileを検出した場合、

- Classification
- Security Check
- Parse
- Transform
- Validate
- Index

を実行する。

---

# 62. Modified File

[DECIDED]

Modified Fileでは、既存Derivedとの差分を確認できることが望ましい。

全KnowledgeをDelete / Recreateするか、Semantic Diffを利用するかはPoC後に判断する。

---

# 63. Deleted File

[PROVISIONAL]

Original削除時にDerivedを単純削除するとは限らない。

Historical Evidenceとして必要な場合、

- deprecated
- source_deleted
- historical

として残す可能性がある。

---

# 64. Renamed / Moved File

[PROVISIONAL]

Git Rename DetectionやStable IDを利用して、Renameを新Documentと誤認しないようにする。

---

# 65. Semantic Diff

[FUTURE]

Documentの意味上の変更を検出することを検討する。

例：

- Expected Result変更
- Requirement追加
- Meeting Decision変更
- Test Condition変更

単純Text Diffだけでは把握しにくい変更を対象とする。

---

# 66. Transformation Log

[DECIDED]

Ingest処理結果を記録する。

候補：

- Source
- Started At
- Completed At
- Parser
- Transformer Version
- Result
- Warning
- Error
- Generated Knowledge Count
- Generated Relation Count
- Review Required

---

# 67. Failure Visibility

[DECIDED]

変換に失敗したDocumentを黙ってIndexから除外しない。

明示する。

例：

- Parse Failed
- Unsupported Format
- Access Denied
- Security Blocked
- Low OCR Quality
- Relation Extraction Failed

---

# 68. Partial Success

[DECIDED]

一部Parseできた場合も、完全成功として扱わない。

例：

- Text extracted
- Diagram not parsed
- Comments unavailable

等をWarningとして残す。

---

# 69. Quality Gate

[PROVISIONAL]

AI-Ready KnowledgeをIndexへ公開する前に、Quality Gateを設けることを検討する。

候補：

- Source Mappingあり
- Document Typeあり
- Required Metadataあり
- Security Check済み
- Parser Errorなし
- Schema Validation成功

重要KnowledgeではHuman ReviewもGateに含める。

---

# 70. Validation

[DECIDED]

以下をValidateする。

- Schema
- ID
- Source Reference
- Required Field
- Relation Type
- Security Classification
- Provenance

Invalid Knowledgeを通常Knowledgeと同列に検索させない。

---

# 71. Human Review対象

[PROVISIONAL]

すべてのDerivedをHuman Reviewすることは現実的でない。

Review優先候補：

- Current Specification
- Historical Agreement
- Responsibility Evidence
- Meeting Decision
- Business Rule
- AI Inferred Relation
- Conflict

---

# 72. Auto-Accept候補

[PROVISIONAL]

機械的に確認できる情報はHuman Review負荷を下げる。

例：

- File Path
- Git Commit
- Code Symbol
- Static CALLS Relation

ただしParser品質を検証してから決定する。

---

# 73. Context Budget

[DECIDED]

AI-Ready化した全Textを毎回Codexへ渡さない。

Case Retrievalで必要部分だけ選択する。

Chunking / SummarizationはContext Selectionのために利用する。

---

# 74. Chunking

[PROVISIONAL]

Document TypeごとにChunk Ruleを変える。

## Design

Section / Feature単位。

## Test Specification

Scenario / Test Case単位。

## Meeting

Topic / Decision単位。

## Inquiry

Issue / Investigation / Conclusion単位。

固定文字数Chunkだけにしない。

---

# 75. Excel Chunking

[OPEN]

Sheet / Table / Scenario / Rowのどれが適切かはGolden Sampleで決定する。

---

# 76. PowerPoint Chunking

[PROVISIONAL]

Slide単位だけではなく、Slide Group / Topic単位も検討する。

---

# 77. Meeting Chunking

[PROVISIONAL]

Meeting MinutesではTopic / Decision単位が有力。

責任判断に使うため、発言文脈を失いすぎないようにする。

---

# 78. Summary

[PROVISIONAL]

長いDocumentにはSummaryを生成できる。

ただしSummaryをOriginal Evidenceの代替としない。

SummaryからOriginal Sectionへ戻れるようにする。

---

# 79. Search Index

[PROVISIONAL]

AI-Ready Knowledgeから以下のIndexを生成する可能性がある。

- Full Text Index
- Metadata Index
- Semantic / Vector Index
- Graph Index
- Code Index

すべてをPoC初期に導入する必要はない。

---

# 80. Vector Index

[OPEN]

Vector SearchはSimilar InquiryやRelevant Document候補に有用な可能性がある。

ただしPoCでは必須としない。

---

# 81. Graph Update

[DECIDED]

Document Transformationで新しいRelationが生成された場合、Graph / Relation Indexへ反映する。

Graph Storageは`12_RUNTIME_AND_STORAGE.md`で決定する。

---

# 82. Human Curated Knowledge

[DECIDED]

CodeやDocumentから再生成できないHuman Curated Knowledgeを区別する。

例：

- Business Mapping
- Responsibility Scope
- Corrected Relation
- Reviewed Summary

Rebuildで失わないようにする。

---

# 83. Generated KnowledgeとCurated Knowledge

[DECIDED]

再生成時には、

- Generated
- Extracted
- Inferred
- Curated

を区別する。

Generatedを再生成してもCuratedを上書きしない。

---

# 84. Existing Inquiry Folder

[OPEN]

既存問い合わせFolderを実査後、Ingest方式を決める。

候補：

- Folder単位でCase化
- Metadataだけ生成
- Investigation Fileを抽出
- Codex Resumeと統合
- Past Inquiry Indexのみ作る

既存構造を先に変更しない。

---

# 85. Past Codex Resumeとの統合

[PROVISIONAL]

既存問い合わせについて、Inquiry FolderよりCodex Resumeに詳細な調査履歴が残っている場合がある。

過去調査Knowledgeを整備する際は、

- Existing Inquiry Folder
- Related Codex Resume
- Final Customer Response

を比較し、必要なPersistent Investigation Knowledgeを作ることを検討する。

---

# 86. Resumeからの自動抽出

[OPEN]

Codex Resumeから、

- Sources Checked
- Technical Cause
- Open Questions

等を自動抽出できるかは、実際のSession参照機能・Format確認後に判断する。

Resumeを直接Canonical Knowledgeにはしない。

---

# 87. AI-Ready KnowledgeのGit管理

[OPEN]

Derived KnowledgeをGit Commitするかは未決定。

利点：

- Diff Review
- History
- Audit
- Human Review

欠点：

- Repository Size
- Generated Noise
- Sensitive Derived Data
- Frequent Changes

PoCで評価する。

---

# 88. Security上Gitへ残せないDerived

[DECIDED]

OriginalをGitへ置けない情報は、Derived Summaryであっても無条件にGitへ保存しない。

Derivedからセンシティブ情報が復元できる可能性を考慮する。

---

# 89. Local RuntimeのみのDerived

[PROVISIONAL]

Security上必要であれば、一部KnowledgeをLocal Runtime Indexにのみ保持する方式も許容する。

ただしPersistent Case Knowledgeとの境界を明確にする。

---

# 90. Semanticaの利用候補

[PROVISIONAL]

Semanticaを採用する場合、以下の領域で利用可能性を評価する。

- File Ingest
- Parse
- Normalize
- Entity Extraction
- Relation Extraction
- Provenance
- Conflict
- Deduplication

ただし、

Original  
→ Semantica Internal Data

をProjectの唯一のCanonical Modelにはしない。

---

# 91. Semantica Adapter方針

[PROVISIONAL]

候補Architecture：

Original  
→ Parser / Semantica  
→ Project Normalized Intermediate  
→ Project Domain Transformer  
→ Project AI-Ready Knowledge  
→ Graph / Index

Semanticaを交換可能にする。

---

# 92. Golden Sample First

[DECIDED]

本Document Ingest設計で最重要なのは、抽象Schemaを先に完成させることではない。

対象Repositoryから実際の代表Documentを一つ選び、

> このDocumentをCodexが問い合わせ調査で使うために、どのOutputが必要か

を先に手作業で定義する。

これをGolden Sampleとする。

---

# 93. Golden Sample候補

[PROVISIONAL]

第一候補：

- 実際の問い合わせに関連するExcel Test Specification

または、

- Design Document
- Existing Inquiry Folder

対象Repository確認後に選ぶ。

---

# 94. Golden Sampleで手作業定義するOutput

[DECIDED]

Golden Sampleでは、最低限以下を手作業で設計する。

- Document Type
- Extracted Content
- Metadata
- Provenance
- Knowledge Objects
- Relations
- Current / Historical
- Security Classification
- Review State

これをParser / Transformer実装の契約とする。

---

# 95. Golden Sampleで確認すること

1. Originalの重要情報を失っていないか
2. Source Locationへ戻れるか
3. Codexが検索しやすいか
4. Case調査で利用できるか
5. Graph Relationを生成できるか
6. Human Reviewしやすいか
7. Original変更時に再生成できるか

---

# 96. AI-Ready Conversion Contract

[PROVISIONAL]

Golden Sample確定後、Document TypeごとにConversion Contractを定義する。

候補項目：

- Supported Source
- Required Metadata
- Parsing Rule
- Chunking Rule
- Security Rule
- Extracted Knowledge Type
- Relation Rule
- Provenance Rule
- Validation Rule
- Review Rule
- Failure Policy

---

# 97. Test Specification Conversion Contract

[OPEN]

対象RepositoryのTest Specification確認後に定義する。

---

# 98. Design Document Conversion Contract

[OPEN]

対象RepositoryのDesign形式確認後に定義する。

---

# 99. Inquiry Conversion Contract

[OPEN]

Existing Inquiry FolderとCodex Resumeの実態確認後に定義する。

---

# 100. Meeting Conversion Contract

[OPEN]

Security / Management確認後に定義する。

---

# 101. Conversion Failure Policy

[DECIDED]

Conversionに失敗した場合、

- Originalは変更しない
- Existing Derivedを無条件に削除しない
- Failureを記録する
- Stale状態を明示する
- Human Review候補にする

Silent Failureを禁止する。

---

# 102. Stale Knowledge

[PROVISIONAL]

Originalが更新されたがDerived生成に失敗した場合、

`stale`

状態を持たせることを検討する。

古いDerivedをCurrentとして無条件に利用しない。

---

# 103. Unsupported Document

[DECIDED]

未対応Formatは無理に処理しない。

Unsupportedとして記録し、

- Manual Review
- Future Parser
- External Reference

のいずれかを選べるようにする。

---

# 104. Document IngestのObservability

[PROVISIONAL]

Developerが以下を確認できることが望ましい。

- Last Scan
- Changed Files
- Converted Files
- Failed Files
- Warning
- Needs Review
- Generated Knowledge
- Stale Knowledge

詳細UIは`13_UI_AND_DEVELOPER_EXPERIENCE.md`で扱う。

---

# 105. PoCで実装すべき最小Pipeline

[PROVISIONAL]

PoCでは以下程度から開始する。

1. Golden Sample Source取得
2. Document Type判定
3. Parse
4. Normalized Representation生成
5. AI-Ready Knowledge生成
6. Provenance付与
7. Validation
8. Work Item Retrievalから利用

Security確認が必要なSourceは対象外にする。

---

# 106. PoCで実装しなくてよいもの

PoC初期では以下を必須としない。

- 全Office Format完全対応
- Full OCR Pipeline
- 全PowerPoint Diagram解析
- Column Level Data Lineage
- Semantic Diff完全実装
- Vector DB
- 全Document自動Review
- 全Meeting Minutes Ingest
- Production Scale Pipeline
- 利用者向けFile Classification / Masking
- Token Vault / Detokenization / In-app Original Reconstruction

---

# 107. PoC Acceptance観点

Document Ingest PoCでは以下を確認する。

- Originalを変更せず変換できる
- AI-Ready OutputからOriginalへ戻れる
- Case調査で必要部分を取得できる
- Test / Design等の意味構造を保持できる
- Relationを生成できる
- Transformation Errorを検出できる
- Human Review Stateを持てる
- 再生成できる

---

# 108. Document IngestのAnti-Patterns

## Office → Markdownで完了

構造・Provenanceを失う。

## All Files First

必要性を確認せずRepository全体を変換する。

## No Source Mapping

AI要約からOriginalへ戻れない。

## AI Extraction = Verified

AI抽出を確定仕様として保存する。

## Security After Ingest

センシティブ情報をAIへ渡した後でMaskする。

## Latest File = Current

更新日時だけでCurrentを決める。

## Silent Parse Failure

変換失敗を利用者へ見せない。

## Framework-Owned Canonical Model

Semantica等の内部形式をProject正本にする。

---

# 109. Current Open Questions

[OPEN]

## Existing File Formats

対象Repository実査後に確認。

## Test Specification Structure

Sheet / Row / Scenario粒度。

## Design Document Structure

Excel / PPT / Word等の比率。

## Intermediate Representation Schema

正式Schema。

## Canonical AI-Ready Format

`content.md` / `metadata.yaml` / `relations.json`採用可否。

## Stable ID

生成方式。

## Current Detection

Rule。

## Semantic Diff

必要性と方式。

## Meeting Minutes

Codex / Git / Repository利用可否。

## Derived Git Storage

Commit範囲。

## Semantica

採用範囲。

---

# 110. 後続ドキュメントへの引き継ぎ

## `09_CASE_INVESTIGATION_WORKFLOW.md`

- CaseでどのKnowledgeを取得するか
- Codex SessionからPersistent Knowledgeへの保存
- Sources Checked
- Human Review

## `10_AGENT_AND_SKILL_ARCHITECTURE.md`

- Ingest Skill
- Parse Skill
- Validate Skill
- Knowledge Extraction Skill

## `11_SECURITY_AND_GOVERNANCE.md`

- Classification
- Masking
- Meeting Minutes
- Customer Data
- Codex Access Policy

## `12_RUNTIME_AND_STORAGE.md`

- Derived Storage
- Runtime Index
- Rebuild
- Incremental Update
- Transformation Log

## `13_UI_AND_DEVELOPER_EXPERIENCE.md`

- Ingest Status
- Conversion Failure
- Review Queue
- Provenance View

---

# 110.1 2026-08-30 Data Lifecycle Refinement

[DECIDED]

PoCではOrganization / AdministratorがAI利用を事前承認したSourceだけを登録対象とする。利用者にFile単位のClassificationやMasking判断を求めず、未承認SourceはIngestしない。Masking、Token Vault、Detokenization、画面表示時の原本復元はProduction向けの将来検討とする。

File登録は、Managed StorageへのUpload、既存Repository FileをCopyしない登録、External Source Referenceの3方式を区別する。Data StateはOriginal Source、Normalized Intermediate、Persistent Knowledge、Runtime Derived Index、System-generated Artifactに分ける。

更新操作はMetadata / Relation更新、Version / Replace、Stable IDを維持したMove / Rename、Work ItemへのLink / Unlink、Archive / Restore、Runtime Reindex / Rebuild、影響Preview付きPermanent Delete候補として明示し、単一の曖昧な「削除」は提供しない。

System-generated Artifactは内容を自動複製せず、保存場所、Checksum、生成元Execution、Input、Status、Retentionを既定で記録する。Human Review後に重要な生成物だけEvidenceへ昇格する。業務上意味のある流れは `UserAction -> Execution -> Input/OutputArtifact` として追跡する。

# 111. Design Decision Summary

## [DECIDED]

- Originalを置き換えない
- Officeから直接Markdownへ落とすだけにしない
- Normalized Intermediate Representationを検討する
- Physical FormatとBusiness Document Typeを分離する
- SecurityをAI利用前に適用する
- AI抽出を確定Knowledgeとして扱わない
- Provenanceを必須とする
- SourceとDerivedをMappingする
- Incremental Processingを基本方向とする
- Failureを隠さない
- Human Curated Knowledgeを再生成で失わない
- Codex Sessionを直接Canonical Knowledgeにしない
- Golden Sampleを先に作る
- 特定FrameworkへCanonical Modelを従属させない

## [PROVISIONAL]

- Intermediate Representation
- AI-Ready Canonical Format
- Stable ID
- Chunking
- Semantic Diff
- Semantica Adapter
- Derived KnowledgeのGit管理

## [OPEN]

- Meeting Minutesの取込方式
- Existing Test粒度
- Existing Design形式
- Current判定Rule
- Stable ID方式
- Canonical Format
- Security Classification
- Git Storage範囲

---

# 112. Document Ingest and Transform Statement

> 本ProjectのDocument Ingestは、AI利用承認済みのExcel、Word、PowerPoint、PDF等を単純にMarkdown化する処理ではなく、Originalを正式Evidenceとして維持したまま、Format固有情報をNormalized Intermediate Representationへ変換し、Domain Transformation、Relation Extraction、Provenance、Validationを経てAI-Ready Knowledgeを生成するPipelineとして設計する。PoCではFileごとのClassificationやMaskingを利用者へ要求せず、未承認Sourceを入口で除外する。Original、Intermediate、Persistent Knowledge、Runtime Index、System-generated Artifactを区別し、すべてのDerived Knowledgeは可能な限りOriginalへ戻り再生成できるようにする。対象Repository全体を一括変換せず、まずGolden Sampleを用いてConversion Contractを確定し、その後Document Typeごとに拡張する。

## 112.1 IaC Ingest and Graph Transform（2026-08-30）

[DECIDED]

Document / Code Ingestの対象へ、承認済みのTerraform HCL、Module、Provider Configuration、Plan Summary、State Metadata、Drift Resultを追加する。抽出候補はResource Address、Type、Module Path、Dependency、Network接続、Compute、Database、IAM Role参照、Source Location、Environment、Plan / Drift Stateである。Credential、Secret値、Sensitive Output、State内の機密Propertyは抽出・表示しない。変換時にFunctionをSystemへ潰さず、Function、System、Infrastructure / IaCの別NodeとBridge Relationを生成する。Vertical StackはIngest Outputではなく、生成されたRelationを用いるPresentation Projectionとする。
