# Use with Codex

The method relies on web search in some cases for fact-checking and gathering context. Confirm that Codex's network access / web search tool is enabled.

## Install as a plugin (nothing to download)

This repository is also a Codex plugin marketplace. No ZIP, no extraction.

```bash
codex plugin marketplace add hat47x/cultural-substrate-weaving
```

Then install `cultural-substrate-weaving-en` (or `cultural-substrate-weaving-ja`). The plugin directory is shared with the Claude Code plugin and carries both a `.codex-plugin/plugin.json` and a `.claude-plugin/plugin.json`.

Codex moved from standalone skills to plugins in June 2026, and `openai/skills` is deprecated. The skill layout below is kept for existing users; prefer the plugin for new installs.

## Install as a skill (legacy, Codex CLI and IDE extension)

The CLI and the IDE extension both run on your local machine and read skills from the same filesystem.

1. Download an OpenAI Skill ZIP for your locale from GitHub Releases.
2. Choose `metered` for explicit invocation only, or `interactive` for eligible implicit activation.
3. Extract the `cultural-substrate-weaving` folder to:
   - `~/.agents/skills/` for personal use; or
   - `.agents/skills/` inside a repository for team use.
4. Restart Codex.

## Using it in Codex Cloud

Codex Cloud tasks run in a sandbox cloned from your repository, so your local `~/.agents/skills/` (personal skills) isn't visible there. To use the method in Codex Cloud, commit the skill folder into the target repository's `.agents/skills/` instead.

## Invoke

```text
$cultural-substrate-weaving Review the responsibility boundaries, information flow, and irreversible choices in this design.
```

Do not use the method for routine implementation, simple proofreading, or a bounded local bug.

## Project instructions

Add only the short fragment under `adapters/project-integrations/en-US/codex/` to `AGENTS.md`. Do not place the full method in a file that is always loaded.
