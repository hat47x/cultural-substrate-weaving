# Catuṣkoṭi target-return worked example

Status: runtime requalification / same-target fixture

## Target

A migration dashboard requires one answer:

> Is the platform migration complete? Yes / No.

Target facts:

- the public read path is fully on the new platform;
- write processing still uses the old worker pool;
- one internal batch path is halfway through migration;
- the archival subsystem was explicitly excluded from the migration scope;
- the dashboard has only one Boolean field.

## Framework contact

Let P be:

> the platform migration is complete.

A catuṣkoṭi pass does not declare all four corners true.

It uses them as probes.

### P

Under the public read-path scope, the migration is complete.

### not-P

Under the write-processing scope, the migration is not complete.

### both

At the whole-program level, a single Boolean predicate collapses completed and incomplete subscopes.

The useful result is not a literal contradiction.

It is:

> different components satisfy opposite evaluations under one over-broad predicate.

### neither

For the archival subsystem, "migration complete / not complete" is not the right classification because that subsystem is explicitly out of scope.

The useful result is:

> the predicate does not apply to every item being grouped under "platform".

## Target return

After removing the four-corner vocabulary, the surviving work is:

- separate migration scope by component / path;
- distinguish in-scope complete, in-scope incomplete, mixed/partial, and out-of-scope;
- define what level the completion predicate applies to;
- replace the Boolean dashboard field if it erases material distinctions;
- state the aggregate completion rule explicitly if management still needs one summary status.

## Why this is useful

The framework does not solve the migration.

It reveals that the original yes/no question loses information before ordinary status aggregation begins.

The actionable product question becomes:

> What is the correct predicate and scope for reporting migration state?

## Boundary

If the dashboard already records component-level states, scope, not-applicable items, and an explicit aggregation rule, do not activate catuṣkoṭi merely to rename those states.
