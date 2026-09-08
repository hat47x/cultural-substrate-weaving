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

## Machine-readable state contract

The explanatory record in this file is paired with:

- `research/skill-prototypes/P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.json`
- validator: `scripts/validate_research_translation_refresh_state.py`
- state-transition helper: `scripts/mark_research_translation_refresh_synchronized.py`
- regressions: `tests/test_research_translation_refresh_state.py` and `tests/test_research_translation_refresh_transition.py`

The JSON contract separates two concepts:

- `scope_files`: the six bilingual files changed by this semantic edit; this remains as history after synchronization;
- `expected_stale_files`: files whose current Japanese bytes are intentionally not yet reflected in `translation-manifest.json`; this becomes empty after synchronization.

English semantic markers remain attached to `scope_files`, including after hash synchronization. The state transition therefore does not erase what semantic boundary was reviewed.

While status is pending, the validator requires:

1. the actual stale set to equal the complete six-file scope;
2. no other translation-manifest entry to have unexpected source-hash drift;
3. every declared English counterpart to exist;
4. the English tension/emergence markers to be present;
5. the normal refresh command to remain `make update-en-hashes`.

This allows the research gate to distinguish **explicitly pending translation tracking** from an unnoticed translation regression.

## Why hashes are not updated in this record

`i18n/translation-manifest.json` stores SHA-256 values computed from canonical Japanese bytes. The current connected execution environment is unavailable, so the normal repository command has not been run:

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

After that transition, `scope_files` and `english_markers` remain, while `expected_stale_files` becomes empty. Do not rewrite this historical explanation to imply the hashes were already synchronized during the current research step.

The translation manifest should be considered **stale for the files above until the refresh and state transition are performed**. This is not evidence that the English text is absent; it means the byte-level source tracking has not yet been refreshed and acknowledged by the research state machine.

## Promotion boundary

This record does not authorize production promotion. A stale translation hash must not be represented as translated-and-validated merely because bilingual prose was edited in the same session.
