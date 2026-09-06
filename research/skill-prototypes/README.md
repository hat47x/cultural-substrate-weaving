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

参照資料のlocale依存とruntime依存は [REFERENCE-CLASSIFICATION.md](REFERENCE-CLASSIFICATION.md) を参照する。

## Package source

`runtime_entry` が存在することと、そのSkillをpackageへ組み立てるsource boundaryが分かっていることを分ける。

locale realizationごとに `package_source` を宣言する。

- `explicit_files`: sibling Skill。source rootからの相対構造を保つfile集合。
- `canonical_manifest`: CSW。既存 `src/manifest.json` とlocale rootを再利用する。

詳細は次を参照する。

- [P1 Locale Realization Audit](P1-LOCALE-REALIZATION-AUDIT-2026-09-07.md)
- [P2 Distribution Layout Plan](P2-DISTRIBUTION-LAYOUT-PLAN-2026-09-07.md)
- [P2 Package Source Descriptor Audit](P2-PACKAGE-SOURCE-DESCRIPTOR-2026-09-07.md)
- [P3 Package Tree Preview](P3-PACKAGE-TREE-PREVIEW-2026-09-07.md)

`package_source` はresearch metadataの全量を意味しない。runtime packageへ必要なsource boundaryだけを表す。

## 研究資料の役割

- `SKILL*.md`: Agent Skill realization
- `references/METHOD*.md`: Method Definition
- `references/REPRESENTATION.md`, schema, renderer: representation / technical assets
- `evidence/`: lineage / external-skill comparison / research basis
- `evals/`: regression fixtures / application records
- `migration/`: split migration and retention audits
- `package_source`: locale realizationをpackageへ投影するときのsource boundary

未翻訳のevidence / eval / migration資料を、英語runtimeの暗黙の実行指示にはしない。

## Existing Skill delegation

狭い目的に既存Skillがそのまま適合する場合は委譲できる。

- simple bottom-up theme clustering → compatible Affinity Mapping Skill
- already-conceptualized proposition network → Concept Mapping
- finished-claim evidence/inference audit → evidence/inference sorting

ただし、それらを順に連結しただけで `affinity-synthesis` 全体と同等とは扱わない。semantic boundary、source return、residual、relation/narrative round-trip等の不変条件を実際に満たす必要がある。

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
   - research metadata / checks
   - hard-dependency boundary
2. distribution layout planner
   - runtimeだけでなくpackage-source descriptorがある場合にだけbuildableとする
3. thin-CSW / sibling Method間のsplit ownership（日英）
4. 三Skill × 二localeのresearch-only package-tree preview
   - `explicit_files` のrelative structure
   - `canonical_manifest` のrouter / modules
   - frontmatter
   - Method Definition
   - relative links
5. affinity-map representationのrecursive grouping / lineage regression

previewを実際に目視したい場合は次を使う。

```bash
make research-skill-preview
```

`dist/research-skill-suite/` に三Skill × 二localeのresearch-only packageを組み立てる。

英語source上の `SKILL.en.md` はpackage entryでは `SKILL.md` へ投影するが、元sourceは `ORIGIN.json` に残す。その他のexplicit fileはsource rootからの相対構造を保つ。

これはOpenAI / Claude / Codex等の公開platform packageではなく、multi-skill build一般化前の構造確認用である。

release側の通常検証は別である。

```bash
make check
```

GitHub Actionsは現在使用していない。ローカルまたは同等の実行環境で実行する。

## Promotion boundary

公開multi-skill distributionへ進む前に、少なくとも次が必要である。

- research gate実行成功
- thin-CSW migration後のgenerated artifacts再build
- repository validation / tests成功
- English sibling realizationの独立査読
- runtimeに必要なtechnical assetのlocale可用性確認
- cross-layer handoff / paired regressionの再確認
- platformごとのdependency / bundle / composite-agent境界の実装

M365だけは、sibling Skill invocationを前提にできないため、現在の限定adapter内に最小compatible material-synthesis fallbackを埋め込む。これはCSW本体がLayer 1を再所有したことを意味しない。

## Current next gate

現在の不足は「source descriptorがないこと」ではない。

次に必要なのは、実行環境で `make research-skill-check` を実際に通し、preview tree・relative link・validator/testの不整合を実データで潰すことである。

その結果が安定するまでproduction `scripts/build.py` のmulti-skill一般化には進まない。
