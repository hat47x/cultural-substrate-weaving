# What the caller supplies

## What this skill provides

cultural-substrate-weaving provides two capabilities: **structure candidates from cultural frameworks** and **KJ-method integration/gap discovery**.

It does not replace the domain expertise or domain-specific skills required for writing, management, software engineering, law, or other fields. Domain accuracy, quality criteria, implementation practice, and output form belong to the caller's context or to a companion domain skill.

## Recommended combination

```text
[Target and material]
Provide the target, sources, and constraints.

[Domain baseline]
First analyze with the domain skill or ordinary domain method.

[Role of cultural-substrate-weaving]
Use cultural frameworks and KJ integration to search for questions, relations, states, transitions, gaps, and compositional candidates absent from the baseline.

[Purpose-specific exit]
For research and diagnosis, validate candidates against professional knowledge, sources, standards, and operating conditions before treating them as findings about the target. For generation and composition, framework-generated structure may be adopted as a compositional resource, but it remains distinct from facts about the target.
```

Where multiple skills can be used, prefer **domain skill + cultural-substrate-weaving**, not replacement of the domain skill.

## Suitable problems

- open problem spaces whose destination is itself unsettled;
- heterogeneous material, actors, time scales, and relations;
- situations where ordinary analysis has converged on one path and another search direction may matter; and
- tasks where candidates can be validated against target-side evidence or conditions for research and diagnosis, or retained with provenance as compositional resources for generation and composition.

## Unsuitable problems

- closed problems whose candidates can be enumerated;
- simple proofreading, translation, calculation, or format conversion;
- bounded local bugs and known procedures; and
- research or diagnostic tasks that require findings about the target but provide no material capable of validating structural hypotheses.

## Taiheki

Taiheki remains as a special case. It is not activated merely because a human appears. Use it only on explicit request or when bodily consistency and tension/relaxation responses are themselves the inquiry. It is a cultural/body-oriented external type, not a diagnosis or fact about personality.

## Validation status

The published v0.4.0 method is being observed prospectively in real work through the Web Chat Living Lab. Use `natural_work` by default so the real task is not stopped for experimental formality. Use `paired_check` only when a method-change decision, harm check, important regression check, or another need for stronger comparison makes it useful to compare a domain baseline with the same task plus CSW.

When no cultural framework was opened, record `activation_scope: non_activation` as the state that was actually observed in that round. Do not infer from that state alone that non-activation was useful, preferable, or avoided harm. If an assessment or interpretation also needs to be preserved, keep it separate from the observed state and retain enough provenance to identify who made the judgment and what it relied on.

Public observations are still limited, so the effectiveness of the skill is not treated as established at this stage. See **[Web Chat Living Lab](experiments/web-chat-living-lab.md)** for the operating protocol.
