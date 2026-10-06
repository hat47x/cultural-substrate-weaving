# Dependent origination target-return example

Status: runtime requalification / same-target fixture

## Target

A distributed job-control service intermittently accepts work but fails to complete it after a rolling deployment.

The first incident summary says:

> An expired worker credential caused the failure.

Target evidence also shows:

- the scheduler can retain cached worker capability for a short time;
- heartbeat freshness affects whether the worker remains eligible;
- the worker request is rejected when the credential is invalid;
- the authoritative state store rejects stale revisions;
- queue delivery can recur independently of authoritative attempt state.

## Framework contact

A dependent-origination pass starts from the visible failure and moves upstream.

One plausible chain is:

```text
attempt fails
  <- worker request rejected
  <- unusable worker was selected
  <- scheduler still treated worker as eligible
  <- cached capability / heartbeat state had not yet reflected credential change
```

The pass then asks the cessation-side question:

> If stale eligibility and capability state are removed promptly when credential state changes, does the observed failure window cease?

This produces useful intervention questions:

- invalidate or version worker capability when credential state changes;
- separate scheduling eligibility from execution authentication;
- test the short interval where heartbeat remains fresh while credential validity has changed;
- verify that a stale queue delivery cannot overwrite a newer authoritative revision.

## Target return

The useful result is not the Buddhist chain itself.

The surviving target-side material is:

- an explicit upstream condition sequence;
- one or more intervention points;
- expected observations after intervention;
- evidence requests for every proposed dependency.

The incident summary becomes more precise than "expired credential was the root cause."

## Limitation exposed by the same target

The target also contains branching and differently typed dependencies.

A single chain does not naturally preserve that:

- heartbeat freshness and capability cache can jointly affect eligibility;
- authoritative revision constrains state transition through another path;
- queue redelivery is a later opportunity rather than the same kind of prerequisite.

For this reason, a chain-oriented pass is not sufficient evidence that dependent origination is the best framework for the target.

The ordinary-baseline and Paṭṭhāna comparisons must be read beside this fixture.
