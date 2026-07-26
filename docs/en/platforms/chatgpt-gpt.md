# Create a custom GPT

Custom GPTs are created and edited in the ChatGPT web interface.

## Build the update pack

```bash
python scripts/build.py
```

Use `dist/en-US/chatgpt-gpt/` for English or `dist/ja-JP/chatgpt-gpt/` for Japanese.

## Create

1. Open GPT creation in ChatGPT.
2. Enter the localized name and description.
3. Paste `instructions.md` into Instructions.
4. Upload all files under `knowledge/`.
5. Add the examples from `conversation-starters.md`.
6. Test both activation and non-activation cases in Preview.
7. Save and choose the sharing scope.

## Update

Replace Instructions, remove old Knowledge files, upload the new files, and follow `deploy-checklist.md`.

Create separate GPTs per locale at first. Mixing two Knowledge languages in one GPT can make retrieval terminology and response language less stable.
