## Summary

## Change class / target

- [ ] Runtime method (`src/<locale>/`)
- [ ] Translation / documentation / adapter
- [ ] Research / evaluation only
- [ ] Repository validation / release maintenance
- [ ] `feature/*`, `research/*`, or `fix/*` targets the active `develop/vX.Y.Z`; `release/vX.Y.Z` targets `main`
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
- [ ] Platform-specific behavior reviewed when adapters changed

## Japanese development-document prose

- [ ] If scoped Japanese public-guide, development, maintainer, research, experiment, or operational prose changed, the factual/technical content was settled first and then the whole document received a separate natural-Japanese rewriting pass
- [ ] Required identifiers, schema fields, commands, numeric results, and evidence boundaries were preserved while awkward literal translation, noun stacking, particles, and sentence flow were reviewed
- [ ] Each changed scoped Japanese document was recorded in `natural-japanese-review-manifest.json` only after that full-document pass

## Checks

- [ ] `make check` was run when local execution was available; otherwise the PR body states which contracts were checked and which remain unverified
- [ ] On a versioned develop/release branch, the local repository-contract check was not bypassed
- [ ] `make main-contract`, when applicable, is treated as a two-parent commit-shape diagnostic rather than proof of pull-request provenance
- [ ] For a public release, packaging is run from a clean Git worktree with no tracked uncommitted changes or non-ignored untracked files
- [ ] For a public release, the tag is derived from `VERSION` and `make release-tag-contract TAG="$TAG"` is run against the final release manifest before tagging
- [ ] For a public release, the final manifest `source_commit` matches the package-producing `HEAD`, and `make release-remote-tag-contract TAG="$TAG"` verifies the pushed remote tag resolves to that commit
- [ ] Absence of a remote GitHub Actions status or GitHub branch protection is not treated as evidence that local validation ran
- [ ] Semantic-retention impact reviewed when runtime meaning changed
- [ ] Changelog updated for user-visible or operational behavior
- [ ] Token-size changes reviewed when runtime/reference content changed
