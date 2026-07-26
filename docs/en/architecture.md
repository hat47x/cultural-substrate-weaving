# Architecture

## Four layers

1. **Semantic canonical source:** `src/ja-JP/`.
2. **Translations:** structurally parallel trees under `src/<locale>/`.
3. **Adapters:** platform and locale templates under `adapters/`.
4. **Dynamic layer:** hypotheses, rejected mappings, and decision records created in each target project.

## Build flow

```text
src/<locale>/ + adapters/<locale>/
             |
             v
       scripts/build.py
             |
             +-- OpenAI Skill
             +-- Claude Code plugin
             +-- ChatGPT GPT update pack
             +-- Microsoft 365 Copilot agent
             +-- canonical document pack
```

Generation prevents platform copies from drifting. Translation hashes detect when the canonical Japanese source changed after a translation was produced.
