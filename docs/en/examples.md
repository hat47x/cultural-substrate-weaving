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

### Observation 5: the blind verdict

The judge, knowing nothing of the method, was given both plans anonymised and asked to describe where they diverge structurally, **without scoring them.**

On the common landing, independently:

> This is close to the standard answer for a contemporary Japanese short story about provincial industrial decline. Third-person limited, no emotion words, density built from technical vocabulary, one technical intern, a quiet ending. Anyone setting out to write this premise seriously in Japanese today **arrives here about eighty per cent of the time.**

**A third party confirmed the local optimum without being told one was being looked for.**

On the divergence: the control put the closure at the endpoint, the treatment at the starting point. The control gained the ninety-two-to-zero spine, an ensemble, and an outside world, and lost the inside of the decision and the after. The treatment gained the empty lot of the genre — the year that follows — a deliberately uneven time signature in which the form enacts the theme, and an antagonist; and it lost its largest scene to chapter one and pushed the employees into the background.

On the prose: the control's opening is **skilful**, the treatment's is **trustworthy**. The control has a habit of adding one more explanatory line after landing a good one; the treatment leaks poetry its viewpoint character would not have, and plants one piece of foreshadowing too visibly. **On the opening itself the judge reads the control as stronger.**

A year out: the control is likelier to be finished; **more would remain from the treatment.** Three reasons — the treatment's theme is a discovery where the control's is a confirmation; the treatment has an other and the control has none; and **only the treatment's ending is undetermined, leaving room for what the author learns while writing.** By number of memorable scenes, the control wins.

### Observation 6: the experiment found a defect in the method

The judge named what **both** plans dropped:

> Both use the technical intern as decoration. In each plan the person whose life is most upended by the closure ends as an ornament in a single scene.

The treatment had **listed "do not make this character a victim" among the things not to break.** It still failed.

**The fault is the method's.** `01-scope-and-facts` requires listing what must not be broken, and item 12 of `09-evaluation-and-domains` checked that the list was made and that local repairs had not smoothed out variation — but **nothing required checking each listed item against the finished work.** Listing does not preserve.

Item 12 now carries that check. **This is the first time an application in an open problem space produced a defect in the method itself.**

The judge also proposed the strongest synthesis: the treatment's time design, with the intern's visa expiry as the count running through it — the material both plans dropped, made the spine.

### Cost

The treatment produced about six times the output of the control. **That is what the method expects.** This is not a comparison at equal token spend.

### Limits

- **n = 1**
- The treatment agent knew it was being asked to demonstrate a method, so movement for its own sake cannot be excluded
- What was compared is a plan and 2,000 characters, not a finished work. A more novel structure need not make a better story
- The treatment hit a session limit during its final pass, with two framework uses still untried

## Where this stands

| Case | Problem space | Standing |
|---|---|---|
| 1 Validation suite | **Closed** | A record of misapplication; fails the precondition |
| 2 Operations policy | Closed-ish | Reference only; a policy can have a settled answer |
| 3 Short story plan | **Open** | **The only case meeting the precondition** |

**What case 3 shows**: a local optimum exists, and a blind third party independently put it at eighty per cent of attempts. The central claim moved. A transition run and a KJ integration pointed at one absence by separate routes. The judge expects more to remain from the treatment. And **one defect in the method surfaced** — a preservation list that nothing audits.

**What it does not show**: the control wrote the better 2,000 characters, and is likelier to finish. **Both plans dropped the same person, so the method did not break the blind spot they shared.** n = 1, and the design and its reading are mine.

What is needed next is more cases in open problem spaces — industry analysis, product value work. Targets chosen by the requester make stronger evidence than targets chosen by the analyst.
