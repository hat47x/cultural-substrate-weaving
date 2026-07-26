# Use with Claude Code

This GitHub repository can be used as a Claude Plugin Marketplace.

## Install

Replace `OWNER` with the actual GitHub user or organization.

```text
/plugin marketplace add OWNER/cultural-substrate-weaving
/plugin install csw-method-en@cultural-substrate-weaving
/reload-plugins
```

The Japanese plugin is `csw-method-ja`.

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
