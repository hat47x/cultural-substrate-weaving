# 日本語文書の推敲記録

- 最新の全体見直し: 2026-09-04
- 初回の開発文書一括見直し: 2026-09-01
- 対象: 公開トップページ、利用者向けガイド、公開リリース文、日本語で記述する利用者向け実行文、開発・保守・研究・実験・運用文書
- 原則: 内容と技術的な意味を確定した後、自然な日本語であることを最優先して文書全体を読み直す

## この記録の目的

日本語文書では、内容が正しいことと、日本語として自然に読めることを別々に確認する。

まず事実、識別子、数値、比較条件、証拠の境界を固める。その後に文書全体を通読し、英語の研究用語や製品用語が日本語文の骨格へそのまま入り込んでいないか、名詞が連続して意味を取りにくくなっていないか、助詞や主語の省略によって読み手へ余計な解釈負担をかけていないかを確認する。

スキーマのフィールド名、コマンド、コミット、正式な製品名、比較条件のラベルなど、識別に必要な表記は原則として保持する。識別子を日本語化することではなく、その周囲の説明を自然な日本語へ整えることを目的とする。

## 現在の鮮度管理対象

次の文書は、全文を日本語として読み直した状態を`natural-japanese-review-manifest.json`で管理する。すでに十分自然な文書は、記録のためだけに書き換えない。

### 公開トップページ、利用者向けガイド、公開リリース文

- `README.md`
- `docs/README.md`
- `.github/release-validation-note.md`の日本語部分
- `docs/ja/getting-started.md`
- `docs/ja/usage-context.md`
- `docs/ja/platforms/chatgpt-gpt.md`
- `docs/ja/platforms/claude-code.md`
- `docs/ja/platforms/codex.md`
- `docs/ja/platforms/microsoft-copilot.md`
- `docs/ja/platforms/project-instructions.md`

Release validation noteはGitHub Releaseへ利用者向けの検証状況としてそのまま掲載される。日本語を含む公開文であるため、技術的な公開契約とは分けたまま、日本語部分の鮮度を管理する。

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
- `docs/ja/maintainers/kj-atlas-merge-semantics-boundary.md`
- `docs/ja/maintainers/natural-japanese-review.md`
- `docs/ja/maintainers/official-sources.md`
- `docs/ja/maintainers/release.md`
- `docs/ja/maintainers/troubleshooting.md`
- `docs/ja/maintainers/v39-deepseek-api-validation.md`
- `docs/ja/maintainers/versioning.md`
- `docs/ja/experiments/web-chat-living-lab.md`
- `.living-lab/README.md`の日本語部分
- `research/human-use-gap-kj/README.md`
- `research/living-lab/observations/README.md`

`research/human-use-gap-kj/README.md`は、個々の研究記録そのものではなく、どの文書を現在地として読むかを案内する継続更新索引である。日付付きの研究記録を後から文体だけの理由で書き換えることは避けつつ、現在地を案内する索引が古い研究状態を指し続けないよう、このREADMEだけを鮮度管理対象に含める。

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

### 2026-09-04

GitHub Actions無効化後のローカル検査を再点検し、旧workflowにだけ残っていたGit管理生成物の鮮度検査を`make check`へ戻した。この変更に合わせて`docs/ja/maintainers/development.md`を全文で読み直し、`.claude-plugin/`、`.agents/`、`plugins/`が生成・Git管理する配布成果物であること、再生成後に変更・削除・未追跡の差分が残れば検査が失敗すること、意図しない差分は生成物を直接直さず入力側へ戻って修正することを、前後の流れを含めて自然な日本語へ整えた。

また、`docs/ja/maintainers/kj-atlas-merge-semantics-boundary.md`を全文で読み直した。KJ Atlas固有の実装語彙とCSWの方法論正本を分ける技術的な意味を確認したうえで、日本語本文はそのままで自然に読めると判断し、記録のためだけの本文変更は行わなかった。鮮度管理対象への登録だけを追加した。

Living Labの公開記録がprospectiveな観測だけでなく、自然な実作業を後から匿名化・抽象化したretrospectiveな記録も含むようになったことに合わせ、`.github/release-validation-note.md`も全文を読み直した。公開時の検証状況説明が両者を区別し、技術的なrelease checkやpackage検証を方法論の有効性証拠へ読み替えないことを確認したうえで、同ファイルを鮮度管理対象へ追加した。

人的利用ギャップ研究では、`research/human-use-gap-kj/README.md`がPR #90後の状態を「最新」として案内したまま、PR #126/#127で行ったcandidate recallの再基準化と正本化を反映していなかった。個々の研究記録は当時の問題設定を残す履歴として維持し、索引READMEだけをPR #127後の現在地へ更新した。全文を読み直し、R1の有効性が実証されたとは書かず、静的残差が後退して自然な挙動観察へ戻ったことが分かるよう整えたうえで、この索引を鮮度管理対象へ追加した。

方法論正本の意味には触れておらず、今回の見直しは開発・配布成果物の保守境界と研究・保守・公開文書の推敲記録に限っている。

## 対象外として扱うもの

次は、この鮮度管理へ機械的には含めない。

- `src/ja-JP/`: 方法論の意味上の正本。変更には方法上の理由と翻訳同期が必要であり、文章の自然さだけを理由に別工程で書き換えない。
- 英語文書: 自然な日本語という基準の対象外。日本語側で事実関係を変えた場合は、必要に応じて意味を同期する。
- `research/living-lab/observations/*.json`: 観測データ。自由記述欄は元の観測内容を保持し、文体だけを理由に履歴データを書き換えない。
- `research/human-use-gap-kj/`配下の日付付き研究記録: 各時点の問題設定、読み違い、訂正過程を含む研究履歴であるため、文体だけを理由に後から書き換えない。現在地を案内する`README.md`だけは別に鮮度管理する。
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

## 2026-09-05の追加レビュー

`docs/ja/maintainers/skill-improvement-direction.md` は、正本・検証コード・公開研究記録との照合を終えた後、全文を独立して通読した。発動範囲と探索・帰属の区別を保ち、語順や助詞、不自然な名詞の連続を修正した。確認済みの事実と改善仮説、旧実験と現行版の証拠の境界は変更していない。

文書案内を追加した `docs/README.md` と、この推敲記録も全文を通読し、周囲の記述とのつながりを確認した。

続いて `docs/ja/maintainers/longitudinal-cognitive-functions.md` を追加し、内容確定後に全文を独立して通読した。認知機能の仮説と実例で確認した事実を区別し、包括化・制御・再現性の意味が連続した文章で伝わるように推敲した。KJ法の生成的な働きと、文化的意味を数理的構造へ還元しきらないという論点も確認した。中心方針を更新した `docs/ja/maintainers/skill-improvement-direction.md` と文書案内についても、周囲の文章を含めて再読した。

企業活動における人間とAIの協働という構想を追記した後、上記二つの方針文書を再び通読した。留保・識別・広域視野の関係、十分なトークンを使って積み上げるもの、本スキルと領域知識・外部記憶・ツールの役割が自然につながるように推敲した。能力の獲得目標と、既に確認した実行結果を混同していないことも確認した。

## 2026-09-06の追加レビュー

`docs/ja/maintainers/v05-cognitive-prompt-roadmap.md`は、段階的な改善方針と独立試行の記録を確定した後、全文を通読した。既存機能、今回の明確化、今後調べる効果が混ざらないように確認し、問いから次の確認へ進む流れを自然な日本語で記述した。試行の出力と担当AIによる解釈も区別した。案内を更新した`docs/README.md`と本記録も、文書全体のつながりを確認した。

`docs/README.md`は以前から全文を通読した記録があった一方、鮮度管理のcheckerとmanifestには含まれていなかった。文書案内の更新後にあらためて全文を読み直し、識別に必要な英語ラベルは残しつつ、日本語文中にそのまま入り込んでいた英語表現や不自然な連結を整えたうえで、鮮度管理対象へ正式に追加した。方法論正本の意味、翻訳の位置づけ、研究・生成物との境界は変更していない。

KJ法由来の技能をCSWから分離する検討として、新しく七つの文書を追加した。`docs/ja/maintainers/affinity-core-and-iterative-synthesis-layering.md`は、一回の材料統合を担う層と複数ラウンドを管理する層をどう分けるかを整理した。`docs/ja/maintainers/external-skill-assimilation-process.md`は、既存Agent Skillの機構を比較して取り込む際の手順を定めた。`docs/ja/maintainers/external-skill-feature-adoption-log.md`は、その手順に沿って個々の外部Skillを採否判定した記録である。`docs/ja/maintainers/kj-skill-delegation-review.md`は、既存の公開Skillへ全面移譲できるかどうかを検討し、できないという結論とその理由を記録した。`docs/ja/maintainers/kj-split-migration-audit.md`は、現行`integration.md`と`iteration.md`の各責務をどの層へ移すかを表形式で監査した。`docs/ja/maintainers/kj-split-packaging-and-dependency-design.md`は、複数Skillへ分けた場合の配布形式と依存関係の設計案を比較した。`docs/ja/maintainers/material-led-synthesis-method-boundary.md`は、分離後の材料統合方法そのものの定義と不変条件をまとめた。

これら七文書は、内容と技術的な意味が固まった状態で全文を通読した。英語の技術用語や識別子が日本語の文の骨格に不自然な影響を与えていないかを中心に確認し、いずれも既に自然な日本語として読めると判断したため、記録のためだけの本文変更は行わなかった。方法論正本である`src/ja-JP/`はこの文書群の対象外であり、変更していない。
