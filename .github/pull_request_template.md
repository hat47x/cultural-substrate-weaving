## Summary

## Change class / target

- [ ] Runtime method (`src/<locale>/`)
- [ ] Translation / documentation / adapter
- [ ] Research / evaluation only
- [ ] Repository validation / release maintenance
- [ ] `feature/*`, `research/*`, or `fix/*` targets the active `develop/vX.Y.Z`; a public release targets `main` from `develop/vX.Y.Z` or, when intentionally used, `release/vX.Y.Z`
- [ ] If this PR targets `main`, it will be merged with the normal merge-commit method rather than squash or rebase merging

## Canonical source impact

If `src/ja-JP/` changes, state the smallest method-level reason for the change and what existing behavior must remain intact.

## Evidence / attribution for runtime changes

If the runtime method changes, identify the observed problem or increment, why it belongs to the two core capabilities rather than a caller/domain/product/model, and the regression case or semantic-retention guard that protects the change. Otherwise write N/A.

## Translation impact

- [ ] Locale trees remain structurally parallel
- [ ] Translation hashes updated after review
- [ ] Terminology checked against `i18n/glossary.yml`

## Platform / generated-artifact impact

- [ ] Generated Claude/Codex plugin artifacts refreshed when build inputs changed
- [ ] After rebuilding, `.claude-plugin/`, `.agents/`, and `plugins/` contain no uncommitted generated drift, including untracked generated files
- [ ] Platform-specific behavior reviewed when adapters changed

## Japanese development-document prose

- [ ] If scoped Japanese public-guide, development, maintainer, research, experiment, or operational prose changed, the factual/technical content was settled first and then the whole document received a separate natural-Japanese rewriting pass
- [ ] Required identifiers, schema fields, commands, numeric results, and evidence boundaries were preserved while awkward literal translation, noun stacking, particles, and sentence flow were reviewed
- [ ] Each changed scoped Japanese document was recorded in `natural-japanese-review-manifest.json` only after that full-document pass

## Checks

- [ ] `make check` was run when local execution was available; otherwise the PR body states which contracts were checked and which remain unverified
- [ ] On a versioned develop/release branch, the local repository-contract check was not bypassed
- [ ] Generated-artifact freshness was not bypassed; when build inputs changed, the generated Git-tracked distribution artifacts were rebuilt and committed
- [ ] `make main-contract`, when applicable, is treated as a two-parent commit-shape diagnostic rather than proof of pull-request provenance
- [ ] For a public release, `CHANGELOG.md` has exactly one empty `## Unreleased` section before a non-empty dated `## X.Y.Z — YYYY-MM-DD` section, and `python scripts/check_release_changelog.py --version "$(cat VERSION)"` was run before the final candidate `make release-check`
- [ ] For a public release, packaging is run from a clean Git worktree with no tracked uncommitted changes or non-ignored untracked files
- [ ] For a public release, the tag is derived from `VERSION` and `make release-tag-contract TAG="$TAG"` reruns the full `release-validate` contract before the tag-specific checks
- [ ] For a public release, the final manifest `source_commit` matches the package-producing `HEAD`, and `make release-remote-tag-contract TAG="$TAG"` revalidates the release set, requires that `source_commit` retain the expected two-parent merge-commit shape and remain in current remote `main` history, rechecks the frozen CHANGELOG boundary for the manifest version, and verifies that the pushed remote tag resolves to that same commit
- [ ] After upload, rerun `make release-remote-tag-contract TAG="$TAG"` to recheck the remote tag against the final manifest, current remote `main` history, expected two-parent merge-commit shape, and frozen CHANGELOG boundary; then `scripts/verify_published_release.py` confirms a non-draft, non-prerelease Release containing `.github/release-validation-note.md` and the exact manifest-declared asset names, sizes, and digests
- [ ] Absence of a remote GitHub Actions status or GitHub branch protection is not treated as evidence that local validation ran
- [ ] Semantic-retention impact reviewed when runtime meaning changed
- [ ] Changelog updated for user-visible or operational behavior
- [ ] Token-size changes reviewed when runtime/reference content changed
