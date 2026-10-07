# Huayan target-return example — canonical Account consolidation

Status: runtime requalification / same-target fixture

## Target

Identity, Billing, Support, and Analytics each have an object called `Account`. A platform initiative proposes one canonical Account service to reduce duplication and inconsistency.

## Generic architecture baseline

A competent first review asks about ownership, duplicate fields, APIs, consistency, availability, latency, security, migration, and failure domains.

That can still leave one assumption untouched:

> the four things called Account are instances of the same conceptual part.

## Huayan contact

### Whole-part reciprocity

Read Account as a part of each containing whole.

- Identity: authentication/security principal.
- Billing: contractual/payer relation.
- Support: service relationship and communication context.
- Analytics: grouping used for analysis, whose boundary may differ from operational ownership.

The question changes from "which system should own Account?" to "what makes this thing Account inside each whole?"

### Context-role re-identification

Move the proposed canonical Account into each context.

- credit hold is essential to Billing but not authentication identity;
- preferred contact channel matters to Support but not contractual identity;
- analytical grouping can conflict with legal billing ownership;
- lockout state should not redefine payer identity.

The shared label hid role-defined differences.

### Perspective-through-node

Read the platform from the proposed canonical Account service. Semantic changes now become platform-wide schema and availability changes.

Read again from Billing and Support. The same central object no longer has the same center of gravity.

### Integration-with-difference

Do not conclude "never integrate."

A target-side design can preserve:

- a stable cross-context identifier where justified;
- context-owned models/projections;
- explicit translation contracts;
- no claim that one canonical attribute set is semantically authoritative everywhere.

## Target return

The surviving questions are:

- Which Account attributes are truly cross-context?
- Which exist only because of a context-specific role?
- Is centralization about identity, transport, storage, or semantic authority?
- Which contexts must be allowed to disagree?
- What differences would be erased by one canonical model?

These are target-side architecture questions, not Huayan metaphysical claims.

## Result

Huayan changes the object of review from "how to centralize a duplicate entity" to "whether entity identity is stable across wholes."

Once that question is visible, bounded-context DDD is an appropriate specialist tool for implementing or validating the result.
