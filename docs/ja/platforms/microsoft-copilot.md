# Microsoft 365 Copilot Agentを作る

このリポジトリは、Microsoft 365 Agents Toolkit向けに日本語版・英語版の宣言型エージェントプロジェクトを生成します。

## 必要なもの

- Microsoft 365 Copilotを利用できるテナント
- Visual Studio CodeとMicrosoft 365 Agents Toolkit、またはAgents Toolkit CLI
- CLIを使う場合: `npm install -g @microsoft/m365agentstoolkit-cli`

## 1. ビルド

```bash
python scripts/build.py
```

日本語版は`dist/ja-JP/microsoft-copilot/`へ生成されます。

## 2. 開発環境を初期化

```bash
python scripts/init_m365_env.py --locale ja-JP --env dev
```

開発者名、Webサイト、プライバシーポリシー等を入力します。

## 3. SharePoint Knowledgeを使う

`dist/ja-JP/microsoft-copilot/knowledge/`のファイルを、一つのSharePointサイトまたはドキュメントライブラリへアップロードします。

```bash
python scripts/init_m365_env.py --locale ja-JP --env dev \
  --sharepoint-url "https://contoso.sharepoint.com/sites/csw"
python scripts/build.py
```

## 4. パッケージと検証

```bash
cd dist/ja-JP/microsoft-copilot/agent-project
atk package --env dev
atk validate --env dev
```

## 5. 試験と公開

個人試験では`atk provision --env dev`を使用します。stagingで限定共有してから、本番環境で`atk publish --env prod`を実行してください。本番公開にはテナント管理者の承認が必要となる場合があります。
