# Aristotle's four causes discovery-value comparison

Status: retrospective runtime requalification / discovery-value comparison

## Purpose

The prior demotion established that a strong systems/design review can reproduce the de-bound four-causes operations after the explanatory jobs are named.

That is **capability-overlap** evidence.

This comparison asks the missing question:

> before four-causes contact, would ordinary design work naturally select purpose/objective, constraints/resources, logical structure, and behavior/mechanism as separate review jobs?

## Fixed target

A multi-tenant API gateway uses a token-bucket rate limiter.

The limiter protects the backend, but premium tenants report that legitimate short bursts are rejected too aggressively after a configuration change.

The first explanation says:

> The bucket size is too small.

## Ex-ante generic design baseline

Do not name Aristotle or the four causes.

Treat the target as an engineered system whose design must be reviewed.

Ask:

- What stakeholder outcomes and service commitments define success?
- Which requirements and constraints bound the design?
- What logical architecture / algorithm implements the limiter?
- How does the design behave under burst, refill, concurrency, stale state, and configuration change?
- Which concrete mechanism produces the observed rejection pattern?
- Which trade-off is intentional when backend protection conflicts with premium burst allowance?
- Which evidence or test validates each objective, constraint, structure, and behavior claim?

These questions arise directly from normal system-design work.

## Domain-standard selection path

NASA's current Systems Engineering Handbook organizes system design into four interdependent processes:

1. stakeholder expectations definition;
2. technical requirements definition;
3. logical decomposition;
4. design solution definition.

The stakeholder process establishes intended use and desired end states. Technical requirements capture measurable requirements and constraints. Logical decomposition creates functional / behavioral architecture. Design solution definition turns those into alternatives and a selected design whose behavior is validated against stakeholder expectations.

Sources:

- NASA Systems Engineering Handbook, System Design Processes:
  https://www.nasa.gov/reference/4-0-system-design-processes/
- NASA Systems Engineering Handbook, Stakeholder Expectations Definition:
  https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/
- NASA Systems Engineering Handbook, Logical Decomposition:
  https://www.nasa.gov/reference/4-3-logical-decomposition/
- NASA Systems Engineering Handbook, Design Solution Definition:
  https://www.nasa.gov/reference/4-4-design-solution-definition/

This does not make these modern categories identical to Aristotle's aitiai.

It shows that, for an engineered artifact, the target category itself selects multiple explanatory / design jobs before four-causes contact.

## Generic baseline on the fixed target

The design review naturally separates:

### Objective / purpose

- backend protection;
- premium burst entitlement;
- tenant fairness;
- latency predictability.

### Constraints / resources

- Redis latency;
- timestamp precision;
- memory / key cardinality;
- network delay;
- consistency and availability bounds.

### Logical structure

- token-bucket algorithm;
- per-tenant keying;
- refill-rate formula;
- shared-state boundary;
- concurrency model.

### Behavior / mechanism

- request arrival;
- token consumption;
- refill timing;
- config rollout;
- stale limiter state;
- concurrent gateway updates.

The initial "bucket size is too small" statement is therefore expanded without requiring four-causes contact.

## Four-causes contact

The de-bound pass asks:

- what resource/material constraints matter?;
- what structure/form makes this the artifact it is?;
- what process or mechanism produces the relevant change?;
- what documented purpose or end is being served?;
- which explanation type is missing or being mixed with another?

These remain coherent and useful questions.

## Ex-ante comparison

| Cognitive job | Generic / ex-ante design review | Four-causes contact | Incremental discovery |
|---|---|---|---|
| identify intended outcome | stakeholder expectations / success criteria | final-cause-side question | low |
| identify constraints/resources | technical requirements and constraints | material-side question | low |
| identify structure/organization | logical decomposition / architecture | formal-side question | low |
| identify producing behavior/mechanism | design solution / behavior / failure review | efficient-side question | low |
| expose explanation gap | missing objective / constraint / architecture / behavior appears as incomplete design record | explanation-gap | low |
| preserve complementary explanations | systems design requires consistency across all design artifacts | multi-cause composition | low |
| distinguish historical explanatory categories | not an engineering requirement | Aristotelian provenance | historical / educational residue |

## Target-return residual

After removing Aristotelian vocabulary, the useful questions are:

- What objective is the limiter required to satisfy?
- Which constraints make the current behavior possible?
- What architecture or algorithm defines the limiter?
- What mechanism produces the observed rejection pattern?
- Which trade-off was intended?
- Which review dimension is missing from the design record?

These are valuable, but for the tested artifact they are already opened by ordinary ex-ante systems/design practice.

## Discovery-value result

The discovery-value counter-hypothesis survives.

Unlike classical stasis theory, where the generic target does not itself demand issue-type discrimination, an engineered artifact is ordinarily reviewed through goals, requirements/constraints, logical structure, design solution, and behavior.

The modern design taxonomy is not Aristotle's four causes. Historical conceptual non-equivalence remains important.

But CSW runtime value is judged by the target-side cognitive job after de-binding. On this tested SIer design target, the same jobs are selected before four-causes contact.

The strongest remaining value is a compact philosophical reminder that "why" can have multiple senses, plus historical and educational value.

## Runtime consequence

The existing operational demotion is **confirmed under the discovery-aware standard**.

Combined evidence now shows:

- matched systems/design review reproduces the capability;
- generic ex-ante design work naturally selects objective, constraint, structure, and behavior/mechanism review;
- no additional target-side discovery survives at comparable selection cost;
- near-neighbor distinctness from dependent origination does not create runtime value.

Preserve Aristotle's four causes as a sourced research candidate for explicit Aristotle, history of philosophy, comparative explanation, education, and future targets where a distinct discovery contribution can be demonstrated.
