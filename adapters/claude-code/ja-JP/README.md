# Cultural Substrate Weaving — 日本語

文化的体系を一時的な認知場として開き、そこから生じた問い・関係・対応候補の由来を保ったまま対象側へ戻して検証する補助スキルです。多数・異種材料の親和統合や複数roundの差分再開が必要な場合は、利用可能なcompatible realizationへ委ねます。

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

例:
- `通常分析を基準線に、文化的体系を限定適用して新しい問いが生じるか確認してください。`
- `文化体系から生じた対応候補を、対象側の材料へ戻して支持・反証を分けてください。`

文化的体系は予言・診断の真理としてではなく構造候補の供給源として扱い、最後に対象側へ返して検証します。KJ法・親和図法・質的統合法に由来する材料統合技能は、research branchでは独立Methodとして分離中です。Taihekiは明示指定または身体的一貫性そのものが探索対象の場合にのみ限定適用します。

## ドキュメント

- [Claude Codeで使う](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/ja/platforms/claude-code.md)
- [Codexで使う](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/ja/platforms/codex.md)
- [アーキテクチャ](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/ja/architecture.md)
