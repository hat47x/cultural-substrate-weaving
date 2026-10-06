# Aristotle's four causes vs ordinary systems / design review

Status: runtime requalification / same-target ordinary-baseline comparison

## Purpose

Aristotle's four causes is currently a default runtime framework and the typology notes that it is one of the model's default picks.

This comparison asks:

> after de-binding, does the framework add a target-relevant cognitive operation that strong ordinary systems engineering and design review do not already provide?

The target is the same multi-tenant API rate limiter used in the positive fixture.

## Condition A — four-causes-derived pass

The de-bound pass separates:

1. resource/material constraints;
2. organization / architecture / algorithm;
3. process, event, actor, or mechanism that produces change;
4. documented purpose / end;
5. gaps caused by collapsing those explanation jobs into one "cause."

For the rate limiter, this yields questions about Redis/network constraints, token-bucket structure, refill/configuration mechanisms, and backend-protection/fairness objectives.

## Condition B — strong ordinary systems-engineering baseline

NASA's system-design process already separates several target-side concerns.

### Stakeholder expectations and objectives

Ordinary review asks:

- who needs the system;
- how it is intended to be used;
- what mission or operational objective defines success;
- what constraints and design drivers matter.

This reproduces the de-bound purpose/end question without importing final causality.

### Technical requirements and constraints

Ordinary review identifies measurable requirements and constraints.

For the target this includes:

- latency;
- capacity;
- resource limits;
- deployment environment;
- consistency and availability constraints.

This reproduces the resource/material-side questions relevant to an engineered system.

### Logical decomposition / architecture

Ordinary review separates functions and architecture before choosing or validating a design solution.

For the target this exposes:

- tenant-keying model;
- token-bucket structure;
- refill logic;
- shared-state boundaries;
- responsibility allocation.

This reproduces the structure/form-side questions.

### Design solution / behavior / mechanism

Ordinary review examines how the design behaves and whether it meets the requirements and stakeholder expectations.

For the target this includes:

- request arrival;
- token consumption;
- refill timing;
- configuration rollout;
- concurrent updates;
- stale state and failure mechanisms.

This reproduces the efficient/change-source question.

## Operation-by-operation comparison

| De-bound operation | Four-causes pass | Ordinary baseline | Residual target-side difference |
|---|---|---|---|
| why-splitting | separate resource, structure, mechanism, purpose | separate expectations, constraints, architecture, behavior | none |
| explanation-gap | ask which explanatory mode is absent | requirements/design review exposes missing objective, constraint, architecture, or behavior | none |
| causal-category-audit | stop mixing purpose, mechanism, structure, resource | ordinary SE artifacts already assign these to different review objects | none |
| multi-cause-composition | allow complementary explanation types | recursive consistency across expectations, requirements, architecture, design | none |
| artifact-design-probe | inspect material/form/process/end | standard artifact design review | none |
| Aristotelian explanatory vocabulary | historically distinctive | absent | provenance / education, not a new target-side operation |

## Important non-equivalence

This comparison does **not** claim that modern stakeholder objectives are literally Aristotle's final causes, or that technical constraints are philosophically identical to material causes.

The claim is narrower:

> after de-binding for the tested SIer use, the target-side questions are already supplied by ordinary engineering practice.

Historical conceptual non-equivalence can remain even when runtime cognitive output is redundant.

## Result

For this target, the ordinary-baseline counter-hypothesis survives.

The framework is an elegant compact reminder that explanations differ in kind, but standard systems/design review produces the same concrete questions without cultural-framework selection.

## Runtime consequence

The current evidence does not support keeping Aristotle's four causes as a general default runtime framework for SIer artifact/design analysis.

Preserve the profile, source basis, target-return fixture, selection cues, typology mapping, and explicit Aristotle/comparative-philosophy use.

## Product-value consequence

Because the framework is also easy for the model to select, retaining it despite ordinary-baseline equivalence adds selection bias and portfolio complexity without increasing target-side cognitive capability.

## Ordinary-baseline references

- NASA Systems Engineering Handbook, System Design Processes: https://www.nasa.gov/reference/4-0-system-design-processes/
- NASA Systems Engineering Handbook, Stakeholder Expectations Definition: https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/
