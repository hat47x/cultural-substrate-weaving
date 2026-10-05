# Greco-Roman method-of-loci candidate profile

Status: profile-ready / research-only

## Identity

- names: method of loci / loci and imagines / artificial memory of places and images / Greco-Roman art of memory
- current scope: the place-and-image mnemonic technique attested in Roman rhetorical sources, especially *Rhetorica ad Herennium* Book III and Quintilian *Institutio Oratoria* XI.2, with later transmission treated only as context
- intended CSW use: separate a stable ordered retrieval scaffold from replaceable content, traverse the scaffold in a fixed order, and localize omissions or swaps without turning spatial position into target truth
- not intended use: a universal theory of memory, a claim that spatial placement creates semantic relations, or a replacement for source-of-truth records and checklists

## Source basis

### Primary rhetorical source — Rhetorica ad Herennium, Book III

https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Rhetorica_ad_Herennium/3%2A.html

The surviving Latin treatment distinguishes stable backgrounds or places from images representing what is to be remembered. It compares backgrounds to writing surfaces and images to letters, recommends a durable ordered set of distinguishable places, and allows the images to be replaced while the places remain available for reuse.

For CSW, the relevant structure is the separation of a persistent positional scaffold from variable bound content. The source's claims about mnemonic effectiveness remain historical technique claims, not target-side evidence.

### Primary rhetorical source — Quintilian, Institutio Oratoria XI.2

https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A2007.01.0068%3Abook%3D11%3Achapter%3D2

Quintilian describes selecting a spacious and differentiated place, fixing its parts in memory, assigning signs or images to successive locations, and later traversing the locations in order to retrieve what was placed there. He also explicitly limits the technique: it can help with ordered items, but may burden continuous verbal material.

This limitation matters to CSW. A candidate operation should not be forced onto targets whose structure is not meaningfully ordered or whose source material is already easier to inspect directly.

### Scholarly reference — Janet Coleman, Ancient and Medieval Memories

https://www.cambridge.org/core/books/abs/ancient-and-medieval-memories/cicero/C93AC479FC8B42D4AFAC4E4C17F53F71

Coleman situates the loci-and-images technique in the Roman rhetorical tradition and discusses Cicero, *Ad Herennium*, and Quintilian as major witnesses to its transmission. This supports a historically bounded Greco-Roman rhetorical scope rather than treating "memory palace" as a timeless universal method.

### Scholarly reference — Kimberley Skelton, The Physicality of Early Modern Memory Spaces

https://www.journals.uchicago.edu/doi/10.1086/731965

Skelton describes the long connection between imagined movement through built spaces and the organisation of knowledge, while also showing that later memory-space practices changed over time. CSW therefore does not collapse antique, medieval, and early-modern arts of memory into one invariant technique.

## Structural core

The useful CSW structure is **stable ordered loci + replaceable bound content + deliberate traversal**.

A minimal structural pass is:

1. define a stable sequence of distinguishable positions;
2. bind one target item or cue to each relevant position;
3. keep the positional scaffold distinct from the bound content;
4. traverse positions in a known order when reconstructing the target;
5. use a position with missing, duplicated, or misplaced content as a localization cue;
6. allow the content to be replaced without silently changing the scaffold;
7. return every discovered omission or order claim to the actual target record.

The historical mnemonic image is not itself required after de-binding. What must survive is the inspectable scaffold/content distinction and ordered traversal.

## Candidate operations

### stable-scaffold-variable-content-separation

Separate the durable indexing structure from the content currently attached to it.

### locus-binding

Bind one inspectable target item or cue to one stable position without claiming that the position explains the item.

### ordered-traversal-reconstruction

Walk the positions in a fixed sequence to reconstruct or review an ordered target.

### cue-to-content-reconstruction

Use a sparse cue at one position to reopen the fuller target-side item that the cue points to.

### sequence-position-localization

When an item is omitted, duplicated, or moved, identify the local position at which the expected sequence stops matching the target.

### scaffold-reuse-rebinding

Reuse the same stable index for a later version while replacing the bound content explicitly rather than confusing an old image with a current item.

## Useful outputs

- stable checkpoint sequence;
- position-to-target-item binding table;
- missing-position question;
- duplicated or swapped-position question;
- scaffold/content separation note;
- old-binding vs current-binding diff;
- target-side source reference for every reconstructed item;
- "the sequence breaks between L6 and L7" review cue.

## Target-return questions

- What target-side order, if any, justifies using an ordered scaffold?
- Which part is stable index and which part is replaceable content?
- If a position is empty, is the target actually missing an item or is the scaffold wrong?
- Does changing the spatial position change target meaning, or only retrieval order?
- Can every reconstructed item be reopened from the source-of-truth material?
- Would an ordinary numbered checklist expose the same omission with less cognitive overhead?
- Is a vivid mnemonic image adding retrieval value, or merely adding framework-specific decoration?
- If the loci vocabulary is removed, does a useful stable-index / variable-content / ordered-traversal distinction remain?

## Distinction from nearby CSW frameworks

- **Vedic recitation pathas** preserve ordered verbal material by exposing multiple recitation forms and adjacency relations. Method of loci instead places variable cues or items into a separately learned positional scaffold.
- **Inka khipu record structure** preserves information in a material hierarchical and positional record. Method of loci is a mnemonic indexing technique; its locations are not themselves the target record.
- **Marshallese wave navigation** updates a route through live environmental cues and disturbances. Method of loci uses a deliberately stable retrieval sequence rather than continuously returning to a changing environment.
- **Tibetan Buddhist mandala** uses lineage-specific spatial organisation and traversal with religious meaning. Method of loci does not make the mnemonic location a cosmological or ritual role.
- **ordinary checklist / numbered outline** may perform most of the de-bound target-side job more simply. This is the most important non-cultural baseline to test before runtime adoption.

## Historical / interpretive boundary

- *Rhetorica ad Herennium* is anonymous; its traditional attribution to Cicero should not be repeated as current authorship.
- The Simonides story in the rhetorical tradition is an origin narrative, not proof that one historical person invented a single fixed technique.
- Roman rhetorical descriptions, later medieval arts of memory, Renaissance memory systems, and contemporary "memory palace" practice are related but not identical.
- The places may be real or imagined. CSW should not turn a historically mnemonic space into a target-domain ontology.
- Source claims about remembering more effectively do not establish that the de-bound operation improves LLM output, software review, or human decision quality.

## What not to import by default

- the claim that a vivid or grotesque image is intrinsically better for every user or task;
- an invented spatial relation as if it were a target-side semantic relation;
- the assumption that every target has one correct linear order;
- the assumption that remembered content is correct because it was easy to retrieve;
- a memory scaffold as a substitute for records, logs, tests, backups, or version control;
- later "memory palace" conventions as if all were present in the ancient sources;
- the claim that a shared locus means two items are causally or conceptually related.

## De-binding route

Before returning a loci-based pass to the target:

1. replace historical "places" with explicit stable checkpoint IDs when physical or imagined space adds no value;
2. keep bound cues separate from the source-of-truth target items;
3. state the target-side reason for any ordering;
4. traverse the checkpoint sequence and record only concrete omissions, duplications, swaps, or unresolved bindings;
5. reopen every cue against the target material before treating it as supported;
6. compare the result with a plain numbered checklist or outline;
7. discard the framework if the plain baseline exposes the same useful differences with lower overhead.

## Runtime decision

Do not adopt into runtime for general CSW analysis.

The direct same-target comparison against an ordinary numbered checklist resolves the strongest counter-hypothesis against promotion. On the migration-plan review target, the checklist reproduces every target-relevant de-bound operation:

- stable scaffold vs replaceable binding;
- ordered traversal;
- omission / duplicate / swap localization;
- explicit rebinding after revision;
- return to source-of-truth material.

It also produces the same L4 restore-rehearsal and L12 post-rollback-verification questions with a simpler representation.

The method-specific residue is the human mnemonic use of places, imagery, and learned spatial traversal. That may be relevant when the target itself concerns human recall or rehearsal, but it is not a distinct generative operation for the current document-grounded AI review use.

Accordingly, the candidate remains a sourced research reference rather than a runtime-queue gap. Reconsider it only for a memory-specific target with a new justification; cultural distinctness alone is not sufficient.

Comparisons and worked examples:

- `research/framework-candidates/worked-examples/greco-roman-method-of-loci.md`
- `research/framework-candidates/worked-examples/greco-roman-method-of-loci-negative.md`
- `research/framework-candidates/comparisons/method-of-loci-vs-sequence-record-route.md`
- `research/framework-candidates/comparisons/method-of-loci-vs-numbered-checklist.md`
