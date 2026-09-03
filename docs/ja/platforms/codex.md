# Codexで使う

現在の事実、外部の文脈、追加の出典探索が必要な課題では、CodexでネットワークアクセスやWeb検索を利用できることを確認してください。手元の資料やリポジトリだけで完結するKJ統合・構造探索では必須ではありません。検索を使えない場合は、不足している外部事実を推測で補わないようにします。

## 推奨：プラグインとして導入

現在のOpenAI製品では、プラグインがChatGPTとCodexのワークフロー機能を発見・配布する主要な単位です。このリポジトリにはCodex向けのプラグインマーケットプレイスが含まれているため、ZIPを手作業で展開せずに導入できます。

ローカルのCodex CLIから導入する場合は、次を実行します。

```bash
codex plugin marketplace add hat47x/cultural-substrate-weaving
codex plugin add cultural-substrate-weaving-ja@cultural-substrate-weaving
```

英語版は`cultural-substrate-weaving-en`です。登録済みのマーケットプレイスやプラグインは、必要に応じて次のコマンドで確認できます。

```bash
codex plugin marketplace list
codex plugin list
```

プラグインのディレクトリはClaude Code向けパッケージと共有しており、`.codex-plugin/plugin.json`と`.claude-plugin/plugin.json`の両方を持ちます。

## ワークスペースで共有する場合

ワークスペース管理者は、GitHub上のマーケットプレイスをWorkspace settingsからインポートし、メンバーが利用できるプラグインとして管理できます。

1. Workspace settingsの「Plugins」から「Add」→「Import marketplace」を開きます。
2. Sourceに`https://github.com/hat47x/cultural-substrate-weaving`を指定します。
3. このリポジトリではマーケットプレイスがルートの`.agents/plugins/marketplace.json`にあるため、Pathは空欄のままにします。
4. インポート後、各プラグインのインストール方針や、必要なアプリがある場合はその利用条件を確認します。

GitHubからインポートしたマーケットプレイスは継続的に同期できます。ワークスペース全体で同じ導入元を管理したい場合は、この経路が適しています。

## スキル形式（直接配置）

単独のSkill形式も、ファイルを直接配置したい場合、既存環境との互換性を保ちたい場合、複数製品へ持ち運びたい場合に利用できます。主な導入経路はプラグインとしつつ、Skill ZIPを一律に無効・非推奨とは扱いません。

ローカルマシンで動くCodex CLIやIDE拡張で、Skillを直接配置する場合は次のようにします。

1. GitHub Releasesから`openai-skill-metered`または`openai-skill-interactive`のZIPを取得します。
2. 展開した`cultural-substrate-weaving`フォルダーを、個人利用なら`~/.agents/skills/`、プロジェクトで共有するならリポジトリの`.agents/skills/`へ置きます。
3. Codexを再起動するか、新しいセッションを開始して読み込み直します。

## Codexクラウドで使う場合

クラウド上のCodexタスクから、ローカルマシンの`~/.agents/skills/`がそのまま見えるとは前提にしません。Skillをリポジトリと一緒に管理する場合は`.agents/skills/`を使います。プラグインを使う場合は、そのCodex環境で利用できるプラグイン設定、Sources / Pluginsの画面、ワークスペースのポリシーに従ってください。

## どちらを選ぶか

- **Plugin**: 現在の主な導入経路。マーケットプレイスからの発見や更新を管理したい場合。
- **metered Skill**: Skill形式を直接配置し、明示した場合だけ起動したい場合。
- **interactive Skill**: Skill形式を直接配置し、関連する依頼で暗黙起動も許可したい場合。

## 使い方

```text
$cultural-substrate-weaving この制度案の責任、情報流、不可逆性を検査してください。
```

単純な校正、定型的な実装、局所的なバグ修正には使用しません。

## AGENTS.mdと組み合わせる

`adapters/project-integrations/ja-JP/codex/AGENTS.fragment.md`にある短い入口だけを、対象リポジトリの`AGENTS.md`へ追加します。常時読み込まれるファイルへ方法論全文を置かないでください。
