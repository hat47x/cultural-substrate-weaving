# Scholastic disputed-question comparison fixture

Status: structural qualification / research-only

## Purpose

This fixture tests whether the de-bound cognitive operation of `scholastic-disputed-question` remains meaningfully distinct from three nearby baselines:

1. a strong ordinary software design review;
2. classical stasis theory;
3. Nyāya five-member inference.

It is not an efficacy benchmark and does not score frameworks. The question is narrower: **after framework-specific vocabulary is removed, what operation remains that another baseline does not already provide?**

The comparison reuses the embedded-state-store target from the positive worked example so the target material stays fixed.

## Fixed target

A team proposes a local-first embedded relational state store for the first release of a small distributed-compute control plane.

The live concerns are:

- O1 — restart durability;
- O2 — concurrent authority;
- O3 — operational recovery;
- O4 — migration lock-in.

The candidate decision is to use an embedded reference store only under bounded durability, conditional-update, replacement-boundary, and operational-evidence requirements.

## A — strong ordinary design-review baseline

Use no cultural framework.

A deliberately strong ordinary review can already require:

- stable concern IDs;
- one explicit decision statement;
- a response mapped to each concern;
- evidence or test requests attached to each response;
- unresolved concerns carried forward rather than closed rhetorically.

Applied to the target, this baseline can preserve O1–O4, map responses R1–R4, and leave O3 unresolved.

### Residual

This is an important overlap, not a failure of the baseline.

If the caller already has stable concern identity, pointwise response coverage, and explicit unresolved-item carry-forward, disputed-question structure adds little beyond provenance and a mnemonic source.

The candidate should therefore **not** activate merely because a task is called a "design review" or contains objections.

## B — classical stasis theory

Stasis theory asks what kind of dispute is live before choosing an argumentative response.

On this target it can expose that the concerns are not one homogeneous "database risk". Some questions ask whether a property actually holds, some ask what the release claim means, some evaluate sufficiency, and some concern the proper boundary of the decision.

### Residual

Stasis is useful when reviewers are answering different kinds of questions as though they were one dispute.

It does **not** by itself require the final determination to return to every prior objection. A review can correctly identify issue types and still leave O3 unanswered.

The de-bound difference is therefore:

```text
stasis:
  what kind of question is live?

disputed-question:
  did the determination actually answer each preserved objection?
```

The operations are complementary rather than substitutes.

## C — Nyāya five-member inference

Nyāya five-member inference can unfold the argument behind the candidate claim:

> an embedded store is sufficient for the first release under the stated scope and replacement boundary.

It asks for the thesis, reason, corroborating case or accepted relation, application to this target, and conclusion. This is especially useful if "the first release does not need a distributed database" is being used as a fluent but incomplete bridge to "the embedded store is sufficient."

### Residual

Nyāya centers the inferential bridge from reason to conclusion.

It can expose a weak application even when no reviewer has articulated O1–O4. Conversely, a sounder inference can still leave an independently raised objection unanswered.

The de-bound difference is therefore:

```text
Nyāya:
  does the reason actually support this conclusion in this case?

disputed-question:
  which preserved objections does the final rationale answer, and which remain?
```

Again, the operations are complementary.

## D — scholastic disputed-question pass

The de-bound form retains only:

1. one explicit decision question;
2. materially distinct objections with stable identities;
3. a candidate determination;
4. pointwise replies linked back to the exact objections;
5. unresolved objections carried forward without manufacturing closure.

For the fixed target:

- O1 receives a restart-conformance evidence requirement;
- O2 receives a bounded conditional-update reply without a multi-instance-safety claim;
- O3 remains unresolved pending inspection/export/backup evidence;
- O4 receives an abstraction-boundary check.

No medieval authority, Latin terminology, master/student hierarchy, or theological proposition is needed for the operation to survive target return.

## Comparison result

### Distinctness from stasis: strong

The primary operation differs. Stasis discriminates issue type; disputed-question checks objection-to-reply coverage.

### Distinctness from Nyāya: strong

The primary operation differs. Nyāya audits an inference bridge; disputed-question preserves multiple adverse arguments through a determination.

### Distinctness from a mature ordinary design review: weak to moderate

A mature review process can reproduce almost the entire de-bound operation with concern IDs and a response matrix.

This means the cultural framework should not be adopted as a universal review layer. Its value is narrower: it provides a portable substrate for **objection identity + pointwise reply coverage + unresolved-objection carry-forward** when the caller does not already have that discipline.

## Qualification decision

Keep `scholastic-disputed-question` at `profile-ready` for now.

The candidate has a real portfolio contribution relative to Stasis and Nyāya, but runtime adoption would be premature until the remaining overlap with ordinary design-review mechanics is handled explicitly.

Refined activation boundary:

- consider contact when materially different objections are being collapsed, silently dropped, or answered only by a global rationale;
- do not activate when the target already maintains stable objection IDs, pointwise response coverage, and unresolved-item carry-forward;
- stop if the "objections" have to be invented because no stable proposal or decision question exists;
- after de-binding, preserve only the target-side question, objection identities, reply links, evidence requests, and unresolved residuals.

## Product-value consequence

The useful contribution is not "medieval debate for software architecture."

The candidate earns a place in the research registry only insofar as it supplies a reproducible missing operation. Where ordinary review already supplies the same operation, CSW should prefer non-activation. This keeps framework count from becoming a proxy for cognitive coverage and protects the Registry from accumulating culturally different names for operationally redundant review mechanics.
