# Release internals

This document records release invariants and implementation details shared across locales. It is not the primary step-by-step guide.

Current procedures:

- [日本語のリリース手順](../ja/maintainers/release.md)
- [English release procedure](../en/maintainers/release.md)

GitHub Actions are currently disabled. There is no automatic Validate or Release workflow. A missing remote status is therefore not evidence that any validation ran. Public release gates are explicit local/manual operations.

## Validation levels

Use the ordinary development path for normal work:

```bash
make check
```

It rebuilds runtime outputs, validates source/generated parity and platform-specific contracts, checks natural-Japanese review freshness, runs tests and token checks, validates Living Lab records, and writes review reports. It does not create the final release manifest.

Use the packaging path for a release candidate:

```bash
make release-check
```

This runs `make check`, creates locale/platform packages, writes `dist/release-manifest.json`, and validates the completed package set.

Neither command by itself proves that the method is empirically effective.

## Release manifest semantics

The release manifest is a **post-package release contract**, not a build-progress marker.

- `files` inventories all files present under `dist/` before the manifest itself is written. It is build provenance and includes generated trees that are not separately published as GitHub Release assets.
- `release_assets` lists exactly the files that must be published for the GitHub Release: the manifest itself, package ZIPs, and validation/review reports.
- `schema_version` versions the manifest structure independently of the CSW method version.

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

- manifest version/locale/schema metadata;
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

A development line may keep work under `## Unreleased`. Before public publication, freeze the release under exactly one dated heading:

```text
## X.Y.Z — YYYY-MM-DD
```

Then restore an `## Unreleased` section for later work.

Validate the boundary explicitly:

```bash
python scripts/check_release_changelog.py \
  --version "$(cat VERSION)"
```

Do not treat successful packaging as permission to publish an unfrozen changelog.

### 2. Validate the exact commit that will be tagged

The tag must point to the commit that actually landed on `main`. After the release pull request merges:

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
make release-check
git merge-base --is-ancestor HEAD origin/main
```

If either validation fails, do not tag the commit.

This ancestry check prevents a version-correct commit that exists only on a development or release branch from becoming the public release commit.

### 3. Create the tag, then publish the manifest-declared assets

Create and push the version tag only after the exact `main` commit has passed the checks:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

GitHub Actions do not publish the Release automatically. Create the GitHub Release explicitly, use `--verify-tag`, and publish exactly the files listed by `release_assets` in the final manifest.

`.github/release-validation-note.md` remains part of the publication disclosure. Packaging success is not evidence that the method is empirically established.

### 4. Verify the remote Release after upload

After GitHub accepts the upload, fetch the Release object and run `scripts/verify_published_release.py`. The verification requires:

- the published tag to match the intended tag;
- the published asset-name set to match the manifest-declared set exactly, with no missing or extra/manual assets;
- every asset to be in the uploaded state;
- published byte sizes to match the final manifest; and
- GitHub's published `sha256:` digest for every asset to match the final manifest, including a directly computed digest for `release-manifest.json`.

This post-publication check is intentionally separate from package construction. `gh release upload --clobber` does not remove unrelated pre-existing assets, so an existing Release with stale or manual extras must fail verification instead of being silently treated as an exact manifest publication.

## Publication disclosure

A technically valid release candidate is not evidence that the method is empirically effective. While the project remains under validation, newly created GitHub Releases must keep that distinction visible to readers who arrive directly at the Release page.

- `.github/release-validation-note.md` is included in the notes for a newly created Release.
- Keep that note semantically aligned with the validation-stage wording in the top-level README.
- Use `gh release create --verify-tag`; publication must refer to a tag that already exists remotely rather than allowing the CLI to synthesize one.
- Re-uploading assets for an existing tag does not automatically correct the release notes. If the disclosure itself needs correction, edit the notes deliberately.

## Relationship to release history

The repository distinguishes a validated version boundary from a published release. See [`release-history.md`](release-history.md) for historical cases and do not infer publication merely from successful local validation or a merge to `main`.
