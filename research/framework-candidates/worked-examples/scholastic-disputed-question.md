# Scholastic disputed-question worked example

Status: hypothetical / research-only

## Target

A team proposes a local-first embedded state store for the first release of a small distributed-compute control plane.

The proposal is plausible, but review comments are being collapsed into a generic "scalability concern".

## Framework contact

The disputed-question pass does not ask which medieval answer is correct. It externalizes one question and preserves distinct objections.

### Question

Can the first release safely use a single-node embedded relational state store while keeping a credible later multi-instance path?

### Objections

- **O1 — restart durability:** a local store is unacceptable if process restart can lose Task / Attempt identity.
- **O2 — concurrent authority:** a single-node design may hide assumptions that break when multiple control-plane instances issue conditional updates.
- **O3 — operational recovery:** local persistence may be technically durable but still hard to inspect, back up, or repair after corruption.
- **O4 — migration lock-in:** an implementation that leaks SQLite-specific semantics into Core contracts could make later replacement expensive.

These objections are not merged into one "database risk" item.

### Contrary consideration

The initial product scope does not require a distributed consensus database, and the architecture already calls for a replaceable State Store SPI. This is a target-side design constraint, not an appeal to scholastic authority.

### Determination candidate

Use an embedded relational reference store only if the implementation proves restart durability and conditional-update semantics through the SPI, keeps queue/delivery non-authoritative, and records an explicit replacement boundary.

### Pointwise replies

- **R1 → O1:** require a restart conformance test that recreates the adapter and verifies the same Task identity and revision.
- **R2 → O2:** do not claim multi-instance safety. Require compare-and-swap/revision semantics in the SPI and leave distributed coordination outside the first implementation claim.
- **R3 → O3:** still unresolved. Define inspection/export/backup evidence before calling the adapter operationally sufficient.
- **R4 → O4:** verify that external and Core contracts contain no SQLite-specific types, paths, SQL dialect, or transaction assumptions.

## Target return

The useful increment is not "the embedded store wins."

The target-side result is:

- one decision question;
- four non-equivalent objections;
- three bounded replies;
- one unresolved operational-recovery item;
- concrete tests or evidence needed for each objection.

The unresolved O3 remains visible. The method therefore prevents a fluent architectural determination from creating the appearance that every objection has been answered.

## Why this is distinct from nearby frameworks

- Stasis theory could classify parts of the dispute as factual, evaluative, or procedural, but does not itself require a reply to each objection.
- Nyāya could inspect the inference supporting "embedded is sufficient", but does not preserve four adversarial concerns as the organizing structure.
- Generic pros/cons could list the concerns, but the disputed-question operation specifically tests whether the final determination returns to each earlier objection.
