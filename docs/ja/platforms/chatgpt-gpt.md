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
