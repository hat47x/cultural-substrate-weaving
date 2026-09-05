# Usage-scope and loading-depth states

Read this when representing how much of the skill is being used and how deeply a cultural framework has been opened.

**This document is not a decision engine for scope or depth.** Values, usage scope, loading depth, stopping, and adoption come from the author's decisions or from settings, instructions, and delegations that the author gives to the generative AI outside this skill.

When the author has delegated those decisions to the generative AI, the AI may decide within that delegation. The authority for the decision is the externally supplied objective, constraints, evaluation axes, and delegation, not a preference intrinsic to this module.

## 0. Separate two state dimensions

1. **Skill usage scope**: `non_activation / limited / exploratory`.
2. **Framework loading depth**: `not_loaded / probe / preview / full / enacted`.

These are vocabulary for recording the current execution state. They do not encode rank, success, failure, or desirability.

## 1. Usage scope

- **`non_activation`**: the skill's operations are not being used under the current external decision or delegated decision.
- **`limited`**: selected operations are being used, such as KJ, provenance, temporal structure, connections, or part of a cultural framework.
- **`exploratory`**: several operations such as cultural-framework exploration, KJ, and transformation are being used iteratively.

Whether the task is simple or complex, open or closed, proofreading, translation, calculation, implementation, or creative work may be relevant context, but task category is not an automatic activation or suppression rule owned by this skill.

Whether the skill was explicitly invoked or not, usage scope is handled through the decision authority and delegation outside the skill.

## 2. Framework loading depth

- **`not_loaded`**: a cultural framework has not been opened yet.
- **`probe`**: lightly exploring questions, relations, states, or transitions that connect target-side language or structure to possible frameworks.
- **`preview`**: making light contact with a candidate framework's major cognitive structure, positions, relations, cycles, boundaries, or related features.
- **`full`**: consulting a wider framework surface such as primary sources, lineage, symbolism, and compound structure.
- **`enacted`**: executing a framework-native operation.

A probe that generates no new question, a preview that mostly duplicates existing understanding, or a full read that mostly adds framework-specific information can be recorded as **observed differences**. Those observations are not automatic triggers to deepen, return, or stop.

A candidate framework may have been explicitly named, arisen from context, or come from the recall anchors in `methods/system-selection.md`; that entry provenance can also be recorded. Which entry to use, how many candidates to inspect, and how deeply to load them follows the external delegation.

## 3. Decision material for changing depth

The following states can be reported as **decision material** for reconsidering usage scope or loading depth:

- new semantic units, relations, or questions did or did not appear;
- overlap with existing content increased;
- framework vocabulary or explanation volume increased;
- descriptions of target facts, boundaries, irreversibility, or evidence state changed;
- artifacts or questions changed or did not change relative to a baseline;
- target-side material relevant to attribution is present or absent;
- work volume, time, computation, or external resource use changed.

This document does not assign the value “reduce,” “continue,” or “stop” to those observations. The author or the delegation outside the skill determines how they are evaluated.

## 4. Ending, reopening, and resource constraints

Where to end a round, how much residual material to preserve, and whether to reopen later follow the external objective, delegation, and resource constraints.

When useful at an endpoint, record the current usage state, unresolved items, residuals, and references that could be opened next. This is a recording operation that preserves restart information; it is not the stopping decision itself.

When external time, cost, context, privacy, or other resource constraints are specified, record them together with the usage state. This skill does not add its own resource values in order to suppress use.
