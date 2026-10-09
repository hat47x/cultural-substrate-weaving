# CodexでCSWを使う

現在の事実、外部の文脈、追加の出典を調べる必要がある場合は、CodexからネットワークやWeb検索を利用できるか確認してください。手元の資料やリポジトリだけで完結する、構造の読み取りや発見には必須ではありません。検索できない場合は、資料にない外部の事実を推測で補わないようにします。

## 推奨：プラグインとして導入

現在のOpenAI製品では、ChatGPTやCodexで使う機能を見つけて配布する主な単位がプラグインです。このリポジトリにはCodex向けのプラグイン配布情報があるため、ZIPファイルを手作業で展開しなくても導入できます。

手元のCodex CLIから導入するには、次のコマンドを実行します。

```bash
codex plugin marketplace add hat47x/cultural-substrate-weaving
codex plugin add cultural-substrate-weaving-ja@cultural-substrate-weaving
```

英語版は`cultural-substrate-weaving-en`です。登録済みの配布元やプラグインは、次のコマンドで確認できます。

```bash
codex plugin marketplace list
codex plugin list
```

プラグインのディレクトリはClaude Code向けパッケージと共有しており、`.codex-plugin/plugin.json`と`.claude-plugin/plugin.json`の両方を持ちます。

## ワークスペースで共有する場合

作業領域の管理者は、GitHub上のプラグイン配布情報をWorkspace settingsから取り込み、メンバーが利用できるように管理できます。

1. Workspace settingsの「Plugins」から「Add」→「Import marketplace」を開きます。
2. Sourceに`https://github.com/hat47x/cultural-substrate-weaving`を指定します。
3. このリポジトリではマーケットプレイスがルートの`.agents/plugins/marketplace.json`にあるため、Pathは空欄のままにします。
4. インポート後、各プラグインのインストール方針や、必要なアプリがある場合はその利用条件を確認します。

GitHubから取り込んだプラグイン配布情報は、その後も同期できます。ワークスペース全体で同じ導入元を管理したい場合は、この経路が適しています。

## スキル形式（直接配置）

スキル形式も、ファイルを直接配置したい場合、既存環境との互換性を維持したい場合、複数の製品で共通して使いたい場合に利用できます。主な導入方法はプラグインですが、ZIP形式のスキルをすべて無効または非推奨とするわけではありません。

ローカルマシンで動くCodex CLIやIDE拡張で、Skillを直接配置する場合は次のようにします。

1. GitHub Releasesから`openai-skill-metered`または`openai-skill-interactive`のZIPを取得します。
2. 展開した`cultural-substrate-weaving`フォルダーを、個人利用なら`~/.agents/skills/`、プロジェクトで共有するならリポジトリの`.agents/skills/`へ置きます。
3. Codexを再起動するか、新しいセッションを開始して読み込み直します。

## Codexクラウドで使う場合

クラウド上で実行するCodexのタスクから、手元の端末にある`~/.agents/skills/`をそのまま参照できるとは限りません。Skillをリポジトリと一緒に管理する場合は`.agents/skills/`を使います。プラグインを使う場合は、そのCodex環境で利用できるプラグイン設定、Sources / Pluginsの画面、ワークスペースのポリシーに従ってください。

## どちらを選ぶか

- **Plugin**: 現在の主な導入経路。マーケットプレイスからの発見や更新を管理したい場合。
- **metered Skill**: Skill形式を直接配置し、明示した場合だけ起動したい場合。
- **interactive Skill**: Skill形式を直接配置し、関連する依頼で暗黙起動も許可したい場合。

## 使い方

```text
$cultural-substrate-weaving この制度案の責任、情報流、不可逆性を検査してください。
```

利用範囲は、依頼内容やプロジェクトで委ねられた権限に従います。課題の種類だけを理由に、CSWを自動的に利用することはしません。

## AGENTS.mdと組み合わせる

`adapters/project-integrations/ja-JP/codex/AGENTS.fragment.md`にある短い入口だけを、対象リポジトリの`AGENTS.md`へ追加します。常に読み込まれるファイルには、方法論の全文を置かないでください。
