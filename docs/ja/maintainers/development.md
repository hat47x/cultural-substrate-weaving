# 開発手順

## 編集対象

主な編集対象は次のとおりです。

- 方法論の意味上の正本: `src/ja-JP/`
- 英語翻訳: `src/en-US/`
- 翻訳用語・翻訳状態: `i18n/`
- プラットフォーム固有の文言や設定: `adapters/`
- テストケース: `evals/`
- 生成処理: `scripts/`

`dist/`は直接編集しません。`.claude-plugin/`、`.agents/`、`plugins/`は、正本やmanifest、adapterなどから生成し、Gitで管理する配布用成果物です。`plugins/`にはClaudeとCodexで共有するスキル本体と、それぞれの配布用メタデータが含まれます。これらを変更する必要がある場合は生成物を直接直すのではなく、元となる正本・manifest・adapterなどを修正し、`make build`で再生成した結果を確認してコミットします。

## 開発サイクル

通常の統合検査には、次を使います。

```bash
make check
```

`make check`は、現在次をまとめて実行します。

- `make repository-contracts`
- `make generated-artifacts-check`（先に`make build`を実行します）
- `make validate`
- `make japanese-docs-check`
- `make test`
- `make tokens`
- `make living-lab-check`
- `make living-lab-summary`

`repository-contracts`では、現在のローカルブランチが`develop/vX.Y.Z`または`release/vX.Y.Z`の場合に、ブランチ名の版と`VERSION`が一致することを確認します。`feature/*`、`fix/*`、`research/*`などの短期ブランチには、この版契約を適用しません。

`generated-artifacts-check`では、まず現在の入力から配布用成果物を再生成し、その後に`.claude-plugin/`、`.agents/`、`plugins/`のGit状態を確認します。追跡中の生成物に変更や削除が残っている場合だけでなく、新しい未追跡の生成物が生じた場合も検査を失敗させます。これにより、正本やadapterを更新したのに、対応する生成物をコミットし忘れた状態を通常の`make check`で検出できます。

この検査に失敗した場合は、差分を確認して必要な生成結果をコミットします。意図しない生成結果であれば、生成物を手作業で合わせるのではなく、正本・manifest・adapter・生成処理など、差分を生んだ入力側へ戻って修正します。

`main`については、通常の短期ブランチ上では「mainへどのように統合されるか」を判定できないため、この確認は`make check`には組み込んでいません。PRをマージした後、`main`のHEADが、リポジトリ運用で想定する「2つの親を持つマージコミット」になっているかを確認するときは、`main`上で次を実行します。

```bash
make main-contract
```

このコマンドは、現在のブランチが`main`であることと、HEADが**ちょうど2つの親を持つこと**を確認するローカル診断です。この形状だけから、そのコミットが実際にGitHubのPRから生成されたことまでは確認できません。また、GitHubへの直接pushを事前に遮断する仕組みでもありません。

GitHub Actionsは現在リポジトリで無効化されています。また、現時点では`main`のbranch protectionとrepository rulesetも設定されていません。そのため、ブランチ契約や生成物の鮮度検査はGitHub側から自動的には強制されません。`make check`や`make main-contract`が成功したことと、GitHubが不適切なpushを拒否することは別の保証として扱います。

必要な箇所だけを調べる場合は、各ターゲットを個別に実行してかまいません。ただし、PRへ出す前には、実行可能な環境で原則として`make check`を通します。

リモートの検査結果が表示されないことを、検査が成功した証拠として扱いません。接続環境などの制約で`make check`を実行できない場合は、PR本文に、実際に確認した契約と未検証の部分を明記します。

公開リリースでは、この例外を使いません。リリース候補と、タグを付ける`main`の公開コミットで`make release-check`を実行できる環境を用意し、`main`では`make main-contract`も確認します。詳細は`release.md`を参照してください。

## 日本語文書を作成・更新する場合

日本語で記述する公開ガイド、開発・保守文書、研究・実験・運用文書は、内容を書き終えた時点で完成とはしません。**内容と構造を固めた後に、自然な日本語であることを最優先する独立した推敲工程を必ず入れます。**

鮮度管理の対象には、少なくとも次を含みます。

- 公開トップページの`README.md`
- `docs/ja/getting-started.md`
- `docs/ja/usage-context.md`
- `docs/ja/platforms/`
- `docs/ja/maintainers/`
- `docs/ja/experiments/`
- 日本語を含む研究・観測用README
- 日本語で記述するアーキテクチャや開発運用の説明文書

PRやIssueで継続的に参照する日本語の設計・検証記録も、同じ基準で推敲します。ただし、履歴として保存する観測データや、方法論の意味上の正本は別の管理境界を持つため、機械的にこの鮮度管理へ含めません。

推奨する順序は次のとおりです。

1. 事実、制約、構造、判断理由、識別子を先に確定する。
2. 技術的な意味、スキーマ名、コマンド、コミット、数値、証拠の境界が変わっていないことを確認する。
3. 内容が固まった後、文書全体を日本語として読み直す。
4. 英語を直訳したような語順、名詞の連結、助詞の不足、同じ主語の過度な省略、長すぎる一文、不要な英語の差し込みを直す。
5. 変更箇所だけでなく、段落どうしのつながりや、見出しから本文への流れも含めて通読する。

スキーマのフィールド名、コマンド名、正式な製品名、比較条件のラベルなど、識別のために必要な英語はそのまま残します。ただし、英語の語順を日本語本文の骨格にはしません。たとえば`framework_use`というフィールド名は保持しても、説明文では「framework useをtraceする」のような表現を必要以上に使わず、「文化体系をどの段階まで利用したかを記録する」のように、日本語の文章として自然な形を優先します。

生成AIが作った初稿、英語資料からの直訳、技術要素を並べただけの下書きは、この推敲を通す前には完成稿とみなしません。

既存文書にも同じ基準を適用します。見直した結果、すでに自然で修正の必要がない文書は、差分を作るためだけに書き換える必要はありません。

## 正本を変更した場合

1. `src/ja-JP/`を変更する。
2. 同じ相対パスの`src/en-US/`を更新する。
3. 用語集を確認する。
4. 翻訳を査読した後に、次を実行する。

```bash
python scripts/update_translation_hashes.py --locale en-US
make check
```

ハッシュ更新コマンドは、翻訳を確認してから実行してください。

## 研究・検証記録

方法論へ新しい規則を加える前に、観察、実験、帰属判定を保守者向け文書として残します。単一ケースや単一モデルで得られた所見を、そのまま`src/<locale>/`へ昇格させません。

主な記録は次のとおりです。

- `v39-deepseek-api-validation.md`: fresh-context API検証で得られた負の結果、実験装置上の限界、そこから現行方法論へ実際に帰属した変更。
- `kj-atlas-cognitive-coevolution.md`: KJ Atlasのdogfoodを用いた長期4-arm比較と、skill / caller / product / experimentを分ける帰属ゲート。
- `kj-atlas-case-portfolio-freeze.md`: KJ Atlas Case 001〜003について、問い、product/skill snapshot、arm treatment、review順序をどの時点で固定したか、および現行CSWを比較条件へ逆流させないための境界。
- `kj-atlas-case000-lessons.md`: 比較プロトコル以前の既存dogfoodを遡及的に読み直して得た初期教訓。
- `framework-loading-depth-observation.md`: 文化体系をどこまで作業コンテキストへ読み込んだかと、有用な増分、anchoring、early stopとの関係を長期的に観察する補助プロトコル。
- `framework-use-lifecycle-trace.md`: 文化体系が候補に上がった段階、実際に読んだ範囲、体系固有の操作、対象側への採用を分けて追跡する研究用の来歴記録。
- `kj-atlas-case001-longitudinal-companion.md`: 独立4-arm比較を汚さず、継続チャットの中で問いの遅延効果、再活性化、KJ再編、実際の採用を追う前向き（prospective）な観察線。

これらの研究文書は、現行方法論の根拠と限界を後から追えるようにするための履歴です。方法論の正本と同じ規範力は持ちません。