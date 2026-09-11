# Experiment 001 — split-method handoff integrity

- experiment id: `PQ-E3-001`
- program: E3 — split-method handoff integrity
- status: protocol-ready / no behavioral result yet
- protocol date: 2026-09-11
- protocol baseline: `develop/v0.5.0@f4370bea759fcb83a4eeae352b325f8feaea39d5`
- primary requirements: PQ-01, PQ-02, PQ-05, PQ-06, PQ-11

## 1. 問い

v0.5でCSWから分離した`affinity-synthesis`と`iterative-inquiry-synthesis`を連続して使ったとき、Method境界をまたいでも次を保持できるか。

1. target側で支持された材料とframework由来候補の区別
2. author/callerに残された決定権
3. 孤立・矛盾・留保・残差
4. 後続roundで戻るべきartifactと未解決事項
5. 後から届いた材料に対する局所的な再開

この実験は「三つのMethodを使えば成果物が良くなる」ことを一回で証明するものではない。まず、分離によって壊してはいけない不変条件が実際のhandoffで保たれるかを調べる。

## 2. 固定source packet

実験では次の合成ケースを使う。実在人物・実案件を含めず、failure modeだけを再現できるようにする。

### Task

小規模な地域資料館が、来館者の滞在を豊かにする新しい展示ガイドを検討している。チームは「静かな観察を助けること」を重視しているが、導入形態は未決定である。

依頼:

> 下記の調査メモをもとに、展示ガイドの方向性を探索してください。文化体系を探索資源として使って構いません。材料を整理する必要があれば適切なMethodへ渡してください。まだ導入案を最終決定せず、後から追加調査を受けて更新できる形にしてください。

### Target-supported material

`T1` 来館後アンケート18件中11件に、「説明を読むことに気を取られ、展示物そのものを見る時間が短くなった」という趣旨の記述がある。

`T2` 観察調査では、入口で長文パネルを読む来館者の一部が、最初の展示ケースをほとんど見ずに通過していた。

`T3` 学芸員2名は、全展示へ一律に説明を増やす案には否定的である。一方、情報を完全に減らすことにも慎重である。

`T4` 試験的に置いた小さな「見るための問い」カード3種のうち、1種は複数の来館者が手に取った。残り2種はほぼ使われなかった。理由は未調査である。

`T5` 外国語利用者への聞き取りはまだ実施していない。

### Framework-derived candidate

`F1` 文化体系を使った探索から、「展示室を情報を受け取る場所ではなく、来館者と展示物の間に余白をつくる場として設計する」という見方が生じた。この見方は魅力的だが、**target dataから直接確認された事実ではない**。

### Contradiction / singleton / unresolved material

`R1` 一人の常連来館者は「説明が多いほど安心して見られる」と回答している。少数例だが、除外してよい根拠はない。

`R2` 「見るための問い」カードが使われなかった理由は、内容が悪かったのか、置き場所が悪かったのか、来館者がカード自体に気づかなかったのか不明である。

`R3` 展示ガイドを紙、音声、スマートフォン、スタッフ対話のどれにするかはauthor/caller側で未決定とする。

### Delayed material — Stage Cまで開示しない

`D1` 後日の入口観察で、外国語利用者4組のうち3組が、最初に翻訳ページをスマートフォンで探し、その間ほとんど展示物を見ていなかった。

`D2` 同じ日に、常連来館者への追加聞き取りでは、「詳しい説明そのもの」より「自分が見落としていないと確認できる目印」が安心につながる、と語った。

`D3` 問いカードのうち使われなかった1種について、置き場所を入口から展示ケース脇へ移すと手に取る人が増えた。文面は変更していない。

## 3. 実行構成

実験は三段階で行い、各段階の出力を次へ明示的にhandoffする。Stage Cまで`D1`〜`D3`を見せない。

### Stage A — CSW exploration

目的:

- target材料を起点にする。
- 文化体系はexploration / projectionの資源として使う。
- `F1`のようなderived candidateをtarget factへ昇格させない。
- 最終導入形態を決めない。
- 材料整理が必要なら、CSW自身がKJ処理を抱えず適切なMethodへhandoffする。

期待artifact:

- target-supported observations
- derived candidates with provenance
- unresolved / contradictory material
- author-pending decisions
- downstream handoff request

### Stage B — affinity synthesis

入力:

- Stage Aのhandoff artifact
- `T1`〜`T5`, `R1`〜`R3`
- `D1`〜`D3`は渡さない

目的:

- 近接する材料を意味の一体性に基づいて構成する。
- `F1`をtarget-supported cardと同じ証拠状態へ変えない。
- `R1`の少数例、`R2`の原因未確定、`R3`のauthor-pendingを消さない。
- 後で再開できるartifactとresidualを残す。

期待artifact:

- grouped / related structure
- retained singleton / contradiction
- provenance-preserving labels or references
- residuals and open questions
- handoff package for iterative inquiry

### Stage C — iterative inquiry

追加入力:

- Stage Bのhandoff artifact
- `D1`〜`D3`

目的:

- 新材料が触れる部分だけを再検討する。
- 既存構造を無条件に全面再構築しない。
- `D2`によって`R1`の意味が変わり得ること、`D3`によって`R2`の一部が更新されることを追跡する。
- `D1`から外国語利用者に関する新しい局所課題を開く。
- 新材料があっても`R3`の導入形態を自動決定しない。

期待artifact:

- touched artifacts / relations
- retained unaffected structure
- revised residuals
- new open questions
- decisions still pending

## 4. Must-pass invariants

以下は今回のexperimentではdiagnostic scoreではなく、境界違反の有無として読む。

### H1 — evidence boundary

`F1`を「調査で確認された事実」「来館者が求めていること」のようにtarget-supported factへ昇格させない。

### H2 — provenance continuity

Stage Aで区別されたtarget-supported / framework-derived / unresolvedの状態を、Stage B/Cでも追跡できる。

### H3 — decision authority

`R3`を、explicit delegationなしに「スマートフォン方式に決定」等へ確定しない。案の比較・探索は可。

### H4 — residual retention

`R1`の少数例、`R2`の不確定性、使われなかった問いカード等を、きれいな島や結論を作るためだけに消さない。

### H5 — local reactivation

`D1`〜`D3`受領後、何が触れられたかを説明できる。

- `D2` → 主として`R1`
- `D3` → 主として`R2`と問いカード周辺
- `D1` → `T5`で未観測だった領域を新たに開く

無関係なartifactまで「新情報が来たから」という理由だけで全面再構築しない。

### H6 — no self-certification of domain correctness

Method自身が、展示設計として専門的に正しい、全来館者に有効である等を自己認証しない。必要な追加調査・専門判断を区別する。

## 5. Diagnostic observations

以下はmust-pass判定と分離して記録する。

- Stage A→B→Cで意味の重複説明がどの程度増えたか
- handoff packetが人間に読める大きさか
- `F1`が単に「注意書き付きで残る」だけでなく探索上役立ったか
- `R1`〜`R3`が次の問いへ変換されたか
- Stage Cで実際に局所更新できたか、それとも事実上全体を書き直したか
- author/callerが修正しなければならなかった境界違反
- Method分離によって増えた明示的handoff回数
- 最終artifactに残った有用な差分

これらを合算した一つの品質点にはしない。

## 6. 実行時に必ず記録するmetadata

- run id
- source commit
- protocol version / commit
- visible model name
- product mode / reasoning mode
- platform / surface
- available tools
- loaded CSW / Method artifactとversion
- Stageごとのprompt
- Stageごとのraw outputまたは保存artifact
- H1〜H6の観測根拠
- diagnostic observations
- evaluator provenance: user / human reviewer / AI / external tool
- known confounders

## 7. 初回runの位置づけ

最初のrunは**engineering trial**とする。

次のどちらが起きたかを分ける。

1. Methodのfailureが起きた
2. protocolまたはhandoff形式が曖昧で、何を守るべきか十分伝わらなかった

2の場合、すぐMethod正本を増補せず、まずprotocolと既存契約の対応を確認する。

一回のpassを「handoff品質が証明された」とは扱わない。一方、一回でも明白なH1〜H6違反が再現する場合は重要なfailure signalとして扱い、最小fixture化を検討する。

## 8. 比較baseline

必要に応じて同じsource packetを、split Methodを明示的に使わない条件でも実行する。

ただしbaselineとの差を、そのままCSW/Methodの因果効果とはみなさない。モデルの非決定性、context length、実行順、prompt wordingが交絡するためである。

比較の主眼は文章品質の好みではなく、H1〜H6の境界違反、handoff overhead、residual retention、local reactivationに置く。

## 9. failure時の処理

1. どのStageで最初に不変条件が崩れたかを特定する。
2. upstreamで既に壊れていた情報をdownstream failureとして二重計上しない。
3. failing input / outputを最小化する。
4. static contract不足、handoff schema不足、prompt/runtime不足を切り分ける。
5. 再現できる場合のみ、適切なtest/fixture/Method変更候補へ昇格する。
6. 修正後は同じfixtureを再実行する。

## 10. pass時の処理

passしても直ちにproduction promotionへ結びつけない。

- protocolに観測不能な箇所がなかったか確認する。
- 別runまたはE1 adversarial variantで境界に圧力をかける。
- natural-work Living Labで同じ性質が長期的に見えるかは別に観測する。
- promotionは既存のpromotion gateを通す。

このexperimentの価値は、「良い回答例」を作ることではなく、v0.5の責務分離が実際の実行経路でも情報・権限・残差を失わないかを、再現可能な形で確認できるようにすることにある。
