# What the caller supplies

## What this skill does

**It uses old frameworks of thought to find the empty spots in your material.**

Frameworks like wuxing, the I Ching, or the KJ method have "slots" fixed before anyone looks at your material. When you map your material onto those slots, **some slots stay empty.** Those are the gaps worth investigating.

At the end, every framework name is deleted. Only what still holds up as a statement about your material gets reported. **Whether the framework is "true" is not the question. Whether it said something real about your material is.**

## What this skill does not do

This part matters. **The skill provides only the capability.** The following four things happen only if **you** specify them.

| The skill does | You specify |
|---|---|
| Applies a framework, finds the gaps | What your request already assumes |
| Checks each gap against the real material | The model's habits you want corrected |
| Stops when the material runs dry | How much budget to spend |
| — | Whether the finished work is any good |

## Copy this and fill it in

```text
/cultural-substrate-weaving-en:weave

[Material]
(describe the target here)

[What this request assumes]
(e.g., I wrote "the year a factory closes" — don't assume closing is a loss)

[Model habits to avoid]
(e.g., don't turn this into "both sides have a point")

[Budget]
(e.g., up to 10 passes, or "keep going until the material runs dry")

[On quality]
(I'll specify separately / not a concern this time)
```

It works with all four blank. **But whatever you leave blank, the model decides for you.**

---

## 1. What your request already assumes

The words of a request settle an answer before anyone starts writing.

| Writing this... | ...already decides this |
|---|---|
| "the year a factory closes" | closing is sad |
| "improve this design" | the current design is bad |
| "why did this fail" | it failed |

**The skill will not question this.** If you want it questioned, say so.

This was tested directly. The same premise was handed to three separate AI runs, and **all three assumed "closing = loss" without ever questioning it** — including the run using this skill.

Example wording:

```text
Write the closure not as a loss, but as business moving to a
competitor and skills moving with the workers who leave.
```

## 2. Model habits

The skill will not fix these. Useful things to specify:

- **Don't split the difference.** Where power, blame, or harm is genuinely lopsided, writing it as balanced erases the imbalance.
- **Don't soften.** "She decided" can drift into "it happened"; a flat statement can drift into a hedge.
- **Don't over-explain.** There's a habit of adding one more sentence right after landing a good line.
- **Don't default to the safe answer.** Almost any premise has an obvious answer that "anyone writing this seriously arrives at about 80% of the time." Say so if you want to avoid it.

## 3. Budget

**This skill does not stop because of cost. It stops only when the material runs dry.** That's deliberate.

Repeating the same move eventually hits a wall. **Getting past that wall is the point — not producing a better result from fewer tokens.**

- Measured: about **3 to 4 times** the output of a single pass.
- If your usage is capped, **tell it how many passes or how much budget up front.**
- If a run gets cut off partway, what exists at that point **is not a result.** Resume it.

## 4. What it's for, and what it isn't

| Good fit | Bad fit |
|---|---|
| Analyzing an industry, shaping what a product should be worth, a plan with no fixed shape yet | Finding a bug, checking spec compliance, following a known procedure |
| Deciding what the destination even is | An answer that's already settled, with countable candidates |

**If the answer is already settled, ordinary methods are enough.** Having structure, complexity, and verifiability is not, by itself, sufficient.

A record of using this on the wrong kind of problem is kept as **a record of misuse** in [worked examples](examples.md), case 1.

## 5. Quality is a separate instruction

The skill guarantees one thing: after deleting every framework name, what remains still holds up as a statement about your material. **It does not guarantee that the result is well written or well designed.**

In a three-way test, **the arm that used no skill at all — just repeated revision — also escaped the obvious answer.** It escaped differently, but a blind reader judged both as "not weak, just different strengths."

If you want better prose or a better design, say so separately.

---

## Appendix: judgments removed from the skill

These used to live inside the skill itself. **They were removed because they are not the capability** — specify them yourself if you need them.

<details>
<summary>Consideration for the reader</summary>

- Let the reader judge their own position, current state, and what might happen next
- Show what's needed to decide before the outcome happens
- Treat exposing someone or forcing a hard look as a separate kind of effect
- For anything heavy: is it needed to draw the reader in? can they step back? is a destination shown? is the intensity no more than necessary?

</details>

<details>
<summary>Value of the finished work</summary>

- **Excess capacity**: does one element do more than its assigned job?
- **Autonomy**: does it work without its creator present?
- **Regenerative value**: does re-reading it produce new understanding?
- **Non-rivalry**: did shareable value increase without using it up?
- Note what gets spent too — attention, energy, time, follow-up effort

</details>

<details>
<summary>Correcting model habits (detailed)</summary>

- Don't turn conflict into "both sides have a point." Where power, responsibility, or harm is genuinely lopsided, treating it as balanced erases that
- Treat the model's own values as an outside influence too. If softening the account for the sake of caution, **say what was changed and what was lost**
- Don't expand a delegated scope on your own — and don't shrink it out of excess caution either
- The stronger the ideology or consensus around a topic, the more it needs checking at a distance from that consensus

</details>

<details>
<summary>Craft techniques</summary>

- **Turn it into experience**: spread it across body/sense, cognition, action/relationship, environment. For harm to a real person, work out how to render it as structure first
- **Give new roles to what's already there** before adding new elements
- **Vary repetition each time**: change the relationship or function with each repeat. Control explicitness through hidden, implied, or explicit
- **Time**: what accumulates, timing, the given versus the task. Render fate-like structure as omens, repetition, and cycles
- **Humor**: separate incongruity, superiority, and release. For work that doesn't judge people, favor the first two
- **Emotion**: classify by mechanism, effect, and placement — not by the emotion's name. An earlier emotion changes how a later one reads
- **Series work**: assume the reader forgets; reintroduce what's needed, with an independent entry point each time
- **Cross-domain retelling**: build a different entry point for each audience, chosen by structural match

</details>

<details>
<summary>Output design</summary>

- Give the reader enough to judge for themselves. For multiple audiences, offer several paths to the same core content
- Place low-effort material where prior knowledge is thin
- Make the key points, minimum viable step, and resume point explicit

</details>

---

- [Worked examples](examples.md) — records of actually running this
- [AGENTS.md](../../AGENTS.md) — what belongs in the skill and what doesn't
