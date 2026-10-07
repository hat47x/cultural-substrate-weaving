# Wuxing discovery-value comparison

Status: runtime requalification / discovery-value comparison

## Purpose

Separate:

1. **capability overlap** — can a specialist method reproduce the operation after it is known?;
2. **discovery value** — would ordinary analysis have selected the same cognitive job before Wuxing contact?

The matched specialist comparison already established high capability overlap with signed causal-loop / system-dynamics analysis.

This file tests the second question.

## Fixed target

A distributed job-control platform scales workers from queue depth.

After a sudden traffic spike, the system repeatedly scales out and in instead of settling. Backend saturation, timeouts, retries, queue pressure, admission throttling, worker count, and delayed recovery are all visible in telemetry.

The first explanation is:

> the autoscaler is unstable.

## Ex-ante generic incident baseline

Do not name Wuxing, system dynamics, signed causal-loop analysis, or any cultural framework.

Start with ordinary incident / reliability questions:

- What changed immediately before oscillation began?
- Which metrics move first, and which follow?
- What action does the autoscaler take in response to queue depth?
- What downstream load changes after scale-out?
- Do retries feed work back into the queue?
- Which actions reduce load or inflow?
- Which controller decisions are delayed?
- Does the relation change between spike, recovery, and steady state?
- What happens if one action is held constant or delayed?

These questions arise directly from the target because the observed symptom is repeated over-correction in a feedback-controlled system.

## Domain-standard selection path

The target itself strongly selects control-loop and stabilization reasoning before Wuxing contact.

Kubernetes documents the HorizontalPodAutoscaler as an intermittent control loop. Its current documentation also describes repeated replica fluctuation as thrashing / flapping and provides stabilization windows and tolerance to damp unwanted scale changes.

Google SRE guidance likewise treats autoscaler reaction time, cautious scale-down, bottleneck distance, and misconfiguration-induced runaway scaling as ordinary reliability concerns.

Sources:

- Kubernetes, Horizontal Pod Autoscaling: https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
- Kubernetes API reference, HorizontalPodAutoscalerBehavior / HPAScalingRules: https://kubernetes.io/docs/reference/kubernetes-api/autoscaling/horizontal-pod-autoscaler-v2/
- Google SRE Workbook, Managing Load: https://sre.google/workbook/managing-load/

The specialist path is therefore not chosen only after seeing Wuxing output. The target category and standard operational literature already make feedback, delay, stabilization, and opposing control actions salient.

## Wuxing contact

The de-bound Wuxing pass asks:

- which relations enable or amplify another state?;
- which relations constrain or counteract another state?;
- which closed paths reinforce an excursion?;
- which paths balance it?;
- does one variable play different roles on different edges?;
- which relation changes between spike and recovery?;
- is a missing or delayed relation responsible for instability?

These remain useful questions.

## Ex-ante comparison

| Cognitive job | Generic / ex-ante baseline | Wuxing contact | Incremental discovery |
|---|---|---|---|
| identify amplification | trace which metric/action increases downstream load | generation/support relation | low |
| identify damping | trace throttle/backoff/completion effects | restraint/counteraction relation | low |
| inspect closed loop | repeated over-correction naturally triggers feedback-loop inspection | cycle inspection | low |
| inspect delay | controller and workload timing are standard instability questions | dynamic relation / phase change | low |
| inspect edge-specific role | scale-out helps queue depth while hurting backend load | relation-role reversal | low |
| inspect state change | compare spike, recovery, steady state | phase-change probe | low |
| identify missing balancing action | ask why controller fails to settle | missing-link probe | low |

## Target-return residual

After removing Wuxing vocabulary, the useful questions survive, but they are already present in the ex-ante baseline:

- Which path amplifies the excursion?
- Which path damps it?
- Where is the delay?
- Which action helps one variable while worsening another?
- What changes between spike and recovery?
- Which control or backoff relation is missing, weak, or late?

No additional target-side question remains that depends on Wuxing contact for this target.

## Discovery-value result

The discovery-value counter-hypothesis survives.

Unlike the Huayan canonical-Account fixture, where generic architecture review can leave context-defined identity unquestioned, the autoscaler target advertises its feedback/control character in the symptom itself.

A competent generic incident review has a direct path from:

```text
autoscaler oscillates
  -> inspect controller inputs, outputs, timing, delays, repeated reactions
  -> inspect reinforcing and damping paths
  -> inspect stabilization / hysteresis / backoff
```

without requiring Wuxing contact.

Wuxing can still serve as a compact cultural reminder of relational and cyclical organization, but the tested general SIer target does not show a distinct discovery contribution at comparable selection cost.

## Runtime consequence

Combined evidence now shows:

- **capability overlap**: signed causal-loop / system-dynamics analysis reproduces the de-bound operations;
- **discovery overlap**: the target and ordinary reliability practice naturally select the same feedback / stabilization job before Wuxing contact;
- **near-neighbor distinctness**: Wuxing remains historically and structurally distinct from dependent origination, but that does not create target-side residual value here.

For this general SIer runtime use, removal from default runtime is supported under the revised discovery-aware standard.

Preserve Wuxing as a sourced research candidate for explicit Wuxing, Chinese intellectual history, comparative systems thinking, education, and future targets where discovery contribution can be demonstrated.
