# Evidence Dossier — Affinity Synthesis

Status: research candidate

この文書は、`affinity-synthesis` が何を既存方法から受け継ぎ、何を生成AI向けに追加しているかを分けて記録する。方法の有効性を必要以上に主張しない。

## 1. What mechanism is being implemented

このrealizationの中心は次である。

1. predefined bucketsを先に置かず、材料側から意味単位を立てる。
2. cluster before namingで、まとまりが立ってから表札を作る。
3. カード化、表札化、上位統合を、材料から意味単位を立てる同じ核操作として扱う。
4. 束を関係構造へ配置し、そこから叙述する。
5. 変換後は元材料へ戻し、意味の欠落・発明・確度変化を点検する。
6. singleton、conflict、gap、unresolvedを消さず、次に再検査できる形で残す。
7. membership / relation / secondary resonance / layout を分離し、同じ構造をtext、machine-readable record、diagramへ投影できるようにする。

## 2. Historical and methodological lineage

### KJ法

株式会社川喜田研究所は、KJ法を川喜田二郎が創案した問題解決・発想のための技法と説明し、フィールドワークのデータを研究成果へ導くために生まれ、幅広い分野へ展開したと説明している。

Reference:
https://kj-kawakita.co.jp/about_kj-method/

本prototypeはKJ法の思想・技法から強く学ぶが、生成AI向け補正を含むため「KJ法の公式Agent Skill」「KJ法の完全再現」とは称さない。

### 親和図法 / Affinity Diagram Method

日本科学技術連盟は、親和図法を、混沌とした状態から収集した言語データを相互の親和性によって統合し、問題や構造を明らかにする方法として説明している。また新QC七つ道具の一つとして、主に言語データを図・表へ整理する方法群の中に位置づけている。

References:
https://www.juse.or.jp/faq_knowledge/glossary.html
https://www.juse.or.jp/faq_knowledge/faq/index.html

この語はKJ法系譜の一部を表すのに有用だが、本prototypeは図解後の叙述と戻し検査まで含むため、公開名を単に `affinity-diagramming` とはしない。

### 質的統合法

山浦晴男氏の質的統合法における単位化・精選・表札づくり・図解・叙述、および04理論の研究記録は、カード化と上位統合を別々の根幹技術へ分解しない設計を考える際の重要な参照系統である。

現段階では、04理論の詳細を原典本文から完全に実装仕様化したとは扱わない。名称や番号体系をSkillの必須手順へ固定しない。

### 核融合法

川喜田系の実践解説から、各材料の核を取り、元材料を一度伏せ、核から表札候補を立て、元材料へ戻して修正する操作を参照している。

この操作を「元材料を伏せれば忠実性が自動的に上がる」ものとは扱わない。生成AIでは、伏せた部分をモデルの流暢な語彙が埋める危険があるため、戻し検査を対として実装する。

## 3. External Agent Skills reviewed

### `think-affinity-mapping`

Source:
https://github.com/product-on-purpose/thinking-framework-skills/tree/main/skills/think-affinity-mapping

Useful mechanisms / packaging:

- cluster before naming
- explicit outlier preservation
- source-item traceability
- clear `When to Use / When NOT to Use`
- output artifact contract
- quality checklist
- evidence dossier separated from runtime instructions
- explicit caveat that human-practice evidence is transferred to AI use
- template / example / evidence / eval separation

Not adopted as-is:

- stopping solely because item count is small
- assuming discrete comparable atomic items before grouping
- making theme size / weight standard output
- treating clustered theme map as the full final artifact

### `synthesis-frameworks`

Source:
https://github.com/slgoodrich/agents/tree/main/plugins/ai-pm-copilot/skills/synthesis-frameworks

Useful mechanisms / packaging:

- progressive references for detailed techniques
- explicit warning against confirmation bias
- explicit instruction to seek disconfirming evidence
- contradiction should not be ignored
- quotes must be real and traceable; fabricated quotes are prohibited
- operational troubleshooting examples

Not adopted as-is:

- atomic extraction as a universal first step
- fixed coding/theme-count ranges
- frequency as a default proxy for importance
- automatic progression from synthesis to actionable recommendation
- product-research-specific prioritization and impact/effort scoring

### `Research Synthesis` style skills

Reviewed example:
https://github.com/SkillMedev/skills/blob/main/skills/research-synthesis/SKILL.md

Useful representation observation:

- cluster output is written as `Theme: "<insight sentence>"`, not merely a noun category;
- tension / disagreement / gap sections are explicit rather than hidden inside a polished summary;
- the output schema is readable without a dedicated UI.

This supports representing a KJ-like label as a meaning-bearing sentence rather than a taxonomy key.

Not adopted as-is:

- mandatory atomic-note extraction;
- topic tagging before grouping;
- automatic `so what / now what` recommendation progression.

### Concept-map style skills

Reviewed example:
https://github.com/bajpainaman/solve/blob/main/frameworks/concept-map.md

Useful representation / packaging observations:

- Markdown report and raw Mermaid `.mmd` are emitted as separate artifacts;
- node inventory and edge inventory tables make the graph auditable without reading the rendered figure;
- edges carry visible labels rather than generic unlabeled lines.

Not adopted as-is:

- controlled edge vocabulary as the only legal semantic grammar;
- forcing every node into exactly one cluster;
- cluster-count and graph-density targets;
- assuming that a relation map is best modeled as a concept graph before affinity integration has stabilized.

Local consequence:

- keep an **edge inventory**, but make the relation `predicate` open natural language;
- represent direction separately from relation meaning;
- do not infer `causes` merely because an arrow is directed.

### Mermaid diagram skills

Reviewed example:
https://github.com/mgranberry/mermaid-diagram-skill

Useful mechanisms / packaging:

- diagram source is kept as `.mmd` or fenced Mermaid rather than only an image;
- diagram type should follow the conceptual structure rather than decorating text;
- large diagrams should be split into views rather than forced into one unreadable canvas;
- render-and-validate loop checks both syntax and resulting layout.

Critical limitation for KJ-like spatial diagrams:

- Mermaid uses automatic layout and does not preserve arbitrary pixel positioning.

Local consequence:

- use Mermaid as a **topology projection**, not as the sole authority for A-type spatial arrangement when proximity / void / peripheral placement itself matters;
- run a projection-integrity check so automatic layout does not become new analysis.

### Excalidraw-style diagram skills

Reviewed example:
https://github.com/diegosouzapw/awesome-omni-skills/blob/main/skills/excalidraw-studio/SKILL.md

Useful representation observation:

- `.excalidraw` is JSON and stores explicit element coordinates and bindings;
- this makes it suitable as one possible projection when free spatial placement matters.

Not adopted as the canonical format:

- Excalidraw element schema, styling and coordinate conventions are renderer-specific;
- method semantics should not depend on one canvas product.

Local consequence:

- store optional normalized positions or layout hints in the interchange layer when spatial placement itself must survive;
- allow Excalidraw / SVG / canvas as render targets without making them method authority.

### Interview synthesis variants

Useful observations:

- multiple quotes from one participant are not multiple independent data points
- participant/source identity should remain traceable for audit
- outliers should not be deleted simply because they fail frequency thresholds

These ideas support the local derivation/double-counting safeguards, but participant-count rules are not generalized into a universal scoring system.

## 4. What is inherited vs AI-specific

### Strongly inherited from existing human methods

- bottom-up integration rather than predefined categorization
- grouping before naming
- labels as expressions of group meaning rather than generic category names
- preserving ungrouped material
- externalizing structure in a diagram
- deriving prose from structured arrangement
- returning from an integrated representation to source material

### AI-specific or AI-strengthened realization choices

- explicit `source provenance != discovery route`
- derivation lineage to prevent false independent repetition
- generated-language audits for invented causality, interior state, generalization, polarity, certainty changes, and dropped agency
- explicit map ↔ narrative delta audit
- preserving inexplicable discomfort as a residual without forcing a hypothesis
- `primary placement / secondary resonance` without duplicating a card as independent support
- separating membership / explicit relation / secondary resonance / layout in the representation grammar
- relation predicates kept as natural-language meaning rather than a mandatory closed edge taxonomy
- machine-readable `affinity-map` interchange candidate
- diagram projection integrity checks
- Mermaid topology projection separated from free-position spatial projection
- separation of Method Definition from Agent Skill realization and from Representation Grammar
- explicit delegation boundary to narrower installed skills
- machine-usable negative eval cases

These additions should not be retroactively attributed to original KJ or affinity-diagram practice unless a primary source independently supports them.

## 5. Evidence limits

Affinity mapping and KJ-family methods have substantial practitioner history, but the existence of long practice does not prove that an AI-produced synthesis is objectively more accurate, less biased, or better for decisions.

Direct evidence for this exact AI realization is currently limited. Evaluation should therefore focus on inspectable preservation properties rather than broad claims of superiority:

- source fidelity
- preservation of epistemic seams
- avoidance of overfragmentation and overcompression
- absence of fabricated evidence or quotations
- explicit derivation lineage
- preservation of singleton/conflict/residual
- ability to round-trip from synthesis to source
- consistency between relational map and narrative
- membership / relation / resonance separation
- diagram projection fidelity
- no semantic inference from renderer-created proximity

## 6. Agent Skill packaging basis

The Agent Skills specification defines a Skill as a directory containing `SKILL.md`, with optional `references/`, scripts and assets, and recommends progressive disclosure so detailed resources are loaded only when needed.

Reference:
https://agentskills.io/specification

The prototype follows that pattern by keeping the activation contract and runtime procedure in `SKILL.md`, while moving method definition, representation grammar, output template, machine-readable schema, evidence discussion, examples, and eval cases into separate files.

## 7. Current evidence posture

Working evidence posture: **practitioner-derived method + AI-specific safeguards under evaluation**.

Do not claim:

- that `affinity-synthesis` is the official KJ method;
- that it reproduces every KJ procedure;
- that it is empirically superior to affinity mapping, thematic analysis, expert reading, or another synthesis method;
- that outputs are unbiased or objectively true;
- that repeated cards imply independent corroboration without lineage inspection;
- that a rendered diagram is more authoritative than the semantic record it projects.

## 8. Promotion requirements

Before this prototype becomes a public independent Skill:

1. run the local eval cases across at least two capable model realizations or prompt variants;
2. compare against current CSW `integration.md` on real, nontrivial tasks;
3. compare against an installed/public Affinity Mapping Skill on tasks inside and outside the narrower affinity-mapping boundary;
4. test the representation grammar on both small and 100+ card cases;
5. validate at least one Mermaid topology projection and one free-position spatial projection against the same semantic record;
6. verify that splitting Layer 1 from iterative inquiry does not lose useful round handoff information;
7. re-check naming collisions and trademark presentation;
8. verify primary-source attribution for public lineage claims;
9. validate the directory with the current Agent Skills reference validator where practical.
