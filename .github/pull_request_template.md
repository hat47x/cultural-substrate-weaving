## Summary

## Change class / target

- [ ] Runtime method (`src/<locale>/`)
- [ ] Translation / documentation / adapter
- [ ] Research / evaluation only
- [ ] CI / release maintenance
- [ ] `feature/*`, `research/*`, or `fix/*` targets the active `develop/vX.Y.Z`; `release/vX.Y.Z` targets `main`

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

- [ ] If Japanese development, maintainer, research, experiment, or operational prose changed, the technical content was settled first and then the whole document received a separate natural-Japanese rewriting pass
- [ ] Required identifiers, schema fields, commands, numeric results, and evidence boundaries were preserved while awkward literal translation, noun stacking, particles, and sentence flow were reviewed

## Checks

- [ ] `make check`
- [ ] Semantic-retention impact reviewed when runtime meaning changed
- [ ] Changelog updated for user-visible or operational behavior
- [ ] Token-size changes reviewed when runtime/reference content changed
