# Theravāda Paṭṭhāna conditional-relations candidate profile

Status: profile-ready / research-only

## Identity

- names: Theravāda Paṭṭhāna conditional relations / Paṭṭhāna paccaya / conditional-relations analysis / 上座部アビダンマ『発趣論』の条件関係
- current scope: the Theravāda Abhidhamma Paṭṭhāna tradition as a highly differentiated analysis of conditional relations, using modern scholarly and Pali Text Society references to bound the historical and doctrinal scope
- intended CSW use: replace a single generic dependency edge with an inspectable network in which conditioning item, conditioned item, relation mode, temporal relation, and convergence with other conditions can be kept separate
- not intended use: importing Buddhist ontology into a target domain, treating all twenty-four paccaya as a software taxonomy, or claiming that a formal condition map proves target causation

## Source basis

### Canonical-text reference — Pali Text Society, Paṭṭhāna

https://palitextsociety.org/product/pa%E1%B9%AD%E1%B9%ADhana/

The Pali Text Society identifies Paṭṭhāna as the final book of the Abhidhamma-piṭaka and describes it as a highly technical, minutely detailed analysis of conditionality. It also records that the English *Conditional Relations* translation covers part of the Tikapaṭṭhāna.

For CSW, this establishes that the source is not merely a modern "systems thinking" analogy. The candidate is anchored in a historically specific Theravāda analytical tradition.

### Translation guide — U Narada, Guide to Conditional Relations

https://palitextsociety.org/product/guide-to-conditional-relations/

The Pali Text Society lists U Narada's *Guide to Conditional Relations* as a dedicated guide to the Paṭṭhāna translation. CSW treats it as a guide to the source structure, not as authority for transferring doctrinal truth into a target domain.

### Scholarly reference — Relations in Buddhism

https://link.springer.com/rwe/10.1007/978-1-4020-8265-8_1597

The Springer reference entry distinguishes Paṭṭhāna's system of conditional relations from the more compact dependent-origination sequence and documents its place within Theravāda Abhidhamma. Its bibliography points to U Narada's translation/guide, Buddhaghosa, and modern studies of the twenty-four conditions.

This supports the main CSW distinction: Paṭṭhāna is useful here because it differentiates modes of conditioning rather than representing every dependency with one undifferentiated arrow.

### Scholarly synthesis — Y. Karunadasa, The Theravada Abhidhamma

https://wisdomexperience.org/product/the-theravada-abhidhamma/

Karunadasa's study treats conditional relations as a major component of Theravāda Abhidhamma's account of conditioned reality. CSW uses this as a modern scholarly boundary source and does not import the book's ontological conclusions into software, organizations, or other targets.

### Practice-oriented outline — Conditionality of Life

https://www.wisdomlib.org/buddhism/book/conditions/d/doc2899.html

Nina van Gorkom's outline explicitly presents twenty-four classes of conditions and emphasizes that a phenomenon can occur through a concurrence of different conditions operating in intricate ways. It is useful for seeing the many-relation structure, but CSW does not use its devotional or doctrinal claims as target evidence.

## Structural core

The useful CSW structure is **typed multi-condition convergence**, not "everything is interconnected."

A working minimum is:

1. name one target-side state or event that needs explanation;
2. separate the conditioning item from the conditioned item;
3. record the mode in which the relation is hypothesized to operate rather than writing only a generic arrow;
4. allow several heterogeneous conditions to converge on one target state;
5. distinguish sequential, simultaneous/co-present, mutually supporting, and persistence/absence-like relations when the target material justifies the distinction;
6. allow one condition to support several downstream states;
7. keep competing relation-mode hypotheses visible when evidence does not decide between them;
8. return every edge and relation-mode label to target-side observations, tests, records, or constraints.

The historical twenty-four paccaya are not copied into a target taxonomy. They function as evidence that the source tradition refuses to reduce all conditioning to one relation type.

## Candidate operations

### conditioning-role-separation

Separate what is acting as a condition from what is being conditioned before discussing "cause" in the abstract.

### relation-mode-differentiation

Ask whether two linked items are related through sequence, co-presence, support, mutual dependence, persistence/absence, or another target-justified mode rather than leaving the edge untyped.

### multi-condition-convergence

Preserve several non-equivalent conditions that jointly support one state instead of selecting one fluent root cause too early.

### one-to-many-conditioning-spread

Check whether one target-side condition participates in several downstream states, exposing shared dependency or common-mode failure without assuming that every downstream relation is identical.

### simultaneous-vs-sequential-audit

Distinguish a condition that must already be present together with the target state from one whose effect is carried from an earlier state.

### reciprocal-support-probe

Test whether A is being modeled as supporting B while B also constrains or sustains A, rather than forcing the pair into a one-way arrow.

### relation-mode-uncertainty-preservation

When evidence supports a dependency but not the precise mode, keep the edge and its relation type at different confidence levels rather than manufacturing precision.

## Useful outputs

- conditioning-item / conditioned-item pair;
- typed dependency edge;
- convergence set for one outcome;
- shared-condition fan-out;
- simultaneous-vs-sequential distinction;
- reciprocal-support candidate;
- relation-mode uncertainty note;
- target-side test or observation request for one edge;
- "the dependency is observed, but the proposed relation mode is not yet supported" diagnostic.

## Target-return questions

- What exactly is conditioning what?
- Is this edge merely correlated, or does target evidence justify treating it as a condition?
- Does the target require one generic dependency relation, or are different relation modes operationally meaningful?
- Which conditions converge on the same outcome without being interchangeable?
- Which conditions must be co-present, and which operate through earlier state?
- Does one shared condition create several downstream vulnerabilities?
- Is a supposed one-way dependency actually reciprocal in the target?
- Which relation-mode labels came from target evidence, and which came only from framework contact?
- Would an ordinary typed dependency graph, fault tree, or causal map expose the same useful distinctions with less cultural/framework overhead?
- If all Pāḷi and Abhidhamma vocabulary is removed, does a useful target-side multi-condition distinction remain?

## Distinction from nearby CSW frameworks

- **Dependent origination** currently gives CSW a strong condition-chain, upstream-condition, and cessation-counterfactual pass. Paṭṭhāna adds value only when the target requires multiple heterogeneous condition modes and convergence beyond a mostly chain-oriented question.
- **Aristotle's four causes** splits a vague "why" into explanatory categories. Paṭṭhāna-inspired analysis instead differentiates relations among conditioning and conditioned states; it should not be used to replace material/formal/efficient/final explanation.
- **Wuxing** can expose cyclic enabling and constraining relations. Paṭṭhāna does not supply a five-phase cycle; it is useful when the network contains several relation modes without one privileged cycle.
- **Pāṇini rule architecture** distinguishes inherited rule context, blocking, and derivation order inside a rule system. Paṭṭhāna is not a rule-resolution framework.
- **ordinary typed dependency graph / fault tree / causal map** is the strongest non-cultural baseline. If target-side edge typing and convergence can be obtained as clearly and cheaply with those ordinary tools, this candidate should remain research-only or be removed from the runtime queue.

## Historical / doctrinal boundary

- Paṭṭhāna is specific to the Theravāda Abhidhamma tradition; do not present it as the single Buddhist theory of causality.
- The twelve-link dependent-origination formulation and Paṭṭhāna's differentiated conditional relations are related but are not interchangeable analytical forms.
- Traditional accounts of authorship and revelation belong to religious tradition and are not required for the structural candidate.
- The twenty-four conditions describe relations among dhammas inside a specific doctrinal analysis. CSW must not rename software services, people, requirements, or database rows as dhammas and thereby imply ontological equivalence.
- Modern summaries vary in translation of paccaya names. Runtime or target-facing output should therefore prefer de-bound target language unless provenance matters.
- A formal relation map is not proof of causality. Target-side evidence and domain expertise remain authoritative.

## What not to import by default

- all twenty-four paccaya as mandatory target categories;
- Abhidhamma ontology or claims about ultimate reality;
- rebirth, kamma, consciousness taxonomy, or liberation goals;
- a claim that every target event has multiple conditions simply because the source framework does;
- a claim that reciprocal or simultaneous conditioning exists without target evidence;
- a claim that a dense network is more insightful than a simple chain;
- relation labels whose only support is resemblance to a historical paccaya term;
- the idea that a religious canonical status creates epistemic authority in the target.

## De-binding route

Before returning a Paṭṭhāna-inspired pass to the target:

1. remove Pāḷi relation names unless provenance is necessary;
2. name the target-side conditioning item and conditioned item;
3. describe the proposed relation mode in ordinary domain language;
4. identify whether the relation is observed, inferred, or merely framework-generated;
5. preserve multiple conditions when the target supports them, but do not manufacture a complete network;
6. turn uncertain relation modes into explicit test or evidence requests;
7. compare the result with an ordinary typed dependency graph / fault tree / causal map;
8. keep only distinctions that survive that baseline comparison and target return.

## Runtime decision

Do not adopt into runtime yet.

The candidate fills a real corpus gap: branching and converging conditional networks with differentiated relation modes. However, generic dependency modeling is a strong baseline and may capture most of the de-bound value.

The first research comparison should therefore test whether Paṭṭhāna contact produces target-supported distinctions that an ordinary typed dependency graph or fault-tree review does not, without importing the twenty-four-condition taxonomy.

Worked examples:

- `research/framework-candidates/worked-examples/theravada-patthana-conditional-relations.md`
- `research/framework-candidates/worked-examples/theravada-patthana-conditional-relations-negative.md`
