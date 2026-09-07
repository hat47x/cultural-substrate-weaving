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
- regression: `tests/test_research_translation_refresh_state.py`

The JSON contract is the machine-readable source for the **current pending refresh scope**. It declares the exact six files expected to be stale, required English semantic markers, the canonical refresh command, and the non-promotion boundary.

The validator computes current Japanese SHA-256 values itself. While status is pending it requires:

1. the actual stale set to equal the declared six-file scope;
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

Run, in order:

```text
make update-en-hashes
make research-skill-check
make build
make check
```

Then inspect the translation-manifest diff and generated-artifact diff.

After the refresh has been reviewed, change the JSON state to `synchronized`, clear `expected_stale_files`, and update/remove tension-specific marker requirements only through an explicit state transition. Do not rewrite this historical explanation to imply the hashes were already synchronized during the current research step.

The translation manifest should be considered **stale for the files above until the command is run**. This is not evidence that the English text is absent; it means the byte-level source tracking has not yet been refreshed.

## Promotion boundary

This record does not authorize production promotion. A stale translation hash must not be represented as translated-and-validated merely because bilingual prose was edited in the same session.
