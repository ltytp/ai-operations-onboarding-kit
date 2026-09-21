# AI-Ready Operations Repository / Codex App
## 09. Case Investigation Workflow

**File Name:** `09_CASE_INVESTIGATION_WORKFLOW.md`  
**Status:** Draft  
**Document Role:** Inquiry / Case Investigation Workflow / Human Review / Persistence  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、問い合わせ等のCaseをどのような手順・状態・判断単位で調査するかを定義する。

本Projectで最も重要なUse Caseは、運用保守における問い合わせ調査である。

本Workflowでは、

- 問い合わせメールをそのままInputとする
- CodexでRepository内を調査する
- 必要に応じてNotebookLM等のExternal Evidenceを確認する
- Technical CauseとSpecification / Responsibility Assessmentを分離する
- Sources Checked / Not Checkedを記録する
- Missing Knowledgeを明示する
- Human Reviewを行う
- Codex Sessionだけに調査結果を残さない
- Human Review後の調査成果をPersistent Investigation Knowledgeとして保存する

ことを基本とする。

---

# 2. Case Workflowの基本思想

[DECIDED]

Case Workflowは、

> AIが最終回答を一回生成する処理

ではない。

以下の一連の調査活動を管理する。

1. 問い合わせを理解する
2. 調査対象を決める
3. Technical Causeを調べる
4. Current Specificationを確認する
5. Historical Evidenceを確認する
6. Assessment Materialを整理する
7. Missing Knowledgeを確認する
8. Human Reviewする
9. Stakeholder向けOutputを作る
10. Investigation Knowledgeを永続化する

---

# 3. Primary Case Type

[DECIDED]

PoCのPrimary Caseは`Inquiry`とする。

将来的には以下へ拡張する。

- Incident
- Bug
- Change Request
- Release
- Investigation
- Operation Task

ただし本Workflowでは問い合わせ対応を中心に記述する。

---

# 4. Caseの入口

[DECIDED]

問い合わせCaseの主な入口は、

> 顧客・利用者から届いた問い合わせメール本文

とする。

人間があらかじめ専用Formへ整理・転記することを必須としない。

現在の運用と同様に、問い合わせメール本文をCodexへそのまま渡して調査を開始できることを基本とする。

---

# 5. Original Inquiryを保持する

[DECIDED]

AIが要約した問い合わせだけを保存せず、可能な範囲でOriginal Inquiryを参照可能にする。

Caseでは、

- Original Inquiry
- AI Structured Summary

を分ける。

AIの解釈ミスがあった場合、Originalへ戻れる必要がある。

---

# 6. Case Workflowの全体像

[DECIDED]

大きなWorkflowは以下とする。

1. Inquiry Intake
2. Symptom Understanding
3. Investigation Planning
4. Technical Investigation
5. Technical Cause Identification
6. Current Specification Check
7. Historical Evidence Check
8. Responsibility / Classification Assessment
9. Coverage / Missing Knowledge Check
10. Human Review
11. Stakeholder Output
12. Persistent Investigation Save
13. Knowledge Feedback

各Stepは必ず完全な直列ではない。

必要に応じて前のStepへ戻る。

---

# 7. Workflowは反復可能とする

[DECIDED]

問い合わせ調査では、

> 原因を調べたら新しい疑問が発生し、別のEvidenceを確認する

ことが普通である。

したがってWorkflowは一本道ではなく、反復可能とする。

例：

Technical Investigation  
→ Historical Evidence  
→ 新しい仮説  
→ Technical Investigationへ戻る

また、

Current Specification  
→ Test確認  
→ Design確認  
→ Code再確認

のような往復を許容する。

---

# 8. Workflow State

[PROVISIONAL]

Case Status候補：

- received
- understanding
- investigating
- awaiting_external_evidence
- assessing
- needs_human_review
- reviewed
- responding
- resolved
- closed
- blocked

物理Schemaは後続実装で決定する。

---

# 9. Step 1: Inquiry Intake

[DECIDED]

問い合わせメール本文をCodexへInputする。

この段階では、AIは問い合わせを勝手に技術原因へ変換せず、まず内容を整理する。

抽出候補：

- Who experienced it
- What happened
- Expected behavior
- Actual behavior
- Target date / period
- Error message
- Affected function
- Affected data
- Timing
- Business impact
- Attachments
- Unknown information

---

# 10. Inquiry Intakeで推測しすぎない

[DECIDED]

問い合わせ文に書かれていない内容を、事実として補完しない。

例えば、

> 画面に表示されない

だけで、

> DatabaseにRecordが存在しない

と確定しない。

これは調査仮説として扱う。

---

# 11. Step 2: Symptom Understanding

[DECIDED]

このStepの目的は、

> 利用者に何が起きたのか

を明確にすることである。

確認対象：

- Actual Behavior
- Expected Behavior
- Reproduction Condition
- Business Context
- Affected User
- Affected Function
- Affected Period
- Scope

---

# 12. Symptom Understandingの完了条件

[PROVISIONAL]

最低限以下が分かれば次へ進める。

- 何が起きているか
- 何が期待されているか
- 調査開始候補があるか

不足情報がある場合も、Missing Informationとして進行可能とする。

---

# 13. Step 3: Investigation Planning

[DECIDED]

問い合わせ内容から、どの領域を確認するか計画する。

候補：

- Screen
- API
- Batch
- Database
- Table
- File
- Source Code
- SQL
- Configuration
- Test
- Design
- Past Inquiry
- Historical Meeting
- Release
- Git History

すべてを毎回確認する必要はない。

---

# 14. Investigation Planは仮説である

[DECIDED]

最初のInvestigation Planを固定しない。

調査中に新しいRelationやEvidenceが見つかったら、Planを更新する。

---

# 15. Step 4: Technical Investigation

[DECIDED]

Technical Investigationでは、

> なぜその事象が発生したのか

を調べる。

ここでは主にRepository内の技術情報を利用する。

候補：

- Source Code
- API
- Batch
- Database
- SQL
- Data
- File
- Configuration
- External System Definition
- Existing Test
- Existing Inquiry

---

# 16. CodexをTechnical Investigationの中心にする

[DECIDED]

現在の運用と同様に、Repositoryから起動したCodexをTechnical Investigationの中心Toolとして利用する。

Codexには、

- Inquiry Text
- Current Repository
- Related Code
- Related Document

を利用して調査させる。

---

# 17. Codex Sessionに残るWorking History

[DECIDED]

調査中のCodex Session / Resumeには、

- 調査仮説
- 読んだFile
- 確認したCode
- Query
- Tool Execution
- 人間から追加されたContext
- 否定された仮説
- Open Questions

が残る可能性がある。

これは引き継ぎ時に重要なInvestigation Sourceとなる。

---

# 18. Codex Resumeを永続Knowledgeの代替にしない

[DECIDED]

Codex Resumeが詳細であっても、Case終了後の正式な調査成果をResumeだけに残さない。

ResumeはWorking History。

Persistent Investigation KnowledgeはHuman Reviewedな再利用対象。

この2つを分離する。

---

# 19. Technical Investigationの調査例

問い合わせ：

> 対象データが画面に表示されない

場合、例えば以下を確認する。

- Screenの表示条件
- API Request / Response
- Service Logic
- SQL
- Table Data
- Batch Processing
- Upstream File
- Aggregation Condition

調査経路はCaseによって異なる。

---

# 20. Layered Graph Viewの利用

[PROVISIONAL]

Graph機能が利用可能な場合、Technical Investigationで以下を利用する。

まず`Case + Current only + Depth 2`で調査範囲を確認し、問いに応じてLayer Viewを切り替える。

- Domain: 問い合わせの業務上の位置
- Function: 関係する機能分解
- System: 関係Component
- Data Flow: 値の流入・変換・出力
- Code: 実装・Call・Data Access
- Test: Expected Behaviorと検証結果
- Evidence / History: 現在仕様の根拠と過去Decision

Technical Traversal例：

- Screen → API
- API → Code Function
- Code Function → Table
- Table ← Batch
- Batch ← File

Graphは調査候補を見つけるために利用する。

GraphにRelationがあるだけで原因を確定しない。

---

# 21. Step 5: Technical Cause Identification

[DECIDED]

Technical Investigationの結果から、

> 技術的に何が原因で事象が発生したか

を整理する。

Technical CauseはSpecification Classificationとは別に保持する。

例：

- Record未生成
- Filterによる除外
- Batch未実行
- Input Data不足
- Mapping Error
- Configuration Error

---

# 22. Technical CauseのEvidence

[DECIDED]

Technical CauseにはEvidenceを紐付ける。

候補：

- Code
- SQL
- Data
- Log
- Test
- Reproduction Result

AIの説明文だけをEvidenceとしない。

---

# 23. Technical Causeが未確定の場合

[DECIDED]

原因が分からない場合、

`unknown`

または

`needs_more_investigation`

として扱う。

AIがもっともらしい原因を確定しない。

---

# 24. Step 6: Current Specification Check

[DECIDED]

Technical Causeが分かった後、

> その挙動がCurrent Specificationとして正しいか

を確認する。

確認候補：

- Current Design
- Current Test Specification
- Operation Manual
- Current Code
- Release Information
- Past Inquiry

---

# 25. Current Codeだけで仕様を確定しない

[DECIDED]

「現在Codeがそうなっている」という事実と、

「それが正しい仕様である」

ことを分ける。

CodeはCurrent BehaviorのEvidenceにはなるが、Specificationの唯一のEvidenceではない。

---

# 26. Test Specificationの利用

[DECIDED]

Test Specificationは、

> 過去にどの条件・Expected Resultを仕様として確認していたか

を判断する重要Evidenceとして扱う。

関連Test Caseが存在する場合、確認対象とする。

---

# 27. Step 7: Historical Evidence Check

[DECIDED]

Current Specificationだけで判断できない場合、開発当時のEvidenceを確認する。

候補：

- Requirement
- Old Design
- Old Test
- Meeting Minutes
- QA
- Release History
- Git History
- Past Inquiry

---

# 28. Historical Evidenceの主目的

[DECIDED]

Historical Evidenceを確認する主目的は、

> 開発時に何が要求され、何が議論され、何が合意されていたか

を確認することである。

特に責任範囲判断では、

- Customer Request
- Development Response
- Agreed Specification
- Missing Requirement
- Design Omission

を洗い出す。

---

# 29. NotebookLMの現在の位置付け

[DECIDED]

現時点では、過去の仕様・設計打ち合わせ・議事録等の確認にはNotebookLMを利用している。

したがってHistorical Evidence Checkでは、

- Codex調査と並行
- Technical Cause判明後
- Current Specification確認後

など、必要なタイミングでNotebookLMを利用する。

固定順序にはしない。

---

# 30. CodexとNotebookLMは並行利用可能

[DECIDED]

現在の実運用では、CodexとNotebookLMは以下のように役割が異なる。

Codex：
- Repository
- Code
- Test
- Current Document

NotebookLM：
- Meeting Minutes
- Historical Discussion
- Historical Specification

人間が両方のEvidenceを統合してAssessmentする。

将来は可能な範囲で一元化を目指す。

---

# 31. Meeting Minutes確認の目的

[DECIDED]

Meeting Minutesを確認する主目的は、

> 今回事象に関係する仕様が、開発当時どのように顧客側と開発側で合意されたか

を確認することである。

Meeting Minutesを単なる参考資料として扱わない。

---

# 32. External Evidence Check

[DECIDED]

Repository外Evidenceを人間が確認した場合、その事実をCaseへ残す。

候補：

- Source Type
- Source Title
- Date
- Checked By
- Summary
- Related Topic
- Access Restriction
- Original Reference

OriginalをRepositoryへ保存できない場合でも、確認したEvidenceの存在を追跡可能にする。

---

# 33. External Evidenceが未確認の場合

[DECIDED]

関連するHistorical Evidenceが存在する可能性があるが未確認の場合、

- Not Checked
- Access Restricted
- Source Unknown

等として明示する。

未確認状態で責任判断を確定しない。

---

# 34. Step 8: Classification / Responsibility Assessment

[DECIDED]

Technical CauseとCurrent / Historical Evidenceをもとに、

> 今回事象をどのように扱う可能性が高いか

を整理する。

候補分類：

- Current Specification
- Implementation Bug
- Specification Omission
- New / Additional Requirement
- Operation Cause
- Data Cause
- Historical SE / Individual Handling Cause
- Unknown

---

# 35. ClassificationとResponsibilityを分ける

[DECIDED]

例えば、

> Implementation Bug

と判断されても、契約・費用・正式責任範囲が自動的に決まるとは限らない。

ClassificationとResponsibility Decisionを別に扱う。

---

# 36. Responsibility Assessment Material

[DECIDED]

AIは以下を整理する。

- Observed Fact
- Technical Cause
- Current Specification
- Historical Agreement
- Difference / Deviation
- Evidence
- Missing Evidence
- AI Assessment

Humanが最終的な責任範囲を判断する。

---

# 37. 開発時合意の代表パターン

[PROVISIONAL]

## Pattern A: 合意済み仕様

顧客・開発間で仕様が合意され、Design / Testも整合している。

→ Current Specification / Additional Requirement候補。

## Pattern B: 合意済みだが実装不一致

仕様は合意済みだがCodeが異なる。

→ Implementation Bug候補。

## Pattern C: 必要条件が提示されたが設計から漏れた

→ Specification / Design Omission候補。

## Pattern D: 開発時に検討自体されていない

→ Responsibility / Requirement Scopeの追加検討が必要。

## Pattern E: SE個別対応によるDeviation

→ Historical Individual Handling起因候補。

これらは自動判定Ruleではなく、Assessment補助の代表例。

---

# 38. Step 9: Coverage Check

[DECIDED]

回答作成前に、

> 今回何を確認したか

を整理する。

候補Knowledge領域：

- Business
- Function
- System / Data
- Implementation
- Test
- Current Design
- Past Inquiry
- Historical Evidence
- Responsibility

---

# 39. Sources Checked

[DECIDED]

Caseに実際に確認したSourceを残す。

例：

- Source Code
- Test Specification
- Past Inquiry
- SQL Result
- Meeting Summary

---

# 40. Sources Not Checked

[DECIDED]

関連候補だが確認していないSourceを残す。

理由候補：

- Access Restricted
- Not Available
- Not Found
- Out of Scope
- Not Required
- Time Constraint

---

# 41. Missing Knowledge

[DECIDED]

判断に必要だが取得できなかったKnowledgeを明示する。

例：

- 開発時のMeeting Minutes未確認
- Old Design未発見
- Release Decision不明
- Historical Test不存在

Missing KnowledgeはCase Outputの一部とする。

---

# 42. Open Questions

[DECIDED]

解決していないQuestionを残す。

例：

- 顧客からこの条件は明示されていたか
- このChangeはどのReleaseで入ったか
- このCode変更の理由は何か

CaseをClosedにしても、Open QuestionをHistorical Knowledgeとして残す場合がある。

---

# 43. Investigation Completion Criteria

[PROVISIONAL]

CaseをHuman Reviewへ進める最低条件候補：

- Symptomが整理されている
- Technical CauseまたはUnknown理由が整理されている
- Current Specification確認状況が分かる
- Evidenceが紐付いている
- Sources Checkedが分かる
- Missing Knowledgeが分かる
- Responsibility Assessment Materialが整理されている

すべてのSource確認完了を必須にはしない。

---

# 44. Step 10: Human Review

[DECIDED]

以下をHumanがReviewする。

- Symptom
- Technical Cause
- Current Specification
- Evidence
- Historical Evidence
- Missing Knowledge
- Classification
- Responsibility Assessment Material
- Customer Response Draft

---

# 45. Human Reviewが必須な事項

[DECIDED]

特に以下はHuman Approvalを必要とする。

- Current Specificationの重要判断
- Historical Agreementの解釈
- Responsibility Scope
- Contract Interpretation
- Cost / Additional Development判断
- Customerへの正式な責任表現

---

# 46. Human Review Result

[PROVISIONAL]

候補：

- approved
- approved_with_changes
- needs_more_investigation
- rejected
- blocked

修正理由を記録できることが望ましい。

---

# 47. Human CorrectionをKnowledgeとして利用する

[DECIDED]

AIのAssessmentがHuman Reviewで修正された場合、

> どこが修正されたか

を残すことを検討する。

これにより、

- Prompt / Agent改善
- Knowledge品質改善
- Future Retrieval改善

に利用できる。

---

# 48. Step 11: Stakeholder Output

[DECIDED]

Human Review後、説明相手に応じてOutputを生成する。

Knowledgeは共通。

PresentationをStakeholderごとに変える。

---

# 49. End User向けOutput

[DECIDED]

主な内容：

- 何が起きたか
- 業務影響
- 現在利用可能か
- 必要な操作
- 回避方法
- 対応予定

技術詳細を必要以上に含めない。

---

# 50. Customer System / Management向けOutput

[DECIDED]

主な内容：

- 発生事象
- Technical Cause
- Current Specification
- Historical Agreement
- Responsibility Assessment Material
- Fix / Change Requirement
- Additional Development候補
- Evidence

正式責任表現はHuman承認後とする。

---

# 51. Developer向けOutput

[DECIDED]

主な内容：

- Reproduction
- Technical Cause
- Code
- SQL
- Data Flow
- Affected Components
- Test Scope
- Fix Candidate
- Related Past Inquiry

---

# 52. Final ResponseとInvestigation Recordを分ける

[DECIDED]

顧客へ送るFinal Responseだけでは、将来調査に必要な技術詳細が不足する可能性がある。

したがって、

- External / Customer Response
- Internal Investigation Record

を分けて保存する。

---

# 53. Step 12: Persistent Investigation Save

[DECIDED]

Case終了前または終了時に、重要な調査内容をCodex Session外へ保存する。

これは本Workflowの必須要素とする。

---

# 54. Persistent Investigation Knowledgeの目的

[DECIDED]

目的：

- Codex Session消失時にも調査成果を残す
- 別担当者へ引き継げる
- 次回Inquiryで検索できる
- Human Reviewedな結論を明確にする
- Working Historyと正式Knowledgeを分離する

---

# 55. Persistent Investigation Knowledge候補

[PROVISIONAL]

最低候補：

- Case ID
- Original Inquiry Reference
- Summary
- Symptom
- Expected Behavior
- Technical Cause
- Current Specification
- Evidence
- Sources Checked
- Sources Not Checked
- Historical Evidence
- Missing Knowledge
- Open Questions
- Assessment
- Human Review
- Final Decision
- Final Response
- Related Code
- Related Test
- Related Release
- Related Codex Session Reference

---

# 56. Persistent File Format

[OPEN]

候補：

- Single Markdown
- Markdown + YAML
- Markdown + JSON
- Existing Inquiry Folderへ追加
- Central Case Record

具体形式はExisting Repository確認後に決める。

---

# 57. Investigation Summary File

[PROVISIONAL]

人間とCodex双方が読みやすいSummaryとしてMarkdownを持つことは有力。

例候補：

- inquiry.md
- investigation.md
- decision.md
- response.md

ただしDirectory / File名は未決定。

---

# 58. Structured Case Metadata

[PROVISIONAL]

検索・Graph・Automation用にStructured Metadataを併用する可能性がある。

候補：

- Case ID
- Status
- Related Function
- Technical Cause Type
- Responsibility Status
- Review Status
- Dates

---

# 59. Codex Resume Reference

[PROVISIONAL]

Persistent Investigation Knowledgeから、利用可能であれば関連Codex Resume / Sessionを参照できることが望ましい。

ただしResumeが参照できなくなっても、Caseの重要結論が失われないようにする。

---

# 60. Resume内容をそのままコピーしない

[DECIDED]

Codex Session全体をそのままCase Recordとして保存することを基本としない。

理由：

- 冗長
- 誤仮説を含む
- Security情報を含む可能性
- Human VerifiedとAI Working Historyが混在
- 検索性が低い

必要な部分だけ整理してPersistent Knowledgeへ残す。

---

# 61. Investigation Step History

[PROVISIONAL]

将来的には、重要な調査Stepだけを構造化して残すことを検討する。

候補：

- Step
- Hypothesis
- Action
- Source
- Result
- Conclusion

すべてのAI思考過程を保存することを目的としない。

---

# 62. Rejected Hypothesis

[PROVISIONAL]

後で有用な場合、否定された主要Hypothesisを残す。

例：

> API側Filterが原因と仮定したが、対象DataはAPI Responseに存在したため否定。

同じ調査を繰り返すことを防げる可能性がある。

ただし詳細な内部推論を保存する必要はない。

---

# 63. Step 13: Knowledge Feedback

[DECIDED]

Case調査で新しく確認されたFact / Relationは、Human Review後にReusable Knowledgeへ反映する。

例：

- FunctionとTableのRelation
- Past Inquiryとの類似性
- Test Evidence
- Business Rule
- Data Flow
- Historical Decision

---

# 64. Case KnowledgeとGeneral Knowledgeを分ける

[DECIDED]

Case固有のFactと、他Caseでも使えるGeneral Knowledgeを分ける。

例：

Case固有：
- 2026-08-xxのRecordが存在しない

General：
- Batch XはTable Yを生成する

General Knowledgeへ昇格する場合はHuman Reviewを行う。

---

# 65. Knowledge Promotion

[PROVISIONAL]

CaseからGeneral Knowledgeへの昇格Flow：

1. Caseで新しいRelation / Fact発見
2. Evidence確認
3. Human Review
4. Existing KnowledgeとのConflict確認
5. General Knowledgeへ保存
6. Graph / Index更新

---

# 66. Case Closure

[PROVISIONAL]

CaseをClosedとする条件候補：

- Human Review完了
- Final Response確定
- Persistent Investigation Knowledge保存済み
- 必要なKnowledge Feedback完了
- Remaining Open Questions記録済み

---

# 67. Blocked Case

[DECIDED]

必要Evidenceへアクセスできず進められない場合、Blocked状態を許容する。

例：

- Meeting MinutesへのAccess待ち
- Customer Data待ち
- Production Log待ち
- Management Decision待ち

AIが無理にClosed扱いしない。

---

# 68. Reopen

[PROVISIONAL]

Closed Caseでも、

- New Evidence
- Customer Follow-up
- Similar Issue
- New Release

等で再Openできることを検討する。

---

# 69. Similar Past Case Retrieval

[DECIDED]

新しいCase開始時に、過去のPersistent Investigation Knowledgeを検索する。

検索候補：

- Same Function
- Same Error
- Same Table
- Same Batch
- Same Technical Cause
- Similar Inquiry Text
- Same Historical Decision

---

# 70. Past Caseをそのまま適用しない

[DECIDED]

類似Caseが見つかっても、

> 前回と同じ原因

と自動決定しない。

Past CaseはInvestigation Starting Pointとして利用する。

---

# 71. Existing Inquiry Folderの利用

[OPEN]

対象Repositoryにある既存問い合わせFolderを実査後、Workflowにどう統合するか決める。

候補：

- Existing FolderをCase Rootとする
- Metadata追加
- Central Case IndexからReference
- New Persistent Investigation File追加

---

# 72. Existing Codex Resumeの利用

[DECIDED]

過去問い合わせ引き継ぎ時に、利用可能であれば関連Codex Resume / Sessionを確認する。

特に、

- Inquiry FolderにFinal Resultしかない
- 調査Sourceが不明
- 原因到達経路が不明

場合に有用。

---

# 73. Existing ResumeからのMigration

[PROVISIONAL]

重要な過去Caseについて、ResumeからPersistent Investigation Knowledgeを作成するMigrationを検討する。

全Sessionを一括MigrationすることはPoCの必須要件としない。

---

# 74. Investigation Coverage Model

[PROVISIONAL]

Caseに以下のCoverageを持つことを検討する。

- Business
- Function
- System
- Data
- Implementation
- Test
- Design
- Historical Evidence
- Responsibility

State候補：

- checked
- partial
- not_checked
- not_applicable
- restricted

---

# 75. Coverageは完了率ではない

[DECIDED]

Coverageを単純なPercentageにしない。

重要なHistorical Evidenceが未確認なら、他領域が100%でも責任判断は不十分な場合がある。

---

# 76. Evidence Chain

[PROVISIONAL]

重要Assessmentについて、Evidence Chainを表示できることが望ましい。

例：

Observed Issue  
→ Technical Cause  
→ Current Design  
→ Test Evidence  
→ Historical Agreement  
→ Assessment

GraphとCase Recordの双方で表現可能とする。

---

# 77. Timeline

[PROVISIONAL]

Caseでは複数の時間を整理できることが望ましい。

例：

- Business Date
- Data Date
- Batch Execution
- Release
- Meeting
- Inquiry
- Investigation
- Answer

Technical TimelineとDecision Timelineを混同しない。

---

# 78. Runtime Timeline

[PROVISIONAL]

事象発生に関するTimeline。

例：

Input File受信  
→ Batch実行  
→ Table更新  
→ User操作  
→ Error発生

---

# 79. Historical Decision Timeline

[PROVISIONAL]

仕様成立に関するTimeline。

例：

Requirement  
→ Design Meeting  
→ Decision  
→ Implementation  
→ Test  
→ Release

---

# 80. Case Timeline View

[FUTURE]

UIではRuntime TimelineとHistorical Decision Timelineを必要に応じて並べて表示することを検討する。

---

# 81. Responsibility Assessment Timeline

[PROVISIONAL]

責任範囲判断で、

> いつ何が合意され、いつ実装されたか

が重要なため、Historical TimelineをAssessment Materialへ含めることを検討する。

---

# 82. Agent Architectureとの関係

[PROVISIONAL]

将来的にMulti-Agentを導入する場合、Workflow StepごとにAgent / Skillを割り当てる可能性がある。

例：

- Code Investigation
- Evidence Retrieval
- Timeline
- Responsibility Assessment
- Stakeholder Output
- Review

ただしWorkflow自体をAgent構成へ依存させない。

---

# 83. Workflow Orchestrator

[PROVISIONAL]

Main Agent / Orchestratorを導入する場合の役割候補：

- Current Stepを判断
- 必要Skillを選択
- Sources Checkedを統合
- Missing Knowledgeを管理
- Human Reviewへ渡す

詳細は`10_AGENT_AND_SKILL_ARCHITECTURE.md`で定義する。

---

# 84. WorkflowのHuman Override

[DECIDED]

人間はいつでも、

- 調査範囲変更
- Source追加
- Hypothesis修正
- Investigation再開
- Classification修正

を行えること。

AI Workflowを強制しない。

---

# 85. Security Checkpoint

[DECIDED]

Case調査中に新しいSourceへアクセスする場合、必要に応じてAccess Policyを確認する。

特に、

- Meeting Minutes
- Customer Information
- Production Data
- Contract Information

は自動参照しない可能性を考慮する。

---

# 86. Restricted Evidence

[DECIDED]

Evidenceが存在するがAIから参照不可の場合、

- Source Exists
- Access Restricted
- Human Check Required

として扱う。

Missing Evidenceと区別する。

---

# 87. Customer ResponseのSecurity

[PROVISIONAL]

Internal Investigation Recordの情報をそのままCustomer Responseへ出さない。

以下を除外・変換する可能性がある。

- Internal Comment
- Personal Information
- Internal Responsibility Discussion
- Sensitive Architecture Detail
- Credential
- Internal Cost Information

---

# 88. Review Agent

[FUTURE]

Customer Response作成前にReview処理を行い、

- Evidence不足
- 未確認の責任断定
- Conflict見落とし
- Stakeholderに不適切な表現
- Security Risk

を検出することを検討する。

---

# 89. Case FileのAuditability

[PROVISIONAL]

Persistent Investigation Knowledgeに、

- Created At
- Updated At
- Reviewed By
- Review Date
- Related Commit

等を持たせることを検討する。

---

# 90. CaseとGit

[PROVISIONAL]

Security上問題がなければ、Human ReviewedなCase KnowledgeをGit管理することで、

- 調査内容の変更履歴
- Review Diff
- Knowledge追加履歴

を追える可能性がある。

具体方針は`11` / `12`で決める。

---

# 91. Investigation Recordの変更

[DECIDED]

過去Case Knowledgeを修正する場合、元の判断を完全に消すのではなく、変更理由を追跡可能にすることが望ましい。

---

# 92. Case Version

[PROVISIONAL]

Case KnowledgeにVersionまたはRevisionを持つことを検討する。

例：

- Initial Investigation
- Customer Follow-up
- New Evidence
- Final Decision

---

# 93. PoCで実装するWorkflow範囲

[DECIDED]

PoCでは一件の実運用に近い問い合わせについて、最低限以下を成立させる。

1. Raw Inquiry Intake
2. Symptom Understanding
3. Repository Investigation
4. Technical Cause
5. Current Specification
6. Evidence
7. Sources Checked
8. Missing Knowledge
9. Human Review
10. Response Draft
11. Persistent Investigation Save

---

# 94. PoC Conditional Scope

[OPEN]

Historical Meeting Evidenceの直接利用は、Codex / Repository / Git利用可否の確認結果に依存する。

利用できない場合でも、

> Historical Evidence未確認

を正しく表現できることをPoC成功条件に含める。

---

# 95. PoCでは必須としないWorkflow

PoC初期では以下を必須としない。

- Fully Automated Agent Orchestration
- Automatic Responsibility Decision
- Automatic Customer Send
- Full Timeline UI
- Full Graph Visualization
- All Past Case Migration
- Automatic Meeting Ingest

---

# 96. Golden Case

[DECIDED]

PoCではGolden Sample Documentだけでなく、Golden Caseを一件選定する。

Golden Caseは、

- 実際に近いInquiry
- Code Investigationが必要
- Test / Document確認が必要
- 可能ならHistorical Evidence確認が必要

なものが望ましい。

---

# 97. Golden Caseで確認すること

1. Raw Emailから開始できるか
2. Codexが関連Codeを調査できるか
3. Related Documentを取得できるか
4. Technical CauseをEvidence付きで整理できるか
5. Current Specificationを確認できるか
6. Historical Evidenceの必要性を認識できるか
7. Sources Checkedを残せるか
8. Missing Knowledgeを残せるか
9. Human Reviewできるか
10. Persistent Investigation Knowledgeへ保存できるか
11. 次回検索できるか

---

# 98. Workflow Acceptance Criteria

PoC成功時、以下の問いに答えられる必要がある。

## Intake

問い合わせメール本文をそのままInputできたか。

## Investigation

人間が最初からFile Pathを指定しなくても関連Sourceへ到達できたか。

## Cause

Technical Causeを特定、または不明理由を明示できたか。

## Specification

Current Specificationとの比較ができたか。

## Evidence

判断根拠へ戻れるか。

## Historical Context

Historical Evidenceが必要かどうか判断できたか。

## Coverage

何を確認し、何を確認していないか分かるか。

## Human Review

責任・仕様判断を人間がReviewできたか。

## Persistence

Codex Session外へ調査成果を保存できたか。

## Reuse

次のInquiryから過去Caseを検索できる形になったか。

---

# 99. Workflow Anti-Patterns

## AI Answer First

Inquiryを受けてすぐに最終回答だけ生成する。

## Technical Cause = Bug

原因判明だけでBug判定する。

## Code = Specification

Codeだけで仕様確定する。

## NotebookLM Check = Optional Detail

責任範囲に重要なHistorical Evidenceを軽視する。

## Resume Only

調査成果をCodex Sessionのみに残す。

## Final Email Only

Customer Responseだけ保存し、Internal Investigationを残さない。

## No Sources Checked

AIが何を見たか分からない。

## Missing Evidence Hidden

Evidence不足でも結論を確定する。

## AI Responsibility Decision

人間承認なしで責任を断定する。

---

# 100. Current Open Questions

[OPEN]

## Case Physical Format

既存Inquiry Folderをどう利用するか。

## Persistent Investigation File

Markdown / YAML等の構成。

## Codex Resume Reference

どのようにSessionをCaseへ紐付けるか。

## Historical Evidence Integration

NotebookLM / Repository / External Referenceの方式。

## Human Review UX

CLI / Markdown / App UI等。

## Case Status Schema

具体値。

## Knowledge Promotion

Case KnowledgeからGeneral Knowledgeへの昇格方式。

## Final Response Storage

どこまで保存するか。

---

# 101. 後続ドキュメントへの引き継ぎ

## `10_AGENT_AND_SKILL_ARCHITECTURE.md`

- Workflow StepとAgent責務
- Orchestrator
- Code / Evidence / Timeline / Review Skill

## `11_SECURITY_AND_GOVERNANCE.md`

- External Evidence Access
- Meeting Minutes
- Customer Response
- Responsibility Approval
- Sensitive Case Data

## `12_RUNTIME_AND_STORAGE.md`

- Case File
- Codex Session
- Runtime State
- Git管理
- Persistent Investigation Knowledge

## `13_UI_AND_DEVELOPER_EXPERIENCE.md`

- Current Case
- Investigation Progress
- Sources Checked
- Missing Knowledge
- Human Review
- Stakeholder Output

## `15_POC_PLAN_AND_ACCEPTANCE_CRITERIA.md`

- Golden Case
- Workflow Test
- Success Metrics

---

# 102. Workflow Decision Summary

## [DECIDED]

- Raw Inquiry Emailを入口にする
- Workflowは反復可能
- CodexをTechnical Investigationの中心にする
- Technical CauseとSpecification Assessmentを分離する
- Historical Evidenceを責任判断の重要Evidenceとする
- NotebookLMを現状のExternal Evidence Sourceとして考慮する
- Codex ResumeをInvestigation Sourceとして利用する
- Resumeだけに調査成果を残さない
- Sources Checked / Not Checkedを記録する
- Missing Knowledgeを明示する
- Human Reviewを必須とする
- Customer ResponseとInternal Investigationを分離する
- Human Review後にPersistent Investigation Knowledgeを保存する
- Case結果を次のInquiryで再利用する

## [PROVISIONAL]

- Case Status
- Coverage Model
- Investigation Step History
- Rejected Hypothesis保存
- Case Version
- Knowledge Promotion Flow

## [OPEN]

- Physical Case Format
- Existing Inquiry Folder Mapping
- Codex Resumeとの具体的Link
- NotebookLM / Meeting統合方式
- Human Review UI
- Persistent File Format

---

# 103. Case Investigation Workflow Statement

> 本ProjectのCase Investigation Workflowは、問い合わせメール本文をそのまま起点としてCodexでRepository内のCode・Data・Test・Documentを調査し、Technical Causeを整理した上でCurrent SpecificationとHistorical Evidenceを照合し、Bug / Specification / Omission / Additional Requirement等のAssessment Materialを作成する。一件の調査ではSources Checked、Sources Not Checked、Missing Knowledge、Open Questionsを明示し、責任・契約・費用を含む最終判断はHuman Reviewを必須とする。Codex Resume / Sessionは詳細なWorking Historyとして引き継ぎに活用する一方、重要な調査成果はSessionのみに依存せず、Human Review後にPersistent Investigation Knowledgeとして外部Fileまたは承認済みStorageへ保存し、次回の問い合わせ調査へ再利用する。

## 103.1 Work Item Workflow Refinement（2026-08-30）

[DECIDED]

本Workflowは問い合わせCaseのGolden Flowを維持しつつ、上位概念をWork Itemへ拡張する。IntakeでPrimary Objectiveを決め、途中でSystem Discovery、Impact Analysis、Estimation、Stakeholder確認などをSecondary Objectiveとして追加できる。ObjectiveごとにChecklistとDeliverableは変えるが、Evidence、Sources Checked / Not Checked、Missing Knowledge、選択対象、Finding、Review Stateは共通Contextとして引き継ぐ。Upload、Execute、Approve、Export、Delete、ReprocessはUserActionとExecutionを分けて記録し、生成ArtifactはReview後に必要なものだけEvidenceへ昇格する。

## 103.2 Cross-Layer Investigation Flow（2026-08-30）

[DECIDED]

調査計画では、`Inquiry / Work Item → Objective → Domain / Function → System / Infrastructure → Code / Data Flow / Test → Evidence`のVertical StackをCoverage Checkとして使用する。Functionでは「何を提供するか」、Systemでは「どのComponentで実現・稼働するか」、Infrastructure / IaCでは「どのTerraform定義・Resourceへ配置されるか」を別の調査質問として扱う。障害・変更・影響分析では、必要に応じてTerraform Module、Resource、Plan、State Metadata、Drift ResultをSources Checkedへ追加する。詳細原因は各Flat Graphで追跡し、層の欠落はMissing Knowledgeとして残す。
