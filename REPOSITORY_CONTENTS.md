# Repository contents

This file is a responsibility-boundary map, not an exhaustive file list.

## Method and localization

- [`src/`](src/) — runtime method source. `src/ja-JP/` is the semantic canonical source, `src/en-US/` is the structurally parallel English translation, and `src/manifest.json` defines the runtime module surface.
- [`i18n/`](i18n/) — glossary, translation provenance, reviewed source hashes, and translation policy.

## Platform packaging and distribution metadata

- [`adapters/`](adapters/) — platform-specific packaging sources for OpenAI Skills, ChatGPT custom GPTs, Claude Code, Microsoft 365 Copilot, and project integrations.
- [`plugins/`](plugins/) — generated, Git-tracked localized plugin trees. Each generated plugin carries the metadata and skill files needed by the supported Claude/Codex distribution surfaces.
- [`.claude-plugin/`](.claude-plugin/) — top-level Claude Plugin Marketplace metadata.
- [`.agents/plugins/`](.agents/plugins/) — top-level Codex plugin marketplace metadata.

## Documentation, research, and observation

- [`docs/`](docs/) — user guides, platform guidance, experiments, maintainer procedures, and shared internals.
- [`research/`](research/) — research records and preserved analysis assets. These do not become runtime method rules merely by existing here.
- [`.living-lab/`](.living-lab/) — private-by-default local Web Chat Living Lab workspace. Git tracks only its operating README; actual local records are ignored unless separately anonymized or abstracted into a publishable research record.
- [`evals/`](evals/) — Living Lab schemas, examples, and other machine-readable evaluation contracts.

## Build, validation, and repository operation

- [`scripts/`](scripts/) — build, validation, packaging, release, provenance, translation, and observation utilities.
- [`tests/`](tests/) — regression and repository-contract tests.
- [`.github/`](.github/) — issue/PR templates and repository publication metadata.
- `dist/` — locally generated release candidates and reports. It is ignored by Git and recreated by the build/package flow.
