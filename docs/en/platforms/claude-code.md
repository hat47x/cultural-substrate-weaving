# Use with Claude Code

This GitHub repository can be used as a Claude Plugin Marketplace.

The method relies on web search in some cases for fact-checking and gathering context. Confirm that the WebSearch/WebFetch tools are available in Claude Code.

`/plugin` opens an interactive panel that only runs in the terminal CLI. How you install the plugin depends on which environment you're using.

## Terminal CLI (the standalone `claude` command)

Run this inside an interactive session:

```text
/plugin marketplace add hat47x/cultural-substrate-weaving
/plugin install csw-method-en@cultural-substrate-weaving
/reload-plugins
```

The Japanese plugin is `csw-method-ja`.

To add it non-interactively (e.g. from a script):

```bash
claude plugin marketplace add hat47x/cultural-substrate-weaving
claude plugin install csw-method-en@cultural-substrate-weaving
```

## Claude Desktop (Code tab, local and SSH sessions)

Desktop's own plugin browser only lists marketplaces that are already registered. To use a non-official marketplace like this one, register it first, either by:

- Running the terminal CLI commands above once (Desktop shares the `~/.claude` configuration with the CLI, so the plugin then appears under **+** → **Plugins** → **Manage plugins**), or
- Adding the following to the repository's `.claude/settings.json` for team-wide setup (teammates are prompted to install it when they trust the folder):

```json
{
  "extraKnownMarketplaces": {
    "cultural-substrate-weaving": {
      "source": { "source": "github", "repo": "hat47x/cultural-substrate-weaving" }
    }
  },
  "enabledPlugins": ["csw-method-en@cultural-substrate-weaving"]
}
```

Once registered, install it from Desktop via **+** → **Plugins** → **Add plugin**.

## Cloud sessions (claude.ai web, etc.)

The plugin browser isn't available in cloud sessions. Configure `extraKnownMarketplaces` and `enabledPlugins` in `.claude/settings.json` as shown above so the plugin installs automatically at session start.

## WSL sessions

Plugins aren't available in WSL sessions.

## If you see "/plugin isn't available in this environment"

This appears when a `/plugin` command is run somewhere other than an interactive terminal session (Desktop, cloud, or a non-interactive session). Follow the matching section above instead.

## Invoke

```text
/csw-method-en:cultural-substrate-weaving-en Review the responsibility boundaries and time-lag effects in this architecture.
```

The plugins use explicit invocation by default to reduce unnecessary context and token consumption.

## Update

```text
/plugin marketplace update cultural-substrate-weaving
/reload-plugins
```

Install one locale unless you have a clear reason to keep both.
