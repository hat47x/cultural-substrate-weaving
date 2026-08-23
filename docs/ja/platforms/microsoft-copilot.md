# Microsoft 365 Copilot Agentを作る

このリポジトリは、Microsoft 365 Copilot向けの宣言型エージェント素材を日本語版・英語版で生成します。導入方法は、GUIのみで完結する「Agent Builder」経路と、Agents Toolkit CLIを使う経路の二つがあります。迷ったら前者を使ってください。

本方法論は事実確認や文脈収集をWeb検索に依存する場面があります。テナントでWeb検索によるグラウンディングが許可されていることを確認してください。

## パッケージを取得

[GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases)から`cultural-substrate-weaving-m365-copilot-ja-JP-vX.Y.Z.zip`を取得し、展開します。中には`instructions.txt`、`knowledge/`（参照モジュールのMarkdownファイル）、そしてAgents Toolkit CLI向けの`agent-project/`が含まれます。

## 方法A：Agent Builder（GUIのみ、推奨）

Microsoft 365 Copilotライセンスがあれば、CLIやコード編集なしでそのまま作成できます。`agent-project/`・Node.js・Visual Studio Codeは不要です。

1. microsoft365.com/chat、office.com/chat、またはTeamsでMicrosoft 365 Copilotを開き、「新しいエージェント」を選びます。
2. 「設定にスキップ」を選び、Configureタブを開きます（自然言語での自動生成を使わず、手動で設定します）。
3. 「Name」「Description」に名前と説明を入力します（Nameは30文字、Descriptionは1,000文字まで）。
4. 「Instructions」に、展開した`instructions.txt`の内容をそのまま貼り付けます（8,000文字制限内に収まるよう、ビルド時点で検証済みです）。
5. 「Knowledge」に、`knowledge/`配下の各ファイルをアップロードします。Agent BuilderはMarkdown（`.md`）を受け付けないため、アップロード前に拡張子を`.txt`へリネームしてください（中身はプレーンテキストなのでリネームだけで問題ありません）。ドラッグ＆ドロップ、または矢印アイコンから追加します。SharePointサイトは不要です（最大20件までの知識ソースを追加できます）。
6. 同じく「Knowledge」で「すべてのWebサイトを検索します。」にチェックを入れます。本方法論は事実確認や文脈収集をWeb検索に依存する場面があるため、無効のままでは判断精度が落ちます。
7. 「Try it」タブで、発動する例・発動しない例の両方を試します。
8. 作成後、「Share」ボタンから特定の人・グループへ直接共有できます。組織全体で使えるようにする場合は、右上の「…」メニューから「Submit to your org catalog」を選び、管理者の承認を経て組織のAgent Storeへ公開します。

## 方法B：Agents Toolkit CLI（上級者・組織展開向け）

AppSourceへの配布、テナント全体での管理配布、SharePointサイトへのグラウンディングなど、Agent Builderでは対応できない構成が必要な場合に使います。

### 必要なもの

- Visual Studio CodeとMicrosoft 365 Agents Toolkit、またはAgents Toolkit CLI
- CLIを使う場合: `npm install -g @microsoft/m365agentstoolkit-cli`

### 1. SharePoint Knowledgeを設定する（実質必須）

宣言型エージェントの`instructions`には、発動判断・最小実行手順・常時維持する判断軸までしか含まれません。詳細な文化体系適用、KJ統合、人間／Taiheki特例、統治・評価の参照は`knowledge/`に収録されるため、この経路で作ったエージェントはSharePoint連携なしではそれらを参照できません。連携なしでは方法論の大部分が機能しないため、パッケージ内の`agent-project/`をそのまま使わず、次の手順でビルドし直してください。

1. `knowledge/`のファイルを、一つのSharePointサイトまたはドキュメントライブラリへアップロードします。
2. リポジトリをクローンします。
3. 次を実行します。

```bash
python scripts/init_m365_env.py --locale ja-JP --env dev \
  --sharepoint-url "https://contoso.sharepoint.com/sites/csw"
python scripts/build.py
```

4. パッケージ内の`agent-project/`の代わりに、`dist/ja-JP/microsoft-copilot/agent-project/`を使用します。

### 2. 環境設定を入力

`agent-project/env/.env.dev.example`を`agent-project/env/.env.dev`としてコピーし、開発者名・WebサイトURL・プライバシーポリシー・利用規約のURL・`M365_APP_ID`（任意のGUID）を入力します。これらは`atk package`実行時にマニフェストへ反映されます。

### 3. パッケージと検証

```bash
cd agent-project
atk package --env dev
atk validate --env dev
```

### 4. 試験と公開

個人試験では`atk provision --env dev`を使用します。stagingで限定共有してから、本番環境で`atk publish --env prod`を実行してください。本番公開にはテナント管理者の承認が必要となる場合があります。
