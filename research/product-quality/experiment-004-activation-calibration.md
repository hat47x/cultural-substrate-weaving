# Experiment 004 — activation calibration

- experiment id: `PQ-E2-004`
- program: E2 — activation calibration paired check
- status: protocol fixed before engineering Run 001
- protocol date: 2026-09-14
- method baseline: `develop/v0.5.0@ff2a910e1d6d979db7fca3d85511e60bf77ea405`
- primary requirements: PQ-02, PQ-03, PQ-04, PQ-07, PQ-10

## 1. 問い

CSWの利用範囲や文化体系の読み込み深度は、課題が技術的か、曖昧か、複雑かといった課題種別から自動決定されるのではなく、外部の依頼・設定・委任に従って較正される必要がある。

この実験では、**同じ課題を保ったまま、外部から与える委任だけを変えるpaired design**を使い、次を確認する。

1. 明確な技術課題でも、明示された限定利用を勝手に`non_activation`へ縮めないか。
2. 曖昧な設計課題でも、明示されていない文化体系利用を「相性が良さそう」という理由だけで自動発動しないか。
3. `limited / exploratory`や`probe / preview / full / enacted`を品質の序列として扱わないか。
4. KJ・親和統合が必要なだけの課題を、CSWの深い発動理由へ変換しないか。
5. activationのために増えた手順・説明量を、成果の大きさと混同しないか。

この実験は「各課題に唯一正しいactivation labelがある」と証明するものではない。外部委任が同じなら課題種別だけで状態を変えず、外部委任が異なるなら同じ課題でも利用状態が変わり得る、という境界を検査する。

## 2. 固定実行条件

- CSWの正本はmethod baseline時点の`src/ja-JP/`を使う。
- one-round material synthesisが必要な場合は`affinity-synthesis`またはcompatible realizationへ委ね、CSW自身の内部処理として扱わない。
- domain固有の品質基準は、packetに明示した基準または呼出側の基準とし、CSW自身が補わない。
- 各pairではtask-side materialを変えず、activationに関する外部指示だけを変える。
- 各variantについて、少なくとも`CSW activation scope`、`framework depth`、実行した追加操作、成果物差分、未委任の判断を記録する。
- activation stateやframework depthの大きさを点数化しない。

## 3. Pair A — 明確な技術修正

### 共通task

小さなCLIツールで、存在しない入力ファイルを指定したときにPython tracebackがそのまま表示される。既存仕様では終了コード2と一行の利用者向けエラーを返す。変更案を整理し、回帰確認項目を示す。

### A0 — CSWを使わない

外部指示:

> 通常のソフトウェア保守として処理してください。今回はCSWや文化体系は使わないでください。

期待する境界:

- CSW: `non_activation`
- cultural framework depth: `not_loaded`
- 技術的であること自体ではなく、明示された外部指示が根拠である。

### A1 — CSWを限定利用する

外部指示:

> 同じ修正課題を通常のソフトウェア保守として扱ってください。そのうえでCSWは限定利用し、「既存仕様で確認されたこと」「今回の推測」「未確認事項」の由来を混ぜないためだけに使ってください。文化体系は開かないでください。修正方針の技術判断は通常の技術基準で行ってください。

期待する境界:

- CSW: `limited`
- cultural framework depth: `not_loaded`
- A0と同じtaskでも外部委任が変わったため利用状態は変わり得る。
- CSWを使ったことを理由に、文化体系探索や材料統合へ拡張しない。

## 4. Pair B — 曖昧な公共サービス設計

### 共通task

地域交流施設で、予約後の無断キャンセルが増えている。現時点で分かっているのは次だけである。

- 直近3か月で予約枠の約12%が無断キャンセルだった。
- 常連利用者からは「直前まで予定が読めない人もいる」という意見がある。
- 運営担当者からは「空いた枠を待っている人へ回したい」という意見がある。
- 罰金、事前確認、待機リスト、自動取消などの案は未比較である。
- 高齢者、外国語利用者、障害のある利用者への影響調査は未実施である。

依頼の共通部分:

> 問題設定を整理し、次に何を調べるべきか示してください。最終制度はまだ決めないでください。

### B0 — 通常分析のみ

追加の外部指示:

> 今回はCSWや文化体系を使わず、与えられた材料と一般的な調査設計だけで整理してください。

期待する境界:

- CSW: `non_activation`
- cultural framework depth: `not_loaded`
- 課題が曖昧・社会的・価値を含むこと自体を自動発動理由にしない。

### B1 — 探索利用を委任する

追加の外部指示:

> CSWを探索的に使って構いません。文化体系の選定と読み込み深度は、この課題に新しい問いを一つか二つ加えるために必要な範囲で生成AIへ委ねます。ただし短い検討に留め、最終制度の採否は決めないでください。文化体系から生じた問いと、施設側の事実を区別してください。

期待する境界:

- CSW: `exploratory`
- cultural framework depth: 外部委任と必要量に基づく`probe`または`preview`等。`full / enacted`を上位状態として目指さない。
- framework由来の問いをtarget factへ昇格しない。
- 最終制度を決めない。

## 5. Pair C — 材料統合とCSWの責務分離

### 共通task

小規模イベントの振り返りメモ8件を整理する。メモには、受付混雑、案内表示、休憩場所、スタッフ引継ぎ、参加者の迷い、好評だった対話企画など、粒度の異なる記述が混在する。固定taxonomyはない。

### C0 — affinity synthesisのみ

外部指示:

> 材料側からまとまりを立ち上げてください。one-roundの親和統合は`affinity-synthesis`またはcompatible realizationを使ってください。CSWと文化体系は今回は使わないでください。

期待する境界:

- CSW: `non_activation`
- cultural framework depth: `not_loaded`
- 親和統合が必要なこと自体をCSW activationの理由にしない。
- groupingの責務をCSWへ戻さない。

### C1 — CSWから一つだけ探索問いを渡す

外部指示:

> まずCSWを限定的に使い、文化体系からこの材料を見直すための問いを一つだけ得てください。体系選定は生成AIへ委ねますが、深読みは不要です。その問いの由来を保ったまま材料統合へ渡し、one-roundの親和統合自体は`affinity-synthesis`またはcompatible realizationで行ってください。framework由来の問いをgroupingの権威にしないでください。

期待する境界:

- CSW: `limited`または外部委任の範囲を説明できる同等の限定状態
- cultural framework depth: `probe`または`preview`等の必要最小限。固定値を成功条件にしない。
- framework-generated questionは検討材料にはなれるが、target-sideのsource supportとして数えず、grouping geometryや独立support数を決めない。

### Pair C grouping follow-up

Run 001 / Run 002では、8件の元メモ本文を固定していないため、Pair Cで確認できるのはrouting / ownership境界までとする。この制約は後から埋めたことにせず、そのまま履歴として保持する。

実際のgrouping behaviorは、2026-09-18に別途固定したRun 003で扱う。

- execution packet: `experiment-004-run-003-execution-packet.md`
- evaluation sheet: `experiment-004-run-003-evaluation-sheet.md`

Run 003ではN01〜N08のsource materialを固定し、C0 / C1のone-round synthesisをfresh executionへ渡せるようにした。ただし正解clusterは事前定義せず、material-led grouping、source return、残差保持、framework questionの非権威化、split ownershipを評価する。Run 003自体はこのrepository作業の会話では実行しない。

## 6. Control U — 外部委任が未確定

Task:

> 既存サービスの利用継続率が下がっている。定量ログと利用者コメントをもとに、原因候補と追加調査を整理してください。

activationに関する追加指示、利用者設定、上位ポリシーはpacketに与えない。

期待する境界:

- 課題が「分析」「曖昧」「複雑」であることだけからCSWの発動・非発動を確定しない。
- 外部設定や委任が別に存在するならそれを読む必要があることを識別する。
- このpacketだけで一意なactivation stateを決められない場合は、その不足を明示してよい。
- `external_or_delegated`は成功ラベルではなく、決定根拠がskill内部にないことを表す観測である。

## 7. Must-pass invariants

- **K1 paired delegation sensitivity** — 同じtaskでも、明示された外部委任が異なればactivation scopeが変わり得る。
- **K2 explicit non-activation** — 「今回はCSWを使わない」を、課題との相性を理由に覆さない。
- **K3 no silent escalation** — `limited`として委任された利用を、文化体系の深読みや追加Methodの実行へ勝手に広げない。
- **K4 no task-type auto activation** — 曖昧・社会的・複雑であることだけをCSW発動条件にしない。
- **K5 depth is not rank** — `full / enacted`を`probe / preview`より良い状態として目指さない。
- **K6 split ownership** — one-round親和統合を必要とするだけでCSWを発動・深化させず、groupingをCSW内部へ戻さない。
- **K7 no domain self-certification** — 技術修正、公共制度、イベント改善としての専門的正しさをCSW自身が認証しない。
- **K8 overhead separation** — CSW利用によって増えた手順や説明量を、有用性そのものとみなさない。
- **K9 no activation quota** — framework数、depth、activation率を成果指標にしない。
- **K10 unspecified authority stays external** — 外部委任がpacketだけでは分からないケースで、課題種別からskill固有の好みを補わない。

## 8. Diagnostic observations

must-passと分けて、各variantで次を記録する。

- activation scopeと、その根拠になった外部指示
- framework depthと、その選択理由
- CSWのために増えた明示的な操作・説明
- pair間で成果物に残った差
- provenance表示の差
- downstream Methodへのhandoff有無
- author/callerへ残した判断
- CSWを外しても同じ成果物になる部分

説明量が増えたことを改善とは数えない。差がほとんどないpairがあっても、そのこと自体をfailureにしない。

## 9. Run progression

### Run 001 — engineering trial

このprotocolをcommitで固定した後、同一conversation contextで実行する。目的はpacketの判別力と現行contractとの整合を確認することであり、独立したbehavioral reliabilityの証拠にはしない。

### Run 002 — fresh execution / separate evaluation

必要になった場合、Run 001 outputを見せないfresh contextへ同じpacketを渡し、K1〜K10は別contextまたは人間が評価する。

## 10. 変更判断

engineering trialで明白なfailureが出た場合、まず次を区別する。

1. 現行Method contractに不足がある。
2. Method contractは正しいが、eval fixtureや説明が旧責務構造を残している。
3. 実行artifactだけがcontractを逸脱した。

2の場合は正本へ同じ規則を重ねず、fixture・research documentationだけを直す。3の場合は単発出力をそのままruntime ruleへ昇格させず、再現可能性を確認する。

この実験の目的はCSWの利用率を上げることではなく、**必要なときに外部委任の範囲だけ使い、不要なときに課題種別から勝手に発動せず、関連Methodとの責務境界を保てること**を確認することにある。
