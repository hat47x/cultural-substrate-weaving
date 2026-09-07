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

baselineは、

```text
adapters/claude-code/locales.json
```

である。

両localeとも既存CSW単体plugin向けcatalogを利用できるが、三Skill bundleのuser-facing wordingとして査読済みとは扱わない。

```text
status = existing-baseline
review_required_for_multi_skill = true
```

research branchでは日英とも三Skill runtime subtreeを計画可能なので、planner上は、

```text
ja-JP runtime_state = buildable
ja-JP metadata_state = review-required

en-US runtime_state = buildable
en-US metadata_state = review-required
```

となる。

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
- multi-Skill bundleでexisting-baselineを使う場合のreview-required保持

ただし、文章品質、host routing精度、公開可否、release readinessは判定しない。

## Coverage planner boundary

`plan_adapter_metadata.py` は、runtime状態とmetadata状態を別々に出す。

これにより、例えばen-USについて、

```text
runtime = buildable
metadata = incomplete-for-realized
```

という状態を正しく表せる。

runtime未実体とmetadata未実体を同じ `blocked` に潰さないことが重要である。

## Why metadata is not auto-generated from SKILL.md

OpenAI `short_description` / `default_prompt` やClaude/Codex bundle descriptionは、host上の入口・routing・activation behaviorへ影響する。

そのためSkill本文から機械的に要約して埋めない。

特に `default_prompt` はMethodの入口を実質的に規定し得るため、runtime本文の単なる派生表示ではない。

## Current unresolved items

1. en-US Affinity / Iterative OpenAI metadataの作成と独立レビュー。
2. ja-JP prototype metadataの実host routing観測または独立評価。
3. Claude/Codex三Skill bundle向けdescription/display review。
4. canonical CSW split後のCSW自身のOpenAI wording再監査。
5. marketplace-level catalog composition。
6. production builder generalization。
7. complete checkoutでのresearch gate / repository gate実行。

## Decision

P2 packaging contractでは、host adapter metadataをruntime/package topologyとは別の層として維持する。

現在のresearch stateは、ja-JP companion OpenAI metadataを `prototype`、en-US companion metadataを `planned` として保持し、Claude/Codexは日英とも `existing-baseline / review-required` とする。

production `scripts/build.py`、production adapter directory、release assetはまだmulti-Skill化しない。
