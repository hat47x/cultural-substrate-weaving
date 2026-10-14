# Jain sevenfold predication — target-return fixture

Status: hypothetical / same-target runtime requalification

## Fixed target A: platform migration

The dashboard asks: "Is the platform migration complete?" The public read path is migrated, write processing is not, a batch path is partial, and the archival subsystem is outside the declared scope.

The Catuṣkoṭi pass on this same target first tests whether a single binary predicate works: P, not-P, mixed cases, and inapplicability. The Jain-derived pass instead binds every subsequent assertion to the standpoint under which it can be made.

| Proposed statement | Explicit qualification | Target support or limitation |
|---|---|---|
| "Migration is complete" | for public reads as of the inspected deployment | read traffic and deployment records |
| "Migration is not complete" | for write processing at the same moment | old worker-pool records |
| "Migration is partly complete" | as a program-level summary across in-scope paths | aggregation rule must be specified |
| "Migration completion cannot be stated" | for archival paths that were excluded from migration | not unknown completion; predicate is out of scope |

The pass also asks which supposedly opposite claims share a referent, time, scope, and definition. It must not simply mark all viewpoints equally valid or invent one of seven target states.

## Fixed target B: service responsiveness

An incident brief claims: "The API is fast." Operations cites p95=120ms for internal requests; customer support cites p99=1.8s on a mobile-facing route. Both measurements are hypothetical fixture data, not facts about a real service.

A Jain-derived pass returns:

- performance is within the internal threshold **for** the internal route, metric, time window, and workload covered by that measurement;
- performance misses the customer-facing objective **for** the mobile route, p99, and measured window;
- neither measurement by itself justifies "the API is fast" across all users;
- a cross-route overall claim is unresolved until the target supplies an agreed metric and aggregation rule.

The supposed contradiction becomes a scope-and-metric comparison, not a philosophical decree.

## Target return

Replace framework vocabulary with a claim record containing: assertion, actor/standpoint, time, service or component, metric/definition, conditions, supporting evidence, and unresolved scope.

No evidence is upgraded by the framework; the two numeric observations remain fixture assumptions until verified against target records.

## Counter-hypothesis

Ordinary requirements validation and behavior-driven examples can already ask for each actor, metric, precondition, and expected observable result. See the ordinary and discovery-value comparisons.

This fixture shows coherent de-bound output. It does **not** by itself show an incremental discovery benefit or justify default runtime retention.
