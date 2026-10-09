# Microsoft 365 Copilotでエージェントを作成する

このリポジトリでは、Microsoft 365 Copilot向けに、日本語と英語の宣言型エージェントの素材を生成します。導入方法は、画面だけで設定するAgent Builderと、コマンドで操作するAgents Toolkit CLIの二つです。組織内への特別な展開要件がなければ、Agent Builderから始める方が簡単です。

手元にある資料だけで完結する材料の統合や構造の探索では、Web検索は必須ではありません。現在の事実、外部の文脈、追加の出典を調べる必要がある場合は、利用する組織の環境でWeb検索を根拠の確認に使えるか確かめてください。

## Microsoft 365版で対応する範囲

Microsoft 365 Copilotでは、Knowledgeは主に事実を裏付ける情報として使います。エージェントが実行する指示をInstructionsからKnowledgeへ移しても、続けて実行されるとは想定できません。

そのため、Microsoft 365向けには、8,000文字以内で必要な指示が完結する**限定的な接続方式**を用意しています。エージェントへの実行指示となるのは、`instructions.txt`に書かれている範囲だけです。

このアダプターは、文化体系の視点による構造読解、発見、帰属保持、対象への返却、具体化を扱います。親和図法の材料統合と複数回の継続管理は別スキルへ委ね、内部手順を埋め込みません。別のスキルを呼び出せない環境では、対応できない範囲を明示します。CSWの構造読解と発見だけで足りる依頼は、その範囲で進められます。

`method-reference/`には、CSWの実行内容と関連資料を、人が確認できる参照資料として含めます。Agent BuilderやSharePointのKnowledgeへアップロードして、`instructions.txt`の続きをエージェントに実行させるためのファイルではありません。

対象となる業務資料、調査資料、組織内文書などをKnowledgeへ追加し、対象側の事実グラウンディングに使うことはできます。

この限定的な接続方式は、ほかの対応環境と同じようにCSWや分離した手法のすべてを実行できることまでは保証しません。詳細な体系固有操作、Taihekiの特例、高度な長期研究設計、完全な親和統合の図解・lineage、完全なround履歴管理などが必要な場合は、より適した実行形態を使ってください。設計経緯と境界の整理はIssue #96に残しています。

## 配布ファイルを取得する

[GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases)から`cultural-substrate-weaving-m365-copilot-ja-JP-vX.Y.Z.zip`を取得し、展開します。中には次が含まれています。

- `instructions.txt`: Microsoft 365 Copilotへ設定する自己完結した限定アダプター
- `method-reference/`: CSW runtimeと関連方法を人間が確認するための参照資料
- `README.txt`: パッケージ内の役割分担と制約
- `agent-project/`: Agents Toolkit CLI向けのプロジェクト

GitHub Releasesで配布する標準ファイルには、**組織固有の情報を含めません**。特定テナントのSharePoint URLや、実際の`.env` / `.env.*`ファイルは入れません。`agent-project/env/`に含めるのは、安全な`.example`テンプレートだけです。テナント固有の設定は、組織へ展開するときに明示的に与えます。

## 方法A：Agent Builderを画面から設定する

Microsoft 365 Copilotライセンスがあれば、CLIやコード編集を使わずに作成できます。この方法では、`agent-project/`、Node.js、Visual Studio Codeは不要です。

このリポジトリでは、用意した`instructions.txt`の内容をそのまま設定できるよう、自然言語による自動生成ではなく、手動で設定します。

1. microsoft365.com/chat、office.com/chat、またはTeamsでMicrosoft 365 Copilotを開き、「新しいエージェント」を選びます。
2. 「設定にスキップ」を選び、Configureタブを開きます。
3. 「Name」と「Description」に名前と説明を入力します。Nameは30文字、Descriptionは1,000文字までです。
4. 「Instructions」に、展開した`instructions.txt`の内容をそのまま貼り付けます。8,000文字の制限内に収まることは、ビルドと検証処理で確認します。
5. 対象となる業務資料や調査資料を使う場合は、「Knowledge」へ追加します。端末から直接アップロードする埋め込みファイルは、知識ソースとして最大20件まで追加できます。パッケージ内の`method-reference/`は、Instructionsの続きを実行させる目的ではアップロードしません。
6. 現在の事実や外部情報を調べる用途がある場合は、「Knowledge」で「すべてのWebサイトを検索します。」を有効にします。手元の資料だけを対象にする場合は必須ではありません。
7. 「Try it」タブで、問題群を読み直す依頼や、発見を構成案にする依頼を試します。必要な作業が限定アダプターの範囲内に収まっているかも確認してください。
8. 作成後は、「Share」ボタンから特定の人やグループへ直接共有できます。組織全体で使えるようにする場合は、右上の「…」メニューから「Submit to your org catalog」を選び、管理者の承認を経て組織のAgent Storeへ公開します。

## 方法B：Agents Toolkit CLIで組織向けに設定する

AppSourceへの配布、テナント全体での管理配布、SharePointサイトを使った対象資料のグラウンディングなど、Agent Builderだけでは対応できない構成が必要な場合に使います。

### 必要なもの

- Visual Studio CodeとMicrosoft 365 Agents Toolkit、またはAgents Toolkit CLI
- CLIを使う場合: `npm install -g @microsoft/m365agentstoolkit-cli`

### 1. SharePoint Knowledgeへ対象資料を用意する

SharePointを参照情報（Knowledge）の置き場として使う場合は、CSWや親和図法の実行規則ではなく、対象を調べるための業務資料、調査資料、組織内文書を置きます。パッケージ内の`method-reference/`をSharePointへ置き、`instructions`の続きを実行させる構成にはしません。

1. エージェントが参照する対象資料を、一つのSharePointサイトまたはドキュメントライブラリへ用意します。
2. リポジトリをクローンします。
3. 展開時だけ使うAgents Toolkitの環境ファイルを作ります。

```bash
python scripts/init_m365_env.py --locale ja-JP --env dev \
  --sharepoint-url "https://contoso.sharepoint.com/sites/csw"
```

ここで作る`.env.dev`は、ローカルでの展開にだけ使う設定です。公開ビルドが自動的に読み込むことはなく、GitHub Releaseにも含めません。

4. SharePoint URLを**明示的に**与えてエージェントをビルドします。Bashなどでは次のように実行します。

```bash
CSW_M365_SHAREPOINT_SITE_URL="https://contoso.sharepoint.com/sites/csw" \
  python scripts/build.py
```

PowerShellでは次のように実行できます。

```powershell
$env:CSW_M365_SHAREPOINT_SITE_URL = "https://contoso.sharepoint.com/sites/csw"
python scripts/build.py
Remove-Item Env:CSW_M365_SHAREPOINT_SITE_URL
```

言語ごとに別のサイトを使う場合は、`CSW_M365_SHAREPOINT_SITE_URL_ja_JP` / `CSW_M365_SHAREPOINT_SITE_URL_en_US`を使用できます。

5. Agents Toolkitを実行する直前に、展開用の環境ファイルを生成済みのプロジェクトへ明示的に配置します。

```bash
python scripts/stage_m365_env.py --locale ja-JP --env dev
```

6. `dist/ja-JP/microsoft-copilot/agent-project/`を使用します。

### 2. 環境設定を確認する

`init_m365_env.py`が作る`adapters/microsoft-copilot/ja-JP/env/.env.dev`には、開発者名、WebサイトURL、プライバシーポリシー、利用規約のURL、`M365_APP_ID`、SharePoint URLが入ります。必要に応じて、生成済みプロジェクトへ配置する前に編集してください。

このファイルは展開時だけ使います。Gitへコミットせず、GitHub Release用の`make package`にも持ち込まないでください。公開パッケージの生成処理は、実際の`.env`、`.example`以外の`.env.*`、`*.local`、`*.secret`、シンボリックリンクを検出すると処理を停止します。

### 3. パッケージを作成して検証する

```bash
cd dist/ja-JP/microsoft-copilot/agent-project
atk package --env dev
atk validate --env dev
```

組織固有の設定を含むAgents Toolkitの配布ファイルは、この手順で作成します。公開GitHub Release用の`make package`とは目的が異なります。

### 4. 試験して公開する

個人で試す場合は`atk provision --env dev`を使用します。限定された環境で検証してから、本番環境で`atk publish --env prod`を実行してください。本番公開には、テナント管理者の承認が必要になる場合があります。

`staging`または`prod`を使う場合は、それぞれ対応する`.env.staging` / `.env.prod`を生成し、同じ手順で生成済みプロジェクトへ配置してください。
