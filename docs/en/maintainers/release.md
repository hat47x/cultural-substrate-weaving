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

Before publication, move the relevant `Unreleased` changes in `CHANGELOG.md` into exactly one dated release section:

```text
## X.Y.Z — YYYY-MM-DD
```

Keep a new `## Unreleased` section for later development, and verify that the dated section matches the changes that will actually be published.

Check the publication boundary explicitly:

```bash
python scripts/check_release_changelog.py \
  --version "$(cat VERSION)"
```

Do not proceed to publication if this check fails. Successful packaging alone must not turn an unfrozen changelog into a public release.

## 4. Validate the release candidate

Run on the release candidate:

```bash
make release-check
```

Review at least:

- `dist/reports/validation-report.json`
- `dist/reports/token-budget.json`
- `dist/release-manifest.json`
- locale-specific ZIP packages under `dist/packages/`

`make release-check` includes `make check`. On `develop/vX.Y.Z` or `release/vX.Y.Z`, that check also verifies that the branch version agrees with `VERSION`.

The final `release-manifest.json` uses schema 2 and records the Git commit that produced the package set in `source_commit`. `release-validate` also requires that `source_commit` to equal the current `HEAD`, so later remote-tag checks can return to the exact package provenance.

GitHub Actions are currently disabled. `main` also has no branch protection or repository ruleset configured at present. Neither an absent remote status nor an accepted push is evidence that the local validation gates succeeded.

Do not proceed with a public release from an environment where `make release-check` cannot be run. Unlike an ordinary pull request where local execution may occasionally be unavailable, publication requires an environment that can generate and validate the actual release packages.

## 5. Merge to `main` through a pull request

Do not commit method or release content directly to `main`.

- with a release branch: `release/vX.Y.Z` → `main`
- without one: `develop/vX.Y.Z` → `main`

Review the cumulative diff, version metadata, changelog, translation status, and `make release-check` result in the pull request. Put any necessary fixes back on the release candidate and rerun the checks.

When merging to `main`, choose the normal merge-commit method rather than squash or rebase merging, so the resulting commit has exactly two parents. After the pull request merges, that merge commit on `main` is the canonical public release commit.

This pull-request policy is not currently enforced by GitHub branch protection or a repository ruleset. Keep the repository policy distinct from the protections that GitHub is actually configured to enforce.

## 6. Revalidate the public commit and tag it

Even when the release candidate was already checked, the tag is placed on the commit that actually landed on `main`. Run the release gates again on that exact commit so the published artifacts are known to come from the tagged content.

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
make main-contract
make release-check
git merge-base --is-ancestor HEAD origin/main
TAG="v$(cat VERSION)"
make release-tag-contract TAG="$TAG"
```

Verify each gate separately:

- `make main-contract`: the current branch is `main` and HEAD has exactly two parents, matching the repository's expected merge-commit shape.
- `make release-check`: the generated release set and release contract are valid on that commit, and the final manifest `source_commit` records that HEAD.
- `git merge-base --is-ancestor`: the current commit is actually part of `origin/main` history.
- `make release-tag-contract`: the tag derived from `VERSION`, `VERSION` itself, and the final `release-manifest.json` version agree.

`make main-contract` checks commit shape only. Two parents do not prove that GitHub created the commit from a pull request, and the command does not prevent a direct push at GitHub. If any gate fails, do not create the tag. Fix the cause on the appropriate development line and merge the corrected release candidate again.

After the checks pass, create the already validated `TAG` on that commit. Do not type the tag version again separately.

```bash
git tag "$TAG"
git push origin "$TAG"
make release-remote-tag-contract TAG="$TAG"
```

`release-remote-tag-contract` fetches the remote tag, peels either a lightweight or annotated tag to its commit, and requires that commit to equal the final manifest `source_commit`.

Do not silently replace files under an existing public tag. Publish a patch version when a released artifact needs correction.

## 7. Publish the GitHub Release assets

GitHub Actions do not currently publish releases automatically. After pushing the tag, manually publish the files listed in `dist/release-manifest.json` under `release_assets` to the GitHub Release for the same tag. Use the artifacts generated by the immediately preceding `make release-check` on the tagged `main` commit.

You may upload the files through the GitHub web interface. With GitHub CLI, for example:

```bash
TAG="v$(cat VERSION)"
make release-tag-contract TAG="$TAG"
make release-remote-tag-contract TAG="$TAG"

mapfile -t ASSETS < <(
  python - <<'PY'
import json
from pathlib import Path

manifest = json.loads(Path("dist/release-manifest.json").read_text(encoding="utf-8"))
for relative in manifest["release_assets"]:
    print((Path("dist") / relative).as_posix())
PY
)

gh release create "$TAG" "${ASSETS[@]}" \
  --verify-tag \
  --generate-notes \
  --notes "$(cat .github/release-validation-note.md)"
```

Do not use an existing release as a way to silently replace already published artifacts. Ship a patch release when published contents need correction.

## 8. Verify the published Release

After publication, verify both that the remote tag still resolves to the manifest `source_commit` and that the GitHub Release matches the final manifest. Example using GitHub CLI:

```bash
TAG="v$(cat VERSION)"
mkdir -p .tmp

make release-remote-tag-contract TAG="$TAG"

gh api "repos/hat47x/cultural-substrate-weaving/releases/tags/${TAG}" \
  > .tmp/published-release.json

python scripts/verify_published_release.py \
  --manifest dist/release-manifest.json \
  --release-json .tmp/published-release.json \
  --tag "$TAG"
```

These are separate boundaries. `release-remote-tag-contract` verifies that the remote tag resolves to the manifest `source_commit`; `verify_published_release.py` rechecks the manifest version and tag, then verifies the published asset names, sizes, and digests. Neither check substitutes for the other.

## 9. Start the next development line

Create the next `develop/vA.B.C` from the newly released `main`. This prevents release-only fixes from disappearing from later development.

For urgent released-version fixes, branch `hotfix/vX.Y.Z` from `main` and reconcile the fix back into any active develop line when applicable.

## 10. Platform follow-up

- Claude Marketplace updates from the tagged repository.
- Custom GPTs are updated manually using the locale-specific update pack.
- Microsoft 365 production publication requires tenant approval after staging validation.

Translation corrections also change public artifacts and therefore ship as a patch release rather than replacing an existing tag.
