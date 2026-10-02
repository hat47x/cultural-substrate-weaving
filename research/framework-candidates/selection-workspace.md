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
  --baseline "target-side baseline before framework contact"
```

The shortlist preserves inventory order and computes no score. The contrast is exact-string only and does not infer semantic equivalence. The worksheet deliberately leaves role, intended cognitive job, near-neighbor difference, target-return questions, de-bound target language, and revision conditions blank.

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
