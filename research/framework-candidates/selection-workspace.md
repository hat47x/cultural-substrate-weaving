# Framework selection workspace

Status: research/toolkit / non-ranking / non-routing

As the framework corpus grows, selection itself becomes a cognitive task. This helper externalizes four parts of that task without deciding them:

1. recall adopted candidates from explicit selection cues written in ordinary Japanese or English;
2. recall candidates that literally mention a needed operation, primitive, or use;
3. contrast explicitly chosen near-neighbors by exact operation labels;
4. create an unfilled worksheet that records why each candidate is being considered and how it must return to the target.

It is not a fit scorer, recommendation engine, or adoption gate.

```bash
INVENTORY=research/framework-candidates/cognitive-operation-inventory.json
TYPOLOGY=research/efficacy-cheap-llm/framework-typology.json
TOOL=research/framework-candidates/scripts/framework_selection_workspace.py

python "$TOOL" list-target-structures "$TYPOLOGY"
python "$TOOL" structure-lookup "$TYPOLOGY" "$INVENTORY" TS-condition-chain

python "$TOOL" inspect "$INVENTORY" dependent-origination

python "$TOOL" recall "$INVENTORY" \
  --need "規則の範囲と例外と文脈補完を分けたい"

python "$TOOL" shortlist "$INVENTORY" threshold --field primitive

python "$TOOL" contrast "$INVENTORY" dependent-origination huayan

python "$TOOL" worksheet "$INVENTORY" \
  --need "separate establishment conditions from whole/part re-identification" \
  --candidate dependent-origination \
  --candidate huayan \
  --baseline "target-side baseline before framework contact" \
  --ref "selection://round-03/framework-choice" \
  --output /tmp/selection.json

python "$TOOL" set-target-structure /tmp/selection.json "$TYPOLOGY" \
  TS-condition-chain \
  --basis "対象側で上流条件の欠落が未解決の仮説として残っている"

python "$TOOL" set-candidate /tmp/selection.json dependent-origination \
  --role primary \
  --job "establishment / cessation conditionsを開く" \
  --operation condition-chain \
  --difference "whole/part identityの再規定とは別の仕事" \
  --return-question "何を外すとこの現象は成立しなくなるか"

python "$TOOL" set-candidate /tmp/selection.json huayan \
  --role reflecting \
  --job "partのroleを別nodeから再同定する"

python "$TOOL" set-consideration /tmp/selection.json dependent-origination \
  --target-connection "対象側に成立条件の空白がある" \
  --structural-difference "node再同定ではなく条件連鎖を開く" \
  --redundancy "huayanと重なるのはboundaryだけ" \
  --target-return "必要条件を対象資料へ戻して確認できる" \
  --misuse-risk "conditionをcauseへ昇格しない" \
  --domain-constraint "設計判断はcaller側が行う"

python "$TOOL" set-guardrail /tmp/selection.json dependent-origination \
  --contact-if "対象側に成立条件の空白が残るときだけ開く" \
  --stop-if "上流条件として分けられる材料が無ければ止める" \
  --survive-if "体系語を外しても対象資料で確認できる問いが残る場合だけ持ち越す"

python "$TOOL" set-non-activation /tmp/selection.json \
  --reason "通常のtarget-side質問だけで十分な可能性を残す" \
  --baseline-note "framework接触前に同じ問いを一度試す" \
  --revisit-if "baselineでは具体的な確認項目が出ないときだけ再検討"

python "$TOOL" review /tmp/selection.json

python "$TOOL" set-cross-framework /tmp/selection.json \
  --primary-job "成立条件を開く" \
  --second-job "part/whole identityを揺らす" \
  --disturb "一方向のcondition-chainへ固定された見方"

python "$TOOL" record-exit /tmp/selection.json \
  --kind question \
  "どの条件が対象側で本当に必要か"

python "$TOOL" show /tmp/selection.json

# After framework-generated cards have been traced with the same selection-ref:
python "$TOOL" audit-map /tmp/selection.json /tmp/board.json

# When a natural-work Living Lab round reused the same selection ref:
python "$TOOL" audit-living-lab /tmp/selection.json /tmp/round.json
```

`inspect` is the Registry-0 boundary view for one candidate. It assembles the candidate's native primitives, operations, ordinary-language cues, full source references, profile/source-packet/runtime paths, positive/negative target-return fixtures, readiness, adoption hold, and `do_not_assume` boundary without computing fit, rank, or activation. Use it before deliberate activation when the model or analyst needs to recover what is actually documented rather than reconstructing a framework from memory.

The provisional target-structure vocabulary is intentionally a separate first step. `list-target-structures` shows the human-authored target-side vocabulary from the research typology. `structure-lookup` accepts exact target-structure IDs and exposes every mapped framework in framework-inventory order. It does not classify natural language into a target structure and does not choose among the mapped frameworks. This boundary responds to the selection experiments in which direct model/Jev framework choice concentrated on a small number of frameworks: the toolkit makes the target-side structural hypothesis explicit instead of hiding that judgment inside a router.

`set-target-structure` records an exact target-structure ID, its current typology definition, and an optional target-side basis in the saved workspace. This is a provisional hypothesis, not a diagnosis or evidence that a mapped framework fits. The hypothesis remains separate from candidate role assignment, no-framework consideration, and activation.

The `recall` command is the bridge from an ordinary-language missing cognitive function to the adopted corpus. It uses only explicit `selection_cues` stored in the inventory, performs punctuation/spacing normalization, preserves inventory order, and defaults to `adopted` candidates. It does not use embeddings, semantic similarity, scoring, or automatic routing. To inspect a research-only readiness state, pass `--readiness` explicitly.

The shortlist preserves inventory order and computes no score. The contrast is exact-string only and does not infer semantic equivalence. The worksheet deliberately starts with role, intended cognitive job, near-neighbor difference, target-return questions, de-bound target language, and revision conditions unfilled.

`set-guardrail` externalizes three candidate-specific non-force conditions: when framework contact is justified (`contact_if`), what target-side observation should stop or weaken the contact (`stop_if`), and what must still survive after de-binding before material is carried forward (`survive_if`). These are reasoning prompts, not an automatic activation gate. `review` surfaces missing guardrails without scoring them or requiring activation.

Each candidate also has six independent, free-text consideration axes: target connection, structural difference, redundancy/overlap, target-return feasibility, misuse/authority risk, and domain constraint. They are kept separate on purpose; the tool does not collapse them into a score. A distinct `no_framework_option` records why non-activation may be preferable and what would reopen the choice.

`review` only surfaces which consideration fields remain blank. Blank fields are prompts for deliberate thought, not failures, coverage metrics, or requirements to activate a framework. This makes non-activation and unresolved selection visible without turning the workspace into a router.

When the selection actually progresses, use `set-candidate`, `set-cross-framework`, and `record-exit` to append explicit reasoning to the saved workspace. `set-candidate --operation` records the exact inventory operation that is intentionally being tried and rejects operation labels not available on that candidate. These operations do not calculate or recommend values; they only preserve what the analyst/skill has explicitly decided or observed.

When a stable `--ref` is supplied, keep that handle with the worksheet and reuse it as `trace-card --selection-ref` on downstream framework-generated cards. The handle is provenance only; it does not make the selection correct or the card target-supported.

`audit-map` can then compare planned operations with exact operation labels observed on cards carrying that selection ref, both across the selection and per exact candidate ID. It also places each candidate's pre-contact non-force guardrails beside the observed target responses / target-return states as candidate guardrail context. This is deliberately not a pass/fail check: the tool does not decide whether a stop condition was satisfied or whether a surviving output is justified. Candidate-level output keeps each framework's observed operations together with its yield kinds, target responses, and target-return states, so an operation or outcome observed under one framework is not credited to another merely because both belonged to the same selection. It also shows candidate-ID label matches/mismatches and downstream cross-field cards. It remains a mechanical provenance audit: a planned operation not observed is not automatically a failure, an observed unplanned operation is not automatically a defect, and the presence or absence of a yield/response/return state is not an effectiveness score.

A useful workflow is:

```text
target-side baseline
  -> name the missing cognitive function
  -> optionally state an exact target-structure hypothesis
  -> inspect the typology mapping without ranking
  -> shortlist without ranking
  -> contrast plausible near-neighbors
  -> keep no-framework as an explicit option
  -> write target connection / structural difference / redundancy / return feasibility / misuse risk separately
  -> write the intended cognitive job for each candidate
  -> choose primary / reflecting framework under external delegation
  -> run framework operations
  -> return generated material to target-side sources/observations
  -> preserve pushback / survival / residuals
  -> de-bind framework language
  -> feed the resulting material back into affinity / iteration
```

`audit-living-lab` joins the workspace to one schema 0.2 Living Lab round by the exact stable `selection_ref`. It places planned operations, recorded framework contacts, artifact provenance, target-return states, user dispositions, and the original non-force guardrails in one read-only view. It does not infer that missing provenance is a failure, that a retained artifact was caused by the framework, that a target-return state is correct, or that a guardrail was satisfied. The official Living Lab validator remains responsible for validating the round record itself.

Do not use the helper to convert readiness into fit, prefer a framework because it has more operations/sources, treat operation-name overlap as semantic equivalence, bypass lineage/adoption holds, or turn cross-framework agreement into target evidence.

## Research-candidate recall

profile-ready candidates also carry explicit selection cues. The default `recall` path remains adopted-only. Research work may opt in with `--readiness profile-ready`; this exposes candidates for investigation without treating readiness as a fit score or bypassing adoption holds.
