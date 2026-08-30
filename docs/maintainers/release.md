# Release maintenance

## Validation levels

Use the lightweight development path for ordinary work:

```bash
make check
```

It rebuilds runtime outputs, validates source/generated parity, runs tests and token checks, validates Living Lab records, and writes review reports. It does **not** declare a release candidate or leave a release manifest behind.

Use the release path only when checking a release candidate:

```bash
make release-check
```

This runs `make check`, creates the locale/platform ZIP packages, writes the final `dist/release-manifest.json`, and independently validates the completed release set.

## Release manifest semantics

The release manifest is a **post-package release contract**, not a build-progress marker.

- `files` inventories all files present under `dist/` before the manifest itself is written. It is build provenance and includes generated trees that are not separately published as GitHub Release assets.
- `release_assets` lists exactly the files the Release workflow publishes: the manifest itself, package ZIPs, and validation/review reports.
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

Microsoft 365 has an additional tenant boundary. The canonical build is tenant-neutral: `scripts/build.py` does not read a local `.env.*` file and does not copy one into `dist/`. A tenant-specific SharePoint capability is added only when `CSW_M365_SHAREPOINT_SITE_URL` (or its locale-specific form) is explicitly present in the build environment.

Agents Toolkit deployment uses a separate explicit step. Generate a deployment file with `scripts/init_m365_env.py`, build with an explicitly injected SharePoint URL when needed, and then use `scripts/stage_m365_env.py` to copy that deployment-only file into the selected generated agent project. Public `make package` intentionally rejects the staged environment file, so tenant deployment and public GitHub Release packaging remain different paths.

The independent post-package validator also rejects private/local file names if they are already present inside a ZIP. For public M365 packages it additionally rejects a concrete `OneDriveAndSharePoint` site URL, so an accidentally tenant-specific build cannot pass the public release contract.

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

The GitHub Release workflow reads the already validated `release_assets` list and passes that exact list to `gh release create` or `gh release upload`. Do not duplicate the publication list as workflow globs.

## Publication disclosure

A technically green release candidate is not evidence that the method is empirically effective. While the project remains in validation, newly created GitHub Releases must keep that distinction visible to readers who arrive directly at the Release page.

- `.github/release-validation-note.md` is prepended to GitHub's automatically generated notes for a newly created Release.
- Keep that note semantically aligned with the validation-stage wording in the top-level README. Do not remove it merely because packaging and release validation are green.
- The Release workflow uses `gh release create --verify-tag`; publication must refer to a tag that already exists remotely rather than allowing the CLI to synthesize one.
- `workflow_dispatch` is for re-publishing assets for an existing tag. When the Release already exists, the workflow uploads/clobbers the validated assets but does not rewrite the release notes. If an existing release needs a disclosure correction, edit its notes deliberately rather than expecting asset re-publication to do so.

## Tag and publication flow

A `vX.Y.Z` tag push is the canonical automatic publication path. The tag must match the checked-out `VERSION`.

`workflow_dispatch` is only for re-publishing assets for an **existing** tag. It is not a substitute for creating a missing release tag.

A release candidate may keep its pending changes under `## Unreleased`. Once publication is deliberately chosen, freeze that material under exactly one dated heading of the form `## X.Y.Z — YYYY-MM-DD`, then restore an `## Unreleased` section for later work. The Release workflow checks the dated version heading before publishing, so packaging success alone cannot silently turn an unfrozen changelog into a release.

Before tagging a new release:

1. reconcile the active `develop/vX.Y.Z` line with `main` if necessary;
2. finalize `CHANGELOG.md` with the intended version and publication date while preserving a new `## Unreleased` section;
3. run/confirm `make release-check` on that finalized release candidate;
4. merge the validated release candidate to `main`;
5. confirm the post-merge Validate workflow succeeds;
6. create and push `vX.Y.Z` at the intended release commit; and
7. confirm the Release workflow and published asset set succeed, including the validation-stage disclosure while it remains applicable.

Do not move an existing release tag to include later development work.
