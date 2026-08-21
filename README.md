# cultural-substrate-weaving

[日本語](README.md) | [English](README.en.md)

文筆・設計・分析・開発など、あらゆる「構造」を扱う領域でメタ認知を高め、対象固有の関係・接続の欠落・反作用・時間差・不可逆性を探索、検証、変換する汎用的なAI方法論です。

文化的・思想的・伝統的体系は中核目的ではなく、通常の領域固有手法だけでは捉えにくい構造を探索するための、選択的な補助モデルとして扱います。

## インストール

**Claude Code**（このリポジトリがそのままPlugin Marketplaceです。ダウンロード不要）

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
```

```bash
claude plugin install csw-method-ja@cultural-substrate-weaving
```

英語版は`csw-method-en@cultural-substrate-weaving`。呼び出しは`/csw-method-ja:cultural-substrate-weaving-ja`です。Desktop・クラウドセッション・チーム共有の手順は[Claude Codeで使う](docs/ja/platforms/claude-code.md)にあります。

**Codex**（同じリポジトリがCodexのPlugin Marketplaceでもあります。ダウンロード不要）

```bash
codex plugin marketplace add hat47x/cultural-substrate-weaving
```

追加後に`csw-method-ja`（英語版は`csw-method-en`）をインストールします。詳細は[Codexで使う](docs/ja/platforms/codex.md)。

**ChatGPT custom GPT / Microsoft 365 Copilot**は[GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases)から言語とプラットフォームに対応するZIPを取得してください。手順は下の表のガイドにあります。

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
git clone https://github.com/hat47x/cultural-substrate-weaving.git
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

## なぜ外部体系を使うのか（機序の仮説）

本方法論は、文化的・思想的・伝統的体系が「正しい」ことを主張しません。**機械学習の転移学習に相当する作用を仮説として置いています。**

転移学習では、大量の源ドメインで事前学習した表現を、データの乏しい目標ドメインへ持ち込みます。事前学習された表現そのものが正しいかではなく、**目標ドメインでの性能が上がるか**で価値が決まります。

| 転移学習 | 本方法論 |
|---|---|
| 事前学習コーパス | 文化的体系（多数の対象を通過して残った構造） |
| 事前学習された表現 | **位置の層**：対象を見る前に意味が定義された、数の決まった置き場所 |
| 帰納バイアス（事前分布） | 対象自身が持たない位置を供給する |
| 目標ドメインでの微調整 | **割当**と、対象側での検証 |
| ドメイン不一致の検査 | **同種性**：単位の種類と分類原理が合うか |
| 負の転移 | **過剰適用**：合わない構造を押し付ける |
| アブレーション | **除去検査**：体系の語彙を全部消し、なお成立する所見を数える |
| 事前学習部分の保持／破棄 | 採用状態：反映／内部足場／補助模型／不採用 |

仮説の要点は二つです。

1. **単一の対象からは誘導できない構造を、事前分布として持ち込める。** 文化的体系は多数の対象を通過して淘汰された構造なので、この性質を持つと考えます。
2. **最も有用な出力は、事前分布と対象が食い違う場所である。** 位置が埋まらないこと自体が所見になります。空白の検出が主産物であるのはこのためです。

**これは仮説であって、測定された主張ではありません。** 反証条件は、除去検査を通過した所見が基準線を上回らないことです。体系を使わない基準線と比べて生存所見が増えないなら、転移は起きていません。本方法論は、この比較を毎回要求します。

## ライセンス

MIT License
