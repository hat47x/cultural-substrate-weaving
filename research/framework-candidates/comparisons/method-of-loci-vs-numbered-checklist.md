# Greco-Roman method of loci vs ordinary numbered checklist

Status: structural counterfactual / no runtime promotion

## Purpose

The existing method-of-loci candidate explicitly leaves one strong counter-hypothesis unresolved:

> if the de-bound operation is reproduced by an ordinary numbered checklist with less cognitive overhead, the cultural framework does not add a distinct CSW runtime operation.

This fixture resolves that question on the same migration-plan target used by the positive worked example. It is a structural comparison, not an empirical efficacy benchmark.

## Fixed target

A migration plan contains preparation, data copy, cutover, verification, and rollback material. Reviewers suspect that important operational steps disappear when the plan is repeatedly summarized.

The method-of-loci worked example uses twelve stable checkpoints and finds two gaps:

- L4 — restore rehearsal evidence;
- L12 — post-rollback verification.

A later revision fills L4 while L12 remains unresolved.

## Condition A — method-of-loci contact

The de-bound operation is:

1. define a stable ordered set of distinguishable positions;
2. bind current target content to those positions;
3. traverse the positions in order;
4. localize an empty, duplicated, or swapped position;
5. replace bindings explicitly when the target changes;
6. return every detected gap to the source-of-truth material.

On the fixed target, this yields the two questions already recorded in the worked example:

- what evidence shows that the backup can actually be restored before cutover?
- after rollback, what establishes that the old service state is healthy again?

## Condition B — ordinary numbered checklist

Use no cultural framework.

Create a reusable review template with the same target-side checkpoints:

1. entry criteria;
2. dependency freeze;
3. backup/export;
4. restore rehearsal evidence;
5. data-copy start;
6. copy completion verification;
7. write cutover;
8. read verification;
9. external integration verification;
10. rollback trigger;
11. rollback execution;
12. post-rollback verification.

For the current plan, map each source statement to the checklist item it satisfies. Do not invent content to fill a blank.

The first pass leaves item 4 and item 12 blank.

The same two target questions follow:

- what evidence shows that the backup can actually be restored before cutover?
- after rollback, what establishes that the old service state is healthy again?

When a later revision adds restore-rehearsal evidence, update item 4's source binding. Item 12 remains unresolved.

## Operation-by-operation comparison

| De-bound operation | Method of loci | Numbered checklist | Residual difference for this target |
|---|---|---|---|
| stable scaffold vs variable content | loci remain stable while images/cues change | checklist IDs remain stable while source bindings change | none needed for target review |
| binding | cue/image -> locus | source statement -> checklist ID | checklist is more direct |
| ordered traversal | mentally/explicitly walk loci | inspect checklist in order | no target-side difference |
| omission localization | empty locus | unchecked / unsupported item | no target-side difference |
| swap / duplicate localization | unexpected content at a locus | wrong / duplicate checklist binding | no target-side difference |
| rebinding after revision | replace image/cue at a locus | replace source binding at an item | no target-side difference |
| source return | reopen target record | reopen target record | identical requirement |
| mnemonic imagery / learned spatial route | native historical technique | absent | human-memory function, not required by this AI review task |

## Result

For this realistic SIer review target, the direct counter-hypothesis survives.

The numbered checklist reproduces every target-relevant de-bound operation and produces the same useful questions with a simpler representation. The method-of-loci-specific residue is the mnemonic use of imagined or learned places and images. That residue can matter for **human recall or rehearsal**, but it does not currently supply a distinct generative operation for document-grounded AI review.

This is stronger than saying that the two methods merely overlap. On this target, the cultural framework adds no demonstrated CSW product value after de-binding.

## Runtime consequence

Do not promote `greco-roman-method-of-loci` into the runtime corpus for general CSW analysis.

Do not treat "stable spatial index / variable-content rebinding / ordered reconstruction" as a currently missing runtime operation family merely because it lacks a cultural framework. An ordinary explicit checklist already supplies the target-relevant operation in the tested use.

Keep the candidate as a sourced research reference because its historical structure is well documented and may become relevant when the **target itself concerns human memory, rehearsal, recall, or spatial mnemonic design**. Such a use would require a new target-specific justification; the current software-review fixture does not establish it.

## Activation boundary

For current CSW use:

- prefer the ordinary checklist when the job is explicit ordered coverage, omission localization, or versioned rebinding;
- do not activate method of loci merely to make an ordered review culturally different;
- reconsider only when the target contains a real human-memory or rehearsal constraint for which place/image binding is itself part of the problem;
- even then, mnemonic recall remains separate from target truth.

## Product-value consequence

A research candidate can be culturally distinctive and historically faithful while still failing to add a new runtime cognitive operation.

Rejecting runtime promotion in that case is a positive Registry result. It prevents raw framework count from masquerading as cognitive coverage and keeps the runtime portfolio focused on operations that change what the system can actually ask, distinguish, or construct.
