# Experiment 003 — Run 002 execution packet

- run: `PQ-E4-003 / Run 002`
- role: **executor-only packet**
- prepared: 2026-09-16
- preparation baseline: `develop/v0.5.0@e6b3c138be38810d4a6869ccad5404282f2ec254`
- status: prepared / not executed

## このpacketの扱い

このファイルは、E4 Run 002をfresh contextで再開する側へ渡す情報だけを固定する。

実行者には、このpacketと実行時点の現行`iterative-inquiry-synthesis`、必要な場合に限りcompatibleなone-round synthesis realizationを渡す。Run 001の出力、評価sheet、L1〜L10の識別子、期待される更新形は渡さない。

このrunは、実時間の記憶保持性能を測るものではない。保存された外部snapshotとdelayed deltaだけから、停止後の調査を再開する契約を検査する。

## Prior snapshot

対象は、小規模な公共図書館が初来館者向けの館内案内を見直している事例である。前回までの調査は2roundでいったん停止したものとする。

### Prior inquiry

> 初来館者が迷わず利用を始められるようにするには、説明情報を増やすべきか、減らすべきか。

### Stable semantic artifacts

- `C01` — 初来館者の一部は、入口の長い案内を読む間に館内へ進めず、最初の行動開始が遅れる。
- `C02` — 繰り返し利用者の多くは、入口案内をほとんど読まず目的の棚へ向かう。
- `C03` — 職員は「説明を減らしすぎると、初来館者が不安になる可能性がある」と述べている。これは職員の見立てであり、初来館者本人への確認は不足している。
- `C04` — 閲覧席の照明については別調査が進んでおり、案内情報量との関係は現時点で確認されていない。
- `F01` — 文化体系を使った探索から、「入口を説明の集積点ではなく、館内へ移るための閾として扱う」という候補が生じた。`framework_generated`であり、対象側の独立supportではない。

### Groups / relations

- `G01` — 「入口で情報を受け取ることが、行動開始と競合する場合がある」
  - members: `C01`, `C02`
- `G02` — 「初来館者には、情報量とは別に安心を支える何かが必要かもしれない」
  - members: `C03`
- `G03` — 「閲覧環境に関する別系統の課題」
  - members: `C04`
- `R01` — `G01 -> Q01` :: 「案内情報量と行動開始の関係を再検討させる」

`F01`は`G01`の独立supportとして数えない。探索上の候補として別に保持する。

### Residuals / questions

- `U01` — 初来館者の「不安」が、説明不足によるものか、現在地・次行動が分からないことによるものかを区別できていない。
- `Q01` — 説明情報を増やす／減らすことのどちらが初来館者を助けるのか。
- `Q02` — 外国語利用者に同じ問題構造があるかは未調査。
- `P01` — 紙、サイン、スマートフォン、スタッフ案内のどれを採るかは図書館側の未決定事項。

### Stop snapshot

前roundは次の理由で停止した。

- `U01`を判別できる初来館者本人の材料がない。
- `Q02`に答える外国語利用者の観察・聞き取りがない。
- `P01`は分析Methodが独立決定する事項ではない。
- 現材料だけでroundを続けても、意味のある構造変化を生む根拠がない。

stop reason:

> **Stop — 現在の問いをさらに判別できる新材料がなく、残差を残したまま一度閉じる。**

## Delayed delta — 6週間後

前roundから6週間後に、次の材料だけが追加されたものとする。

- `D01` 初来館者8名への短い聞き取りで、5名が「詳しい説明がほしい」というより、「今どこにいて、次に何をすればよいか分かると安心する」と答えた。
- `D02` 入口の長文案内を変えず、主要ゾーンへ向かう一行の方向表示だけを追加した小規模観察では、初来館者が入口付近で立ち止まる時間が短くなった。サンプルは少なく、長期効果は未確認である。
- `D03` 外国語利用者3組の観察では、2組が日本語の入口案内を読まず、スマートフォンで館内図を探していた。理由の聞き取りは行っていない。
- `D04` 閲覧席の照明調査では、夕方の一部利用者からまぶしさの訴えがあった。案内情報量との関係を示す材料はない。

## 実行指示

`iterative-inquiry-synthesis`または同じMethod Definitionを満たすcompatible realizationを使い、prior snapshotを上書きせず、新しいroundとして再開する。

必要な場合だけcompatible one-round synthesisを使う。使わなかった処理を実行済みと称しない。

実行artifactには、少なくとも次を外部化する。

1. current inquiry
2. delayed delta
3. reopened prior artifacts / touched semantic IDs
4. なぜその範囲を再開したか
5. structural delta
6. carried but untouched artifacts
7. residuals
8. question shift
9. continuation boundary
10. 次roundへのhandoff

private chain-of-thoughtは出力しない。

## 実行記録として返すもの

- 実行日時
- source commit / protocol commit
- visible model / product mode / surface / tools
- 実際に読み込んだSkill / Method
- 上記の再開artifact
- 実行中に不足していた情報や、実行不能だった処理

評価、合否判定、Run 001との比較は実行者自身の役割に含めない。
