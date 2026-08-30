# 02a-framework-application

Read this when bringing a selected framework into contact with a target. Decide framework, use, exploration/attribution mode, and application scope first in `02-system-selection.md`.

## 3.0 Exploratory use and attribution use

In **exploratory use**, treat positions, paths, cycles, symbols, and relation vocabulary as cognitive resources for generating questions, hypotheses, contrasts, research targets, and compositional candidates. The target need not be assigned to every framework position, and empty positions are not target gaps. Outputs remain `framework_generated` until independently supported on the target side.

In **attribution use**, the claim is that the target itself has a framework-shaped position, state, transition, or gap. Then use the assignment, transition, and post-use checks below.

Do not silently switch from exploration to attribution.

## 3a. Fix the assignment

A framework has at least two layers.

- **Position layer**: a fixed set of positions defined before seeing the target. This layer can be used for classification.
- **Interpretive-language layer**: judgments, imagery, correspondences, and character descriptions that can be broadly applied through analyst similarity judgments. Do not use this layer as the classifier.

Distinguish predicates that decide assignment.

- **Counting predicate**: counts items whose membership can be decided mechanically, such as literal strings.
- **Computational predicate**: determines position through a target-independent procedure, such as a calendrical calculation.
- **Similarity judgment**: requires the analyst to decide item by item that something is similar or has a certain quality.

**Fix assignment from the position layer before using interpretive language. Do not infer assignment backward from an interpretation.** If no external procedure determines position, attribution use requires an explicit external convention that maps observable target facts to positions.

A framework may provide the number of positions without providing the rule for cutting the target into that number. The cut is also part of assignment.

### Make external conventions visible

Name tie-breaking rules, boundaries, vocabulary-to-position mappings, and other decisions supplied by neither the target nor the framework. If reversing one of these conventions moves the result substantially, the conclusion depends more on the convention than on the target.

A numerical output does not make the predicate mechanical. If membership itself depends on similarity judgment, the procedure remains judgment-based. When counts matter, inspect how boundary cases and conventions move the result.

Declare the layer to which the predicate applies. Do not mix target events, acts of description or observation, and other objects mentioned inside the target.

### Separate reproducibility from correctness

**A unique assignment and a correct assignment are different things.** Mechanical procedures first buy reproducibility. Return every important filled position to the target and inspect its basis.

When coverage matters, look in both directions: how much of the framework's position vocabulary was used, and how much of the target was captured by at least one position.

Distinguish at least three kinds of empty position.

1. No candidate for that relation appears in the target.
2. A candidate appears, but the relation is not described.
3. It is empty in the declared layer but filled in another layer.

The third is not a target gap.

For important assignments, apply the rule **independently twice**. Do not build a target finding on positions that do not reproduce.

### Separate derivation from convention

A position system may contain parts regenerable from rules and parts preserved only as lineage-specific conventions.

- Mechanically validate derivable parts: element counts, transitions, inverse operations, impossible connections, and similar properties.
- For conventional parts, identify the lineage and source; where material, compare at least one relevant alternative lineage.

Do not use a derivable component that fails validation. Do not invent analyst-defined transitions and then attribute them to a framework that has no transition rule.

### Keep interpretive language available

The interpretive-language layer is not used for assignment, but in exploration it can generate secondary-effect questions, counter-hypotheses, sensitivity checks, inspection items, conflict structures, and expression candidates.

Do not suppress framework-generated ideas. Keep enough provenance to tell which framework, part, or operation generated them.

## 3ab. Run transitions

Use this when a transition model is being used for **attribution**. Treat the position layer as a state set and test transitions defined by the framework itself on the target.

1. **Lay out the state grid**: assign target events, elements, or actors to states. Keep empty states visible.
2. **Test transitions**: apply the framework's transition rule and ask whether a corresponding movement is observable in the target. Never use “the framework says it should happen” as target evidence.
3. **Keep differences visible**: distinguish unreachable states, transitions that never occur, and states entered but not returned from. Separate target absence from missing description, not-yet-observed events, and framework-side prohibitions.
4. **Check coverage**: determine whether the grid covers the target broadly or only a fragment.
5. **Keep trajectories separate by factor**: preserve the states and order traversed by each actor or element rather than averaging them together.

**A transition run first produces hypotheses.** Return apparent irreversibility and missing transitions to the target for independent checking.

Do not use a framework without transition rules for transition-model attribution. A metaphorical transition used for exploration remains `framework_generated`.

## 3b. Check after use

For attribution use, perform these checks. For exploration-only use, apply the portions needed to prevent over-importing framework structure.

- **Reversal check**: try to falsify the claim produced by the framework. Do not absorb counterexamples back into support. If every counterexample can be explained away, remove that framework from attribution use for this target.
- **Alternative check**: if another framework yields the same candidate finding, do not treat it as framework-specific contribution. Distinguish a framework that could not be assigned from one that was assigned and did not yield the finding.
- **Misfit record**: preserve where the framework does not fit. Separate gaps known from the framework's coverage before application from misfits discovered only after contact with the target.
- **Removal check**: remove framework names, correspondence tables, and interpretive vocabulary, then ask whether each candidate still reads as a meaningful target-side question, hypothesis, or description.

**The removal check performs de-binding; it does not create evidence.** Survival after removal does not by itself move an item to `target_supported`. In research or diagnosis, confirm independent target-side sources, observation, or falsification before making that move. Do not ask whether the same question could have been invented without the framework.

The same candidate appearing from several frameworks does not create several independent pieces of target evidence. Counts, when kept, are guards against overclaiming rather than quality scores.

## 3c. Exit according to purpose

### Research and diagnosis

Return framework-generated material as researchable questions, hypotheses, falsification conditions, observation items, comparison axes, additional sources to seek, and residuals. Move only independently supported items to `target_supported`.

### Generation and composition

For writing, art, design concepts, or worldbuilding, `framework_generated` structure may be adopted as a compositional resource. Colors, numbers, cycles, contrasts, paths, and symbolic surplus may remain when they improve the artifact.

Do not confuse compositional adoption with a historical fact about the tradition, a causal law of the real world, or an empirical finding about the target.

A third structure arising from contact among frameworks remains `cross_field_emergent`; do not write it back into the canonical framework itself.

## 3d. Adoption state and over-application

When useful, distinguish reflection into the artifact, internal scaffolding, a reusable auxiliary model, rejection, and detected distortion. Rejecting a framework does not require deleting every question it generated.

Over-application tends to show up as one-to-one mappings multiplying, pressure to fill empty positions, explanation volume growing without target-side movement, or conflict and irreversibility being absorbed into harmony. Even when these signs are absent, check coverage: a framework may simply be explaining only a small part of the target.
