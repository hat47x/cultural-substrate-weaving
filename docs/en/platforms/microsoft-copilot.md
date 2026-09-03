# Create a Microsoft 365 Copilot agent

The repository generates localized declarative-agent material for Microsoft 365 Copilot in Japanese and English. There are two ways to install it: a GUI-only route through Agent Builder, or a route through the Agents Toolkit CLI. If you do not need a special organization-managed deployment, Agent Builder is the simpler place to start.

Web search is not required when the task can be completed from supplied material alone, such as KJ integration over a closed source set. When a task needs current facts, external context, or additional source discovery, confirm that web-search grounding is permitted for your tenant.

## Current scope of the Microsoft 365 package

In Microsoft 365 Copilot, Knowledge is primarily a source of factual grounding. Do not treat it as a reliable continuation of the agent-level instructions in **Instructions**.

For Microsoft 365, this repository therefore provides a self-contained **limited profile** that stays within the 8,000-character Instructions limit. Only the method written in `instructions.txt` is treated as executable agent instructions. It carries the core retained by this profile: staying revisable by the target, KJ integration around semantic units and epistemic boundaries, provenance controls for cultural-framework exploration, delegated-scope discipline, and separation of observation from AI interpretation.

The richer CSW method modules are still bundled under `method-reference/` so that people can inspect the full method without discarding that material. They are human-readable reference assets, not files to upload to Agent Builder or SharePoint Knowledge in order to extend Instructions.

You can still add business documents, research material, organization documents, and other target-side sources to Knowledge for factual grounding.

This limited profile does not claim full CSW parity with the other supported platforms. Detailed framework-specific operations, the Taiheki special case, the complete longitudinal research protocol, and other procedures not present in `instructions.txt` remain outside this profile. Use the Codex, Claude Code, or ChatGPT distributions when those capabilities are required. The design history and boundary are tracked in Issue #96.

## Get the package

Download `cultural-substrate-weaving-m365-copilot-en-US-vX.Y.Z.zip` (or `-ja-JP-` for Japanese) from [GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases) and extract it. It contains:

- `instructions.txt`: the self-contained Microsoft 365 limited profile;
- `method-reference/`: human-readable reference material for the full CSW method;
- `README.txt`: the package boundary and usage notes; and
- `agent-project/`: the Agents Toolkit CLI project.

The standard GitHub Release package is **tenant-neutral**. It does not contain a tenant-specific SharePoint site URL or actual `.env` / `.env.*` files. Only safe `.example` templates are included under `agent-project/env/`. Tenant-specific values are injected explicitly when you prepare an organization deployment.

## Method A: Agent Builder (GUI only)

If you have a Microsoft 365 Copilot license, you can create the agent directly with no CLI or code editing. You don't need `agent-project/`, Node.js, or Visual Studio Code.

This repository uses manual configuration so the prepared `instructions.txt` can be applied directly instead of relying on the natural-language auto-generation flow.

1. Open Microsoft 365 Copilot at microsoft365.com/chat, office.com/chat, or in Teams, and select **New agent**.
2. Select **Skip to configure** to open the **Configure** tab.
3. Fill in **Name** and **Description** (30 and 1,000 characters respectively).
4. Paste the contents of the extracted `instructions.txt` into **Instructions** as-is. Build and validation checks keep it within the 8,000-character limit.
5. If the agent needs target-side business or research material, add it under **Knowledge**. You can add up to 20 files uploaded directly from the device as embedded knowledge sources. Do not upload the package's `method-reference/` directory in order to extend Instructions.
6. If the agent needs current facts or external information, enable **Search all websites** under **Knowledge**. It is not required when the agent should stay within supplied material.
7. Test both activation and non-activation examples on the **Try it** tab. Also verify that the work you need fits within the limited profile.
8. After creating the agent, use **Share** for direct sharing. For organization-wide availability, use **…** → **Submit to your org catalog** and follow your administrator's review process.

## Method B: Agents Toolkit CLI (advanced / org-managed deployment)

Use this route when you need AppSource distribution, tenant-wide managed deployment, SharePoint grounding for target-side sources, or another configuration that Agent Builder does not provide.

### Requirements

- Visual Studio Code with Microsoft 365 Agents Toolkit, or the Agents Toolkit CLI.
- For CLI use: `npm install -g @microsoft/m365agentstoolkit-cli`.

### 1. Prepare target-side material in SharePoint Knowledge

When SharePoint is used as Knowledge, put the business, research, or organization documents that the agent should use as factual grounding there. Do not place the package's `method-reference/` material in SharePoint with the expectation that it will act as a continuation of `instructions`.

1. Put the target-side source material in one SharePoint site or document library.
2. Clone the repository.
3. Create a deployment-only Agents Toolkit environment file.

```bash
python scripts/init_m365_env.py --locale en-US --env dev \
  --sharepoint-url "https://contoso.sharepoint.com/sites/csw"
```

The resulting `.env.dev` is local deployment configuration. Public builds do not read or copy it automatically, and GitHub Releases do not contain it.

4. Build the agent with the SharePoint URL injected **explicitly**. In Bash or a similar shell:

```bash
CSW_M365_SHAREPOINT_SITE_URL="https://contoso.sharepoint.com/sites/csw" \
  python scripts/build.py
```

In PowerShell:

```powershell
$env:CSW_M365_SHAREPOINT_SITE_URL = "https://contoso.sharepoint.com/sites/csw"
python scripts/build.py
Remove-Item Env:CSW_M365_SHAREPOINT_SITE_URL
```

If the locales use different sites, use `CSW_M365_SHAREPOINT_SITE_URL_ja_JP` and `CSW_M365_SHAREPOINT_SITE_URL_en_US` instead.

5. Immediately before running Agents Toolkit, explicitly stage the deployment-only environment into the generated project:

```bash
python scripts/stage_m365_env.py --locale en-US --env dev
```

6. Use `dist/en-US/microsoft-copilot/agent-project/`.

### 2. Review the deployment environment

`init_m365_env.py` writes `adapters/microsoft-copilot/en-US/env/.env.dev` with the developer name, website URL, privacy URL, terms URL, `M365_APP_ID`, and SharePoint URL. Edit it as needed before staging it.

This file is deployment-only. Do not commit it and do not feed it into the public GitHub Release path. Public package creation fails closed on actual `.env` files, non-example `.env.*`, `*.local`, `*.secret`, and symlinks.

### 3. Package and validate

```bash
cd dist/en-US/microsoft-copilot/agent-project
atk package --env dev
atk validate --env dev
```

Tenant-specific Agents Toolkit packages belong to this deployment flow. They are intentionally separate from the public `make package` release flow.

### 4. Test and publish

Use `atk provision --env dev` for personal testing. Move through staging before production. Production publication requires tenant permissions and administrator approval. For staging or production, generate and stage the corresponding `.env.staging` or `.env.prod` file.
