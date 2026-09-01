# Living Labの公開観測記録

このディレクトリには、公開して差し支えないprospective／retrospectiveの観測記録だけを置く。

- 実案件の私的な原本は、`.living-lab/`またはリポジトリ外に置く。
- ここに置く記録は、公開情報だけで構成するか、私的な原本とは別に匿名化・抽象化したものとする。
- round／eventは、方法の因果効果や有用性を証明するものではない。後から作業の経過を確かめるための記録として扱う。
- `activation_scope`は、そのラウンドで実際に記録された発動状態を表す。`non_activation`であったという事実だけから、その状態が適切だった、有用だったとは判断しない。
- eventには、できるだけ「何が起きたか」を中立的に記録する。有用性、害、因果などについての解釈も残す場合は、判断した主体を明示して`interpretations`へ分ける。
- 利用者の判断、生成AIの解釈、外部資料の評価を、同じ来歴のものとして扱わない。
- 測定値や比較で確認された差と、それに対する評価を分ける。
- event件数、文化体系の利用数、framework contact数、`activation_scope`の分布をKPIにしない。
- 単発の記録や生成AI自身の評価だけを根拠に、`src/`の静的ルールを増やさない。

## schema 0.2

schema 0.2では、観測と評価を記録上でも分けられるようにした。

- event本文は`observation`に記録する。
- 解釈や評価は`interpretations`へ置き、`source_type`で起源を残す。
- roundの制約、残差、再開条件も、誰の判断なのか後からたどれる形で記録する。
- paired checkでは、`observed_differences`、`measurements`、`interpretations`を分ける。
- `useful_nonuse`と`harm_detected`はevent種別として用いない。非発動はroundの状態として記録でき、有用性や害についての評価は別に扱う。

2026-08-30の最初の公開roundは、当時の生成AIによる解釈を`source_type: ai`として残したうえで、schema 0.2へ移行した。旧`useful_nonuse` eventは、現在の公開観測集合から外している。Git履歴には残っているが、「不使用が適切だった」ことを示す証拠としては再利用しない。

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

roundに`task.domain`が記録されている場合、summaryにはその原文と分布も含まれる。これも観測集合の構成を見るための補助情報であり、領域分類を固定したり、各領域に件数のノルマを設けたりするためのものではない。
