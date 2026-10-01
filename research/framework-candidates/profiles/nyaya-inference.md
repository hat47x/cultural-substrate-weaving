# Nyāya inference candidate profile

Status: profile-ready / research-only

## Identity

- names: Nyāya / ニヤーヤ
- scope: classical Nyāya inference and argument structure, especially the five-member presentation used in polemical or didactic contexts
- intended CSW use: unfold compressed arguments, separate reasons from general rules, and make application steps visible

## Source basis

### Scholarly reference

Stanford Encyclopedia of Philosophy, Logic in Classical Indian Philosophy

https://plato.stanford.edu/entries/logic-india/

Useful for the history of Indian reasoning and the Nyāya-sūtra as a foundational source for Nyāya logic.

### Scholarly reference

Stanford Encyclopedia of Philosophy, Epistemology in Classical Indian Philosophy

https://plato.stanford.edu/entries/epistemology-india/

Useful for keeping inference inside the broader pramāṇa / knowledge-source context rather than treating it as detached formalism.

### Scholarly reference

Internet Encyclopedia of Philosophy, Nyaya

https://iep.utm.edu/nyaya/

Useful for the five-member argument and the distinction among thesis, reason, example/concomitance, application, and conclusion.

## Structural core

For public, polemical, or didactic reasoning, a classical Nyāya presentation can distinguish:

1. pratijñā — thesis;
2. hetu — reason;
3. udāharaṇa / dṛṣṭānta — general relation illustrated through an example, classically including positive and negative comparison;
4. upanaya — application of that relation to the case at hand;
5. nigamana — conclusion.

The CSW value is not "use five bullets." The value is that an apparently direct claim can be unfolded into different epistemic jobs.

## Native operation candidates

### argument-unfolding

Expand a compressed claim into thesis, reason, rule/example, case application, and conclusion.

Questions:

- Which step is currently hidden?
- Is the conclusion merely repeating the thesis?
- Does the stated reason actually connect to the conclusion?

### reason-rule-separation

Separate "this case has feature X" from "cases with X are related to Y."

Questions:

- Is the reason an observation about this case, or a general rule?
- Which part would need independent support?

### example-counterexample-probe

Use positive and negative cases to inspect the proposed relation.

Questions:

- What is a case where the relation appears to hold?
- What is a nearby case where it should not hold?
- Does the supposed general relation survive both?

### rule-application-audit

Inspect the move from a general relation to the present case.

Questions:

- Has the case actually been shown to meet the rule's condition?
- Is a hidden exception being ignored?
- Has a category changed between the general statement and the application?

### inference-gap-detection

When the five jobs are externalized, preserve any missing bridge as a gap instead of filling it from intuition.

Outputs:

- missing-premise question
- counterexample
- scope condition
- unsupported application
- residual

## What not to import by default

- Nyāya as a complete representation of all Indian logic;
- the five-member form as a universal modern proof standard;
- theological or metaphysical conclusions from Nyāya texts into unrelated targets;
- the assumption that a well-formed argument is therefore sound or true;
- pramāṇa as a generic checklist detached from its philosophical context;
- later Navya-Nyāya developments as if they were identical to early/classical Nyāya.

## Exploratory prompts

- What exactly is the thesis?
- What observation or reason is offered for it?
- What general connection is being assumed?
- Which positive and negative examples test that connection?
- Has the general connection actually been applied to this case?
- Which step would fail first if the conclusion were wrong?

## De-binding

Before returning to the target:

1. remove Nyāya terminology unless needed for provenance;
2. preserve the five epistemic jobs only where they clarify the target;
3. convert examples into target-side comparison cases;
4. mark unsupported general relations as hypotheses;
5. do not upgrade argument structure into evidence quality.

## Adoption gap

The profile is ready to be used as a research candidate without web lookup for the core operations above.

Before runtime adoption, add:

- a compact note on hetvābhāsa / reason failures without turning the dossier into a generic fallacy catalog;
- at least one target-return example outside philosophy;
- a clear boundary between early/classical Nyāya and later Navya-Nyāya.
