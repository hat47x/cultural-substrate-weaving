# Split Method Research Suite

Status: research-only

このディレクトリは、`cultural-substrate-weaving` から材料統合と複数roundの再開管理を分離する研究suiteである。

ここにある `affinity-synthesis` / `iterative-inquiry-synthesis` は、現時点では公開済みの独立Skillではない。

## 三層

```text
cultural-substrate-weaving
  cultural-framework exploration / attribution / target return

        ↓ material / framework-generated candidates

affinity-synthesis
  one-round material-led synthesis
  card / group / label / relation / narrative / source return

        ↓ delta / residual / stable semantic handles

iterative-inquiry-synthesis
  multi-round delta-based reopening
  question shift / append-only history / stop-restart boundary
```

### Layer 0 — Cultural Substrate Weaving

CSWは文化的・思想的・伝統的体系を一時的な認知場として開き、そこから得た問い・対比・対応候補を由来付きで対象へ戻す。

親和統合や一般的なmulti-round orchestrationの内部アルゴリズムを所有しない。

### Layer 1 — Affinity Synthesis

異種材料から、先験的taxonomyを置かずにmeaning-bearing unit、group、label、relation、narrativeを立ち上げ、元材料へ戻して検査する一回の統合Method。

KJ法・親和図法・質的統合法の系譜を参照するが、生成AI向け補正を含むため公式KJ法Skillや完全再現とは称しない。

### Layer 2 — Iterative Inquiry Synthesis

一回の統合結果を固定結論へせず、新材料が触れたartifactだけを必要に応じてreopenし、問い・残差・履歴・停止／再開条件をround間で保つMethod。

Layer 1のgrouping / labeling algorithmを再実装しない。

現在の中心境界は次である。

```text
preserve / carry forward
    !=
reopen now
    !=
continue another round
```

前roundから持ち越したsemantic handleやresidualは、identityやrestart可能性を保存するためのstateであり、それだけで再開・継続命令にはならない。

## Method Definitionとrealizationを分ける

```text
Method Definition
    != Agent Skill realization
    != package source descriptor
    != representation / renderer
    != evaluation fixture
    != application record
    != recommendation / decision
    != action execution
```

Method Definitionの不変条件を別realizationが満たせるなら、local Skill realizationは置換・縮小できる。

独自Skillを維持すること自体を目的にしない。

## Locale

### Japanese

- CSW: `src/ja-JP/` がsemantic canonical runtime
- Affinity Synthesis: `affinity-synthesis/SKILL.md` / `references/METHOD.md` がresearch canonical
- Iterative Inquiry Synthesis: `iterative-inquiry-synthesis/SKILL.md` / `references/METHOD.md` がresearch canonical

### English

- CSW thin runtime: `src/en-US/`
- Affinity Synthesis draft: `affinity-synthesis/SKILL.en.md` / `references/METHOD.en.md`
- Iterative Inquiry Synthesis draft: `iterative-inquiry-synthesis/SKILL.en.md` / `references/METHOD.en.md`

英語sibling realizationは `translated-draft`。runtime artifactと英語Method Definitionは存在するが、独立した人手査読済みとは扱わない。

Layer 2については、実際に英語MethodからI15が一時欠落したparity driftが見つかったため、現在はI1〜I16のinvariant surfaceを静的に照合するcheckをresearch gateへ追加している。このcheckは翻訳査読の代替ではない。

参照資料のlocale依存とruntime依存は [REFERENCE-CLASSIFICATION.md](REFERENCE-CLASSIFICATION.md) を参照する。

## Package境界

`runtime_entry` が存在することと、そのSkillをpackageへ組み立てるsource boundaryが分かっていることを分ける。

locale realizationごとに `package_source` を宣言する。

- `explicit_files`: sibling Skill。source rootからの相対構造を保つfile集合。
- `canonical_manifest`: CSW。既存 `src/manifest.json` とlocale rootを再利用する。

さらに、package sourceが宣言されているだけでは十分ではない。runtime entryが参照する `references/`、`evals/`、`evidence/` 等が `package_source.files` から抜けていないことをreference-closure validatorで確認する。

詳細は次を参照する。

- [P1 Locale Realization Audit](P1-LOCALE-REALIZATION-AUDIT-2026-09-07.md)
- [P2 Distribution Layout Plan](P2-DISTRIBUTION-LAYOUT-PLAN-2026-09-07.md)
- [P2 Package Source Descriptor Audit](P2-PACKAGE-SOURCE-DESCRIPTOR-2026-09-07.md)
- [P2 Skill Subtree Plan](P2-SKILL-SUBTREE-PLAN-2026-09-07.md)
- [P2 Skill Entry Transform](P2-SKILL-ENTRY-TRANSFORM-2026-09-07.md)
- [P3 Package Tree Preview](P3-PACKAGE-TREE-PREVIEW-2026-09-07.md)

`package_source` はresearch metadataの全量を意味しない。runtime packageへ必要なsource boundaryだけを表す。

特にLayer 2のexternal-loop comparison dossierはsuite manifest上の必須research evidenceとして追跡するが、Japanese / English runtime packageには含めない。

## Host adapter metadata

runtime/package treeの成熟度と、host固有metadataの成熟度も分ける。

`adapter-metadata-plan.json` は、少なくとも次を独立に追跡する。

- OpenAI Skill: Skill × locale × interactive/metered profile
- Claude plugin: locale bundle
- Codex plugin: locale bundle

現在はja-JP / en-USとも、

- CSW OpenAI metadata = `existing`
- Affinity / Iterative OpenAI metadata = `prototype`
- Claude/Codex三Skill bundle metadata = `prototype`

である。

したがって、両localeともresearch上はSkill treeとpackage-local host metadataを組み立てる最低条件がそろっている。ただし、prototype wordingがhost上で適切に見え、routingされることを実証したわけではない。

詳細は [P2 Adapter Metadata Plan](P2-ADAPTER-METADATA-PLAN-2026-09-07.md) を参照する。

## 二段のmaterializer

production builderへ直接進まず、repository外の一時領域だけを使う二段のprobeを置く。

### 1. Skill tree

`research/skill-prototypes/scripts/materialize_skill_tree.py`

対象:

- OpenAI Skill tree
- Claude shared `skills/` tree
- Codex shared `skills/` tree

この段階ではhost manifestを生成しない。

詳細は [P2 Research Skill-tree Materializer](P2-RESEARCH-SKILL-TREE-MATERIALIZER-2026-09-07.md) を参照する。

### 2. Host package shape

`research/skill-prototypes/scripts/materialize_host_package.py`

Skill treeを再利用し、package-local metadataだけを追加する。

- OpenAI: `<skill>/agents/openai.yaml`
- Claude: `.claude-plugin/plugin.json`
- Codex: `.codex-plugin/plugin.json`

marketplace、README、archive、release manifest、release assetは生成しない。

詳細は [P3 Research Host Package Materializer](P3-RESEARCH-HOST-PACKAGE-MATERIALIZER-2026-09-07.md) を参照する。

両materializerは、suite / package target / adapter metadata / package reference closureをpreflightとして共有する。

## 研究資料の役割

- `SKILL*.md`: Agent Skill realization
- `references/METHOD*.md`: Method Definition
- `references/REPRESENTATION*.md`, schema, renderer: representation / technical assets
- `evidence/`: lineage / external-skill comparison / research basis
- `evals/`: regression fixtures / application records
- `migration/`: split migration and retention audits
- `package_source`: locale realizationをpackageへ投影するときのsource boundary
- `adapter-metadata-plan.json`: host metadataのsourceとmaturity
- `P2/P3-...MATERIALIZER...md`: production migration前のpackage projection boundary

Layer 2では `evidence/dossier.md` にautoresearch / autonomous research loop / systematic searchとの比較を残す。採用するのはgoal、append-only ledger、recovery、evidence refs、explicit stop等の移植可能なmechanismであり、mandatory scalar metric、autonomous-until-budget、universal search backlog等はMethod不変条件にしない。

未翻訳のevidence / eval / migration資料を、英語runtimeの暗黙の実行指示にはしない。

## Existing Skill delegation

狭い目的に既存Skillがそのまま適合する場合は委譲できる。

- simple bottom-up theme clustering → compatible Affinity Mapping Skill
- already-conceptualized proposition network → Concept Mapping
- finished-claim evidence/inference audit → evidence/inference sorting
- metric-driven autonomous experiment loop → compatible autoresearch realization
- candidate-centric systematic search → compatible search-loop realization

ただし、それらを順に連結しただけで `affinity-synthesis` や `iterative-inquiry-synthesis` 全体と同等とは扱わない。それぞれのMethod Definitionの不変条件を実際に満たす必要がある。

## Checks

```bash
make research-skill-check
```

現在のresearch gateは少なくとも次を検査する。

1. formal suite validator
   - locale realization
   - Method Definition
   - installable name / frontmatter
   - `package_source`
   - source-root escape
   - promotion-relevant skill evidence registration
   - research metadata / checks
   - hard-dependency boundary
2. declared-check / suite-validator wiring validator
   - `suite-manifest.json` のSkill-owned `checks` は `research-skill-check` で直接実行される
   - Skill source root配下でgateへ直接実行するcheckはmanifestにも登録される
   - root `scripts/validate_research_*.py` はすべて `research-skill-check` でちょうど1回直接実行される
   - 存在しない `scripts/validate_research_*.py` をMakefileへ直書きできない
   - plannerはこの命名規約ではなく、Makefileとplanner固有test/contractで追跡する
3. package target / package-local reference closure
4. distribution layout / Skill subtree / entry transform planner
5. OpenAI per-Skill / Claude-Codex bundle adapter metadata validator
6. thin-CSW / sibling Method間のsplit ownership（日英）
7. 三Skill × 二localeのresearch-only package-tree preview
8. affinity-map representationのrecursive grouping / lineage / handoff regression
9. iterative-inquiry-synthesis Method Definitionの日英I1〜I16 parity check
10. `test_research_*.py` のunit test一式
   - bilingual Skill-tree materialization
   - bilingual host-package materialization
   - adapter metadata
   - package reference closure
   - suite/layout/target/entry transform等
   - Layer 1 / Layer 2 promotion-relevant evidence registration
   - Skill-owned check wiringのpositive / missing / unregistered回帰
   - suite-level validator wiringのmissing / unknown / duplicate回帰
   - Layer 2 Method parity checker自身のnegative regression
   - complete-checkout evidence binding

checkの所有権と実行配線を別々の人手記憶にしない。

```text
Skill-owned:
  suite-manifest checks
      <=>
  research-skill-check direct execution

Suite-level:
  scripts/validate_research_*.py
      <=>
  research-skill-check direct execution exactly once
```

complete-checkout gateが `passed` になる場合は、現在のevidence-binding contractに従い、検証commit V上でcanonical commandsを実行し、descriptor gate遷移とexecution recordだけを含むevidence-only child Eを作る。古いcommitのPASS recordを後続のvalidation-relevant HEADへ持ち越さない。

previewを実際に目視したい場合は次を使う。

```bash
make research-skill-preview
```

`dist/research-skill-suite/` に三Skill × 二localeのresearch-only package previewを組み立てる。

英語source上の `SKILL.en.md` はpackage entryでは `SKILL.md` へ投影するが、元sourceは `ORIGIN.json` に残す。その他のexplicit fileはsource rootからの相対構造を保つ。

これはOpenAI / Claude / Codex等の公開platform packageではなく、multi-skill build一般化前の構造確認用である。

release側の通常検証は別である。

```bash
make check
```

GitHub Actionsは現在使用していない。ローカルまたは同等の実行環境で実行する。

## Promotion boundary

公開multi-skill distributionへ進む前に、少なくとも次が必要である。

- complete checkoutで `make research-skill-check` が成功する
- complete-checkout evidence-binding contractに従い、PASSが検証commit Vとevidence-only child Eへ正しく束縛される
- bilingual Skill-tree materializer testsが成功する
- bilingual host-package materializer testsが成功する
- materialized packageと現行production generated packageの構造差分を監査する
- thin-CSW migration後のgenerated artifacts再build
- repository validation / tests成功
- English sibling realizationの独立査読
- runtimeに必要なtechnical assetのlocale可用性確認
- Layer 1 / Layer 2 / CSWのcross-layer handoff / paired regression再確認
- platformごとのdependency / bundle / composite-agent境界の実装

M365だけは、sibling Skill invocationを前提にできないため、現在の限定adapter内に最小compatible material-synthesis fallbackを埋め込む。これはCSW本体がLayer 1を再所有したことを意味しない。

## Current next gate

現在の不足は、runtime、package source、adapter metadata、materializer source、Layer 2 external evidence、Method parity check、research-gate wiring validatorが存在しないことではない。

次に必要なのは、**complete checkoutで現在のvalidation-relevant commit V上のresearch gateとmaterializer testsを実際に通し、生成した日英host package treeを現行production artifactと比較すること**である。

現時点の実行環境ではrepository checkoutを取得できず、接続済み開発端末もofflineだったため、その実行証拠はまだない。

その証拠が得られるまで、production `scripts/build.py` のmulti-Skill一般化、marketplace変更、release asset変更には進まない。