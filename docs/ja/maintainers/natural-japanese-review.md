# 日本語開発文書の推敲記録

- Review date: 2026-09-01
- Scope: 日本語で記述された開発・保守・研究・実験・運用文書
- Principle: 内容と技術的な意味を確定した後、自然な日本語であることを最優先して文書全体を読み直す

## この記録の目的

日本語の開発文書では、技術的に正しいことと、日本語として自然に読めることを別々に確認する。

今回の見直しでは、まず事実、識別子、数値、比較条件、証拠の境界を固定し、その後に文書全体を通読した。英語の研究用語を日本語文の骨格へそのまま差し込んだ箇所、名詞が連続して意味を取りにくい箇所、助詞や主語の省略によって読みにくくなった箇所を中心に修正した。

schemaのフィールド名、コマンド、commit、正式な製品名、比較条件のラベルなど、識別に必要な表記は原則として変更していない。

## 今回、全文を推敲して修正した文書

- `docs/ja/architecture.md`
- `docs/ja/maintainers/development.md`
- `docs/ja/maintainers/framework-loading-depth-observation.md`
- `docs/ja/maintainers/framework-use-lifecycle-trace.md`
- `docs/ja/maintainers/kj-atlas-case-portfolio-freeze.md`
- `docs/ja/maintainers/kj-atlas-case000-lessons.md`
- `docs/ja/maintainers/kj-atlas-case001-longitudinal-companion.md`
- `docs/ja/maintainers/kj-atlas-cognitive-coevolution.md`
- `docs/ja/maintainers/release.md`
- `docs/ja/maintainers/v39-deepseek-api-validation.md`
- `docs/ja/maintainers/versioning.md`
- `docs/ja/experiments/web-chat-living-lab.md`
- `.living-lab/README.md`の日本語部分
- `research/living-lab/observations/README.md`

## 通読し、意味を変える差分は不要と判断した文書

- `docs/ja/maintainers/official-sources.md`
- `docs/ja/maintainers/troubleshooting.md`

これらも推敲工程そのものは実施している。差分を作ることを目的化せず、現状の日本語が十分に自然で、書き換えによる改善が小さい場合はそのまま維持した。

## 今回の対象外

次は今回の「開発文書の自然な日本語」見直しとは目的が異なるため、文体だけを理由には変更していない。

- `src/ja-JP/`: 方法論の意味上の正本。変更には方法上の理由と翻訳同期が必要。
- `docs/ja/getting-started.md`、`docs/ja/platforms/`、`docs/ja/usage-context.md`: 利用者向け文書。別途、利用者向け文書としての読みやすさを評価する。
- `README.md`: 公開トップページ。開発文書とは分けて扱う。
- 英語文書: 自然な日本語という基準の対象外。
- `research/living-lab/observations/*.json`: 観測データ。自由記述欄は元の観測内容を保持し、文体だけを理由に履歴データを書き換えない。
- 生成物: 元文書やテンプレートを修正し、生成結果を直接推敲しない。

## 今後の運用

新しい日本語開発文書を作る場合も、既存文書を大きく更新する場合も、次の順序を守る。

1. 内容と構造を作る。
2. 技術的な意味と証拠の境界を確認する。
3. 自然な日本語を最優先して、文書全体を独立して推敲する。
4. 推敲を終えた文書をレビューmanifestへ記録する。
5. PRで、この推敲工程を実施したことを確認する。

この工程は、文章を装飾的にするためのものではない。技術文書の意味を、読者が余計な翻訳作業をせずに受け取れる形へ整えるための工程である。

## 推敲記録の鮮度を確認する

`docs/ja/maintainers/natural-japanese-review-manifest.json`には、推敲済み文書ごとのGit blob SHAと確認日を記録する。

manifestの役割は、日本語の良し悪しを機械判定することではない。**推敲後に本文が変わっていないことを確認し、更新された文書が古い推敲記録のままCIを通ることを防ぐ**ための鮮度管理である。

文書を全文推敲した後、変更した文書だけを明示して記録する。

```bash
python scripts/check_natural_japanese_review.py \
  --record docs/ja/maintainers/example.md \
  --review-date YYYY-MM-DD
```

複数の文書を同時に推敲した場合は、`--record`の後へパスを並べる。

その後に`make check`を実行する。対象文書が新規追加された、削除された、または推敲記録後に変更された場合、鮮度検査はfail closedで停止する。

manifestを更新する操作そのものは、推敲を実施した証明にはならない。内容が固まった文書を実際に通読し、自然な日本語として整えた後にだけ記録を更新する。
