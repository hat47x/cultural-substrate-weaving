# cultural-substrate-weaving

[日本語](README.md) | [English](README.en.md)

文筆・設計・分析・開発など、あらゆる「構造」を扱う領域でメタ認知を高め、対象固有の関係・接続の欠落・反作用・時間差・不可逆性を探索、検証、変換する汎用的なAI方法論です。

文化的・思想的・伝統的体系は中核目的ではなく、通常の領域固有手法だけでは捉えにくい構造を探索するための、選択的な補助モデルとして扱います。

## 対応言語

| 言語 | 状態 | 備考 |
|---|---|---|
| 日本語 (`ja-JP`) | 意味上の正本 | 方法論の判断基準となる版 |
| English (`en-US`) | 翻訳版 | 利用可能。権威的な公開前には独立した人手査読を推奨 |

## 対応プラットフォーム

- OpenAI Codex Skill（暗黙発動版／明示発動版）
- Claude Code Plugin Marketplace
- ChatGPT custom GPT更新パック
- Microsoft 365 Copilot declarative agent
- `AGENTS.md`／`CLAUDE.md`からの参照

## 初めて使う方

| 利用先 | 日本語ガイド | English guide |
|---|---|---|
| Codex | [Codexで使う](docs/ja/platforms/codex.md) | [Use with Codex](docs/en/platforms/codex.md) |
| Claude Code | [Claude Codeで使う](docs/ja/platforms/claude-code.md) | [Use with Claude Code](docs/en/platforms/claude-code.md) |
| ChatGPT GPTs | [カスタムGPTを作る](docs/ja/platforms/chatgpt-gpt.md) | [Create a custom GPT](docs/en/platforms/chatgpt-gpt.md) |
| Microsoft 365 Copilot | [Copilot Agentを作る](docs/ja/platforms/microsoft-copilot.md) | [Create a Copilot agent](docs/en/platforms/microsoft-copilot.md) |

## ビルド

Python 3.11以上が必要です。外部Pythonパッケージは不要です。

```bash
git clone https://github.com/OWNER/cultural-substrate-weaving.git
cd cultural-substrate-weaving
make check
make package
```

成果物は`dist/<locale>/`と`dist/packages/`に生成されます。

## 正本・翻訳・生成物

- `src/ja-JP/`: 意味上の正本
- `src/en-US/`: 同じ構造を持つ英語翻訳
- `i18n/`: 用語集、翻訳元ハッシュ、査読方針
- `adapters/`: プラットフォームと言語ごとのテンプレート
- `scripts/`: 多言語成果物の生成・検証
- `plugins/`: Claude Marketplace用に生成され、Git管理する成果物
- `dist/`: リリース用生成物。Git管理しない

## 中核原則

> 外部体系から得た構造は、対象へ返して検証する。残った構造は、体系ではなく対象に属する。

## ライセンス

MIT Licenseです。公開者情報、Microsoft 365 Agentのプライバシーポリシー等は、公開前に実際の情報へ置き換えてください。
