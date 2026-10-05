# Cultural Substrate Weaving — 日本語

文化体系の視点から対象や問題群の本質構造を捉え直し、発見を問い・比較・構成へ具体化する補助スキルです。既存資料と定性的な判断を使い、対象側へ戻して読みを修正します。親和図法の材料統合と複数回の継続管理は、利用可能な別スキルへ委ねます。

Version {{VERSION}} · MIT · [リポジトリ](https://github.com/hat47x/cultural-substrate-weaving)

## インストール

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
claude plugin install cultural-substrate-weaving-ja@cultural-substrate-weaving
```

## 使い方

**明示呼び出し専用**です。

```text
/cultural-substrate-weaving-ja:weave <依頼内容>
```

本スキルは領域固有の専門知識を置き換えません。必要に応じて、領域固有スキルで基準線を作ったうえで併用してください。

依頼の例は次のとおりです。

- `この問題群を異なる文化体系の視点で読み直し、共通構造と違いを整理してください。`
- `既存文書から本質価値を捉え直し、それを体現する具体的な構成案を選んでください。`

体系由来の問いや構成案と、対象についての事実は区別します。実証実験を毎回の必須段階にはしません。親和図法の材料統合を担う`affinity-synthesis`などの別スキルは、この配布物に含まれません。体癖は、明示指定または身体的一貫性そのものが探索対象の場合に限定して扱います。日本語の仕上げには、利用可能で依頼に合う場合、外部の`yomiyasu`を併用できます。

## ドキュメント

- [Claude Codeで使う](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/ja/platforms/claude-code.md)
- [Codexで使う](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/ja/platforms/codex.md)
- [アーキテクチャ](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/ja/architecture.md)
