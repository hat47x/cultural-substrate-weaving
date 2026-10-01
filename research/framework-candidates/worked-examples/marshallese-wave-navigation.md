# Worked example — Marshallese wave-navigation operations after de-binding

Status: research-only / target-return example / not a cultural simulation

## Purpose

This example tests whether the candidate still contributes a distinctive cognitive operation after island / swell / canoe vocabulary is removed.

It does **not** simulate Marshallese navigation. It uses only the de-bound operations documented in the candidate profile:

- relative-route model;
- cue-sequence wayfinding;
- model / environment return;
- disturbance-as-signal;
- embodied / abstract complementarity translated to model / situated observation.

## Target

A distributed data-processing incident has incomplete global observability.

Known observations:

- O1: jobs entering queue Q-A complete normally.
- O2: after handoff to service S-B, retry counts begin to oscillate.
- O3: downstream service S-C sometimes receives work, so the route is not completely broken.
- O4: the topology diagram says S-B should call S-C directly.
- O5: live traces show an intermediate proxy P-X on some requests.
- O6: latency spikes become stronger when requests pass through one deployment zone.
- O7: no evidence yet proves that P-X or the zone causes the retries.

The ordinary temptation is to rebuild a complete global dependency graph immediately and search for a single broken edge.

## Operation 1 — relative-route model

Instead of requiring a complete topology, record only relations currently supported by the incident evidence.

```text
Q-A
  -> S-B
  -> [sometimes P-X]
  -> S-C

observed disturbance:
  retry oscillation begins after S-B
  latency disturbance strengthens in one deployment zone
```

This is not yet a causal graph.

### target-return check

- Q-A → S-B is supported by traces.
- P-X is present only on some observed paths.
- S-B → S-C remains partly successful.
- “P-X causes retry” is **not** supported.

The operation adds value because it permits useful route work without pretending that the full topology is known.

## Operation 2 — cue-sequence wayfinding

Define local cues that would justify moving the investigation one step farther.

```text
cue A:
  retry oscillation appears after S-B

if cue A:
  inspect whether P-X is present on the same request

cue B:
  P-X present

if cue B:
  compare zone and latency pattern

cue C:
  same retry pattern without P-X

if cue C:
  weaken the P-X hypothesis and reopen S-B / zone boundary
```

The “route” here is an investigation sequence, not a claim about causation.

### target-return check

Each cue is observable in target logs/traces. If a cue does not appear, the next step is not licensed by the framework alone.

## Operation 3 — model / environment return

The architecture diagram is a preparatory model. The live trace is situated evidence.

Difference:

```text
model:
  S-B -> S-C

live observation:
  S-B -> P-X -> S-C on some requests
```

The framework contribution is to keep these two layers separate rather than forcing the live evidence back into the cleaner architecture diagram.

### target-return check

- The diagram remains useful as intended topology.
- The trace remains evidence of actual execution.
- Neither layer automatically invalidates the other.
- The mismatch becomes a question: under what conditions is P-X inserted?

## Operation 4 — disturbance-as-signal

The stronger latency oscillation in one zone may contain location information.

Generated question:

> Does the disturbance become stronger at the same route boundary across independent requests, or is the correlation incidental?

This is deliberately weaker than:

> The deployment zone causes the incident.

### target-return check

Compare independent requests and zones. If the pattern does not replicate, withdraw the location hypothesis.

## Operation 5 — local update instead of total remap

Suppose a new trace shows that P-X also appears on successful requests.

Do **not** rebuild the whole incident theory. Update only the local route segment:

```text
before:
  P-X was a possible discriminator

after:
  P-X presence alone is insufficient
  reopen:
    S-B state
    zone boundary
    retry timing
```

This is the closest analogue to local cue-based route correction.

## What this candidate adds beyond a generic graph

A graph can draw Q-A, S-B, P-X, and S-C.

The candidate adds a stronger procedural distinction:

1. incomplete relative route is still usable;
2. a preparatory model is not the same thing as live evidence;
3. local cues determine what to inspect next;
4. a disturbance may be informative without being causal;
5. new evidence can update a local segment without forcing total remapping.

If these five distinctions are removed, the candidate collapses to generic graph reasoning and should not be retained as an independent framework.

## Cultural boundary check

Nothing in the target output claims:

- that the software system is “like the Marshall Islands”;
- that traditional wave patterns map onto latency metrics;
- that public stick-chart descriptions reproduce navigator knowledge;
- that the cultural tradition validates the incident hypothesis.

The cultural framework only supplied a temporary generator for route/cue/model-return questions. All retained claims are target-side observations or explicitly marked hypotheses.

## Result

The profile passes this first target-return test provisionally.

It contributes more than “draw a network” because **relative route + cue sequence + model/environment return + disturbance-as-signal** survive de-binding.

This does not justify runtime adoption yet. A second comparison against another non-medical wayfinding tradition is still required to test whether these operations are Marshallese-specific enough to preserve as an independent candidate rather than a generic method.
