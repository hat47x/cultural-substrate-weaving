# Huayan discovery-value comparison

Status: runtime requalification / discovery-value comparison

## Purpose

Separate:

1. **capability overlap** — can a specialist method reproduce the operation after it is known?;
2. **discovery value** — would ordinary analysis have selected that operation before framework contact?

## Fixed target

> Identity, Billing, Support, and Analytics duplicate Account data. Create one canonical Account service.

## Ex-ante generic architecture baseline

A strong generic review naturally examines:

- ownership;
- duplicated fields;
- APIs;
- consistency;
- latency and availability;
- migration;
- security;
- failure domains;
- cost.

A plausible result is:

> centralize common Account data and leave extension fields to consumers.

That can be coherent while still assuming one underlying Account identity.

## Huayan contact

Huayan injects a different question:

> If this part is removed from its current whole and placed in another, is it still the same part in the relevant sense?

This exposes authentication Account, payer Account, support-relationship Account, and analytical grouping Account as potentially different role-defined identities despite a shared label.

The integration-with-difference pass then asks:

> Which differences must remain explicit even if identification or transport is centralized?

## Post-contact specialist baseline

Once context-sensitive identity is visible, bounded-context DDD becomes an obvious specialist tool.

The provenance sequence is:

```text
generic architecture review
  -> canonical entity remains plausible
Huayan contact
  -> identity-across-wholes becomes explicit
  -> bounded-context DDD becomes the specialist validation/implementation method
```

If DDD had already been selected before contact, Huayan's discovery contribution would be smaller.

## Target-return residual

After removing Huayan vocabulary:

- Are the four Account identities actually the same domain object?
- Which attributes exist only because of context-specific roles?
- Can shared identification be separated from semantic authority?
- Which differences must remain after integration?
- What platform-wide dependency is created if semantic authority is centralized?

These questions survive target return.

## Decision

For this target, specialist methods reproduce the capability but generic ex-ante analysis does not necessarily select the same cognitive job.

Huayan therefore retains a runtime contribution as a compact discovery move, not as a uniquely capable formalism or source of authority.

## Falsifier

Weaken this retention claim if natural-work evidence shows that generic CSW analysis routinely generates the same identity-across-context and difference-preservation questions without Huayan contact at comparable selection cost.
