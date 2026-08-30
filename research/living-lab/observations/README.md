# Living Lab public observations

このディレクトリには、公開可能と判断した prospective / retrospective の観測記録だけを置く。

- 実案件の私的原本は `.living-lab/` またはリポジトリ外へ置く。
- ここへ置く記録は、公開情報だけで構成するか、別途匿名化・抽象化したものとする。
- round/eventは方法の因果効果を証明するものではない。後から作業軌跡と境界を確認するための観測記録である。
- `non_activation` / `useful_nonuse` を正常な観測として扱う。
- event件数、文化体系利用数、framework contact数をKPIにしない。
- 単発記録だけを根拠に `src/` の静的ルールを増やさない。

Closed record setとして検査する場合は、roundとeventをまとめて指定する。

```bash
python scripts/validate_living_lab.py --record-set research/living-lab/observations/*.json
```
