# Cultural Substrate Weaving — 日本語

文化的体系による構造候補とKJ法による断片統合を組み合わせ、通常分析にない問い・関係・空白を探索し、対象側で検証する補助スキルです。

Version 0.5.0 · MIT · [リポジトリ](https://github.com/hat47x/cultural-substrate-weaving)

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

例:
- `この材料をKJ法で統合し、既成分類では見えない関係と空白を探してください。`
- `通常分析を基準線に、文化的体系を限定適用して新しい問いが生じるか確認してください。`

文化的体系は予言・診断の真理としてではなく構造候補の供給源として扱い、最後に対象側へ返して検証します。Taihekiは明示指定または身体的一貫性そのものが探索対象の場合にのみ限定適用します。

## ドキュメント

- [Claude Codeで使う](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/ja/platforms/claude-code.md)
- [Codexで使う](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/ja/platforms/codex.md)
- [アーキテクチャ](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/ja/architecture.md)
