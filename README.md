# cultural-substrate-weaving

[日本語](README.md) | [English](README.en.md)

**文化体系の視点から対象の本質構造を捉え直し、発見を使える問い・比較・構成へ具体化する補助AIスキル**です。研究者が異質な概念との出会いから深い発見をする体験を出発点に、文化的・思想的・伝統的体系を一時的な認知場として開きます。問題群の共通性や違いを読み直す働きと、体系固有の操作から新しい問いを得る働きを、依頼に合わせて組み合わせます。

> **このresearch branchでは方法分離を試験中です。** 日本語canonical sourceと英語CSW runtimeでは、一回の材料統合を `affinity-synthesis`、複数roundの差分再開を `iterative-inquiry-synthesis` という独立Methodへ委ねるthin-CSW構造を適用しました。2つのsibling prototypeには、日本語research realizationに加えて英語の `SKILL.en.md` と `METHOD.en.md` の初期版も置いています。これはまだ公開済みの三Skill構成を意味しません。CSWの配布物は再生成しますが、三スキルの公開配布、英語prototypeの独立査読、補助的なresearch reference / evalの言語整理は未完です。

本リポジトリの方法群は、執筆、経営、ソフトウェア開発、法務などの領域固有知識や品質基準を置き換えません。必要な領域能力は、依頼側のコンテキストまたは併用する領域スキルから受け取ります。

> **現在は検証段階です。** v0.4.0でWeb Chat Living Labを導入し、公開済み方法論を実作業の中で観測しています。公開記録には、あらかじめ観測系を置いたprospectiveな記録と、自然な作業を後から匿名化・抽象化したretrospectiveな記録を区別して含めています。公開観測はまだ限定的であり、現時点で方法の有効性が確立したとは扱いません。→ **[Web Chat Living Lab](docs/ja/experiments/web-chat-living-lab.md)** / **[公開観測記録](research/living-lab/observations/)**

## Research branchの三層

```text
cultural-substrate-weaving
  文化体系を開く
  → framework由来候補の帰属を保つ
  → 対象へ戻す

        ↕ optional material / handoff

affinity-synthesis   [research prototype]
  一回の材料主導統合
  → card / group / label / relation
  → 図解 ↔ 叙述 ↔ 元材料の照合

        ↕ optional delta / residual

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

## 根幹価値

> **見方を変え、対象の構造を読み直し、得られた発見を人間の思索と具体的な構成へつなぐ。**

本質構造は、今回の目的に照らして対象の成り立ちや違いを説明する、関係・条件・変化のまとまりです。文化体系は問題群を見渡す視点を与えます。その視点で各対象の位置づけを説明します。複数の視点を交差させるときは、概念の重なりや相互依存ができるだけ小さく、独立性の高い要素を切り出せる組み合わせを選びます。

直交性の判断では、数学的直交性や統計的独立性との近似性を重視します。五行と五大は、その意図を示す直交性の高い組み合わせです。選定や配置は、資料と人的な判断にもとづく定性的な見立てとして理由を示します。数値化や新しい実験を前提にはせず、数理的な証明や統計的な実測とは分けて記します。

体系自身の分節、関係、変化、実践を読み、対象の資料、具体例、例外へ戻して見立てを修正します。既存文書、関連研究、人間の経験や判断も使い、実証実験を毎回の必須条件にはしません。判断まで委ねられていれば、理由を添えて最適と思われる具体案を選びます。

実行本文と配布構成をこの価値から組み直しました。親和図法による材料統合と複数回の継続管理は別スキルの責務です。日本語の仕上げには、利用可能で依頼に合う場合、外部の`yomiyasu`を併用できます。いずれもCSWの必須依存にはしません。詳しくは[本質価値から組み直すプロダクト構成](docs/ja/maintainers/value-first-product-design.md)と[文書材料の親和統合記録](docs/ja/maintainers/value-first-material-synthesis.md)を参照してください。

## 中核原則

CSW側の中核は次です。

> **外部体系から得た構造は対象へ返して確かめる。対象側の材料によって独立に支えられた部分だけを、対象についての所見として扱う。**

`affinity-synthesis`は、親和図法による材料主導の統合を担う別スキルの研究実現です。手法の系譜と生成AI向けの補正は、[方法定義](research/skill-prototypes/affinity-synthesis/references/METHOD.md)と研究資料に残しています。その境界判断の中心は次です。

> **意味の一体性を守るためには結合し、証拠状態を守るためには分割する。**

公開の方式名には「親和図法」を使います。由来となった手法の公式実装や完全再現を称するものではありません。

## なぜ外部体系を使うのか（機序の仮説）

文化的体系が「正しい」ことを主張するものではありません。対象を見る前から存在する位置・関係・遷移を、通常分析とは異なる探索方向を生む事前構造として利用する、という仮説です。ここで体系は触媒として働きます。触媒は反応を促しますが、生成物の成分にはなりません。調査・診断では、体系は発見の触媒であって、所見の根拠ではありません。

体系名や対応表を外した後も、意味のある問い・仮説・記述として残ることはあります。ただし、それは体系の権威から切り離せたことを示すだけであり、それ自体で対象側の証拠が増えたことにはなりません。調査・診断では、対象側の資料・観察・反証によって独立に支えられた部分だけを所見として扱います。生成・構成では、文化体系から生じた構造を構成資源として採用できますが、対象についての事実とは区別します。

体系を使わない基準線との差は、問い、探索先、成果物、判断などに何が増えたかを見る材料にはできますが、件数だけで方法の有効性を証明しません。

## ライセンス

MIT License
