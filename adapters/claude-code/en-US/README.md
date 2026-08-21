# Cultural Substrate Weaving — English

Structural review for writing, design, analysis, and architecture. It surfaces missing connections, feedback effects, time lags, and irreversible choices, and validates each finding against your target before reporting it.

Version {{VERSION}} · MIT · [Repository](https://github.com/hat47x/cultural-substrate-weaving)

## Install

Claude Code:

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
```

```bash
claude plugin install csw-method-en@cultural-substrate-weaving
```

Codex reads the same plugin directory:

```bash
codex plugin marketplace add hat47x/cultural-substrate-weaving
```

## Use

The skill is **explicit-invocation only**. It never fires on its own, and it costs nothing until you call it.

```text
/csw-method-en:cultural-substrate-weaving-en <your request>
```

Examples:

- `Review this on-call rotation policy for missing handoffs and irreversible escalations.`
- `Check this service's responsibility boundaries — what breaks if the owning team changes?`
- `This chapter draft feels flat. Find what the structure is missing, not what the prose is missing.`
- `Our postmortem lists causes. Which relationships between them are unstated?`

## A worked example

Given a short on-call rotation policy (rotation is daily; the on-call engineer stays the customer's single point of contact even after escalating; response records are one line and counted monthly), an ordinary review returns the obvious gaps: no after-hours coverage, no definition of "cannot answer", no deadline on escalated cases.

Two findings came from the structural pass and survived the removal check:

1. **Daily rotation contradicts the single-point-of-contact promise.** The engineer who owns an escalated case is a different person tomorrow, and no handoff is defined.
2. **No path carries judgment forward.** Where the line falls for "cannot answer" varies by person, records are one line, and only counts are aggregated — so what one engineer decided never reaches the next.

Neither is in the baseline review. Both are statements about the policy, not about any framework.

## What is in this plugin

Fifteen Markdown files and two JSON manifests. **No executables, no MCP servers, no hooks, no network access, no bundled binaries.** The skill reads your material and writes its analysis; that is all it does.

Reference files load only when the analysis needs them, so a session that does not use the skill pays nothing for it.

## How it works, and what it does not claim

The method starts with ordinary domain analysis as a baseline, then borrows structure from external frameworks to find what the baseline missed, and validates every candidate against your material.

Cultural, philosophical, and traditional frameworks appear in the reference files as **examples of structure sources** — sets of positions defined before looking at your target. **The method does not assert that any of them is true, and it produces no predictions, divination, diagnoses, or claims about real people.**

The hypothesis is that such a framework behaves the way a pretrained representation behaves in transfer learning: a prior carrying structure that a single target cannot induce, whose value is settled by whether it improves the result rather than by its own correctness. The method enforces this with a **removal check** — every framework name, table, and term is deleted, and only findings that still stand as statements about your target are reported. The stated falsification condition is that surviving findings do not exceed the baseline.

See [Why an external framework at all](https://github.com/hat47x/cultural-substrate-weaving#why-an-external-framework-at-all-a-hypothesis-about-the-mechanism) for the full correspondence.

## Documentation

- [Use with Claude Code](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/en/platforms/claude-code.md)
- [Use with Codex](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/en/platforms/codex.md)
- [Architecture](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/en/architecture.md)
