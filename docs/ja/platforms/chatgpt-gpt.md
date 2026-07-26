# ChatGPTでカスタムGPTを作る

GPTの作成・編集はChatGPTのWeb版で行います。

## 準備

[GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases)から`cultural-substrate-weaving-chatgpt-gpt-ja-JP-vX.Y.Z.zip`を取得し、展開します。`instructions.md`、`knowledge/`、`conversation-starters.md`、`deploy-checklist.md`が含まれます。リポジトリをビルドする必要はありません。

リポジトリを保守・翻訳している場合は、`python scripts/build.py`で同じ内容を`dist/ja-JP/chatgpt-gpt/`へ生成できます。詳細は[開発手順](../maintainers/development.md)を参照してください。

## 作成手順

1. ChatGPTの「GPTs」から「作成」を開きます。
2. 「構成」画面で名前と説明を入力します。
3. 「機能」で「ウェブ検索」を有効にします。本方法論は事実確認や文脈収集を検索に依存する場面があるため、無効のままでは判断精度が落ちます。
4. 展開した`instructions.md`をInstructionsへ貼り付けます。
5. `knowledge/`内の全ファイルをKnowledgeへアップロードします。
6. `conversation-starters.md`の例を会話スターターへ登録します。
7. Previewで発動・非発動の両方を試します。
8. 保存し、共有範囲を選びます。

## 更新手順

1. 新しいリリースのGPT更新パックを取得します。
2. Instructionsを置き換えます。
3. 古いKnowledgeファイルを削除し、新しいファイルをアップロードします。
4. `deploy-checklist.md`を確認します。
5. GPTのバージョン履歴を確認して保存します。

GPTsは通常のChatGPTメモリを正本として使わないため、詳細方法論はInstructionsとKnowledgeで管理します。

## 代替方法：Skillsへのアップロード（Business/Enterprise/Healthcare/Edu向け）

カスタムGPTとは別に、ChatGPT本体のSkills機能からのアップロードでも利用できます。ただし現状はChatGPT Business・Enterprise・Healthcare・Eduのワークスペースのみ利用可能で、個人のFree/Plus/Proアカウントでは使えません。ワークスペース管理者が「Enable skills」「Enable skill uploading」の権限を有効にしている必要もあります。

1. GitHub Releasesから`openai-skill-metered`または`openai-skill-interactive`のZIPを取得します（[Codexで使う](codex.md)と共通のパッケージです。ChatGPT向けにはどちらも同じ内容として扱われます）。
2. ChatGPTのサイドバーで「Plugins」を開き、「Skills」タブを選びます。
3. 「Create」＞「Upload」から、そのZIPをそのままアップロードします。
4. アップロード後、ChatGPT側で自動スキャンが行われます。「Needs Review」や「Blocked」と表示された場合は、内容を確認したうえで対応してください。

個人用Skillsはデスクトップ版とWeb/モバイル版で同期されないため、両方で使う場合はそれぞれの環境で個別にアップロードしてください。
