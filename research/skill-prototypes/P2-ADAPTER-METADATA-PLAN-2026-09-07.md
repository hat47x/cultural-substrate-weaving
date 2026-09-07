# Research Skill Suite — P2 Adapter Metadata Plan 2026-09-07

Status: research adapter metadata contract; production build remains unchanged

## Purpose

P2 packagingでは、runtime/package側について次を分離した。

1. locale realization availability
2. package source boundary
3. distribution target name
4. source→target Skill subtree path
5. Skill entry frontmatter transform

この文書では、その外側にあるhost adapter metadataを独立した成熟度軸として扱う。

重要な境界は次である。

```text
runtime exists
  != package target is known
  != host metadata exists
  != host wording is reviewed
  != production distribution is approved
```

## Descriptor

adapter metadataは `suite-manifest.json` のruntime/package contractへ直接混ぜず、次で管理する。

```text
research/skill-prototypes/adapter-metadata-plan.json
```

理由は、Skill runtime realizationが存在することと、host固有metadataが完成していることを独立に追跡するためである。

## OpenAI Skill metadata

OpenAI Skillは `per_skill_per_profile` とし、profilesは次の二つとする。

```text
interactive
metered
```

各 Skill × locale × profile のstatusは次の三状態を取る。

```text
planned | prototype | existing
```

- `planned`: metadata source未作成。source pathを宣言しない。
- `prototype`: research-only sourceが存在し、構文・policy検証対象だがproduction採用済みではない。
- `existing`: production adapter sourceが存在する。

profile差は、現段階では方法論を二重化せず、implicit invocation policyだけに限定する。

```text
interactive: allow_implicit_invocation = true
metered:     allow_implicit_invocation = false
```

## Current OpenAI state

### ja-JP

三Skillともruntime/package source/targetは研究上buildableである。

metadataは次の状態である。

```text
cultural-substrate-weaving = existing
affinity-synthesis          = prototype
iterative-inquiry-synthesis = prototype
```

したがってcoverageは、

```text
runtime_state     = buildable
metadata_coverage = prototype-for-realized
```

となる。

### en-US

research branchでは、Affinity / Iterativeの英語runtimeとMethod Definition draftもすでに実体化している。

したがって三Skillともruntime/package source/targetはbuildableである。

一方、companion OpenAI metadataはまだ作成していない。

```text
cultural-substrate-weaving = existing
affinity-synthesis          = planned
iterative-inquiry-synthesis = planned
```

したがってcoverageは、

```text
runtime_state     = buildable
metadata_coverage = incomplete-for-realized
```

となる。

これは英語runtime draftの存在を否定するものではない。runtime maturityとhost metadata maturityを分離した結果である。

## ja-JP companion OpenAI prototype

research-only sourceとして次を置く。

```text
research/skill-prototypes/adapters/openai-skill/ja-JP/
  affinity-synthesis/
    openai.interactive.yaml
    openai.metered.yaml
  iterative-inquiry-synthesis/
    openai.interactive.yaml
    openai.metered.yaml
```

Affinity metadataは、一回のmaterial-led synthesisに留める。

- 先に分類体系を置かない。
- 元材料の来歴と認識状態を保つ。
- 意味単位・束・関係・残差を立ち上げる。
- multi-round orchestrationや文化体系探索を所有しない。

Iterative metadataは、round間の差分再開に留める。

- 前roundを上書きしない。
- touched regionだけをreopenする。
- 必要な一回統合を互換realizationへ委ねる。
- 残差・次の問い・停止理由を追跡する。
- Layer 1 grouping/labelingを自前所有しない。

## Claude / Codex bundle metadata

Claude/Codexは `locale_bundle` であり、per-Skill metadataではなくbundle-level metadataを持つ。

production baselineは、

```text
adapters/claude-code/locales.json
```

である。

### ja-JP

既存CSW単体向けcatalogを三Skill bundleの説明として暗黙流用せず、research-only prototypeを置く。

```text
research/skill-prototypes/adapters/claude-codex/ja-JP/bundle-metadata.json
```

prototypeは既存plugin identityを保つ。

```text
plugin_name = cultural-substrate-weaving-ja
display = Cultural Substrate Weaving — 日本語
invocation_policy = explicit
```

そのうえで `contains` に三Skillを明示し、descriptionでは、

- 文化的体系による探索
- 材料主導の一回統合
- 複数ラウンドの探索継続

を責務の異なるSkillとして説明し、handoff、帰属・残差・未解決の保持、一つの万能手順へ混ぜないことを示す。

planner上は、

```text
runtime_state  = buildable
metadata_state = prototype
source_kind    = research-prototype
```

となる。

`prototype` は reviewed / production-approved を意味しない。multi-Skill bundleなので `review_required_for_multi_skill = true` も維持する。

### en-US

三Skill runtime/package source/targetはresearch上buildableであるが、英語三Skill bundle専用metadataはまだ作成していない。

既存single-Skill locale catalogをbaselineとして保持する。

```text
runtime_state  = buildable
metadata_state = review-required
source_kind    = locale-catalog
```

したがってja-JPとen-USを同じ成熟度へ丸めない。

## Validator boundary

`validate_research_adapter_metadata.py` は次を検査する。

- descriptor schema
- suite manifest参照
- Skill-tree distribution集合との一致
- OpenAI Skill / locale / profile集合の一致
- planned / prototype / existing stateの整合
- prototype / existing source fileの存在
- OpenAI metadata必須marker
- interactive / metered implicit invocation policy
- Claude/Codex locale catalog必須field
- bundle prototypeのschema / locale / status
- bundle prototypeの `contains` とsuite compositionの一致
- bundle prototypeのexplicit invocation
- bundle prototypeが既存plugin nameを保持すること
- multi-Skill bundleでexisting-baselineまたはprototypeを使う場合のreview-required保持

ただし、文章品質、host routing精度、公開可否、release readinessは判定しない。

## Coverage planner boundary

`plan_adapter_metadata.py` は、runtime状態とmetadata状態を別々に出す。

現在の期待値は次である。

```text
ja-JP OpenAI       buildable / prototype-for-realized
ja-JP Claude       buildable / prototype
ja-JP Codex        buildable / prototype

en-US OpenAI       buildable / incomplete-for-realized
en-US Claude        buildable / review-required
en-US Codex         buildable / review-required
```

runtime未実体とmetadata未実体を同じ `blocked` に潰さないことが重要である。

## Why metadata is not auto-generated from SKILL.md

OpenAI `short_description` / `default_prompt` やClaude/Codex bundle descriptionは、host上の入口・routing・activation behaviorへ影響する。

そのためSkill本文から機械的に要約して埋めない。

特に `default_prompt` はMethodの入口を実質的に規定し得るため、runtime本文の単なる派生表示ではない。

同様にbundle descriptionも、「三Skillを同梱する」ことを「三Skillを一つの方法へ混ぜる」ことへ変えてはならない。

## Current unresolved items

1. en-US Affinity / Iterative OpenAI metadataの作成と独立レビュー。
2. ja-JP OpenAI prototype metadataの実host routing観測または独立評価。
3. ja-JP Claude/Codex bundle prototypeのhost表示・routing観測または独立評価。
4. en-US Claude/Codex三Skill bundle専用metadataの設計とreview。
5. canonical CSW split後のCSW自身のOpenAI wording再監査。
6. marketplace-level catalog composition。
7. production builder generalization。
8. complete checkoutでのresearch gate / repository gate実行。

## Decision

P2 packaging contractでは、host adapter metadataをruntime/package topologyとは別の層として維持する。

現在のresearch stateは、

- ja-JP companion OpenAI metadata: `prototype`
- en-US companion OpenAI metadata: `planned`
- ja-JP Claude/Codex bundle metadata: `prototype`
- en-US Claude/Codex bundle metadata: `existing-baseline / review-required`

とする。

production `scripts/build.py`、production adapter directory、release assetはまだmulti-Skill化しない。
