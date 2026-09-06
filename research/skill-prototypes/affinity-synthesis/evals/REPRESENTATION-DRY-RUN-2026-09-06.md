# Representation Dry Run — 2026-09-06

Status: research note

## Purpose

Check whether the proposed `affinity-map` interchange and reference Mermaid renderer can preserve the intended distinctions among group membership, explicit relation, secondary resonance, and gap-as-question on a small real-task-derived example.

## Fixture

Input:

- `examples/minimal-map.json`
- schema candidate: `references/affinity-map.schema.json`
- renderer: `scripts/render_mermaid.py`

The example is derived from the earlier accountability / non-conversion synthesis comparison, simplified for representation testing.

## Checks performed

### 1. JSON / schema

The schema was loaded with a Draft 2020-12 validator and checked as a schema.

`examples/minimal-map.json` validated successfully against the candidate schema.

Result: **pass**

### 2. Group projection generation

Command-equivalent:

```text
python render_mermaid.py minimal-map.json --view group
```

Observed source shape:

```mermaid
flowchart LR
    G01["G01｜自己防御を過度に刺激せず、具体的な責任行為へ戻れる通路を保つ"]
    G02["G02｜配慮が責任の希薄化へ変わる境界は別に監査する必要がある"]
    Q01["Q01?｜時間差を許すことが、どの条件で責任放棄へ変わるのか"]

    G01 -->|"R01｜通路を保つ配慮は、責任の希薄化へ変わる境界を同時に監査する必要を生む [supported as synthesis]"| G02
    G01 -.->|"question / not asserted relation"| Q01
    G02 -.->|"question / not asserted relation"| Q01
```

Checks:

- R01 remains a full natural-language predicate rather than becoming `causes` / `depends-on`.
- the directed connector does not itself claim causality; predicate text carries the meaning.
- Q01 links are explicitly labeled as question links, not asserted semantic relations.

Result: **pass for source generation**

Rendered visual inspection has not yet been performed in this branch.

### 3. Membership projection generation

Command-equivalent:

```text
python render_mermaid.py minimal-map.json --view membership
```

Observed source shape:

```mermaid
flowchart TB
    subgraph SG_G01["G01｜自己防御を過度に刺激せず、具体的な責任行為へ戻れる通路を保つ"]
        G01_anchor["G01｜自己防御を過度に刺激せず、具体的な責任行為へ戻れる通路を保つ"]
        C001["C001｜人格否定ではなく具体的な行為へ話を戻すと、自己防御を強めず責任を扱える。"]
        C002["C002｜その場での改心を迫らず、理解や反応に時間差が生じる余地を残す。"]
    end
    subgraph SG_G02["G02｜配慮が責任の希薄化へ変わる境界は別に監査する必要がある"]
        G02_anchor["G02｜配慮が責任の希薄化へ変わる境界は別に監査する必要がある"]
        C003["C003｜反発を避けることが、責任そのものを曖昧にする方向へ流れる危険もある。"]
    end
    C003 -.->|"X01｜resonance / not membership｜G01の成立条件を裏側から限定するが、G01のmemberとして同化しない。"| G01_anchor
```

Checks:

- C003 remains a member of G02 only.
- X01 is not represented by duplicating C003 inside G01.
- resonance is visibly labeled `not membership`.

Result: **pass for source generation**

## Findings

### F1. Separate projections are preferable to one overloaded map

The group map and membership map answer different review questions. Combining both into one diagram would add visual density and make a dashed resonance easy to misread as an ordinary semantic edge.

Current decision: keep projection-specific views.

### F2. A question link needs explicit non-assertion labeling

A dashed line by itself is not enough. Different renderers and readers attach different meanings to line style.

Current decision: keep textual labels such as `question / not asserted relation` and `resonance / not membership`; do not rely on color or dash style alone.

### F3. Mermaid does not cover the spatial-map requirement

The reference renderer intentionally ignores free-position layout coordinates except for a warning comment. This is correct for the topology projection but leaves a deliberate open item: a spatial renderer must preserve coordinates without turning them into semantic edges.

## Remaining gates

1. render the generated Mermaid with an actual Mermaid renderer and visually inspect line crossing / label clipping;
2. run the same semantic record through a free-position projection such as Excalidraw or SVG;
3. test with a nested higher-order group;
4. test with 100+ cards and verify that overview/detail splitting remains usable;
5. add lineage projection after the core notation stabilizes.
