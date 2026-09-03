# Use with Codex

When a task needs current facts, external context, or additional source discovery, confirm that Codex network access or web search is available. It is not required for KJ integration or structural exploration that can be completed from the supplied repository or material alone. If search is unavailable, do not guess missing external facts.

## Recommended: install as a plugin

Plugins are now the primary unit for discovering and distributing workflow capabilities across ChatGPT and Codex. This repository includes a Codex plugin marketplace, so you can install it without manually extracting a ZIP.

For a local Codex CLI installation:

```bash
codex plugin marketplace add hat47x/cultural-substrate-weaving
codex plugin add cultural-substrate-weaving-en@cultural-substrate-weaving
```

The Japanese plugin is `cultural-substrate-weaving-ja`. Inspect configured marketplaces and plugins when needed:

```bash
codex plugin marketplace list
codex plugin list
```

The plugin directory is shared with the Claude Code package and carries both `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`.

## Share through a workspace

Workspace administrators can import the GitHub marketplace through Workspace settings and manage the plugins that members can use.

1. Open **Workspace settings > Plugins > Add > Import marketplace**.
2. Set Source to `https://github.com/hat47x/cultural-substrate-weaving`.
3. Leave Path empty because this repository stores the marketplace at the root under `.agents/plugins/marketplace.json`.
4. After import, review the installation policy for each plugin and any requirements for included apps.

A marketplace imported from GitHub can stay synchronized with the repository. This route is useful when a workspace should manage one shared installation source.

## Skill format (direct placement)

The standalone Skill format remains useful for direct placement, compatibility with existing setups, and portability across products. Prefer the plugin for the main installation path, but do not treat Skill ZIPs as categorically invalid or deprecated.

For a local Codex CLI or IDE setup that uses directly placed Skills:

1. Download the `openai-skill-metered` or `openai-skill-interactive` ZIP from GitHub Releases.
2. Extract the `cultural-substrate-weaving` folder to:
   - `~/.agents/skills/` for personal use; or
   - `.agents/skills/` inside a repository for team use.
3. Restart Codex or start a new session so the Skill is reloaded.

## Using it in Codex Cloud

Do not assume that a cloud task can see the local machine's `~/.agents/skills/`. For repository-carried Skills, use `.agents/skills/`. For plugins, follow the plugin configuration, Sources / Plugins UI, and workspace policy exposed by the Codex environment you are using.

## Which form to choose

- **Plugin**: recommended current installation path when you want marketplace-based discovery and updates.
- **metered Skill**: direct Skill placement with explicit invocation only.
- **interactive Skill**: direct Skill placement where eligible implicit activation is acceptable.

## Invoke

```text
$cultural-substrate-weaving Review the responsibility boundaries, information flow, and irreversible choices in this design.
```

Do not use the method for routine implementation, simple proofreading, or a bounded local bug.

## Project instructions

Add only the short fragment under `adapters/project-integrations/en-US/codex/` to `AGENTS.md`. Do not place the full method in a file that is always loaded.
