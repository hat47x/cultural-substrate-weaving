# Release internals

This document records release invariants and implementation details shared across locales. It is not the primary step-by-step guide.

Current procedures:

- [日本語のリリース手順](../ja/maintainers/release.md)
- [English release procedure](../en/maintainers/release.md)

GitHub Actions are currently disabled. There is no automatic Validate or Release workflow. `main` also has no branch protection or repository ruleset configured at present. A missing remote status or an accepted push is therefore not evidence that any local validation or repository-policy check ran successfully. Public release gates are explicit local/manual operations.

## Validation levels

Use the ordinary development path for normal work:

```bash
make check
```

It first runs the local repository contract check. On `develop/vX.Y.Z` or `release/vX.Y.Z`, the branch version must agree with `VERSION`. It then rebuilds runtime outputs, validates source/generated parity and platform-specific contracts, checks natural-Japanese review freshness, runs tests and token checks, validates Living Lab records, and writes review reports. It does not create the final release manifest.

The `main` merge-commit shape policy is a separate local diagnostic:

```bash
make main-contract
```

This target must be run on `main`; it checks that HEAD has exactly two parents. That shape does not prove that GitHub created the commit from a pull request. The target also does not prevent a direct push at GitHub and must not be described as remote enforcement.

Use the packaging path for a release candidate:

```bash
make release-check
```

This runs `make check`, requires a clean Git worktree, creates locale/platform packages, writes `dist/release-manifest.json`, and validates the completed package set. Tracked uncommitted changes and untracked files that Git does not ignore are release blockers. Files intentionally excluded through `.gitignore`, such as `dist/`, `.tmp/`, and the local Living Lab workspace, do not make the worktree dirty.

Once the final manifest exists and the intended release tag has been derived from `VERSION`, use the tag-version gate separately:

```bash
TAG="v$(cat VERSION)"
make release-tag-contract TAG="$TAG"
```

This target is itself bound to the public `main` commit. It reruns `main-contract`, requires the current HEAD to be present in `origin/main` history, and reruns the full `release-validate` contract immediately before the tag-specific checks. The current manifest, packages, reports, hashes, clean worktree, and `source_commit == HEAD` relationship must therefore still be valid on the two-parent `main` commit that is actually present remotely. It then checks the intended tag against `VERSION` and the final manifest version and requires the dated CHANGELOG boundary to be frozen. The target remains separate from `make release-check` because the tag is an explicit publication-time input rather than a package-build input.

After the tag exists remotely, use the remote-tag provenance gate:

```bash
make release-remote-tag-contract TAG="$TAG"
```

This again reruns `release-validate` before the remote-tag-specific check. It then fetches the exact remote tag, peels lightweight or annotated tag objects to the commit they ultimately reference, and requires that commit to equal the final manifest `source_commit`. Unlike the tag-creation gate, this post-tag check is not restricted to the `main` branch so it can also be rerun from another clean checkout of the exact release commit.

None of these commands by itself proves that the method is empirically effective.

## Release manifest semantics

The release manifest is a **post-package release contract**, not a build-progress marker.

- `files` inventories all files present under `dist/` before the manifest itself is written. It is build provenance and includes generated trees that are not separately published as GitHub Release assets.
- `release_assets` lists exactly the files that must be published for the GitHub Release: the manifest itself, package ZIPs, and validation/review reports.
- `source_commit` records the Git `HEAD` that produced the final package set. This provenance is accepted only from a clean worktree. Post-package validation requires the worktree to remain clean and `source_commit` to equal the current `HEAD`; post-publication tag validation returns to this value.
- `schema_version` versions the manifest structure independently of the CSW method version. Schema 2 adds `source_commit` as required release provenance.

`scripts/build.py` never writes a release manifest. `scripts/package.py` is the sole manifest producer, so a manifest exists only after `make package` or `make release-check` reaches the packaging stage. Do not treat ordinary build output as a release contract.

## Package reproducibility

Release ZIP creation normalizes:

- member ordering;
- archive paths to POSIX separators;
- ZIP timestamps;
- regular-file type and 0644/0755 permission bits; and
- the DEFLATE compression level.

This removes checkout/file-mtime and ordinary archive-metadata variance. It is not a claim that different Python or zlib implementations must always emit byte-identical compressed streams.

## Local/private configuration boundary

Packaging is fail-closed for local configuration that may exist only in a maintainer checkout.

- `.env` and non-example `.env.*` files are rejected.
- `*.local` and `*.secret` files are rejected.
- `.env.*.example` templates remain publishable.
- symlinks are rejected rather than dereferenced into a release package.

Microsoft 365 has an additional tenant boundary. The canonical public build is tenant-neutral: `scripts/build.py` does not read a local `.env.*` file and does not copy one into `dist/`. A tenant-specific SharePoint capability is added only when `CSW_M365_SHAREPOINT_SITE_URL` or its locale-specific form is explicitly present in the build environment.

Agents Toolkit deployment is a separate explicit path. Generate a deployment file with `scripts/init_m365_env.py`, build with an explicitly injected SharePoint URL when needed, and then use `scripts/stage_m365_env.py` to copy that deployment-only file into the selected generated agent project. Public `make package` intentionally rejects the staged environment file, so tenant deployment and public GitHub Release packaging remain different paths.

The independent post-package validator also rejects private/local file names if they are already present inside a ZIP. For public Microsoft 365 packages it additionally rejects a concrete `OneDriveAndSharePoint` site URL, so an accidentally tenant-specific build cannot pass the public release contract.

## Release validation

`python scripts/validate_release.py` runs after packaging and checks, among other things:

- clean Git worktree state;
- manifest version/locale/schema metadata;
- manifest `source_commit` against the current Git `HEAD`;
- exact `dist/` file inventory, sizes, and SHA-256 values;
- exact locale × platform package set;
- required validation, token-budget, and Living Lab reports;
- agreement between `release_assets` and the publication boundary;
- readable, non-empty ZIPs with safe member paths;
- absence of local/private configuration members;
- tenant-neutral public Microsoft 365 packages; and
- normalized ZIP metadata and permissions.

When publishing manually, read the already validated `release_assets` list and pass that exact set to `gh release create` or `gh release upload`. Do not duplicate the publication list as shell globs or a second handwritten package list.

## Publication gates after GitHub Actions were disabled

The following checks used to be performed around the automated publication path. They remain release requirements even though the workflow no longer exists.

### 1. Freeze the changelog boundary

A development line may keep work under `## Unreleased`. Before public publication, move the release-bound contents under exactly one dated heading:

```text
## X.Y.Z — YYYY-MM-DD
```

Keep exactly one new `## Unreleased` section before that dated section for later work, but leave it empty until publication is complete. The dated release section itself must contain release contents rather than serving as an empty marker.

Validate the boundary explicitly:

```bash
python scripts/check_release_changelog.py \
  --version "$(cat VERSION)"
```

Do not treat successful packaging as permission to publish an unfrozen changelog.

### 2. Validate the exact commit and tag that will be published

The tag must point to the commit that actually landed on `main`. Merge the release pull request with the normal merge-commit method rather than squash or rebase merging. After it merges:

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
make main-contract
make release-check
git merge-base --is-ancestor HEAD origin/main
TAG="v$(cat VERSION)"
make release-tag-contract TAG="$TAG"
```

Require all four checks to succeed. `make main-contract` verifies that the local `main` HEAD has exactly two parents, `make release-check` validates the actual release set from a clean worktree and records that HEAD as manifest `source_commit`, and the explicit ancestry check confirms early that the commit is in `origin/main` history. `make release-tag-contract` then fails closed on those publication prerequisites itself: it reruns `main-contract`, rechecks that HEAD is in `origin/main`, revalidates the full release set, and finally binds the intended tag to `VERSION`, the final manifest version, the exact clean `HEAD`, and the frozen dated CHANGELOG boundary.

The explicit `make main-contract` and ancestry commands remain useful as separate diagnostics before invoking the tag gate; their repetition inside `release-tag-contract` prevents accidentally skipping them at publication time.

These are local/manual gates. The two-parent shape does not prove pull-request provenance, and because GitHub branch protection and repository rulesets are not currently configured, these checks do not imply that an invalid direct push would be rejected remotely.

The ancestry requirement prevents a version-correct commit that exists only on a development or release branch from becoming the public release commit. The tag-version check prevents a correct package set from being published under a different version tag.

### 3. Create the tag, verify its remote commit, then publish manifest-declared assets

Create and push only the already validated tag:

```bash
git tag "$TAG"
git push origin "$TAG"
make release-remote-tag-contract TAG="$TAG"
```

Do not retype a separate version string after the tag-version contract has passed. The remote-tag contract revalidates the full local release set again, then confirms that the remote tag resolves to the manifest `source_commit`; it does not rely on the GitHub Release `tag_name` or `target_commitish` as commit provenance.

GitHub Actions do not publish the Release automatically. Create the GitHub Release explicitly, use `--verify-tag`, and publish exactly the files listed by `release_assets` in the final manifest.

`.github/release-validation-note.md` remains part of the publication disclosure. Packaging success is not evidence that the method is empirically established.

### 4. Verify the remote tag and Release after upload

After GitHub accepts the upload, rerun `make release-remote-tag-contract TAG="$TAG"`, fetch the Release object, and run `scripts/verify_published_release.py`. The two checks cover different boundaries.

Remote-tag verification requires:

- the full local release set to remain valid immediately before the tag-specific check;
- the remote tag to exist;
- lightweight or annotated tag structure to peel successfully to a commit; and
- that resolved commit to match the final manifest `source_commit`.

Release-object verification requires:

- the supplied tag to match the final manifest version;
- the published tag to match that validated tag;
- the Release to be neither a draft nor a prerelease;
- the Release body to contain the required `.github/release-validation-note.md` disclosure, while allowing generated notes or other additional text;
- the published asset-name set to match the manifest-declared set exactly, with no missing or extra/manual assets;
- every asset to be in the uploaded state;
- published byte sizes to match the final manifest; and
- GitHub's published `sha256:` digest for every asset to match the final manifest, including a directly computed digest for `release-manifest.json`.

These post-publication checks are intentionally separate from package construction and from each other. Rechecking the tag against the manifest prevents the same incorrect tag value from being passed circularly to both Release lookup and verification; resolving the remote tag back to `source_commit` prevents a moved tag from silently changing the commit associated with the published version. The Release-object verifier independently checks publication state, disclosure text, and manifest-declared assets. `gh release upload --clobber` does not remove unrelated pre-existing assets, so an existing Release with stale or manual extras must fail verification instead of being silently treated as an exact manifest publication.

## Publication disclosure

A technically valid release candidate is not evidence that the method is empirically effective. While the project remains under validation, newly created GitHub Releases must keep that distinction visible to readers who arrive directly at the Release page.

- `.github/release-validation-note.md` is included in the notes for a newly created Release and is verified again from the published Release object.
- Keep that note semantically aligned with the validation-stage wording in the top-level README.
- Use `gh release create --verify-tag`; publication must refer to a tag that already exists remotely rather than allowing the CLI to synthesize one.
- Re-uploading assets for an existing tag does not automatically correct the release notes. If the disclosure itself needs correction, edit the notes deliberately and rerun published-release verification.

## Relationship to release history

The repository distinguishes a validated version boundary from a published release. See [`release-history.md`](release-history.md) for historical cases and do not infer publication merely from successful local validation or a merge to `main`.
