# CSW thin Japanese canonical — post-apply audit

Date: 2026-09-06
Status: source migration applied on research branch
Branch: `research/kj-skill-delegation-v0.5`

## Applied changes

Japanese canonical source has been changed in-place:

- `src/ja-JP/ROUTER.md`
- `src/ja-JP/methods/integration.md`
- `src/ja-JP/core/iteration.md`
- `src/manifest.json` ja-JP capability description / en-US parity note

The old monolithic KJ / multi-round implementation is no longer owned by the Japanese CSW runtime source.

Current ownership:

```text
Cultural Substrate Weaving
  owns:
    cultural-framework exploration
    framework depth / native-operation contact
    attribution and target return
    framework-contact handoff

Affinity Synthesis
  owns:
    one-round material-led integration
    card / group / label / relation / narrative
    source-return and transformation audit
    representation / lineage

Iterative Inquiry Synthesis
  owns:
    multi-round delta / reopen
    stable semantic handles
    question / structural delta
    append-only history
    stop / restart / handoff
```

## Comparison range

Compared branch state:

- base: `775b26baed6303a6f3b4f857362c27b604904cdb`
- applied head at audit time: `48ffec269619c89714a2d9c91e8933c44d8cef48`

Result:

- ahead by 12 commits
- no unrelated file changes observed in the compare result

Changed files in the migration range:

1. `research/skill-prototypes/affinity-synthesis/evidence/KJ-LINEAGE-CARRYOVER.md`
2. `research/skill-prototypes/evals/THREE-LAYER-PAIRED-RUN-2026-09-06.md`
3. `research/skill-prototypes/migration/CSW-THIN-MIGRATION-AUDIT-2026-09-06.md`
4. `research/skill-prototypes/migration/CSW-THIN-SOURCE-RETENTION-CHECK-2026-09-06.md`
5. `research/skill-prototypes/migration/thin-csw-integration-candidate.md`
6. `research/skill-prototypes/migration/thin-csw-iteration-candidate.md`
7. `research/skill-prototypes/migration/thin-csw-router-candidate.md`
8. `research/skill-prototypes/suite-manifest.json`
9. `src/ja-JP/ROUTER.md`
10. `src/ja-JP/core/iteration.md`
11. `src/ja-JP/methods/integration.md`
12. `src/manifest.json`

## Gates now passed

- [x] Layer 1 Method Definition exists.
- [x] Layer 1 representation / hierarchy / lineage regression exists.
- [x] 114-card synthetic scale regression exists.
- [x] Layer 2 Method Definition exists.
- [x] Layer 2 delta-reopen eval cases exist.
- [x] CSW cross-layer handoff cases exist.
- [x] analysis / creative real-material Layer-1 paired comparison exists.
- [x] three-layer paired comparison exists.
- [x] source-to-thin semantic-retention audit passed.
- [x] ROUTER ownership mismatch identified and corrected.
- [x] Japanese canonical integration / iteration / router thin replacement applied.
- [x] ja-JP manifest capability description aligned.
- [x] KJ legacy source / trademark detail carried into Layer-1 migration evidence.

## Gates still open

### 1. Generated artifacts have not been rebuilt

The repository build copies / concatenates canonical source into multiple generated surfaces. This connector session does not have a checked-out repository execution environment, so the build has not been run after the source replacement.

Do not manually patch every generated artifact as a substitute for the build.

Required in a checkout or CI-capable environment:

```text
make research-skill-check
make build
python scripts/check_generated_artifacts.py
python scripts/validate.py
python -m unittest discover -s tests
```

Then inspect generated Japanese OpenAI / Claude / Codex / GPT / M365 surfaces for stale monolithic ownership wording.

### 2. English realization is intentionally not migrated yet

`src/en-US` remains the pre-split monolithic realization on this research branch.

`src/manifest.json` now records this as a parity backlog in `review_note`.

Do not claim ja/en semantic parity until the English thin translation and review are complete.

### 3. Generated knowledge-group filename is historically named

`src/manifest.json` still uses:

```text
01-framework-and-kj.md
```

for one generated knowledge group.

This is structurally harmless for the first in-place migration because file membership paths remain valid, but the name becomes conceptually stale after CSW stops owning KJ integration.

Do not rename it casually before checking downstream references and generated-artifact tests. Treat it as a packaging cleanup candidate.

### 4. External-compatible Skill conformance remains open

The thin CSW says `compatible realization`, not merely a Skill with a similar name.

Future work must define or operationalize how compatibility with the Layer-1 / Layer-2 Method Definition is asserted without creating a hard dependency or a brittle registry.

## Regression watch after build

After generated artifacts are rebuilt, inspect especially:

- Router still must not say CSW itself owns KJ grouping / labeling.
- `10-integration.md` generated reference should contain the thin connection, not the former monolithic KJ procedure.
- `00-iteration.md` generated reference should contain framework-delta handoff, not general multi-round orchestration.
- cultural-framework candidates must remain attributed across composite surfaces.
- absence of Layer 1 / Layer 2 must not be hidden by platform-specific prompt text.
- current target attention should not become dominated by provenance metadata.

## Current decision

**Japanese source migration: applied and semantically acceptable for continued research.**

**Repository / release migration: not yet complete.**

The next engineering step is generated-artifact rebuild and repository validation in an execution environment, followed by Japanese composite-runtime inspection. English migration should follow only after the Japanese split behavior remains stable.
