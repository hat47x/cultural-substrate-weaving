# Development

## Edit locations

- Canonical method: `src/ja-JP/`.
- Translations: `src/<locale>/`.
- Translation tracking: `i18n/`.
- Platform wording and configuration: `adapters/`.
- Test cases: `evals/`.
- Generation logic: `scripts/`.

Do not edit `dist/` directly. `.claude-plugin/`, `.agents/`, and `plugins/` are generated, Git-tracked distribution artifacts. The `plugins/` trees contain the shared skill content plus the Claude and Codex distribution metadata. When these artifacts need to change, edit the canonical source, manifest, adapters, or other build inputs, run `make build`, review the generated changes, and commit the result rather than treating generated files as source.

## Cycle

Use the integrated check for normal pre-PR validation:

```bash
make check
```

It currently runs the local repository contract check, rebuilds the generated distribution artifacts and verifies their Git freshness, then runs validation, Japanese-document review checks, unit tests, token-budget checks, Living Lab validation, and Living Lab summary generation. Individual Make targets may be used while diagnosing a narrower problem.

`make repository-contracts`, which is part of `make check`, compares the current local branch name with `VERSION` when the branch is `develop/vX.Y.Z` or `release/vX.Y.Z`. Short-lived branches such as `feature/*`, `fix/*`, and `research/*` are not subject to that version contract.

`make generated-artifacts-check`, also part of `make check`, runs the build first and then checks the Git status of `.claude-plugin/`, `.agents/`, and `plugins/`. It fails on modified or deleted tracked output and on new untracked generated files. This catches changes to canonical source or adapters that were rebuilt locally but whose corresponding generated artifacts were not committed.

When that check fails, review and commit the intended generated changes. If the output is not intended, fix the canonical source, manifest, adapters, or generation logic that produced it rather than editing generated files to make the check pass.

## Branch lifecycle

Small repository-maintenance changes may be committed directly to the active `develop/vX.Y.Z` when appropriate. Substantial method changes, experiments, or isolated implementation work should use a short-lived `feature/*`, `research/*`, or `fix/*` branch created from the active develop branch and return through a pull request targeting that develop branch.

When a short-lived branch is used, treat the following as one completion contract:

- Keep one coherent task on one short-lived branch and one pull request.
- Do not create sibling or successor branches merely because the work continues in another session or context.
- Immediately before merging, refetch both base and head and verify that concurrent work has either not changed the base or has been reconciled.
- After merging the pull request back into its originating branch, refetch the base and verify that the result is actually present before marking the task complete.
- If merging is genuinely blocked, keep the same branch and pull request as the single continuation point, record the blocker, and do not create a successor branch for the same task.

This is a repository workflow rule rather than a GitHub branch-protection guarantee. Its purpose is to keep task history coherent and prevent parallel work from being silently skipped or overwritten.

The `main` merge-commit shape check is deliberately separate from normal feature-branch checks. After a pull request has been merged, run the following on `main` when that local contract needs to be verified:

```bash
make main-contract
```

This is a local diagnostic. It requires the current branch to be `main` and checks that HEAD has exactly two parents. That shape does not prove that GitHub created the commit from a pull request, and the command does not prevent a direct push to GitHub.

GitHub Actions are currently disabled. `main` also has no branch protection or repository ruleset configured at present, so branch contracts and generated-artifact freshness are not remotely enforced by GitHub. A successful local check and GitHub rejecting an invalid push are separate guarantees.

Run `make check` before proposing changes when local execution is available. If the current environment cannot run it, state in the pull request which contracts were checked and which remain unverified. The absence of a remote status is not evidence that validation ran.

A public release is stricter: use an environment that can run `make release-check` on both the release candidate and the exact `main` commit that will be tagged, and run `make main-contract` on that `main` commit. See `release.md`.

When the canonical source changes, update translations and run:

```bash
python scripts/update_translation_hashes.py --locale en-US
make check
```

Run the hash-update command only after reviewing the translation against the new canonical content.
