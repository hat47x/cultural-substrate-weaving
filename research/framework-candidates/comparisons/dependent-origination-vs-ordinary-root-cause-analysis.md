# Dependent origination vs ordinary root-cause / dependency analysis

Status: runtime requalification / same-target ordinary-baseline comparison

## Purpose

Dependent origination was previously a default runtime framework and the typology notes that it has also been a model default pick.

This comparison applies the current requalification question:

> after de-binding, does dependent origination add a target-relevant cognitive operation that strong ordinary root-cause, fault-tree, dependency, and counterfactual analysis does not already provide?

The target is the same rolling-deployment job-control incident used in the dependent-origination and Paṭṭhāna fixtures.

## Fixed target

Observed symptom:

> a job is accepted, but some attempts fail after a rolling deployment.

Known evidence includes credential validity, cached worker capability, heartbeat freshness, state revision, and queue redelivery.

## Condition A — dependent-origination-derived pass

The de-bound pass performs five jobs:

1. **condition-chain** — expand a compressed cause statement into upstream conditions;
2. **upstream-condition** — continue past the nearest symptom;
3. **cessation-counterfactual** — ask what should stop when a condition is removed;
4. **dependency-reframing** — treat apparently self-standing behavior as condition-dependent;
5. **intervention-point selection** — look for observable or modifiable conditions.

A representative chain is:

```text
attempt failure
  <- rejected worker request
  <- unusable worker selected
  <- stale eligibility/capability state
  <- credential-state change did not propagate
```

The resulting target questions include cache invalidation, credential refresh propagation, and expected failure cessation.

## Condition B — strong ordinary engineering baseline

### Five Whys / root-cause drill-down

ASQ describes Five Whys as repeatedly moving through layers of symptoms to underlying causes.

Applied to the same target:

- Why did the attempt fail? The worker request was rejected.
- Why was that worker selected? Scheduler state still marked it usable.
- Why was scheduler state stale? Capability / eligibility did not update with credential state.
- Why did that update lag? The invalidation boundary did not include credential-state change.
- What change prevents recurrence? Make credential-state transition invalidate or version the relevant scheduler state.

This reproduces upstream-condition search and chain expansion.

### Fault-tree analysis

NASA's Software Fault Tree Analysis starts from a system-level failure and expands necessary preconditions, using logical AND / OR relationships.

For the same target, the top event can be represented as combinations such as:

```text
failed execution after dispatch
  AND/OR
    unusable credential
    worker still selected
      AND
        stale capability/eligibility state
        dispatch occurs inside stale-state window
```

This ordinary method not only reproduces condition expansion but handles branching and combinations more explicitly than the current chain-oriented framework pass.

### Counterfactual / intervention question

Ordinary causal analysis can ask directly:

> if capability state were invalidated when credential state changed, while other conditions were held fixed, would the failure window disappear?

That reproduces the cessation/intervention job without requiring Buddhist provenance.

### Dependency analysis

Normal systems analysis already assumes that service behavior depends on configuration, credentials, caches, network state, authoritative state, and other components.

The target-side question "is this component really self-standing?" is therefore not distinct for this engineering target.

## Operation-by-operation comparison

| De-bound operation | Dependent-origination pass | Ordinary baseline | Residual target-side difference |
|---|---|---|---|
| condition-chain | expand symptom into upstream conditions | Five Whys / dependency graph / FTA | none |
| upstream-condition | continue beyond nearest symptom | RCA explicitly drills below symptoms | none |
| cessation-counterfactual | remove/change a condition and predict cessation | counterfactual/intervention test | none |
| intervention-point probe | find observable or modifiable condition | corrective-action / causal intervention design | none |
| dependency-reframing | reject self-standing component story | ordinary systems dependency analysis | none |
| anti-essentialist philosophical orientation | historically and philosophically distinctive | not required for engineering analysis | provenance / intellectual orientation, not a new target-side operation |

## Near-neighbor boundary — Paṭṭhāna

The Paṭṭhāna research candidate asks a different question:

> are several dependencies operating through different relation modes, converging or fanning out in ways that one chain hides?

That distinction is meaningful at the framework level. However, Paṭṭhāna must itself beat ordinary typed dependency graphs / fault trees before runtime promotion.

A cultural framework being distinct from another cultural framework does not establish product value.

## Result

For this SIer target, the matched engineering baseline reproduces the de-bound dependent-origination **capability**.

The framework pass is coherent and useful, but once upstream-condition search, branching preconditions, dependency analysis, and intervention testing are already selected, ordinary engineering methods can represent those jobs directly.

This file therefore establishes capability overlap. It does **not by itself** establish that the same cognitive job would have been selected before framework contact.

## Runtime consequence

Do not use this file alone to justify runtime demotion.

The missing ex-ante selection question is evaluated separately in:

- `research/framework-candidates/comparisons/dependent-origination-discovery-value.md`

That retrospective comparison finds that ordinary post-incident practice already asks for contributing components / conditions / actions / events, deeper causes, mitigations, preventive actions, and evidence-backed corrective changes before dependent-origination contact.

Under the revised discovery-aware standard, the combined evidence confirms the existing runtime demotion.

## Product-value consequence

This matters because dependent origination has been an easy framework for the model to select.

Where both capability overlap and discovery overlap hold, keeping a culturally marked default adds selection bias and context without opening a new target-side cognitive job. Preserving the sourced research candidate while keeping it out of general runtime is therefore the lower-overhead product choice for the tested SIer incident family.

## Ordinary-baseline references

- ASQ, Five Whys and Five Hows: https://asq.org/quality-resources/five-whys
- NASA Software Engineering Handbook, Software Fault Tree Analysis: https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695720/8.07%2B-%2BSoftware%2BFault%2BTree%2BAnalysis
- Stanford Encyclopedia of Philosophy, Counterfactual Theories of Causation: https://plato.stanford.edu/entries/causation-counterfactual/
