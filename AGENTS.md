# Repository instructions

## What belongs in the skill, and what does not

The skill has two core capabilities:

1. **Cultural-framework exploration** — obtain position layers, relations, transitions, and other structure candidates from cultural, philosophical, and traditional frameworks, then return them to the target for validation.
2. **KJ-method integration** — preserve heterogeneous fragments as living semantic units, let relations and gaps emerge without premature classification, and integrate them while retaining provenance and epistemic boundaries.

It is **not** the skill's job to supply domain expertise in writing, management, software engineering, product design, law, medicine, or other fields. Domain-specific quality criteria and procedures belong to the caller's context or to another installed skill used alongside this one.

Before adding anything to `src/<locale>/`, classify it:

| Belongs in the skill | Belongs in domain/caller context |
|---|---|
| How a cultural framework supplies structure and how that structure is validated against the target | Domain-specific professional knowledge and quality criteria |
| KJ carding, grouping, integration, gap discovery, and transformation checks | Writing craft, management practice, software design, legal analysis, etc. |
| Activation, attribution, falsification, stopping, and provenance rules required by the two capabilities | General communication, output design, collaboration, or model-style correction |
| Taiheki as a limited cultural/body framework for observing human bodily consistency | Character-writing technique or personality diagnosis |

A finding from an experiment is not automatically a change to the skill. A finding about how a request was posed, about domain quality, or about the model's default style belongs outside the skill unless it is necessary to execute or validate the two core capabilities.

## Living Lab research workflow

Use the Web Chat Living Lab to observe the released method in real work without turning ordinary work into an experiment for its own sake.

- Use `natural_work` by default. Use `paired_check` only when a method-change decision, an important regression question, or a repeated unexplained difference makes a stronger comparison useful.
- Treat `activation_scope` as a record of what happened in the round. `non_activation` means that no cultural framework was opened; it does not by itself establish that non-activation was useful, harmful, correct, or incorrect.
- Record events with observation-oriented types. Keep judgments of usefulness, harm, causation, or appropriateness out of the event type itself.
- Keep directly observable changes, measurements, user judgments, and AI or external interpretations on separate provenance paths. An AI evaluator's conclusion is an attributed interpretation, not a measurement and not a user judgment.
- Never force a cultural framework into a task merely to increase framework-use count or observation coverage.
- Do not fabricate additional cases to fill domain categories. `task.domain` in the summary is coverage context only, not a taxonomy, quota, KPI, score, or release gate.
- Keep real or private round/event records under `.living-lab/` or outside the repository. Commit only public-safe or separately anonymized/abstracted records under `research/living-lab/observations/`.
- Prefer opaque references over copying source material into records when the copied material would disclose more than is needed for later review. Do not commit secrets, identifying private data, or confidential source content into public observations.
- Public observation files must form a valid closed record set. Run `make check` before proposing changes; Living Lab validation and summary generation are part of that check.
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

- Edit method content only under `src/<locale>/`.
- `src/ja-JP/` is the semantic canonical source.
- When Japanese canonical content changes, update the corresponding translation and `i18n/translation-manifest.json`.
- Keep identical relative file structures across locales.
- Do not edit `dist/` directly.
- `.claude-plugin/`, `.agents/`, and `plugins/` are generated by `scripts/build.py`; edit canonical source, manifests, adapters, or generation logic rather than treating generated files as source.
- Run `make build` after changing build inputs, review the generated Git diff, and commit the intended generated artifacts. `make check` fails when generated tracked artifacts are stale or new generated files are left untracked.
- Run `make check` before proposing changes when local execution is available. If it is not available, record the specific contracts checked and the parts left unverified; do not treat the absence of a remote GitHub Actions status as evidence that validation ran.
- Do not apply the cultural-substrate-weaving method automatically to routine repository maintenance.