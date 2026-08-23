# 02 — Framework Selection

Read this file when selecting cultural frameworks and checking unit compatibility, rejection conditions, and limits.

## 3. Investigate framework candidates

Narrow candidates by differences in structural type rather than by listing framework names. For each framework, examine:

- components and classification principles;
- relationships among elements;
- time, cycles, and stages;
- generation and inhibition;
- original domain of application;
- historical context;
- competing interpretations and limits.

Choose one of four uses.

1. **Structural model:** Examine relationships and placement across the target.
2. **Consistency model:** Examine the behavior of a single target by comparison with an externally supplied type.
3. **Temporal model:** Examine timing, cycles, accumulation, recurrence, and phase change.
4. **Transition model:** Treat the framework as a state machine and run its transitions over the target. Look for states never reached, transitions that never fire, and states entered but never left.

Define the use first and make evaluation criteria explicit. **The transition model lays the framework's states over the search space as a grid and reads the target by which cells fill and which stay empty.** It looks at where things can move rather than at static placement, so declare it separately from the structural model. The procedure is in `02a-framework-application.md`.

**The temporal and transition models produce structure that static placement cannot. Reach for them.** A placement diagram gets you as far as which element sits where. Following each factor's change of state gets you when it enters and when it leaves, whether it can return, and which orderings are the only ones that occur. **Those are properties of the target, and placement does not show them.**

Before detecting absence or bias, determine whether the framework's elements and the target's structural units are of the same kind. Only compatible units support reasoning about missing or overrepresented elements. For example, if an external framework uses types as its units while the target uses individual events, the units are heterogeneous even if their counts look comparable. Do not infer absence from that pairing; use it only for candidate relations or questions.

**Compatibility is a property of the framework paired with a layer, not of the framework.** One framework can be compatible at one layer and incompatible at another. Do not write that a framework is compatible without saying at which layer. **Units of the same kind still make an incompatible pair when the principle of division differs.** Where the framework divides its positions by order and the target divides itself by something else, no absence follows.

When structural units differ, treat exhaustive review as a search for analogous relationships and sampling as a test for coincidental matches. Do not use either as evidence of absence.

For heterogeneous frameworks, switch to one of these uses:

- obtain verbs that express relationships;
- establish contrast axes;
- generate expression candidates.

Before adopting a framework, define results that would lead to rejection. Exclude frameworks that fit every possible result, because they add confirmation without discriminating hypotheses.

**A framework you decide to adopt goes on to `02a-framework-application.md`, which holds the assignment procedure and the four post-adoption checks. A finding that has not been through those checks is not a result.**
