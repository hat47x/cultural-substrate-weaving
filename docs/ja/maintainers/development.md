# 開発手順

## 編集対象

- 方法論の意味上の正本: `src/ja-JP/`
- 英語翻訳: `src/en-US/`
- 翻訳用語・状態: `i18n/`
- プラットフォーム固有の文言や設定: `adapters/`
- テストケース: `evals/`
- 生成処理: `scripts/`

`dist/`を直接編集しません。`plugins/`はClaude Marketplace配布に必要な生成物なので、`build.py`で再生成してコミットします。

## 開発サイクル

```bash
make build
make validate
make test
make tokens
```

`make check`で一括実行できます。

## 正本を変更した場合

1. `src/ja-JP/`を変更する
2. 同じ相対パスの`src/en-US/`を更新する
3. 用語集を確認する
4. 翻訳査読後に次を実行する

```bash
python scripts/update_translation_hashes.py --locale en-US
make check
```

ハッシュ更新コマンドは、翻訳を確認した後にだけ実行してください。
