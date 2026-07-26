# Create a Microsoft 365 Copilot agent

The repository generates a localized declarative-agent project for Microsoft 365 Agents Toolkit.

## Requirements

- A tenant licensed for Microsoft 365 Copilot.
- Visual Studio Code with Microsoft 365 Agents Toolkit, or the Agents Toolkit CLI.
- For CLI use: `npm install -g @microsoft/m365agentstoolkit-cli`.

## Build

```bash
python scripts/build.py
```

Choose `dist/en-US/microsoft-copilot/agent-project/` or the Japanese equivalent.

## Initialize an environment

```bash
python scripts/init_m365_env.py --locale en-US --env dev
```

The command creates a local environment file with publisher, privacy, terms, scope, and app ID values.

## Add detailed knowledge

Upload the files under `dist/en-US/microsoft-copilot/knowledge/` to one SharePoint site or document library, then rebuild with its URL:

```bash
python scripts/init_m365_env.py --locale en-US --env dev \
  --sharepoint-url "https://contoso.sharepoint.com/sites/csw"
python scripts/build.py
```

## Package and validate

```bash
cd dist/en-US/microsoft-copilot/agent-project
atk package --env dev
atk validate --env dev
```

## Test and publish

Use `atk provision --env dev` for personal testing. Move through staging before production. Production publication requires tenant permissions and administrator approval.
