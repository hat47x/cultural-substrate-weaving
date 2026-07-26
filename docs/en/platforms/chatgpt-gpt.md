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
