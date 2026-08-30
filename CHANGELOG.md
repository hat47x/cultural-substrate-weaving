# Changelog

## Unreleased

- Separated CSW activation scope from cultural-framework loading depth. A run may use the skill without opening a framework, and framework contact now progresses only as needed through `not_loaded / probe / preview / full / enacted` rather than treating deeper loading as success.
- Separated exploratory framework use from attribution use. Frameworks may freely generate questions, contrasts, hypotheses, research targets, and compositional resources, while claims about the target require target-side support and the relevant homogeneity, assignment, convention, lineage, and transition checks.
- Reframed the removal check as de-binding rather than evidence generation, and added explicit provenance states: `target_supported / framework_generated / cross_field_emergent / unresolved`.
- Clarified that reducing or rejecting CSW or a particular framework does not narrow the task scope entrusted by the caller; work can return to the domain method while preserving residuals and reopening conditions.
- Added lightweight longitudinal rounds and event vocabulary for delayed change without turning framework count or trajectory length into KPIs.
- Added the Web Chat Living Lab research layer with `natural_work` and selective `paired_check` modes, round/event schemas, examples, a dependency-free validator, tests, and Japanese/English operating guidance. Living Lab findings remain research evidence and are not automatically promoted into runtime method rules.
- Began the prospective Living Lab observation cycle with public/private record separation: real records are private-by-default under `.living-lab/` or outside the repository, while publishable or separately anonymized observations may be kept under `research/living-lab/observations/` and are validated as a closed record set.
- Added a non-scoring Living Lab review inventory to CI reports. It preserves per-round activation, task-domain coverage context, events, artifacts, residuals, and reopening conditions while explicitly treating counts and distributions as review aids rather than KPIs, scores, win/loss labels, or causal evidence.
- Aligned the dependency-free Living Lab validator with the published round/event JSON Schemas, including nested additional-property, type, comparison, enum, and date-time checks, and added schema-parity regression coverage so the two validation surfaces cannot silently drift apart.
- Aligned English translation `source_version` with the active `VERSION`, made reviewed-hash updates advance that metadata automatically, and added validation/regression coverage so version drift cannot remain CI-green.
- Updated GitHub Actions Python setup to `actions/setup-python@v7`, removing the Node 20 deprecation path from validation, release, and Microsoft 365 packaging workflows.
- Simplified release triggering so tag pushes are the canonical automatic publication path and `workflow_dispatch` is the explicit re-publication path; publishing a GitHub Release no longer recursively starts the release workflow a second time.
- Added a CI branch-version contract: `develop/vX.Y.Z` and `release/vX.Y.Z` must carry the same `VERSION`, preventing a development or release line from silently building packages under a different version.
- Added runtime-package boundary tests so generated OpenAI and Claude/Codex references must match the canonical manifest exactly, while repository-only research, maintainer, test, and workflow material stays out of runtime output trees.
- Added generated-skill link integrity tests so local Markdown links stay inside the runtime package, resolve to bundled files, and reference only manifest-declared runtime references.

## 0.3.0 — 2026-08-30

- Bounded framework application depth: adopting a framework no longer implies exhausting all positions, interpretive vocabulary, or transitions; application stays scoped to target-side need and stops rather than filling unused structure.
- Extended iterative KJ work across delayed rounds: carry unresolved questions, isolated semantic units, and held relations forward; reopen them when later material touches them; and observe whether earlier questions change later research, regrouping, artifacts, or decisions without treating that record as causal proof.
- Purified the skill boundary: domain-specific craft, output-design, and general collaboration guidance are no longer part of the runtime method. The intended composition is a domain skill or domain method plus cultural-substrate-weaving.
- Retired the standalone creative-pattern module. Taiheki remains only as a limited cultural/body-oriented lens for human observation, not as an automatic character-writing module or diagnosis.
- Reworked KJ integration around semantic units and epistemic boundaries: join to preserve semantic unity, split to preserve evidence state, keep unresolved attention in natural language, and treat fixed counts and error signs as heuristics rather than truth conditions.
- Consolidated carding, grouping, labelling, folding, and semantic compression around the same integration kernel, with post-transformation comparison back to source material.
- Clarified separation of source from discovery path, independent evidence from reposts/derivations, and research retention thresholds from publication thresholds.
- Clarified cultural-framework use as a source of candidate structure rather than domain truth, with assignment checks, removal checks, misfit records, and return-to-target validation.
- Updated activation, routing, adapters, evaluation, and documentation to match the purified scope.
- Reset validation documentation for the purified current version. Validation starts from new comparisons against domain-method baselines.

## 0.2.0 — 2026-08-21

Historical section reconstructed from the published `v0.2.0` tag and the `v0.1.0...v0.2.0` repository diff. The tagged changelog still carried these changes under `Unreleased`, so this section restores the missing release boundary without rewriting the tagged artifact.

- Added the KJ integration kernel for raising a whole picture from heterogeneous fragments while keeping blanks, isolated material, and return-to-source checks visible.
- Expanded framework selection and validation: distinguish position layers from interpretive layers, declare assignment predicates and external conventions, check lineage and unit compatibility by layer, and use substitution, removal, misfit, and coverage checks before treating framework-derived structure as a target-side result.
- Strengthened iterative exploration: change the question across passes, use blanks to direct later gathering, distinguish conclusion movement from mere text growth, and keep unresolved implementation questions for later handoff rather than filling them speculatively.
- Made baseline and preservation constraints explicit, including what must not be broken, what counts as a target-side fact, and why recurrence alone does not establish sameness or centrality.
- Strengthened provenance and epistemic boundaries: keep source separate from discovery path, avoid double-counting reposts or derivations, preserve judgment origin and adoption state, and separate research-retention thresholds from publication thresholds.
- Refined over-application controls so framework mismatch, conventional choices, empty positions, and coverage gaps remain visible instead of being converted automatically into claims about the target.
- Expanded platform guidance and regenerated multilingual Claude, ChatGPT, Codex, and Microsoft 365 Copilot artifacts for the 0.2.0 method surface.
- Synchronized repository, plugin, manifest, and build-package version metadata to `0.2.0` and published locale/platform packages from the `v0.2.0` tag.

## 0.1.0 — Initial public release

- Semantic canonical source under `src/ja-JP/`, with a structurally parallel English translation under `src/en-US/`.
- Glossary, translation source hashes, and review policy under `i18n/`.
- Locale-aware builders for Codex, Claude Code, custom GPTs, and Microsoft 365 Copilot.
- Language-specific release assets and beginner guides.
- CI checks for source-tree parity and stale translations.
