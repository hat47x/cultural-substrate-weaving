# Nyāya five-member inference non-activation example

Status: negative example / runtime requalification support

## Target

An incident-analysis record already stores the causal claim as:

- claim: configuration revision R caused the batch failure;
- observation: failures began after R;
- proposed rule: under condition C, R produces state S;
- supporting comparison: a controlled reproduction shows R + C -> S;
- target application: the failed batch had condition C;
- counterexample search: batches with R but without C do not fail;
- intervention: reverting R removes S;
- evidence links: every step points to logs, experiment output, or configuration history.

## Why Nyāya should not be activated

The target already externalizes the de-bound cognitive jobs:

- thesis and reason are separate;
- the general relation is explicit;
- supporting and disconfirming cases are recorded;
- application to the current target is a separate step;
- the final claim is linked to target-side evidence and intervention.

Reformatting the same record as five members would add historical vocabulary without opening a new question.

## Correct CSW result

Use the existing causal argument record.

Do not activate Nyāya merely because a claim has a reason or because an incident has a suspected cause.

Reopen the framework when a fluent claim jumps from one observation or analogy to a conclusion without making the warrant and its application inspectable.

## Boundary

Non-activation says nothing against Nyāya's historical or philosophical importance.

It means only that this target has already done the de-bound inferential-bridge work directly.
