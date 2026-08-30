# Web Chat Living Lab

## Purpose

This is not an API benchmark for running large fixed test suites. It is an operating observation system for real writing, research, design, and analysis carried out in Web chat products such as ChatGPT.

The aim is not to make cultural-substrate-weaving (CSW) look good. The aim is to preserve enough evidence to revisit questions such as:

- Did the question itself change?
- Did the next search or observation target change?
- Did later material reorganize an earlier KJ grouping or blank?
- What actually survived into an artifact or decision?
- When was non-use better?
- Did a residual that looked unimportant become useful later?

Framework count, full-read count, native-operation count, and event count are not KPIs.

## Two operating modes

### `natural_work`

Use this by default. Continue the real task without turning it into a laboratory exercise.

A round normally needs only this:

1. Notice the material delta: new sources, observation, falsification, or execution results.
2. Reopen only old residuals or isolated material touched by that delta.
3. Use KJ and cultural frameworks only as far as the current question requires.
4. Observe what survives into the real artifact, decision, or research direction.
5. Preserve important residuals and reopening conditions, then close the round.
6. Record an event only when a change occurred that may matter later.

Do not reread the whole history or fill every record field every round.

### `paired_check`

Use this only when a stronger comparison is useful, for example:

- before promoting a new operation into a static rule;
- after `harm_detected`;
- when an unexpectedly strong result repeats and its conditions need checking;
- before a release containing an important method change;
- when it is useful to separate possible CSW contribution from ordinary model variation.

A paired check can be run entirely in Web chat:

1. Prepare the same task and source material.
2. In a fresh chat A, use the domain method without CSW as the baseline.
3. In a fresh chat B, use the same material with CSW.
4. Keep visible model label, product mode, tool access, and timing as similar as practical.
5. Across several cases, alternate baseline-first and treatment-first order.
6. When useful, give de-labeled outputs to a third fresh chat for comparison.

Web chat is not deterministic. A paired check improves comparability but is not treated as a strict causal experiment.

## What to compare

Do not collapse the comparison into one score. Preserve a difference map. Useful dimensions include:

- **target fidelity**: target-specific facts, exceptions, asymmetry, and irreversibility remain intact;
- **question gain**: concrete researchable questions appeared beyond the baseline;
- **provenance cleanliness**: framework-generated material was not silently converted into target fact;
- **non-forcing**: the target was not reread merely to fill the framework;
- **artifact usefulness**: the difference survived into real writing, design, research, or decisions;
- **residual quality**: unresolved material remained open in a form that later work could receive.

Scales may be used when useful, but averages and win/loss labels are not the value of the method itself.

## Round records

The machine-readable format is `evals/living-lab-round.schema.json`. See `evals/living-lab-round.example.json` for a normal round and `evals/living-lab-paired.example.json` for a positive paired-check example.

The record is intended to preserve only what may matter later:

- round and case identifiers;
- `natural_work` or `paired_check` mode;
- time and, where relevant, visible Web-chat environment;
- task summary and source references;
- activation scope;
- actual framework contacts and `probe / preview / full / enacted` depth;
- KJ snapshot references;
- artifacts that survived into real work;
- residuals and reopening conditions.

A round in which no cultural framework is opened is a normal outcome. Do not compensate for `non_activation` or equivalent non-use as if it were failure.

## Event ledger

Do not create an event for every round. Record only changes that can matter to later review using `evals/living-lab-event.schema.json`.

- `question_shift`
- `search_shift`
- `kj_reconfiguration`
- `artifact_adoption`
- `decision_change`
- `delayed_reactivation`
- `repeated_transfer`
- `useful_nonuse`
- `harm_detected`

An event is not proof of causal effect. It records what happened and which references support that observation.

Use `retrospective` for events assigned after rereading old work and `prospective` for events observed under an already-declared observation plan.

## What not to record

Observation overhead should not become heavier than the real task. Normally do not ledger:

- every message;
- every candidate framework;
- exhaustive lists of unused frameworks;
- mere rewording or explanation-volume growth;
- several derived cards as several independent effects;
- the same target finding rediscovered through several frameworks as several pieces of evidence.

Rich preservation of source material does not require copying every item into the observation ledger.

## Promoting findings into the method

Do not create a permanent rule from one successful case. Before promotion, ask:

1. Did the same function recur across different real tasks?
2. Can its benefit be described as an effect on the target or cognitive trajectory rather than by the framework name?
3. Are conditions for non-use, weakening, or harm becoming visible?
4. Is it genuinely different from an existing rule?
5. Would it be better kept as an auxiliary note or dynamic practice rather than static method content?

`repeated_transfer` is not enough by itself. Boundaries revealed by `useful_nonuse` and `harm_detected` matter equally.

## Web-chat-specific cautions

- Models and product modes change. Record only visible environment information; do not guess hidden versions.
- Fresh chats improve separation but do not create perfectly independent trials.
- Do not produce baseline and treatment sequentially in one chat when comparison matters; earlier output contaminates later work.
- Match Web search and connected-tool access where practical, without distorting the real task merely for experimental control.
- Long-running work will naturally cross model updates. The Living Lab values what survives into real work more than perfect reproducibility.

## Validation

The included examples and local records can be checked without external dependencies:

```bash
# Validate the bundled natural / paired / event examples as one record set.
python scripts/validate_living_lab.py

# Validate individual record shapes only.
python scripts/validate_living_lab.py path/to/round.json path/to/event.json

# Validate a closed set, including duplicate IDs and event -> round references.
python scripts/validate_living_lab.py --record-set path/to/round.json path/to/event.json
```

Individual validation allows an event's round to live elsewhere. With `--record-set`, the supplied files are treated as one closed record set: `round_id` / `event_id` values must be unique and every event's `round_id` must resolve within the set.

The validator does not score research quality. It checks record consistency such as required fields, identifiers, enums, paired-check references, and event evidence references.

## When to background the Living Lab

The observation system does not need to stay foregrounded permanently. Reduce recording frequency when the method is stable and continued observation produces few new boundaries or recurring patterns.

Bring it forward again when a new framework family, model generation, use domain, or previously harmful operation is introduced.
