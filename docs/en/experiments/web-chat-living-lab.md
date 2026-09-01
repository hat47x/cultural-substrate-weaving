# Web Chat Living Lab

## Purpose

The Web Chat Living Lab is not an API benchmark for running large fixed test suites. It is an operating observation system for real writing, research, design, and analysis carried out in Web chat products such as ChatGPT.

Its purpose is not to make cultural-substrate-weaving (CSW) look effective. It preserves enough traceable material to revisit changes such as:

- the working question changed;
- a new search or observation target appeared;
- later material reorganized a KJ grouping, relation, or blank;
- something was adopted into an artifact and later withdrawn or transformed;
- an earlier residual became relevant again;
- the degree of contact with a cultural framework changed.

Record these first as **events or observable states**. Whether a change was useful, harmful, appropriate, or caused by CSW is a separate judgment.

Framework count, full-read count, native-operation count, and event count are not KPIs.

## Separate observation from evaluation

Do not collapse the following into one record:

1. **Direct observation** — a change that can be traced back to artifacts, questions, search targets, KJ arrangements, or activation state.
2. **User judgment** — an adoption, correction, rejection, withdrawal, or other judgment stated by the user.
3. **AI interpretation** — an explanation or evaluation added by the model, including claims of usefulness, harm, or causation.
4. **Measurement** — a value actually recorded in a comparison or measurement procedure.
5. **Evaluation of the measurement** — a separate judgment about what that value means.

AI judgments may be preserved, but do not merge them into user judgments or measurements. If an AI defines an evaluation axis, scores its own output, and interprets the result, keep the score and the interpretation on separate provenance paths.

## Two operating modes

### `natural_work`

Use this by default. Continue the real task without turning it into a laboratory exercise.

A round normally needs only this:

1. Notice the material delta: new sources, observations, falsification, or execution results.
2. Reopen only old residuals or isolated material touched by that delta.
3. Use KJ and cultural frameworks in the form required by the current work.
4. Observe what actually changed in the artifact, decision, research direction, or other real work.
5. Preserve residuals and reopening conditions with enough provenance to identify whose judgment they represent.
6. Record an event only when a change occurred that may matter to later review.

Do not reread the whole history or fill every record field on every round.

### `paired_check`

Use this when a method decision needs a somewhat more comparable observation of the same task.

1. Prepare the same task and source material.
2. In a fresh chat A, use the domain method without CSW as the baseline.
3. In a fresh chat B, use the same material with CSW.
4. Keep visible model label, product mode, tool access, and timing as similar as practical.
5. Record run order when several cases are compared.
6. When useful, give de-labeled outputs to a third fresh chat for comparison.

Web chat is not deterministic. A paired check improves comparability but is not treated as a strict causal experiment.

A third AI chat is not a neutral measuring instrument. Its conclusions belong under attributed `interpretations`, not under measurements.

## Paired-check records

Schema 0.2 separates comparison material into:

- `observed_differences` — differences that can be checked by referring back to the outputs;
- `measurements` — values actually recorded, together with their source;
- `interpretations` — judgments about those differences or values, with provenance.

For example, "the treatment output contains one research question absent from the baseline" is an observable difference. "The question was caused by CSW, so the treatment is better" is an interpretation.

## Round records

The machine-readable format is `evals/living-lab-round.schema.json`. See `evals/living-lab-round.example.json` for a normal round and `evals/living-lab-paired.example.json` for a paired-check example.

The record is intended to preserve only what may matter later:

- round and case identifiers;
- `natural_work` or `paired_check` mode;
- time and, where relevant, visible Web-chat environment;
- task summary and source references;
- `activation_scope`;
- actual framework contacts and `probe / preview / full / enacted` depth;
- KJ snapshot references;
- artifacts that survived into real work;
- sourced constraints, residuals, and reopening conditions;
- sourced interpretations when they are worth preserving.

`activation_scope: non_activation` records that no cultural framework was opened during that round. The state alone does not establish that non-activation was useful, harmful, correct, or incorrect.

## Event ledger

Do not create an event for every round. Record only changes that may matter to later review using `evals/living-lab-event.schema.json`.

- `question_shift`
- `search_shift`
- `kj_reconfiguration`
- `artifact_adoption`
- `artifact_withdrawal`
- `decision_change`
- `delayed_reactivation`
- `repeated_transfer`
- `framework_contact_change`

Schema 0.2 no longer uses `useful_nonuse` or `harm_detected` as event types. The former combined a state with a judgment of usefulness; the latter combined an event with an evaluation of harm.

Write the traceable change itself in `observation`. When an explanation or evaluation is worth preserving, put it under `interpretations` and record its `source_type`.

Use `retrospective` for events assigned after rereading old work and `prospective` for events observed under an already-declared observation plan. This distinction is not a quality ranking.

## `source_type`

Sourced judgments use one of these values:

- `user` — a judgment stated by the user;
- `ai` — a judgment or interpretation added by a generative-AI system;
- `external` — a judgment originating in an external source or evaluator;
- `mixed` — several origins cannot usefully be separated or jointly produced the statement;
- `unknown` — the available record does not identify the origin.

These values are provenance, not confidence scores. `user` does not mean "fact," and `ai` does not mean "worthless." The purpose is to avoid mistaking one origin for another during later review.

## Separate private records from public observations

Real round/event records are not assumed to belong in the public repository. Records that touch private chats, unpublished drafts, internal material, client information, or similar context should normally stay under `.living-lab/` or outside the repository. Everything under `.living-lab/` except its README is ignored by Git.

Only observations suitable for publication belong under `research/living-lab/observations/`. A public record should either rely only on public information or be a separately anonymized or abstracted version of a private original. Prefer opaque references such as `chat:case-a-round-3` or `artifact:draft-7` when copying source content would disclose more than the observation requires.

Publication safety and research usefulness are separate questions.

## What not to record

Observation overhead should not become heavier than the real task. Normally do not ledger:

- every message;
- every candidate framework;
- exhaustive lists of unused frameworks;
- mere rewording or explanation-volume growth;
- several derived cards as several independent effects;
- the same target finding rediscovered through several frameworks as several pieces of evidence.

Rich preservation of source material does not require copying every item into the observation ledger.

## Before promoting a finding into the method

Do not create a permanent rule from one case or from an AI's evaluation of its own output.

Before proposing a method change, return to at least the following:

1. What did the user adopt, correct, reject, or later withdraw?
2. Is there a traceable difference in the artifact, KJ arrangement, search path, or decision?
3. Did the same function appear in another real task?
4. Can the difference be explained by returning to source material rather than relying on the evaluator's judgment?
5. Is the candidate already covered by an existing rule?
6. Would an example, auxiliary note, or dynamic record preserve the finding better than another static rule?

Measurements do not bypass these questions. Keep the recorded value separate from the meaning an evaluator assigns to it.

## Web-chat-specific cautions

- Models and product modes change. Record only visible environment information; do not guess hidden versions.
- Fresh chats improve separation but do not create perfectly independent trials.
- Do not produce baseline and treatment sequentially in one chat when comparison matters; earlier output contaminates later work.
- Match Web search and connected-tool access where practical, without distorting the real task merely for experimental control.
- Long-running work will naturally cross model updates. Do not assume perfect reproducibility.

## Validation

The included examples and local records can be checked without external dependencies:

```bash
python scripts/validate_living_lab.py
python scripts/validate_living_lab.py path/to/round.json path/to/event.json
python scripts/validate_living_lab.py --record-set path/to/round.json path/to/event.json
python scripts/validate_living_lab.py --record-set research/living-lab/observations/*.json
```

The validator checks schema shape, required fields, enum values, and record-set references. **A record passing validation does not establish that an observation or AI interpretation is correct.**
