# Claude Codeで使う

このGitHubリポジトリは、ClaudeのPlugin Marketplaceとして利用できます。

現在の事実、外部の文脈、追加の出典探索が必要な課題では、Claude CodeのWebSearch / WebFetchツールを利用できることを確認してください。手元の資料やリポジトリだけで完結するKJ統合・構造探索では必須ではありません。検索の可否は利用できる情報面として扱い、検索できない範囲を推論・仮説・断定のどれとして扱うかは、依頼側の証拠基準や委任に従います。

`/plugin`は、ターミナルCLIの対話画面で使うコマンドです。利用している環境に応じて、次の導入方法を選びます。

## ターミナルCLI（標準の`claude`コマンド）

対話セッション内では、次を実行します。

```text
/plugin marketplace add hat47x/cultural-substrate-weaving
/plugin install cultural-substrate-weaving-ja@cultural-substrate-weaving
/reload-plugins
```

スクリプトなどから非対話で追加する場合は、次を実行します。

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
claude plugin install cultural-substrate-weaving-ja@cultural-substrate-weaving
```

## Claude Desktop（Codeタブ、ローカル・SSHセッション）

Claude Desktopのプラグイン画面には、すでに登録されているマーケットプレイスだけが表示されます。このリポジトリのような公式以外のマーケットプレイスを使う場合は、先に次のどちらかの方法で登録します。

- 一度だけ、上記のターミナルCLIコマンドを実行する。`~/.claude`の設定はCLIとDesktopで共有されるため、以後はDesktopの「＋」→「Plugins」→「Manage plugins」に表示されます。
- チームで共有する場合は、リポジトリの`.claude/settings.json`へ次の設定を追加する。メンバーがフォルダーを信頼した際に、インストールが案内されます。

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

登録後は、Desktopの「＋」→「Plugins」から利用可能なプラグインを確認できます。製品画面の名称は更新されることがあるため、見つからない場合はClaude Codeの`/plugin`画面も確認してください。

## クラウドセッション（claude.aiのWeb版など）

クラウドセッションでは、ローカルのClaude Codeと同じプラグイン管理画面やファイルシステムを使えるとは前提にしません。リポジトリ側の設定を利用する場合は、その環境がプロジェクト設定やプラグインマーケットプレイスをどのように読み込むかを確認してください。

## より簡単な代替方法：Skillsへアップロードする

Plugin Marketplaceからの導入が難しい場合は、Claude本体のSkills機能へアップロードして利用することもできます。利用できる画面、プラン、管理設定は、製品側の提供状況に従います。

1. GitHub Releasesから`openai-skill-metered`または`openai-skill-interactive`のZIPを取得します。[Codexで使う](codex.md)と共通のパッケージです。
2. 利用中のClaude画面にSkillsのアップロード機能がある場合は、そのZIPをそのままアップロードします。
3. インストール後、その環境・ワークスペース・プロジェクト設定に従って呼び出し挙動を確認します。

Plugin版とアップロードしたSkill版のどちらにも、このリポジトリ側から「明示呼び出し専用」を強制する設定は入れません。明示呼び出しだけに限定したい場合や、暗黙呼び出しを許可したい場合は、Claude側の設定、プロジェクト指示、著者の運用方針で決めます。

## WSL

Claude CodeはWSLをサポートしており、プラグインマーケットプレイスの設定もLinux / WSL環境で利用できます。WSLだからという理由だけでプラグインを無効とみなさず、通常のターミナルCLI手順を使用してください。

組織管理下では、Windows側の管理設定をWSLへ引き継ぐ設定が適用される場合があります。

## `/plugin isn't available in this environment`と表示された場合

対話ターミナル以外で`/plugin`系のコマンドを直接実行した場合などに表示されることがあります。その環境でプラグイン管理画面またはプロジェクト設定を利用できるか確認し、利用できない場合はターミナルCLIから設定してください。

## 呼び出し

明示的に呼び出す場合は、たとえば次のように指定できます。

```text
/cultural-substrate-weaving-ja:weave このアーキテクチャの責任境界を検査してください。
```

これは呼び出し方法の一例であり、スキル側の必須条件ではありません。実際の発動範囲は、Claudeの製品設定、ワークスペース／プロジェクト設定、著者が与えた指示・委任に従います。

## 更新

```text
/plugin marketplace update cultural-substrate-weaving
/reload-plugins
```

新しい版が公開された後、必要に応じてプラグインを更新してください。
