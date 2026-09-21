# AI-Ready Operations Repository / Codex App
## 02. Vision and Goals

**File Name:** `02_VISION_AND_GOALS.md`  
**Status:** Draft  
**Document Role:** Vision / Goals / Non-Goals  
**Last Updated:** 2026-08-30

---

# 1. このドキュメントの目的

本ドキュメントは、`01_BACKGROUND_AND_PROBLEM.md` で整理した運用保守上の問題に対して、

> このPoCおよび将来の仕組みで、どのような状態を実現したいか

を定義する。

本ドキュメントでは主に以下を整理する。

- Vision
- Target User
- Goals
- PoC Goals
- Future Goals
- Non-Goals
- Representative Use Cases
- Success Criteria

具体的な実装方式や製品選定は、後続の設計ドキュメントで扱う。

---

# 2. Vision

本プロジェクトのVisionは、

> 運用保守担当者が、開発当時の詳細な背景をすべて記憶していなくても、問い合わせや障害を起点として、業務・仕様・コード・データ・テスト・過去問い合わせ・設計時の合意・変更履歴など必要なEvidenceへ辿り、根拠を確認しながら自律的に調査・判断できる環境を作ること

である。

単にAIへ質問して回答を得ることを目的としない。

重要なのは、

> AIがなぜその回答に到達したかを、人間がRepository上または関連Knowledge Source上のEvidenceまで追跡できること

である。

---

# 3. 現在の問い合わせ調査の進め方

現在の問い合わせ調査では、問い合わせメールを受け取った後、まずその本文をほぼそのままCodexへ入力して調査を開始している。

現在の大まかな流れは以下である。

```text
問い合わせメール受信
        ↓
メール本文をCodexへそのまま入力
        ↓
CodexでRepository内を調査
        ├─ Source Code
        ├─ 現行仕様に関する資料
        ├─ テスト項目書
        ├─ 過去問い合わせ
        └─ その他Repository内資料
        ↓
技術的な事象・原因・現行仕様を整理
```

ただし、問い合わせによってはRepository内の情報だけでは判断できない。

特に、

- 開発当時の仕様検討
- 顧客との設計打ち合わせ
- 当時の合意内容
- 過去の仕様変更経緯

などは、現時点では主にNotebookLM側に存在している。

そのため、CodexによるRepository調査と並行して、または技術的な原因をある程度把握した後に、NotebookLMで過去資料を確認する。

```text
問い合わせメール
        ↓
CodexでRepository調査
        ↓
技術的原因・現行仕様の整理
        ↓
必要に応じてNotebookLMを確認
        ├─ 過去仕様
        ├─ 設計打ち合わせ議事録
        ├─ 顧客との合意内容
        └─ 開発時の経緯
        ↓
Codex側の調査結果と
NotebookLM側のEvidenceを人間が接続
        ↓
バグ / 仕様 / 責任範囲を整理
        ↓
利用者・顧客への回答を作成
```

実際にはCodexとNotebookLMの確認順序は固定ではなく、必要に応じて並行して進める。

例えば、

```text
                    ┌→ Codex
                    │   ├ Code
                    │   ├ Data
問い合わせメール ───┤   ├ Test
                    │   └ Repository内資料
                    │
                    └→ NotebookLM
                        ├ 過去仕様
                        ├ 議事録
                        └ 開発時の合意
```

のように、それぞれ異なるKnowledge Sourceを確認している。

現状では、最終的にこれらの情報を担当者自身が頭の中で接続し、

> 今回の事象は何が原因で、現行仕様上どのように扱うべきで、開発時の合意を踏まえるとどちらの責任範囲として整理すべきか

を判断している。

---

# 4. 目指す運用保守の状態

将来的には、この複数ツール・複数Knowledge Sourceを人間が毎回手動で接続する負荷を減らしたい。

目指す大きな流れは以下である。

```text
問い合わせ
↓
Caseとして整理
↓
必要な調査領域を特定
↓
関連Knowledge / Code / Evidenceを探索
↓
技術的原因を整理
↓
現行仕様と比較
↓
開発時の合意・過去Evidenceを確認
↓
責任範囲の判断材料を整理
↓
不足情報を明示
↓
人間が確認
↓
利用者・顧客へ説明
```

重要なのは、NotebookLMを単純に置き換えることではない。

現時点ではRepository内外に分散しているKnowledgeを、

> 一つの問い合わせ調査として関連付けて扱えること

を目指す。

---

# 5. AIの役割

[DECIDED]

本プロジェクトでは、AIを「最終判断者」としてではなく、

> 運用保守担当者が必要な情報を探索・整理・比較・説明するための調査支援者

として位置付ける。

AIに期待する主な役割は以下である。

- 問い合わせメール内容の整理
- 発生事象・期待動作の整理
- 調査開始点の提示
- 関連Knowledgeの探索
- Source Codeの調査
- Data Flowの追跡
- 過去問い合わせの検索
- Evidenceの抽出
- 現行仕様と過去情報の比較
- 矛盾・不足情報の検出
- Timelineの整理
- 調査結果の要約
- Stakeholderに応じた説明案の生成

---

# 6. 人間の役割

[DECIDED]

以下については、人間が最終的な責任を持つ。

- 調査結果の妥当性確認
- Evidenceの解釈
- 責任範囲の最終判断
- 契約上の判断
- 費用判断
- 顧客への正式回答
- Security上の判断
- Repository運用ルールの承認

AIによる推論と、人間が確認した事実を区別できる状態を目指す。

---

# 7. Primary Target User

本PoCのPrimary Userは、

> 対象システムの運用保守を担当するDeveloper / Engineer

とする。

特に、

- 開発当時の全経緯を把握していない
- 問い合わせ調査を担当する
- Source Codeを確認する
- データやBatch等を調査する
- テストやリリース作業を行う
- 顧客への技術説明を準備する

担当者を主な対象とする。

---

# 8. Secondary User

将来的には以下のUserも利用可能性がある。

- 新しく運用保守へ参加したDeveloper
- 開発担当者
- Team Lead
- Project Manager
- Reviewer
- System Analyst

ただしPoCでは、

> 非技術者向けの汎用AIツール

を作ることは主目的としない。

---

# 9. Goal 1: 問い合わせメールから調査を開始できる

現在の実運用では、問い合わせメール本文をそのままCodexへ入力して調査を開始している。

この使い方は、PoCでも重要な入口として維持したい。

将来的には、問い合わせメール等の文章から、

- 何が起きているか
- 利用者が何を期待しているか
- 対象業務
- 対象機能
- 調査開始候補
- 確認が必要なKnowledge Source

を整理できることを目指す。

つまり、人間が事前に問い合わせを構造化してからAIへ渡すことを必須としない。

---

# 10. Goal 2: 調査範囲を構造的に辿れる

問い合わせごとに、

```text
Screen
→ API
→ Service
→ Database
```

だけ確認すればよい場合もあれば、

```text
Input File
→ Batch
→ Table
→ Aggregation
→ API
→ Screen
```

まで必要な場合もある。

本プロジェクトでは、

> 今回事象を確認するために、どの範囲を辿る必要があるか

を関係情報から探索できることを目指す。

---

# 11. Goal 3: Codeだけでなく業務・仕様まで接続する

Source Codeだけを解析できても、運用保守として十分ではない。

目指す状態は、

```text
Business
↓
Function
↓
System
↓
Implementation
```

が接続されていることである。

例えば、

> このCode Functionは、どの画面・機能・業務のために存在するのか

まで辿れる状態を目指す。

---

# 12. Goal 4: 技術的原因と仕様判断を分離する

本プロジェクトでは、

> 原因が分かった

ことと、

> それがバグである

ことを同一視しない。

例えば、

```text
技術的原因
↓
現行仕様
↓
設計
↓
テスト
↓
開発時の合意
```

を確認することで、

- 現行仕様
- 実装バグ
- 仕様漏れ
- 追加要望
- 運用・データ起因
- 個別対応起因

などを整理できることを目指す。

---

# 13. Goal 5: Repository外のEvidenceも調査対象として扱う

[DECIDED]

現時点では、問い合わせ調査に必要なKnowledgeがすべてRepository内に存在するわけではない。

特に、

- 過去仕様
- 開発当時の設計打ち合わせ
- 議事録
- 顧客との合意内容

などはNotebookLM側で確認している。

そのため本ツールの設計では、

> Repositoryに存在するKnowledgeだけを前提にしない

ことが重要である。

将来的にはSecurity・組織ルール上可能であればRepositoryへの一元管理を目指すが、それが不可能な場合でも、外部Knowledge SourceをEvidenceとして扱える構造を検討する。

---

# 14. Goal 6: 開発時の合意までEvidenceを追跡する

問い合わせによっては、現在の仕様だけでは責任範囲を判断できない。

その場合、

> 開発当時、顧客側と開発側で何が話し合われ、何が合意されたのか

まで確認する必要がある。

将来的には、Security上許可される範囲で、

- Requirement
- Design
- Test
- Meeting
- QA
- Release
- Commit
- Inquiry

等を関連付け、

```text
Current Issue
↓
Current Specification
↓
Historical Design
↓
Meeting / Agreement
```

まで辿れる状態を目指す。

---

# 15. Goal 7: 責任範囲の判断材料を整理する

AIが責任を自動決定することは目的としない。

一方、

```text
Observed Fact
↓
Technical Cause
↓
Current Specification
↓
Historical Evidence
↓
Agreement
↓
Difference / Deviation
```

を整理し、

> 人間が責任範囲を判断するために必要な材料

を揃えられる状態を目指す。

---

# 16. Goal 8: 過去問い合わせをKnowledgeとして再利用する

既存Repositoryには、問い合わせごとの調査結果が存在する。

これらを単なる過去ファイルとして残すだけでなく、

```text
Current Inquiry
↓
Similar Past Inquiry
↓
Past Investigation
↓
Past Cause
↓
Past Resolution
```

として再利用できる状態を目指す。

問い合わせ対応が増えるほど、次の調査がしやすくなる仕組みを目標とする。

---

# 17. Goal 9: テストを仕様Evidenceとして利用する

テスト項目書を単なる品質保証資料ではなく、

> 過去にどの条件・期待結果を仕様として確認していたか

を示すEvidenceとして利用できる状態を目指す。

将来的には、

```text
Function
↓ TESTED_BY
TestCase
```

や、

```text
Requirement
↓ VERIFIED_BY
TestCase
```

のようなRelationを持てることが望ましい。

具体的なKnowledge粒度は後続設計で決定する。

---

# 18. Goal 10: AIの調査過程を確認可能にする

回答だけではなく、

- 何を確認したか
- 何を確認していないか
- どのEvidenceを使用したか
- どの情報から推論したか
- どこに不確実性があるか

を確認できる状態を目指す。

例えば、

```text
Sources Checked
- Source Code
- Current Test Specification
- Related Past Inquiry

External Evidence Checked
- Historical Design Meeting Summary

Not Checked
- Original Meeting Minutes

Missing Knowledge
- Decision record for specification X
```

のように調査Coverageを確認できることが望ましい。

---

# 19. Goal 11: Missing Knowledgeを発見する

AIが不明な点を推測で補完するのではなく、

> 判断に必要な情報が存在しない、または確認できない

ことを明示できるようにする。

例えば、

```text
Missing Knowledge
↓
必要資料を追加・確認
↓
Knowledge更新
↓
次回から調査可能
```

という循環につなげる。

---

# 20. Goal 12: Existing Repositoryを活かす

[DECIDED]

本PoCは、既存Repositoryを作り直すことを目的としない。

まず現在のRepositoryを理解し、

- 既存Directory
- 問い合わせ管理
- テスト管理
- Source Code
- 運用保守資料

など、すでに有効に機能している構造を可能な限り活用する。

その上で、

> AIが探索しやすくするために不足する情報やRelationだけを追加する

方向を優先する。

---

# 21. Goal 13: 人間の通常作業を大きく増やさない

AI-Ready Repositoryを維持するために、

> 人間が同じ内容をOriginalとAI向けファイルへ二重入力する

状態は避ける。

理想的には、

```text
Human updates normal document
↓
AI-Ready Knowledge updates automatically
```

となることを目指す。

ただしPoC段階で完全自動化を必須条件とはしない。

---

# 22. Goal 14: Repositoryを利用するほどKnowledgeが改善する

本プロジェクトではRepositoryを静的なDocument置き場ではなく、

> 運用保守業務を通じて継続的にKnowledgeが改善される仕組み

として扱いたい。

例えば、

```text
New Inquiry
↓
Investigation
↓
Evidence
↓
Cause
↓
Assessment
↓
Answer
↓
Knowledge Update
```

という循環を作る。

---

# 23. Goal 15: Stakeholderに応じたOutputを生成する

同じ調査結果をそのまま全員へ提示するのではなく、説明相手に応じて内容を変えられる状態を目指す。

## 利用者向け

- 何が起きたか
- 業務影響
- 必要な操作
- 回避方法

## 顧客側システム担当・管理者向け

- 発生事象
- 技術的原因
- 現行仕様
- 過去の合意
- 責任範囲の判断材料
- 改修要否

## Developer向け

- Reproduction
- Code
- SQL
- Data Flow
- Root Cause
- Impact
- Test Scope

---

# 24. Goal 16: 層別Graph Viewを調査へ利用する

[PROVISIONAL]

問い合わせ調査では、単なる全文検索だけではなく、

```text
Screen
→ API
→ Code
→ Table
```

や、

```text
File
→ Batch
→ Table
→ Report
```

のような関係を辿ることが有効と考えている。

そのため、

- Case
- Domain / Business
- Function
- System / Architecture
- Data Flow
- Code Structure
- Test
- Evidence / History

等を1つのCanonical Relation Modelから用途別に表示し、層をまたいで関係を辿れることを目指す。

日常調査はCase Viewを入口とし、必要に応じてData、Code、Test、History等へ切り替える。

ただしGraph Database等の具体的な実装方式は未決定である。

---

# 25. Goal 17: Knowledge Sourceを可能な範囲で一元化する

現在は、

```text
Codex
→ Repository / Source Code / Repository内資料

NotebookLM
→ 過去仕様 / Meeting Minutes / Historical Discussion
```

のようにKnowledge Sourceが分散している。

将来的にはSecurity・組織ルール上問題がなければ、

> 調査時に必要なKnowledgeを一つの仕組みから横断的に参照できる状態

を目指す。

特に議事録等をRepositoryへ一元管理できる場合は、他の資料やCodeとのRelationを持たせたい。

ただし、

- Codex直接参照可否
- Git管理可否
- Git履歴保持可否
- Masking要件
- Access Control

等については未確定である。

---

# 26. PoCの目的

本PoCでは、最終構想のすべてを実装することを目的としない。

PoCの中心目的は、

> 既存Repositoryを活かしながら、実際の問い合わせメール一件を起点に、Codexが必要なCode・Document・過去Evidenceへ辿り、技術的原因と現行仕様を整理し、その根拠を人間が確認できる仕組みが成立するかを検証すること

である。

また、NotebookLMで現在確認している過去仕様・議事録等については、利用可否やRepository統合可否を確認しながらPoC Scopeを調整する。

---

# 27. PoCで最低限検証したいこと

[PROVISIONAL]

PoCでは少なくとも以下を検証対象とする。

1. 既存Repository構造を理解できること
2. 問い合わせメール本文をそのまま調査開始Inputとして利用できること
3. 問い合わせを一つの調査単位として扱えること
4. 問い合わせから関連Codeへ辿れること
5. 関連する既存Documentへ辿れること
6. 過去問い合わせを検索・参照できること
7. 技術的原因を整理できること
8. 現行仕様との比較ができること
9. Evidenceを回答根拠として提示できること
10. 未確認情報を明示できること
11. 調査結果を人間がReviewできること

過去議事録等については、Codexからの直接参照可否およびRepository統合可否の確認結果によってPoC Scopeを変更する可能性がある。

---

# 28. PoCの代表Scenario

PoCでは、実際の運用保守に近い問い合わせメールを一件選び、End-to-Endで検証する。

例えば、

> 対象データが画面に表示されない

という内容の問い合わせメールをそのままInputとして、

```text
Inquiry Email
↓
Symptom Understanding
↓
Related Function
↓
Code / Data Investigation
↓
Technical Cause
↓
Current Specification
↓
Related Test / Document
↓
Historical Evidence
↓
Assessment
↓
Answer Draft
```

まで行えるかを確認する。

過去EvidenceがRepository外にある場合には、

```text
Codex Investigation
+
NotebookLM / External Evidence
↓
Human Review / Integration
```

もPoC上の重要な検証対象とする。

---

# 29. PoC成功時の状態

PoCが成功している状態とは、

> AIが正しい答えを一回出せた

ことではない。

以下が成立することを重視する。

## Investigation

問い合わせメールから必要な調査を開始できる。

## Traceability

調査結果からSourceまで戻れる。

## Evidence

判断根拠が明示されている。

## Coverage

何を確認し、何を確認していないか分かる。

## Reusability

調査結果を次回の問い合わせで利用できる。

## Maintainability

AI-Ready化のために過度な手作業が発生しない。

## Existing Repository Compatibility

現在のRepository運用を不必要に壊さない。

## Multi-Source Awareness

Repository外のEvidenceが必要であることを認識し、未確認のまま判断を確定しない。

---

# 30. PoC成功指標

具体的な数値目標は後続のPoC Planで決定するが、評価軸として以下を想定する。

- 調査開始までの時間
- 原因到達までの時間
- 確認したEvidence数
- Evidence Traceability
- 過去Case再利用率
- Missing Knowledge検出数
- AI回答に対するHuman Correction量
- 調査漏れの減少
- Repository更新に必要な追加作業量
- 複数Knowledge Source間の情報接続負荷

---

# 31. Future Vision

PoC後、仕組みが有効であれば、問い合わせ対応だけでなく、

- Incident
- Bug
- Change Request
- Release
- Test
- Impact Analysis
- 新規開発
- 設計Review

などへ拡張することを検討する。

例えば変更要求に対して、

```text
Change Request
↓
Affected Business
↓
Affected Function
↓
Affected Code
↓
Affected Data
↓
Related Tests
↓
Related Documents
↓
Impact
```

まで調査できる状態が考えられる。

---

# 32. Future Vision: 新規開発への活用

将来的には運用保守Knowledgeを、新しい開発にも利用できることが望ましい。

例えば、

> この機能を変更したい

という要望に対して、

- 過去に同様の変更があったか
- なぜ現在の仕様なのか
- どの業務へ影響するか
- どのTestを変更すべきか
- どのStakeholderへ確認すべきか

を確認できる状態を目指す。

---

# 33. Non-Goal: AIによる完全自動運用

[DECIDED]

PoCでは、

> AIへ問い合わせを渡せば、人間確認なしですべて回答・改修・リリースまで完了する

状態を目標としない。

Human Reviewを前提とする。

---

# 34. Non-Goal: Repositoryの全面再構築

[DECIDED]

AIのために既存Repositoryを全面的に作り直すことは目的としない。

既存構造を分析し、必要な部分のみ拡張する。

---

# 35. Non-Goal: すべてのDocumentを一律に変換する

[DECIDED]

すべてのOffice Documentを一律にMarkdown等へ変換することは目的としない。

Knowledgeとして必要な資料と必要な粒度を確認しながら対象を決める。

---

# 36. Non-Goal: Graph化そのものを目的にする

[DECIDED]

すべての情報をGraphへ入れることや、巨大なGraphを可視化すること自体は目的ではない。

Graph等のRelation表現は、

> 問い合わせ調査に必要なKnowledgeへ到達しやすくするため

に利用する。

---

# 37. Non-Goal: 特定技術への依存

[DECIDED]

本プロジェクトのDomain Modelを、

- Semantica
- Neo4j
- Vector DB
- 特定Agent Framework

など、特定製品のデータモデルへ合わせることは目的としない。

技術は交換可能な実装手段として扱う。

---

# 38. Non-Goal: AIによる責任・契約判断の自動確定

[DECIDED]

AIは、

- Evidence
- 合意内容
- Current Specification
- Difference
- Investigation Result

を整理する。

しかし、

> 誰に法的・契約的責任があるか

をAIだけで確定することは目的としない。

---

# 39. Non-Goal: 議事録の無条件なRepository統合

[DECIDED]

議事録をRepositoryへ一元化することは望ましい将来候補だが、

- Security
- Git管理可否
- Codex参照可否
- 組織ルール

を確認せずに実施しない。

---

# 40. 本PoCで最も重要な価値

本PoCで最も重要なのは、

> AIの回答精度だけを上げること

ではない。

目指す価値は、

```text
調査できる
+
根拠を辿れる
+
不足情報が分かる
+
複数Knowledge Sourceを接続できる
+
人間が検証できる
+
次の問い合わせへ再利用できる
```

ことである。

---

# 41. 本プロジェクトが目指す最終状態

最終的には、運用保守担当者が問い合わせメールを受け取った際に、その本文を起点として、

```text
What happened?
↓
Why?
↓
Where in the system?
↓
What does the current specification say?
↓
What was agreed during development?
↓
Is there a similar past case?
↓
What evidence supports the assessment?
↓
What is still unknown?
↓
How should this be explained?
```

をRepositoryとCodexを中心に、一貫して確認できる状態を目指す。

Repository外のKnowledgeが残る場合でも、

> 何を外部で確認する必要があるのか

を明示できる状態とする。

---

# 42. Vision Statement

> 既存の運用保守Repositoryと、現在NotebookLM等に分散している過去の仕様・設計合意Knowledgeを活かし、問い合わせメールをそのまま起点として、Codexが技術的原因・現行仕様・過去Evidence・不足情報まで横断的に探索し、その調査過程を人間が検証しながら自律的な運用保守判断へ到達できる環境を構築する。

## 42.1 2026-08-30 Vision Refinement

[DECIDED]

最終Visionは問い合わせ専用Toolではなく、利用者が最初に目的を選び、途中で目的を変えても調査資産を失わない運用保守Workspaceである。Work Itemから業務、機能、システム、Data、Code、Test、Operation、Stakeholder、Evidenceを横断し、問い合わせ対応・システム理解・運用・障害・変更・見積り・Knowledge整備に同じKnowledgeを再利用する。PoCは問い合わせをGolden Objectiveとするが、将来の目的追加を妨げないDomain ModelとUI契約をGoalに含める。

## 42.2 Graph Vision Refinement（2026-08-30）

[DECIDED]

Work Itemから、Technology非依存のFunction、実現・稼働境界であるSystem、Terraform等から得るInfrastructure / IaC、Code / Data Flow / Test、Evidenceまでを一続きに辿れる状態をGoalへ加える。利用者は同一層の詳細を平面Graphで確認し、層をまたぐ位置関係と欠落を縦断Stackで把握できる。両表示は同じCanonical Relation Modelを使い、別Knowledge Storeを作らない。
