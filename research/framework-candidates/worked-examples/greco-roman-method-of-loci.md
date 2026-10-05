# Greco-Roman method-of-loci worked example

Status: hypothetical / research-only

## Target

A migration plan is written as several pages of prose. The plan contains preparation, data-copy, cutover, verification, and rollback material, but reviewers repeatedly discuss individual details without noticing whether the operational sequence itself is complete.

The source-of-truth document remains the migration plan. The framework is used only as a temporary review scaffold.

## Framework contact

Create a stable sequence of deliberately plain checkpoints:

- L1 — entry criteria;
- L2 — dependency freeze;
- L3 — backup/export;
- L4 — restore rehearsal evidence;
- L5 — data-copy start;
- L6 — copy completion verification;
- L7 — write cutover;
- L8 — read verification;
- L9 — external integration verification;
- L10 — rollback trigger;
- L11 — rollback execution;
- L12 — post-rollback verification.

Bind the plan's current statements to these positions. Do not invent content merely to fill every position.

## Traversal

The first pass finds target material for L1–L3 and L5–L11.

L4 has no target-side evidence: the plan says a backup is taken, but nowhere records that a restore has been rehearsed.

L12 is also empty: rollback steps exist, but there is no explicit verification step after rollback.

The useful result is not "a memory palace found two risks." It is two localized target questions:

- **L4:** what evidence shows that the exported backup can actually be restored before cutover?
- **L12:** after rollback, what target-side checks establish that the old service state is healthy again?

## Rebinding check

A later migration-plan revision adds restore-rehearsal evidence at L4. The scaffold can be reused, but the old L4 binding is replaced explicitly rather than assumed to remain current.

L12 remains unresolved.

## Target return

The two questions are reopened against the migration document and its test evidence.

- L4 survives because a real target-side omission existed and is later filled.
- L12 survives as an unresolved operational-review item.
- The spatial labels themselves are discarded from the final design record unless they remain useful for review navigation.

## Why this might be distinct

The contact separates a stable review sequence from version-specific content, then uses traversal to localize where the prose no longer supplies an expected item.

However, a numbered checklist could plausibly produce the same result. The candidate therefore remains research-only until that baseline comparison shows whether the loci-derived scaffold contributes anything beyond ordinary explicit ordering.
