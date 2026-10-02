# Inka khipu record-structure candidate profile

Status: profile-ready / research-only / undeciphered-semantics-sensitive

## Identity

- names: khipu / quipu / Inka-style khipu
- current scope: historically documented Inka-style knotted-cord record structures, especially attachment hierarchy and securely understood numerical conventions
- intended CSW use: preserving information carried by position, attachment, grouping, and multiple representational channels when a target is flattened or digitized
- not intended use: decoding unknown khipu semantics, claiming all khipus are numerical, or treating a modern tree/database as historically equivalent to khipu

## Source basis

### Open corpus / structural metadata

Open Khipu Repository

https://github.com/khipulab/open-khipu-repository

Zenodo archive:

https://zenodo.org/records/5037552

The repository records extant Inka-style khipus and their structural metadata. It is useful for verifying that research tracks cords, knots, attachments, and other physical features without implying that every feature has a known meaning.

### Museum object layer

Peabody Museum Collections Online, Quipu

https://collections.peabody.harvard.edu/objects/details/80232

The object record documents a carrying/primary cord, secondary cords, and attached knotted strings. CSW uses such museum records to anchor attachment hierarchy in actual artifacts rather than a software-tree analogy.

### Scholarly institutional overview

Dumbarton Oaks, “Inka Khipus (1450–1534 CE)”

https://www.doaks.org/resources/online-exhibits/written-in-knots/inka

The overview distinguishes statistical/accounting khipus and describes features such as color organization and base-10 positional knot notation. These securely understood numerical conventions are kept separate from disputed or undeciphered non-numerical semantics.

### Corpus-scale scholarship

Latin American Antiquity, “How Can Data Science Contribute to Understanding the Khipu Code?”

https://www.cambridge.org/core/journals/latin-american-antiquity/article/how-can-data-science-contribute-to-understanding-the-khipu-code/E2D0E68A0515F3F9582A23C63693F4CE

The study examines structural and numerical relations across a large corpus. CSW uses it to support grouping/summary-relation questions, not to claim a general decipherment.

## Structural core

The reusable structure is not “knots equal data.”

It is that information may be distributed across several channels at once:

- attachment hierarchy: primary, pendant, subsidiary, and deeper attached cords;
- position along a cord;
- knot form and count;
- grouping or summary relations;
- color, material, twist, or other recorded physical attributes whose semantics may be known, uncertain, or context-dependent.

For some statistical khipus, decimal positional values and numerical relations are well established. Other semantic dimensions remain debated or undeciphered. CSW must preserve that asymmetry.

## Native operation candidates

### attachment-hierarchy-preservation

Ask what meaning is carried by what is attached to what, rather than flattening all items into one list.

### positional-value-channel

Ask whether position within a carrier encodes a different dimension from the item value itself.

### multichannel-record-probe

Inventory distinct channels—value, position, attachment, color, material, orientation, annotation—before deciding which are semantically active in the target.

### grouping-and-summary-relation

Ask whether parent/summary elements aggregate or classify attached detail records, while requiring target evidence for the relation.

### undeciphered-semantics-preservation

Preserve structured but unexplained target features as unknown rather than inventing a meaning because another channel is understood.

### flattening-loss-audit

Before converting a structured artifact into rows or text, identify which relations would disappear when hierarchy, position, or non-textual channels are removed.

## Target-return questions

- Which information lives in the item value, and which lives in attachment or position?
- Does flattening the target erase parent/child, group/summary, or ordering relations?
- Which channels have independently documented meanings?
- Which visible regularities remain semantically unknown?
- Is an absent value equivalent to zero, or merely no mark/no observation?
- Which relations survive if color or formatting is removed?
- What target-side evidence licenses a parent/summary interpretation?
- After removing khipu vocabulary, does a multi-channel record-preservation problem remain?

## Near-neighbor differentiation

### Khipu vs generic tree

A generic tree captures parent/child links but can ignore positional value, physical channels, or undeciphered-but-structured attributes.

The khipu candidate is useful only when the target risks losing information through flattening across multiple channels.

### Khipu vs Hadith isnād / matn

Hadith structure separates transmitted content from provenance path.

Khipu structure here separates representational channels inside one record artifact and preserves attachment/position without assuming a transmission chain.

### Khipu vs Llull's Ars

Llull systematically generates unseen combinations.

Khipu does not generate combinations. It asks what information is already encoded across multiple structural channels and what would be lost by flattening.

## Historical and epistemic boundaries

- Do not claim all khipus are numerical records.
- Do not assign universal meanings to color, twist, fiber, orientation, or non-numerical patterns unless the cited target-specific scholarship supports them.
- Do not infer narrative content from structural regularity.
- Do not equate khipu with a modern database, spreadsheet, binary code, or writing system as if the equivalence were settled.
- Keep Inka-style archaeological/museum khipus distinct from post-Inka and living Andean khipu traditions unless separately sourced.
- Do not use undeciphered semantics as an invitation for model completion.

## De-binding route

1. remove Quechua/Andean cultural labels from the target-facing result;
2. enumerate only target-observable channels such as value, position, attachment, grouping, formatting, material, or orientation;
3. separate known semantics from unknown-but-structured features;
4. label any proposed relation as `framework_generated` until target evidence supports it;
5. preserve hierarchy and position during transformation when they demonstrably carry information;
6. reject the framework if the target is already fully represented by an explicit flat schema with no lost relational or positional channel.

## Profile-ready decision

The candidate has multiple independent source classes, a bounded historical scope, explicit undeciphered-semantics limits, native operations, target-return questions, de-binding, and positive/negative examples.

It remains outside runtime. The next decision should test whether multi-channel record preservation produces distinct questions beyond generic data-modeling language while retaining the discipline of unknown-semantics preservation.

Worked examples:

- `research/framework-candidates/worked-examples/inka-khipu-record-structure.md`
- `research/framework-candidates/worked-examples/inka-khipu-record-structure-negative.md`
