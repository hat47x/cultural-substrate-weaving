# cultural-substrate-weaving

[日本語](README.md) | [English](README.en.md)

A complementary AI skill that **opens cultural, philosophical, and traditional frameworks as temporary cognitive fields, then returns the questions, relations, states, and transition candidates they produce to the target for validation**. Cultural frameworks are not treated as answers or classifiers. Only portions independently supported by target-side material are treated as findings about the target.

> **This research branch is testing a method split.** Both the Japanese canonical source and the English CSW runtime now use the thin-CSW boundary: one-round material synthesis is delegated to `affinity-synthesis`, while multi-round delta/reopen orchestration is delegated to `iterative-inquiry-synthesis`. The two sibling prototypes now also have initial English `SKILL.en.md` and `METHOD.en.md` drafts alongside their Japanese research realizations. This does not mean that a three-Skill distribution has already been publicly released. Multi-skill distribution generation/rebuild, independent review of the English prototype realizations, and classification or translation of ancillary research references/evals remain incomplete.

These methods do **not** replace domain expertise or quality criteria in writing, management, software engineering, law, or other fields. Domain capability comes from the caller's context or another domain-specific skill used alongside them.

> **The project is still under validation.** The Web Chat Living Lab was introduced in v0.4.0, and the published method is being observed in real work. Public records distinguish prospective observations made under an already-declared observation plan from retrospective records anonymized or abstracted from natural work after the fact. Public observations are still limited, and the effectiveness of the method is not treated as established at this stage. See **[Web Chat Living Lab](docs/en/experiments/web-chat-living-lab.md)** / **[public observations](research/living-lab/observations/)**.

## Three layers on this research branch

```text
cultural-substrate-weaving
  open a cultural framework
  -> preserve attribution of framework-generated candidates
  -> return them to the target

        ↓ material / handoff

affinity-synthesis   [research prototype]
  one-round material-led synthesis
  -> card / group / label / relation
  -> diagram <-> narrative <-> source checks

        ↓ delta / residual

iterative-inquiry-synthesis   [research prototype]
  multi-round delta-based reopening
  -> reopen only touched artifacts when appropriate
  -> preserve history, residuals, and stop/restart conditions
```

Method Definitions are separated from their Agent Skill realizations. If a future external Skill satisfies the same invariants and regression fixtures, the local realization should be replaceable or reducible rather than preserved for its own sake.

## Install

The commands below refer to the current `cultural-substrate-weaving` distribution. Do not treat `affinity-synthesis` or `iterative-inquiry-synthesis` as separately released Skills yet.

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

These methods do not provide domain-specific professional competence. Accuracy standards, implementation procedures, craft quality, style, and other domain criteria belong to the caller's context or another domain skill used alongside them. See **[Usage context](docs/en/usage-context.md)**.

## Languages

| Locale | Status | Note |
|---|---|---|
| Japanese (`ja-JP`) | Semantic canonical source | Thin CSW plus the canonical research realizations for both sibling methods |
| English (`en-US`) | Translated draft | Thin CSW runtime is translated; initial English runtime / Method Definition drafts now exist for both sibling Skills. Independent review and ancillary research-material parity remain incomplete |

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
make research-skill-check   # when changing the split-method prototypes
make check
make package
```

GitHub Actions are currently disabled. Validation is performed in a local or equivalent execution environment.

## Canonical sources, translations, and generated artifacts

- `src/ja-JP/`: semantic canonical source for the CSW runtime
- `src/en-US/`: English CSW runtime translation
- `research/skill-prototypes/`: split Method Definitions, Skill realizations, evals, and representation research, including Japanese research canon and English realization drafts
- `i18n/`: terminology, source hashes, translation-review policy
- `adapters/`: platform- and locale-specific templates
- `scripts/`: multilingual build and validation tooling
- `plugins/`: generated and Git-tracked artifacts
- `dist/`: release artifacts; not tracked by Git

## Core principles

The CSW boundary is:

> **Return structures obtained from external frameworks to the target for validation. Treat only the parts independently supported by target-side material as findings about the target.**

The research Method Definition for `affinity-synthesis` draws from KJ-method, affinity-diagram, and qualitative-synthesis lineage while recording AI-era implementation corrections separately. A central boundary rule is:

> **Join when semantic unity must be preserved; split when epistemic state must be preserved.**

KJ Method is a registered trademark of Kawakita Research Institute. This prototype does not claim to be an official KJ Method Agent Skill or a complete reproduction of the method.

## Why use an external framework? A hypothesis

The method does not claim that cultural frameworks are true. It treats their pre-existing positions, relations, and transitions as prior structure that may open search directions ordinary analysis does not produce.

Questions, hypotheses, or descriptions may remain meaningful after framework names and correspondence tables are removed. That only shows that they have been de-bound from the framework's authority; it does not create additional target-side evidence. In research and diagnosis, only parts independently supported by target-side sources, observations, or falsification are treated as findings. In generation and composition, framework-generated structure may be adopted as a compositional resource, but it remains distinct from facts about the target.

A no-framework baseline can help show what changed in questions, search directions, artifacts, or decisions, but counts alone do not establish the effectiveness of the method.

## License

MIT License
