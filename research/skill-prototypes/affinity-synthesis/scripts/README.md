# Prototype Scripts

These scripts operate on the research `affinity-map` interchange format. They are **representation helpers**, not a KJ engine. None of them may infer a new semantic relation merely to satisfy a renderer.

## `validate_map.py`

Checks semantic cross-references that JSON Schema alone cannot express conveniently.

```bash
python scripts/validate_map.py examples/minimal-map.json
```

Checks include:

- duplicate IDs within a namespace;
- source / member / relation / question references;
- duplicate group members;
- direct and indirect group-membership cycles;
- relation endpoints and readable predicates;
- resonance target resolution;
- warning when a declared secondary resonance duplicates existing membership;
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
- It does not render lineage yet.
- Successful Mermaid source generation is not the same as visual render validation.

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
