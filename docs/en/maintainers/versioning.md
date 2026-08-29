# Versioning

The method and every adapter use the same base version. Locale-specific packages include the locale in their filename, not a separate semantic version.

The `X.Y.Z` in `develop/vX.Y.Z` is the **intended release version** for that development line. During development, `VERSION`, `src/manifest.json`, and `pyproject.toml` may already carry that intended version; it becomes a published repository version only after the candidate is merged to `main` and the resulting commit is tagged `vX.Y.Z`.

If the intended release version changes before publication, rename or replace the develop/release line and update the version metadata together rather than leaving ambiguous version state.

A translation correction changes a public artifact and therefore increments at least the patch version. Do not silently replace a released translation under the same tag.
