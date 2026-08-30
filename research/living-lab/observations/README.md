# Living Labの公開観測記録

このディレクトリには、公開して差し支えないと判断したprospective / retrospectiveの観測記録だけを置く。

- 実案件の私的な原本は、`.living-lab/`またはリポジトリ外へ置く。
- ここへ置く記録は、公開情報だけで構成するか、私的原本とは別に匿名化・抽象化したものとする。
- round / eventは、方法の因果効果を証明するものではない。後から作業の経過と境界を確認するための観測記録として扱う。
- `non_activation` / `useful_nonuse`も正規の観測結果として扱う。
- event件数、文化体系の利用数、framework contact数をKPIにしない。
- 単発の記録だけを根拠に、`src/`の静的ルールを増やさない。

一つのclosed record setとして検査する場合は、roundとeventをまとめて指定する。

```bash
python scripts/validate_living_lab.py --record-set research/living-lab/observations/*.json
```

公開観測を後から見直すための一覧は、次のコマンドで生成できる。

```bash
python scripts/summarize_living_lab.py
```

既定では`dist/reports/living-lab-observation-summary.json`へ出力され、通常の`make check`とCIでも生成される。このsummaryは評価スコアではない。roundごとの課題、発動範囲、event、残差、再開条件を後から読み返すための一覧である。件数や分布をKPI、勝敗、因果効果として解釈しない。

roundに`task.domain`が記録されている場合、summaryにはその原文と分布も含まれる。これは、観測が特定の領域へ偏っていないか後から気づくための補助情報である。領域分類を固定するためのものでも、各領域へ件数ノルマを設けるためのものでもない。
