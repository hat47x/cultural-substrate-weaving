# トラブルシューティング

## `plugins/`に意図しない差分が出る

生成物を直接直さず、`src/ja-JP/`または`adapters/claude-code/`を修正して`python scripts/build.py`を再実行します。

## Codexでスキルが表示されない

配置先、フォルダー名、`SKILL.md`のフロントマターを確認し、Codexを再起動します。

## ClaudeでMarketplaceが見つからない

GitHubのOWNER/REPOを確認し、`.claude-plugin/marketplace.json`がデフォルトブランチにあることを確認します。

## GPTがKnowledgeを使わない

規則はInstructions、参照資料はKnowledgeへ置きます。ファイル名とInstructions内の参照関係を確認します。

## Microsoft Agentの検証が失敗する

`atk doctor`、環境ファイル、GUID、URL、アイコン、スキーマ版を確認します。Toolkit更新後は`atk upgrade`も検討します。
