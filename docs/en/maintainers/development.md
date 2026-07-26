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

```bash
make build
make validate
make test
make tokens
```

`make check` runs all checks.

When the canonical source changes, update translations and run:

```bash
python scripts/update_translation_hashes.py --locale en-US
```

Run that command only after reviewing the translation against the new canonical content.
