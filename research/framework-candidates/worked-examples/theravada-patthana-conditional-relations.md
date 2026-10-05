# Theravāda Paṭṭhāna conditional-relations worked example

Status: hypothetical / research-only

## Target

A distributed job-control service intermittently accepts work but fails to complete it after a rolling deployment.

The first incident summary says:

> The root cause was an expired worker credential.

That statement is partly true, but it compresses several different operational dependencies into one linear cause.

Target-side evidence already shows:

- worker credentials expire and must be refreshed;
- scheduler instances cache worker capability for a short period;
- the state store rejects stale revisions;
- a queue delivery can be retried independently of authoritative task state;
- workers disappear from eligibility when heartbeats age past a threshold.

## Baseline problem

A simple chain can be written as:

```text
credential expires
  -> worker call fails
  -> attempt fails
```

This is useful but incomplete. It does not explain why only some attempts fail, why retries sometimes succeed, or why the symptom persists briefly after credential refresh.

## Framework contact

The Paṭṭhāna-inspired pass does not apply twenty-four historical condition labels.

It asks whether the target contains **different modes of conditioning** that converge on the same observable failure.

### C1 — credential validity → worker request accepted

Target-side relation hypothesis:

- mode: prerequisite / presence-like support;
- evidence: request logs show authentication rejection while the credential is expired.

### C2 — cached worker capability → scheduler chooses that worker

Target-side relation hypothesis:

- mode: persistence from an earlier observation;
- evidence: scheduler cache retains the worker briefly after its usable credential state has changed.

### C3 — current state revision → conditional transition succeeds

Target-side relation hypothesis:

- mode: concurrent state constraint;
- evidence: the authoritative store rejects transitions based on an old revision.

### C4 — recent heartbeat → worker remains eligible

Target-side relation hypothesis:

- mode: co-present eligibility condition;
- evidence: eligibility is recalculated from heartbeat age.

### C5 — queue redelivery → another attempt may be observed

Target-side relation hypothesis:

- mode: sequential opportunity, not authority;
- evidence: queue delivery can recur after the authoritative attempt state has already changed.

## Convergence

The incident is no longer represented as one root-cause chain.

The failure window appears when several conditions overlap:

- an expired or recently refreshed credential;
- stale capability information;
- an eligible-looking heartbeat;
- a revision race on authoritative state.

No single one of these is promoted to "the cause" merely because the framework asked for multiple relations.

## One-to-many probe

The same cached-capability condition also affects:

- scheduling choice;
- retry destination;
- operator-facing worker availability.

This suggests a common dependency worth inspecting, but each downstream relation still needs its own target-side evidence.

## Target return

The useful target-side results are concrete tests and design questions:

- invalidate or version capability cache when credential state changes;
- test the window where heartbeat remains fresh but credential validity has changed;
- verify that stale queue delivery cannot overwrite a newer authoritative attempt revision;
- distinguish "eligible for scheduling" from "authenticated for execution";
- document which state is authoritative when cache, heartbeat, queue, and store disagree.

The Pāḷi names and doctrinal ontology do not enter the final design record.

## Why this may add value beyond dependent origination

A condition-chain pass can expose upstream factors and cessation counterfactuals.

The extra candidate value here is that the failure is supported by **heterogeneous condition modes that converge and fan out**, and that a generic arrow would hide operationally different test obligations.

## Strong baseline challenge

An ordinary typed dependency graph or fault-tree analysis may produce the same distinctions.

The candidate earns further attention only if framework contact consistently opens additional target-supported relation-mode questions without adding more taxonomy overhead than value.
