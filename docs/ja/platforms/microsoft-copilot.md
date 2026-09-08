# Microsoft 365 Copilot Agentを作る

このリポジトリでは、Microsoft 365 Copilot向けの宣言型エージェント素材を、日本語版と英語版で生成します。導入方法は、画面操作だけで完結するAgent Builderと、Agents Toolkit CLIを使う方法の二つです。特別な組織展開要件がなければ、Agent Builderから始めるのが簡単です。

手元の資料だけで完結する材料統合や構造探索では、Web検索は必須ではありません。現在の事実、外部の文脈、追加の出典探索が必要な課題では、利用するテナントでWeb検索によるグラウンディングが許可されているか確認してください。

## 現在のMicrosoft 365版の位置づけ

Microsoft 365 Copilotでは、Knowledgeは主として事実のグラウンディングに使うものであり、エージェントの実行指示をInstructionsからKnowledgeへ退避する用途は前提にできません。

そのため、Microsoft 365向けには、8,000文字以内で自己完結する**限定composite adapter**を用意しています。エージェントの実行指示として扱うのは`instructions.txt`に書かれた範囲だけです。

このadapterの中心は、CSWが担当する文化体系探索、帰属保持、対象へのreturnです。ただし、Microsoft 365では独立した兄弟Skillを常に呼べるとは限らないため、材料が複数・異種である場合にも安全に作業できるよう、**親和統合コアの最小互換手順を`instructions.txt`へ埋め込んでいます。** これはCSW本体が材料統合アルゴリズムを所有するという意味ではありません。また、`affinity-synthesis`の完全なrepresentation／lineage機能や、`iterative-inquiry-synthesis`の完全な複数round管理を再現したものでもありません。

埋め込みの材料統合は、KJ法・親和図法・質的統合法の系譜を参照し、意味単位、証拠状態、先に分類名を置かない束ね、元材料への戻し検査などの中核を限定的に保持します。KJ法は株式会社川喜田研究所の登録商標であり、このadapterはKJ法の公式実装を称しません。

`method-reference/`には、CSW runtimeや関連する方法資料を、人間が確認するための参照として同梱します。Agent BuilderやSharePointのKnowledgeへアップロードして、`instructions.txt`の続きをエージェントに実行させるためのファイルではありません。

対象となる業務資料、調査資料、組織内文書などをKnowledgeへ追加し、対象側の事実グラウンディングに使うことはできます。

この限定adapterは、他の対応プラットフォームと同等の完全なCSW／分離Method実行を保証しません。詳細な体系固有操作、Taihekiの特例、高度な長期研究設計、完全な親和統合の図解・lineage、完全なround履歴管理などが必要な場合は、より適した実行形態を使ってください。設計経緯と境界の整理はIssue #96に残しています。

## パッケージを取得する

[GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases)から`cultural-substrate-weaving-m365-copilot-ja-JP-vX.Y.Z.zip`を取得し、展開します。中には次が含まれています。

- `instructions.txt`: Microsoft 365 Copilotへ設定する自己完結した限定composite adapter
- `method-reference/`: CSW runtimeと関連方法を人間が確認するための参照資料
- `README.txt`: パッケージ内の役割分担と制約
- `agent-project/`: Agents Toolkit CLI向けのプロジェクト

GitHub Releaseで配布する標準パッケージには、**テナント固有の情報を含めません**。特定テナントのSharePoint URLや、実際の`.env` / `.env.*`ファイルは入れません。`agent-project/env/`に含めるのは、安全な`.example`テンプレートだけです。テナント固有の設定は、組織へ展開するときに明示的に与えます。

## 方法A：Agent Builder（画面操作だけで作成）

Microsoft 365 Copilotライセンスがあれば、CLIやコード編集を使わずに作成できます。この方法では、`agent-project/`、Node.js、Visual Studio Codeは不要です。

このリポジトリでは、用意済みの`instructions.txt`をそのまま反映しやすいよう、自然言語による自動生成ではなく手動設定を使います。

1. microsoft365.com/chat、office.com/chat、またはTeamsでMicrosoft 365 Copilotを開き、「新しいエージェント」を選びます。
2. 「設定にスキップ」を選び、Configureタブを開きます。
3. 「Name」と「Description」に名前と説明を入力します。Nameは30文字、Descriptionは1,000文字までです。
4. 「Instructions」に、展開した`instructions.txt`の内容をそのまま貼り付けます。8,000文字の制限内に収まることは、ビルドと検証処理で確認します。
5. 対象となる業務資料や調査資料を使う場合は、「Knowledge」へ追加します。端末から直接アップロードする埋め込みファイルは、知識ソースとして最大20件まで追加できます。パッケージ内の`method-reference/`は、Instructionsの続きを実行させる目的ではアップロードしません。
6. 現在の事実や外部情報を調べる用途がある場合は、「Knowledge」で「すべてのWebサイトを検索します。」を有効にします。手元の資料だけを対象にする場合は必須ではありません。
7. 「Try it」タブで、文化体系を使う例、使わない例、埋め込みの材料統合だけで足りる例を試します。必要な作業が限定adapterの範囲内に収まっているかも確認してください。
8. 作成後は、「Share」ボタンから特定の人やグループへ直接共有できます。組織全体で使えるようにする場合は、右上の「…」メニューから「Submit to your org catalog」を選び、管理者の承認を経て組織のAgent Storeへ公開します。

## 方法B：Agents Toolkit CLI（組織展開などの高度な構成向け）

AppSourceへの配布、テナント全体での管理配布、SharePointサイトを使った対象資料のグラウンディングなど、Agent Builderだけでは対応できない構成が必要な場合に使います。

### 必要なもの

- Visual Studio CodeとMicrosoft 365 Agents Toolkit、またはAgents Toolkit CLI
- CLIを使う場合: `npm install -g @microsoft/m365agentstoolkit-cli`

### 1. SharePoint Knowledgeへ対象資料を用意する

SharePointをKnowledgeとして使う場合は、CSWや親和統合の実行規則ではなく、エージェントが対象について参照する業務資料・調査資料・組織内文書を置きます。パッケージ内の`method-reference/`をSharePointへ置き、`instructions`の続きを実行させる構成にはしません。

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

テナント固有のAgents Toolkitパッケージは、この展開経路で作成します。公開GitHub Release用の`make package`とは目的が異なります。

### 4. 試験して公開する

個人で試す場合は`atk provision --env dev`を使用します。限定された環境で検証してから、本番環境で`atk publish --env prod`を実行してください。本番公開には、テナント管理者の承認が必要になる場合があります。

`staging`または`prod`を使う場合は、それぞれ対応する`.env.staging` / `.env.prod`を生成し、同じ手順で生成済みプロジェクトへ配置してください。
