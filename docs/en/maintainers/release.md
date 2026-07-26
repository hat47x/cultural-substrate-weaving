# Release procedure

## 1. Choose a version

Update `VERSION`, `src/manifest.json`, and `CHANGELOG.md`.

- major: incompatible change to core principle, activation, or evaluation structure;
- minor: backward-compatible rule, module, locale, or adapter addition;
- patch: clarification, packaging, translation correction, or build fix.

## 2. Check translation status

Review `i18n/translation-manifest.json`. A stale translation blocks release by default.

## 3. Run checks

```bash
make release-check
```

Review reports and language-specific packages under `dist/`.

## 4. Commit and tag

```bash
git add .
git commit -m "release: vX.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

The release workflow attaches all locale-specific packages.

## 5. Platform follow-up

- Claude Marketplace updates from the tagged repository.
- Custom GPTs are updated manually using the locale-specific update pack.
- Microsoft 365 production publication requires tenant approval after staging validation.
