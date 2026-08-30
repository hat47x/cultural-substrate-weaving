# Claude Codeで使う

このGitHubリポジトリはClaude Plugin Marketplaceとして利用できます。

現在の事実、外部文脈、追加の出典探索が必要な課題では、Claude CodeのWebSearch/WebFetchツールが利用できることを確認してください。手元の資料やリポジトリだけで完結するKJ統合・構造探索では必須ではありません。検索を使えない場合は、不足する外部事実を推測で補わないようにします。

`/plugin`はターミナルCLIの対話パネルで動作するコマンドです。実行環境によって導入手順が異なります。

## ターミナルCLI（標準の`claude`コマンド）

対話セッション内で実行します。

```text
/plugin marketplace add hat47x/cultural-substrate-weaving
/plugin install cultural-substrate-weaving-ja@cultural-substrate-weaving
/reload-plugins
```

非対話（スクリプト）から追加する場合:

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
claude plugin install cultural-substrate-weaving-ja@cultural-substrate-weaving
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
  "enabledPlugins": {
    "cultural-substrate-weaving-ja@cultural-substrate-weaving": true
  }
}
```

登録後は、Desktopの「＋」→「Plugins」から利用可能なプラグインを確認できます。製品UIの名称は更新されることがあるため、見つからない場合はClaude Codeの`/plugin`画面を基準にしてください。

## クラウドセッション（claude.aiのWeb版など）

クラウドセッションでは、ローカルClaude Codeと同じプラグイン管理UIやファイルシステムを前提にしないでください。リポジトリ側で利用する場合は、対象環境がproject settingsとplugin marketplaceをどのように読み込むかを確認します。

## より簡単な代替方法：スキルのアップロード

Plugin Marketplace経由の導入が難しい場合は、Claude本体のSkills機能からのアップロードでも利用できます。利用できる画面・プラン・管理設定は製品側の提供状況に従います。

1. GitHub Releasesから`openai-skill-metered`または`openai-skill-interactive`のZIPを取得します（[Codexで使う](codex.md)と共通のパッケージです）。
2. 利用中のClaude画面にSkillsのアップロード機能がある場合、そのZIPをそのままアップロードします。
3. インストール後に発動・非発動の両方を確認します。

**注意**：この形式のSKILL.mdには明示呼び出し専用の設定（`disable-model-invocation`）が含まれていません。そのためPlugin版（`cultural-substrate-weaving-ja`）とは発動制御が異なる可能性があります。明示呼び出しを厳密に保ちたい場合はPlugin Marketplace経由を優先してください。

## WSL

Claude CodeはWSLをサポートしており、plugin marketplace設定もLinux/WSL向け設定の対象です。WSLだからという理由だけでプラグインを無効とみなさず、通常のターミナルCLI手順を使用してください。組織管理下では、Windows側のmanaged settingsをWSLへ継承する設定が適用される場合があります。

## `/plugin isn't available in this environment`と表示された場合

対話ターミナル以外で`/plugin`系コマンドを直接実行した場合などに表示されることがあります。その環境でplugin管理UIまたはproject settingsが利用できるかを確認し、利用できない場合はターミナルCLIから設定してください。

## 呼び出し

```text
/cultural-substrate-weaving-ja:weave このアーキテクチャの責任境界を検査してください。
```

明示呼び出しを標準にしているため、不要なトークン消費を抑えられます。

## 更新

```text
/plugin marketplace update cultural-substrate-weaving
/reload-plugins
```

バージョンが更新された後、必要に応じてプラグインを更新します。
