# ChatGPTでカスタムGPTを作る

GPTの作成・編集はChatGPTのWeb版で行います。

## 準備

[GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases)から`cultural-substrate-weaving-chatgpt-gpt-ja-JP-vX.Y.Z.zip`を取得し、展開します。`instructions.md`、`knowledge/`、`conversation-starters.md`、`deploy-checklist.md`が含まれます。リポジトリをビルドする必要はありません。

リポジトリを保守・翻訳している場合は、`python scripts/build.py`で同じ内容を`dist/ja-JP/chatgpt-gpt/`へ生成できます。詳細は[開発手順](../maintainers/development.md)を参照してください。

## 作成手順

1. ChatGPTの「GPTs」から「作成」を開きます。
2. 「構成」画面で名前と説明を入力します。
3. 現在の事実、外部文脈、追加の出典探索を扱う用途では、「機能」の「ウェブ検索」を有効にします。手元の資料だけを対象にするKJ統合や構造探索では必須ではありません。検索を使えない場合は、不足する外部事実を推測で補わないようにします。
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

## 代替方法：Skillsへのアップロード（対象ワークスペース向け）

カスタムGPTとは別に、ChatGPT本体のSkills機能からのアップロードでも利用できます。Skillsは現在、対象となるChatGPT Business・Enterprise・Healthcare・Eduユーザーに提供され、利用可否はワークスペース設定・ロール・製品面にも依存します。

1. GitHub Releasesから`openai-skill-metered`または`openai-skill-interactive`のZIPを取得します（[Codexで使う](codex.md)と共通のパッケージです。ChatGPTでは、どちらもアップロード可能なSkillとして扱えます）。
2. ChatGPTのサイドバーから「プラグイン」を開き、Plugin Directoryの「Skills」タブで「作成」→「パソコンからアップロード」を選び、そのZIPをそのままアップロードします。
3. アップロード後、ChatGPT側で自動スキャンが行われます。「Needs Review」や「Blocked」と表示された場合は、内容を確認したうえで対応してください。

Skillsの利用可否や同期範囲は製品・ワークスペースによって異なるため、ChatGPTとCodexで同じSkillが自動的に共有されるとは前提にしないでください。
