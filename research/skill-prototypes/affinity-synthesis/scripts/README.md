# Prototype Scripts

## `render_mermaid.py`

Reference renderer for the research `affinity-map` interchange format.

It intentionally renders only **projections** of the semantic record. It is not a KJ engine and does not infer new relationships.

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

### Non-goals

- It does not preserve arbitrary spatial coordinates; Mermaid is used as a topology projection.
- It does not convert proximity into semantic edges.
- It does not classify natural-language relation predicates into a closed relation taxonomy.
- It does not render lineage or free-position spatial maps yet.
- It does not claim that successful Mermaid source generation means the rendered layout has been visually validated.
