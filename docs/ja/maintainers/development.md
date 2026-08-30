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

## 研究・検証記録

方法論へ規則を追加する前に、観察・実験・帰属判定をmaintainer文書へ残します。単一ケースや単一モデルの所見を、直ちに`src/<locale>/`へ昇格させません。

- `v39-deepseek-api-validation.md`: fresh-context API検証の負結果、装置上の限界、現行方法論へ実際に帰属した変更。
- `kj-atlas-cognitive-coevolution.md`: KJ Atlas dogfoodによる長期4arm比較と、skill / caller / product / experimentの帰属ゲート。
- `kj-atlas-case000-lessons.md`: 比較プロトコル以前の既存dogfoodを遡及的に読んだ初期教訓。
- `framework-loading-depth-observation.md`: frameworkをどこまでworking contextへ読み込んだかと、増分・anchoring・early stopの関係を長期観察する補助プロトコル。
- `framework-use-lifecycle-trace.md`: frameworkが候補に上がった段階、実際に読んだ範囲、体系固有操作、対象側への採用を分離して追う研究用来歴。
- `kj-atlas-case001-longitudinal-companion.md`: 独立4armを汚さず、継続チャットで問いの遅延効果・再活性化・KJ再編・実採用を追うprospective companion lane。

研究文書は、現行方法論の根拠や限界を追えるようにするための履歴です。方法論正本と同じ規範力を持たせません。
