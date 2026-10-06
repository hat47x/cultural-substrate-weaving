# Aristotle's four causes target-return example

Status: runtime requalification / same-target fixture

## Target

A multi-tenant API gateway uses a token-bucket rate limiter.

The limiter successfully protects the backend from overload, but premium tenants report that legitimate short bursts are rejected too aggressively after a configuration change.

The first explanation says:

> The bucket size is too small.

That statement may be relevant, but it mixes several explanatory jobs.

## Framework contact

### Resource / material-side question

What substrate or constraint makes the behavior possible?

Target-side candidates:

- Redis round-trip latency;
- timestamp precision;
- memory / key cardinality limits;
- network delay between gateway instances and shared state.

### Structure / form-side question

What organization makes this the limiter it is?

Target-side candidates:

- token-bucket algorithm;
- per-tenant keying;
- bucket capacity;
- refill-rate formula;
- distributed consistency model.

### Change-source / mechanism question

What actually produces the observed rejection pattern?

Target-side candidates:

- incoming request burst;
- refill calculation timing;
- configuration rollout;
- stale limiter state;
- concurrent gateway updates.

### Purpose / end question

What documented purpose is the design meant to satisfy?

Target-side objectives:

- protect the backend;
- preserve tenant fairness;
- allow contracted premium burst capacity;
- keep latency predictable.

## Target return

The useful result is not "the four causes explain the limiter."

The useful target-side questions are:

- is the premium burst objective explicit and testable?
- is the configured bucket capacity consistent with that objective?
- does the distributed refill mechanism behave as the architecture assumes?
- are Redis/network/timestamp constraints material to the observed rejection window?
- which trade-off was actually intended when backend protection conflicts with burst allowance?

These questions are concrete and useful.

## Requalification significance

The same target is re-read in the ordinary-baseline comparison.

If standard systems engineering already separates objectives, constraints, architecture, and behavior/mechanism and produces the same questions, the framework has not added a distinct runtime operation even though the pass itself was useful.
