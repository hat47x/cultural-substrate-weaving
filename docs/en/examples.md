# Worked examples

Records of the method actually being applied. These are **measurement records rather than a display of successes**: each one states what ordinary methods alone produce (the baseline) before showing what was added to it.

**There are three cases so far. One is a record of misapplying the method, one is borderline, and only the third meets the method's own precondition. That is not enough to establish that it works.**

**Do not read the counts as a score.** A removal-check count is a guard against overclaiming, not a measure of value (see [02a](../../src/en-US/methods/framework-application.md)). The tallies below exist for one direction only: nothing survived, so withdraw the claim.

**This method is for open problem spaces.** Where an answer can be settled and the candidates enumerated, ordinary methods suffice. Its purpose is to get past the point where repeating the same move stops paying — not to produce more from the same number of tokens. Getting past that point takes more passes, not fewer.

---

## Case 1: structure of a validation suite (**a record of misapplication**)

> **This case is out of scope.** It fails the first activation condition in `00-activation`, that the problem space be open. A validation suite is a closed problem space — an answer can be settled, the checks enumerated, and verification decides the matter — so ordinary methods suffice.
>
> **The text at the time permitted this misapplication.** Activation turned on structure, interacting dimensions, verifiability, and plausible increment, and asked nothing about how open the problem space was. This case is what added the first condition, so it is kept as a record of the failure.
>
> What follows is preserved as it was judged at the time. **The findings hold, but they do not demonstrate the method's value** — the substitution check already reported that they were not specific to the framework, which is the expected result in a closed problem space.

**Target**: `scripts/validate.py` in this repository — a validation suite of ten check functions.

**What must not break**: `make check` completes in about a second, needs no network, and does not require the plugin to be installed.

**Primary change structure**: a change to the source travels through generated artifacts into the user's environment, and the checks are what stop it.

### Baseline (ordinary code review)

1. `check_translation_hashes` verifies only that the English file **exists**. An empty file passes.
2. `check_semantics` searches the concatenation of all files. A required phrase that migrates into the wrong file still passes.
3. `check_modules` compares bytes, but only for the OpenAI tree under `dist/`. **The `plugins/` tree that users actually install is never content-compared.**
4. `check_versions` does a substring search on `pyproject.toml`. A dependency pinned to the same version string would satisfy it.
5. `check_budgets` reads the `plugins/` SKILL.md for **size only**, never content.

### Framework pass

**Framework**: the six lines of a hexagram. **Use**: structural model.

**Unit compatibility**: the framework's units are ordered positions; the target's units are ordered stages in a pipeline. Same kind of unit, and the same principle of division (position within a progression), so they are compatible at the position layer.

**External convention**: assign each check to the position matching **the layer of file it reads**. This follows mechanically from the paths the code opens, so it is a counting predicate.

| Position | Layer | Checks |
|---|---|---|
| 1st | Source | `check_json_files`, `check_locale_parity` |
| 2nd | Translation | `check_translation_hashes` |
| 3rd | Semantic content | `check_semantics` |
| 4th | Generated | `check_modules`, `check_budgets` |
| 5th | Packaged catalogue | `check_claude_marketplace`, `check_codex_marketplace`, `check_m365` |
| 6th | — | **empty** |

**Sensitivity of the stipulation**: assigning by the layer a check *protects* rather than the layer it *reads* moves `check_budgets` toward the 4th/5th boundary. **The 6th stays empty either way**, so the empty position does not rest on the stipulation.

**Which kind of empty**: candidates exist — the artifact really is consumed — but the relation is never named. That is a gap in the description, so there is something to go and get.

### Finding

**No check reads the artifact as the consumer receives it.** Whether the SKILL.md frontmatter parses, whether a cross-reference inside a reference file resolves in the installed layout, whether the plugin loads at all — none of these are checked.

### The four checks

- **Inversion**: do `check_m365` or `check_claude_marketplace` already cover the 6th? Both inspect the package, not the consumed state. A tool that would cover it (`claude plugin validate`) exists but is not wired into `make check`. **Not refuted; the attempt strengthened it.**
- **Substitution**: a plain pipeline model (source → build → package → ship) surfaces the same absence. **Nothing about this framework in particular was needed for it.** The finding still stands.
- **Misfit record**: the hexagram supplies correspondence between paired lines and the centrality of the 2nd and 5th, neither of which maps onto a check pipeline. Those are listable before looking at the target, so they are subtracted. After subtraction no further misfits appeared — **which means the framework was barely tested.**
- **Removal check**: delete every hexagram term. "Nothing in `make check` reads the artifact in the form the consumer receives it" stands as a statement about `validate.py`. **One surviving finding.**

### Verification

The finding was confirmed against a real failure. Earlier in the same session a reference file was written with `[02a-framework-application.md](methods/framework-application.md)` inside it. `make check` passed — but the build rewrites links only in the router, not inside reference files, so the link would have shipped dead. It was caught by reading `build.py`, not by any check.

A `check_reference_links` check was added from the finding, and the same bug was re-injected to confirm detection:

```text
ERROR: Unresolvable link in installed layout:
  plugins/cultural-substrate-weaving-ja/skills/weave/references/02-system-selection.md
  -> methods/framework-application.md
```

### Honest accounting

| | Count |
|---|---|
| Baseline | 5 |
| Surviving the removal check | 1 |
| Of those, specific to the framework | **0** (substitution shows a plain model finds it) |

What the framework did was force the question **"is there a position after the last one?"** The baseline's check-by-check reading never asked it. The finding does not depend on the framework; the question did.

> Note: `AGENTS.md` forbids applying this method automatically to routine repository maintenance. This case is a deliberate application for validation, not automatic application to routine work.

---

## Case 2: structure of an operations policy (analysing existing text)

**Target**: a 15-line on-call policy for first-response to customer enquiries. Rotation is daily; the on-call engineer remains the customer's single point of contact even after escalating; response records are one line each and aggregated monthly as counts.

**What must not break**: the 30-minute first response, the single point of contact, and keeping implementation work off the on-call engineer's day.

### Baseline (ordinary review)

No after-hours coverage; no definition of "cannot answer"; no deadline on escalated cases; no rule for when an urgent swap cannot be agreed; monthly aggregation produces counts with no stated use; no handling of mid-month absence; no exceptions named for the "as a rule" clause. Seven findings.

### Framework pass

**Framework**: the five Confucian relations. **Use**: structural model. **External convention**: for each relation, a counting predicate on whether the corresponding pair of actors is named in the policy.

| Position | Assignment | State |
|---|---|---|
| Ruler–subject | Manager and on-call | Present |
| Husband–wife | On-call and owning engineer | Present |
| Friend–friend | On-call to on-call | Partial (same-day swap only) |
| Elder–younger | Yesterday's and today's on-call | **Empty** (gap in the description) |
| Parent–child | Succession, induction | **Empty** (gap in the description) |

### Findings and removal check

1. **Daily rotation structurally contradicts the single-point-of-contact promise.** The engineer holding an escalated case is a different person tomorrow, and no handoff is defined.
2. **No path carries judgment to the next engineer.** Where the line falls varies by person, records are one line, and only counts are aggregated.

Delete every Confucian term and both still stand as statements about the policy. **Two surviving findings.**

The second appears as a **connection between** two baseline findings — "no definition of cannot-answer" and "counts only". The baseline listed both and did not join them.

### Honest accounting

| | Count |
|---|---|
| Baseline | 7 |
| Surviving the removal check | 2 |

---

## Case 3: planning a short story (an open problem space, controlled)

> **All three arms have converged, and a three-way blind verdict has been taken.**
>
> For the record: the treatment first stopped on a **session usage limit**, not because its material ran out. I evaluated it at that interruption point and recorded a negative conclusion — the self-fulfilling verdict `00-activation` names, since the return on an untried move cannot be measured. On resuming, **the central claim moved right after that interruption point (passes 9–10).** That mistake produced one correction to the method (Observation 7).
>
> The original control had also written only once. Since the hypothesis is about getting past a plateau that plain repetition hits, **the correct control is repetition without the method.** A third arm was added (Observation 8).
>
> The appendix keeps the verdict taken at the unconverged point, **not overwritten, as a record of what the wrong judgment looked like.**

**This is the only case so far that meets the precondition.** Planning a story admits no settled answer, its candidates cannot be enumerated, and fixing the destination is part of the work.

### Design

To secure independence, **three agents that shared no context** were used.

| Role | Condition |
|---|---|
| Control | The premise only. Knows nothing of the method |
| Treatment | The same premise, plus full application of the method |
| Judge | Both plans anonymised into a matched format. Knows nothing of the method |

Premise: **"A small factory in a provincial city closes down. A short story covering that year."** Plan plus a 2,000-character opening.

### Observation 1: both landed in the same place

**Both agents independently titled the piece after the riser** — the sacrificial reservoir of molten iron set above a casting to feed its shrinkage, cut off after solidification and melted down again. Both made it the central metaphor.

More telling: **the baseline the treatment agent wrote for itself was structurally the control's plan** — four seasons, decision to notice to last job to removal, closing on traces in the floor. Its own assessment of that baseline:

> This plan works. But the structure is already known. The search has set into a single groove. Every scene is doing nothing but heading toward the ending; not one scene carries two functions.

**A local optimum exists, and independent attempts converge on it.** That is the method's own precondition, observed.

### Observation 2: the central claim moved

The treatment adopted a Buddhist memorial-day system as a **transition model** — declaring the lineage, naming an alternative sect and the difference between them, and **recording explicitly that it had not consulted primary sources and was therefore self-reporting.**

**It measured the sensitivity of the stipulation.** Where to place the day of death comes from neither the framework nor the target:

| Placing the day of death at | Result |
|---|---|
| The dissolution resolution | Memorial days and statutory deadlines overlap; the grid loses discrimination |
| The handover of the premises | Seven of nine positions empty |
| **The last day of operation** | **Eight of nine positions filled** |

> The stipulation moves the result a long way. Every conclusion from here is therefore not about the target but **about the target given that the last day of operation is the day of death.** Do not drop that qualifier.

| | Baseline | Final plan |
|---|---|---|
| The year | April to March, chosen without noticing | Last product shipped, to the same date a year later, chosen deliberately |
| Structure | Decision, notice, last job, removal | **The closure is chapter one. The remaining eleven months are "after the end"** |
| Theme | The end of craft, succession broken | **You can choose the date of the end; the speed of ending differs by thing** |
| Opposing pole | **None** | The neighbour who complained for forty years, standing before the silent factory |

### Observation 3: two operations pointed at the same blank

The transition run found the fourteenth-day position **never reached**. Independently, the KJ integration left exactly one card in no group at all: "the person who was waiting for it to close."

> This is the only place where fragment integration and the transition model pointed independently at the same spot.

That became the opposing pole. **A grid of states and an accumulation of fragments arrived at one absence by separate routes** — which is the mechanism the method hypothesises.

Grid coverage came out at 50 per cent. The uncovered half — monthly rent, quarterly filings, the summer and new-year holidays, snow, the neighbour — was reused as "time a day-count grid cannot measure", and became the reason the second half of the story runs as sparse monthly fragments. **A misfit put to work rather than discarded.**

### Observation 4: where the frameworks ended up

| Framework | State |
|---|---|
| Memorial days | Internal scaffolding — no framework term appears in the work |
| The twenty-four solar terms | Internal scaffolding |
| Wuxing | **Rejected** — the inversion check saw every edge absorbed as supporting evidence |
| Periodic rebuilding of a shrine | Auxiliary model |

The treatment wrote, unprompted:

> The first state is empty. Do not offer that as evidence of a strict check. It is the shape of where two rules meet, not the quality of a judgment.

> Read a count of zero signs only after measuring how much of the target the work accounts for. Where the work explains nothing — money, one character's interior, anything past the year — no sign can appear either.

### Observation 5: convergence (passes 7–12)

Six further passes after resuming; total treatment spend 212K tokens.

| Pass | Use / operation | Central claim |
|---|---|---|
| 7 | Re-materialize the prose | Unmoved (3 new units) |
| 8 | Structural model (Confucian relations) | Unmoved (reinforcement) |
| 9 | Consistency model (the pre-modern "house" applied to the organization) | **Moved** |
| 10 | Rewrite the central claim | **Moved** |
| 11 | Audit the preserved items | Unmoved |
| 12 | Re-materialize the revised prose | Unmoved |

**The interruption point was pass 6. The claim moved right after it, in passes 9–10.**

The new central claim:

> **All that vanishes in a closure is one line in a corporate register.** The machines get bought and run in another factory. The skill goes with the workers who move on. (…) **What takes a year is not disappearance, but a shift into a state with no name.**

And the old theme was overturned outright — **"what broke was the corporation and the place, not the skill; the old theme was factually wrong."**

The treatment ran its own check on the move:

> Did I move this because I wanted to move it? **No.** Pass 7's blank 19 and pass 9's E-1/E-3 came from the material as things the old claim could not explain. **The material pushed.**

**Stopping condition**: "the increment duplicates what is already there" (primary) / "the framework returns what the baseline already had" (secondary). **New cards were still rising, so the first condition did not apply.** All four uses in `02` were exhausted. **Judged by the material, not by cost.**

### Observation 6: auditing the preserved items found three failures

The clause added to item 12 of `09` after the earlier blind verdict — "check each listed item against the finished work, one at a time" — **worked immediately on the very next run.**

- The headcount ("six employees") had no grounding; only four appear in the prose → corrected to five. **This was an error in the preservation list itself**, not something the work failed to honour.
- "Use the season as a working condition" was violated by one detail that only marks a date, not a working condition → **one declared violation.**
- The retention period on a record form ("five years") could not be settled → left undetermined, with a falsification condition attached.

> **Without the audit, none of these three would have surfaced.**

### Observation 7: a conclusion withdrawn

I had written that "both arms dropped the same character, so the method did not break the shared blind spot." **I withdraw that.** In the converged output:

- "The youngest person knew the closing procedures best"
- "The skill did not break — both workers carry on"

The intern moves from decoration to a structural position. **The negative verdict drawn at the unconverged point turned out to be wrong.**

### Observation 8: a third arm (iteration without the method)

Noticing the control had written only once, a third arm was added. **The hypothesis is about getting past a plateau plain repetition hits, so the correct control is repetition without the method.** A single-shot control cannot separate the effect of iteration itself from the effect of the method.

| | Single-shot control | Iterated control | Treatment |
|---|---:|---:|---:|
| Passes | 1 | 10 | 12 |
| Tokens | 57K | **163K** | 212K |
| Times the theme moved | — | 2 / 10 | 2 / 12 |
| Stopping reason | request complete | revisions became paraphrase | increment duplicated |

**The local optimum was confirmed independently a third time.** The iterated control, unprompted:

> The first plan I wrote in pass 1 was nearly identical to the existing `novel-control.md` — the same competent female clerk, the same second-generation owner, the same old craftsman, the same Vietnamese intern, twelve months, a shrinking count, ages within a few years. **That is evidence my "unexpected" choice was this task's default pull, and grounds to discard the whole vessel.**

**And the iterated control escaped the local optimum too.** It replaced the whole setting — a foundry became an offset print shop — and reached "precision has no direction": thirty-nine years of a falsified time card kept on the shelf beside the true machine log. **On fewer tokens than the treatment.**

The route out differed. The iterated control:

> Both times the theme moved, it did not move because I was trying to rework the theme. **It came out of fixing a technical failure.**

The treatment's move, in pass 9, came from following the rule "try one untried stage before stopping." **Accident versus procedure.** With n = 1 each, no claim of reproducibility follows.

### Observation 9: the three-way blind verdict

All three plans were anonymised and given to a new judge who knew nothing of the method (the earlier judge was not reused, since it had seen the unconverged version).

On the shared pull, the judge found the decisive evidence unprompted:

> **B and C, without knowing of each other, both chose a foundry and both chose the riser as their central metaphor.** A metaphor two independent plans arrive at is not a discovery but a default answer, and C loses by staking its theme on it.

On the kind of escape:

| | Verdict |
|---|---|
| Iterated control | Kept the vessel, moved off it on an **ethical coordinate** (the viewpoint character allocates zero to the man owed the most) |
| Treatment | Moved off it in **form** (the time structure that puts the closure in chapter one and the remaining eleven months "after the end") |
| Single-shot control | **Did not move off it** |

> **B moved in form, A moved in ethics. C did not move.**

On the prose: the iterated control has the highest density but its skill shows; **the treatment's "discipline of speaking only through objects is the most thorough"** (singling out "five minutes early, because the scrap bin wasn't emptied" as the standout line), though one paragraph on the hollow left by a wooden mold strays outside the viewpoint. The single-shot control explains more, and **is the only one of the three with more than one place where the viewpoint character becomes an information-delivery device.**

A year out: the iterated control leaves a proposition (it puts the reader on the side of the person who caused harm). The treatment leaves a state (the feel of an absent vocabulary; **highest ceiling, highest failure risk**). The single-shot control leaves an image (best liked, forgotten soonest).

**Stated directly**: the single-shot control is a notch weaker. **The iterated control and the treatment are not weak — they simply depend on different things** (restraint versus endurance).

### Observation 10: what all three dropped — a finding about the caller's context, not the method

> The standard answer sits deeper than the vessel or the center: in **the stance toward the premise itself.** (…) **All three plans take it as given that this factory's closing is a loss.**

Dropped: the zero-sum fact that a closure is someone else's gain in orders; the question of whether the company's not surviving might have been correct; the younger side's viewpoint; bodily harm; personal guarantees and the home put up against them. The treatment did not reach these either, across 12 passes, 212K tokens, and all four framework uses.

**But this is not a defect in the method.** It is a finding that **the request itself — "write the year a factory closes" — had already assumed loss.** How a request is framed is not the method's job. All three plans dropped the same thing because all three received the same request.

**What the skill itself is for is a framework supplying structure and that structure being returned to the target for validation.** What a request assumes, and what the model does by default, belong to **the context the caller builds around the skill.** That boundary is now stated in [AGENTS.md](../../AGENTS.md).

A clause drawn from this finding was briefly added to `01-scope-and-facts` — telling the analyst to rule on the stance a request implies — and then **reverted as a confusion of roles.** A finding from an experiment does not automatically become a change to the skill. Of the three findings this experiment produced, two belonged to the skill (auditing the preservation list; what an interrupted run is worth) and one belonged to the context.

### Appendix: the verdict taken at the interruption point (kept as a record)

As noted in Observation 5, the treatment was first evaluated at the pass-6 interruption, with only two arms (control and treatment) put to a judge. **The text below is preserved, not overwritten.** At that point, Observations 7 and 9 had not yet corrected it.

The finding that both plans used the technical intern as decoration was, at that point, treated as a defect in the method. Passes 5–7 later showed the treatment converging and the intern moving into a structural position (Observation 7), and Observation 10 showed this class of finding properly belongs to the caller's context. **The current conclusion differs from the one recorded here.** See Observations 7 and 10.

### Cost

The treatment produced about 4 times the output of the single-shot control and about 1.3 times the iterated control. **This is not a comparison at equal token spend.** It is what the method's design — run until the material is exhausted — expects.

### Limits

- **n = 1** per arm
- The treatment agent knew it was being asked to demonstrate a method, so movement for its own sake cannot be excluded
- What was compared is a plan and 2,000 characters, not a finished work. A more novel structure need not make a better story
- Both the iterated control and the treatment stopped on their own report that "the increment duplicates what is already there" — whether the material had genuinely run dry was not verified from outside
- The experiment's design, the premise, and the format shown to the judges were all mine

## Where this stands

| Case | Problem space | Standing |
|---|---|---|
| 1 Validation suite | **Closed** | A record of misapplication; fails the precondition |
| 2 Operations policy | Closed-ish | Reference only; a policy can have a settled answer |
| 3 Short story plan (three arms) | **Open** | **The only case meeting the precondition** |

**What case 3 shows**

- **A local optimum is real.** Three independent attempts — control, iterated control, treatment — first landed in the same place. A blind judge, told nothing of the experiment's design, independently named that landing "about eighty per cent of the time."
- **Escape happens without the method too.** The iterated control escaped by replacing the vessel outright, in 10 passes and 163K tokens. The treatment escaped by keeping the vessel and shifting the center, in 12 passes and 212K tokens. The judge called both "not weak, just different strengths." **The method's effect looks less like enabling escape and more like the shape the escape takes** — a formal departure a framework's structure tends to induce.
- **The route from framework to moved claim is traceable.** A consistency-model pass produced a new center, and the old theme was judged factually wrong. A transition run and a KJ integration independently pointed at the same blank — the missing opposing pole.
- **One defect in the method was found and fixed.** A preservation list is not honoured merely by being written; it has to be checked against the finished work.
- **One finding was separated out as belonging to the caller's context.** All three arms inherited the premise's emotional stance without questioning it — a fact about how the request was framed, not a defect in the method. A clause drawn from it was briefly added to the skill, then reverted (Observation 10, AGENTS.md).

**What it does not show**: on the 2,000-character opening itself, the judge read the iterated control as the densest and the treatment as merely "trustworthy." **Using the method is not shown to produce better prose.** n = 1, and the design and its reading are mine.

What is needed next is more cases in open problem spaces — industry analysis, product value work. Targets chosen by the requester make stronger evidence than targets chosen by the analyst.
