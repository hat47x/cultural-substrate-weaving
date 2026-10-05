# Scholastic disputed-question candidate profile

Status: profile-ready / research-only

## Identity

- names: disputed question / quaestio disputata / scholastic disputation / quaestio method
- current scope: Latin medieval university disputation and its literary realization, especially the 13th-century disputed-question form and Aquinas's use of it
- intended CSW use: preserve materially different objections, make a proposed determination answer them one by one, and expose when a main rationale leaves an objection untouched
- not intended use: theological authority transfer, generic debate scoring, or a claim that one scholastic form represents all medieval intellectual practice

## Source basis

### Scholarly reference — literary and institutional form

Stanford Encyclopedia of Philosophy, "Literary Forms of Medieval Philosophy", section "Disputation, Quaestio, Quodlibetal Question".

https://plato.stanford.edu/entries/medieval-literary/

The entry describes disputed questions as a regular teaching and research form in the medieval university. Arguments on opposing sides were brought forward; the master later made a determination and responded to the opposing arguments. It also distinguishes ordinary disputed questions from quodlibetal disputations and warns that literary forms and actual classroom events are not identical.

### Scholarly reference — Aquinas's characteristic use

Stanford Encyclopedia of Philosophy, "Thomas Aquinas".

https://plato.stanford.edu/entries/aquinas/

The entry describes Aquinas's characteristic disputed-question structure: arguments on one side, a contrary position, a main reply, and replies to the initial arguments. It explicitly notes that the carefully composed written works should not be treated as literal transcripts of classroom debate.

### Primary-work translation — article form

Thomas Aquinas, *Summa Theologiae*, Prima Pars, question 2, article 2, "Whether it can be demonstrated that God exists?"

https://www.newadvent.org/summa/1002.htm

The article visibly preserves multiple objections, a contrary position, the main response, and separate replies to each objection. CSW uses this only as evidence of the literary structure; the theological propositions are not transferred into target domains.

## Structural core

The useful CSW structure is **objection-preserving determination**, not "argue both sides" in general.

A working minimum is:

1. pose one explicit question or thesis;
2. preserve materially different objections as separate objects rather than summarizing them into one opposition;
3. record a contrary consideration or counter-position without treating authority quotation as target evidence;
4. make a determination / main response;
5. return to each earlier objection and answer it individually;
6. keep an objection visible when the determination does not actually answer it.

Historical forms vary, and actual university disputations, reportationes, quodlibetal questions, and carefully composed summa articles should not be collapsed into one invariant procedure.

## Candidate operations

### question-boundary

Turn a broad disagreement into one inspectable question before trying to resolve it.

### objection-preservation

Keep distinct objections separate. Do not replace three different failure modes with a single "counterargument" summary.

### adverse-case coverage

Ask whether the proposed determination addresses every materially different objection or merely restates the preferred thesis.

### pointwise-reply

Require a reply that names the objection it answers and explains the bridge from the determination to that objection.

### distinction-before-dismissal

When an objection and the determination seem incompatible, test whether the conflict depends on two senses, scopes, actors, times, or conditions before declaring one side simply wrong.

### unresolved-objection carry-forward

If an objection survives the determination, keep it as an unresolved item rather than manufacturing a reply.

### determination-vs-authority separation

Keep the adopted reasoning distinct from cited authority, institutional preference, or a rhetorically convenient "on the contrary" statement.

## Useful outputs

- explicit question card;
- objection set with stable identities;
- determination candidate;
- pointwise reply map;
- unanswered-objection residual;
- scope / term distinction;
- counter-evidence request;
- "main rationale does not answer objection O3" diagnostic.

## Target-return questions

- What exact question is being decided?
- Which objections are genuinely different failure modes rather than paraphrases?
- Does the proposed answer address each objection, or only the easiest one?
- Which objection would still stand if the main thesis were granted?
- Is a reply changing the meaning, scope, actor, time, or condition of a key term?
- Is an authority citation being used where the target requires evidence?
- Which objection remains unresolved after the determination?
- If the scholastic labels are removed, is there still an inspectable question → objections → determination → pointwise replies structure?

## Distinction from nearby CSW frameworks

- **Classical stasis theory** asks what kind of dispute is live: fact, definition, evaluation, competence/procedure. Scholastic disputation instead asks whether a determination has faced and answered the articulated objections to one question.
- **Nyāya five-member inference** exposes the inferential bridge from thesis and reason through example/application to conclusion. Scholastic disputation is organized around a question and multiple adverse arguments, followed by pointwise replies.
- **Mīmāṃsā hermeneutics** helps inspect prescriptive sentence meaning, context, purpose, and apparent rule conflict. Scholastic disputation does not provide a norm-interpretation rule; it structures opposition and response.
- **Catuṣkoṭi** can reopen proposition space beyond a binary frame. Scholastic disputation does not supply alternative truth-value structure.
- **affinity-synthesis** may group or integrate objections after material-led analysis. CSW should not use scholastic disputation as a substitute for that synthesis layer.

## Historical / institutional boundary

- The disputed question was an institutional teaching and research form of medieval universities, not a timeless universal argument protocol.
- Ordinary disputations, public/quodlibetal disputations, written reportationes, and literary imitations such as the *Summa Theologiae* differ.
- The master's determinatio reflects an institutional asymmetry. CSW must not import that hierarchy as a rule that one actor has epistemic authority over the target.
- Arguments from recognized authorities belong to the historical method. In CSW target return, an authority quotation remains provenance or argument material and does not become target-side evidence merely because the historical form gave it a formal place.
- Aquinas is a particularly well-documented realization, not the definition of all scholastic disputation.

## What not to import by default

- Christian theological propositions or doctrinal authority;
- the master/student hierarchy as a target governance rule;
- the assumption that every question must end in one determination;
- the assumption that all objections can be reconciled by terminological distinction;
- "sed contra" as permission to answer evidence with authority;
- the assumption that the longest or most elegant reply has addressed the objection;
- the assumption that objections written by an author state that author's own view.

## De-binding route

Before returning a disputed-question pass to the target:

1. remove Latin labels unless provenance matters;
2. restate the question in target vocabulary;
3. preserve objections as target-side concerns with stable identities;
4. replace historical authority with the actual target evidence or accepted constraint, if any;
5. state the determination as a candidate decision or explanation, not truth by form;
6. map every reply to the exact objection it addresses;
7. keep unanswered objections as unresolved residuals;
8. separate target-supported replies from framework-generated distinctions.

## Runtime decision

Do not adopt into runtime yet.

The same-target comparison now shows strong structural distinctness from classical stasis theory and Nyāya, but only weak-to-moderate distinctness from a mature ordinary design-review baseline.

The residual contribution is narrower than "adversarial review" in general:

```text
stable objection identity
  -> candidate determination
  -> pointwise reply coverage
  -> unresolved objection carry-forward
```

This is useful when review comments are being collapsed, globally answered, or silently dropped. It is redundant when the caller already maintains stable concern IDs, pointwise responses, and explicit unresolved-item carry-forward.

Runtime adoption therefore remains on hold. The next adoption decision should ask whether CSW needs this portable objection-coverage primitive often enough to justify a runtime framework, rather than treating cultural distinctness or historical richness as sufficient reason.

Worked examples:

- `research/framework-candidates/worked-examples/scholastic-disputed-question.md`
- `research/framework-candidates/worked-examples/scholastic-disputed-question-negative.md`
- `research/framework-candidates/worked-examples/scholastic-disputed-question-comparison.md`
