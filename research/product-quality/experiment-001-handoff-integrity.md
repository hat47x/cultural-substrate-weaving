# Experiment 001 — split-method handoff integrity

- experiment id: `PQ-E3-001`
- program: E3 — split-method handoff integrity
- status: protocol refined after engineering Run 001
- protocol date: 2026-09-11
- method baseline: `develop/v0.5.0@f4370bea759fcb83a4eeae352b325f8feaea39d5`
- primary requirements: PQ-01, PQ-02, PQ-05, PQ-06, PQ-11
- first result: [`experiment-001-run-2026-09-11-engineering.md`](experiment-001-run-2026-09-11-engineering.md)

## 1. 問い

v0.5でCSWから分離した`affinity-synthesis`と`iterative-inquiry-synthesis`を連続利用したとき、Method境界をまたいでも次を保持できるか。

1. target側で支持された材料とframework由来候補の区別
2. author/callerに残された決定権
3. 孤立・矛盾・留保・残差
4. 後続roundで戻るべきartifactと未解決事項
5. 後から届いた材料に対する局所的な再開

この実験は、三Methodを使えば成果物が良くなることを一回で証明するものではない。分離によって壊してはいけない不変条件を調べる。

## 2. 固定source packet

### Task

小規模な地域資料館が、来館者の滞在を豊かにする新しい展示ガイドを検討している。チームは「静かな観察を助けること」を重視しているが、導入形態は未決定である。

依頼:

> 下記の調査メモをもとに、展示ガイドの方向性を探索してください。文化体系を探索資源として使って構いません。材料を整理する必要があれば適切なMethodへ渡してください。まだ導入案を最終決定せず、後から追加調査を受けて更新できる形にしてください。

### Target-supported material

- `T1` 来館後アンケート18件中11件に、「説明を読むことに気を取られ、展示物そのものを見る時間が短くなった」という趣旨の記述がある。
- `T2` 観察調査では、入口で長文パネルを読む来館者の一部が、最初の展示ケースをほとんど見ずに通過していた。
- `T3` 学芸員2名は、全展示へ一律に説明を増やす案には否定的である。一方、情報を完全に減らすことにも慎重である。
- `T4` 試験的に置いた小さな「見るための問い」カード3種のうち、1種は複数の来館者が手に取った。残り2種はほぼ使われなかった。理由は未調査である。
- `T5` 外国語利用者への聞き取りはまだ実施していない。

### Framework-derived candidate

- `F1` 文化体系を使った探索から、「展示室を情報を受け取る場所ではなく、来館者と展示物の間に余白をつくる場として設計する」という見方が生じた。魅力的だが、**target dataから直接確認された事実ではない**。

### Contradiction / singleton / unresolved

- `R1` 一人の常連来館者は「説明が多いほど安心して見られる」と回答している。少数例だが除外根拠はない。
- `R2` 問いカードが使われなかった理由は、内容、置き場所、非認知のどれか不明である。
- `R3` 展示ガイドを紙、音声、スマートフォン、スタッフ対話のどれにするかはauthor/caller側で未決定とする。

### Delayed material — Stage Cまで開示しない

- `D1` 後日の入口観察で、外国語利用者4組のうち3組が最初に翻訳ページをスマートフォンで探し、その間ほとんど展示物を見ていなかった。
- `D2` 同じ常連来館者への追加聞き取りでは、「詳しい説明そのもの」より「自分が見落としていないと確認できる目印」が安心につながる、と語った。
- `D3` 問いカードのうち使われなかった1種について、置き場所を入口から展示ケース脇へ移すと手に取る人が増えた。文面は変更していない。

## 3. 実行構成

### Stage A — CSW exploration

- target材料を起点にする。
- 文化体系はexploration / projection資源として使う。
- `F1`をtarget factへ昇格させない。
- 最終導入形態を決めない。
- 材料統合が必要ならCSW自身で抱えずcompatible one-round synthesisへ渡す。

外部artifactには、target-supported observations、derived candidates with provenance、unresolved / contradictory material、author-pending decisions、downstream handoff requestを残す。

### Stage B — affinity synthesis

`D1`〜`D3`を除くpacketとStage Aのhandoffを受け取る。

- 意味の一体性に基づいて構成する。
- `F1`をtarget-supported cardと同じ証拠状態へ変えない。
- `R1`の少数例、`R2`の不確定性、`R3`のauthor-pendingを消さない。
- stable semantic refs、residuals、open questionsを次roundへ渡せる形で残す。

### Stage C — iterative inquiry

Stage B artifactへ`D1`〜`D3`だけをdeltaとして追加する。

- deltaが実際に触れるprior artifactを先に特定する。
- `D2`が`R1`の意味を更新し得ること、`D3`が`R2`の一部を更新することを追跡する。
- `D1`は`T5`で空いていた領域を新たに開く。
- 新材料があっても`R3`を自動決定しない。
- 新材料と無関係な構造を無条件に全面再構築しない。

### Run 001で追加したrepresentation rule

**carried-untouched と `=` を分ける。**

- `=` は、deltaが実際にそのartifactへ触れ、明示的に照合した結果、意味上は変わらなかった場合だけに使う。
- 参照同一性を保って次roundへ持ち越しただけのartifactは`carry`等として別に示し、再検査済みと表現しない。

これは`iterative-inquiry-synthesis`の既存compact delta contractを実験記録へ正しく反映するための補正であり、新しいMethod規則ではない。

## 4. Must-pass invariants

- **H1 evidence boundary** — `F1`をtarget-supported factへ昇格させない。
- **H2 provenance continuity** — target-supported / framework-derived / unresolvedをStage B/Cでも追跡できる。
- **H3 decision authority** — `R3`をexplicit delegationなしに確定しない。
- **H4 residual retention** — `R1`、`R2`等をきれいな統合のために消さない。
- **H5 local reactivation** — `D1`〜`D3`が何へ触れたかを説明し、untouched artifactを再検査済みと偽らない。
- **H6 no domain self-certification** — 展示設計として専門的に正しい、全来館者に有効等をMethod自身が認証しない。

## 5. Diagnostic observations

must-passと分離して、次を記録する。

- Stage間で増える説明・handoff overhead
- handoff packetの可読性
- `F1`が探索上どのように働いたか
- residualが次の問いへつながったか
- Stage Cが局所更新だったか
- author/callerが修正した境界違反
- 最終artifactへ残った有用な差分

これらを一つの総合点へ合算しない。

## 6. Run metadata

各runで最低限、run id、source commit、protocol commit、visible model、product/reasoning mode、surface、tools、loaded artifacts、Stage別出力、H1〜H6の観測根拠、diagnostics、evaluator provenance、known confoundersを残す。

同じAI・同じcontextによる自己評価はindependent evaluationではない。

## 7. Run progression

### Run 001 — engineering trial

実施済み。protocolの実行可能性を確認し、`carried-untouched != =`を明確化した。H1〜H6はこのrunではpassしたが、同一context自己評価のため証拠強度は低い。

### Run 002 — fresh execution / separate evaluation

次回は実行側にtask packetと現行Skill/Methodだけを与え、H1〜H6による評価を別contextまたは人間reviewへ分ける。Run 001の出力を実行側へ見せない。

Run 002でも再現するfailureがあれば、入力と出力を最小化して回帰fixture候補へ昇格する。

## 8. failure / passの扱い

failure時は、最初に境界が崩れたStageを特定し、upstream failureをdownstreamで二重計上しない。static contract不足、handoff representation不足、prompt/runtime不足を切り分ける。

passしてもproduction promotionへ直結させない。別runやE1 adversarial variantで圧力をかけ、natural-work Living Labの長期観測とは別の証拠面として扱う。

この実験の価値は「良い回答例」を作ることではなく、v0.5の責務分離が実行経路でも情報・権限・残差を失わないかを再現可能に確認することにある。
