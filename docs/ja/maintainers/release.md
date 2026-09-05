# リリース手順

## 1. リリース候補を確定する

通常は、対象バージョンの統合線 `develop/vX.Y.Z` をリリース候補とします。ブランチ名に含まれる版と、次の版情報を一致させます。

- `VERSION`
- `src/manifest.json`
- `pyproject.toml`
- `CHANGELOG.md`

版を決める目安は次のとおりです。

- major: 中核原則、発動条件、評価構造に関わる非互換変更
- minor: 後方互換性のある規則、モジュール、言語、アダプターの追加
- patch: 誤記、明確化、翻訳修正、配布・ビルド修正

安定化のための修正を通常開発から分けたい場合に限り、`develop/vX.Y.Z` から `release/vX.Y.Z` を切ります。リリース用ブランチでは、リリース成立に必要な修正、文書、版情報の整理に範囲を絞り、新しい方法論機能は原則として追加しません。

リリース用ブランチを使わない場合は、`develop/vX.Y.Z` をそのまま `main` へのリリース候補にできます。

## 2. `main` との差分を確認する

リリース候補を作った後に `main` が進んでいる場合は、`main` の変更を先にリリース候補へ取り込みます。リリース時だけ古い `main` へ戻したり、両者の差分を暗黙に捨てたりしません。

少なくとも次を確認します。

```bash
git fetch origin
git log --oneline --left-right origin/main...HEAD
```

`main` にだけ存在する変更がある場合は、その内容を確認してリリース候補へ統合し、検査をやり直します。

## 3. 翻訳状態とCHANGELOGを確認する

`i18n/translation-manifest.json` を確認します。日本語正本を変更した後、英語版が参照する翻訳元ハッシュが古いままだと、リリース検証は失敗します。

公開前には、`CHANGELOG.md` の対象となる `Unreleased` の変更を、次の形式の日付付きの節へ移します。

```text
## X.Y.Z — YYYY-MM-DD
```

その後の開発に使う新しい `## Unreleased` 節は残します。実際に公開する変更内容と、日付付きの節の記載が一致していることも確認します。新しい `## Unreleased` 節は公開が完了するまで空のままにし、公開対象の変更が残っている場合は、日付付きの節へ移してからこの検査を通します。日付付きの節そのものも空にはせず、公開する内容を記載します。

日付付きの公開境界が一つだけ存在することを、明示的に検査します。

```bash
python scripts/check_release_changelog.py \
  --version "$(cat VERSION)"
```

この検査に通らない状態では公開へ進みません。パッケージを正常に作れたとしても、CHANGELOGの公開境界が確定していない状態でリリースしないための確認です。

## 4. リリース候補を検査する

リリース候補上で次を実行します。

```bash
make release-check
```

少なくとも次を確認します。

- `dist/reports/validation-report.json`
- `dist/reports/token-budget.json`
- `dist/reports/living-lab-observation-summary.json`
- `dist/release-manifest.json`
- `dist/packages/` の言語別ZIP

`make release-check`には`make check`が含まれます。`develop/vX.Y.Z`または`release/vX.Y.Z`上では、ブランチ名の版と`VERSION`の一致もこの中で確認されます。

公開パッケージは、Gitの作業ツリーに未コミットの変更がない状態でだけ作成します。追跡中のファイルに未コミットの変更がある場合や、Gitに無視されていない未追跡ファイルがある場合は、パッケージ生成とリリース検証を停止します。`dist/`、`.tmp/`、ローカルLiving Lab領域など、`.gitignore`で明示的に除外している作業用ファイルはこの判定には含まれません。

最終`release-manifest.json`はschema 2で、`source_commit`にパッケージを生成したGitコミットを記録します。`source_commit`が生成物の来歴として意味を持つのは、パッケージ生成時の作業ツリーが上記の状態にある場合だけです。`release-validate`は、作業ツリーに未コミット差分がないことに加え、`source_commit`が検査時の`HEAD`と一致することも確認します。これにより、公開後にタグが指すコミットを、生成物の来歴へ戻して照合できます。

GitHub Actionsは現在リポジトリで無効化されています。また、`main`のbranch protectionとrepository rulesetも現時点では設定されていません。リモートの検査結果が表示されないことや、pushが受理されたことを、ローカル検査が成功した証拠として扱いません。

`make release-check`を実行できない環境からリリース作業を進めないでください。通常のPRでやむを得ずローカル実行できなかった場合とは異なり、公開リリースでは、実際にパッケージを生成して検証できる環境を用意することを必須とします。

## 5. PRで `main` へ統合する

方法論やリリース内容を `main` へ直接コミットしません。

- リリース用ブランチを使う場合: `release/vX.Y.Z` → `main`
- 使わない場合: `develop/vX.Y.Z` → `main`

PRでは、累積差分、版情報、CHANGELOG、翻訳状態、`make release-check` の結果を確認します。修正が必要な場合はリリース候補側へ入れ、検査をやり直します。

`main`へ統合するときは、squash mergeやrebase mergeではなく、2つの親を持つ通常のマージコミットを作る方法を選びます。PRをマージした後は、その`main`のマージコミットが公開版の正本になります。

このPR経由の運用は、現在GitHubのbranch protectionやrulesetによって自動的に強制されているわけではありません。GitHub側の保護設定がないことと、リポジトリとしてPR経由を求めることは分けて扱います。

## 6. 公開版のコミットをもう一度検査し、タグを付ける

リリース候補で検査済みでも、タグを付けるのは `main` へ統合された後のコミットです。公開物が、実際にタグを付けるコミットと同じ内容から生成されたことを確認するため、`main` の実際の公開コミットでも検査をやり直します。

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
make main-contract
make release-check
git merge-base --is-ancestor HEAD origin/main
TAG="v$(cat VERSION)"
make release-tag-contract TAG="$TAG"
```

四つの検査をそれぞれ確認します。

- `make main-contract`: 現在のブランチが`main`で、HEADがちょうど2つの親を持つマージコミットの形になっていること。
- `make release-check`: 公開する生成物とリリース契約が、作業ツリーに未コミット差分のない状態でそのコミットから生成され、最終manifestの`source_commit`がそのHEADを記録していること。
- `git merge-base --is-ancestor`: 現在のコミットが実際に`origin/main`の履歴へ入っていること。
- `make release-tag-contract`: `origin/main`をリモートから更新して、現在のHEADが最新の`origin/main`履歴に含まれることをtarget自身でも再確認します。そのうえで、タグ固有の検査に入る前に`release-validate`を再実行して最終release set全体がなお有効であることを確かめ、`VERSION`から導出したタグ名、`VERSION`、最終`release-manifest.json`の版、clean worktree、`source_commit == HEAD`、日付付きCHANGELOG境界を確認します。

`make main-contract`が確認できるのはコミットの形状までです。2つの親を持つことだけから、そのコミットが実際にGitHubのPRから生成されたことまでは証明できません。また、このコマンドはGitHubへの直接pushを事前に拒否する仕組みでもありません。いずれかの検査が失敗した場合はタグを付けず、原因を修正し、必要な開発線へ戻してから改めて`main`へ統合します。

検査が成功したら、検査済みの`TAG`をそのコミットへ付けます。タグ名を別途入力し直しません。

```bash
git tag "$TAG"
git push origin "$TAG"
make release-remote-tag-contract TAG="$TAG"
```

`release-remote-tag-contract`は、リモートタグ固有の検査に入る前にも`release-validate`を再実行し、現在のmanifest・package・report・hash・clean worktreeが最終release setとしてなお有効であることを確認します。その後、指定したタグ名が最終manifestの版と一致すること、最終manifestの`source_commit`がリポジトリ方針どおり2つの親を持つマージコミットの形であること、そのコミットが現在のリモート`main`履歴に含まれていること、対象版のCHANGELOG公開境界が凍結済みであることを確認します。さらにリモートタグを取得し、軽量タグでも注釈付きタグでも最終的に指すコミットまで解決して、`source_commit`との一致を照合します。現在のブランチ自体が`main`であることは要求しないため、同じrelease commitの別のclean checkoutからも再検証できます。ここで確認する2親形状も、`main-contract`と同じく、それだけでPR由来を証明するものではありません。

公開済みタグの内容を後から無言で差し替えません。修正が必要な場合はパッチ版を作ります。

## 7. GitHub Releaseへ成果物を公開する

現在はGitHub ActionsによるReleaseの自動公開を行いません。タグをpushした後、直前の `make release-check` が生成した `dist/release-manifest.json` の `release_assets` に列挙されたファイルを、同じタグのGitHub Releaseへ手動で公開します。

GitHubのWeb画面から公開してもかまいません。GitHub CLIを使う場合は、たとえば次のようにmanifestから公開対象を取り出せます。

```bash
TAG="v$(cat VERSION)"
make release-tag-contract TAG="$TAG"
make release-remote-tag-contract TAG="$TAG"

mapfile -t ASSETS < <(
  python - <<'PY'
import json
from pathlib import Path

manifest = json.loads(Path("dist/release-manifest.json").read_text(encoding="utf-8"))
for relative in manifest["release_assets"]:
    print((Path("dist") / relative).as_posix())
PY
)

gh release create "$TAG" "${ASSETS[@]}" \
  --verify-tag \
  --generate-notes \
  --notes "$(cat .github/release-validation-note.md)"
```

`--notes`で追加する検証状況の注記も公開契約の一部であり、公開後にもう一度確認します。GitHubのWeb画面から公開する場合も、Release本文に`.github/release-validation-note.md`と同じ内容を含めます。

既存のReleaseへ成果物を追加・修正する必要がある場合も、公開済み版を黙って差し替える運用にはしません。原則としてパッチ版を作ります。

## 8. 公開済みReleaseを検証する

公開後は、リモートタグの版が最終manifestと一致し、そのタグが引き続きmanifestの`source_commit`を指していることに加え、`source_commit`が2つの親を持つマージコミットの形を保ち、現在のリモート`main`履歴に残っていることと、対象版のCHANGELOG公開境界が凍結されたままであることを確認します。そのうえで、GitHub上のReleaseが最終的な公開契約を満たしていることも検証します。GitHub CLIを使う場合の例です。

```bash
TAG="v$(cat VERSION)"
mkdir -p .tmp

make release-remote-tag-contract TAG="$TAG"

gh api "repos/hat47x/cultural-substrate-weaving/releases/tags/${TAG}" \
  > .tmp/published-release.json

python scripts/verify_published_release.py \
  --manifest dist/release-manifest.json \
  --release-json .tmp/published-release.json \
  --tag "$TAG"
```

ここでは二つの異なる境界を確認します。`release-remote-tag-contract`はrelease set全体を再検証したうえで、リモートタグ名と最終manifestの版、`source_commit`の2親マージコミット形状、`source_commit`と現在のリモート`main`履歴、対象版のCHANGELOG公開境界、リモートタグが最終的に指すコミットと`source_commit`をそれぞれ照合します。`verify_published_release.py`は独立してmanifestの版とタグ名を再確認し、Releaseがdraftやprereleaseではなく、本文に`.github/release-validation-note.md`の開示文が含まれていることを確かめたうえで、成果物名、サイズ、ダイジェストをGitHub Release上の実物と照合します。片方の成功を、もう片方の代わりにはしません。

## 9. 次の開発線を始める

リリース後の新しい `develop/vA.B.C` は、タグを付けた最新の `main` から切ります。リリース用ブランチにだけ入った修正を、後続の開発線から欠落させないためです。

緊急修正は `hotfix/vX.Y.Z` を `main` から切り、公開後は必要に応じて進行中の開発線にも戻します。

## 10. 各プラットフォームでの公開を確認する

- Claude Code: Marketplaceの版をタグと一致させる。
- ChatGPT GPTs: 言語別の更新パックをGPTエディターへ手動で反映する。
- Microsoft 365 Copilot: ステージングで検証した後、管理者承認を経て本番公開する。

公開済みタグの翻訳を後から無言で差し替えません。翻訳修正もパッチ版として公開します。
