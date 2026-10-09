# Claude CodeでCSWを使う

このGitHubリポジトリは、Claude向けのプラグイン配布元として利用できます。

現在の事実、外部の文脈、追加の出典を調べる必要がある場合は、Claude CodeのWebSearchまたはWebFetchを使えるか確認してください。手元の資料やリポジトリだけで完結する構造の読み取りや発見には、Web検索は必須ではありません。検索できるかどうかは、利用可能な情報の範囲として扱います。検索できない部分について、どこまで推論・仮説・断定を認めるかは、依頼の証拠基準と委任の範囲に従います。

`/plugin`は、ターミナルで動かすCLIの対話画面で使うコマンドです。利用している環境に応じて、次の導入方法を選びます。

## ターミナルから操作する場合

対話中に、次のコマンドを実行します。

```text
/plugin marketplace add hat47x/cultural-substrate-weaving
/plugin install cultural-substrate-weaving-ja@cultural-substrate-weaving
/reload-plugins
```

スクリプトなどから対話なしで導入する場合は、次のコマンドを実行します。

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
claude plugin install cultural-substrate-weaving-ja@cultural-substrate-weaving
```

## Claude Desktop（Codeタブ、ローカル・SSHセッション）

Claude Desktopのプラグイン画面には、登録済みの配布元だけが表示されます。このリポジトリのような公式以外の配布元を使う場合は、まず次のどちらかの方法で登録します。

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

登録後は、Claude Desktopの「＋」→「Plugins」から利用できるプラグインを確認できます。画面の名称は変更されることがあります。項目が見つからない場合は、Claude Codeの`/plugin`画面も確認してください。

## クラウド上で使う場合

クラウド上のセッションから、手元のClaude Codeと同じプラグイン管理画面やファイルシステムが使えるとは限りません。リポジトリ側の設定を利用する場合は、その環境がプロジェクト設定やプラグインマーケットプレイスをどのように読み込むかを確認してください。

## 別の導入方法：スキルとして登録する

プラグイン配布元からの導入が難しい場合は、Claudeのスキル機能へファイルを登録する方法もあります。登録できる画面、利用プラン、管理設定は、製品側の対応状況によって異なります。

1. GitHub Releasesから`openai-skill-metered`または`openai-skill-interactive`のZIPを取得します。[Codexで使う](codex.md)と共通のパッケージです。
2. 利用中のClaude画面にSkillsのアップロード機能がある場合は、そのZIPをそのままアップロードします。
3. インストール後、その環境・ワークスペース・プロジェクト設定に従って呼び出し挙動を確認します。

プラグイン版には、明示的な呼び出しに限定するため`disable-model-invocation: true`を設定しています。直接アップロードするSkill版は、選んだ配布プロファイルと利用先の対応状況に従います。プロジェクトでの利用範囲や判断の委任は、依頼者の指示に従って定めてください。

## WSL

Claude CodeはWSLに対応しており、プラグイン配布元の設定もLinuxやWSL上で利用できます。WSLだからという理由だけでプラグインを無効とみなさず、通常のターミナルCLI手順を使用してください。

組織管理下では、Windows側の管理設定をWSLへ引き継ぐ設定が適用される場合があります。

## `/plugin isn't available in this environment`と表示された場合

対話ターミナル以外で`/plugin`系のコマンドを直接実行した場合などに表示されることがあります。その環境でプラグイン管理画面またはプロジェクト設定を利用できるか確認し、利用できない場合はターミナルCLIから設定してください。

## 呼び出し

明示的に呼び出す場合は、次のように指定できます。

```text
/cultural-substrate-weaving-ja:weave このアーキテクチャの責任境界を検査してください。
```

Plugin版はこのように明示的に呼び出します。呼び出した後の利用範囲と判断は、著者が与えた指示・委任に従います。

## 更新

```text
/plugin marketplace update cultural-substrate-weaving
/reload-plugins
```

新しい版が公開されたら、必要に応じてプラグインを更新してください。
