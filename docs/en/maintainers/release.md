# Release procedure

## 1. Finalize the release candidate

Normally, the versioned integration line `develop/vX.Y.Z` is the release candidate. Keep the version in the branch name aligned with:

- `VERSION`
- `src/manifest.json`
- `pyproject.toml`
- `CHANGELOG.md`

Version guidance:

- major: incompatible change to core principles, activation, or evaluation structure;
- minor: backward-compatible rule, module, locale, or adapter addition;
- patch: clarification, packaging, translation correction, or build fix.

Create `release/vX.Y.Z` from `develop/vX.Y.Z` only when release-stabilization work should be isolated from normal development. Keep a release branch limited to fixes, documentation, packaging, and version finalization needed to ship; do not normally add new method capabilities there.

When no separate stabilization branch is needed, `develop/vX.Y.Z` itself can be the release candidate for `main`.

## 2. Reconcile with `main`

If `main` advanced after the release candidate was created, bring those changes into the release candidate before release. Do not silently release from an older lineage or discard the divergence at merge time.

At minimum, inspect:

```bash
git fetch origin
git log --oneline --left-right origin/main...HEAD
```

If commits exist only on `main`, review and integrate them into the release candidate, then run the checks again.

## 3. Check translation and changelog state

Review `i18n/translation-manifest.json`. A stale translation blocks release by default.

Before publication, turn the relevant `Unreleased` entries in `CHANGELOG.md` into the section for the version being released and make sure the list matches the actual cumulative diff.

## 4. Run release checks

Run on the release candidate:

```bash
make release-check
```

Review:

- `dist/reports/validation-report.json`
- `dist/reports/token-budget.json`
- `dist/release-manifest.json`
- locale-specific packages under `dist/packages/`

Confirm that CI on the release candidate also succeeds.

## 5. Merge to `main` through a pull request

Do not commit method or release content directly to `main`.

- with a release branch: `release/vX.Y.Z` → `main`
- without one: `develop/vX.Y.Z` → `main`

Review the cumulative diff, version metadata, changelog, translation status, and release-check result in the pull request. Put any necessary fixes back on the release candidate and rerun CI.

After the pull request merges, the merge commit on `main` is the canonical public release commit.

## 6. Tag the merged `main` commit

Only after the release candidate is merged, tag the resulting `main` commit. The tag must match `VERSION`.

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
git tag vX.Y.Z
git push origin vX.Y.Z
```

Pushing the tag runs the release workflow and attaches locale/platform packages to the GitHub Release.

Do not silently replace files under an existing public tag. Publish a patch version when a released artifact needs correction.

## 7. Start the next development line

Create the next `develop/vA.B.C` from the newly released `main`. This prevents release-only fixes from disappearing from later development.

For urgent released-version fixes, branch `hotfix/vX.Y.Z` from `main` and reconcile the fix back into any active develop line when applicable.

## 8. Platform follow-up

- Claude Marketplace updates from the tagged repository.
- Custom GPTs are updated manually using the locale-specific update pack.
- Microsoft 365 production publication requires tenant approval after staging validation.

Translation corrections also change public artifacts and therefore ship as a patch release rather than replacing an existing tag.
