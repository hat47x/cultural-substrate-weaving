# Aristotle's four causes vs dependent origination

Status: runtime requalification / near-neighbor differentiation

## Purpose

Both frameworks can appear in response to a vague "why did this happen?" question, but they transform the question differently.

This comparison preserves that distinction while separating framework distinctness from runtime product value.

## Aristotle's four causes

Primary job:

> split one why-question into different kinds of explanation.

Typical de-bound distinctions:

- resource/material constraint;
- structure / organization;
- mechanism / source of change;
- documented purpose / end.

The operation is plural explanatory framing.

## Dependent origination

Primary job:

> move from an observed state toward the conditions under which it arises and ask what should change when conditions cease.

Typical de-bound distinctions:

- upstream condition;
- condition chain;
- cessation counterfactual;
- intervention point;
- dependency reframing.

The operation is conditional-chain analysis.

## Same target

For a rate limiter that rejects legitimate bursts:

### Four-causes pass

asks separately about:

- Redis/network/resource constraints;
- token-bucket architecture;
- refill/configuration mechanism;
- backend-protection and fairness objectives.

### Dependent-origination pass

would more naturally trace:

```text
burst rejected
  <- insufficient available tokens
  <- refill / bucket state
  <- prior request and timing conditions
```

and ask what intervention would stop the rejection pattern.

## Distinction

The framework-level difference is real:

- four causes pluralizes explanation types;
- dependent origination traces conditional dependence and cessation.

But runtime product value requires a second test.

Dependent origination has already been removed from default runtime because ordinary RCA / fault-tree / dependency analysis reproduced its tested SIer operations.

If ordinary systems/design review likewise reproduces the four-causes questions, then cultural distinctness between the two frameworks is not enough to retain either in default runtime.

## Decision boundary

Keep this comparison as provenance and selection research.

Do not use "different from another cultural framework" as evidence that a framework adds a unique operation beyond ordinary target-side analysis.
