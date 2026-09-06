# CSW thin source-to-candidate semantic retention check

Date: 2026-09-06
Status: research audit

## Scope

Compare current Japanese canonical sources:

- `src/ja-JP/ROUTER.md`
- `src/ja-JP/methods/integration.md`
- `src/ja-JP/core/iteration.md`

against thin candidates:

- `research/skill-prototypes/migration/thin-csw-router-candidate.md`
- `research/skill-prototypes/migration/thin-csw-integration-candidate.md`
- `research/skill-prototypes/migration/thin-csw-iteration-candidate.md`

The purpose is not textual preservation. It is to verify that every behavior still needed by CSW remains either:

1. in thin CSW,
2. in Layer 1 (`affinity-synthesis`),
3. in Layer 2 (`iterative-inquiry-synthesis`), or
4. in an explicit evidence / governance artifact.

## Retention matrix

| Current behavior / knowledge | Thin CSW | Layer 1 | Layer 2 | Evidence / other | Status |
|---|---:|---:|---:|---:|---|
| target can correct the analyst's reading | yes | yes | yes | cognitive stance | PASS |
| cultural frameworks are cognitive fields, not answers | yes | n/a | n/a | principles | PASS |
| target-supported vs framework-generated attribution | yes | input status respected | external output status respected | principles | PASS |
| cross-field emergence not backdated to source | yes | inherited/emergent/residual audit | history preserves emergence timing | principles | PASS |
| material-led grouping, not predefined buckets | connection only | yes | n/a | Method Definition | PASS |
| meaning-bearing card boundary | no local implementation | yes | n/a | Layer-1 METHOD | PASS |
| epistemic seam | no local implementation | yes | external status preserved | Layer-1 METHOD | PASS |
| card/group/label integration kernel | no local implementation | yes | n/a | Layer-1 METHOD | PASS |
| singleton/conflict/weak discomfort preservation | no local implementation | yes | reopenable residual | Layer-1 METHOD | PASS |
| source/provenance/discovery/derivation separation | handoff preserves provenance | yes | carry across rounds | Layer-1 representation | PASS |
| derived/reposted material not double-counted | connection forbids authority bonus | yes | preserves realization/material difference | lineage | PASS |
| A-type map / B-type narrative round-trip | no local implementation | yes | representation delta separated | Layer-1 Method | PASS |
| membership/relation/resonance/layout distinction | connection warns against verification leak | yes | semantic vs representation delta | representation grammar | PASS |
| new material is a delta, not restart | framework contact handoff only | n/a | yes | Layer-2 METHOD | PASS |
| reopen only touched artifacts unless global contradiction | connection only | n/a | yes | Layer-2 METHOD | PASS |
| old structure has no immunity | framework reading can weaken/withdraw | one-round resynthesis can change structure | yes | Layer-2 METHOD | PASS |
| question shift versioning | no local implementation | n/a | yes | Layer-2 METHOD | PASS |
| append-only round history | no local implementation | n/a | yes | Layer-2 METHOD | PASS |
| stop with unresolved material | yes for framework exploration | residual is valid | yes | principles | PASS |
| no-useful-increment is valid | yes | n/a | no reopen required | thin iteration | PASS |
| fixed framework count/depth is not completion criterion | yes | n/a | continuation needs reason | activation/principles | PASS |
| framework output does not gain authority inside synthesis | yes | yes | yes across rounds | connection contract | PASS |
| framework interpretation may be refuted by target | yes | target material can remain conflicting | weakened/withdrawn state | principles | PASS |
| missing Layer 1 must not be hidden | yes | n/a | n/a | fallback contract | PASS |
| missing Layer 2 must not be hidden | yes | n/a | n/a | fallback contract | PASS |
| KJ historical lineage / primary-book inventory | removed from runtime | Method has lineage | n/a | KJ-LINEAGE-CARRYOVER + dossier | PASS for migration |
| KJ trademark caution | removed from runtime | not Method invariant | n/a | KJ-LINEAGE-CARRYOVER | PASS for migration; reverify before promotion |
| 04 / nuclear-fusion-related learning | removed from CSW runtime | evidence / realization layer | n/a | dossier | PASS |
| preserve thick history but foreground selectively | yes | provenance retained | local reopen | principles | PASS |
| domain-specific expertise stays outside CSW | yes | yes | yes | router | PASS |
| user / caller retains decision authority | yes | no authority claimed | no authority claimed | principles | PASS |

## Router-specific checks

### R1. Capability ownership wording

Current router says CSW itself combines:

- cultural framework exploration
- KJ-method integration

That becomes inaccurate after split.

Thin router changes this to:

- CSW owns cultural-framework exploration / attribution.
- one-round synthesis may be delegated to a compatible Layer-1 realization.
- multi-round orchestration may be delegated to a compatible Layer-2 realization.

Result: **PASS; ownership statement corrected.**

### R2. Cognitive stance is not lost

The current router foregrounds the stance of remaining revisable by the target. The thin router retains this before delegation.

Result: **PASS.**

### R3. Target return remains central

The thin router keeps target return and attribution as the central loop, rather than turning CSW into a framework lookup tool.

Result: **PASS.**

### R4. KJ-specific phrase is no longer used as CSW's own runtime authority

The thin router no longer claims that CSW itself performs KJ. The methodological stance survives in the generic form: do not place one's explanation above the target; let target material correct it.

Result: **PASS.**

## Integration-specific checks

### I1. No semantic integration behavior is silently deleted

All cardization/grouping/label/diagram/narrative/source-return behavior is present in Layer 1 Method/Skill.

Result: **PASS.**

### I2. CSW-specific boundary survives

Framework candidates remain attributed, do not become higher-authority material, and may be weakened or withdrawn after target return.

Result: **PASS.**

### I3. Lack of synthesis Skill is survivable

Thin CSW can still return framework-generated questions and verification handoffs without falsely claiming KJ/affinity execution.

Result: **PASS.**

## Iteration-specific checks

### T1. Generic multi-round logic is not duplicated

Delta/reopen/history/stable IDs/semantic-vs-representation delta move to Layer 2.

Result: **PASS.**

### T2. Framework-specific delta survives

A later framework contact is handed off as a delta with origin and possible touched artifacts.

Result: **PASS.**

### T3. No-useful-increment remains a valid exit

Thin CSW keeps this explicitly.

Result: **PASS.**

## Build / packaging impact

Current `src/manifest.json` references the same paths:

- `core/iteration.md`
- `methods/integration.md`

The thin migration can replace file contents in-place. Therefore module IDs, skill-reference filenames, and knowledge-group paths do not need structural changes for the first Japanese research migration.

Current `scripts/build.py` copies modules based on the manifest path and concatenates knowledge groups based on the same relative paths. It does not inspect KJ-specific section names in the file contents.

Therefore:

> **in-place Japanese content replacement does not require a build-script structural change.**

However, generated plugin / dist artifacts will change after build and must be regenerated in a checkout or CI environment before merge/release.

## Manifest semantic impact

`src/manifest.json` locale descriptions still describe CSW as directly combining cultural-framework supply with KJ-method integration.

After canonical thin replacement, those descriptions become semantically stale even though the file structure remains valid.

Required follow-up:

- update the ja-JP description to describe delegation / compatible synthesis rather than owned KJ integration;
- decide whether en-US remains a pre-split control temporarily or receives equivalent translation before promotion;
- do not mark translation parity as complete until the English router/modules have been migrated and reviewed.

## Remaining open risks

1. A composite runtime may still load all three skills in one prompt and accidentally blur ownership despite file separation.
2. Handoff metadata can become too prominent in creative work.
3. External compatible affinity skills may not satisfy the same Method Definition despite similar names.
4. The historical KJ / trademark inventory must be externally reverified before public promotion.
5. Build-generated artifacts have not yet been regenerated in this connector-only session.

## Decision

**Semantic-retention gate: PASS.**

No CSW behavior required for the split was found to exist only in the monolithic source with no destination.

**Router/build impact gate: PASS for in-place Japanese research replacement, with two required companion changes:**

1. replace `ROUTER.md` together with `integration.md` and `iteration.md`;
2. update the ja-JP manifest description so capability ownership is not stale.

The next safe action is to apply these Japanese canonical replacements on the research branch, preserve the old English realization as an explicit parity backlog rather than silently claiming equivalence, and then inspect repository-generated artifact implications.
