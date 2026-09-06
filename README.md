# cultural-substrate-weaving

[日本語](README.md) | [English](README.en.md)

**文化的・思想的・伝統的体系を一時的な認知場として開き、そこから得た問い・関係・状態・遷移候補を対象へ戻して確かめる**補助AIスキルです。文化体系を答えや分類器として固定せず、対象側の材料で独立に支えられた部分だけを対象所見として扱います。

> **このresearch branchでは方法分離を試験中です。** 日本語canonical sourceと英語CSW runtimeでは、一回の材料統合を `affinity-synthesis`、複数roundの差分再開を `iterative-inquiry-synthesis` という独立Methodへ委ねるthin-CSW構造を適用しました。2つのsibling prototypeには、日本語research realizationに加えて英語の `SKILL.en.md` と `METHOD.en.md` の初期版も置いています。これはまだ公開済みの三Skill構成を意味しません。生成distributionのmulti-skill化・再build、英語prototypeの独立査読、補助的なresearch reference / evalの言語整理は未完です。

本リポジトリの方法群は、執筆、経営、ソフトウェア開発、法務などの領域固有知識や品質基準を置き換えません。必要な領域能力は、依頼側のコンテキストまたは併用する領域スキルから受け取ります。

> **現在は検証段階です。** v0.4.0でWeb Chat Living Labを導入し、公開済み方法論を実作業の中で観測しています。公開記録には、あらかじめ観測系を置いたprospectiveな記録と、自然な作業を後から匿名化・抽象化したretrospectiveな記録を区別して含めています。公開観測はまだ限定的であり、現時点で方法の有効性が確立したとは扱いません。→ **[Web Chat Living Lab](docs/ja/experiments/web-chat-living-lab.md)** / **[公開観測記録](research/living-lab/observations/)**

## Research branchの三層

```text
cultural-substrate-weaving
  文化体系を開く
  → framework由来候補の帰属を保つ
  → 対象へ戻す

        ↓ material / handoff

affinity-synthesis   [research prototype]
  一回の材料主導統合
  → card / group / label / relation
  → 図解 ↔ 叙述 ↔ 元材料の照合

        ↓ delta / residual

iterative-inquiry-synthesis   [research prototype]
  複数roundの差分再開
  → touched artifactだけを必要に応じてreopen
  → 履歴・残差・停止／再開条件を保持
```

方法定義とAgent Skill realizationは分けています。将来、既存の外部Skillが同じ不変条件と評価fixtureを満たすなら、独自realizationを縮小・置換できる設計を目指しています。

## インストール

以下は現在の `cultural-substrate-weaving` 配布物の利用方法です。research prototypeの `affinity-synthesis` / `iterative-inquiry-synthesis` を独立公開済みとみなさないでください。

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

**ChatGPT custom GPT / Microsoft 365 Copilot**はGitHub Releasesから言語とプラットフォームに対応するZIPを取得してください。Microsoft 365版は、現時点では`instructions.txt`に収録された範囲を実行指示として扱う限定的な対応です。詳細は[Microsoft 365 Copilot向けガイド](docs/ja/platforms/microsoft-copilot.md)を参照してください。

## 呼ぶ側が用意するもの

本方法群は領域固有の専門能力を提供しません。課題の専門的な正確性、品質基準、実装手順、文体などは、依頼側のコンテキストまたは併用する領域スキルが担います。→ **[呼ぶ側が用意するもの](docs/ja/usage-context.md)**

## 対応言語

| 言語 | 状態 | 備考 |
|---|---|---|
| 日本語 (`ja-JP`) | 意味上の正本 | thin-CSWと2つのresearch sibling realizationの正本 |
| English (`en-US`) | translated draft | thin-CSW runtimeは翻訳済み。2 sibling Skillのruntime / Method Definition初期英訳も追加済み。独立査読と補助research資料の整理は未完 |

## 対応プラットフォーム

- OpenAI Codex Plugin / 直接配置Skill
- Claude Code Plugin Marketplace
- ChatGPT custom GPT更新パック
- Microsoft 365 Copilot declarative agent（現行は限定対応。詳細はプラットフォームガイドを参照）
- `AGENTS.md`／`CLAUDE.md`からの参照

## ビルド

Python 3.11以上が必要です。外部Pythonパッケージは不要です。

```bash
git clone https://github.com/hat47x/cultural-substrate-weaving.git
cd cultural-substrate-weaving
make research-skill-check   # split-method prototypeを変更した場合
make check
make package
```

GitHub Actionsは現在使用していません。ローカルまたは同等の実行環境で検証します。

## 正本・翻訳・生成物

- `src/ja-JP/`: CSW runtimeの意味上の正本
- `src/en-US/`: CSW runtimeの英語翻訳
- `research/skill-prototypes/`: 分離中のMethod Definition / Skill realization / eval / representation。日本語research正本と英語realization draftを含む
- `i18n/`: 用語集、翻訳元ハッシュ、査読方針
- `adapters/`: プラットフォームと言語ごとのテンプレート
- `scripts/`: 多言語成果物の生成・検証
- `plugins/`: 生成され、Git管理する成果物
- `dist/`: リリース用生成物。Git管理しない

## 中核原則

CSW側の中核は次です。

> **外部体系から得た構造は対象へ返して確かめる。対象側の材料によって独立に支えられた部分だけを、対象についての所見として扱う。**

`affinity-synthesis` の研究Method Definitionでは、KJ法・親和図法・質的統合法の系譜を参照しつつ、生成AI向けの補正を独立して記述しています。その境界判断の中心は次です。

> **意味の一体性を守るためには結合し、証拠状態を守るためには分割する。**

KJ法は株式会社川喜田研究所の登録商標です。本prototypeはKJ法の公式Agent Skillまたは完全再現を称しません。

## なぜ外部体系を使うのか（機序の仮説）

文化的体系が「正しい」ことを主張するものではありません。対象を見る前から存在する位置・関係・遷移を、通常分析とは異なる探索方向を生む事前構造として利用する、という仮説です。

体系名や対応表を外した後も、意味のある問い・仮説・記述として残ることはあります。ただし、それは体系の権威から切り離せたことを示すだけであり、それ自体で対象側の証拠が増えたことにはなりません。調査・診断では、対象側の資料・観察・反証によって独立に支えられた部分だけを所見として扱います。生成・構成では、文化体系から生じた構造を構成資源として採用できますが、対象についての事実とは区別します。

体系を使わない基準線との差は、問い、探索先、成果物、判断などに何が増えたかを見る材料にはできますが、件数だけで方法の有効性を証明しません。

## ライセンス

MIT License
