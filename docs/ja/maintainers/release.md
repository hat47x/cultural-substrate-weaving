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

その後の開発に使う新しい `## Unreleased` 節は残します。実際に公開する変更内容と、日付付きの節の記載が一致していることも確認します。

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
- `dist/release-manifest.json`
- `dist/packages/` の言語別ZIP

GitHub Actionsは現在リポジトリで無効化されています。リモートの検査結果が表示されないことを、検査が成功した証拠として扱いません。

`make release-check` を実行できない環境からリリース作業を進めないでください。通常のPRでやむを得ずローカル実行できなかった場合とは異なり、公開リリースでは、実際にパッケージを生成して検証できる環境を用意することを必須とします。

## 5. PRで `main` へ統合する

方法論やリリース内容を `main` へ直接コミットしません。

- リリース用ブランチを使う場合: `release/vX.Y.Z` → `main`
- 使わない場合: `develop/vX.Y.Z` → `main`

PRでは、累積差分、版情報、CHANGELOG、翻訳状態、`make release-check` の結果を確認します。修正が必要な場合はリリース候補側へ入れ、検査をやり直します。

PRをマージした後は、`main` のマージコミットが公開版の正本になります。

## 6. 公開版のコミットをもう一度検査し、タグを付ける

リリース候補で検査済みでも、タグを付けるのは `main` へ統合された後のコミットです。公開物が、実際にタグを付けるコミットと同じ内容から生成されたことを確認するため、`main` の実際の公開コミットでも `make release-check` を再実行します。

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
make release-check
git merge-base --is-ancestor HEAD origin/main
```

`make release-check` と `git merge-base --is-ancestor` の両方が成功したことを確認します。後者は、現在のコミットが実際に `origin/main` の履歴へ入っていることを確かめるための検査です。

どちらかが失敗した場合はタグを付けません。原因を修正し、必要な開発線へ戻してから改めて `main` へ統合します。

検査が成功したら、`VERSION` と同じ版のタグを、そのコミットへ付けます。

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

公開済みタグの内容を後から無言で差し替えません。修正が必要な場合はパッチ版を作ります。

## 7. GitHub Releaseへ成果物を公開する

現在はGitHub ActionsによるReleaseの自動公開を行いません。タグをpushした後、直前の `make release-check` が生成した `dist/release-manifest.json` の `release_assets` に列挙されたファイルを、同じタグのGitHub Releaseへ手動で公開します。

GitHubのWeb画面から公開してもかまいません。GitHub CLIを使う場合は、たとえば次のようにmanifestから公開対象を取り出せます。

```bash
TAG=vX.Y.Z

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

既存のReleaseへ成果物を追加・修正する必要がある場合も、公開済み版を黙って差し替える運用にはしません。原則としてパッチ版を作ります。

## 8. 公開済みReleaseを検証する

公開後は、GitHub上のReleaseが最終manifestと一致していることを確認します。GitHub CLIを使う場合の例です。

```bash
TAG=vX.Y.Z
mkdir -p .tmp

gh api "repos/hat47x/cultural-substrate-weaving/releases/tags/${TAG}" \
  > .tmp/published-release.json

python scripts/verify_published_release.py \
  --manifest dist/release-manifest.json \
  --release-json .tmp/published-release.json \
  --tag "$TAG"
```

この検証では、manifestに記載された成果物名、サイズ、ダイジェストと、GitHub Release上の実物が一致していることを確認します。

## 9. 次の開発線を始める

リリース後の新しい `develop/vA.B.C` は、タグを付けた最新の `main` から切ります。リリース用ブランチにだけ入った修正を、後続の開発線から欠落させないためです。

緊急修正は `hotfix/vX.Y.Z` を `main` から切り、公開後は必要に応じて進行中の開発線にも戻します。

## 10. 各プラットフォームでの公開を確認する

- Claude Code: Marketplaceの版をタグと一致させる。
- ChatGPT GPTs: 言語別の更新パックをGPTエディターへ手動で反映する。
- Microsoft 365 Copilot: ステージングで検証した後、管理者承認を経て本番公開する。

公開済みタグの翻訳を後から無言で差し替えません。翻訳修正もパッチ版として公開します。
