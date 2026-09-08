# Prototype Scripts

These scripts operate on the research `affinity-map` interchange format. They are **representation helpers**, not a KJ engine. None of them may infer a new semantic relation merely to satisfy a renderer.

## `validate_map.py`

Checks semantic cross-references that JSON Schema alone cannot express conveniently.

```bash
python scripts/validate_map.py examples/minimal-map.json
```

Checks include:

- duplicate IDs within a namespace;
- source / member / relation / narrative / question references;
- duplicate group members;
- direct and indirect group-membership cycles;
- relation endpoints and readable predicates;
- narrative basis refs for map ↔ narrative return checks;
- resonance target resolution;
- warning when a declared secondary resonance duplicates existing membership;
- warning when one card is directly placed in multiple groups and may have been confused with secondary resonance;
- normalized spatial positions and position references.

Warnings are deliberately separate from errors because some questionable states require human/material judgment rather than automatic rejection.

## `render_mermaid.py`

Reference renderer for topology-oriented projections.

### Group relationship map

```bash
python scripts/render_mermaid.py examples/minimal-map.json \
  --view group \
  -o /tmp/minimal-group-map.mmd
```

Shows group labels, explicit relations, and gap-as-question links.

### Membership map

```bash
python scripts/render_mermaid.py examples/minimal-map.json \
  --view membership \
  -o /tmp/minimal-membership-map.mmd
```

Shows group membership and secondary resonance. A resonance is rendered as a dashed cross-link labeled `resonance / not membership`.

### Mermaid non-goals

- It does not preserve arbitrary spatial coordinates; Mermaid is used as a topology projection.
- It does not convert proximity into semantic edges.
- It does not classify natural-language relation predicates into a closed relation taxonomy.
- Successful Mermaid source generation is not the same as visual render validation.

## `render_hierarchy.py`

Shows recursive group membership without expanding leaf cards.

```bash
python scripts/render_hierarchy.py /tmp/large-114.json \
  --with-relations \
  -o /tmp/large-114-hierarchy.mmd
```

A higher-order edge is always labelled:

```text
higher-order membership / not semantic relation
```

`--with-relations` may overlay explicit semantic relations, but they remain visibly distinct from containment/membership.

Use this projection when the important question is how leaf islands form higher-order integration units.

## `render_lineage.py`

Traces one artifact backward through its externally inspectable lineage.

```bash
python scripts/render_lineage.py /tmp/large-114.json \
  --focus N001 \
  --detail groups \
  -o /tmp/large-114-lineage.mmd
```

Detail modes:

- `groups` — direct cards are collapsed as `N cards collapsed`; higher groups remain explicit.
- `cards` — cards and their source refs are expanded.

This renderer is intentionally **focus-based**. It does not treat a full all-artifact graph as the default human diagram.

## `render_spatial_svg.py`

Reference renderer for a **free-position group-level spatial projection**.

```bash
python scripts/render_spatial_svg.py examples/minimal-spatial-map.json \
  -o /tmp/minimal-spatial-map.svg
```

The input uses normalized `layout.positions` coordinates. The renderer preserves those positions while drawing only explicit semantic relations plus clearly labelled question-provenance links.

Use this type of projection when proximity, distance, blank space, center/periphery, or another placement feature must survive automatic layout.

### Spatial renderer non-goals

- Coordinates do not create semantic relations.
- It does not infer edge types from geometry.
- It currently renders groups and questions, not a full card-level A-type diagram.
- It is a portable SVG reference implementation, not a replacement for Excalidraw or another interactive canvas.

## `generate_large_fixture.py`

Creates a public, synthetic 114-card recursive-grouping fixture.

```bash
python scripts/generate_large_fixture.py -o /tmp/large-114.json
```

Its ten leaf-group sizes mirror the structural load used in the 114-card real-task scale evaluation, but it contains no project card text. It exists to test validators and projections without publishing private/project-specific source material.

## Validation order

When possible:

```text
JSON Schema
  -> semantic cross-reference validator
  -> projection source generation
  -> renderer-specific syntax/render check
  -> visual inspection
  -> projection-integrity check against semantic record
```

A figure can be syntactically valid and still be semantically misleading. Visual validation must therefore check not only clipping and line crossing, but whether layout makes an unasserted hierarchy, causality, or membership look asserted.

For recursive grouping and multi-zoom lineage rules, see `../references/HIERARCHY-AND-LINEAGE.md`.
