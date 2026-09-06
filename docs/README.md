# Documentation / ドキュメント

このページは、cultural-substrate-weavingの利用・方法論・研究・保守文書を読むための**案内板**です。

ここで方法論の意味を新たに定義しません。日本語の方法論正本は`src/ja-JP/`、英語は`src/en-US/`の翻訳版です。`docs/`は利用者向け説明、研究・評価、保守手順を読みやすく案内するための文書群です。

> 全文書を順番に読む必要はありません。目的に応じて入口を選んでください。

## Quick navigation / クイックナビゲーション

| 目的 | 最初に読む文書 | 次に読む場所 |
| --- | --- | --- |
| 日本語で使い始める | [Getting Started — 日本語](ja/getting-started.md) | [呼ぶ側が用意するもの](ja/usage-context.md) |
| Start in English | [Getting Started — English](en/getting-started.md) | English usage docs under `en/` |
| 方法論そのものを確認する | [`src/ja-JP/ROUTER.md`](../src/ja-JP/ROUTER.md) | [`src/ja-JP/core/`](../src/ja-JP/core/) |
| 英語の方法論を確認する | [`src/en-US/ROUTER.md`](../src/en-US/ROUTER.md) | [`src/en-US/core/`](../src/en-US/core/) |
| 改善方針・認知機能分析を読む | [スキルの全体理解と改善方針](ja/maintainers/skill-improvement-direction.md) | [長期的認知機能の分析](ja/maintainers/longitudinal-cognitive-functions.md) |
| 実使用での観測を見る | [Web Chat Living Lab](ja/experiments/web-chat-living-lab.md) | [`research/living-lab/observations/`](../research/living-lab/observations/) |
| 開発・リリースを行う | [開発手順](ja/maintainers/development.md) | [リリース手順](ja/maintainers/release.md) |
| 多言語・release内部契約を保守する | [Multilingual maintenance](maintainers/multilingual.md) | [Release internals](maintainers/release.md) |

## 文書の役割 / Document roles

| 場所 | 主な役割 | 正本性 |
| --- | --- | --- |
| `src/ja-JP/` | 方法論・実行規則・判断境界 | **意味上の正本** |
| `src/en-US/` | 日本語正本に対応する英語版 | 翻訳版。独立した第二正本ではない |
| `docs/ja/` | 日本語の利用ガイド、実験説明、maintainer向け説明 | 説明・運用文書。方法論の第二正本ではない |
| `docs/en/` | English guides and experiment documentation | English documentation; not an independent methodology authority |
| `docs/maintainers/` | 多言語生成、release等の共有内部手順 | repository maintenance contract / procedure |
| `research/` | 研究、Living Lab、観測・評価材料 | Evidence / observation material。方法論の有効性を自動的に証明しない |
| `plugins/` | sourceから生成されGit管理される配布成果物 | generated artifact。手編集の方法論正本ではない |
| `dist/` | release用生成物 | generated release output。Git管理しない |

## 日本語で利用する / Use in Japanese

- [Getting Started](ja/getting-started.md)
- [呼ぶ側が用意するもの](ja/usage-context.md)
- [Microsoft 365 Copilot向けガイド](ja/platforms/microsoft-copilot.md)

方法論の細かな判断基準を確認するときは、説明文書だけで完結させず、必要に応じて[`src/ja-JP/ROUTER.md`](../src/ja-JP/ROUTER.md)と`src/ja-JP/core/`へ戻ります。

## English usage

- [Getting Started](en/getting-started.md)
- [Web Chat Living Lab — English](en/experiments/web-chat-living-lab.md)

The English methodology under `src/en-US/` follows the Japanese semantic source. It should not be treated as a separate authority when the two diverge.

## Research and evaluation / 研究・評価

- [スキルの全体理解と改善方針](ja/maintainers/skill-improvement-direction.md)
- [文化体系とKJ法による認知機能の定性的解析と再現設計](ja/maintainers/longitudinal-cognitive-functions.md)
- [v0.5.0の段階的なプロンプト改善](ja/maintainers/v05-cognitive-prompt-roadmap.md)
- [Web Chat Living Lab — 日本語](ja/experiments/web-chat-living-lab.md)
- [Web Chat Living Lab — English](en/experiments/web-chat-living-lab.md)
- [公開観測記録](../research/living-lab/observations/)

研究・観測文書は、prospective / retrospective、対象側Evidence、未測定の効果等の区別を保持します。観測記録が存在することだけで、本スキル全体の有効性が確立したとは扱いません。

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

意味や運用が変わった場合は、まず対応する正本・契約を更新し、この案内板は読み手導線だけを追随させます。
