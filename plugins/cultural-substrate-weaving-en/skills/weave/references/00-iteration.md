# Framework contact and round handoff

Read this when work resumes because of new material or contact with another cultural framework.

This document does not implement multi-round inquiry orchestration itself. Delta-based reopening, stable artifacts, question shifts, append-only round history, and related concerns are delegated to a dedicated Method / compatible realization. CSW hands off what newly arose from framework contact with its origin intact.

## Responsibility boundary

When multi-round reopening or delta management is needed, use `iterative-inquiry-synthesis` or another compatible realization satisfying the same Method Definition when available.

Delegate these concerns to the iterative layer:

- input delta
- touched-artifact reopen
- local / global reopen decision with reason
- stable semantic IDs across rounds
- structural delta
- question shift
- semantic delta vs representation delta
- append-only history
- residual / reopen condition
- continue / stop / handoff reason

CSW does not independently re-implement this general round governance.

## Hand new framework contact off as a delta

When a later point in the work produces a new candidate from:

- another cultural framework;
- another position in the same framework;
- another native operation;
- a depth change from preview to full; or
- a different question exposed by revisiting the framework,

do not automatically re-synthesize all prior material.

When useful, hand off at least:

```text
new material / question:
origin / framework ref:
possibly touched prior artifact / residual:
framework contact change:
```

The iterative Method decides how far reopening should extend.

## A framework contact may yield no useful increment

If a probe or preview produces no new question, contrast, or residual worth returning to the target, treat that as a valid result.

For example:

```text
framework contact: no_useful_increment
material delta: none
reopen request: none
```

Do not manufacture an insight or another round merely because a framework was opened.

## Preserve attribution across rounds

If later target-side material supports, refutes, or modifies a framework-generated candidate, do not erase where the original question came from.

Origin and verification can remain separate.

```text
meaning: <current meaning>
origin: framework_generated
verification: target_supported | unresolved | contradicted / weakened | other explicit state
verification_basis: <target-side refs>
```

Later support does not justify rewriting the earlier round as if the candidate had been a target fact from the start.

When target material refutes a framework reading, do not weaken the target material to protect the framework.

## When no iterative realization is available

Even when no compatible Layer 2 realization is available, CSW can return a one-pass exploration result containing:

- newly generated framework candidates;
- origin;
- what needs target-side verification;
- where later work should return; and
- unresolved / reopen conditions.

But if append-only round history, touched-artifact reopening, structural delta, and similar behaviors were not actually run, do not claim that multi-round orchestration was executed.

## CSW-specific event

General longitudinal event taxonomies belong to iterative / governance layers.

What remains especially relevant to CSW is being able to trace that framework contact changed.

When useful, record an event equivalent to `framework_contact_change`.

Example:

```text
framework: FW-A -> FW-B
change: preview position changed / native operation changed / no-useful-increment
produced: F5, Q2
handed_to: iterative inquiry round N
```

The event itself is not a judgment of usefulness or correctness.

## Stopping and reopening

Do not require a fixed number of frameworks, rounds, `full` depth, or framework-native operations as a CSW completion condition.

If a framework produces a concrete new question that justifies reopening, hand that question to Layer 2.

If additional framework contact does not move target-side questions, material arrangement, artifacts, or decisions, stopping with `no_useful_increment` intact is valid.

Authority over stopping, adoption, and action follows the delegation boundary in `core/principles-and-constraints.md`.

## Minimal handoff

When handing work to iterative inquiry, include only what the current task needs, such as:

- current inquiry;
- new framework-derived material / question;
- origin / framework ref;
- touched candidate refs if known;
- unresolved / verification need; and
- return-to-target condition.

Do not copy the complete text of prior rounds.

## CSW canonical responsibilities

Higher-level principles remain in `core/principles-and-constraints.md`.

In particular, keep possibility separate from adoption, cognition separate from fact, and preservation separate from current attention.
