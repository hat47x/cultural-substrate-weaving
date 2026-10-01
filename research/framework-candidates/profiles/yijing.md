# Yijing framework profile candidate

Status: adopted / runtime-corpus

## Identity

- names: 易 / 易経 / Yijing / Book of Changes
- family: early and classical Chinese change/correlative traditions
- intended CSW use: exploratory cognitive field, not divination service
- current profile scope: line / trigram / hexagram / change structure only

## Source basis

### Primary-text digital edition

Chinese Text Project, Book of Changes: Xi Ci I

https://ctext.org/book-of-changes/xi-ci-shang

The received commentary tradition describes the formation of eight trigrams and sixty-four hexagrams from combinations of divided/undivided lines and treats change as central to the system.

### Scholarly reference

Stanford Encyclopedia of Philosophy, Metaphysics in Chinese Philosophy

https://plato.stanford.edu/entries/chinese-metaphysics/

Useful here for distinguishing Chinese process/correlative metaphysics from substance-style classification and for situating the Yijing alongside yin-yang and wuxing.

## Structural core retained by this profile

### Binary line

A line has a divided / undivided contrast. For CSW, this is useful first as a minimal distinction capable of recombination, not as a ready-made mapping to target properties.

### Trigram

Three lines compose one of eight trigrams.

Cognitive use:

- hold a small state configuration;
- compare configurations that differ by one component;
- change viewing position without collapsing the whole into one label.

### Hexagram

Two trigrams / six lines form one of sixty-four hexagrams.

Cognitive use:

- treat a situation as a composite configuration;
- distinguish local component change from whole-state change;
- preserve multiple positions before narrating one global interpretation.

### Change

The system's value to CSW is not merely the inventory of sixty-four named states. It is the ability to ask what becomes visible when a configuration is transformed.

This profile therefore privileges:

- configuration;
- changed line;
- transformed configuration;
- contrast between before and after;
- alternative configuration as counter-view.

It does not encode a universal algorithm saying which target feature maps to which line.

## Native operation candidates

### configure

Represent a target question as a hypothetical multi-position configuration.

Output type:

- distinction
- question

Boundary:

The configuration is framework_generated; it is not a finding about the target.

### single-change

Change one position while holding the others fixed.

Questions:

- What assumption changed?
- Which previously stable relation becomes unstable?
- Does the target evidence distinguish the two configurations?

Output type:

- transition-candidate
- falsifier
- contrast

### invert-or-counter-view

Construct an opposed or transformed view and ask what the original framing hid.

Output type:

- counter-question
- distinction
- residual

Do not claim that the opposed hexagram is historically the only legitimate opposite without a lineage-specific rule.

### decompose-recompose

Read upper/lower or component structure separately, then return to the whole.

Output type:

- component distinction
- relation-candidate
- recomposed question

This is especially useful when a target description has prematurely become one label.

## What not to import by default

The following require separate source and lineage work before runtime use:

- a complete divination procedure;
- judgments attached to every hexagram/line;
- King Wen sequence as a universal transition graph;
- nuclear trigrams;
- plum blossom numerology;
- calendrical correspondences;
- wuxing correspondences;
- medical correspondences;
- modern psychological mappings.

These may be legitimate within particular traditions, but this minimal profile does not treat them as one undifferentiated canonical layer.

## Exploratory prompts produced by this profile

- If the current account is one configuration rather than one essence, which component is doing the most work?
- What changes if exactly one assumption flips?
- Which part of the target remains invariant across that change?
- What does the counter-configuration make visible that the current framing suppresses?
- Are two apparently different cases actually the same configuration at a different position?
- Which proposed transition has no target-side evidence?

## De-binding

Before returning a candidate to the target:

1. remove hexagram/trigram names unless needed for provenance;
2. restate the candidate in target vocabulary;
3. keep framework_generated origin;
4. state what target observation would support or push back on it;
5. preserve any useful residual even if the Yijing mapping itself is withdrawn.

## Adoption synchronization

This framework is adopted in `src/ja-JP/frameworks/yijing.md` as a minimal catalytic dossier.

Runtime adoption licenses configuration, position, nesting, contrast, and clearly-labelled CSW mutation probes. It does not license a complete divination procedure or one universal transformation convention.

Compact glossary:

- line / 爻: one binary position;
- trigram / 卦: three-line local configuration;
- hexagram / 六十四卦の一卦: six-line composite configuration.

Target-return example: if a project plan is hypothetically represented as six dependent positions, changing one assumption may expose which downstream relation actually depends on it. The hexagram mapping is then removed; the surviving target question is “which observed dependency changes when this assumption changes?” Further historical transformation conventions remain enrichment work, not blockers to this minimal runtime use.
