# Wuxing target-return example

Status: runtime requalification / same-target fixture

## Target

A distributed job-control platform scales workers from queue depth.

After a sudden traffic spike, the system oscillates instead of settling:

1. queue depth rises;
2. autoscaling adds workers;
3. backend load rises;
4. timeout and retry volume rise;
5. retries increase queue pressure;
6. admission throttling eventually reduces intake;
7. queue depth falls sharply;
8. the autoscaler removes workers;
9. the next retry wave raises queue depth again.

The first explanation is simply: “the autoscaler is unstable.”

## Wuxing-derived contact

Do **not** assign Wood, Fire, Earth, Metal, and Water names to target components.

De-bind the runtime operation into relation modes.

### Enabling / amplifying relations

Target-side candidates:

- queue depth -> worker scale-out;
- retry volume -> queue pressure;
- worker concurrency -> backend request volume;
- timeout -> retry volume.

### Constraining / counteracting relations

Target-side candidates:

- admission throttling -> new queue inflow;
- completed jobs -> queue depth;
- scale-in -> worker concurrency;
- retry backoff -> retry request rate.

### Loop questions

Potential reinforcing path:

```text
backend saturation
  -> timeout
  -> retries
  -> queue pressure
  -> scale-out
  -> backend request volume
  -> backend saturation
```

Potential balancing path:

```text
queue pressure
  -> admission throttling
  -> reduced inflow
  -> lower queue pressure
```

### Relation-role questions

Worker count is not intrinsically “supporting” or “constraining.”

- more workers can reduce queue depth;
- the same increase can raise backend contention;
- scale-in can protect the backend while worsening queue latency.

Its role depends on the relation and operating state.

## Target return

The useful questions are:

- which links amplify the oscillation?
- which links damp it?
- which damping link is too delayed or too weak?
- does retry behavior turn a balancing scale-out action into a reinforcing overload loop?
- which link changes between spike, recovery, and steady-state periods?
- which proposed edges are supported by telemetry or intervention tests?

These are useful target-side questions.

## Requalification significance

The same target is re-read in the ordinary-baseline comparison.

If signed causal-loop / system-dynamics analysis generates the same questions directly, Wuxing remains a useful historical substrate but does not add a distinct general runtime operation for this SIer target.
