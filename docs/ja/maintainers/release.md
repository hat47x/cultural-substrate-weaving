# リリース手順

## 1. 版を決める

`VERSION`、`src/manifest.json`、`CHANGELOG.md`を更新します。

- major: 中核原則、発動条件、評価構造の非互換変更
- minor: 後方互換の規則、モジュール、言語、アダプター追加
- patch: 誤記、明確化、翻訳修正、配布・ビルド修正

## 2. 翻訳状態を確認する

`i18n/translation-manifest.json`を確認します。正本変更後に英語版の翻訳元ハッシュが古い場合、リリース検証は失敗します。

## 3. 検査とパッケージ作成

```bash
make release-check
```

確認するもの:

- `dist/reports/validation-report.json`
- `dist/reports/token-budget.json`
- `dist/release-manifest.json`
- `dist/packages/`の言語別ZIP

## 4. コミットとタグ

```bash
git add .
git commit -m "release: vX.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

タグをpushすると、GitHub Actionsが全言語を検査し、言語・プラットフォーム別ZIPをReleaseへ添付します。

## 5. 各プラットフォーム

- Claude Code: Marketplaceの版をタグと一致させる
- ChatGPT GPTs: 言語別更新パックをGPTエディターへ手動反映する
- Microsoft 365 Copilot: staging検証後、管理者承認を経て本番公開する

公開済みタグの翻訳を無言で差し替えず、翻訳修正もパッチ版として公開します。
