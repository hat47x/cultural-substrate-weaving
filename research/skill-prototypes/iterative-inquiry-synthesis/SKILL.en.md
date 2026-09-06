---
name: iterative-inquiry-synthesis
description: Orchestrates repeated inquiry rounds in which new material is synthesized, residual gaps and conflicts become explicit next questions, and later evidence is returned to prior material state without overwriting history. Use for long-running research, analysis, design, or creative inquiry that needs delta-based reopening across rounds. Do not use for a single synthesis round or as a domain-specific research method.
---

# Iterative Inquiry Synthesis

Status: research English realization

Do not freeze a one-round synthesis as a permanent conclusion. Preserve what later material changes, what it leaves unchanged, and what remains unresolved, then reopen only what the new delta actually touches unless a global contradiction requires broader reconsideration.

This Skill **does not own the one-round synthesis algorithm**. When available, use `affinity-synthesis` or another realization satisfying the same Method Definition for the synthesis step inside a round.

## When to use

Use it when:

- research, design, creative work, or analysis will receive material over multiple rounds;
- a prior synthesis has produced gaps, conflicts, singletons, or unresolved questions that may become relevant later;
- new material should be compared against existing structure rather than causing a full restart each time;
- the inquiry itself may shift as material changes;
- long-running work needs a traceable account of what changed and what survived.

## When not to use

Do not prioritize this Skill when:

- one synthesis round is enough;
- the same fixed dataset is simply rerun with no changing inquiry or material state;
- the primary need is domain-specific search strategy, legal/medical judgment, product prioritization, or another domain method;
- running a predetermined number of rounds has become the goal.

## Core round

Persist inspectable artifacts rather than private chain-of-thought.

1. **Receive delta**
   - new source, observation, counterexample, execution result, or changed constraint.
2. **Locate touched semantic artifacts**
   - bring forward only relevant prior cards, groups, relations, secondary resonance, residuals, and questions.
   - reuse stable semantic handles when available.
3. **State the current inquiry**
   - write one sentence saying what this round is trying to distinguish or understand.
   - do not assume the prior question is still the right one.
4. **Run one synthesis realization**
   - send new material plus only the needed prior material to one compatible synthesis method.
   - record which realization was used.
5. **Inspect structural delta**
   - what emerged?
   - what changed?
   - what was explicitly checked but remained semantically stable?
   - what weakened or was withdrawn?
6. **Separate semantic delta from representation-only delta**
   - distinguish changes in card meaning, membership, labels, explicit relations, resonance, residuals, or questions from wording, renderer, line wrapping, or layout changes.
7. **Externalize residuals**
   - preserve gaps, conflicts, singletons, unresolved questions, and weak relations that remain open.
8. **Decide the continuation boundary**
   - is there material that can actually discriminate the remaining question?
   - is another round useful for the current purpose?
   - is the next step a human/domain decision or external action rather than more synthesis?
9. **Freeze a round snapshot**
   - append the delta and return points without overwriting previous rounds.

## Round contract

A round should be able to expose, as needed:

- round id;
- current inquiry / purpose;
- input delta;
- reopened prior artifact refs / touched semantic IDs;
- synthesis realization id or name;
- representation/schema ref when available;
- output artifact refs;
- residual refs;
- semantic structural delta;
- representation-only delta when relevant;
- possible next inquiry / verification target;
- stop / continue / handoff reason.

The storage format is not fixed.

### Compact delta notation

With stable IDs, these symbols may describe **change operations**:

```text
+  newly emerged
~  changed
=  touched and explicitly checked, but semantically unchanged
-  withdrawn / no longer supported
?  unresolved / residual remains
```

Example:

```text
+ C115 := "meaning unit raised from new material"
~ G03 := members + {C115}; label "old label" -> "revised label"
= G04 :: "new material checked; semantic core still holds"
- R02 :: "previous direction is no longer supported"
+ R05: G03 -- G07 :: "new relation predicate"
? Q08 :: "current material still cannot discriminate this"
```

These symbols describe change. They are not a taxonomy for cards or groups.

## Stable semantic handles

When the one-round synthesis representation has stable IDs such as `C / G / R / X / U / Q`, reuse them across rounds while semantic identity survives.

- Do not assign new IDs merely because wording was polished.
- The same ID can still record meaningful change, e.g. `~ G03`.
- When a unit splits or merges and identity no longer survives, create new IDs and preserve derivation from the old ones.

Stable IDs are handles for local reopening and history comparison, not semantic classes.

## Semantic delta is not diagram delta

A change in node position, line curvature, automatic layout, line wrapping, color, or shape is not automatically a new discovery.

A representation change may make a previously unnoticed relation candidate visible. If that happens, record it as a **candidate** and return it to the semantic record and source material before promotion.

Do not convert visual proximity into a relation, or vertical placement into hierarchy or causality, without semantic support.

## Do not rebuild without cause

New material by itself is not a reason to reconstruct every prior group and relation.

Ask first:

- does the new material actually change an existing core?
- can it be added locally?
- does it raise a genuinely independent appeal?
- does it resolve or deepen an existing conflict?

If the old structure still represents the material well, preserve it and record only the meaningful delta.

## Residuals are reopenable anchors

Residual material is not deleted merely because it remains unresolved.

Examples include:

- gap: an absence or relation worth checking later;
- conflict: material that cannot currently be reconciled;
- singleton: an appeal not yet grouped with others;
- unresolved: a distinction current material cannot make.

These are examples rather than a closed taxonomy.

Background them when irrelevant to the current inquiry. Reopen them when later material actually touches them.

## Question shift

Questions may move backward, forward, or sideways. Problem-solving work may involve situation, problem framing, essence, conception, concrete measures, sequencing, and validation, but these are not fixed stage gates.

When the question changes, do not rewrite prior rounds to make the new question appear to have been the old one. Record what caused the shift and what from the earlier structure remains useful.

## Stop conditions

A complete explanation or zero residuals is not required.

A round sequence may stop when:

- additional rounds no longer produce meaningful structural change for the current inquiry;
- unresolved material remains but no currently available evidence can discriminate it;
- the intended level of understanding has been reached;
- the next step is a domain decision, human value judgment, or external action;
- further exploration costs more than the expected cognitive gain;
- external conditions require closing.

## Restart conditions

Reopen when there is a reason such as:

- new source or observation;
- counterexample;
- environmental change;
- contact with an old residual;
- explicit revisit;
- a different cognitive field exposes a concrete new question.

Do not treat a prior stop as failure. Reopen only what the new reason touches unless its impact is global.

## External exploration routes

Web research, interviews, experiments, cultural frameworks, or domain skills may supply material or questions to a later round.

They supply input; they do not automatically determine truth status.

When `cultural-substrate-weaving` supplies a framework-generated question or correspondence candidate, preserve its origin and return it to target-side material rather than promoting it directly to an observation.

## Quality checklist

- [ ] Round count is not being optimized for its own sake.
- [ ] Previous rounds remain inspectable rather than overwritten.
- [ ] Material that did not touch an artifact did not trigger needless reconstruction.
- [ ] Stable semantic IDs survive when identity survives.
- [ ] The synthesis realization used in each round is traceable.
- [ ] Semantic delta is separated from wording/renderer/layout delta.
- [ ] Diagram proximity or hierarchy was not promoted into semantic relation automatically.
- [ ] Gaps, conflicts, singletons, and unresolved items were not converted into observations.
- [ ] Question shift was not treated as failure or as a progress score.
- [ ] Stop/continue reasoning is externally inspectable.
- [ ] Stored history consists of external artifacts and decisions, not private chain-of-thought.

## Progressive references

- English Method Definition: `references/METHOD.en.md`
- Japanese research round template: `references/ROUND-TEMPLATE.md`
- Layer 1 semantic representation: sibling prototype `../affinity-synthesis/`

The untranslated round-template prose is not treated as additional English runtime instruction. The round contract above is authoritative for this English research realization.

## Boundary

This Skill does not decide what is true, which recommendation should be adopted, or which action should be executed.

Its role is to **preserve inquiry, material, synthesis results, and meaningful delta across rounds so the next cognitive round can reopen the right place without destroying history**.
