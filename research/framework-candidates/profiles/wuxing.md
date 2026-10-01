# Wuxing framework profile candidate

Status: adopted / runtime-corpus

## Identity

- names: 五行 / Wuxing / Five Phases
- family: Chinese correlative and process traditions
- intended CSW use: relation/cycle generator, not elemental personality typing
- current profile scope: phase relations and transformation only

## Source basis

### Scholarly references

Stanford Encyclopedia of Philosophy, Metaphysics in Chinese Philosophy

https://plato.stanford.edu/entries/chinese-metaphysics/

This source describes wuxing as wood, earth, fire, water, and metal within a process/cycle-oriented Chinese metaphysical context and explicitly notes generation sheng and overcoming ke progressions.

Stanford Encyclopedia of Philosophy, Religious Daoism

https://plato.stanford.edu/entries/daoism-religion/

Useful for the historical role of the five agents/phases as a system that classifies and relates phenomena across domains.

## Structural core retained by this profile

### Five phases

- Wood
- Fire
- Earth/Soil
- Metal
- Water

For CSW these are not treated as five physical substances. The first cognitive value is that the system supplies a small closed set of relationally differentiated phases.

### Generation relation

A cycle of generation / production.

Cognitive use:

- ask what enables or feeds what;
- trace indirect enabling around a loop;
- identify where a process expected to continue does not.

### Overcoming relation

A distinct cycle of constraint / overcoming.

Cognitive use:

- separate enabling from limiting;
- ask whether a stable system requires both;
- expose cases where a proposed solution strengthens one path but removes a necessary constraint.

### Correlative extension

Historically wuxing was extended across many domains.

For this profile, that fact is a caution and optional research direction, not permission to load every correspondence table at once.

## Native operation candidates

### generation-pass

Apply only the generation relation as an as-if model.

Questions:

- What feeds the next condition?
- What depends on a previous phase?
- Where is the expected handoff absent?

Output type:

- relation-candidate
- transition-candidate
- residual

### constraint-pass

Apply only the overcoming/constraint relation.

Questions:

- What limits excess?
- Which relation acts as a brake rather than a source?
- Is an apparently negative constraint structurally stabilizing?

Output type:

- counter-relation
- falsifier
- observation target

### dual-relation-pass

Compare generation and constraint without merging them.

Questions:

- Does the same target pair participate differently under enabling vs limiting views?
- Is a single causal verb hiding two relation types?
- Does the proposed improvement create runaway reinforcement by removing constraint?

Output type:

- distinction
- relation-candidate
- counter-view

### cycle-break

Remove or weaken one link hypothetically.

Questions:

- Does the cycle still close?
- Which downstream element becomes unsupported?
- Does another path compensate?

Output type:

- falsifier
- transition-candidate
- residual

## What not to import by default

- body organ correspondences;
- personality typing;
- colors, directions, planets, sounds, emotions, tastes, seasons as one undifferentiated canonical table;
- medical diagnosis;
- feng shui rules;
- astrology;
- claims that a target literally possesses one of the five phases.

Specific correspondence layers may be researched later with lineage and source labels.

## Exploratory prompts produced by this profile

- Which relation is generative, and which is constraining?
- If this is a loop rather than a chain, where does feedback return?
- What is currently overproduced because its counter-relation is absent?
- What appears harmful locally but stabilizing globally?
- If one link is removed, where does the first observable failure appear?
- Does the target require a five-way classification at all, or is the useful contribution only the relation grammar?

The last question is important: CSW may keep a relation question even when the five-phase assignment itself is discarded.

## De-binding

1. remove Wood/Fire/Earth/Metal/Water labels from the target-facing candidate;
2. preserve the relation verb that proved useful;
3. state whether it came from generation, overcoming, or another explicitly sourced relation;
4. return the candidate to target evidence;
5. if target material does not support the phase mapping, withdraw the mapping without discarding a surviving question.

## Adoption synchronization

This framework is adopted in `src/ja-JP/frameworks/wuxing.md` as a relation/cycle dossier.

Runtime adoption licenses the explicitly sourced generation and overcoming relations, role reversal, cycle-break questions, and de-binding back to target relation verbs. It does not load medical, astrological, directional, or personality correspondence tables.

Target-return example: a five-phase assignment may be discarded after use, while the surviving target question “which enabling relation became unstable because a constraining relation was removed?” remains testable in the target. Historical correspondence layers remain enrichment work rather than part of the adopted core.
