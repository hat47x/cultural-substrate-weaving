# Prototype Scripts

These scripts operate on the research `affinity-map` interchange format. They are **representation helpers**, not a KJ engine. None of them may infer a new semantic relation merely to satisfy a renderer.

## `affinity_board.py`

Small working-board CLI for manipulating the research `affinity-map` without turning representation code into a synthesis engine.

Typical flow:

```bash
python scripts/affinity_board.py init /tmp/board.json \
  --question "What structure is emerging?"

python scripts/affinity_board.py add-source /tmp/board.json \
  --ref "notes://001" \
  --provenance "target-side notes" \
  --status "target_supported"

python scripts/affinity_board.py add-card /tmp/board.json \
  "Meaning-bearing card A" \
  --source S001

python scripts/affinity_board.py add-card /tmp/board.json \
  "Meaning-bearing card B with a different timing" \
  --source S001

python scripts/affinity_board.py add-group /tmp/board.json \
  --label "First integrated meaning" \
  --member C001

python scripts/affinity_board.py add-group /tmp/board.json \
  --label "Second integrated meaning" \
  --member C002

# Preserve explicit geometry when spatial arrangement itself matters.
python scripts/affinity_board.py set-position /tmp/board.json G001 0.18 0.42 \
  --projection spatial-map
python scripts/affinity_board.py set-position /tmp/board.json G002 0.58 0.37

# Audit what the grouping kept, newly created, and still failed to integrate.
python scripts/affinity_board.py audit-group /tmp/board.json G001 \
  --inherited "C001の具体的な制約を保持する" \
  --emergent "他のまとまりと並べると選択上のトレードオフが見える" \
  --residual "C002との時間感覚の差はなお未解消" \
  --preserved-difference "時間感覚の差を表札へ吸収しない"

python scripts/affinity_board.py add-residual /tmp/board.json \
  "Difference that should not be forced into either group" \
  --ref C001 --ref C002

# Keep a possible relation as a question first.
python scripts/affinity_board.py add-question /tmp/board.json \
  "G001とG002の間に時間差を介した接続があるか" \
  --between G001 G002 \
  --state unresolved

# Only after returning to the material, promote it explicitly.
python scripts/affinity_board.py promote-question /tmp/board.json Q001 \
  --direction directed \
  --predicate "G001で生じた遅れがG002の選択余地を狭める" \
  --basis C001 --basis C002 --state supported

# Narrate from explicit map refs and keep transformation provenance visible.
python scripts/affinity_board.py add-narrative /tmp/board.json \
  "G001からG002への制約は支持されたが、U001の時間差は未統合のまま残る" \
  --basis G001 --basis G002 --basis R001 --basis U001 \
  --inherited "G001とG002は別のまとまりとして立つ" \
  --emergent "接続から選択余地の縮小が見える" \
  --residual "U001の時間差はなお未統合"

# A return-check may weaken an already asserted relation.
python scripts/affinity_board.py revise-relation /tmp/board.json R001 \
  --direction directed \
  --predicate "G001はG002の一部の選択肢を狭める可能性がある" \
  --basis C001 --state tentative \
  --note "戻し検査で主張を弱めた"

# If the relation no longer survives, remove R and reopen it as Q.
python scripts/affinity_board.py demote-relation /tmp/board.json R001 \
  "G001とG002の間に、なお支持できる関係は残るか" \
  --id Q002 --would-clarify C001 --would-clarify C002

# Optionally prepare a handoff capsule without starting another round.
python scripts/affinity_board.py update-handoff /tmp/board.json \
  --semantic-ref G001 \
  --residual-ref Q002 \
  --source-ref S001 \
  --do-not-assume "Q002が示すrelationはまだ支持されていない"

python scripts/affinity_board.py handoff-add-check /tmp/board.json \
  "新材料がQ002へ実際に触れた場合だけ再検査する" \
  --ref Q002 --ref G001 --status candidate

# Reopen only the local semantic neighborhood of one stable ref.
python scripts/affinity_board.py focus /tmp/board.json G001

python scripts/affinity_board.py status /tmp/board.json
```

Supported operations include explicit source/card/group creation, post-group transformation audit, group membership edits, primary-card moves, explicit normalized spatial positions, secondary resonance, relations, residuals, questions, explicit question-to-relation promotion after return-check, narrative synthesis with basis/transformation audit, relation revision/demotion after another return-check, optional handoff-capsule maintenance, one-hop semantic focus, and board status.

Design constraints:

- every mutation is validated before replacing the file;
- failed mutations leave the previous board unchanged;
- IDs are stable references, not ontology classes;
- `move-card` changes direct membership but preserves the card itself;
- `audit-group` is a post-grouping audit: inherited / emergent / residual are recorded after a working group/label exists, not used as a pre-grouping taxonomy;
- `status` reports groups that still lack transformation audit so a polished-looking map does not silently skip the return-check;
- `set-position` / `clear-position` manipulate only normalized layout coordinates for card/group/narrative/residual/question refs; proximity never creates membership, relation, resonance, importance, or support;
- relation predicates and group labels are never inferred;
- questionable connections can remain questions instead of being promoted to relations;
- an existing relation is not sticky: `revise-relation` requires the caller to restate predicate/direction, and `demote-relation` removes the `R` before creating a new unresolved `Q`;
- relation demotion preserves the prior predicate only as audit history, not as a current assertion;
- `update-handoff` only records refs/provenance/guardrails selected from the current synthesis; it does not reopen them or start another round;
- `handoff-add-check` records a possible next check as a candidate, without executing, prioritizing, or treating it as required work;
- `add-narrative` requires at least one explicit `--basis` ref so map ↔ narrative return-check remains inspectable.
- `focus` is read-only and one-hop: it exposes the selected artifact plus directly connected membership, relation, resonance, narrative, residual, question, source, handoff context, and that ref's explicit layout position without recursively reopening the whole map. Handoff `do_not_assume` guardrails are surfaced only when the selected ref is actually carried or referenced by a next-check candidate.
- `status` surfaces ungrouped cards, multiple direct memberships, singleton groups, narratives, residuals, questions, and validation warnings.

The CLI is useful when conversation context is no longer a reliable place to remember card identity and movement. For small cases, directly editing the JSON or using the Markdown template can remain simpler.

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
