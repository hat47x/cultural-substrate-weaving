# Use with Claude Code

This GitHub repository can be used as a Claude Plugin Marketplace.

When a task needs current facts, external context, or additional source discovery, confirm that Claude Code's WebSearch/WebFetch tools are available. They are not required for perspective analysis or discovery that can be completed from the supplied repository or material alone. Treat search availability as part of the available information surface; whether unsupported areas may be handled as inference, hypothesis, or assertion follows the evidence standard and delegation supplied by the requester.

`/plugin` opens the interactive plugin manager in terminal Claude Code. Installation details vary by surface.

## Terminal CLI (the standalone `claude` command)

Run this inside an interactive session:

```text
/plugin marketplace add hat47x/cultural-substrate-weaving
/plugin install cultural-substrate-weaving-en@cultural-substrate-weaving
/reload-plugins
```

The Japanese plugin is `cultural-substrate-weaving-ja`.

To add it non-interactively, for example from a script:

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
claude plugin install cultural-substrate-weaving-en@cultural-substrate-weaving
```

## Claude Desktop (Code tab, local and SSH sessions)

For a non-official marketplace such as this repository, register the marketplace before expecting its plugin to appear in a plugin browser. One option is to run the terminal CLI commands above once. For a repository-scoped team setup, use `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "cultural-substrate-weaving": {
      "source": { "source": "github", "repo": "hat47x/cultural-substrate-weaving" }
    }
  },
  "enabledPlugins": {
    "cultural-substrate-weaving-en@cultural-substrate-weaving": true
  }
}
```

After registration, use the plugin UI available on your current Claude surface. Product UI labels can change; the `/plugin` manager in terminal Claude Code is the reference path when available.

## Cloud sessions (claude.ai web, etc.)

Do not assume that a cloud session exposes the same local plugin manager or filesystem as terminal Claude Code. If you expect repository configuration to load a plugin, confirm how that surface handles project settings and plugin marketplaces.

## A simpler alternative: upload it as a Skill

If the Plugin Marketplace route is inconvenient, you can use Claude's Skills feature on a surface that supports skill upload. Plan, UI, and administrator availability are controlled by the Claude product rather than this repository.

1. Download the `openai-skill-metered` or `openai-skill-interactive` ZIP from GitHub Releases (the same package used in [Use with Codex](codex.md)).
2. If your Claude surface provides Skills upload, upload the ZIP as-is.
3. After installation, check invocation behavior under that surface's workspace and project settings.

The Claude Plugin declares `disable-model-invocation: true` and therefore uses explicit invocation. An uploaded Skill follows its package profile and the host surface's behavior; do not assume it has the same activation policy as the plugin.

## WSL

Claude Code supports WSL, and plugin marketplace settings are part of the Linux/WSL configuration surface. Do not treat plugins as unavailable merely because the session runs in WSL; use the normal terminal CLI flow. In managed environments, Windows-side managed settings can also be configured to flow into WSL.

## If you see "/plugin isn't available in this environment"

This can appear when plugin commands are invoked from a surface that does not expose the interactive terminal manager. Check whether that surface provides another plugin UI or reads project settings; otherwise configure the marketplace from terminal Claude Code.

## Invoke

For explicit invocation, for example:

```text
/cultural-substrate-weaving-en:weave Review the responsibility boundaries and time-lag effects in this architecture.
```

The plugin uses explicit invocation. The scope of the work follows the request or project delegation, together with the settings supported by the Claude surface.

## Update

```text
/plugin marketplace update cultural-substrate-weaving
/reload-plugins
```

Install one locale or both according to your workspace or author-defined configuration.
