# Jingluo route-network candidate profile

Status: profile-ready / research-only / medical-tradition-sensitive

## Identity

- names: Jingluo / 經絡 / 经络 / meridian and collateral system
- current scope: classical and standardized route-network distinctions in Chinese medicine
- intended CSW use: main-route / collateral-route separation, branching, reconvergence, bypass, and route discontinuity
- not intended use: diagnosis, treatment, acupuncture efficacy, biomedical anatomy, or qi physiology claims

## Source basis

### Classical text layer

Chinese Text Project, 《黃帝內經・靈樞經・經脈》

https://ctext.org/huangdi-neijing/jing-mai/zh

The classical text distinguishes 經脈 and 絡脈 and describes routes, branches, connections, and divergence. CSW uses the Chinese text and edition/facsimile metadata as a historical source layer.

The modern English translation displayed by Chinese Text Project is not treated as an authoritative translation for this dossier.

### Institutional terminology layer

World Health Organization, *WHO international standard terminologies on traditional Chinese medicine* (2022)

https://www.who.int/publications-detail-redirect/9789240042322

WHO Standard Acupuncture Nomenclature, Part 2 (1991)

https://iris.who.int/bitstream/handle/10665/207637/Standard_acupuncture_nomenclature_1991_partII_eng.pdf?sequence=1

The nomenclature material distinguishes Jing / Luo / Jingluo as meridian / collateral / meridian-and-collateral terminology. CSW uses these sources to track standardized vocabulary, not to prove biomedical structures.

### Categorial representation layer

ISO/TS 16843-4:2017, *Health informatics — Categorial structures for representation of acupuncture — Part 4: Meridian and collateral channels*

https://www.iso.org/standard/68587.html

This confirms that meridian/collateral concepts have a formalized subject-field representation in health informatics. That fact is not anatomical evidence.

### Boundary literature

“A 4D systemic view on meridian essence: Substantial, functional, chronological and cultural attributes”

https://pubmed.ncbi.nlm.nih.gov/34896049/

“Historical Review about Research on ‘Bonghan System’ in China”

https://pmc.ncbi.nlm.nih.gov/articles/PMC3687598/

These sources are used to keep traditional structure, modern hypotheses, and anatomical claims separate. In particular, CSW does not identify Jingluo with a proven modern anatomical substrate.

## Structural core

The de-bound structural core retained by CSW is deliberately small.

### Main route vs collateral route

A network may contain differentiated route classes rather than one undifferentiated set of edges.

### Branch / divergence / reconvergence

A route can split, connect into another route, or rejoin a larger path.

### Route continuity

The path itself can be inspected independently of the nodes it connects.

### Route-before-node perspective

A system can be read by asking “what path carries or connects this?” before asking “what are the important nodes?”

### Main-path / side-path asymmetry

A collateral path is not automatically a duplicate main path. It may expose local, secondary, bypass, or connecting structure that a main-route-only model suppresses.

## Candidate operations

### main-vs-collateral-pass

Separate principal paths from secondary or connecting paths without treating the latter as noise.

### route-before-node-reframe

Re-represent a target around paths, handoffs, and continuity before optimizing individual nodes.

### branching-path-probe

Ask where one route splits into alternatives and whether those branches later reconverge.

### alternate-path / bypass probe

Look for paths that become relevant only under exceptional conditions or when the main route fails.

### route-discontinuity check

Find where an otherwise connected process or network loses continuity.

### cross-route connection probe

Ask whether two apparently separate routes are connected by a collateral path that changes the effective topology.

## Target-return questions

- Which route is principal, and which routes are collateral or connecting?
- Where does the route actually branch?
- Which branches reconverge, and which remain separate?
- Is there a bypass or exception path that becomes visible only when the main route fails?
- Are important failures located at nodes, or at the handoff between them?
- Is a “secondary” route carrying a function that the main route cannot replace?
- If Jingluo vocabulary is removed, do route class, branch, reconvergence, bypass, and continuity still describe observable target-side structure?
- What target-side records would falsify the proposed route map?

## Worked non-medical example

For a document-publication process:

- draft → review → approval → publish is the main route;
- security review, legal review, and exception handling may branch from the main route;
- some side routes reconverge before approval;
- emergency publication may bypass part of the normal route;
- a missing handoff can break route continuity even if every individual participant is functioning.

The useful output is a route map and discontinuity question.

CSW must not say that any workflow node “corresponds” to a meridian, organ, acupoint, qi state, or treatment concept.

## Distinction from nearby frameworks

### Jingluo vs dependent origination

Dependent origination asks which conditions make an outcome arise or cease.

Jingluo route-network asks which routes, branches, connections, and discontinuities connect parts of the target.

A path can exist without being a causal condition chain, and a causal condition can matter without being part of one route.

### Jingluo vs Huayan

Huayan asks how part/whole identity and perspective are constituted through relations.

Jingluo asks how differentiated routes connect, branch, bypass, and reconverge.

### Jingluo vs generic graph inspection

Generic graph language can represent nodes and edges, but the candidate is useful only if it preserves operations that are easy to omit in a flat graph:

- route classes;
- main vs collateral asymmetry;
- path continuity;
- branch / reconvergence;
- bypass structure.

If these distinctions produce no additional target-side question, Jingluo should not be selected merely for cultural variety.

## Medical and epistemic boundaries

- Do not infer a modern anatomical structure from the traditional route model.
- Do not convert qi or blood circulation in traditional descriptions into modern physiological flow claims.
- Do not use this dossier for diagnosis, treatment, acupoint selection, or efficacy claims.
- Do not treat WHO or ISO terminology standards as biomedical validation.
- Do not claim the Huangdi Neijing is one historically uniform layer.
- Do not infer that a target “really has meridians.” The framework generates route questions only.
- Do not import organ, channel, point, yin-yang, or disease correspondences into unrelated targets.

## De-binding route

1. remove medical and physiological vocabulary;
2. restate the candidate as route classes, branches, connections, bypasses, reconvergence, and discontinuities;
3. mark which topology was framework-generated;
4. return every route to target-side events, links, records, or handoffs;
5. preserve missing, contested, or cyclic paths instead of repairing them automatically;
6. discard the framework if the target is better represented by an undifferentiated graph or causal chain.

## Adoption gap

The source packet is now sufficient for research profile use.

Before runtime adoption:

- strengthen the textual-history boundary among Huangdi Neijing layers and later commentarial traditions;
- document Jing / Luo / Jingluo translation history more explicitly;
- add a second non-medical target-return example with a different topology;
- verify that route-class operations remain distinct from generic graph inspection in actual CSW use;
- keep all medical efficacy and anatomy questions outside the runtime dossier.
