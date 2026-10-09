# Nyāya five-member inference vs Toulmin-style argument review

Status: runtime requalification / capability-overlap comparison

## Purpose

Nyāya five-member inference is useful when a fluent argument hides the bridge from a reason to a concrete conclusion.

This comparison asks the capability question:

> once that inferential-bridge job is already selected, can a strong ordinary argument-analysis method reproduce the de-bound Nyāya operations?

The discovery question is evaluated separately.

## Fixed target

A team claims:

> Configuration revision R causes the recurring batch failure because failed runs appear after R. Another service showed the same pattern, so R is the cause here too.

Target evidence is incomplete:

- R is present on failed runs;
- some successful runs also contain R;
- the comparison service had an additional condition C;
- the current batch has not yet been checked for C;
- no controlled rollback or reproduction has been run.

## Nyāya-derived pass

The de-bound pass separates:

1. thesis — R causes the batch failure;
2. reason — failures occur when R is present;
3. example / corroboration — another case associates R with failure;
4. application — the relation from the comparison case must actually apply to this batch;
5. conclusion — only after the application survives should the causal claim be restated.

It also asks for counterexamples and flags a reason that merely repeats or redescribes the thesis.

## Toulmin-style baseline

The Toulmin method separates:

- claim;
- grounds / data;
- warrant connecting grounds to claim;
- backing for the warrant;
- qualifier;
- rebuttal.

Purdue OWL describes the warrant as the assumption, explicit or implied, that links grounds to the claim. Backing can support the warrant; qualifiers and rebuttals expose conditions and exceptions.

Source:

- Purdue OWL, Toulmin Argument:
  https://owl.purdue.edu/owl/general_writing/academic_writing/historical_perspectives_on_argumentation/toulmin_argument.html

Applied to the target:

- claim: R causes the failure;
- grounds: R is present in failed runs;
- warrant: under the relevant operating conditions, R produces the failure mode;
- backing: controlled reproductions or independent cases that establish that relation;
- qualifier: only when condition C holds;
- rebuttal: successful runs with R, or failures without R.

The target application then asks whether the current batch actually satisfies C.

## Operation-by-operation comparison

| De-bound operation | Nyāya pass | Toulmin-style baseline | Residual capability |
|---|---|---|---|
| argument-unfolding | thesis / reason / example / application / conclusion | claim / grounds / warrant / backing / qualifier / rebuttal | low |
| reason-rule-separation | distinguish observed reason from relation licensing inference | grounds vs warrant | none |
| example-counterexample-probe | corroborating case and dissimilar case | backing / rebuttal / qualifier | low |
| rule-application-audit | ask whether the known relation applies here | apply warrant + qualifier to current case | low |
| inference-gap-detection | expose missing bridge or pseudo-reason | expose missing/unsupported warrant | none |
| debate-facing restatement | put argument in inspectable sequence | structured argument presentation | low |

## Important non-equivalence

This comparison does not claim that Nyāya inference is Toulmin argumentation, that dṛṣṭānta is simply backing, or that upanaya is merely a modern qualifier check.

The historical systems have different aims, epistemic settings, vocabularies, and internal theories.

The product claim is narrower:

> after de-binding, a specialist argument-analysis method can reproduce most of the target-side capability once the inferential-bridge job is already selected.

## Capability result

Capability overlap is strong.

Nyāya does not need to be retained because no other method can represent claim, evidence, warrant, counterexample, and application.

The remaining runtime question is discovery value:

> does ordinary SIer review naturally externalize the warrant and target-application steps before Nyāya contact, or does Nyāya reliably reveal that missing cognitive job?
