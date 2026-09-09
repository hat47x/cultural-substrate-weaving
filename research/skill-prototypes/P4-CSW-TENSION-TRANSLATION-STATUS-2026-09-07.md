# P4 CSW Tension / Emergence Translation Status — 2026-09-07

Status: bilingual semantic edit applied; translation-manifest hash refresh pending

## Scope

The target/framework tension and cross-field emergence update changed these canonical Japanese files and their English counterparts on the research branch:

- `src/ja-JP/ROUTER.md` / `src/en-US/ROUTER.md`
- `src/ja-JP/core/cognitive-stance.md` / `src/en-US/core/cognitive-stance.md`
- `src/ja-JP/core/principles-and-constraints.md` / `src/en-US/core/principles-and-constraints.md`
- `src/ja-JP/methods/transformation.md` / `src/en-US/methods/transformation.md`
- `src/ja-JP/methods/integration.md` / `src/en-US/methods/integration.md`
- `src/ja-JP/governance/evaluation.md` / `src/en-US/governance/evaluation.md`

The English files were edited in the same work sequence to preserve the same method boundary:

- cultural-framework fit is not privileged over informative misfit;
- target/framework tension may generate `cross_field_emergent` candidates;
- sublation is not a fixed thesis-antithesis-synthesis runtime stage model;
- a third structure remains non-factual until independently supported on the target side;
- the generating tension is preserved when handing material to Layer 1;
- Layer 1 does not acquire CSW-specific dialectical ownership;
- evaluation does not reward correspondence count or force a third structure when tension remains unresolved.

## Snapshot re-review — 2026-09-09

A later author-decision-authority refactor changed two bilingual pairs after the original semantic-review snapshot:

- `src/ja-JP/ROUTER.md` / `src/en-US/ROUTER.md`
- `src/ja-JP/core/principles-and-constraints.md` / `src/en-US/core/principles-and-constraints.md`

Both current Japanese/English pairs were re-read semantically rather than accepting a hash-only refresh. The revised texts remain aligned on these boundaries:

- values, usage scope, loading depth, stopping, adoption, publication, and action are not independently decided by the skill;
- author decisions and explicit delegation outside the skill remain the authority for those judgments;
- provenance and state labels remain information surfaces rather than automatic action permissions;
- informative misfit, resistance, and cross-field emergence remain available as cognitive material;
- `cross_field_emergent` still does not declare contradiction resolved, and third structures are not promoted to target-side fact without independent support.

The other four files in `scope_files` still match their previously reviewed Japanese source blobs. Accordingly, `reviewed_source_blobs` is advanced only for the two re-reviewed Japanese files:

- `ROUTER.md`: `14c0a772591a566d473379b29117e821207d3952`
- `core/principles-and-constraints.md`: `c8d5e31c2208d21d3bc54bc4c9fc851099b524d4`

The author-decision-authority integration had already refreshed the translation-manifest entries for these two bilingual pairs. They are therefore no longer part of the pending stale set. The remaining pending refresh covers four files: `core/cognitive-stance.md`, `governance/evaluation.md`, `methods/integration.md`, and `methods/transformation.md`. This partial synchronization does not authorize production promotion.

## Machine-readable state contract

The explanatory record in this file is paired with:

- `research/skill-prototypes/P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.json`
- validator: `scripts/validate_research_translation_refresh_state.py`
- state-transition helper: `scripts/mark_research_translation_refresh_synchronized.py`
- regressions: `tests/test_research_translation_refresh_state.py` and `tests/test_research_translation_refresh_transition.py`

The JSON contract separates two concepts:

- `scope_files`: the six bilingual files changed by this semantic edit; this remains as history after synchronization;
- `expected_stale_files`: the subset of `scope_files` whose current Japanese bytes are not yet reflected in `translation-manifest.json`; this may shrink during a pending partial refresh and becomes empty only through the explicit synchronization transition after all entries are current.

English semantic markers remain attached to `scope_files`, including after individual manifest entries or the whole scope are synchronized. Refresh progress therefore does not erase what semantic boundary was reviewed.

While status is pending, the validator requires:

1. the actual stale set to equal `expected_stale_files`, which remains a nonempty subset of `scope_files` until the explicit synchronization transition;
2. no translation-manifest entry outside `expected_stale_files` to have unexpected source-hash drift;
3. every declared English counterpart to exist;
4. the English tension/emergence markers to be present across the full semantic-review scope;
5. the normal refresh command to remain `make update-en-hashes`.

This allows the research gate to distinguish **explicitly pending translation tracking** from an unnoticed translation regression while also tolerating legitimate partial synchronization of already reviewed pairs.

## Why hashes are not updated in this record

`i18n/translation-manifest.json` stores SHA-256 values computed from canonical Japanese bytes. The remaining four stale entries have not been refreshed through the normal repository command in a complete checkout:

```text
make update-en-hashes
```

Do not guess or hand-enter replacement hashes merely to make the manifest look current.

The existing `update_translation_hashes.py` command records that the English translation has been reviewed/updated against the current Japanese source. Therefore a hash refresh should follow review of the bilingual semantic edit rather than being used to hide a stale review state.

## Required follow-up in a complete checkout

Run the transition explicitly:

```text
make update-en-hashes
# inspect the translation-manifest diff and confirm the bilingual semantic edit
python scripts/mark_research_translation_refresh_synchronized.py
make research-skill-check
make build
make check
```

The synchronization helper refuses to change state unless all tracked Japanese/source hashes are already synchronized and every declared English tension marker remains present. It changes only the research status JSON; it does not write translation hashes.

After that transition, `scope_files` and `english_markers` remain, while `expected_stale_files` becomes empty. Do not rewrite this historical explanation to imply that the remaining hashes were synchronized before the complete-checkout refresh actually occurred.

The translation manifest should be considered **stale only for the files currently named in `expected_stale_files` until the refresh and state transition are performed**. This is not evidence that the English text is absent; it means byte-level source tracking for those remaining files has not yet been refreshed and acknowledged by the research state machine.

## Promotion boundary

This record does not authorize production promotion. A stale translation hash must not be represented as translated-and-validated merely because bilingual prose was edited in the same session.
