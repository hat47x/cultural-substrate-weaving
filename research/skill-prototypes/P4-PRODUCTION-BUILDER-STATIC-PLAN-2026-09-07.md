# P4 Production Builder Static Plan — 2026-09-07

Status: design only; production builder unchanged

## Purpose

`P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json` で定めたproduction name / source / bundle identityを、将来の `scripts/build.py` が生成すべき具体的なtreeへ投影する。

この段階では次を行わない。

- `src/skills/` の作成
- `src/skill-suite.json` の作成
- production adapter metadataの作成
- `scripts/build.py` / `scripts/validate.py` / `scripts/package.py` の一般化
- generated artifactの再build
- production promotionの承認

complete-checkout gateとEnglish independent reviewが未完であるため、production codeへ先回りして実装しない。

## Canonical research assets

Builder変更の意味を二重管理しないため、役割を分ける。

```text
P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json
  public installable name
  production source candidate
  distribution target name
  locale plugin identity
  release shape

P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json
  source mode -> build operation
  distribution -> output shape
  deferred composite boundary
  validation obligations

plan_production_builder_generalization.py
  上記2つを具体的なlocale/profile/pathへ投影するread-only planner
```

`P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json` はproduction manifestではない。builderは将来これをruntime inputとして読まない。

## Production target projection

### OpenAI Skill

各locale・各profileで三つのstandalone Skillを同じdistribution rootへ置く。

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

Layer 1のresearch IDは `affinity-synthesis` だが、production path / frontmatter / adapter targetへresearch IDを漏らさない。

### Claude plugin

locale plugin identityは既存のまま維持する。

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

`weave` は既存CSW bundle内Skill identityとして維持する。

### Codex plugin

Codex用に同じSkillをもう一度copyしない。

Claudeと同じplugin root / `skills/` treeを使い、`.codex-plugin/plugin.json` がそのtreeを参照する。

したがって第一波では新しいCodex ZIP kindを追加しない。

## Source-mode boundary

二つのsource modeは無理に統一しない。

### `canonical_manifest`

CSW専用。

```text
src/manifest.json
+ src/<locale>/ROUTER.md
+ manifest modules
  -> runtime entry render
  -> references copy
```

既存rendererの意味を保つ。

### `locale_tree`

Sibling Skills専用。

```text
src/skills/<public-name>/<locale>/
  SKILL.md
  references/...
  ...
  -> package-relative treeを保ってcopy
```

production canonical `SKILL.md` 自身のfrontmatter `name` はproduction target nameと一致していることをpromotion時に検査する。Layer 1では `material-led-synthesis` であり、research sourceの `affinity-synthesis` をそのままproductionへcopyしない。

## First builder change decomposition

production実装へ進める段階では、巨大な `build_*` 関数へ三Skill分岐を直接埋め込まず、少なくとも次の責務に分ける。

```text
load production suite composition
        ↓
resolve one Skill source for locale
        ↓
materialize one Skill subtree
        ↓
compose distribution root
        ↓
write host metadata once per locale/profile/plugin
```

概念的には次の境界が望ましい。

```text
materialize_csw_skill(...)
materialize_locale_tree_skill(...)

build_openai_locale_profile(...)
build_claude_locale_bundle(...)
build_codex_manifest_for_existing_bundle(...)
```

関数名そのものは固定しない。重要なのは、

- source interpretation
- Skill subtree materialization
- distribution composition
- host metadata

を一つの分岐だらけの処理へ潰さないことである。

## Validator changes required after promotion

production sourceを作る段階になったら、normal validatorへ少なくとも次を追加する。

1. OpenAI各profileの三Skill composition。
2. Claude/Codex bundleの三Skill composition。
3. production descriptor sourceとgenerated sibling treeのparity。
4. 全installed `SKILL.md` へのruntime byte budget。
5. 全Skill subtreeのreference closure。
6. Layer 1 canonical frontmatterが `material-led-synthesis` であること。
7. Layer 2 canonical frontmatterが `iterative-inquiry-synthesis` であること。
8. release ZIP内部の三Skill composition。
9. CodexがClaudeと同じSkill treeを参照し、新しいrelease ZIP kindを増やしていないこと。

## Deferred composites

第一波では次を変えない。

```text
chatgpt_gpt
microsoft_copilot
```

これは「三Skill構造と無関係」という意味ではない。

両者はstandalone Skill-tree distributionではなくcomposite realizationなので、別のcomposition contractとevalを必要とするという意味である。

特にMicrosoft Copilotの限定embedded fallbackを、Layer 1 / Layer 2全文copyへ膨らませない。

## Static regression added

research gateには次を追加した。

- `scripts/validate_research_production_builder_contract.py`
- `research/skill-prototypes/scripts/plan_production_builder_generalization.py`
- `tests/test_research_production_builder_contract.py`

負例では少なくとも次を固定する。

- production builder pathをresearchへ戻さない。
- target nameをresearch IDへ戻さない。
- OpenAI `metered` profileを落とさない。
- Codex用Skill treeを別copyしない。
- M365を第一波へ混入させない。
- Layer 1 production pathを `affinity-synthesis` へ戻さない。
- CSWの既存OpenAI / Claude identityを変えない。

## Current conclusion

production builderの次の変更内容は、コードを書く前にpath-levelまで投影できる状態になった。

一方、現在のgate stateは引き続き次である。

```text
complete checkout execution    blocked / not run
English independent review     pending
production promotion           not authorized
```

したがって、このstatic planの存在を理由にproduction source / builderへ進めない。
