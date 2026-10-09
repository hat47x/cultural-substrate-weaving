# Hadith isnād / matn candidate profile

Status: profile-ready / research-only / religious-tradition-sensitive / no-runtime

## Identity

- names: hadith isnād / matn, إسناد / متن, ハディース伝承鎖と本文
- current scope: the structural distinction between report content and attributed transmission chain, plus modern scholarly caution about reconstructing transmission
- intended CSW use: provenance-chain externalization, branching/convergence comparison, content/provenance separation, and uncertainty localization
- not intended use: issuing religious authenticity judgments

## Source basis

### Scholarly overview

Oxford Bibliographies, Hadith

https://academic.oup.com/reference/62361/reference-article-abstract/554579067

Useful for the basic distinction between matn and isnād and for situating hadith inside a long historical transmission and compilation process.

### Scholarly overview of modern debates

Modern Hadith Studies: Continuing Debates and New Approaches — Introduction

https://academic.oup.com/edinburgh-scholarship-online/book/37555/chapter-abstract/331803753

Useful for defining matn / isnād while also showing why the history of hadith transmission cannot be reduced to one simple validation rule.

### Scholarly method reference

The Wiley Blackwell Concise Companion to the Hadith — Dating

https://onlinelibrary.wiley.com/doi/10.1002/9781118638477.ch6

Useful for isnād-cum-matn analysis: reconstructing and dating traditions by combining transmission lines with substantive textual variation.

### Historical-source criticism reference

Verifying Source Citations in the Hadith Literature

https://online.ucpress.edu/jmw/article/1/3/5/51002/Verifying-Source-Citations-in-the-Hadith

Useful because it explicitly warns against taking isnāds at face value and discusses errors, back-projections, and source-attribution problems.

## Structural core

A hadith report is commonly represented with two analytically distinct parts:

- **matn** — the substantive report;
- **isnād** — the attributed chain by which the report reached a collector/transmitter.

For CSW, the useful structure is not a religious authenticity label. It is the discipline of keeping **what is said** separate from **how that saying is attributed and transmitted**.

The second useful structure is multiplicity. A report may be encountered through more than one transmission path, and textual variants can be compared with those paths.

## Native operation candidates

### transmission-content separation

Externalize report content and transmission path as different objects.

Questions:

- What is the content independent of the chain?
- What claims are made only by the chain?
- Has source prestige leaked into the content claim?

### branch-and-convergence comparison

Place multiple chains side by side.

Questions:

- Where do they diverge?
- Where do they converge?
- Is a common node early, late, or reconstructed?

### attribution-path audit

Mark each handoff in the transmission claim.

Outputs:

- observed source link
- asserted link
- missing link
- uncertain identity
- later editorial attribution

### matn-variant comparison

Compare textual/content variants without assuming one chain is automatically superior.

Questions:

- Which content differences correlate with transmission branches?
- Which differences appear independent of chain structure?
- Is a later harmonization hiding earlier variation?

### provenance-content non-equivalence

Explicitly ask whether provenance evidence and content evidence support different claims.

A well-documented route does not by itself establish the truth of the transmitted proposition.

## What not to import by default

- religious authenticity grades as general-purpose truth scores;
- narrator evaluation as a universal person-reliability model;
- the existence of an isnād as proof that a report is historically true;
- one modern historical method as if it were identical to classical hadith criticism;
- the assumption that all Islamic traditions or schools apply one identical hadith method;
- simulated scholarly or religious authority.

## Historical / methodological caution

Classical hadith criticism and modern historical source criticism ask overlapping but non-identical questions.

The profile therefore preserves at least three layers:

1. report structure: matn + isnād;
2. tradition-internal methods of transmission and evaluation;
3. modern historical reconstruction using chain and text evidence.

CSW must not collapse these into one "reliability algorithm."

## Exploratory prompts

- What is the claim, and what is only the claim about transmission?
- How many independent-looking paths carry this material?
- Where do those paths actually share a source?
- Which content variants align with which paths?
- Which handoff is inferred rather than directly documented?
- Would the content claim remain equally strong if the source chain were removed?
- Would the provenance claim remain equally strong if the wording varied?

## De-binding

1. remove hadith-specific religious authority language unless provenance requires it;
2. represent the target as content objects plus transmission edges;
3. keep asserted, observed, and reconstructed edges distinct;
4. compare content variants separately from path variants;
5. return every factual claim to target-side evidence;
6. preserve unresolved chain gaps instead of silently filling them.

## Runtime requalification

### Positive target-return fixture

See:

- `research/framework-candidates/worked-examples/hadith-isnad-matn.md`

Three apparent confirmations of one policy claim turn out to descend from one meeting statement. The pass separates content variants from transmission paths and prevents three documents from becoming three independent origins.

### Non-activation fixture

See:

- `research/framework-candidates/worked-examples/hadith-isnad-matn-negative.md`

When the target already has immutable artifact IDs, derivation / quotation edges, explicit common-origin grouping, content diffs, and evidence state separate from provenance, hadith contact adds no target-side job.

### Capability-overlap comparison

See:

- `research/framework-candidates/comparisons/hadith-isnad-matn-vs-ordinary-provenance-and-csw-core.md`

W3C PROV can represent derivation, quotation, revision, agents, and provenance bundles. C2PA explicitly separates verifiable provenance from judgments about whether content is true or factual.

More importantly, CSW's always-on core already requires same-origin derivatives not to count as independent support and keeps discovery path separate from evidence-source independence.

These ordinary/core mechanisms reproduce all current de-bound runtime operations.

### Discovery-value comparison

See:

- `research/framework-candidates/comparisons/hadith-isnad-matn-discovery-value.md`

This is the decisive product-specific test.

Hadith has high intellectual relevance to CSW's provenance discipline, but the framework's most valuable de-bound lessons have already been promoted into the **pre-framework core**:

- same origin != independent support;
- provenance != proposition truth;
- discovery path != evidence source;
- asserted provenance edge != independently verified target support.

Because those safeguards run before framework selection, hadith contact does not open a distinct default-runtime cognitive job on the tested provenance target.

### Near-neighbor comparison

See:

- `research/framework-candidates/comparisons/hadith-isnad-matn-vs-vedic-recitation-pathas.md`

Hadith focuses on content/provenance separation and lineage topology. Vedic recitation pathas focus on ordered-sequence and boundary fidelity. The distinction is real, but framework-to-framework distinctness does not by itself justify runtime retention.

### Requalification result

The current evidence supports removing hadith isnād / matn from **general default runtime** while preserving it as a sourced research candidate. The mechanical runtime demotion is now complete.

This is not a judgment that the tradition is unimportant. The opposite is true: its structural distinction has had high product relevance because CSW itself needs strong provenance discipline.

The product reason for demotion is that the relevant cognitive work is now already performed by CSW core before any cultural-framework contact. Keeping the framework in the default selection portfolio would duplicate an always-on safeguard and add selection complexity without opening a new target-side question.

Preserve the research asset for:

- explicit hadith or Islamic intellectual-history work;
- comparative source criticism;
- educational explanation of lineage/content non-equivalence;
- future targets where a tradition-specific transmission operation survives beyond CSW core;
- intellectual provenance for CSW's own design history.

Do not generalize religious authenticity grades or narrator evaluation into generic trust scoring.
