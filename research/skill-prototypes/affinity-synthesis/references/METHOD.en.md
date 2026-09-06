# Affinity Synthesis Method Definition

Status: research candidate, English translation draft

## Purpose

Raise meaning units and relations from heterogeneous, uneven, and tension-bearing material without imposing the analyst's classification system first, then integrate the whole while repeatedly returning transformations to the source.

The goal is not a clean theme list by itself. The method should preserve a structure supportable by the material together with remaining singletons, conflicts, gaps, and unresolved material in a form that can be rechecked later.

## Lineage and scope

This method learns from KJ Method, affinity-diagram, and qualitative-integration lineages. The Agent Skill realization also contains AI-era safeguards, so it is not positioned as an official implementation or complete reproduction of those methods. KJ Method is a registered trademark of Kawakita Research Institute.

Keep historical lineage distinct from current implementation corrections.

### Core inherited from the lineages

- Do not force material into a priori categories; let structure arise from the material.
- A group label should voice what the group is saying, not merely name a category.
- Do not force isolated material into an existing group.
- Externalize relations in a map/diagram and narrate from that structure.
- Return synthesis to the source material for checking.

### AI-era corrections

- Protect meaning-bearing units and epistemic seams at the same time.
- Separate source provenance from discovery route.
- Preserve derivation lineage to prevent false repetition.
- Check common fluent additions such as causality, inner state, generalization, evaluation direction, and confidence shifts.
- Cross-check diagram and narrative in both directions.
- Audit post-transformation meaning as inherited / emergent / residual rather than rewriting emergent meaning backward into the source.
- Keep membership / explicit relation / secondary resonance / layout distinct.
- Preserve externally inspectable artifacts, provenance, and residuals rather than private chain-of-thought.

## Applicability

Good fits include:

- qualitative synthesis;
- open-ended research;
- heterogeneous document or note synthesis;
- conflicting observations or accounts;
- material-led structure discovery;
- creative or analytical work where source texture and residual difference matter.

Poor fits include:

- fixed-taxonomy coding;
- simple summarization;
- deterministic classification;
- tasks needing only bottom-up theme clustering;
- tasks whose primary need is recommendation ranking or decision authority.

## Inputs

Allowed input concepts remain broad:

- source material;
- observation;
- quote or reported statement;
- note;
- document fragment;
- prior meaning-bearing card;
- explicit hypothesis or unresolved item, provided its status remains visible.

The method does not require JSON, Markdown, a canvas, a database, or another specific medium.

## Outputs

- meaning-bearing card;
- group / bundle;
- label / higher-order meaning unit;
- relational structure;
- narrative synthesis;
- singleton;
- tension / conflict;
- unresolved item;
- gap-as-question;
- provenance / derivation references;
- cross-check result.

A `gap` may be an absence that becomes visible in the arrangement and is worth checking next. It is not automatically a factual claim that a missing element exists.

## Invariants

### I1. Material-led structure

Meaning distance arises from content. Source, speaker identity, faction, card type, metadata, or a prior taxonomy must not be the initial grouping geometry.

### I2. Meaning-bearing unit

Do not mechanically decompose cards into the smallest possible fact fragment. Preserve one experience, judgment, or causal movement as a unit when splitting would destroy its meaning.

### I3. Epistemic seam

Do not silently erase boundaries such as observation / interpretation, confirmed / inferred, or speaker statement / third-party interpretation.

When I2 and I3 pull in different directions, seek wording or a split that protects both semantic unity and evidence state.

### I4. Same integration kernel across granularity

Carding, labeling, higher-order labeling, refinement, and semantic-overlap reduction use the same underlying operation at different scales:

1. inspect the boundary;
2. identify what cannot be lost without changing the meaning;
3. form an integrated unit only when one meaning can genuinely arise from the materials;
4. return to the source and inspect invention, omission, and confidence change.

### I5. Cluster before naming

Do not place theme names before a group has arisen.

### I6. Label is advocacy, not a class name

A label should carry a specific appeal that belongs to this group rather than escaping upward into a generic category. Portability to other groups is a warning sign, not an automatic invalidation rule.

### I7. Return to source and audit transformation

Every transformation must remain returnable to source material. If the return produces resistance, treat that resistance as something to repair or preserve as residual.

When useful, distinguish transformed meaning as:

- **inherited**: directly retained from input;
- **emergent**: newly raised through contact, grouping, placement, or narration;
- **residual**: difference, contradiction, temperature, unresolved material, or intentionally dropped detail not absorbed into the synthesis.

This is a post-transformation audit distinction, not an a priori input taxonomy.

### I8. Provenance is audit, not geometry

Preserve source provenance, discovery route, derivation, and collection context when needed for audit and restoration. Do not let them decide initial semantic distance.

### I9. No false independent repetition

Do not count a repost, repeated description of one event, or multiple descendants of one source artifact as independent corroboration.

### I10. Preserve singleton and conflict

Do not delete ungrouped material, opposition, or unexplained attention for the sake of completeness.

### I11. Diagram and narrative remain mutually checkable

Neither the map nor the prose is the sole authority. Narrative-only relations must return to the map/source; map relations omitted from prose must also be inspected.

### I12. Residual is not failure

Residuals, gaps, conflicts, and unresolved material may accurately mark the limit of what current material can say.

### I13. Membership, relation, resonance, and layout remain distinct

Representations must preserve a semantic distinction among:

- membership;
- explicit relation with a readable predicate;
- secondary resonance that does not add membership or independent support;
- visual layout.

Do not infer a semantic relation merely from visual proximity, and do not turn secondary resonance into duplicate membership or support.

### I14. Rendering is a projection, not the method authority

Mermaid, SVG, canvas, or another renderer is a projection of the semantic structure. Tool or layout constraints must not rewrite group membership, relation predicates, directions, uncertainty, or residuals.

If spatial position itself carries analytic meaning, retain positional information separately from topology-only automatic layouts.

## Frequent AI failure modes

- fluent paraphrase erases source-specific texture or temperature;
- conjunctions add causality absent from the source;
- actor or responsibility disappears;
- plausible inner state is invented;
- inference, hearsay, or hypothesis is promoted to fact;
- one vivid case becomes a general trend;
- derived cards are counted as independent voices;
- cluster size is treated as importance or truth;
- elegant labels hide weak group coherence;
- prose adds logic absent from the map;
- later insight is rewritten backward as if the original card had already contained it;
- one card is duplicated across groups and secondary resonance becomes multiple votes;
- automatic layout creates imagined semantic relations;
- visual neatness turns tentative relations into strong assertions.

## Relationship to external methods and skills

### Affinity Mapping / Affinity Diagramming

A shared core is bottom-up clustering without predefined buckets. This method additionally owns semantic-unit boundaries, epistemic seams, higher-order integration, relational structure, narrative, and source-return checks within one synthesis round.

If the task only needs theme clustering, a dedicated Affinity Mapping Skill may be delegated to unchanged.

### Concept Mapping

Concept Mapping can be useful downstream when the items are already conceptualized and explicit propositions are needed. It is not the default preprocessing step because early conversion into concept nodes can erase source texture.

### Diagram-generation skills

A diagram skill can render a projection from the semantic record. Its visual grammar does not outrank the synthesis grammar.

### Evidence / Inference auditing

A downstream evidence/inference audit can be useful after synthesis. The method does not require placing all source material into a closed claim taxonomy before grouping.

## Representation boundary

Concrete notation, interchange schema, and diagram projections belong to representation assets rather than the Method Definition.

The method does not own ID prefixes, JSON property names, Mermaid syntax, colors, shapes, or a particular canvas geometry. Representation can change while the method remains the same if I1-I14 continue to hold.

## Realization boundary

The Method Definition does not own a particular Agent Skill wording, model, prompt, tool, UI, card count, text length, or rendering surface.

A realization may be replaced by an existing external Skill if it satisfies these invariants and the relevant regression fixtures. The existence of a local realization is not itself a reason to preserve it.
