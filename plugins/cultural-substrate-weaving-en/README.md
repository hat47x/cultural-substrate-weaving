# Cultural Substrate Weaving — English

Structural review for writing, design, analysis, and architecture. It surfaces missing connections, feedback effects, time lags, and irreversible choices, and validates each finding against your target before reporting it.

Version 0.2.0 · MIT · [Repository](https://github.com/hat47x/cultural-substrate-weaving)

## Install

Claude Code:

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
```

```bash
claude plugin install cultural-substrate-weaving-en@cultural-substrate-weaving
```

Codex reads the same plugin directory:

```bash
codex plugin marketplace add hat47x/cultural-substrate-weaving
```

## Use

The skill is **explicit-invocation only**. It never fires on its own, and it costs nothing until you call it.

```text
/cultural-substrate-weaving-en:weave <your request>
```

Examples:

- `Review this on-call rotation policy for missing handoffs and irreversible escalations.`
- `Check this service's responsibility boundaries — what breaks if the owning team changes?`
- `This chapter draft feels flat. Find what the structure is missing, not what the prose is missing.`
- `Our postmortem lists causes. Which relationships between them are unstated?`

## A worked example

For the premise "a small factory in a provincial city closes down; a short story covering that year", a controlled run used three agents sharing no context: a control with no method, a treatment applying it in full, and a blind judge.

**Both arms landed independently on the same central metaphor.** The judge, knowing nothing of the method, wrote that anyone setting out to write this premise seriously "arrives here about eighty per cent of the time". **A third party confirmed the local optimum.**

The baseline the treatment wrote for itself was structurally the control's plan. The framework pass moved the central claim off it — the closure went from endpoint to starting point, the eleven months after became the book, and an antagonist appeared.

**A transition run found a state never reached, and the one card the KJ integration could not group landed exactly there.** Separate routes, one absence.

The judge expects the control to be finished and more to remain from the treatment. **On the 2,000-character opening itself, the control is the better piece of writing.** Both arms also dropped the same character, so the method did not break the blind spot they shared.

The treatment produced about six times the output. This is not a comparison at equal token spend.

## Worked examples

[Worked examples](https://github.com/hat47x/cultural-substrate-weaving/blob/main/docs/en/examples.md) records each application with its baseline alongside the increment. **Three cases so far, only one of which meets the precondition — not enough to establish that the method works.** The falsification condition is stated and each case is measured against it.

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
