# Configuring use scope, loading depth, and round boundaries

Read this when mapping conditions supplied from outside the skill into runtime states for how much of the skill to use, how deeply to read cultural frameworks, and where to delimit a round.

## 0. Separate the decision-maker from runtime states

This file provides vocabulary for describing use states and the operations available in those states. It is not a rule set by which the skill independently decides the task's value, priority, scope of use, or stopping conditions.

Use conditions come from explicit requests by the requester or author, the calling context, higher-level settings or instructions, or discretion explicitly delegated by those sources to the executing AI. When details are delegated, the executing AI may adjust states within that delegation.

Keep two kinds of state distinct.

1. **Skill use scope**: non-use / limited use / exploratory use.
2. **Framework loading depth**: `not_loaded / probe / preview / full / enacted`.

These describe capabilities and progress states, not a value ranking of which state ought to be chosen.

## 1. Skill use scope

- **Non-use**: do not use this skill's operations in the current work.
- **Limited use**: use only designated or delegated operations, such as KJ, provenance, temporal structure, or missing connections.
- **Exploratory use**: move iteratively between cultural-framework exploration and KJ material integration, working broadly with structure, relations, states, transitions, and related forms.

Do not encode a rule in this skill that decides use or non-use merely from a task category such as open problem, closed problem, proofreading, translation, calculation, implementation, or urgent work. Task type may still inform a requester or an executing AI acting within delegated discretion.

When the skill is explicitly requested, receive that request as a use condition. If the request is broad, such as "use CSW," and leaves details delegated, the executing AI may adjust use scope and depth to the task.

## 2. Framework loading depth

- **`not_loaded`**: no cultural framework is currently open.
- **`probe`**: explore an entry into another cognitive field through cycles, paths, boundaries, center/periphery, multiple timescales, flow, continua, repetition and offset, or related structures.
- **`preview`**: make light contact with a candidate framework's main cognitive structure, positional relations, temporal structure, and limits.
- **`full`**: read primary sources, lineage, symbolism, and compound structure.
- **`enacted`**: execute a framework-native operation in relation to the target.

All of the following are available paths: beginning from `probe`, previewing structurally different candidates from recall anchors, directly previewing a named framework, and proceeding to `full` or `enacted`. Which path is taken follows the external use conditions and the scope of delegation.

During exploration, the recall anchors in `methods/system-selection.md` can be used for state grids, time, paths, directions, flow, and related structures. Questions, contrasts, research targets, and candidate KJ material generated from a framework retain provenance through states such as `framework_generated`.

## 3. Observation signals

During a run, the following states can be observed and recorded.

- whether new semantic units, relations, or questions are appearing;
- whether increments duplicate existing material;
- whether only framework vocabulary is increasing;
- what is happening to target facts, boundaries, irreversibility, and evidence state;
- where differences from the baseline lie;
- how much target-side material exists for an attribution claim;
- what artifacts, decision material, research directions, residuals, and reopening conditions currently exist.

These are not automatic stop rules that command reduction, continuation, deeper loading, or termination. If external use conditions reserve the decision to the requester, return them as decision material. If the decision has been delegated to the executing AI, use them within that delegation.

## 4. Delimiting and reopening

Distinguish stopping use of an individual framework, changing this skill's use scope, and ending the entrusted task itself.

When delimiting a round, preserve the current result, unresolved residuals, and reopening conditions. Later material that touches those residuals can reopen work from the previous state.

Value judgments such as resource limits, deadlines, publication, adoption, or rejection follow the external use conditions. Static rules inside this skill do not independently add them.
