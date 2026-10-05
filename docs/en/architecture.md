# Architecture

## From value to execution

CSW re-reads essential structure through cultural perspectives and makes discoveries usable as questions, comparisons, or compositions. `src/<locale>/ROUTER.md` is the entry. Choose problem-set perspective analysis or framework-native discovery as the request requires; move between them when useful.

Conditional references cover perspective analysis, framework selection, discovery, attribution and transformation, framework dossiers, and records. Delegate affinity-diagramming synthesis and multi-round continuity to separate skills. Domain judgment comes from caller context or domain skills. An external yomiyasu may polish settled Japanese prose.

## Source and distribution

`src/ja-JP/` is the semantic canonical CSW source; `src/en-US/` has a parallel translated tree. `adapters/` contains platform settings and explanations. `scripts/build.py` generates distributions. Project-specific hypotheses, correspondences, and decision records remain in the caller's project.

```text
src/<locale>/ + adapters/
             |
             v
       scripts/build.py
             |
             +-- OpenAI Skill / Codex Plugin
             +-- Claude Code Plugin
             +-- ChatGPT GPT update pack
             +-- Microsoft 365 limited adapter
             +-- canonical document pack
```

OpenAI and Claude Code receive a short entry and conditional references. ChatGPT Knowledge has six groups: stance, perspectives and discovery, target return and connections, framework library, optional body framework, and records and reflection. Microsoft 365 receives self-contained instructions within 8,000 characters and separate human-readable references. No adapter embeds affinity-diagramming algorithms.

Sibling research realizations remain in `research/skill-prototypes/`. Rebuilding CSW does not mean public three-Skill release or independent English review.

## Translation and generated consistency

`i18n/translation-manifest.json` records the Japanese source hashes translated by English files. Updating Japanese alone fails synchronization checks. Build projection maps source references to distributed locations and checks closure and content consistency. Generate artifacts from canonical sources and adapters to prevent drift. The current design decision is documented in the Japanese [product design](../ja/maintainers/value-first-product-design.md).
