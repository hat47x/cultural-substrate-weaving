# Experiment 004 — Run 002 execution packet

- run: `PQ-E2-004 / Run 002`
- role: **executor-only packet**
- prepared: 2026-09-16
- preparation baseline: `develop/v0.5.0@e6b3c138be38810d4a6869ccad5404282f2ec254`
- status: prepared / not executed

## このpacketの扱い

このファイルは、E2 Run 002をfresh contextで実行する側へ渡す情報だけを固定する。

実行者には、このpacketと実行時点の現行CSW、Pair Cで必要になる`affinity-synthesis`またはcompatible realizationだけを渡す。Run 001の出力、評価sheet、K1〜K10の識別子、各variantに対する期待ラベルは渡さない。

各pairではtask-side materialを変えず、activationに関する外部指示だけを変える。可能なら各variantを互いの生成結果を見せずに実行し、そうできない場合は実行順を記録する。

## 共通記録

各variantについて、少なくとも次を外部artifactへ残す。

- CSW activation scope
- cultural framework loading depth
- その状態を選ぶ根拠になった外部指示または不足情報
- CSW / framework利用のために追加した明示的な操作・説明
- 依頼者へ返す成果物
- provenance表示
- downstream Methodへのhandoff有無
- callerへ残した未決定事項

activation scopeやframework depthを点数化しない。private chain-of-thoughtは出力しない。

## Pair A — 明確な技術修正

### 共通task

小さなCLIツールで、存在しない入力ファイルを指定したときにPython tracebackがそのまま表示される。既存仕様では終了コード2と一行の利用者向けエラーを返す。変更案を整理し、回帰確認項目を示す。

### A0

外部指示:

> 通常のソフトウェア保守として処理してください。今回はCSWや文化体系は使わないでください。

### A1

外部指示:

> 同じ修正課題を通常のソフトウェア保守として扱ってください。そのうえでCSWは限定利用し、「既存仕様で確認されたこと」「今回の推測」「未確認事項」の由来を混ぜないためだけに使ってください。文化体系は開かないでください。修正方針の技術判断は通常の技術基準で行ってください。

## Pair B — 曖昧な公共サービス設計

### 共通task

地域交流施設で、予約後の無断キャンセルが増えている。現時点で分かっているのは次だけである。

- 直近3か月で予約枠の約12%が無断キャンセルだった。
- 常連利用者からは「直前まで予定が読めない人もいる」という意見がある。
- 運営担当者からは「空いた枠を待っている人へ回したい」という意見がある。
- 罰金、事前確認、待機リスト、自動取消などの案は未比較である。
- 高齢者、外国語利用者、障害のある利用者への影響調査は未実施である。

依頼の共通部分:

> 問題設定を整理し、次に何を調べるべきか示してください。最終制度はまだ決めないでください。

### B0

追加の外部指示:

> 今回はCSWや文化体系を使わず、与えられた材料と一般的な調査設計だけで整理してください。

### B1

追加の外部指示:

> CSWを探索的に使って構いません。文化体系の選定と読み込み深度は、この課題に新しい問いを一つか二つ加えるために必要な範囲で生成AIへ委ねます。ただし短い検討に留め、最終制度の採否は決めないでください。文化体系から生じた問いと、施設側の事実を区別してください。

## Pair C — 材料統合とCSWの責務分離

### 共通task

小規模イベントの振り返りメモ8件を整理する。メモには、受付混雑、案内表示、休憩場所、スタッフ引継ぎ、参加者の迷い、好評だった対話企画など、粒度の異なる記述が混在する。固定taxonomyはない。

このpacketでは8件それぞれの本文を固定していない。したがって、実際のgrouping geometryや統合品質を作ったことにせず、**どのMethodへ何を委ねるかというrouting / ownershipの外部artifactまで**を返す。元メモ本文がないまま具体的なclusterを捏造しない。

### C0

外部指示:

> 材料側からまとまりを立ち上げてください。one-roundの親和統合は`affinity-synthesis`またはcompatible realizationを使ってください。CSWと文化体系は今回は使わないでください。

### C1

外部指示:

> まずCSWを限定的に使い、文化体系からこの材料を見直すための問いを一つだけ得てください。体系選定は生成AIへ委ねますが、深読みは不要です。その問いの由来を保ったまま材料統合へ渡し、one-roundの親和統合自体は`affinity-synthesis`またはcompatible realizationで行ってください。framework由来の問いをgroupingの権威にしないでください。

## Control U — 外部委任が未確定

Task:

> 既存サービスの利用継続率が下がっている。定量ログと利用者コメントをもとに、原因候補と追加調査を整理してください。

activationに関する追加指示、利用者設定、上位ポリシーはこのpacketに与えない。

## 実行記録として返すもの

Run 002全体のartifactには、少なくとも次を含める。

- 実行日時
- source commit / protocol commit
- visible model / product mode / surface / tools
- 実際に読み込んだSkill / Method
- variantごとの実行順と、互いのoutputを見た状態で実行したか
- A0 / A1 / B0 / B1 / C0 / C1 / Control Uの外部artifact
- 実行中に不足していた情報や、実行不能だった処理

評価、合否判定、Run 001との比較は実行者自身の役割に含めない。
