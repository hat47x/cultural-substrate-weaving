# Create a Microsoft 365 Copilot agent

The repository generates localized declarative-agent material for Microsoft 365 Copilot, in Japanese and English. There are two ways to install it: a GUI-only route through Agent Builder, or a route through the Agents Toolkit CLI. If you're unsure which to use, use Agent Builder.

The method relies on web search in some cases for fact-checking and gathering context. Confirm that web search grounding is allowed for your tenant.

## Get the package

Download `cultural-substrate-weaving-m365-copilot-en-US-vX.Y.Z.zip` (or `-ja-JP-` for Japanese) from [GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases) and extract it. It contains `instructions.txt`, `knowledge/` (the reference modules as Markdown files), and `agent-project/` for the Agents Toolkit CLI.

## Method A: Agent Builder (GUI only, recommended)

If you have a Microsoft 365 Copilot license, you can create the agent directly with no CLI or code editing. You don't need `agent-project/`, Node.js, or Visual Studio Code.

1. Open Microsoft 365 Copilot at microsoft365.com/chat, office.com/chat, or in Teams, and select **New agent**.
2. Select **Skip to configure** to open the **Configure** tab directly (instead of the natural-language auto-generation flow).
3. Fill in **Name** and **Description** (30 and 1,000 characters respectively).
4. Paste the contents of the extracted `instructions.txt` into **Instructions** as-is. It's already validated to stay within the 8,000-character limit at build time.
5. Under **Knowledge**, drag and drop each file under `knowledge/`, or use the upload arrow icon. No SharePoint site is required (up to 20 knowledge sources).
6. Test both activation and non-activation examples on the **Try it** tab.
7. After creating the agent, use the **Share** button to share it directly with specific people or groups. To make it available org-wide, use the **…** menu → **Submit to your org catalog**; an admin reviews and publishes it to the organization's Agent Store.

## Method B: Agents Toolkit CLI (advanced / org-managed deployment)

Use this if you need something Agent Builder can't do: AppSource distribution, tenant-wide managed deployment, or grounding via a SharePoint site.

### Requirements

- Visual Studio Code with Microsoft 365 Agents Toolkit, or the Agents Toolkit CLI.
- For CLI use: `npm install -g @microsoft/m365agentstoolkit-cli`.

### 1. Add SharePoint knowledge (effectively required)

The declarative agent's `instructions` field only carries the activation check, minimum execution steps, and the judgment axes — nothing more. The 11 detailed reference modules that back actual judgment (activation criteria, the four viewpoints and five constraints, iteration, scope and facts, system selection, transformation, generation and validation, character and taiheki, output and collaboration, creative patterns, governance and records, final evaluation) exist only under `knowledge/`, and an agent built this way has no way to read them unless they're grounded via SharePoint. Without this step, the agent can only handle the shallow "obviously not applicable / narrow scope" cases — most of the method simply doesn't work. Don't use the `agent-project/` from the package as-is; rebuild it with the steps below first.

1. Upload the files under `knowledge/` to one SharePoint site or document library.
2. Clone the repository.
3. Run:

```bash
python scripts/init_m365_env.py --locale en-US --env dev \
  --sharepoint-url "https://contoso.sharepoint.com/sites/csw"
python scripts/build.py
```

4. Use `dist/en-US/microsoft-copilot/agent-project/` instead of the one in the package.

### 2. Fill in the environment file

Copy `agent-project/env/.env.dev.example` to `agent-project/env/.env.dev` and fill in the developer name, website URL, privacy policy URL, terms URL, and a `M365_APP_ID` (any GUID). These are substituted into the manifest when you run `atk package`.

### 3. Package and validate

```bash
cd agent-project
atk package --env dev
atk validate --env dev
```

### 4. Test and publish

Use `atk provision --env dev` for personal testing. Move through staging before production. Production publication requires tenant permissions and administrator approval.
