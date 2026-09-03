# 日本語文書の推敲記録

- 最新の全体見直し: 2026-09-03
- 初回の開発文書一括見直し: 2026-09-01
- 対象: 公開トップページ、利用者向けガイド、日本語で記述する利用者向け実行文、開発・保守・研究・実験・運用文書
- 原則: 内容と技術的な意味を確定した後、自然な日本語であることを最優先して文書全体を読み直す

## この記録の目的

日本語文書では、内容が正しいことと、日本語として自然に読めることを別々に確認する。

まず事実、識別子、数値、比較条件、証拠の境界を固める。その後に文書全体を通読し、英語の研究用語や製品用語が日本語文の骨格へそのまま入り込んでいないか、名詞が連続して意味を取りにくくなっていないか、助詞や主語の省略によって読み手へ余計な解釈負担をかけていないかを確認する。

スキーマのフィールド名、コマンド、コミット、正式な製品名、比較条件のラベルなど、識別に必要な表記は原則として保持する。識別子を日本語化することではなく、その周囲の説明を自然な日本語へ整えることを目的とする。

## 現在の鮮度管理対象

次の文書は、全文を日本語として読み直した状態を`natural-japanese-review-manifest.json`で管理する。すでに十分自然な文書は、記録のためだけに書き換えない。

### 公開トップページと利用者向けガイド

- `README.md`
- `docs/ja/getting-started.md`
- `docs/ja/usage-context.md`
- `docs/ja/platforms/chatgpt-gpt.md`
- `docs/ja/platforms/claude-code.md`
- `docs/ja/platforms/codex.md`
- `docs/ja/platforms/microsoft-copilot.md`
- `docs/ja/platforms/project-instructions.md`

### 利用者向け実行文

- `adapters/microsoft-copilot/ja-JP/instructions.md`
- `adapters/microsoft-copilot/ja-JP/package-readme.txt`

Microsoft 365向けのこの2ファイルは、生成物そのものではなく、その日本語本文を生み出すadapter側の正本である。利用者が直接読む実行指示とパッケージ内説明であるため、方法論正本とは分けたまま、日本語の鮮度管理対象に含める。

### 開発・保守・研究・実験・運用文書

- `docs/ja/architecture.md`
- `docs/ja/maintainers/development.md`
- `docs/ja/maintainers/framework-loading-depth-observation.md`
- `docs/ja/maintainers/framework-use-lifecycle-trace.md`
- `docs/ja/maintainers/kj-atlas-case-portfolio-freeze.md`
- `docs/ja/maintainers/kj-atlas-case000-lessons.md`
- `docs/ja/maintainers/kj-atlas-case001-longitudinal-companion.md`
- `docs/ja/maintainers/kj-atlas-cognitive-coevolution.md`
- `docs/ja/maintainers/natural-japanese-review.md`
- `docs/ja/maintainers/official-sources.md`
- `docs/ja/maintainers/release.md`
- `docs/ja/maintainers/troubleshooting.md`
- `docs/ja/maintainers/v39-deepseek-api-validation.md`
- `docs/ja/maintainers/versioning.md`
- `docs/ja/experiments/web-chat-living-lab.md`
- `.living-lab/README.md`の日本語部分
- `research/living-lab/observations/README.md`

## 見直しの履歴

### 2026-09-01

開発・保守・研究・実験・運用文書を一括して通読した。英語を直訳したような語順、名詞の過度な連結、不自然な助詞、省略しすぎた主語などを中心に修正した。すでに十分自然だった`docs/ja/maintainers/official-sources.md`と`docs/ja/maintainers/troubleshooting.md`は、通読したうえで変更しなかった。

### 2026-09-03

リリース・開発手順をGitHub Actions無効化後の現行運用へ合わせて再度全文推敲した。さらに、公開トップページと利用者向けガイドも鮮度管理の対象へ加え、内容を現在の製品情報と照合したうえで全文を読み直した。

`docs/ja/getting-started.md`、`docs/ja/usage-context.md`、ChatGPT・Claude Code・Codex・Microsoft 365 Copilotの各ガイドは、日本語の流れを整えた。`README.md`はMicrosoft 365版の現行制約を明示するために更新した。`docs/ja/platforms/project-instructions.md`は全文を通読したが、意味のある改善差分は不要と判断して本文を維持した。

製品仕様に関する実質的な更新は、文体修正とは分けて扱った。CodexにはGitHubマーケットプレイスをワークスペースへインポートする現行経路を日英で補足した。Microsoft 365 Copilotでは、「最大20件」が端末から直接アップロードする埋め込みファイルの上限であることを明確にしたうえで、公式資料を再確認した。

その再確認により、Microsoft 365 CopilotのKnowledgeは事実のグラウンディングに使うもので、8,000文字のInstructions制限を回避するために方法論の実行指示をKnowledgeへ退避する構成は前提にできないことが分かった。利用者向けガイドではまずこの制約を明示し、Issue #96でadapter本体の再設計へ進んだ。

Issue #96の再設計では、Microsoft 365版を無理に完全対応とせず、`instructions.txt`だけで自己完結する限定プロファイルへ改めた。詳細な方法モジュールは、エージェントの実行指示ではなく人間向け参照資料であることが分かるよう`method-reference/`へ分離した。Microsoft 365のKnowledgeは、利用者が分析対象とする業務資料や調査資料などの事実グラウンディングに使う。

この再設計に伴い、`adapters/microsoft-copilot/ja-JP/instructions.md`と`package-readme.txt`を全文で読み直した。限定プロファイルであることを理由に必要以上に判断を弱めず、一方で実行できない詳細手順を実行したように見せない境界を、日本語として自然に読める形へ整えた。

この修正では、Microsoft 365固有の制約をCSW全体の方法論へ逆流させていない。`src/ja-JP/`は変更せず、プラットフォーム固有の実行範囲とパッケージ構造だけをadapter側で明示している。

## 対象外として扱うもの

次は、この鮮度管理へ機械的には含めない。

- `src/ja-JP/`: 方法論の意味上の正本。変更には方法上の理由と翻訳同期が必要であり、文章の自然さだけを理由に別工程で書き換えない。
- 英語文書: 自然な日本語という基準の対象外。日本語側で事実関係を変えた場合は、必要に応じて意味を同期する。
- `research/living-lab/observations/*.json`: 観測データ。自由記述欄は元の観測内容を保持し、文体だけを理由に履歴データを書き換えない。
- 生成物: 元文書やadapterを修正し、生成結果そのものを直接推敲しない。

対象外であっても、日本語の成果物を新たに作成する場合は自然な日本語を重視する。ただし、それぞれが持つ意味管理・履歴保存・生成物管理の境界を壊してまで、このmanifestへ統合しない。

## 今後の運用

新しい対象文書を作る場合も、既存文書を更新する場合も、次の順序を守る。

1. 内容と構造を作る。
2. 技術的な意味と証拠の境界を確認する。
3. 自然な日本語を最優先して、文書全体を独立して推敲する。
4. 推敲を終えた文書をレビューmanifestへ記録する。
5. PRで、この推敲工程を実施したことを確認する。

この工程は、文章を装飾的にするためのものではない。技術文書、利用者向けガイド、実行指示の意味を、読者が頭の中で余計な翻訳をしなくても受け取れる形へ整えるための工程である。

## 推敲記録の鮮度を確認する

`docs/ja/maintainers/natural-japanese-review-manifest.json`には、推敲済み文書ごとのGit blob SHAと確認日を記録する。

manifestの役割は、日本語の良し悪しを機械判定することではない。**推敲後に本文が変わっていないことを確認し、更新された文書が古い推敲記録のまま`make check`の鮮度検査を通ることを防ぐ**ための管理記録である。

文書を全文推敲した後、実際に確認した文書だけを明示して記録する。

```bash
python scripts/check_natural_japanese_review.py \
  --record docs/ja/maintainers/example.md \
  --review-date YYYY-MM-DD
```

複数の文書を同時に推敲した場合は、`--record`の後へパスを並べる。

その後に`make check`を実行する。対象文書が新規追加された、削除された、または推敲記録後に変更された場合、鮮度検査は停止して差分を報告する。

manifestを更新する操作そのものは、推敲を実施した証明にはならない。内容が固まった文書を実際に通読し、自然な日本語として整えた後にだけ記録を更新する。
