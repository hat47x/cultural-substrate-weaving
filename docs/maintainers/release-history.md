# Release history notes

This file records publication-boundary facts that are not fully expressible by version headings alone.

## v0.4.0

Status: **published Git tag and GitHub Release.**

- Published tag: `v0.4.0`
- Tagged commit: `eb31af5bb934934315b03d95c2d30980b6bb36ff`
- Release PR: #62
- GitHub Release: `https://github.com/hat47x/cultural-substrate-weaving/releases/tag/v0.4.0`
- Release workflow run #7 completed successfully through the final remote asset verification step.
- Published set: 12 locale × platform package ZIPs, 3 validation/research reports, and `release-manifest.json`.
- Final manifest: 34,981 bytes; SHA-256 `6cddeb03f3f4ecae078417d1c08250f8196880c11597f1b86e7e626c2601d14e`.
- The published Release retains the bilingual validation-stage disclosure: technical release success does not establish method effectiveness.

The annotated tag resolves to the validated `main` commit above. The release workflow re-ran `make release-check`, verified tag/version, `main` ancestry, the dated changelog boundary, and the final remote asset set/state/size/SHA-256 values before completion.

## v0.3.0

Status: **validated and merged to `main`, but never published as a Git tag or GitHub Release; superseded by the v0.4.0 release line.**

- Frozen validated commit: `94308c359b69624e1c5fffa0f240f9aa1d2afe59`
- Release-candidate merge: PR #14
- `VERSION` at the frozen commit: `0.3.0`
- Validation and release-package checks completed successfully before and after the merge to `main`.
- No `v0.3.0` tag was created.
- No GitHub Release `v0.3.0` was published.

The `## 0.3.0 — 2026-08-30` changelog section therefore records the validated version boundary and its accumulated changes, not a claim that a public GitHub Release existed on that date.

The project deliberately does not backfill the missing v0.3.0 publication now. The historical v0.3.0 workflow predates the stricter v0.4.0 publication boundary, including manifest-driven publication, existing-tag verification, validation-stage disclosure, `main` ancestry checks, publication-time changelog checks, and remote post-publication asset verification. Publishing the old commit now would execute that historical workflow rather than retroactively inheriting the current release safeguards.

The next intended public release after v0.2.0 is therefore v0.4.0. The v0.3.0 commit remains part of repository history as a validated intermediate boundary and must not be retagged or rewritten to include later v0.4.0 work.

## Interpretation

A version may have three distinct states in this repository:

1. **development version** — active work exists under a versioned development line;
2. **validated version boundary** — a candidate has been technically validated and may have reached `main`;
3. **published release** — the corresponding Git tag and GitHub Release actually exist and the publication workflow has completed.

Do not infer state 3 from state 2. Changelog headings, validated commits, or a `VERSION` value alone are not evidence that a GitHub Release was published.
