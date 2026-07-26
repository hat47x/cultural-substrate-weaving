# Claude Codeで使う

このGitHubリポジトリはClaude Plugin Marketplaceとして利用できます。

本方法論は事実確認や文脈収集をWeb検索に依存する場面があります。Claude CodeでWebSearch/WebFetchツールが利用可能な設定になっていることを確認してください。

`/plugin`はターミナルCLIの対話パネルで動作するコマンドです。実行環境によって導入手順が異なります。

## ターミナルCLI（標準の`claude`コマンド）

対話セッション内で実行します。

```text
/plugin marketplace add hat47x/cultural-substrate-weaving
/plugin install csw-method-ja@cultural-substrate-weaving
/reload-plugins
```

非対話（スクリプト）から追加する場合:

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
claude plugin install csw-method-ja@cultural-substrate-weaving
```

## Claude Desktop（Codeタブ、ローカル・SSHセッション）

Claude Desktop単体のプラグインブラウザーは、すでに登録済みのマーケットプレイスしか一覧に出ません。このリポジトリのような公式以外のマーケットプレイスを使うには、先にどちらかの方法で登録します。

- 一度だけ上記のターミナルCLIのコマンドを実行する（`~/.claude`の設定はCLIとDesktopで共有されるため、以後Desktopの「＋」→「Plugins」→「Manage plugins」に表示されます）。
- チーム共有にする場合は、リポジトリの`.claude/settings.json`へ次を追加する（メンバーがフォルダーを信頼した際にインストールを促されます）。

```json
{
  "extraKnownMarketplaces": {
    "cultural-substrate-weaving": {
      "source": { "source": "github", "repo": "hat47x/cultural-substrate-weaving" }
    }
  },
  "enabledPlugins": ["csw-method-ja@cultural-substrate-weaving"]
}
```

登録後は、Desktopの「＋」→「Plugins」→「Add plugin」からインストールできます。

## クラウドセッション（claude.aiのWeb版など）

クラウドセッションにプラグインブラウザーはありません。上記の`.claude/settings.json`の`extraKnownMarketplaces`と`enabledPlugins`をリポジトリに設定し、セッション開始時に自動導入させてください。

## より簡単な代替方法：スキルのアップロード

Plugin Marketplace経由の導入が難しい場合は、Claude本体の汎用Skills機能（Claude Desktop／claude.aiの「カスタマイズ」＞「スキル」）からのアップロードでも利用できます。マーケットプレイス登録やターミナル操作は不要です。

1. GitHub Releasesから`openai-skill-metered`または`openai-skill-interactive`のZIPを取得します（[Codexで使う](codex.md)と共通のパッケージです）。
2. Claude Desktopの「カスタマイズ」＞「スキル」＞「追加」＞「スキルをアップロード」から、そのZIPをそのままアップロードします。
3. claude.ai Web版でも、設定の「スキル」から同様にアップロードできます。

**注意**：この形式のSKILL.mdには明示呼び出し専用の設定（`disable-model-invocation`）が含まれていません。そのためPlugin版（`csw-method-ja`）と異なり、Claudeが関連すると判断した場面で自動的に呼び出されます（`openai-skill-interactive`と同様の挙動）。トークン消費を抑えたい場合は、上記のPlugin Marketplace経由の導入を優先してください。

## WSLセッション

WSLセッションではプラグインを利用できません。

## `/plugin isn't available in this environment`と表示された場合

対話ターミナル以外（Desktop、クラウド、非対話セッションなど）で`/plugin`系コマンドを直接実行した場合に出るメッセージです。上記の該当する環境の手順に読み替えてください。

## 呼び出し

```text
/csw-method-ja:cultural-substrate-weaving-ja このアーキテクチャの責任境界を検査してください。
```

明示呼び出しを標準にしているため、不要なトークン消費を抑えられます。

## 更新

```text
/plugin marketplace update cultural-substrate-weaving
```

バージョンが更新された後、必要に応じてプラグインを更新し、`/reload-plugins`を実行します。
