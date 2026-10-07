# Dependent origination discovery-value comparison

Status: retrospective runtime requalification / discovery-value comparison

## Purpose

The prior demotion established that Five Whys, fault-tree analysis, dependency analysis, and counterfactual intervention can reproduce the de-bound dependent-origination operations after those jobs are named.

That is **capability-overlap** evidence.

This comparison asks the missing question:

> before dependent-origination contact, would an ordinary incident / post-incident review naturally select upstream-condition search, multiple contributing conditions, and a mitigation / cessation question?

## Fixed target

A distributed job-control service intermittently accepts work but fails to complete it after a rolling deployment.

Known evidence includes:

- credential validity;
- cached worker capability;
- heartbeat freshness;
- scheduler eligibility;
- authoritative state revision;
- queue redelivery.

The first incident summary says:

> An expired worker credential caused the failure.

## Ex-ante generic incident baseline

Do not name dependent origination, Five Whys, fault-tree analysis, or counterfactual causation.

Use ordinary post-incident questions:

- What happened?
- What components, conditions, actions, and events contributed?
- What was the immediate failure path?
- Which earlier conditions made that path possible?
- Which contributing factors were simultaneous or interacting?
- Which mitigation stopped or reduced the incident?
- What change would prevent recurrence?
- What observation should change after that corrective action?
- What evidence supports each contributing-factor claim?

These questions are not invented from the framework output.

Current reliability guidance already frames post-incident analysis around contributing factors, deeper causes, mitigations, and preventive actions.

Sources:

- AWS Well-Architected, OPS11-BP02 Perform post-incident analysis:
  https://docs.aws.amazon.com/wellarchitected/latest/framework/ops_evolve_ops_perform_rca_process.html
- AWS Well-Architected, REL12-BP02 Perform post-incident analysis:
  https://docs.aws.amazon.com/wellarchitected/2023-10-03/framework/rel_testing_resiliency_rca_resiliency.html
- Google SRE, Incident Management Guide:
  https://sre.google/resources/practices-and-processes/incident-management-guide/

AWS explicitly describes a predefined process for determining the components, conditions, actions, and events that contributed to an incident, then developing mitigations to limit or prevent recurrence.

Google SRE likewise treats postmortems as a way to document how an incident unfolded, its root causes, and corrective actions rather than stopping at the immediate symptom.

## Generic baseline on the fixed target

Without framework contact, the target naturally invites a condition-oriented investigation:

```text
attempt failed
  -> request rejected
  -> why was an unusable worker selected?
  -> what scheduler / capability / heartbeat state permitted selection?
  -> what credential-state change failed to propagate?
```

The same review also asks:

- was stale capability alone sufficient?;
- did fresh heartbeat and stale capability jointly preserve eligibility?;
- was dispatch inside a stale-state window required?;
- did queue redelivery create a later independent opportunity?;
- which corrective change removes the failure window?;
- did the failure actually cease after that change?

This baseline can remain branching rather than forcing one linear chain.

## Dependent-origination contact

The de-bound pass asks:

- what upstream conditions permit the observed state?;
- what apparently self-standing component depends on surrounding conditions?;
- what should cease or change if one relevant condition is removed?;
- which condition is observable or modifiable?;
- what target-side evidence supports the relation?

These are coherent and useful questions.

## Ex-ante comparison

| Cognitive job | Generic / ex-ante incident review | Dependent-origination contact | Incremental discovery |
|---|---|---|---|
| move beyond immediate symptom | standard contributing-factor / root-cause work | upstream-condition | low |
| expand required conditions | standard component/condition/event investigation | condition-chain | low |
| avoid single-component story | multiple contributing factors are ordinary post-incident material | dependency-reframing | low |
| identify modifiable condition | mitigation / corrective action is standard | intervention-point selection | low |
| ask whether failure stops after change | verify mitigation / recurrence prevention | cessation-counterfactual | low |
| preserve branching / multiple factors | ordinary post-incident analysis can do so directly | current chain pass needs explicit caution | no discovery advantage |
| challenge essentialized component explanation | systems/reliability review already treats behavior as configuration/state/dependency-sensitive | anti-essentialist counter-view | low for tested target |

## Target-return residual

After removing Buddhist vocabulary, the useful questions are:

- Which earlier conditions made the failure possible?
- Which factors were jointly necessary or merely contributory?
- Which condition can be changed?
- What should change after the intervention?
- Did the failure stop after that change?
- Which dependency claim is supported by logs, traces, tests, or intervention?

These questions remain useful, but they are already opened by the generic ex-ante incident baseline.

## Discovery-value result

The discovery-value counter-hypothesis survives.

Unlike classical stasis theory, where a generic postmortem can retain several incompatible answer-types without exposing the issue mismatch, this target already presents itself as a failure whose contributing conditions and prevention actions must be investigated.

The ordinary incident category therefore selects the relevant cognitive job before dependent-origination contact.

The framework's paired arising / cessation formulation remains historically and philosophically distinctive, but on this tested SIer target it does not produce a target-side discovery that is difficult to reach from ordinary incident practice at comparable selection cost.

## Runtime consequence

The original operational demotion is **confirmed under the discovery-aware standard**.

Combined evidence now shows:

- matched RCA / FTA / dependency analysis reproduces the capability;
- generic ex-ante post-incident practice naturally selects contributing-condition and mitigation questions;
- the target-return residual is already available without framework contact;
- near-neighbor distinctness from Paṭṭhāna does not create additional target-side value.

Preserve dependent origination as a sourced research candidate for explicit Buddhist, comparative-philosophy, historical, educational, or future targets where a distinct discovery contribution can be demonstrated.
