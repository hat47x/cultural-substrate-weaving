---
name: affinity-synthesis
description: Integrates heterogeneous source material bottom-up into traceable meaning-bearing cards, emergent groups, relational structure, and narrative, then checks each transformation back against the source. Use when structure should emerge from the material rather than a predefined taxonomy, and when contradictions, epistemic seams, provenance, and residuals must remain visible. Do not use for simple fixed-category sorting, ordinary summarization, or multi-round inquiry orchestration.
---

# Affinity Synthesis

Status: research English realization

Raise structure from heterogeneous material without placing an analyst-defined taxonomy above it.

This Skill owns **one synthesis round**. It does not own source collection strategy, the decision about what to investigate next, or multi-round inquiry governance.

It learns from KJ Method, affinity-diagram, and qualitative-integration lineages while adding safeguards for generative-AI failure modes such as over-fragmentation, fluent overwrite, provenance loss, and false independent repetition. It does **not** claim to be an official implementation or complete reproduction of any historical method. KJ Method is a registered trademark of Kawakita Research Institute.

## When to use

Use it when several of these conditions apply:

- material is heterogeneous in granularity, speaker, or epistemic state;
- the right categories are not known in advance;
- you need more than a theme list: groups, relations, residuals, and a narrative are relevant;
- returning every synthesis to the source matters;
- contradictions, isolated material, weak unease, ambiguity, or unresolved material should not be smoothed away.

Do not select or reject this Skill by item count alone. A small set may still require careful semantic-boundary work.

## When not to use

Prefer another method when:

- the task is coding into a fixed taxonomy or authoritative classification;
- ordinary summarization or formatting is sufficient;
- the only need is bottom-up theme clustering, with no relation/narrative/source-return work;
- the task is a finished-claim Evidence / Inference / Assumption audit;
- the task requires repeated searching, question shifts, or multi-round continuation decisions. Use an iterative inquiry realization for that orchestration.

## Core contract

### 1. Let structure be material-led

Do not name buckets first and then fill them.

Read the material before naming groups. Similarity should arise from what the items are saying, not from source, speaker, faction, document type, metadata, or a predefined taxonomy.

### 2. Preserve meaning-bearing units and epistemic seams

A card is not mechanically the smallest fact fragment. It is a meaning-bearing unit that can stand on its own well enough to preserve what the source is saying.

Use this boundary rule:

> **Join when semantic unity must be preserved; split when epistemic state must be preserved.**

Do not split one experience, judgment, or causal movement merely because it contains several clauses. Do split when an important epistemic seam would otherwise disappear, such as observation vs interpretation, confirmed vs inferred, or a person's statement vs a third party's interpretation.

### 3. Keep provenance for audit, not grouping geometry

Preserve enough information to return a card to its source. When relevant, distinguish:

- source provenance: where the content comes from;
- discovery route: how that source was found;
- derivation: whether this card or claim was produced from another artifact.

Do not use these metadata fields as the first grouping axis.

A repost, restatement of the same event, or multiple descendants of one source card do not become independent corroboration merely because they appear several times.

### 4. Group by what the cards are saying

Form groups from semantic affinity. Small groups can be a useful working heuristic, but fixed group sizes or final theme counts are not success conditions.

Keep singletons. Keep conflicts. Do not force borderline material into a clean group just to complete the map.

If one card also strongly resonates with another group, preserve that as **secondary resonance** rather than duplicating the card or counting it as independent support.

Cluster size, repetition, or vividness is not automatically truth, importance, or independent support.

### 5. Form labels by integration, not categorization

A label should voice what the material in that group is saying together. It is not merely a category name.

When a label is difficult, use this integration kernel:

1. Inspect the boundary: what belongs together, and what must remain separate?
2. Take the core: what would be lost if each item were reduced further?
3. Temporarily put the source wording out of sight and let one new meaning unit arise from the cores rather than concatenating them with connectives.
4. Reopen the original material and repair distortion.

The temporary hiding step creates room for synthesis **and** for analyst vocabulary to enter. Therefore the return check is mandatory.

### 6. Return every synthesis to the source

After forming cards, labels, higher-order labels, relations, or narrative, return them to the input.

Look especially for additions or distortions such as:

- unsupported causality;
- invented intention or inner state;
- generalization beyond the material;
- a changed direction of evaluation;
- inference promoted to fact or hearsay promoted to confirmation;
- loss of actor, agency, or responsibility;
- silent weakening, sanitizing, or blurring;
- loss of source-specific temperature, bodily sense, scene, ambiguity, or contradiction.

After a transformation, distinguish when useful:

- **inherited**: meaning directly retained from input;
- **emergent**: meaning newly produced by contact among materials, grouping, placement, or narration;
- **residual**: difference, contradiction, texture, or uncertainty not absorbed into the synthesis.

These are post-transformation audit states, not a taxonomy imposed on input cards.

### 7. Build relational structure after groups become meaningful

Place stable groups and labels into a relational structure. Relations may include causality, mutual influence, opposition, temporal order, condition, cycle, or other predicates that the material supports.

Do not preselect relation types and make the material fit them.

Keep these representation concepts distinct:

- **membership**: a card or lower group constitutes a group;
- **explicit relation**: a readable predicate between meaning units;
- **secondary resonance**: semantic cross-contact that does not add membership or independent support;
- **layout**: visual proximity, distance, direction, enclosure, or position.

A drawn edge is not automatically causal. Visual proximity is not automatically a semantic relation.

### 8. Narrate from the relational structure

Write a narrative from the groups and relations without using prose fluency to add unsupported logic.

If narration reveals a new relation candidate, return it to the semantic record and source material before treating it as grounded. If supported, add it. Otherwise keep it as a hypothesis, unresolved relation, or narrative convenience.

### 9. Cross-check source, synthesis, map, and narrative

Before finalizing, inspect at least these directions:

- **source → synthesis**: did an important appeal disappear?
- **synthesis → source**: did the synthesis invent meaning?
- **map ↔ narrative**: did the prose add a relation absent from the map, or omit a relation the map claims?

Zero difference is not a completeness score. A visible difference may be a supported revision, emergent meaning, or residual that should remain explicit.

### 10. Treat diagrams as projections

A diagram is a projection from the semantic record, not the method authority.

Useful views can include:

- group relationship map;
- membership map;
- lineage map from source → card → group / relation / narrative claim;
- spatial map when layout itself carries analytic meaning.

Automatic layout must not create semantic assertions. If position itself matters, retain positional information separately from a topology-only renderer.

## Output contract

Use the level of externalization the task needs. A complete research-grade output may include:

- meaning-bearing cards with source/derivation references;
- groups and labels;
- singletons, conflicts, residuals, and unresolved items;
- explicit relations and secondary resonance;
- a narrative synthesis;
- source-return / transformation audit notes;
- a representation projection when useful.

Do not expose private chain-of-thought. Preserve inspectable artifacts, provenance, and transformation results instead.

## Delegation boundary

A narrower affinity-mapping Skill may be used unchanged when the task only needs bottom-up theme clustering. A concept-mapping Skill may be useful after the material is already conceptualized. Evidence/inference sorting may be useful as a downstream audit.

Do not chain those narrower operations and claim that the chain is equivalent to this method unless the invariants and regression cases are actually satisfied.

## Quality checklist

- [ ] Groups emerged from meaning, not metadata or prior categories.
- [ ] Semantic unity was not mechanically fragmented.
- [ ] Important epistemic seams remain visible.
- [ ] Derived/reposted material was not double-counted as independent support.
- [ ] Singletons, conflicts, ambiguity, and residuals were not removed for neatness.
- [ ] Labels are specific enough to voice their groups rather than merely classify them.
- [ ] Every important synthesis can be returned to source material.
- [ ] Invented causality, inner state, generalization, evaluation direction, and confidence shifts were checked.
- [ ] Membership, explicit relation, secondary resonance, and layout are distinguishable.
- [ ] Narrative-only relations were returned to the map/source before promotion.
- [ ] Rendering constraints did not rewrite semantic structure.

## Progressive references

- English Method Definition: `references/METHOD.en.md`
- Shared representation grammar: `references/REPRESENTATION.md`
- Shared machine-readable schema: `references/affinity-map.schema.json`

The shared representation files are technical research assets and may still contain Japanese explanatory prose. This English realization does not treat untranslated prose there as additional runtime instructions.
