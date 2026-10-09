# Catuṣkoṭi non-activation example

Status: negative example / runtime requalification support

## Target

A rollout system already stores status per deployment unit using an explicit state model:

- planned;
- in-progress;
- complete;
- failed;
- not-applicable.

Every unit has:

- a scope identifier;
- transition rules;
- completion criteria;
- an explicit aggregation rule for the program dashboard.

The dashboard can show mixed unit states without forcing one Boolean value.

## Why catuṣkoṭi should not be activated

The target already preserves the distinctions that a four-corner probe would otherwise reveal:

- different scopes can have different states;
- mixed state is explicit;
- not-applicable is explicit;
- the predicate is defined at the correct level;
- aggregation does not overwrite unit-level truth.

Running P / not-P / both / neither would only rename an existing state model.

## Correct CSW result

Use the target's state model and aggregation rules directly.

Do not activate catuṣkoṭi merely because a target contains yes/no values or several status states.

Reopen it when the framing itself collapses incompatible scopes or leaves no place for an inapplicable / category-error residual.

## Boundary

Non-activation does not imply that catuṣkoṭi is reducible to a software enum.

It means only that the current target has already performed the de-bound binary-frame and predicate-audit work.
