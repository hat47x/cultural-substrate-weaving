# Development

## Edit locations

- Canonical method: `src/ja-JP/`.
- Translations: `src/<locale>/`.
- Translation tracking: `i18n/`.
- Platform wording and configuration: `adapters/`.
- Test cases: `evals/`.
- Generation logic: `scripts/`.

Do not edit `dist/` directly. `plugins/` is generated and committed for Claude Marketplace delivery.

## Cycle

Use the integrated check for normal pre-PR validation:

```bash
make check
```

It currently runs the local repository contract check, build, validation, Japanese-document review checks, unit tests, token-budget checks, Living Lab validation, and Living Lab summary generation. Individual Make targets may be used while diagnosing a narrower problem.

`make repository-contracts`, which is part of `make check`, compares the current local branch name with `VERSION` when the branch is `develop/vX.Y.Z` or `release/vX.Y.Z`. Short-lived branches such as `feature/*`, `fix/*`, and `research/*` are not subject to that version contract.

The `main` merge-commit shape check is deliberately separate from normal feature-branch checks. After a pull request has been merged, run the following on `main` when that local contract needs to be verified:

```bash
make main-contract
```

This is a local diagnostic. It requires the current branch to be `main` and checks that HEAD has exactly two parents. That shape does not prove that GitHub created the commit from a pull request, and the command does not prevent a direct push to GitHub.

GitHub Actions are currently disabled. `main` also has no branch protection or repository ruleset configured at present, so these branch contracts are not remotely enforced by GitHub. A successful local check and GitHub rejecting an invalid push are separate guarantees.

Run `make check` before proposing changes when local execution is available. If the current environment cannot run it, state in the pull request which contracts were checked and which remain unverified. The absence of a remote status is not evidence that validation ran.

A public release is stricter: use an environment that can run `make release-check` on both the release candidate and the exact `main` commit that will be tagged, and run `make main-contract` on that `main` commit. See `release.md`.

When the canonical source changes, update translations and run:

```bash
python scripts/update_translation_hashes.py --locale en-US
make check
```

Run the hash-update command only after reviewing the translation against the new canonical content.
