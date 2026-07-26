# ChatGPTでカスタムGPTを作る

GPTの作成・編集はChatGPTのWeb版で行います。

## 準備

```bash
python scripts/build.py
```

`dist/ja-JP/chatgpt-gpt/`に更新パックが生成されます。

## 作成手順

1. ChatGPTの「GPTs」から「作成」を開きます。
2. 「構成」画面で名前と説明を入力します。
3. `dist/ja-JP/chatgpt-gpt/instructions.md`をInstructionsへ貼り付けます。
4. `dist/ja-JP/chatgpt-gpt/knowledge/`内の全ファイルをKnowledgeへアップロードします。
5. `conversation-starters.md`の例を会話スターターへ登録します。
6. Previewで発動・非発動の両方を試します。
7. 保存し、共有範囲を選びます。

## 更新手順

1. 新しいリリースのGPT更新パックを取得します。
2. Instructionsを置き換えます。
3. 古いKnowledgeファイルを削除し、新しいファイルをアップロードします。
4. `deploy-checklist.md`を確認します。
5. GPTのバージョン履歴を確認して保存します。

GPTsは通常のChatGPTメモリを正本として使わないため、詳細方法論はInstructionsとKnowledgeで管理します。
