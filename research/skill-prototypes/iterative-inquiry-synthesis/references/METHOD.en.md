# Iterative Inquiry Synthesis — Method Definition

Status: research candidate, English translation draft

## Purpose

Do not freeze one synthesis result as a final conclusion. Return unresolved material, conflicts, gaps, and new evidence to only the parts of the inquiry that need reopening.

The goal is not to maximize the number of rounds.

> **Preserve what changed, what did not change, and what remains unknown, and continue inquiry only while there is meaningful delta to examine.**

## Scope

This method owns multi-round inquiry orchestration.

It owns:

- current inquiry / purpose;
- input delta;
- prior artifact reopening;
- synthesis-realization binding;
- structural delta;
- residuals / unresolved material;
- continuation / stop / handoff reason;
- append-only round history;
- restart conditions.

It does not own:

- the one-round synthesis algorithm;
- web/search strategy itself;
- domain expertise;
- recommendation or decision authority;
- action execution;
- private chain-of-thought.

## Relationship to iterative research practices

Useful operational ideas from autonomous or iterative research systems include:

- make the current objective explicit;
- record external artifacts per iteration;
- keep an append-only ledger;
- retain recovery points;
- state stop conditions;
- carry evidence/source state into the next round.

The following are not invariants of this method:

- mandatory scalar optimization metrics;
- exactly one change per experiment;
- continuing until a maximum iteration count is exhausted;
- requiring machine-checkable success for normal stopping;
- a mandatory search backlog;
- autonomous execution as the default.

This method also supports inquiry in research, creation, analysis, and design that cannot be reduced to one scalar metric.

## Inputs

- current inquiry / question;
- previous round snapshot or artifact references;
- new material / counterexample / changed constraint / external result;
- existing residuals;
- optional prior synthesis structure.

## Outputs

- round snapshot;
- reopened artifact refs;
- synthesis-realization binding;
- structural delta;
- newly emerged meaning / relation / question;
- preserved unchanged structure;
- weakened or withdrawn prior interpretation;
- residuals;
- possible next inquiry;
- stop / continue / handoff reason.

## Invariants

### I1. A round is a delta, not a restart

Do not summarize or regenerate the entire history merely because new material arrived. First locate which artifacts, groups, relations, residuals, or questions the delta touches.

### I2. Reopen only what is touched unless a global contradiction appears

If the delta is local, reopen locally. Reopen more broadly only when a counterexample, changed premise, or question shift can affect the wider structure.

### I3. Old structure has no immunity

Preserving existing groups, labels, or hypotheses is not a goal in itself. If new material changes the core, split, merge, relabel, weaken, or withdraw the old structure.

"Do not destroy existing structure casually" is not the same as "treat existing structure as correct."

### I4. Structural delta is explicit

After a round, it should be possible to distinguish at least:

- newly emerged;
- changed;
- explicitly checked but unchanged;
- weakened / withdrawn;
- unresolved.

No semantic change can itself be a meaningful result.

### I5. Residuals are reopenable anchors

Do not delete gaps, conflicts, singletons, or unresolved items merely because they are incomplete. Preserve them as anchors that later material can touch.

### I6. Question shift is versioned, not rewritten

When the inquiry changes, do not rewrite earlier rounds to use the current question. Preserve what triggered the shift and which parts of the earlier understanding remain useful.

### I7. Continuation requires an externally intelligible reason

A next round needs a reason such as:

- new material exists;
- a residual can now be checked;
- a contradiction needs discrimination;
- narration produced an unverified relation;
- environmental conditions changed;
- the user explicitly requests a revisit;
- another cognitive field exposes a concrete new question.

"Too few rounds have happened" is not a reason.

### I8. Stopping with unresolved material is valid

Normal stopping may occur when:

- additional material is not currently obtainable;
- additional rounds produce no meaningful structural change;
- the current purpose has reached sufficient granularity;
- the next requirement is a human value judgment, domain decision, or external action;
- expected cognitive gain is lower than exploration cost.

Zero gaps and complete explanation are not required.

### I9. Append-only history, current-state projection

Do not destructively update earlier rounds. A current-state projection may be maintained, but the history must remain returnable to the round in which each change occurred.

### I10. Method realization is explicit

Track which synthesis realization was used in each round. If the realization changes, preserve that fact because output differences may arise from the method implementation rather than new material.

### I11. External exploration outputs keep their epistemic status

Web research, interviews, experiments, and cultural frameworks may supply material or questions. Do not erase their source/epistemic state and merge them directly into established facts.

An exploration route supplies input; it does not automatically determine truth status.

### I12. No private chain-of-thought as history

The method history consists of externally meaningful artifacts: inquiry, material, outputs, deltas, residuals, and decision reasons. Token-by-token hidden reasoning is not the canonical record.

### I13. Stable semantic handles survive across rounds when identity survives

When one-round synthesis artifacts have stable IDs, reuse the same handle while semantic identity remains.

A wording change alone does not require a new ID. The same handle may record changed membership, label, or meaning. When split/merge destroys identity, use new IDs and preserve derivation from the old ones.

### I14. Semantic delta and representation delta are distinct

Distinguish:

- **semantic delta**: changes in card meaning, membership, labels, explicit relation predicates/direction/state, secondary resonance, residuals, or questions;
- **representation delta**: line wrapping, wording normalization, renderer change, color/shape, automatic layout, or visual position adjustment.

Do not count a moved diagram node or changed sentence order as a new structural discovery by itself.

If representation change may have altered interpretation, return from the projection to the semantic record and recheck it.

## Round kernel

```text
receive delta
  ↓
locate touched artifacts / stable semantic IDs
  ↓
state current inquiry
  ↓
reopen locally or globally with reason
  ↓
run one compatible synthesis realization
  ↓
compare with prior semantic structure
  ↓
separate semantic delta from representation-only delta
  ↓
record new / changed / unchanged / withdrawn / residual
  ↓
continue | stop | handoff
  ↓
append round snapshot
```

## AI-era advantage and risk

Generative AI can reread and resynthesize material cheaply, making many rounds easier than in older human-only workflows. The same ability can create failure modes:

- rebuilding everything each round and causing history drift;
- counting wording change as discovery;
- repeatedly processing derivatives until they look like independent support;
- deleting residuals to manufacture completion;
- confusing endless iteration with depth;
- treating renderer/layout changes as meaning changes.

The central AI-era correction is to use recomputation capacity for **delta-based reopening rather than automatic total regeneration**.

## Relationship to Affinity Synthesis

`affinity-synthesis` owns one-round meaning integration.

`iterative-inquiry-synthesis` owns how the input, output, residuals, and realization binding move across rounds.

Layer 2 does not reimplement Layer 1 grouping or labeling algorithms.

If the one-round representation has stable semantic IDs, Layer 2 may reuse them for local reopening and delta comparison.

## Relationship to Cultural Substrate Weaving

CSW is one possible external exploration route. It may return questions, contrasts, or correspondence candidates from cultural frameworks.

Layer 2 preserves that origin when connecting them to later material. Framework-generated candidates are not automatically promoted to target-supported observations.

## Failure modes

- rebuilding the whole structure whenever any new material arrives;
- forcing new material into old groups to protect prior structure;
- erasing question shifts from history;
- using round count or token volume as progress;
- converting guesses into facts to eliminate unresolved material;
- treating stopping as failure and iterating indefinitely;
- confusing realization changes with material changes;
- promoting an external exploration hypothesis to source fact;
- counting wording/renderer/layout changes as semantic discoveries;
- assigning new IDs every round and making local comparison impossible.

## Realization boundary

This Method Definition does not require a particular filesystem layout, JSON schema, autonomous-agent loop, search tool, maximum round count, time budget, or model.

An Agent Skill realization may implement templates or ledgers as needed. It may also be replaced if another realization satisfies these invariants and the relevant regression cases.
