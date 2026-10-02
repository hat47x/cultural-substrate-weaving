# Heavenly Stems / Earthly Branches candidate profile

Status: profile-ready / research-only / early-calendrical-layer-bounded

## Identity

- names: 天干地支, 十干十二支, Heavenly Stems / Earthly Branches, sexagenary cycle
- current scope: the ordered pairing of ten stems and twelve branches in early/historical calendrical and time-reckoning use
- intended CSW use: synchronized coupled cycles, partial/full recurrence, coordinate pairs, and unreachable pair-state probing
- not intended use: astrology, personality typing, medicine, Five-Phase correspondences, fortune telling, or later cosmological associations

## Source basis

### Historical calendrical scholarship

Cambridge University Press, “Evolution of the calendar in Shang China,” in *The Archaeology of Measurement*

https://www.cambridge.org/core/books/abs/archaeology-of-measurement/evolution-of-the-calendar-in-shang-china/C6465ACCE5ACC6D6EF27922B8665EAA4

Useful for the early calendrical/time-reckoning layer and for keeping the stem/branch system historically grounded rather than starting from later divinatory correspondence.

### History of Chinese astronomy and mathematics

Cambridge University Press, *Astronomy and Mathematics in Ancient China* — excerpt

https://assets.cambridge.org/97805210/35378/excerpt/9780521035378_excerpt.pdf

The source describes the ten-sign stem cycle and twelve-sign branch cycle used in calendrical reckoning.

The runtime candidate does not rely on later zodiacal or medical interpretation.

## Structural core

Two ordered cycles advance together:

- a ten-position stem cycle;
- a twelve-position branch cycle.

A joint state is the pair at one step.

Because both advance synchronously, the joint state repeats after the least common multiple of 10 and 12: 60 steps.

This is **not** the full Cartesian product of 120 pairs. The shared divisor means only a constrained subset of pair states is reached under synchronous advancement.

That unreachable-state property is the main structural contribution beyond generic coupled-cycle reasoning.

## Native operation candidates

### synchronized-cycle-pairing

Represent one state as the simultaneous coordinate of two cycles that advance together.

### coordinate-pair

Keep both coordinates visible instead of replacing the joint state with one opaque label.

### partial-vs-full-recurrence

Distinguish recurrence of one coordinate from recurrence of the complete pair.

### recurrence-distance

Compute or reason about when the full joint state returns.

### unreachable-pair-state-probe

Ask which apparent cross-product combinations can never occur when the two cycles are phase-locked and advance synchronously.

### phase-offset

Inspect how one coordinate changes while the other has already repeated.

## Target-return questions

- Are two periodic coordinates advancing together or independently?
- When one coordinate repeats, what remains different on the other?
- What is the full joint recurrence distance?
- Is the analyst assuming every pairwise combination is reachable?
- Which states are impossible under the target's coupling rule?
- Would allowing independent advancement change the reachable state space?
- If stem/branch vocabulary is removed, does constrained coupled-cycle reasoning remain useful?

## Near-neighbor differentiation

### Stems / Branches vs Maya coupled calendars

Both supply coupled-cycle reasoning.

The distinctive CSW contribution here is that cycle lengths 10 and 12 share a divisor, so synchronized advancement reaches a constrained 60-state subset rather than all 120 mathematical pairings.

By contrast, a coprime pair of cycles can traverse the full Cartesian combination set before joint recurrence.

### Stems / Branches vs Wuxing

Wuxing supplies relational generation/constraint cycles. Stems/Branches here supply coordinate recurrence mechanics, not causal or relational roles.

### Stems / Branches vs generic least-common-multiple calculation

The candidate is useful only when the target truly has two synchronized periodic coordinates and the reachable/unreachable pair distinction matters. A bare arithmetic exercise is not a cultural-framework yield.

## Historical / lineage boundary

- Keep early calendrical/time-reckoning mechanics separate from later astrology, zodiac animals, medicine, divination, and personality systems.
- Do not import Five-Phase, yin-yang, Na-yin, Four Pillars, or other later correspondences into this candidate.
- Do not treat all East Asian historical uses as one invariant Chinese system.
- The mathematical 60-step recurrence does not imply any target-side cultural meaning.

## De-binding route

1. remove stem and branch names from the target-facing result;
2. identify the two target-owned periodic coordinates;
3. verify whether they really advance synchronously;
4. compute/inspect partial and full recurrence;
5. mark unreachable pair states only if the target coupling rule supports them;
6. reject the framework when the two cycles can advance independently or when no coupled recurrence exists.

## Profile-ready decision

The candidate now has a bounded early-calendrical layer, distinct synchronized-cycle operations, an explicit non-overlap condition against Maya calendars, target-return questions, de-binding, and positive/negative examples.

It remains outside runtime until actual target use shows that unreachable-pair-state probing adds enough beyond generic modular arithmetic to justify adoption.

Worked examples:

- `research/framework-candidates/worked-examples/heavenly-stems-earthly-branches.md`
- `research/framework-candidates/worked-examples/heavenly-stems-earthly-branches-negative.md`
