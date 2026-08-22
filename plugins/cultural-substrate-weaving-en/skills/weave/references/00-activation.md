# Detailed Activation Decisions

Read this file when deciding activation scope, implicit activation, explicit invocation, or early termination.

## 0. Decide whether to activate

Activate the method when it is likely to provide a **meaningful increment over domain-specific methods**. For implicit activation, prioritize precision so the method does not interrupt unrelated work.

**Do not make non-activation the default for an evenly balanced decision.** Left balanced and unactivated, whether an increment existed goes unmeasured and stands as "no increment." The return on an untried move cannot be measured, so that verdict is self-fulfilling. When the decision is balanced, **try it at the cheapest scope and measure.** Under implicit activation, try limited application where the cost of interrupting is low; where that cost is high (see "Conditions for prioritizing ordinary methods" below), run the ordinary procedure first.

Choose one of three scopes.

1. **No activation:** Achieve the objective using domain-specific methods.
2. **Limited application:** Use only the required examination, such as character consistency, temporal structure, missing connections, or irreversibility.
3. **Full application:** Perform structural exploration, target-side validation, and transformation into a target-specific procedure as one sequence.

Use limited application when the target's primary change structure is already defined and the examined aspect can be separated from other structures. Use full application when the change structure itself must be defined, when multiple dimensions change one another's states, or when an irreversible decision must be examined across the target as a whole. When the decision is close, begin with limited application and expand only after target-side increment is confirmed.

### Required conditions for implicit activation

All five conditions must be met.

1. **The problem space is open:** no single answer settles it, the candidates worth exploring cannot be enumerated in advance, and fixing the destination is itself part of the work.
2. **The task concerns structure:** Its purpose is creation, design, revision, modeling, causal analysis, or structural review.
3. **Multiple dimensions interact:** At least two among elements, actors, relationships, time, responsibility, value, and constraints are handled together.
4. **Target-side validation is possible:** The resulting structure can be compared with facts, purpose, intent, requirements, or field conditions of the target.
5. **An outcome beyond ordinary analysis is plausible:** The method may generate a new judgment, design candidate, falsification condition, or research question.

**The first condition is the load-bearing one.** A closed problem space — one where an answer can be settled, the candidates enumerated, and verification decides the matter — is served by ordinary methods. Holding structure, interacting dimensions, and verifiability is not enough on its own: **a closed problem space satisfies two through five and still fails at the first.** Analysing an industry's structure, designing what a product should be worth, working out the shape of something not yet made — a search space that is wide and a destination that is undecided — is where this method belongs.

### Conditions for prioritizing ordinary methods

Use ordinary domain-specific methods for:

- simple proofreading, rephrasing, shortening, summarization, or translation;
- fact checking, search, numerical calculation, or format conversion;
- routine implementation, dependency updates, formatting, or execution of a known procedure;
- a local bug with a limited cause and impact range;
- work whose objective can be met by standard methods alone;
- work lacking the facts or conditions needed to validate structural hypotheses;
- emergency response, safety assurance, legal deadlines, or other work where established procedures must come first.

Decide activation from these conditions, not from words in the request. Terms such as “structure,” “culture,” “framework,” or “deep layer” are supporting signals only.

### When the user explicitly invokes the method

**Explicit invocation replaces the activation decision.** Do not decline an explicitly invoked activation on the prediction that the increment will be small. Declining leaves the increment unmeasured, and the verdict "it was not needed" fulfills itself. An explicit invocation is an entrusted scope, and narrowing it on a prediction is the excessive self-restraint the five required constraints forbid. What gets adjusted is the scope of application, not whether to activate.

- If an increment is plausible, choose limited or full application.
- Where ordinary methods appear sufficient, **still run limited application.** Write out what ordinary methods yield as the baseline first, then show what was added to it. If nothing was added, report "limited application run, no increment." **Do not skip it at the prediction stage.**
- If validation material is insufficient, retain framework-derived readings as hypotheses and state the information or research questions needed.

When choosing a scope narrower than the one specified, say so and give the reason. Ground the reason in what was measured on the target, not in what was predicted.

### Stopping conditions after activation

Stopping is decided by **whether the material has run out.** Reduce scope or terminate when any of the following occurs:

- **no new card is raised** — further passes bring no new unit up out of the material;
- **the increment that comes out duplicates what is already there;**
- **the framework returns the same result** — laying the position layer over the target points nowhere the baseline did not;
- the baseline alone achieves the objective;
- no framework with structural units compatible with the target can be identified;
- target-side validation material is insufficient.

**Cost is not a stopping condition.** Whether analysis cost or explanation burden outweighs the increment is not this method's judgment to make. Whether to let an exploration run long or cut it off is **the human's decision**, weighing spend against expectation. This method judges only whether the material is exhausted.

Where usage limits are tight, the human sets a pass count or a budget up front and hands it over. The method assumes an environment without a hard ceiling.

Record the activation decision and stopping reason in the internal work record. When non-activation or early termination affects the user's expectations, state the conclusion and reason briefly.
