# Catuṣkoṭi vs ordinary state decomposition and requirements review

Status: runtime requalification / capability-overlap comparison

## Purpose

This comparison asks the capability question:

> once the binary-frame problem is already recognized, can ordinary requirements/state modeling reproduce the de-bound catuṣkoṭi output?

The discovery question is evaluated separately.

## Fixed target

A migration dashboard requires:

> Is the platform migration complete? Yes / No.

The target contains completed, incomplete, partial, and explicitly out-of-scope components.

## Catuṣkoṭi-derived pass

Using P = "the migration is complete", the de-bound pass asks:

- under what scope does P hold?;
- under what scope does not-P hold?;
- does "both" reveal mixed time, layer, actor, component, or definition?;
- does "neither" reveal not-applicable material or a missing category?;
- is P itself the wrong predicate at the current aggregation level?

## Strong ordinary baseline

Once the binary problem is already recognized, ordinary requirements/state review can:

- define scope and level;
- split one overloaded status by component;
- require one unambiguous interpretation;
- use an explicit multi-state model;
- represent not-applicable / don't-care conditions;
- define an aggregation rule;
- reject a Boolean field that cannot preserve required distinctions.

NASA requirements guidance explicitly asks whether a requirement is clear and unambiguous, expresses one thought, has one subject and one predicate, is stated at the correct level, is internally consistent, and makes "don't care" conditions explicit where applicable.

Sources:

- NASA Systems Engineering Handbook, Appendix C — How to Write a Good Requirement:
  https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/
- NASA Software Engineering Handbook, Software Requirements Analysis:
  https://swehb.nasa.gov/spaces/7150/pages/16450593/SWE-051%2B-%2BSoftware%2BRequirements%2BAnalysis

## Operation-by-operation comparison

| De-bound operation | Catuṣkoṭi pass | Ordinary state / requirements baseline | Residual capability |
|---|---|---|---|
| binary-break | open beyond P / not-P | replace Boolean with multi-state model | none |
| both-probe | inspect mixed scopes / times / actors | component/state decomposition | none |
| neither-probe | preserve outside-category residual | not-applicable / don't-care / missing state | low |
| predicate-audit | ask whether P applies at all | clarity / correct level / correct predicate | none |
| de-reification | stop treating opposition as one fixed object | revise model / split dimensions | low |

## Important non-equivalence

This comparison does not claim that catuṣkoṭi is a requirements-state taxonomy or that historical Buddhist uses are equivalent to software state modeling.

The product claim is narrower:

> after the framing defect is already identified, ordinary target-language modeling can represent the distinctions produced by the de-bound four-corner pass.

## Capability result

Capability overlap is strong.

Catuṣkoṭi does not need runtime retention because only it can represent mixed or inapplicable states.

The remaining question is discovery value:

> before the binary framing is recognized as defective, does ordinary review naturally open "both", "neither", and predicate failure, or does catuṣkoṭi expose that missing cognitive job?
