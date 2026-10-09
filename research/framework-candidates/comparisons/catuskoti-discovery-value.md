# Catuṣkoṭi discovery-value comparison

Status: runtime requalification / discovery-value comparison

## Purpose

The capability comparison shows that ordinary state modeling and requirements review can represent the de-bound output after the binary-frame defect has already been recognized.

This comparison asks:

> before catuṣkoṭi contact, does ordinary requirements/project review naturally test both, neither, and predicate failure, or does it mostly try to make the original yes/no question clearer?

## Fixed target

A migration dashboard requires one answer:

> Is the platform migration complete? Yes / No.

Facts:

- public read path: complete;
- write processing: incomplete;
- internal batch path: partial;
- archival subsystem: explicitly out of scope;
- dashboard: one Boolean field.

## Ex-ante generic requirements / project baseline

Do not name catuṣkoṭi or multi-valued logic.

Use ordinary review questions:

- What does "complete" mean?
- What is the scope?
- Is the requirement/status clear and unambiguous?
- Is it stated at the correct level?
- Are there conflicting observations?
- Are all relevant components covered?
- Is there a measurable completion criterion?
- Are any conditions not applicable or "don't care"?
- What aggregation rule should management use?

NASA requirements guidance explicitly asks whether requirements are:

- clear and unambiguous;
- limited to one thought with one subject and predicate;
- complete;
- stated at the correct level;
- consistent and non-conflicting;
- explicit about "don't care" conditions where applicable.

Sources:

- NASA Systems Engineering Handbook, Appendix C — How to Write a Good Requirement:
  https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/
- NASA Software Engineering Handbook, Software Requirements Analysis:
  https://swehb.nasa.gov/spaces/7150/pages/16450593/SWE-051%2B-%2BSoftware%2BRequirements%2BAnalysis

This is a strong baseline.

It can eventually replace the Boolean with a better state model.

## Where the generic baseline tends to go

The ordinary review usually treats the problem as:

> make "migration complete" precise enough to produce one valid status.

That leads naturally to:

- define scope;
- define completion criteria;
- split components;
- choose an aggregation rule.

Those are useful corrections.

But the baseline does not structurally require the analyst to **inhabit the rejected corners before repairing the model**.

In particular, it does not force:

- "both" — where do P and not-P each appear to hold?;
- "neither" — where is the predicate inapplicable or category-defective?;
- "is P itself the wrong predicate at this level?"

## Catuṣkoṭi contact

The four-corner pass deliberately resists early repair.

With P = "the platform migration is complete":

- P finds scopes where completion holds;
- not-P finds scopes where it does not;
- both looks for mixed scope/time/layer that the Boolean erases;
- neither looks for out-of-scope material or predicate failure.

Only after those residuals are exposed does target return translate them into:

- component-level states;
- scope definitions;
- not-applicable states;
- revised predicates;
- explicit aggregation rules.

## Ex-ante comparison

| Cognitive job | Generic requirements/project review | Catuṣkoṭi contact | Incremental discovery |
|---|---|---|---|
| clarify P | strong | P / not-P framing | low |
| split scope / component | strong once ambiguity is recognized | both-probe often reveals need | moderate |
| represent not-applicable | available through N/A / don't-care | neither-probe | moderate |
| deliberately search for simultaneous P and not-P under hidden dimensions | not structurally required | both-probe | high |
| deliberately search for failure of the predicate itself | possible, but review often repairs definition instead | neither / predicate-audit | high |
| preserve residual before choosing a clean state model | not a default requirement | four-corner exploration | high |

## Discovery-value result

A distinct discovery contribution remains.

Ordinary requirements review has the **capability** to resolve the target once the Boolean defect is visible.

Catuṣkoṭi contributes an earlier exploratory move:

> before choosing a clearer definition, force the frame to confront the mixed and outside-category cases it currently cannot express.

That move can reveal which dimension or predicate must change.

The target-return value is not "both and neither are true."

It is:

- identify mixed scopes;
- identify inapplicability;
- expose the wrong aggregation level;
- replace or decompose the predicate only after the residual is visible.

## Non-activation boundary

Do not activate catuṣkoṭi when:

- the target already has an explicit state machine;
- mixed and not-applicable states are represented;
- scope and aggregation are explicit;
- the user needs a direct binary compliance result whose predicate and scope are already fixed.

Do not use "both" to preserve avoidable ambiguity, or "neither" to evade a required decision.

## Runtime consequence

Runtime retention is supported under the discovery-aware standard.

The reason is not unique four-valued capability.

The reason is the low-cost **binary-frame disruption** that exposes both/neither/predicate-failure residuals before ordinary modeling selects the final state representation.

Keep the historical and lineage boundaries intact: the runtime use is a de-bound exploratory probe, not a claim that Buddhist catuṣkoṭi is one modern four-valued logic.
