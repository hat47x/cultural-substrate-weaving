# Microsoft 365 Copilot Agentを作る

このリポジトリは、Microsoft 365 Agents Toolkit向けに日本語版・英語版の宣言型エージェントプロジェクトを生成します。

## 必要なもの

- Microsoft 365 Copilotを利用できるテナント
- Visual Studio CodeとMicrosoft 365 Agents Toolkit、またはAgents Toolkit CLI
- CLIを使う場合: `npm install -g @microsoft/m365agentstoolkit-cli`
- テナント側でWeb検索によるグラウンディングが許可されていること。本方法論は検索による事実確認を前提とします

## 1. パッケージを取得

[GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases)から`cultural-substrate-weaving-m365-copilot-ja-JP-vX.Y.Z.zip`を取得し、展開します。`agent-project/`にAgents Toolkitプロジェクト一式が含まれます。リポジトリをビルドする必要はありません。

## 2. 環境設定を入力

`agent-project/env/.env.dev.example`を`agent-project/env/.env.dev`としてコピーし、開発者名・WebサイトURL・プライバシーポリシー・利用規約のURL・`M365_APP_ID`（任意のGUID）を入力します。これらは`atk package`実行時にマニフェストへ反映されます。

## 3. SharePoint Knowledgeを使う（任意）

デフォルトのエージェントは`knowledge/`のファイルを直接参照しません。SharePoint上のドキュメントを根拠情報として追加したい場合は、リポジトリをクローンしてビルドし直す必要があります。

1. `knowledge/`のファイルを、一つのSharePointサイトまたはドキュメントライブラリへアップロードします。
2. リポジトリをクローンします。
3. 次を実行します。

```bash
python scripts/init_m365_env.py --locale ja-JP --env dev \
  --sharepoint-url "https://contoso.sharepoint.com/sites/csw"
python scripts/build.py
```

4. 手順1で展開したものの代わりに、`dist/ja-JP/microsoft-copilot/agent-project/`を使用します。

## 4. パッケージと検証

```bash
cd agent-project
atk package --env dev
atk validate --env dev
```

## 5. 試験と公開

個人試験では`atk provision --env dev`を使用します。stagingで限定共有してから、本番環境で`atk publish --env prod`を実行してください。本番公開にはテナント管理者の承認が必要となる場合があります。
