# リリース手順

## 1. リリース候補を確定する

通常は、対象バージョンの統合線 `develop/vX.Y.Z` をリリース候補とします。ブランチ名の版と次を一致させます。

- `VERSION`
- `src/manifest.json`
- `pyproject.toml`
- `CHANGELOG.md`

版の目安:

- major: 中核原則、発動条件、評価構造の非互換変更
- minor: 後方互換の規則、モジュール、言語、アダプター追加
- patch: 誤記、明確化、翻訳修正、配布・ビルド修正

安定化修正を通常開発から分離したい場合だけ、`develop/vX.Y.Z` から `release/vX.Y.Z` を切ります。release branchでは、リリースを成立させるための修正、文書、版情報の整理に範囲を絞り、新しい方法論機能は原則として追加しません。

release branchを使わない場合は、`develop/vX.Y.Z` 自体をそのまま`main`へのリリース候補にできます。

## 2. `main`との差分を確認する

リリース候補を作った後に`main`が進んでいた場合は、`main`の変更をリリース候補へ先に取り込みます。release時だけ古い`main`へ戻したり、両者の差分を暗黙に捨てたりしません。

少なくとも次を確認します。

```bash
git fetch origin
git log --oneline --left-right origin/main...HEAD
```

`main`にだけ存在する変更がある場合は、内容を確認してリリース候補へ統合し、再度検査します。

## 3. 翻訳状態を確認する

`i18n/translation-manifest.json`を確認します。正本変更後に英語版の翻訳元ハッシュが古い場合、リリース検証は失敗します。

公開前には`CHANGELOG.md`の`Unreleased`を対象バージョンの節へ整理し、実際に含まれる変更と一致させます。

## 4. 検査とパッケージ作成

リリース候補上で実行します。

```bash
make release-check
```

確認するもの:

- `dist/reports/validation-report.json`
- `dist/reports/token-budget.json`
- `dist/release-manifest.json`
- `dist/packages/`の言語別ZIP

リリース候補のCIも成功していることを確認します。

## 5. `main`へPRで統合する

方法論やrelease内容を`main`へ直接コミットしません。

- release branchを使う場合: `release/vX.Y.Z` → `main`
- 使わない場合: `develop/vX.Y.Z` → `main`

のPRを作ります。

PRでは、累積差分、版情報、CHANGELOG、翻訳状態、`make release-check`の結果を確認します。必要な修正はリリース候補側へ入れ、CIを再実行します。

PRをmergeした後、`main`のmerge commitが公開版の正本になります。

## 6. `main`のmerge commitへタグを付ける

`main`へ統合されたcommitを確認してから、そのcommitへタグを付けます。タグは`VERSION`と一致させます。

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
git tag vX.Y.Z
git push origin vX.Y.Z
```

タグをpushすると、GitHub Actionsが全言語を検査し、言語・プラットフォーム別ZIPをReleaseへ添付します。

公開済みタグの内容を後から無言で差し替えません。修正が必要ならpatch版を作ります。

## 7. 次の開発線を開始する

リリース後の新しい`develop/vA.B.C`は、タグを付けた最新`main`から切ります。release branchでのみ入れた修正を、後続のdevelopから欠落させないためです。

緊急修正は`hotfix/vX.Y.Z`を`main`から切り、公開後は必要に応じて進行中のdevelopにも戻します。

## 8. 各プラットフォーム

- Claude Code: Marketplaceの版をタグと一致させる
- ChatGPT GPTs: 言語別更新パックをGPTエディターへ手動反映する
- Microsoft 365 Copilot: staging検証後、管理者承認を経て本番公開する

公開済みタグの翻訳を無言で差し替えず、翻訳修正もpatch版として公開します。
