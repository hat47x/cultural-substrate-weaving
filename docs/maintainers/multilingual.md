# Multilingual maintenance

## Canonical and translated sources

- `src/ja-JP/` is the semantic canonical source.
- Every supported locale has the same relative Markdown file paths.
- `i18n/translation-manifest.json` records the canonical source hash used by each translation.

## Canonical change workflow

1. Edit the Japanese canonical file.
2. Update the corresponding translated file.
3. Check terminology against `i18n/glossary.yml`.
4. Review conditions, exceptions, and stopping rules -- not only wording.
5. Run `python scripts/update_translation_hashes.py --locale en-US`.
6. Run `make check`.

The hash command marks the translation as reviewed against the current canonical source. Do not run it before reviewing the translation.

## Adding another locale

1. Add locale metadata to `src/manifest.json`.
2. Copy the canonical relative file structure under `src/<locale>/`.
3. Add locale-specific adapter templates.
4. Add semantic-retention phrases and activation cases.
5. Extend token budgets and tests.
6. Generate locale-specific release packages.
