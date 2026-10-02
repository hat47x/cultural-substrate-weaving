# Framework selection workspace

Status: research/toolkit / non-ranking / non-routing

As the framework corpus grows, selection itself becomes a cognitive task. This helper externalizes three parts of that task without deciding them:

1. recall candidates that literally mention a needed operation, primitive, or use;
2. contrast explicitly chosen near-neighbors by exact operation labels;
3. create an unfilled worksheet that records why each candidate is being considered and how it must return to the target.

It is not a fit scorer, recommendation engine, or adoption gate.

```bash
INVENTORY=research/framework-candidates/cognitive-operation-inventory.json
TOOL=research/framework-candidates/scripts/framework_selection_workspace.py

python "$TOOL" shortlist "$INVENTORY" threshold --field primitive

python "$TOOL" contrast "$INVENTORY" dependent-origination huayan

python "$TOOL" worksheet "$INVENTORY" \
  --need "separate establishment conditions from whole/part re-identification" \
  --candidate dependent-origination \
  --candidate huayan \
  --baseline "target-side baseline before framework contact" \
  --ref "selection://round-03/framework-choice" \
  --output /tmp/selection.json

python "$TOOL" set-candidate /tmp/selection.json dependent-origination \
  --role primary \
  --job "establishment / cessation conditionsを開く" \
  --operation condition-chain \
  --difference "whole/part identityの再規定とは別の仕事" \
  --return-question "何を外すとこの現象は成立しなくなるか"

python "$TOOL" set-candidate /tmp/selection.json huayan \
  --role reflecting \
  --job "partのroleを別nodeから再同定する"

python "$TOOL" set-cross-framework /tmp/selection.json \
  --primary-job "成立条件を開く" \
  --second-job "part/whole identityを揺らす" \
  --disturb "一方向のcondition-chainへ固定された見方"

python "$TOOL" record-exit /tmp/selection.json \
  --kind question \
  "どの条件が対象側で本当に必要か"

python "$TOOL" show /tmp/selection.json
```

The shortlist preserves inventory order and computes no score. The contrast is exact-string only and does not infer semantic equivalence. The worksheet deliberately starts with role, intended cognitive job, near-neighbor difference, target-return questions, de-bound target language, and revision conditions unfilled.

When the selection actually progresses, use `set-candidate`, `set-cross-framework`, and `record-exit` to append explicit reasoning to the saved workspace. `set-candidate --operation` records the exact inventory operation that is intentionally being tried and rejects operation labels not available on that candidate. These operations do not calculate or recommend values; they only preserve what the analyst/skill has explicitly decided or observed.

When a stable `--ref` is supplied, keep that handle with the worksheet and reuse it as `trace-card --selection-ref` on downstream framework-generated cards. The handle is provenance only; it does not make the selection correct or the card target-supported.

A useful workflow is:

```text
target-side baseline
  -> name the missing cognitive function
  -> shortlist without ranking
  -> contrast plausible near-neighbors
  -> write the intended cognitive job for each candidate
  -> choose primary / reflecting framework under external delegation
  -> run framework operations
  -> return generated material to target-side sources/observations
  -> preserve pushback / survival / residuals
  -> de-bind framework language
  -> feed the resulting material back into affinity / iteration
```

Do not use the helper to convert readiness into fit, prefer a framework because it has more operations/sources, treat operation-name overlap as semantic equivalence, bypass lineage/adoption holds, or turn cross-framework agreement into target evidence.
