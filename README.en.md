# cultural-substrate-weaving

[日本語](README.md) | [English](README.en.md)

A complementary AI skill that combines **structure candidates from cultural, philosophical, and traditional frameworks** with **KJ-method integration and gap discovery**. It explores questions, relations, states, and transitions that ordinary domain methods may not surface, then validates them against the target.

The skill does **not** replace domain expertise or quality criteria in writing, management, software engineering, law, or other fields. Use it alongside a **domain-specific skill** when appropriate; cultural-substrate-weaving is responsible only for the increment produced by its cultural-framework and KJ capabilities.

> **The project is still under validation.** The Web Chat Living Lab was introduced in v0.4.0, and the published v0.4.0 method is being observed in real work. Public records distinguish prospective observations made under an already-declared observation plan from retrospective records anonymized or abstracted from natural work after the fact. Public observations are still limited, and the effectiveness of the skill is not treated as established at this stage. See **[Web Chat Living Lab](docs/en/experiments/web-chat-living-lab.md)** / **[public observations](research/living-lab/observations/)**.

## Install

**Claude Code**

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
claude plugin install cultural-substrate-weaving-en@cultural-substrate-weaving
```

**Codex**

```bash
codex plugin marketplace add hat47x/cultural-substrate-weaving
```

For ChatGPT custom GPT and Microsoft 365 Copilot, use the platform package from GitHub Releases. The current Microsoft 365 distribution is a limited adapter: only the content under `instructions.txt` is treated as agent instructions. See the [Microsoft 365 Copilot guide](docs/en/platforms/microsoft-copilot.md) for the current boundary.

## What the caller supplies

This skill does not provide domain-specific professional competence. Accuracy standards, implementation procedures, craft quality, style, and other domain criteria belong to the caller's context or to another domain skill used alongside this one. See **[Usage context](docs/en/usage-context.md)**.

## Languages

| Locale | Status | Note |
|---|---|---|
| Japanese (`ja-JP`) | Semantic canonical source | Authoritative method text |
| English (`en-US`) | Translation | Usable; independent human review is recommended before authoritative publication |

## Platforms

- OpenAI Codex Plugin / directly placed Skill
- Claude Code Plugin Marketplace
- ChatGPT custom GPT update pack
- Microsoft 365 Copilot declarative agent (currently limited; see the platform guide)
- References from `AGENTS.md` / `CLAUDE.md`

## Build

Python 3.11+; no external Python packages are required.

```bash
git clone https://github.com/hat47x/cultural-substrate-weaving.git
cd cultural-substrate-weaving
make check
make package
```

## Core principle

> **Return structures obtained from external frameworks to the target for validation. What remains belongs to the target, not to the framework.**

In KJ integration, do not force material into prior card types. Preserve semantic unity and epistemic boundaries while integrating it.

> **Join when semantic unity must be preserved; split when epistemic state must be preserved.**

## Why use an external framework? A hypothesis

The method does not claim that cultural frameworks are true. It treats their pre-existing positions, relations, and transitions as prior structure that may open search directions ordinary analysis does not produce.

At the end, framework names and correspondence tables are removed. Only findings that still stand as statements about the target remain. If surviving findings do not exceed a no-framework baseline, no skill-specific increment has been demonstrated.

## License

MIT License
