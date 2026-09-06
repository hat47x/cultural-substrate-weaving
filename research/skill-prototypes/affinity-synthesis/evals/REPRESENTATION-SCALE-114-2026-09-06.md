# Affinity Synthesis Representation Scale Test — 114 cards

Date: 2026-09-06
Status: research evaluation note

## Purpose

Test whether the representation layer can carry a real-task-sized affinity synthesis without forcing all cards into one unreadable diagram.

This evaluation used a 114-card / 10-leaf-group working structure from a private project artifact for the semantic dry run. Raw project card text is intentionally **not copied into this repository**. A structurally matched synthetic fixture can be generated with `scripts/generate_large_fixture.py`.

## Observed real-task structure

The inspected working artifact had:

- 114 cards
- 10 leaf groups
- leaf group sizes: `14, 20, 8, 9, 10, 18, 11, 7, 13, 4`
- every card placed exactly once as a direct member of one leaf group in that round
- two higher-order series in its provisional A-type structure
- two important leaf groups that connected or constrained the two series rather than fitting cleanly inside either series
- one provisional whole-synthesis label above them

For representation testing this was modeled as:

```text
114 cards
  ↓
10 leaf groups
  ↓
2 higher-order series + 2 direct connector/constraining groups
  ↓
1 root group
```

The point of this model is not to canonize that project structure. It is to test recursive grouping and projection behavior on a structure that actually occurred in practice.

## Validation result

A local `affinity-map` representation of the real-task structure contained:

- 114 cards
- 13 groups total (10 leaf + 2 series + 1 root)
- 10 explicit semantic relations
- 3 narrative audit units
- 1 root

`validate_map.py` reported:

```text
Affinity map semantic validation passed (0 warning(s))
```

Direct leaf-card membership count:

```text
114 cards × exactly 1 direct leaf membership
```

Higher-order groups contain lower groups, not duplicate copies of their cards. This avoids turning recursive grouping into false repetition.

## Projection size comparison

Using the same semantic record:

| Projection | Approx. generated Mermaid source lines | Observation |
|---|---:|---|
| hierarchy overview + explicit relations | 41 | readable as group-level structure; cards remain collapsed |
| narrative lineage, groups collapsed | 49 | lineage remains inspectable without enumerating 114 cards |
| one large leaf-group detail with cards + source | 64 | practical for local return-to-source inspection |
| narrative lineage, all 114 cards expanded | 372 | too dense for ordinary human overview; useful only as machine/audit output |

Line count is not a method metric. It is used here only to make the visual-density difference concrete.

## Finding 1 — recursive grouping is necessary

A flat `group -> cards` model cannot represent the actual move from leaf islands to higher-order series and then to a whole provisional label without inventing a separate, disconnected structure.

Allowing `group.members` to contain lower groups preserves the same integration grammar across granularity:

```text
card → group → higher group
```

The validator therefore allows recursive grouping but rejects membership cycles.

## Finding 2 — connector groups must not be forced into a series

The real-task A-type structure contained important groups whose function was to connect or constrain the two main series. Forcing them into either series would make the hierarchy look cleaner at the cost of changing the meaning.

The representation therefore allows a root group to contain:

```text
root := {series_1, series_2, connector_group_1, connector_group_2}
```

This is preferable to requiring all leaf groups to have the same depth.

## Finding 3 — overview and audit need different zoom levels

A single full map is not the standard output for 100+ cards.

Recommended projection pattern:

1. **overview** — higher groups, leaf groups, explicit relations; show card counts only.
2. **island detail** — open one leaf group and its cards/resonances.
3. **focused lineage** — trace one relation, narrative, residual, or question backward; collapse cards by default.
4. **full lineage** — expand all cards/source refs only for machine audit or a deliberately narrow review.

This follows the representation rule:

> preserve the full semantic record, but thin the current visual attention.

## Finding 4 — B-type prose needs its own lineage handles

The earlier interchange format could carry cards, groups, relations, residuals, and questions but not a separately addressable piece of narrative synthesis.

The schema now permits optional `narratives` entries with:

- stable ID
- canonical text
- optional display label
- basis refs
- state
- optional inherited / emergent / residual transformation audit

A narrative unit is not required to be one sentence or one atomic claim. It is a practical return-to-map audit unit.

## Finding 5 — full lineage should not be the visual default

Expanding 114 cards and their source links creates a graph whose completeness is useful for machine checking but whose visual density hides the very structure the diagram is meant to reveal.

Therefore no Method Definition rule such as `maximum 20 cards` is introduced. Instead the realization chooses a projection based on the review question.

## Public regression fixture

The repository does not store the private 114 project cards.

To reproduce the structural load:

```bash
python scripts/generate_large_fixture.py -o /tmp/large-114.json
python scripts/validate_map.py /tmp/large-114.json
python scripts/render_hierarchy.py /tmp/large-114.json -o /tmp/large-114-hierarchy.mmd
python scripts/render_lineage.py /tmp/large-114.json --focus N001 --detail groups -o /tmp/large-114-lineage.mmd
```

The generator preserves only the structural group-size distribution and recursive shape needed for the scale test.

## Current conclusion

The representation layer should not optimize for a single universal diagram.

Its primary artifact is the semantic record. Diagrams are purpose-specific projections:

```text
semantic record
  ├─ hierarchy overview
  ├─ group relationship map
  ├─ membership detail
  ├─ focused lineage
  └─ spatial map
```

This design preserves KJ-family movement from cards to higher integration while making the result usable in an AI workflow that may revisit the same material many times.
