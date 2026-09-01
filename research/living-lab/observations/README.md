# Living Labの公開観測記録

このディレクトリには、公開して差し支えないprospective / retrospectiveの観測記録だけを置く。

- 実案件の私的な原本は、`.living-lab/`またはリポジトリ外へ置く。
- ここへ置く記録は、公開情報だけで構成するか、私的原本とは別に匿名化・抽象化したものとする。
- round / eventは、方法の因果効果や有用性を証明するものではない。後から作業の経過を確認するための記録として扱う。
- `activation_scope`は、そのラウンドで実際に記録された発動状態である。`non_activation`であったことだけから、その状態が適切・有用だったとは判断しない。
- eventは、できるだけ「何が起きたか」を中立に記録する。有用性、害、因果などの解釈が必要な場合は、判断主体を明示した`interpretations`へ分ける。
- 利用者の判断、生成AIの解釈、外部資料の評価を、同じ来歴として扱わない。
- 測定値や比較差分と、それに対する評価を分ける。
- event件数、文化体系の利用数、framework contact数、activation scopeの分布をKPIにしない。
- 単発の記録やAI自身の評価だけを根拠に、`src/`の静的ルールを増やさない。

## schema 0.2

schema 0.2では、観測と評価の分離を明示した。

- event本文は`observation`へ記録する。
- 解釈や評価は`interpretations`へ置き、`source_type`で起源を残す。
- roundの制約、残差、再開条件も、誰の判断かを追える形で記録する。
- paired checkでは、`observed_differences`、`measurements`、`interpretations`を分ける。
- `useful_nonuse`と`harm_detected`はevent typeとして用いない。非発動はroundの状態として記録でき、害や有用性は別の判断として扱う。

2026-08-30の最初の公開roundは、当時のAI解釈を`source_type: ai`として残したうえでschema 0.2へ移行した。旧`useful_nonuse` eventはactiveな公開観測集合から外した。Git履歴は残るが、「不使用が適切だった」という証拠として再利用しない。

## 検証

一つのclosed record setとして検査する場合は、roundとeventをまとめて指定する。

```bash
python scripts/validate_living_lab.py --record-set research/living-lab/observations/*.json
```

公開観測を後から見直すための一覧は、次のコマンドで生成できる。

```bash
python scripts/summarize_living_lab.py
```

既定では`dist/reports/living-lab-observation-summary.json`へ出力され、通常の`make check`とCIでも生成される。このsummaryは評価スコアではない。roundごとの課題、発動状態、event、残差、再開条件、出所付きの解釈を後から読み返すための一覧である。

summaryに含まれる件数や分布は、観測集合の構成を確認するための補助情報にすぎない。KPI、勝敗、有用性、害、因果効果として解釈しない。

roundに`task.domain`が記録されている場合、summaryにはその原文と分布も含まれる。これは観測集合の構成を見るための補助情報であり、領域分類を固定したり、各領域へ件数ノルマを設けたりするためのものではない。
