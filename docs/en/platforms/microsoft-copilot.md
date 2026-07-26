# Create a Microsoft 365 Copilot agent

The repository generates a localized declarative-agent project for Microsoft 365 Agents Toolkit.

## Requirements

- A tenant licensed for Microsoft 365 Copilot.
- Visual Studio Code with Microsoft 365 Agents Toolkit, or the Agents Toolkit CLI.
- For CLI use: `npm install -g @microsoft/m365agentstoolkit-cli`.
- Web search grounding allowed for the tenant. The method assumes fact-checking via search.

## 1. Get the package

Download `cultural-substrate-weaving-m365-copilot-en-US-vX.Y.Z.zip` (or `-ja-JP-` for Japanese) from [GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases) and extract it. It contains the full Agents Toolkit project under `agent-project/`. No build step is required.

## 2. Add SharePoint knowledge (effectively required)

The declarative agent's `instructions` field only carries the activation check, minimum execution steps, and the judgment axes — nothing more. The 11 detailed reference modules that back actual judgment (activation criteria, the four viewpoints and five constraints, iteration, scope and facts, system selection, transformation, generation and validation, character and taiheki, output and collaboration, creative patterns, governance and records, final evaluation) exist only under `knowledge/`, and the agent has no way to read them unless they're grounded via SharePoint. Without this step, the agent can only handle the shallow "obviously not applicable / narrow scope" cases — most of the method simply doesn't work. Don't use the package extracted in step 1 as-is; rebuild it with the steps below first.

1. Upload the files under `knowledge/` to one SharePoint site or document library.
2. Clone the repository.
3. Run:

```bash
python scripts/init_m365_env.py --locale en-US --env dev \
  --sharepoint-url "https://contoso.sharepoint.com/sites/csw"
python scripts/build.py
```

4. Use `dist/en-US/microsoft-copilot/agent-project/` instead of the one extracted in step 1.

## 3. Fill in the environment file

Copy `agent-project/env/.env.dev.example` to `agent-project/env/.env.dev` and fill in the developer name, website URL, privacy policy URL, terms URL, and a `M365_APP_ID` (any GUID). These are substituted into the manifest when you run `atk package`.

## 4. Package and validate

```bash
cd agent-project
atk package --env dev
atk validate --env dev
```

## 5. Test and publish

Use `atk provision --env dev` for personal testing. Move through staging before production. Production publication requires tenant permissions and administrator approval.
