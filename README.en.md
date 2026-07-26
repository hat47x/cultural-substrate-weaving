# cultural-substrate-weaving

[日本語](README.md) | [English](README.en.md)

A general-purpose AI method for improving metacognition wherever structure is written, analyzed, designed, or implemented. It explores, validates, and transforms target-specific relationships, missing connections, feedback effects, time lags, and irreversible choices.

Cultural, philosophical, and traditional frameworks are not the primary purpose. They are optional auxiliary models for discovering structures that ordinary domain-specific methods may not reveal.

## Supported locales

| Locale | Status | Note |
|---|---|---|
| Japanese (`ja-JP`) | Semantic canonical source | Governs method-level interpretation |
| English (`en-US`) | Translated | Usable; independent human review is recommended before authoritative publication |

## Platform adapters

- OpenAI Codex Skill, in implicit and explicit-invocation profiles
- Claude Code Plugin Marketplace
- ChatGPT custom GPT update pack
- Microsoft 365 Copilot declarative agent
- Project entry points for `AGENTS.md` and `CLAUDE.md`

## First steps

| Platform | English guide | Japanese guide |
|---|---|---|
| Codex | [Use with Codex](docs/en/platforms/codex.md) | [Codexで使う](docs/ja/platforms/codex.md) |
| Claude Code | [Use with Claude Code](docs/en/platforms/claude-code.md) | [Claude Codeで使う](docs/ja/platforms/claude-code.md) |
| ChatGPT GPTs | [Create a custom GPT](docs/en/platforms/chatgpt-gpt.md) | [カスタムGPTを作る](docs/ja/platforms/chatgpt-gpt.md) |
| Microsoft 365 Copilot | [Create a Copilot agent](docs/en/platforms/microsoft-copilot.md) | [Copilot Agentを作る](docs/ja/platforms/microsoft-copilot.md) |

## Build

Python 3.11 or later is required. No third-party Python packages are needed.

```bash
git clone https://github.com/hat47x/cultural-substrate-weaving.git
cd cultural-substrate-weaving
make check
make package
```

Generated artifacts are written under `dist/<locale>/` and `dist/packages/`.

## Source, translations, and generated files

- `src/ja-JP/`: semantic canonical source
- `src/en-US/`: structurally parallel English translation
- `i18n/`: glossary, source hashes, and review policy
- `adapters/`: platform- and locale-specific templates
- `scripts/`: multilingual build and validation
- `plugins/`: generated and committed Claude Marketplace plugins
- `dist/`: release artifacts; not committed

## Core principle

> Return structures obtained from external frameworks to the target for validation. Whatever remains belongs not to the framework, but to the target.

## License

MIT License. Replace publisher details and Microsoft 365 privacy and terms URLs before public deployment.
