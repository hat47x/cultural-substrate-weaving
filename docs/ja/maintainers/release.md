# リリース手順

## 1. リリース候補を確定する

通常は、対象バージョンの統合線`develop/vX.Y.Z`をリリース候補とします。ブランチ名に含まれる版と、次の版情報を一致させます。

- `VERSION`
- `src/manifest.json`
- `pyproject.toml`
- `CHANGELOG.md`

版を決める目安は次のとおりです。

- major: 中核原則、発動条件、評価構造に関わる非互換変更
- minor: 後方互換性のある規則、モジュール、言語、アダプターの追加
- patch: 誤記、明確化、翻訳修正、配布・ビルド修正

安定化のための修正を通常開発から分けたい場合に限り、`develop/vX.Y.Z`から`release/vX.Y.Z`を切ります。release branchでは、リリース成立に必要な修正、文書、版情報の整理に範囲を絞り、新しい方法論機能は原則として追加しません。

release branchを使わない場合は、`develop/vX.Y.Z`をそのまま`main`へのリリース候補にできます。

## 2. `main`との差分を確認する

リリース候補を作った後に`main`が進んでいる場合は、`main`の変更を先にリリース候補へ取り込みます。リリース時だけ古い`main`へ戻したり、両者の差分を暗黙に捨てたりしません。

少なくとも次を確認します。

```bash
git fetch origin
git log --oneline --left-right origin/main...HEAD
```

`main`にだけ存在する変更がある場合は、その内容を確認してリリース候補へ統合し、検査をやり直します。

## 3. 翻訳状態を確認する

`i18n/translation-manifest.json`を確認します。日本語正本を変更した後、英語版が参照する翻訳元ハッシュが古いままだと、リリース検証は失敗します。

公開前には、`CHANGELOG.md`の`Unreleased`を対象バージョンの節へ整理し、実際に含まれる変更内容と一致させます。

## 4. 検査とパッケージ作成を行う

リリース候補上で次を実行します。

```bash
make release-check
```

少なくとも次を確認します。

- `dist/reports/validation-report.json`
- `dist/reports/token-budget.json`
- `dist/release-manifest.json`
- `dist/packages/`の言語別ZIP

リリース候補のCIも成功していることを確認します。

## 5. PRで`main`へ統合する

方法論やリリース内容を`main`へ直接コミットしません。

- release branchを使う場合: `release/vX.Y.Z` → `main`
- 使わない場合: `develop/vX.Y.Z` → `main`

のPRを作ります。

PRでは、累積差分、版情報、CHANGELOG、翻訳状態、`make release-check`の結果を確認します。修正が必要な場合はリリース候補側へ入れ、CIを再実行します。

PRをmergeした後は、`main`のmerge commitが公開版の正本になります。

## 6. `main`のmerge commitへタグを付ける

`main`へ統合されたcommitを確認してから、そのcommitへタグを付けます。タグの版は`VERSION`と一致させます。

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
git tag vX.Y.Z
git push origin vX.Y.Z
```

タグをpushすると、GitHub Actionsが全言語を検査し、言語・プラットフォーム別のZIPをReleaseへ添付します。

公開済みタグの内容を後から無言で差し替えません。修正が必要な場合はpatch版を作ります。

## 7. 次の開発線を始める

リリース後の新しい`develop/vA.B.C`は、タグを付けた最新の`main`から切ります。release branchにだけ入った修正を、後続のdevelopから欠落させないためです。

緊急修正は`hotfix/vX.Y.Z`を`main`から切り、公開後は必要に応じて進行中のdevelopにも戻します。

## 8. 各プラットフォームでの公開を確認する

- Claude Code: Marketplaceの版をタグと一致させる。
- ChatGPT GPTs: 言語別の更新パックをGPTエディターへ手動で反映する。
- Microsoft 365 Copilot: stagingで検証した後、管理者承認を経て本番公開する。

公開済みタグの翻訳を後から無言で差し替えません。翻訳修正もpatch版として公開します。
