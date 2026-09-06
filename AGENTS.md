# Repository instructions

## What belongs in each method layer, and what does not

This repository currently contains one canonical runtime skill plus two research-stage sibling method prototypes. Keep their ownership separate.

1. **cultural-substrate-weaving (CSW)** — open cultural, philosophical, and traditional frameworks as temporary cognitive fields; preserve framework-specific structure; keep attribution explicit; return framework-generated questions, contrasts, correspondences, and other candidates to the target for validation.
2. **affinity-synthesis (research prototype)** — perform one-round material-led synthesis: meaning-bearing units, grouping, labels, higher-order integration, relations, diagram/narrative round-trip, provenance, source-return checks, and representation/lineage.
3. **iterative-inquiry-synthesis (research prototype)** — orchestrate multi-round inquiry through material deltas, touched-artifact reopening, stable semantic handles, append-only round history, residuals, and stop/restart conditions.

The split is a responsibility boundary, not a claim that the KJ lineage has been discarded. KJ-method, affinity-diagram, and qualitative-synthesis lineage belongs to the evidence and Method Definition of `affinity-synthesis`; CSW should not silently re-implement those internals in `src/<locale>/`.

None of these methods supplies domain expertise in writing, management, software engineering, product design, law, medicine, or other fields. Domain-specific quality criteria and procedures belong to the caller's context or to another installed skill used alongside them.

Before adding a rule, classify it by ownership:

| CSW runtime (`src/<locale>/`) | Research sibling methods (`research/skill-prototypes/`) | Domain/caller context |
|---|---|---|
| Framework activation, native structure, correspondence provenance, target return, attribution boundaries | Carding, grouping, labels, source-return synthesis, A/B-like diagram/narrative checks, representation grammar | Domain-specific professional knowledge and quality criteria |
| `target_supported / framework_generated / cross_field_emergent / unresolved` and related CSW attribution rules | Round delta/reopen, stable semantic IDs, append-only inquiry history, stop/restart orchestration | Writing craft, management practice, software design, legal analysis, etc. |
| Taiheki as a limited cultural/body framework when explicitly used | General material-led synthesis that does not depend on cultural frameworks | Character-writing technique or personality diagnosis |

A finding from an experiment is not automatically a runtime rule. A finding about how a request was posed, domain quality, output style, or a particular model's default behavior belongs outside a Method Definition unless it is necessary to execute or validate that method across cases.

## Split-method research workflow

The files under `research/skill-prototypes/` are research candidates, not automatically released Skills.

- Treat Method Definition, Agent Skill realization, representation grammar, evaluation fixture, and application record as separate artifacts.
- Compare existing external Skills before adding local behavior. Reuse or delegate when a narrower external Skill fully satisfies the intended boundary; otherwise absorb useful mechanisms without importing incompatible assumptions.
- For `affinity-synthesis`, preserve the KJ/affinity/qualitative-synthesis lineage while distinguishing AI-era additions such as provenance/discovery separation, transformation audit, secondary resonance, and renderer-independent semantic records.
- For `iterative-inquiry-synthesis`, keep one-round synthesis out of the orchestrator. Its distinctive concern is delta-based reopening rather than repeated full regeneration.
- Cross-layer handoffs must preserve origin and verification separately. Framework-generated material may participate in synthesis without gaining an authority bonus or becoming target-supported merely because it clusters well.
- Do not create a hard public dependency between Skills unless the target platform has an explicit dependency mechanism and the repository deliberately adopts it. A missing compatible realization must be surfaced rather than simulated.
- Run `make research-skill-check` when changing the split-method prototypes or suite manifest.

## Living Lab research workflow

Use the Web Chat Living Lab to observe the released method in real work without turning ordinary work into an experiment for its own sake.

- The existing Living Lab records concern the released/composite method at the time of observation. Do not retroactively rewrite old observations as if the later three-layer split had already existed.
- Use `natural_work` by default. Use `paired_check` only when a method-change decision, an important regression question, or a repeated unexplained difference makes a stronger comparison useful.
- Treat `activation_scope` as a record of what happened in the round. `non_activation` means that no cultural framework was opened; it does not by itself establish that non-activation was useful, harmful, correct, or incorrect.
- Record events with observation-oriented types. Keep judgments of usefulness, harm, causation, or appropriateness out of the event type itself.
- Keep directly observable changes, measurements, user judgments, and AI or external interpretations on separate provenance paths. An AI evaluator's conclusion is an attributed interpretation, not a measurement and not a user judgment.
- Never force a cultural framework into a task merely to increase framework-use count or observation coverage.
- Do not fabricate additional cases to fill domain categories. `task.domain` in the summary is coverage context only, not a taxonomy, quota, KPI, score, or release gate.
- Keep real or private round/event records under `.living-lab/` or outside the repository. Commit only public-safe or separately anonymized/abstracted records under `research/living-lab/observations/`.
- Prefer opaque references over copying source material into records when the copied material would disclose more than is needed for later review. Do not commit secrets, identifying private data, or confidential source content into public observations.
- Public observation files must form a valid closed record set. Run `make check` before proposing release changes; Living Lab validation and summary generation are part of that check.
- Do not change `src/` from one case, one event, one score, or the AI's own evaluation of its output. Return to traceable artifact differences, user corrections, later withdrawals or reuse, and repeated observations across real tasks before considering promotion.
- Prefer changing research records, auxiliary guidance, or tooling over adding static runtime rules when the available material does not justify a stable method rule.

## Branch and release workflow

Use a lightweight Git Flow around versioned development lines.

- `main` is the release-quality canonical branch and the base for a new version line.
- Start the next version as `develop/vX.Y.Z` from the current `main`. The branch name declares the intended release version.
- `make check` runs the local repository-contract check, rebuilds the Git-tracked distribution artifacts, and fails when `.claude-plugin/`, `.agents/`, or `plugins/` still contains modified, deleted, or untracked generated output. On `develop/vX.Y.Z` or `release/vX.Y.Z`, the branch version must also match `VERSION`; short-lived feature/fix/research branches are not subject to that version contract.
- Small repository-maintenance changes may be committed directly to the active `develop/vX.Y.Z` branch.
- Substantial method changes, experiments, or isolated implementation work should use a short-lived branch such as `feature/<topic>`, `research/<topic>`, or `fix/<topic>` from the active develop branch and target that develop branch with a pull request.
- Finalize a release by bringing the active develop branch back to `main` through a pull request using the normal merge-commit method, running the full release checks on both the release candidate and the exact `main` commit, running `make main-contract` on `main`, deriving `TAG="v$(cat VERSION)"`, and running `make release-tag-contract TAG="$TAG"` before creating the tag.
- Public release packaging requires a clean Git worktree. Tracked uncommitted changes and non-ignored untracked files invalidate package provenance and must be committed, removed, or intentionally ignored before `make release-check` can complete.
- The final release manifest uses schema 2 and records the package-producing Git commit as `source_commit`; `release-validate` requires both a clean worktree and `source_commit` equal to the current `HEAD`.
- After pushing the tag, run `make release-remote-tag-contract TAG="$TAG"`. It resolves the remote tag to the commit it ultimately references and requires that commit to match the manifest `source_commit`.
- `make main-contract` checks only that the local `main` HEAD has exactly two parents. That shape does not prove that GitHub created the commit from a pull request.
- The release-tag contract checks that the intended tag, `VERSION`, and the final release-manifest version agree. Do not retype a separate tag version after that check passes.
- Urgent released-version fixes may use `hotfix/vX.Y.Z` from `main`; merge the fix back into both `main` and any active develop line when applicable.
- Do not make method-content commits directly to `main` except for an explicitly chosen hotfix path.
- If `main` advances while a develop line is active, reconcile those changes into the develop line before release rather than letting the branches silently diverge.
- GitHub Actions are disabled, and `main` currently has no branch protection or repository ruleset. Local checks express and diagnose repository policy; they do not imply that GitHub will reject an invalid direct push.

## Japanese development-document drafting

For Japanese public user guides and Japanese development, maintainer, research, experiment, and operational documents, completing the factual or technical content is not the final drafting step.

1. Draft the facts, structure, constraints, and technical meaning first.
2. Check that the draft preserves the intended meaning, identifiers, schema field names, commands, and evidence boundaries.
3. **Always perform a separate natural-Japanese rewriting pass after the content is settled.** Treat natural Japanese as the highest-priority prose criterion at this stage. Rewrite awkward word order, missing or overloaded particles, excessive noun chains, literal translations, and unnecessary English insertions while preserving technical meaning.
4. Reread the whole document as continuous Japanese prose rather than validating only changed lines. A locally correct sentence may still be unnatural in the surrounding paragraph.
5. Keep literal identifiers and established technical terms when they are needed for precision, but do not let their English wording determine the surrounding Japanese syntax.

In short: **自然な日本語であることを最優先し、内容確定後に必ず独立した推敲工程を通す。** A first draft, generated draft, or literal translation is not considered complete until this pass has been performed.

Apply this rule to the scoped Japanese public guides and development documents, including existing files. When an existing document is reviewed and no wording change is needed, record the review without forcing a cosmetic diff.

## Working rules

- Edit canonical CSW runtime content under `src/<locale>/`.
- Edit split-method research prototypes under `research/skill-prototypes/`; do not move their internal algorithms back into `src/` merely to make the composite runtime self-contained.
- `src/ja-JP/` is the semantic canonical source for CSW. Prototype Method Definitions declare their own research canonical documents in `research/skill-prototypes/suite-manifest.json`.
- When Japanese canonical runtime content changes, update the corresponding English translation and `i18n/translation-manifest.json` before release. A research branch may explicitly carry an English parity backlog, but it must not claim locale parity or pass the release validation until resolved.
- Keep identical relative file structures across runtime locales.
- Do not edit `dist/` directly.
- `.claude-plugin/`, `.agents/`, and `plugins/` are generated by `scripts/build.py`; edit canonical source, manifests, adapters, or generation logic rather than treating generated files as source.
- Run `make build` after changing build inputs, review the generated Git diff, and commit the intended generated artifacts. `make check` fails when generated tracked artifacts are stale or new generated files are left untracked.
- Run `make research-skill-check` for research-suite changes and `make check` before proposing release changes when local execution is available. If execution is unavailable, record the exact contracts checked and the parts left unverified; do not treat the absence of a remote GitHub Actions status as evidence that validation ran.
- Do not apply cultural-substrate-weaving, affinity-synthesis, or iterative-inquiry-synthesis automatically to routine repository maintenance.