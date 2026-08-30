# Create a custom GPT

Custom GPTs are created and edited in the ChatGPT web interface.

## Get the update pack

Download `cultural-substrate-weaving-chatgpt-gpt-en-US-vX.Y.Z.zip` (or `-ja-JP-` for Japanese) from [GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases) and extract it. It contains `instructions.md`, `knowledge/`, `conversation-starters.md`, and `deploy-checklist.md`. No build step is required.

If you maintain the repository, `python scripts/build.py` generates the same content under `dist/<locale>/chatgpt-gpt/`. See [Development](../maintainers/development.md).

## Create

1. Open GPT creation in ChatGPT.
2. Enter the localized name and description.
3. Enable Web Search under Capabilities when the intended work needs current facts, external context, or additional source discovery. It is not required for KJ integration or structural exploration over a closed set of supplied material. If search is unavailable, do not guess missing external facts.
4. Paste `instructions.md` into Instructions.
5. Upload all files under `knowledge/`.
6. Add the examples from `conversation-starters.md`.
7. Test both activation and non-activation cases in Preview.
8. Save and choose the sharing scope.

## Update

Replace Instructions, remove old Knowledge files, upload the new files, and follow `deploy-checklist.md`.

Create separate GPTs per locale at first. Mixing two Knowledge languages in one GPT can make retrieval terminology and response language less stable.

## Alternative: upload it as a Skill (eligible workspaces)

Separately from custom GPTs, you can upload the package through ChatGPT's Skills feature. Skills are currently available to eligible ChatGPT Business, Enterprise, Healthcare, and Edu users, subject to workspace settings, role, and product availability.

1. Download the `openai-skill-metered` or `openai-skill-interactive` ZIP from GitHub Releases (the same package used in [Use with Codex](codex.md)). Both can be uploaded as ChatGPT Skills.
2. In the ChatGPT sidebar, open **Plugins**, select the **Skills** tab in the Plugin Directory, then choose **Create** → **Upload from your computer** and upload the ZIP as-is.
3. ChatGPT scans the upload automatically. If it is marked **Needs Review** or **Blocked**, review the content before proceeding.

Skill availability and syncing can differ by product and workspace, so do not assume that a Skill installed in ChatGPT is automatically installed or synchronized in Codex.
