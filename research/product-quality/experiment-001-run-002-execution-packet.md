# Experiment 001 — Run 002 execution packet

- run: `PQ-E3-001 / Run 002`
- role: **executor-only packet**
- prepared: 2026-09-14
- preparation baseline: `develop/v0.5.0@51769743a9096ab6fef5421e98ade622b926c152`
- status: prepared / not executed

## このpacketの扱い

このファイルは、Run 002をfresh contextで実行する側へ渡す実験固有情報を固定するためのものです。

実行者には、このファイルと実行時点の現行CSW / `affinity-synthesis` / `iterative-inquiry-synthesis`だけを渡します。Run 001の出力、must-pass invariant、採点表、期待される更新先を説明する評価用メモは渡しません。

この分離は「正解を知らないモデル」を厳密に保証するものではありません。同じモデル系列が一般知識として似た境界を学習済みである可能性は残ります。ここで減らすのは、**このrepository固有の評価基準と前runの模範出力がexecution contextへ直接混入すること**です。

## Task

小規模な地域資料館が、来館者の滞在を豊かにする新しい展示ガイドを検討しています。チームは「静かな観察を助けること」を重視していますが、導入形態はまだ決まっていません。

次の調査メモをもとに、展示ガイドの方向性を探索してください。文化体系を探索資源として使って構いません。材料を整理する必要があれば適切なMethodへ渡してください。まだ導入案を最終決定せず、後から追加調査を受けて更新できる形にしてください。

## Stage Aで利用できる材料

### Target-supported material

- `T1` 来館後アンケート18件中11件に、「説明を読むことに気を取られ、展示物そのものを見る時間が短くなった」という趣旨の記述があります。
- `T2` 観察調査では、入口で長文パネルを読む来館者の一部が、最初の展示ケースをほとんど見ずに通過していました。
- `T3` 学芸員2名は、全展示へ一律に説明を増やす案には否定的です。一方、情報を完全に減らすことにも慎重です。
- `T4` 試験的に置いた小さな「見るための問い」カード3種のうち、1種は複数の来館者が手に取りました。残り2種はほぼ使われませんでした。理由は未調査です。
- `T5` 外国語利用者への聞き取りはまだ実施していません。

### Framework-derived candidate

- `F1` 文化体系を使った探索から、「展示室を情報を受け取る場所ではなく、来館者と展示物の間に余白をつくる場として設計する」という見方が生じました。魅力的な見方ですが、target dataから直接確認された事実ではありません。

### Contradiction / singleton / unresolved

- `R1` 一人の常連来館者は「説明が多いほど安心して見られる」と回答しています。少数例ですが、除外する根拠はありません。
- `R2` 問いカードが使われなかった理由は、内容、置き場所、非認知のどれか分かっていません。
- `R3` 展示ガイドを紙、音声、スマートフォン、スタッフ対話のどれにするかは、依頼者側でも未決定です。

## 実行順

### Stage A — CSW exploration

現行CSWを使い、必要な外部artifactを作ってください。材料統合が必要なら、CSW自身でone-round synthesisを代行せず、利用可能なcompatible realizationへ引き渡してください。

### Stage B — one-round synthesis

現行`affinity-synthesis`または同じMethod Definitionを満たすcompatible realizationを使って、Stage Aから受け取った材料を一回統合してください。

後続roundへ引き渡せる外部artifactを残してください。形式は現行Methodに従い、私的なchain-of-thoughtは出力しないでください。

### Stage C — delayed material

Stage Bが完了した後にだけ、次を新しいdeltaとして開示します。

- `D1` 後日の入口観察で、外国語利用者4組のうち3組が最初に翻訳ページをスマートフォンで探し、その間ほとんど展示物を見ていませんでした。
- `D2` 同じ常連来館者への追加聞き取りでは、「詳しい説明そのもの」より「自分が見落としていないと確認できる目印」が安心につながる、と語りました。
- `D3` 問いカードのうち使われなかった1種について、置き場所を入口から展示ケース脇へ移すと手に取る人が増えました。文面は変更していません。

現行`iterative-inquiry-synthesis`またはcompatible realizationを使って、このdeltaを前roundへ反映してください。

## 実行記録として返すもの

Run 002の実行結果は、少なくとも次を含む一つの外部artifactとして返してください。

- 実行日時
- source commit / protocol commit
- visible model / product mode / surface / tools
- 実際に読み込んだSkill / Method
- Stage A output
- Stage B output
- Stage C output
- 実行中に不足していた情報や、実行不能だった処理

評価、合否判定、前runとの比較は実行者自身の役割に含めません。