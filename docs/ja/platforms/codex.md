# Codexで使う

本方法論は事実確認や文脈収集をWeb検索に依存する場面があります。Codexのネットワークアクセス／Web検索ツールが利用可能な設定になっていることを確認してください。

## 最も簡単な方法（Codex CLI・IDE拡張）

ローカルマシンで動くCodex CLIとIDE拡張は、同じファイルシステムからスキルを読みます。

1. GitHub Releasesから`openai-skill-metered`または`openai-skill-interactive`のZIPを取得します。
2. 展開した`cultural-substrate-weaving`フォルダーを、個人利用なら`~/.agents/skills/`、プロジェクト共有ならリポジトリの`.agents/skills/`へ置きます。
3. Codexを再起動します。

## Codexクラウドで使う場合

Codexクラウドのタスクは、リポジトリをクローンしたサンドボックスで動作するため、ローカルの`~/.agents/skills/`（個人用）は参照されません。クラウドで使うには、対象リポジトリの`.agents/skills/`へスキルフォルダーをコミットしてください。

## どちらを選ぶか

- **metered**: 明示した場合だけ起動します。従量課金・利用量制限を重視する場合の推奨です。
- **interactive**: 関連する依頼で暗黙起動できます。定額利用や探索的作業向けです。

## 使い方

```text
$cultural-substrate-weaving この制度案の責任、情報流、不可逆性を検査してください。
```

単純な校正、定型実装、局所的バグ修正では使用しません。

## AGENTS.mdとの組み合わせ

`adapters/project-integrations/codex/AGENTS.fragment.md`の短い入口だけを対象リポジトリの`AGENTS.md`へ追加します。方法論全文は置かないでください。
