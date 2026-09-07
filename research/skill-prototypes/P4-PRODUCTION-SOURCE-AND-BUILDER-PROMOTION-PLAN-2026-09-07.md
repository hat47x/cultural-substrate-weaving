# P4 Production Source and Builder Promotion Plan — 2026-09-07

Status: design only; do not apply before the complete-checkout research gate passes

## 目的

research suiteで検証してきた三Skill構造を、production source / builderへ昇格させる場合の最小変更境界を決める。

この文書はpromotionを承認するものではない。

```text
research package shape is buildable
  != research gate passed
  != public name approved
  != production source promoted
  != release ready
```

現時点ではcomplete checkout上の `make research-skill-check` が未実行であるため、production `scripts/build.py` は変更しない。

## 現行production契約から分かったこと

### `src/manifest.json`

現行manifestはCSW一Skillのruntime sourceを正確に表す。

- canonical locale
- locale description
- router
- modules
- knowledge groups

これはthin-CSW後も有効である。

三Skill化のためにこのmanifestを汎用suite schemaへ変形すると、CSW自身の既存build / translation / GPT / M365契約まで同時に揺らす。

その必要はない。

### `scripts/package.py`

OpenAIとClaudeのrelease ZIP名はlocale単位のsuiteブランドとしてそのまま利用できる。

```text
cultural-substrate-weaving-openai-interactive-<locale>-v<version>.zip
cultural-substrate-weaving-openai-metered-<locale>-v<version>.zip
cultural-substrate-weaving-claude-plugin-<locale>-v<version>.zip
```

中身が一Skillから三Skillになっても、ZIP publication identityを直ちに変更する必要はない。

### `scripts/validate_release.py`

release package kind集合も、OpenAI / Claude / GPT / M365 / canonical docsというdistribution単位である。

したがってOpenAI ZIPの内部に三つのstandalone Skill directoryを含め、Claude plugin内部に三つのSkill subtreeを含めても、package kindそのものを増やす必要はない。

Codexは現行でもClaudeと同じplugin directoryの `skills/` を参照するため、独立ZIP kindを新設する必要はない。

## Production source layout

### 原則

CSW canonical sourceとsibling Skill canonical sourceを別契約として保つ。

```text
src/manifest.json
  = CSW runtime manifest

production suite descriptor
  = distribution composition / sibling package sources
```

research `suite-manifest.json` をproduction builderから直接読まない。

research metadataには、eval、migration、evidence、promotion stateなどrelease runtimeに不要な情報が含まれるためである。

### sibling canonical source候補

working layout:

```text
src/
  skills/
    affinity-synthesis/
      ja-JP/
        SKILL.md
        references/
          METHOD.md
          REPRESENTATION.md
          TEMPLATE.md
          affinity-map.schema.json
        evals/
          CASES.md
        evidence/
          dossier.md
      en-US/
        SKILL.md
        references/
          METHOD.md
          REPRESENTATION.md
          affinity-map.schema.json

    iterative-inquiry-synthesis/
      ja-JP/
        SKILL.md
        references/
          METHOD.md
          ROUND-TEMPLATE.md
      en-US/
        SKILL.md
        references/
          METHOD.md
          ROUND-TEMPLATE.md
```

ここではsource側でもpackage entry名を `SKILL.md` に正規化する。

research段階の `SKILL.en.md` は、英語draftであることを明示するためのincubation namingであり、production canonical sourceへそのまま持ち込まない。

### shared technical asset

`REPRESENTATION.md` やschemaが実質的にlocale-neutralでも、production packageからrepository外shared pathを参照する設計にはしない。

各locale packageのclosureを優先する。

重複排除が必要なら、source generationまたはcanonical-copy validationを別途設計するが、runtime packageの自己完結性を壊さない。

## Production suite descriptor

`src/manifest.json` を置換せず、別のproduction descriptorを追加する方向を第一候補とする。

working name:

```text
src/skill-suite.json
```

責務は次だけに限定する。

```text
suite id
version / locale set
Skill ids
locale별 canonical package source
OpenAI / Claude / Codex target names
distribution composition
production adapter metadata source
```

含めないもの:

```text
research eval history
migration records
paired-run evidence
unresolved naming discussion
promotion rationale
research-only status
```

CSW entryは `src/manifest.json` を参照する `canonical_manifest` modeとして残せる。

Sibling entryはproduction `src/skills/...` を指す `explicit_files` modeでよい。

これによりP2で検証したsource descriptorを、research metadataから切り離してproduction inputへ昇格できる。

## Adapter metadata promotion

### OpenAI

CSWの既存sourceは維持する。

```text
adapters/openai-skill/<locale>/openai.interactive.yaml
adapters/openai-skill/<locale>/openai.metered.yaml
```

Sibling prototypeをpromotionする場合は、production adapter directoryへ移す。

候補:

```text
adapters/openai-skill/<locale>/affinity-synthesis/openai.interactive.yaml
adapters/openai-skill/<locale>/affinity-synthesis/openai.metered.yaml
adapters/openai-skill/<locale>/iterative-inquiry-synthesis/openai.interactive.yaml
adapters/openai-skill/<locale>/iterative-inquiry-synthesis/openai.metered.yaml
```

Research pathをproduction builderが直接読まない。

### Claude / Codex

production bundle identityは現行locale catalogを維持できる。

```text
adapters/claude-code/locales.json
```

promotion時にはdescriptionをsplit-aware wordingへ更新する。

research bundle metadataにある `contains` はsuite descriptor側で保持し、host manifestへ未知fieldとして追加しない。

既存plugin identityは維持する。

```text
cultural-substrate-weaving-ja
cultural-substrate-weaving-en
```

## `scripts/build.py` の最小一般化

### OpenAI

現行 `build_openai()` はCSW一Skillを生成している。

promotion後は概念的に次へ分ける。

```text
build_openai_csw(...)
build_openai_explicit_skill(...)
build_openai_locale_suite(...)
```

ただし既存CSW rendererを捨てない。

CSW:

```text
router + modules
  -> generated SKILL.md + references/
```

Sibling:

```text
canonical SKILL.md + explicit package files
  -> target Skill directory
```

両者を一つのsource formatへ無理に揃えない。

OpenAI profileごとに、

```text
dist/<locale>/openai-skill/<profile>/
  cultural-substrate-weaving/
  affinity-synthesis/
  iterative-inquiry-synthesis/
```

を生成する。

### Claude / Codex

plugin root identityは一つのままにする。

```text
plugins/cultural-substrate-weaving-<locale>/
  skills/
    weave/
    affinity-synthesis/
    iterative-inquiry-synthesis/
```

`build_claude()` は、

1. plugin manifest
2. CSW `weave` subtree
3. sibling subtrees

を生成する構造へ分ける。

`build_codex_plugin()` は同じ `skills/` directoryを参照し続けられるため、主な変更はbundle descriptionの更新である。

### ChatGPT GPT / Microsoft Copilot

P4最初のproduction generalizationには含めない。

これらはcomposite realizationであり、standalone Skill treeをそのまま同梱する契約ではない。

M365の限定embedded fallbackも維持する。

三Skill promotionを理由に、M365へfull Layer 1 / Layer 2 implementationをコピーしない。

## `scripts/validate.py` の必要変更

### そのまま利用できるもの

`check_reference_links()` はinstalled plugin配下の全 `skills/*/SKILL.md` を走査するため、sibling Skillにも自然に拡張できる。

Claude/Codex marketplaceはlocale plugin identityを検査しているため、plugin内部のSkill数が増えてもmarketplace plugin集合自体は変わらない。

### 追加が必要なもの

#### Skill composition

各distributionで期待するSkill集合を検査する。

```text
OpenAI:
  cultural-substrate-weaving
  affinity-synthesis
  iterative-inquiry-synthesis

Claude/Codex:
  weave
  affinity-synthesis
  iterative-inquiry-synthesis
```

#### sibling source / generated parity

production suite descriptorに宣言したexplicit filesが、generated treeへ欠落なく写っていることを検査する。

#### byte budget

現行 `check_budgets()` は主にCSW `SKILL.md` を検査している。

Sibling runtimeにもbudgetを設けるか、全installed Skill entryを共通capで検査する必要がある。

固定の「カード数」等をMethodへ戻す話ではなく、package/runtime file sizeの運用budgetである。

#### locale review

CSWの既存translation manifestとsibling Skillのlocale reviewを混ぜない。

production promotion時には、英語sibling realizationが独立reviewを通ったことをproduction suite descriptorまたは専用translation trackingで確認する。

## `scripts/package.py` / release validation

P4第一段階では、原則としてpackage kindを増やさない。

OpenAI / Claude ZIPはsuite distributionとして既存命名を維持する。

その代わり、release validatorへpackage内部の三Skill composition確認を加えることを検討する。

単にZIPが存在するだけでなく、promotion後にsibling treeが脱落していないことをrelease境界でも確認するためである。

## Public name gate

`affinity-synthesis` と `iterative-inquiry-synthesis` は現時点でworking / research nameである。

特にLayer 1はKJ法・親和図法・質的統合法の系譜を受けつつ、生成AI向け補正を含む。

production canonical pathとinstallable nameを固定する前に、少なくとも次を再確認する。

1. `affinity-synthesis` が公開名称として十分に非誤認的か。
2. KJ法を公式再現と誤認させないdescriptionになっているか。
3. 既存Agent Skill ecosystemで重大な名称衝突がないか。
4. KJ法®等の商標・系譜表記をnameではなくlineage/referenceへ置く方針を維持するか。

production sourceへ昇格した後のrenameはpackage compatibilityへ影響するため、ここはpromotion前gateとする。

## Promotion sequence

```text
P3 complete-checkout research gate PASS
        ↓
public name / independent English review
        ↓
production source layout作成
        ↓
production suite descriptor作成
        ↓
OpenAI / Claude / Codex adapter metadata promotion
        ↓
production builder generalization
        ↓
generated artifact diff review
        ↓
normal validate / tests / token budgets
        ↓
release package internal-composition validation
        ↓
public multi-Skill promotion判断
```

途中の一段が通ったことを、後続段階の成功として扱わない。

## 現時点の判断

P4で採用する第一候補は次である。

- `src/manifest.json` はCSW一Skill manifestとして維持する。
- sibling Skillsは別canonical source treeへ昇格する。
- `src/skill-suite.json` のような薄いproduction suite descriptorを追加する。
- research `suite-manifest.json` をproduction builderから直接読まない。
- OpenAI / Claude / Codexだけを最初のstandalone/bundle promotion対象とする。
- package/releaseの外形は可能な限り維持する。
- GPT / M365 composite realizationは別段階とする。

この設計は、complete checkoutでP3のresearch gateが通るまでは実装へ移さない。
