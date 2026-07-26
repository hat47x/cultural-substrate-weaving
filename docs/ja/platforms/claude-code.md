# Claude Codeで使う

このGitHubリポジトリはClaude Plugin Marketplaceとして利用できます。

## インストール

Claude Code内で実行します。`OWNER`は実際のGitHubユーザーまたは組織名へ置き換えてください。

```text
/plugin marketplace add OWNER/cultural-substrate-weaving
/plugin install csw-method-ja@cultural-substrate-weaving
/reload-plugins
```

CLIから追加する場合:

```bash
claude plugin marketplace add OWNER/cultural-substrate-weaving
```

## 呼び出し

```text
/csw-method-ja:cultural-substrate-weaving-ja このアーキテクチャの責任境界を検査してください。
```

明示呼び出しを標準にしているため、不要なトークン消費を抑えられます。

## 更新

```text
/plugin marketplace update cultural-substrate-weaving
```

バージョンが更新された後、必要に応じてプラグインを更新し、`/reload-plugins`を実行します。
