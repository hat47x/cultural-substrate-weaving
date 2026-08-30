# cultural-substrate-weaving

[日本語](README.md) | [English](README.en.md)

**文化的・思想的・伝統的体系による構造候補の供給**と、**KJ法による断片統合・空白探索**を組み合わせ、通常の領域手法では立ち上がりにくい問い・関係・状態・遷移候補を探索し、対象側で検証する補助スキルです。

本スキルは、執筆、経営、ソフトウェア開発、法務などの領域固有知識や品質基準を置き換えません。必要に応じて**領域固有スキルと併用**し、本スキルは文化的体系とKJ法から生じる増分を担当します。

> **現在は検証段階です。** v0.4.0開発線では、Webチャット上の実作業を対象とするprospectiveなLiving Lab観測を開始しています。公開観測はまだ限定的であり、現時点で本スキルの有効性が確立したとは扱いません。→ **[Web Chat Living Lab](docs/ja/experiments/web-chat-living-lab.md)** / **[公開観測記録](research/living-lab/observations/)**

## インストール

**Claude Code**

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
claude plugin install cultural-substrate-weaving-ja@cultural-substrate-weaving
```

**Codex**

```bash
codex plugin marketplace add hat47x/cultural-substrate-weaving
```

追加後に`cultural-substrate-weaving-ja`（英語版は`cultural-substrate-weaving-en`）をインストールします。

**ChatGPT custom GPT / Microsoft 365 Copilot**はGitHub Releasesから言語とプラットフォームに対応するZIPを取得してください。

## 呼ぶ側が用意するもの

本スキルは領域固有の専門能力を提供しません。課題の専門的な正確性、品質基準、実装手順、文体などは、依頼側のコンテキストまたは併用する領域スキルが担います。→ **[呼ぶ側が用意するもの](docs/ja/usage-context.md)**

## 対応言語

| 言語 | 状態 | 備考 |
|---|---|---|
| 日本語 (`ja-JP`) | 意味上の正本 | 方法論の判断基準となる版 |
| English (`en-US`) | 翻訳版 | 利用可能。権威的な公開前には独立した人手査読を推奨 |

## 対応プラットフォーム

- OpenAI Codex Plugin / 直接配置Skill
- Claude Code Plugin Marketplace
- ChatGPT custom GPT更新パック
- Microsoft 365 Copilot declarative agent
- `AGENTS.md`／`CLAUDE.md`からの参照

## ビルド

Python 3.11以上が必要です。外部Pythonパッケージは不要です。

```bash
git clone https://github.com/hat47x/cultural-substrate-weaving.git
cd cultural-substrate-weaving
make check
make package
```

## 正本・翻訳・生成物

- `src/ja-JP/`: 意味上の正本
- `src/en-US/`: 同じ構造を持つ英語翻訳
- `i18n/`: 用語集、翻訳元ハッシュ、査読方針
- `adapters/`: プラットフォームと言語ごとのテンプレート
- `scripts/`: 多言語成果物の生成・検証
- `plugins/`: 生成され、Git管理する成果物
- `dist/`: リリース用生成物。Git管理しない

## 中核原則

> **外部体系から得た構造は、対象へ返して検証する。残った構造は、体系ではなく対象に属する。**

KJ法では、材料を先験的な種類へ押し込めず、意味の一体性と証拠状態を保ちながら統合します。

> **意味の一体性を守るためには結合し、証拠状態を守るためには分割する。**

## なぜ外部体系を使うのか（機序の仮説）

文化的体系が「正しい」ことを主張するものではありません。対象を見る前から存在する位置・関係・遷移を、通常分析とは異なる探索方向を生む事前構造として利用する、という仮説です。

最終的には体系名や対応表を除去し、なお対象について成立する所見だけを残します。体系を使わない基準線と比べて生存所見が増えない場合、本スキル固有の増分は確認できません。

## ライセンス

MIT License
