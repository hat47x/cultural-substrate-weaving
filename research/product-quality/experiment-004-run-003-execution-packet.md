# E2 Run 003 — Pair C grouping behavioral packet

- experiment id: `PQ-E2-004-R003`
- role: executor-only packet
- prepared: 2026-09-18
- source snapshot: `develop/v0.5.0@9bd8d7957680c26daae5d51d942543f7033df382`
- status: prepared / not executed in the repository-working conversation
- scope: Pair C only — material synthesis / CSW responsibility boundary
- source provenance: synthetic fixed material for controlled comparison; not a Living Lab or empirical observation

## このpacketの目的

E2 Run 002では、Pair Cの元メモ本文が固定されていなかったため、routing / ownership境界までしか評価できなかった。

Run 003では、同じ8件の振り返りメモをC0 / C1へ渡し、実際のone-round groupingが行われる状況でも、次の境界が保たれるかを観測する。

- 親和統合の責務をCSWへ戻さない。
- C1で文化体系から得た問いを、groupingの分類器や証拠権威にしない。
- source noteの質感、矛盾、成功と摩擦の併存、残差を失わない。
- C0 / C1の差を「CSWを使った方が優れている」という順位へ変換しない。

このrunは唯一の正しいclusterを求めるものではない。材料から複数の妥当なまとまりが立ち上がり得ることを前提に、責務・来歴・source returnを観測する。

## executorへ渡してよいもの

各variantでは、次だけを渡す。

1. このexecution packet
2. source snapshotに対応するCSW
3. source snapshotに対応する`affinity-synthesis`、または実際に利用可能なcompatible one-round realization
4. surfaceの通常利用に必要なplatform標準情報

次は渡さない。

- `experiment-004-run-003-evaluation-sheet.md`
- Run 001 / Run 002の出力
- もう一方のvariantの出力
- 「期待するcluster」や「正解の島名」
- 文化体系の選定例や、そこから出るはずの問い

compatible realizationが実際には利用できない場合、完全な`affinity-synthesis`を実行したと称さず、その制約をmetadataへ残す。

## 実行方法

C0とC1は、可能なら互いの出力を見ないfresh contextで別々に実行する。

同じexecutor contextで続けて実行する場合は、その事実と順序をmetadataへ記録し、比較時のconfounderとする。

Web検索や外部調査でsource materialを増補しない。

## 固定source material

以下の8件は、controlled comparisonのために作成した合成source materialであり、実在イベントの観測記録ではない。書かれている順序をtaxonomyや重要度とみなさず、C0 / C1で同じ材料として使う。IDはsource returnのための安定参照であり、分類ラベルではない。

### N01

開場10分後、受付前に列ができ、参加者2人が「先に会場へ入っていいですか」と質問した。名簿確認と参加費の受け取りを同じ机で一人が担当し、後ろの人が入口付近に広がった。

### N02

入口の案内板には会場名と矢印はあったが、受付後にどこで待つかは書かれていなかった。初参加者が常連らしい人について奥の部屋へ入り、スタッフに呼び戻された。

### N03

廊下のベンチを休憩用に残していたが、昼前には資料箱と上着が置かれ、座れない時間があった。歩行に不安のある参加者が壁際でしばらく立っていたことを、終了後になってスタッフが知った。

### N04

午後担当へ引き継ぐメモには進行時刻と備品数はあったが、「受付で迷った人が多かった」「休憩場所を聞かれた」ことは口頭だけで、交代時に伝わらなかった。

### N05

対話企画では、進行役が説明を短くし、参加者の言葉を待つ時間を取った。アンケートには「話を聞いてもらえた」「知らない人の話をもっと聞きたかった」とあり、予定を10分過ぎても数人が席を立たなかった。

### N06

対話企画の終了後も参加者同士の会話がロビーまで続き、次の回の受付列と重なった。スタッフは会話を止めたくなくて誘導をためらい、入口が見えにくくなった。

### N07

混雑時、受付担当は一人ずつ説明するのをやめ、会場図を指して案内した。列は早く進んだが、2人から後で「休める場所が分からなかった」と聞いた。

### N08

終了後のスタッフ振り返りでは、「案内を増やすべき」という意見と「文字を増やすと見なくなる」という意見が両方出た。あるスタッフは「迷った時に誰へ聞けばよいかが見えれば十分かもしれない」と話した。

## C0 — affinity synthesisのみ

### 外部指示

> この8件を、材料側からまとまりが立ち上がるようにone-roundで親和統合してください。`affinity-synthesis`または実際に利用可能なcompatible realizationを使い、CSWと文化体系は今回は使わないでください。固定taxonomyを先に置かず、元メモへ戻れる形で、まとまり・関係・残る違和感や未統合要素を示してください。

### executorが返すもの

- CSW activation scope
- cultural framework depth
- 実際に利用したMethod / realization
- source IDへ戻れるgrouping artifact
- group labelと、そのlabelが保持する核
- group間の関係が見える場合はその関係
- 無理に統合しなかった残差・緊張・反例
- source returnで気付いた取りこぼし
- domain上の最終改善案を決めていないこと

## C1 — CSWから一つだけ問いを渡してからaffinity synthesis

### 外部指示

> 最初にCSWを限定的に使い、この8件を見直すための問いを文化体系から一つだけ得てください。体系選定は依頼の範囲で判断して構いませんが、深読みは不要です。その問いを`framework_generated`として明示し、対象事実やgroupingの分類器にしないでください。その後、同じ8件を`affinity-synthesis`または実際に利用可能なcompatible realizationでone-round親和統合してください。まとまりは材料側から立ち上げ、元メモへ戻れる形で、関係・残差・反例も残してください。

### executorが返すもの

C0と同じ項目に加え、次を返す。

- 選んだ文化体系と読み込み深度
- 一つだけのframework-generated question
- その問いがgroupingへ渡された経路
- その問いをtarget-supported evidenceへ昇格させていないこと
- grouping後に、その問いが何を照らし、何を照らさなかったか

## metadata

variantごとにraw outputと別枠で保存する。

```text
run_id:
variant: C0 / C1
visible_model:
product_mode_or_reasoning_mode:
source_commit: 9bd8d7957680c26daae5d51d942543f7033df382
csw_package_or_path:
affinity_realization:
invocation_route:
tools_available:
tools_actually_used:
execution_date:
execution_context_fresh_for_e2_pair_c: yes / no / unknown
other_variant_output_seen_before_execution: yes / no / unknown
capability_limitations_observed:
```

確認できない項目は`unknown`とし、推測で補わない。

## executorが行わないこと

- C0 / C1の優劣判定
- 期待clusterへの寄せ
- sourceにない参加者反応や因果の創作
- frameworkとの対応だけを根拠にしたgrouping
- framework questionを追加source noteとしてsupport数へ数えること
- `affinity-synthesis`が利用不能なのに実行済みと書くこと
- 最終的なイベント改善策の採否決定

## 完了条件

各variantは、raw outputとmetadataが保存された時点でexecution artifactとして完了する。

C0 / C1の両方が揃えばpaired evaluationへ進める。片方しかない場合は、そのvariant単独の責務・provenance評価だけを行い、paired差分は`not available`とする。
