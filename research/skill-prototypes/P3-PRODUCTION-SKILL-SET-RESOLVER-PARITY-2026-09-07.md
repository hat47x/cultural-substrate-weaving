# Production Skill-set resolver parity — 2026-09-07

## 位置づけ

`src/skill-set.json` を追加しても、現行 `scripts/build.py` はまだ `src/manifest.json` を直接読む単一 Skill builder である。

この状態で descriptor と builder を並存させると、両者が静かにずれる可能性がある。そのため、multi-Skill build wiringへ進む前の暫定 bridge として、descriptor から解決した production Skill が現行 builder の入力と一致することを検査する。

## Resolver

`scripts/production_skill_set.py` は production descriptor を read-only で解決する。

責務は次だけである。

1. `src/skill-set.json` を読む。
2. production Skill-set validatorを通す。
3. 各entryの `source_manifest` を読み、descriptor順で返す。

resolverは次を行わない。

- research candidateの探索
- production昇格判断
- Skill名の決定
- canonical責務移動
- host adapter metadataの合成
- OpenAI / Claude / Codex target名の選択
- runtime artifact生成
- routing

したがって、他のCSW改善レーンで `affinity-synthesis` / `iterative-inquiry-synthesis` の設計が進んでも、その存在だけでresolver結果は増えない。

## Legacy parity gate

`scripts/check_production_skill_set_legacy_parity.py` は、現行buildとの移行期間だけ次を要求する。

- production Skillはちょうど1件である。
- Skill idは `cultural-substrate-weaving` である。
- source manifestは `src/manifest.json` である。
- descriptor経由で読んだmanifest全体が、現行 `common.manifest()` の結果と等しい。

Skillが2件以上になった場合、このgateは自動追随しない。

```text
legacy production build bridge requires exactly one Skill;
replace this gate intentionally when multi-Skill build wiring is introduced
```

と失敗させる。

これはmulti-Skill化を妨げる恒久制約ではなく、**公開集合を増やす変更とbuild wiringを必ず同じ意図的変更として扱うための移行制約**である。

## 他レーンとの協調

このgateがある間、他レーンはproduction builderの都合で研究判断を急ぐ必要がない。

- one-round KJ系技能の公開名称は引き続き検討できる。
- iterative inquiryのhandoff/fallback評価を継続できる。
- CSW→Iterative→Affinityのprovenance seamを追加評価できる。
- canonical `integration.md` / `iteration.md` を保持したまま比較できる。
- en-US companion parityを後から判断できる。

逆に、このレーンは他レーンの評価途中でdescriptorへcandidateを追加しない。

## Gateを置き換える条件

legacy parity gateを削除または一般化するのは、少なくとも次の変更を同じ統合単位で確認できる段階とする。

1. production generic Skill writerが統合されている。
2. production generic Skill validatorが統合されている。
3. production descriptorから複数Skill sourceを解決するbuild pathが実装される。
4. 追加Skillのproduction inclusion判断が別途確定している。
5. host別metadata / target nameがproduction reviewed状態にある。
6. generated artifact集合の増加が意図したものとしてレビューされる。
7. package / release validatorが全追加Skillを検査する。
8. 完全checkout上で `make check` とrelease系検査を実行する。

この条件が揃うまでは、現在の単一Skill buildをdescriptorと一致させるだけに留める。

## 現段階の意味

この変更によってproduction multi-Skill化そのものが進んだわけではない。

進んだのは、

```text
research candidate
  -> explicit production inclusion decision
  -> minimal production Skill-set
  -> read-only resolver
  -> current build input parity
```

という境界線である。

この線を明示したことで、他レーンが方法論と評価を進める一方、このレーンはproduction配布の安全な受け皿だけを先に整えられる。
