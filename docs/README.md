# Documentation / ドキュメント

現在の製品が持つ本質的な価値と実装方針は、[本質価値から組み直すプロダクト構成](ja/maintainers/value-first-product-design.md)で説明しています。既存文書の検討で用いた親和図法の記録は、[文書材料の親和統合記録](ja/maintainers/value-first-material-synthesis.md)を参照してください。

本質構造の発見を深める方式とSUI資料の分析は、[表層的な発想から、本質構造を変える発見へ](ja/maintainers/generative-depth-and-product-wisdom.md)を参照してください。

多義的な体系を状況に即して読み、実務者の価値観で有益性を捉える方式は、[多義性を生かす読解と実務上の有益性](ja/maintainers/situated-polysemy-and-practical-value.md)にまとめています。

このページは、cultural-substrate-weavingの利用方法、方法論、研究、保守に関する文書を探すための案内です。

このページで方法論の意味を新たに定義することはありません。方法論の日本語の正本は`src/ja-JP/`にあり、`src/en-US/`はその英語翻訳です。`docs/`には、利用者向けの説明、研究・評価資料、保守手順と、これらの文書への案内を置いています。

> 全文書を順番に読む必要はありません。目的に応じて入口を選んでください。

## Quick navigation / クイックナビゲーション

| 目的 | 最初に読む文書 | 次に読む場所 |
| --- | --- | --- |
| 日本語で使い始める | [Getting Started — 日本語](ja/getting-started.md) | [呼ぶ側が用意するもの](ja/usage-context.md) |
| Start in English | [Getting Started — English](en/getting-started.md) | English usage docs under `en/` |
| 方法論そのものを確認する | [`src/ja-JP/ROUTER.md`](../src/ja-JP/ROUTER.md) | [`src/ja-JP/core/`](../src/ja-JP/core/) |
| 英語の方法論を確認する | [`src/en-US/ROUTER.md`](../src/en-US/ROUTER.md) | [`src/en-US/core/`](../src/en-US/core/) |
| 根幹価値と具現化方針を読む | [根幹価値と具現化方針](ja/maintainers/core-value-and-embodiment-policy.md) | [`src/ja-JP/core/discovery-pathway.md`](../src/ja-JP/core/discovery-pathway.md) |
| 改善方針・認知機能分析を読む | [スキルの全体理解と改善方針](ja/maintainers/skill-improvement-direction.md) | [長期的認知機能の分析](ja/maintainers/longitudinal-cognitive-functions.md) |
| プロダクト品質の要件・実験方針を確認する | [プロダクト品質プログラム](ja/maintainers/product-quality-program.md) | [`research/product-quality/`](../research/product-quality/) |
| 実使用での観測を見る | [Web Chat Living Lab](ja/experiments/web-chat-living-lab.md) | [`research/living-lab/observations/`](../research/living-lab/observations/) |
| 開発・リリースを行う | [開発手順](ja/maintainers/development.md) | [リリース手順](ja/maintainers/release.md) |
| 多言語・リリース内部契約を保守する | [Multilingual maintenance](maintainers/multilingual.md) | [Release internals](maintainers/release.md) |

## 文書の役割 / Document roles

| 場所 | 主な役割 | 正本性 |
| --- | --- | --- |
| `src/ja-JP/` | 方法論・実行規則・判断境界 | **意味上の正本** |
| `src/en-US/` | 日本語正本に対応する英語版 | 翻訳版。独立した第二正本ではない |
| `docs/ja/` | 日本語の利用ガイド、実験説明、maintainer向け説明 | 説明・運用文書。方法論の第二正本ではない |
| `docs/en/` | English guides and experiment documentation | English documentation; not an independent methodology authority |
| `docs/maintainers/` | 多言語生成、リリースなどの共有内部手順 | repository maintenance contract / procedure |
| `research/` | 研究、Living Lab、観測・評価材料 | 証拠・観測資料。方法論の有効性を自動的に証明しない |
| `plugins/` | 正本・アダプターから生成され、Gitで管理される配布成果物 | 生成物。手編集する方法論正本ではない |
| `dist/` | リリース用の生成物 | Git管理しない生成物 |

## 日本語で利用する / Use in Japanese

- [Getting Started](ja/getting-started.md)
- [呼ぶ側が用意するもの](ja/usage-context.md)
- [Microsoft 365 Copilot向けガイド](ja/platforms/microsoft-copilot.md)

方法論の判断基準を詳しく確認する場合は、説明文書だけで判断せず、必要に応じて[`src/ja-JP/ROUTER.md`](../src/ja-JP/ROUTER.md)と`src/ja-JP/core/`の正本を確認します。

## English usage

- [Getting Started](en/getting-started.md)
- [Web Chat Living Lab — English](en/experiments/web-chat-living-lab.md)

The English methodology under `src/en-US/` follows the Japanese semantic source. It should not be treated as a separate authority when the two diverge.

## Research and evaluation / 研究・評価

- [根幹価値と具現化方針 — 触媒的発見の経路](ja/maintainers/core-value-and-embodiment-policy.md)
- [スキルの全体理解と改善方針](ja/maintainers/skill-improvement-direction.md)
- [文化体系とKJ法による認知機能の定性的解析と再現設計](ja/maintainers/longitudinal-cognitive-functions.md)
- [v0.5.0の段階的なプロンプト改善](ja/maintainers/v05-cognitive-prompt-roadmap.md)
- [プロダクト品質を育てるための要件・設計・実験プログラム](ja/maintainers/product-quality-program.md)
- [Web Chat Living Lab — 日本語](ja/experiments/web-chat-living-lab.md)
- [Web Chat Living Lab — English](en/experiments/web-chat-living-lab.md)
- [公開観測記録](../research/living-lab/observations/)
- [プロダクト品質の監査・実験記録](../research/product-quality/)

研究や観測の文書では、事前に計画した観測（`prospective`）と事後に整理した観測（`retrospective`）、対象に関する証拠、未測定の効果を区別します。観測の記録があるというだけで、このスキル全体の有効性が確立したとはみなしません。

## Maintainers / 保守

### Procedures / 手順

- [開発手順 — 日本語](ja/maintainers/development.md)
- [リリース手順 — 日本語](ja/maintainers/release.md)
- [Development procedure — English](en/maintainers/development.md)
- [Release procedure — English](en/maintainers/release.md)

### Shared internals / 共通の内部資料

- [Multilingual maintenance](maintainers/multilingual.md)
- [Release internals](maintainers/release.md)
- [Release history](maintainers/release-history.md)

## 読むときの境界 / Reading boundaries

```text
user-facing explanation
  != methodology authority

translated text
  != independent semantic source

research observation
  != established effectiveness

generated plugin / release artifact
  != hand-edited source of truth
```

方法論の意味や運用の規則を変更する場合は、まず対応する正本や契約を更新します。この案内には、読む順序や参照先に関わる変更だけを反映します。
