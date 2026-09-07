# P4 Production Builder Static Plan — 2026-09-07

Status: design only; production builder unchanged

## 目的

`P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json` に記した公開名称、production source候補、bundle identityを、将来 `scripts/build.py` が生成すべき具体的なtreeへ投影する。

この段階では、まだ次を行わない。

- `src/skills/` の作成
- `src/skill-suite.json` の作成
- production用adapter metadataの作成
- `scripts/build.py` / `scripts/validate.py` / `scripts/package.py` の一般化
- generated artifactの再build
- production promotionの承認

complete-checkout gateとEnglish independent reviewが未完であるため、production codeを先回りして変更しない。

## Research側で持つ三つの役割

builder変更の意味を複数箇所で重複管理しないよう、research assetの役割を分ける。

```text
P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json
  公開用installable name
  production source候補
  distributionごとのtarget name
  locale plugin identity
  release shape

P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json
  source mode -> build operation
  distribution -> output shape
  deferred composite boundary
  validation obligations

plan_production_builder_generalization.py
  上記2つをlocale / profile / pathへ具体化するread-only planner
```

`P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json` はproduction manifestではない。将来のbuilderがruntime inputとして読むものでもない。

## Production-only suite manifestへの投影

research用promotion descriptorには、査読状態、gate、research IDなど、production builderには不要な情報が含まれている。そのため、将来の `src/skill-suite.json` は別のproduction-only contractとする。

現在は `plan_production_suite_manifest.py` が、その候補形をread-onlyで投影する。

投影後には次を残さない。

- `research_id`
- public nameの審査状態
- complete-checkout gate
- English independent review state
- promotion preconditions
- `research/skill-prototypes/...` へのpath
- `planned-promotion-from-research-prototype` のようなresearch maturity表現

adapter metadataも、research上の成熟度ではなく、productionでどこから読むかだけを表す語彙へ正規化する。

```text
source_patternあり -> per_locale_profile
sourceあり         -> locale_catalog
```

これにより、production builderはresearch workflowを理解せずに済む。

## Production targetの投影

### OpenAI Skill

各locale・各profileで、三つのstandalone Skillを同じdistribution rootへ置く。

```text
dist/<locale>/openai-skill/interactive/
  cultural-substrate-weaving/
  material-led-synthesis/
  iterative-inquiry-synthesis/

dist/<locale>/openai-skill/metered/
  cultural-substrate-weaving/
  material-led-synthesis/
  iterative-inquiry-synthesis/
```

Layer 1のresearch IDは `affinity-synthesis` だが、production path、frontmatter、adapter targetへは漏らさない。

### Claude plugin

localeごとのplugin identityは、既存のものを維持する。

```text
plugins/cultural-substrate-weaving-ja/
  skills/
    weave/
    material-led-synthesis/
    iterative-inquiry-synthesis/

plugins/cultural-substrate-weaving-en/
  skills/
    weave/
    material-led-synthesis/
    iterative-inquiry-synthesis/
```

`weave` は既存CSW bundle内のSkill identityとして維持する。

### Codex plugin

Codex向けに同じSkillをもう一度copyしない。

Claudeと同じplugin rootの `skills/` treeを使い、`.codex-plugin/plugin.json` からそのtreeを参照する。

したがって第一波では、新しいCodex ZIP kindを追加しない。

## Source modeの境界

二つのsource modeは、無理に一つの形式へ統一しない。

### `canonical_manifest`

CSW専用とする。

```text
src/manifest.json
+ src/<locale>/ROUTER.md
+ manifest modules
  -> runtime entryをrender
  -> referencesをcopy
```

既存rendererの意味を保つ。

### `locale_tree`

Sibling Skills専用とする。

```text
src/skills/<public-name>/<locale>/
  SKILL.md
  references/...
  ...
  -> package内の相対treeを保ったままcopy
```

promotion時には、production canonical `SKILL.md` 自身のfrontmatter `name` がproduction target nameと一致することを検査する。

Layer 1なら `material-led-synthesis` であり、research sourceの `affinity-synthesis` をそのままproductionへcopyしない。したがって、builder側にresearch nameからpublic nameへの暗黙の書換え処理を持たせる必要はない。

## 最初のbuilder変更をどう分けるか

production実装へ進める段階でも、巨大な `build_*` 関数へ三Skill分の条件分岐を直接埋め込まない。

少なくとも、次の責務は分けて扱う。

```text
production suite compositionを読む
        ↓
localeごとのSkill sourceを解決する
        ↓
一つのSkill subtreeをmaterializeする
        ↓
distribution rootへ合成する
        ↓
host metadataをlocale / profile / plugin単位で一度だけ書く
```

概念上は、次のような境界が考えられる。

```text
materialize_csw_skill(...)
materialize_locale_tree_skill(...)

build_openai_locale_profile(...)
build_claude_locale_bundle(...)
build_codex_manifest_for_existing_bundle(...)
```

関数名そのものは固定しない。重要なのは、

- sourceの解釈
- Skill subtreeのmaterialization
- distributionへの合成
- host metadataの生成

を、一つの分岐だらけの処理へ押し込まないことである。

## Promotion後にnormal validatorへ必要な検査

production sourceを実際に作る段階では、通常のvalidatorへ少なくとも次を追加する。

1. OpenAI各profileに三Skillが揃っていること。
2. Claude/Codex bundleに三Skillが揃っていること。
3. production descriptorのsourceとgenerated sibling treeが一致すること。
4. 全installed `SKILL.md` にruntime byte budgetを適用すること。
5. 全Skill subtreeでreference closureが成立すること。
6. Layer 1 canonical frontmatterが `material-led-synthesis` であること。
7. Layer 2 canonical frontmatterが `iterative-inquiry-synthesis` であること。
8. release ZIP内部にも三Skillが揃っていること。
9. CodexがClaudeと同じSkill treeを参照し、新しいrelease ZIP kindを増やしていないこと。

## 第一波から外すcomposite realization

第一波では次を変更しない。

```text
chatgpt_gpt
microsoft_copilot
```

これは、三Skill構造と無関係という意味ではない。

両者はstandalone Skill-tree distributionではなくcomposite realizationであり、別のcomposition contractとevalが必要だからである。

特にMicrosoft Copilotの限定embedded fallbackを、Layer 1 / Layer 2の全文copyへ膨らませない。

## 追加した静的regression

research gateには次を追加した。

- `scripts/validate_research_production_builder_contract.py`
- `research/skill-prototypes/scripts/plan_production_suite_manifest.py`
- `research/skill-prototypes/scripts/plan_production_builder_generalization.py`
- `tests/test_research_production_builder_contract.py`
- `tests/test_research_production_suite_manifest_projection.py`

負例では、少なくとも次を固定する。

- production builder pathをresearch側へ戻さない。
- target nameをresearch IDへ戻さない。
- OpenAI `metered` profileを落とさない。
- Codex向けSkill treeを別copyしない。
- M365を第一波へ混入させない。
- Layer 1 production pathを `affinity-synthesis` へ戻さない。
- CSWの既存OpenAI / Claude identityを変えない。
- research promotion stateをproduction-only suite manifestへ持ち込まない。

## 現時点の判断

次にproduction builderへ加える変更は、コードを書く前にpath単位まで投影できる状態になった。

一方、現在のgate stateは引き続き次のとおりである。

```text
complete checkout execution    blocked / not run
English independent review     pending
production promotion           not authorized
```

したがって、このstatic planができたこと自体を理由に、production sourceやbuilderの変更へは進めない。
