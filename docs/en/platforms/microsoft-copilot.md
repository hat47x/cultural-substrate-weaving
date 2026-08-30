# Create a Microsoft 365 Copilot agent

The repository generates localized declarative-agent material for Microsoft 365 Copilot in Japanese and English. There are two ways to install it: a GUI-only route through Agent Builder, or a route through the Agents Toolkit CLI. If you're unsure which to use, use Agent Builder.

Web search is not required when the task can be completed from supplied material alone, such as KJ integration over a closed source set. When a task needs current facts, external context, or additional source discovery, confirm that web-search grounding is permitted for your tenant.

## Get the package

Download `cultural-substrate-weaving-m365-copilot-en-US-vX.Y.Z.zip` (or `-ja-JP-` for Japanese) from [GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases) and extract it. It contains `instructions.txt`, `knowledge/` (the reference modules as Markdown files), and `agent-project/` for the Agents Toolkit CLI.

The standard GitHub Release package is **tenant-neutral**. It does not contain a tenant-specific SharePoint site URL or actual `.env` / `.env.*` files. Only safe `.example` templates are included under `agent-project/env/`. Tenant-specific values are injected explicitly when you prepare an organization deployment.

## Method A: Agent Builder (GUI only, recommended)

If you have a Microsoft 365 Copilot license, you can create the agent directly with no CLI or code editing. You don't need `agent-project/`, Node.js, or Visual Studio Code.

1. Open Microsoft 365 Copilot at microsoft365.com/chat, office.com/chat, or in Teams, and select **New agent**.
2. Select **Skip to configure** to open the **Configure** tab directly instead of the natural-language auto-generation flow.
3. Fill in **Name** and **Description** (30 and 1,000 characters respectively).
4. Paste the contents of the extracted `instructions.txt` into **Instructions** as-is. It is validated at build time to stay within the 8,000-character limit.
5. Under **Knowledge**, upload each file under `knowledge/`. Agent Builder doesn't accept Markdown (`.md`), so rename each file's extension to `.txt` before uploading; the contents are plain text, so renaming is enough. No SharePoint site is required for this route.
6. If the agent needs current facts or external information, enable **Search all websites** under **Knowledge**. It is not required when the agent should stay within supplied material.
7. Test both activation and non-activation examples on the **Try it** tab.
8. After creating the agent, use **Share** for direct sharing. For organization-wide availability, use **…** → **Submit to your org catalog** and follow your administrator's review process.

## Method B: Agents Toolkit CLI (advanced / org-managed deployment)

Use this route when you need AppSource distribution, tenant-wide managed deployment, SharePoint grounding, or another configuration that Agent Builder does not provide.

### Requirements

- Visual Studio Code with Microsoft 365 Agents Toolkit, or the Agents Toolkit CLI.
- For CLI use: `npm install -g @microsoft/m365agentstoolkit-cli`.

### 1. Add SharePoint knowledge

The declarative agent's `instructions` field carries only the activation decision, minimal procedure, and persistent judgment axes. Detailed cultural-framework application, KJ integration, the human/Taiheki special case, governance, and evaluation live under `knowledge/`; to use the full method through the CLI route, make those references available through SharePoint or another supported knowledge path.

1. Upload the files under `knowledge/` to one SharePoint site or document library.
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
