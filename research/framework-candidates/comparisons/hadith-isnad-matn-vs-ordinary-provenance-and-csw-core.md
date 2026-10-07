# Hadith isnād / matn vs ordinary provenance and CSW core

Status: runtime requalification / capability-overlap comparison

## Purpose

Hadith isnād / matn is one of the most product-relevant CSW frameworks because its de-bound structure resembles CSW's own provenance discipline.

That makes requalification more important, not less.

This comparison asks:

> once the hadith-derived jobs are known, can ordinary provenance modeling plus CSW's always-on core rules reproduce them?

## Fixed target

A policy sentence appears in:

1. meeting notes;
2. a later chat message;
3. a summary memo.

At first glance this can look like three confirmations.

Closer inspection shows:

- the chat quotes the meeting statement;
- the memo summarizes the chat;
- wording changes slightly in the memo;
- none of those transmission facts independently proves the policy proposition itself.

## Hadith-derived pass

The de-bound pass performs five jobs:

1. **transmission-content separation** — keep the proposition separate from the claimed path;
2. **branch-and-convergence comparison** — identify shared and independent-looking origins;
3. **attribution-path audit** — distinguish observed, asserted, missing, and reconstructed handoffs;
4. **content-variant comparison** — compare wording changes separately from path changes;
5. **provenance-content non-equivalence** — do not turn documented provenance into truth of the proposition.

## Ordinary provenance baseline

### W3C PROV

W3C PROV models entities, activities, agents, derivation, quotation, revision, alternate entities, and provenance bundles.

That is enough to represent:

- one document derived from another;
- one document quoting another;
- several revisions of a content entity;
- shared origins;
- responsibility and generation events;
- provenance of provenance.

Sources:

- W3C PROV Model Primer: https://www.w3.org/TR/prov-primer/
- W3C PROV Overview: https://www.w3.org/TR/prov-overview/

### C2PA provenance boundary

C2PA provides a current content-provenance example with an explicit epistemic boundary.

Its guiding principles say provenance assertions may be verifiably associated with an asset without the specification judging whether the provenance is "good" or "bad".

Its explainer states that provenance alone cannot determine whether digital content is true, accurate, or factual.

Sources:

- C2PA Guiding Principles: https://c2pa.org/principles/
- C2PA Explainer: https://c2pa.org/specifications/specifications/1.3/explainer/_attachments/Explainer.pdf

This reproduces the provenance-content non-equivalence job without hadith-specific categories.

## CSW always-on core baseline

CSW already requires, independently of any framework selection:

- judgment origin and source references to remain traceable;
- framework-generated material not to become target-supported without independent target-side support;
- the same source reposted or transformed into several artifacts not to count as independent support;
- evidence source independence to be separated from the path by which an insight was discovered;
- observations, recorded values, user judgments, and AI interpretations not to be conflated.

Relevant runtime core:

- `src/ja-JP/governance/governance-and-records.md`
- `src/ja-JP/core/cognitive-stance.md`
- `src/ja-JP/governance/evaluation.md`

For this target the core already asks the most important hadith-derived question:

> are these really independent supports, or several descendants of one origin?

It also prevents the second major error:

> documented provenance does not by itself make the proposition target-supported.

## Operation-by-operation comparison

| De-bound operation | Hadith-derived pass | Ordinary provenance + CSW core | Residual capability |
|---|---|---|---|
| transmission-content separation | matn vs isnād | content entity vs provenance graph / evidence state | none |
| branch-and-convergence comparison | compare chains | derivation / quotation graph + common-origin analysis | none |
| attribution-path audit | inspect each handoff | provenance edges with asserted / observed / reconstructed state | none |
| content-variant comparison | matn variants | revision / quotation / diff over content entities | none |
| provenance-content non-equivalence | chain strength != proposition truth | C2PA epistemic boundary + CSW target-support rules | none |
| religious / historical hadith method | tradition-specific | absent | provenance / historical residue only |

## Important non-equivalence

This comparison does **not** claim that:

- W3C PROV is a modern version of isnād;
- C2PA implements hadith criticism;
- classical narrator criticism is equivalent to software provenance;
- hadith authenticity judgments should be translated into generic trust scores.

The comparison is only about the target-side cognitive operations that remain after de-binding for CSW use.

## Capability result

For the tested target, ordinary provenance modeling and CSW's own always-on governance rules reproduce all current runtime operations.

The framework retains historical, religious, and comparative value, but it does not possess a target-side representation that the current product cannot otherwise express.

This establishes capability overlap only. Discovery value is evaluated separately.
