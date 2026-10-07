# Classical stasis theory discovery-value comparison

Status: retrospective runtime requalification / discovery-value comparison

## Purpose

The prior demotion established that a deliberately constructed target-language issue table can reproduce the de-bound stasis operations.

That is a **capability-overlap** result.

This comparison asks the missing question:

> before stasis contact, would an ordinary incident / postmortem review naturally select issue-type discrimination and stasis-switch detection, or was that specialist issue table chosen because the stasis output had already revealed the cognitive job?

## Fixed target

After a release incident:

- one participant says rollback never happened;
- another says the action should not count as a rollback;
- a third accepts the event but argues it was justified;
- a fourth argues that only the incident commander had authority to decide.

The four claims occur in the same review conversation and appear, at first glance, to be competing answers about one incident.

## Ex-ante generic incident baseline

Do not name stasis theory and do not predefine an issue-type table.

Use a normal incident/postmortem structure:

- summarize what happened;
- establish impact;
- reconstruct the timeline;
- identify trigger and contributing causes;
- record mitigation and recovery;
- inspect responder decisions and roles;
- identify lessons learned;
- create corrective actions.

This is a strong and useful baseline.

Google SRE postmortem guidance centers incident record, impact, root causes / trigger, recovery efforts, preventive actions, and data-backed conclusions.

Atlassian's incident-postmortem guidance similarly foregrounds summary, timeline, root-cause analysis, impact, lessons learned, and corrective actions.

Sources:

- Google SRE Workbook, Postmortem Culture: https://sre.google/workbook/postmortem-culture/
- Google SRE Book, Postmortem Culture: https://sre.google/sre-book/postmortem-culture/
- Atlassian, Incident Postmortem Process: https://www.atlassian.com/incident-management/postmortem/templates

These practices can capture all four statements as incident material. They do not, by themselves, require the reviewer to classify each disagreement by **what kind of question it is answering**.

## What the generic baseline can do

The generic baseline can establish:

- whether logs show a rollback-like action;
- what the runbook says;
- what decisions responders made;
- who held incident roles;
- why the incident unfolded;
- what action should change.

A careful reviewer may notice that the participants are talking past one another.

But the baseline does not necessarily force the distinction:

```text
did it happen?
what counts as "rollback"?
was it justified?
who had authority to decide?
```

Nor does it necessarily require every rebuttal to declare which of those questions it answers.

## Stasis contact

A de-bound stasis pass asks first:

> What kind of issue is live?

It then separates:

- fact / occurrence;
- definition / classification;
- quality / evaluation;
- procedure / competence / authority.

The important discovery is not the four labels themselves.

It is the realization that the apparent single dispute contains **different answer-types with different evidence requirements**.

The pass also exposes a second job:

> Has a reply silently switched issue type while appearing to refute the prior claim?

## Post-contact specialist baseline

Once issue-type separation is visible, the ordinary issue table from the prior comparison becomes an excellent implementation:

| issue | target-language question |
|---|---|
| observed event | what happened? |
| classification | what operational definition applies? |
| evaluation | was the action acceptable / justified? |
| authority / process | who could decide, under which rule? |
| evidence | which record can answer this issue? |
| unresolved | what remains open? |

This table reproduces the capability.

The provenance sequence is therefore:

```text
generic incident review
  -> timeline / root cause / decisions / roles
  -> one mixed disagreement can remain
stasis contact
  -> issue-type mismatch becomes explicit
  -> stasis-switch detection becomes explicit
  -> target-language issue table becomes the specialist implementation
```

## Ex-ante comparison

| Cognitive job | Generic / ex-ante incident review | Stasis contact | Incremental discovery |
|---|---|---|---|
| establish event facts | strong | fact / conjecture issue | low |
| inspect terminology / classification | possible when disputed | definition issue | moderate |
| separate evaluation from fact | often implicit, not structurally required | quality-after-concession | moderate |
| separate authority/process from substance | roles/runbook are reviewed, but issue separation is not guaranteed | competence/procedure | moderate |
| detect parties answering different question types | not a standard postmortem field | stasis-switch detection | high |
| bind evidence relevance to live issue type | evidence is collected, but may be reused across mixed issues | issue-specific evidence | high |
| ask whether disagreement remains after conceding one issue | not usually a default postmortem move | fact/definition/quality progression | high |

## Target-return residual

After removing Greek / Latin rhetorical vocabulary, useful questions remain:

- Which exact question is each participant answering?
- If the event is conceded, what disagreement remains?
- If the definition is fixed, what disagreement remains?
- Is a policy document being used to answer a factual timeline question?
- Is log evidence being used to answer a normative justification question?
- Is a procedural objection being mistaken for denial of the event?
- Did the conversation shift issue type without acknowledging the shift?

These are directly usable in an incident review and are not merely historical provenance.

## Discovery-value result

The retrospective discovery review supports a **distinct discovery contribution**.

The prior ordinary issue-triage baseline can reproduce the stasis output once the issue-separation job is already known. But common ex-ante incident/postmortem structures do not force reviewers to identify issue-type mismatch or stasis switches before evaluating the competing claims.

On this target, stasis contact changes the review object from:

> four people disagree about the rollback

to:

> four people are answering four different questions, and the evidence for one question cannot settle the others.

That change survives de-binding and materially changes what the reviewer asks next.

## Runtime consequence

The original capability-overlap evidence remains valid, but the original demotion rationale is incomplete under the revised discovery-aware standard.

For the tested disagreement target:

- specialist issue triage reproduces the capability after selection;
- generic ex-ante incident review does not reliably select issue-type discrimination;
- stasis contact exposes issue-type mismatch and switch detection at low selection cost;
- the resulting questions survive target return.

Therefore **runtime restoration is supported** under the discovery-aware standard.

Preserve the non-activation boundary: do not activate stasis merely because an incident or disagreement exists. Activate it when the missing cognitive job is locating what kind of question is actually disputed or detecting an unacknowledged issue switch.
