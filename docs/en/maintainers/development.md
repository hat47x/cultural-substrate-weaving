# Development

## Edit locations

- Canonical method: `src/ja-JP/`.
- Translations: `src/<locale>/`.
- Translation tracking: `i18n/`.
- Platform wording and configuration: `adapters/`.
- Test cases: `evals/`.
- Generation logic: `scripts/`.

Do not edit `dist/` directly. `plugins/` is generated and committed for Claude Marketplace delivery.

## Cycle

Use the integrated check for normal pre-PR validation:

```bash
make check
```

It currently runs build, validation, Japanese-document review checks, unit tests, token-budget checks, Living Lab validation, and Living Lab summary generation. Individual Make targets may be used while diagnosing a narrower problem.

GitHub Actions are currently disabled in this repository. The absence of a remote status is not evidence that validation ran. If the current environment cannot run `make check`, state in the pull request which contracts were checked and which remain unverified.

A public release is stricter: use an environment that can run `make release-check` on both the release candidate and the exact `main` commit that will be tagged. See `release.md`.

When the canonical source changes, update translations and run:

```bash
python scripts/update_translation_hashes.py --locale en-US
make check
```

Run the hash-update command only after reviewing the translation against the new canonical content.
