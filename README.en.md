# cultural-substrate-weaving

[日本語](README.md) | [English](README.en.md)

A general-purpose AI method for improving metacognition wherever structure is written, analyzed, designed, or implemented. It explores, validates, and transforms target-specific relationships, missing connections, feedback effects, time lags, and irreversible choices.

Cultural, philosophical, and traditional frameworks are not the primary purpose. They are optional auxiliary models for discovering structures that ordinary domain-specific methods may not reveal.

## Install

**Claude Code** — this repository is the plugin marketplace. Nothing to download.

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
```

```bash
claude plugin install csw-method-en@cultural-substrate-weaving
```

For Japanese, use `csw-method-ja@cultural-substrate-weaving`. Invoke with `/csw-method-en:cultural-substrate-weaving-en`. Desktop, cloud sessions, and team-wide setup are covered in [Use with Claude Code](docs/en/platforms/claude-code.md).

**Codex** — the same repository is also a Codex plugin marketplace. Nothing to download.

```bash
codex plugin marketplace add hat47x/cultural-substrate-weaving
```

Then install `csw-method-en` (or `csw-method-ja`). See [Use with Codex](docs/en/platforms/codex.md).

**ChatGPT custom GPT and Microsoft 365 Copilot**: download the ZIP for your locale and platform from [GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases). The guides in the table below cover each one.

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

## Why an external framework at all (a hypothesis about the mechanism)

This method does not claim that cultural, philosophical, or traditional frameworks are true. **It hypothesizes that they act the way transfer learning acts in machine learning.**

In transfer learning, a representation pretrained on a large source domain is carried into a target domain that has too little data to induce it. What decides the value of the pretrained representation is not whether it is itself correct, but **whether performance on the target improves.**

| Transfer learning | This method |
|---|---|
| Pretraining corpus | A cultural framework — a structure that survived passage through many targets |
| Pretrained representation | The **position layer**: a fixed set of places whose meanings are defined before looking at the target |
| Inductive bias (a prior) | Supplies positions the target does not hold on its own |
| Fine-tuning on the target | **Assignment**, and validation against the target |
| Domain-mismatch check | **Unit compatibility**: whether the kinds of unit and the principles of division agree |
| Negative transfer | **Over-application**: imposing a structure that does not fit |
| Ablation | The **removal check**: delete the framework's vocabulary and count the findings that still stand |
| Keeping or discarding the pretrained part | Adoption state: carried into the artifact, internal scaffolding, auxiliary model, rejected |

The hypothesis has two parts.

1. **A structure that cannot be induced from one target can be carried in as a prior.** Cultural frameworks are structures selected across many targets, so they are taken to have this property.
2. **The most useful output is where the prior and the target disagree.** A position that will not fill is itself a finding. This is why detecting blanks is the primary product.

**This is a hypothesis, not a measured claim.** It is falsified when findings that survive the removal check do not exceed the baseline. If surviving findings do not increase against a baseline built without the framework, no transfer occurred. The method requires that comparison on every run.

## License

MIT License. Replace publisher details and Microsoft 365 privacy and terms URLs before public deployment.
