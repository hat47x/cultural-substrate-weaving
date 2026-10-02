# Llull Ars target-return example

Status: hypothetical / runtime adoption support

A requirement review has three distinctions:

- actor: operator / automated job;
- data state: current / stale / missing;
- action: read / write / delete.

The existing discussion covers familiar paths such as operator × current × read and operator × missing × write. A late-Ars-inspired pass systematically crosses the distinctions and exposes combinations that ordinary discussion never placed together.

One generated combination is:

automated job × stale data × write.

The framework does not assert that this situation exists or is defective. It creates a target-return question:

- Can an automated job write while its input is stale?
- If the combination is impossible by design, where is that constraint documented?
- If it is possible, which existing requirement governs it?

The operation is useful when the combination survives target-side constraints and becomes a concrete question. Formal enumeration alone is not counted as a yield.
