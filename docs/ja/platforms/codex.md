# Codexで使う

現在の事実、外部文脈、追加の出典探索が必要な課題では、Codexのネットワークアクセス／Web検索が利用できることを確認してください。手元の資料やリポジトリだけで完結するKJ統合・構造探索では必須ではありません。検索を使えない場合は、不足する外部事実を推測で補わないようにします。

## 推奨：プラグインとして導入

OpenAIでは現在、プラグインがChatGPTとCodexのワークフロー機能を発見・配布する主要な単位です。このリポジトリはCodex用のplugin marketplaceを含むため、ZIPを手作業で展開せずに導入できます。

```bash
codex plugin marketplace add hat47x/cultural-substrate-weaving
codex plugin add cultural-substrate-weaving-ja@cultural-substrate-weaving
```

英語版は`cultural-substrate-weaving-en`です。利用可能なmarketplaceやpluginは、必要に応じて次で確認できます。

```bash
codex plugin marketplace list
codex plugin list
```

Claude Code版と同じpluginディレクトリを共有しており、`.codex-plugin/plugin.json`と`.claude-plugin/plugin.json`の両方を持ちます。

## スキル形式（直接配置）

standalone skill形式も、直接配置・既存環境との互換・他製品との可搬性が必要な場合に利用できます。プラグインを主要な導入経路としつつ、skill ZIPを一律に無効・非推奨とは扱いません。

ローカルマシンで動くCodex CLIとIDE拡張でskill配置を使う場合:

1. GitHub Releasesから`openai-skill-metered`または`openai-skill-interactive`のZIPを取得します。
2. 展開した`cultural-substrate-weaving`フォルダーを、個人利用なら`~/.agents/skills/`、プロジェクト共有ならリポジトリの`.agents/skills/`へ置きます。
3. Codexを再起動または新しいセッションで読み込みます。

## Codexクラウドで使う場合

Codexのクラウドタスクでは、ローカルマシンの`~/.agents/skills/`がそのまま見えるとは前提にしません。対象リポジトリへskillを配置する場合は`.agents/skills/`を使い、pluginを使う場合は、そのCodex surfaceで利用可能なplugin設定・Sources/Plugins UI・workspace policyに従ってください。

## どちらを選ぶか

- **Plugin**: 現在の推奨導入経路。marketplace経由で更新・発見を管理したい場合。
- **metered skill**: skill形式を使い、明示した場合だけ起動したい場合。
- **interactive skill**: skill形式を使い、関連する依頼で暗黙起動も許可したい場合。

## 使い方

```text
$cultural-substrate-weaving この制度案の責任、情報流、不可逆性を検査してください。
```

単純な校正、定型実装、局所的バグ修正では使用しません。

## AGENTS.mdとの組み合わせ

`adapters/project-integrations/codex/AGENTS.fragment.md`の短い入口だけを対象リポジトリの`AGENTS.md`へ追加します。方法論全文は置かないでください。
