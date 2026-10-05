# Pāṇini rule architecture vs ordinary rule-system review

Status: structural counterfactual / no runtime promotion

## Purpose

This comparison asks whether the de-bound operations extracted from the Pāṇinian rule architecture add a distinct CSW runtime capability beyond a strong ordinary review of a rule system.

The target is the existing YAML migration example.

## Fixed target

A specification has a parent heading, "all externally emitted records", with child rules:

- remove `internal_note`;
- preserve `internal_note` for audit-retention output;
- sign after output content is finalized.

A migration splits the rules into separate YAML files. The parent scope is lost from two rules and signing is moved before transformation.

## Pāṇini-derived pass

The profile asks to:

1. expand inherited context;
2. reconstruct each rule's scope;
3. detect overlap between general and narrower rules;
4. inspect ordering dependencies;
5. separate object rules from rules about rule application;
6. return uncertainty to specification and tests.

This produces four target questions:

- was the parent external-output scope preserved in every YAML rule?
- is audit-retention an explicit exception to the deletion rule?
- is signing defined before or after transformation?
- are these relations fixed by regression tests?

## Ordinary rule-system review

Use no cultural framework.

Normalize each rule into an explicit review table containing:

- full applicability predicate, including inherited parent scope;
- effect;
- narrower/special-case predicate;
- priority or conflict-resolution rule;
- ordering dependencies;
- whether the rule changes target data or controls rule application.

Then inspect predicate overlap, missing inherited conditions, special-case conflicts, order-sensitive transformations, and the tests that establish the intended behavior.

This yields the same four target questions.

## Operation-by-operation comparison

| De-bound operation | Pāṇini-derived pass | Ordinary rule-system review | Residual difference on this target |
|---|---|---|---|
| inherited-context expansion | anuvṛtti-inspired attention | inline parent/header predicates | none |
| scope reconstruction | recover inherited domain | normalize applicability predicates | none |
| general/specific interaction | narrower-rule probe | overlap/specificity analysis | none |
| derivation-order audit | inspect ordered derivation | dependency/order analysis | none |
| metarule/object-rule separation | separate application rules | separate execution rules from priority/control rules | none |
| implicit dependency reveal | expose omitted inherited context | normalize dependencies before review | none |
| historical compressed-rule architecture | native cultural structure | absent | provenance/analogy only; no target-side capability added |

## Mīmāṃsā boundary

Pāṇini remains structurally different from Mīmāṃsā.

Mīmāṃsā asks how prescriptive units, syntactic expectancy, semantic fitness, contextual supplementation, and apparent norm conflicts should be read. Pāṇini-derived analysis foregrounds inherited scope, rule interaction, derivation order, and rules about rule application.

That distinction is real, but it does not by itself justify a second runtime framework when ordinary rule-system review already supplies the target-relevant operations.

## Result

For this SIer target, the no-framework counter-hypothesis survives.

The ordinary review reproduces every target-relevant de-bound operation and produces the same questions with less cultural and historical overhead.

Pāṇini therefore remains valuable as a sourced research example of an historically sophisticated compressed rule architecture, but this fixture does not show a distinct runtime operation for general software or policy-rule review.

## Runtime consequence

Do not promote `panini-ashtadhyayi-rule-architecture` into the general runtime corpus on the basis of inherited scope, specificity, ordering, or metarule separation alone.

Prefer ordinary rule-system normalization when the target is already a software rule engine, configuration system, policy DSL, or specification whose predicates and dependencies can be made explicit directly.

Reconsider the candidate only if a target has a genuinely compressed, inherited, textually distributed rule architecture where the Pāṇinian structure generates questions not reproduced by ordinary normalization or by the adopted Mīmāṃsā dossier.

## Product-value consequence

The Registry should not count a culturally distinct rule architecture as new cognitive coverage when standard rule analysis already supplies the same de-bound operations.

A non-promotion result is useful: it narrows the runtime corpus to frameworks that change what CSW can actually distinguish, ask, or construct.
