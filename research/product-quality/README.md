# Product Quality Research

このディレクトリは、CSWの**プロダクト品質を観測・検証するための監査記録と制御実験**を置く場所です。

方法論そのものの意味上の正本ではありません。日本語の方法論正本は`src/ja-JP/`、research prototypeの機械可読な契約は`research/skill-prototypes/`にあります。

## ここに置くもの

- 現行品質証拠のcoverage audit
- 制御されたbehavioral experimentのprotocol
- experiment runの観測記録
- 既知failureから切り出した回帰候補
- quality requirementと証拠の対応記録

## ここに置かないもの

- 新しい方法論規則の第二正本
- AI自己採点だけで成立する「品質スコア」
- Living Labの自然利用記録のコピー
- production promotionを自動承認する判定

## 証拠の扱い

品質証拠は最低限、次を区別します。

1. **static / deterministic evidence** — repository contract、validator、schema、生成物一致など
2. **controlled behavioral evidence** — 固定packetと不変条件を用いたモデル実行
3. **natural-work evidence** — Living Lab等の自然な実作業から得た観測
4. **interpretation** — 人間・AI・外部評価者による解釈

static checkが通ったことをモデル行動の保証とみなさず、単発の良いモデル出力を方法論全体の有効性ともみなしません。

## 命名

- 監査: `YYYY-MM-DD-<topic>-audit.md`
- 実験protocol: `experiment-NNN-<topic>.md`
- 実行記録: `experiment-NNN-run-YYYY-MM-DD[-suffix].md`

実行記録では、可能な限りsource commit、visible model / product mode / tools、入力packet、出力artifact、must-pass invariant、diagnostic observation、評価者の来歴を残します。

## 現在の入口

- [`2026-09-11-quality-evidence-audit.md`](2026-09-11-quality-evidence-audit.md) — E0: 現行品質証拠の初回監査
- [`experiment-001-handoff-integrity.md`](experiment-001-handoff-integrity.md) — E3: CSW → affinity synthesis → iterative inquiryのhandoff integrity protocol
- [`experiment-001-run-2026-09-11-engineering.md`](experiment-001-run-2026-09-11-engineering.md) — E3 Run 001: 同一contextでのengineering trial
- [`../../docs/ja/maintainers/product-quality-program.md`](../../docs/ja/maintainers/product-quality-program.md) — 品質要件・検証層・実験ポートフォリオ全体

## 現在の実験状態

Run 001ではH1〜H6を外部artifactとして検査でき、明白なMethod contract違反は観測されませんでした。ただしprotocol作成・実行・評価が同じAI contextにあるため、behavioral reliabilityの強い証拠とは扱いません。

Run 001から得た具体的なprotocol補正は、`carried-untouched`と`=`（touched and explicitly checked, but semantically unchanged）を分けることです。次はfresh execution / separate evaluationのRun 002を優先します。

## 改善へ反映するとき

観測からruntimeや正本を変える場合は、先にfailure modeを明示します。既存規則の言い換えで済むのか、fixture追加で済むのか、実際に方法の変更が必要なのかを分けます。

重大なfailureが再現できる場合は、まず再現packetを最小化し、可能なら回帰fixtureへ落とします。実験で良い結果が出たことだけを理由にresearch prototypeのpromotion gateを迂回しません。
