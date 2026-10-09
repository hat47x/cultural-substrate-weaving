# Nyāya five-member inference discovery-value comparison

Status: runtime requalification / discovery-value comparison

## Purpose

The capability comparison shows that Toulmin-style argument review can reproduce most de-bound Nyāya operations after the inferential-bridge job has already been selected.

This comparison asks the stricter question:

> before Nyāya contact, does ordinary SIer incident/review practice naturally separate the observed reason, the general relation that licenses the inference, and the application of that relation to the current target?

## Fixed target

A team claims:

> Configuration revision R causes the recurring batch failure because failed runs appear after R. Another service showed the same pattern, so R is the cause here too.

Known target material:

- R is present on failed runs;
- some successful runs also contain R;
- the comparison service had an additional condition C;
- the current batch has not yet been checked for C;
- no controlled rollback or reproduction has been run.

## Ex-ante generic incident baseline

Do not name Nyāya, Toulmin, argument mapping, or warrant analysis.

Use ordinary incident/postmortem questions:

- What happened?
- What changed?
- What is the suspected root cause and trigger?
- What evidence supports that diagnosis?
- What other contributing conditions are present?
- Can the suspected cause be reproduced, removed, or falsified?
- Are there successful cases with the same configuration?
- What preventive action follows if the diagnosis is correct?

Google SRE postmortem guidance emphasizes root causes, triggers, lower-level details, evidence, and corrective actions.

NASA mishap/RCA guidance likewise requires evidence analysis and deductive reasoning, and notes that elimination, simulation, and system-history studies may be required when evidence is incomplete.

Sources:

- Google SRE Workbook, Postmortem Analysis:
  https://sre.google/workbook/postmortem-analysis/
- Google SRE Workbook, Postmortem Culture:
  https://sre.google/workbook/postmortem-culture/
- NASA NPR 8621.1, Root Cause Analysis Methodology / Evidence and Data Analysis:
  https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_8621_0001_&page_name=AppdxI1
  https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_8621_0001_&page_name=AppdxI2

This is a strong ex-ante baseline.

It may discover condition C by comparing cases or reproducing the failure.

It does **not**, however, require the reviewer to externalize three different epistemic jobs:

1. the observation used as a reason;
2. the generalized relation that would license the inference;
3. the claim that the generalized relation actually applies to this target.

## Nyāya contact

The de-bound Nyāya pass asks:

- What exactly is the thesis?
- What observation is functioning as the reason?
- What accepted or independently checked case supports the proposed relation?
- What is the relation being generalized from that case?
- Does the current target satisfy the conditions under which that relation held?
- What counterexample narrows or defeats the proposed relation?
- After the application check, what conclusion remains justified?

On the fixed target, the key new question is:

> The comparison service failed under R + C. Do we know that C holds in this batch, or are we importing the relation from another case without checking its applicability?

That question is more specific than "do we have evidence?" It exposes **application of a warrant to this target** as a separate inspectable step.

## Ex-ante comparison

| Cognitive job | Generic incident review | Nyāya contact | Incremental discovery |
|---|---|---|---|
| identify claim | root-cause statement is recorded | thesis | low |
| inspect evidence | evidence / facts are collected | reason | low |
| search alternative causes | contributing factors / elimination | counterexample pressure | low-moderate |
| state the generalized relation linking reason to claim | often implicit | reason-rule separation | high |
| test whether that general relation applies to this target | may emerge through reproduction or domain investigation, but is not a required argument step | application audit | high |
| expose analogy/comparison misuse | possible, not structurally required | example + application separation | high |
| restate conclusion after bridge survives | often root-cause conclusion is revised | conclusion after application | moderate |

## Direct-test boundary

Nyāya should not be used when a direct target-side test already settles the causal question.

For example, if:

- reverting R reliably removes the failure;
- reapplying R reliably restores it;
- condition C is controlled;
- competing causes have been excluded;

then a separate five-member pass adds little.

The framework earns discovery value mainly when reasoning relies on:

- compressed "therefore" steps;
- analogy to another system or incident;
- an unstated generalization;
- a rule whose applicability to the current target has not been checked.

## Target-return residual

After removing Nyāya vocabulary, useful questions remain:

- What observation is actually doing the work as the reason?
- What general relation are we assuming from that observation to the conclusion?
- What independent case or test supports that relation?
- Under what conditions does the relation hold?
- Does this target satisfy those conditions?
- Which counterexample narrows the relation?
- What conclusion survives after application is checked?

These questions are not merely historical labels.

They change what the reviewer must inspect before accepting a fluent causal or architectural argument.

## Discovery-value result

A distinct discovery contribution remains on the tested target.

A specialist argument method such as Toulmin can reproduce much of the structure after selection, so Nyāya does not have unique formal capability.

But ordinary ex-ante incident review does not reliably force the analyst to separate:

```text
observed reason
  -> generalized relation
  -> application to this target
```

Nyāya contact exposes that bridge at low selection cost and makes analogy/application failure directly inspectable.

## Runtime consequence

Runtime retention is supported under the discovery-aware standard.

Retention is conditional, not universal:

- do not activate Nyāya for every argument;
- do not use it when a direct test already settles the claim;
- do not treat an example as independent evidence merely because it fits the five-member form;
- activate it when the missing cognitive job is an unstated warrant, analogy leap, or unchecked application from a general relation to the present target.

The historical five-member structure remains provenance. The runtime value is the surviving target-side inferential-bridge question.
