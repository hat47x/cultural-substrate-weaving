# Create a custom GPT

Custom GPTs are created and edited in the ChatGPT web interface.

## Get the update pack

Download `cultural-substrate-weaving-chatgpt-gpt-en-US-vX.Y.Z.zip` (or `-ja-JP-` for Japanese) from [GitHub Releases](https://github.com/hat47x/cultural-substrate-weaving/releases) and extract it. It contains `instructions.md`, `knowledge/`, `conversation-starters.md`, and `deploy-checklist.md`. No build step is required.

If you maintain the repository, `python scripts/build.py` generates the same content under `dist/<locale>/chatgpt-gpt/`. See [Development](../maintainers/development.md).

## Create

1. Open GPT creation in ChatGPT.
2. Enter the localized name and description.
3. Under Capabilities, enable Web Search. The method relies on search for fact-checking and gathering context, so leaving it off reduces judgment quality.
4. Paste `instructions.md` into Instructions.
5. Upload all files under `knowledge/`.
6. Add the examples from `conversation-starters.md`.
7. Test both activation and non-activation cases in Preview.
8. Save and choose the sharing scope.

## Update

Replace Instructions, remove old Knowledge files, upload the new files, and follow `deploy-checklist.md`.

Create separate GPTs per locale at first. Mixing two Knowledge languages in one GPT can make retrieval terminology and response language less stable.

## Alternative: upload it as a Skill (Business/Enterprise/Healthcare/Edu)

Separately from custom GPTs, you can also install this into ChatGPT's own Skills feature. This currently requires a ChatGPT Business, Enterprise, Healthcare, or Edu workspace — it isn't available on individual Free/Plus/Pro accounts. Workspace admins must also have the "Enable skills" and "Enable skill uploading" permissions turned on.

1. Download the `openai-skill-metered` or `openai-skill-interactive` ZIP from GitHub Releases (the same package used in [Use with Codex](codex.md); both are treated identically for ChatGPT).
2. In ChatGPT web, go to Plugins → Skills → **+** → **Upload from computer**, and upload that ZIP as-is.
3. ChatGPT scans the upload automatically. If it's marked "Needs Review" or "Blocked," review the content before proceeding.

Personal skills don't sync between desktop and web/mobile, so upload separately on each surface if you use both.
