# Research Skill Suite — P2 Adapter Metadata Plan 2026-09-07

Status: research adapter metadata contract; production build remains unchanged

## Purpose

P2ではここまでに、runtime/package側について次を分離した。

1. locale realization availability
2. package source boundary
3. distribution target name
4. source→target Skill subtree path
5. Skill entry frontmatter transform

しかし実際のhost packageには、Skill subtreeの外側または横にadapter metadataがある。

現行productionでは特に二種類がある。

### OpenAI Skill

各standalone Skill packageは、

```text
agents/openai.yaml
```

を持つ。

現行CSWではprofileごとに、

- `interactive`: `allow_implicit_invocation: true`
- `metered`: `allow_implicit_invocation: false`

を使い分ける。

`display_name`、`short_description`、`default_prompt`もSkill package固有のmetadataである。

### Claude / Codex plugin

ClaudeとCodexは、現行構造では同じlocale plugin directoryと `skills/` treeを共有する。

plugin-level metadataはSkillごとではなくbundleに一つある。

- Claude: `.claude-plugin/plugin.json`
- Codex: `.codex-plugin/plugin.json`
- locale catalog / marketplace metadata

現行builderでは両方とも `adapters/claude-code/locales.json` をbaselineとして使う。

したがってOpenAIのper-Skill metadataと、Claude/Codexのbundle metadataを一つの「Skill metadata」へ潰さない。

## Separate research descriptor

adapter metadataは `suite-manifest.json` のruntime/package contractへ直接混ぜず、

```text
research/skill-prototypes/adapter-metadata-plan.json
```

で管理する。

理由は、runtime realizationが完成していることとhost metadataが完成していることを独立に追跡するためである。

## OpenAI metadata states

`openai_skill` は、

```text
scope = per_skill_per_profile
```

とする。

profiles:

```text
interactive
metered
```

各Skill × locale × profileについて、

```text
status = existing | planned
```

を宣言する。

`existing` ならsource fileを必須とする。

`planned` ならsourceを持たせない。

この差は「まだ書いていないmetadata」を既存adapterの暗黙流用で済ませないためである。

### Current CSW

CSW ja-JP / en-USは既存adapterをそのままsourceとして登録する。

```text
adapters/openai-skill/<locale>/openai.interactive.yaml
adapters/openai-skill/<locale>/openai.metered.yaml
```

validatorはexisting sourceについて少なくとも次を確認する。

- fileが実在する。
- `interface:` がある。
- `display_name:` がある。
- `short_description:` がある。
- `default_prompt:` がある。
- `policy:` がある。
- profileに対応する `allow_implicit_invocation` 値を持つ。

### Current companion Skills

Affinity / Iterativeは、ja-JP runtime prototypeは既にある。

しかしOpenAI用の、

- display name
- short description
- default prompt
- interactive / metered profile metadata

はまだ設計していない。

そのためja-JPでもmetadata statusは `planned` とする。

これはruntime subtree plannerの `buildable` と矛盾しない。

`buildable` は「runtime source + target pathが分かる」という限定された意味だった。

host packageとして完成しているという意味ではない。

## Claude / Codex bundle metadata states

Claude/Codexは、

```text
scope = locale_bundle
source_mode = locale_catalog
source = adapters/claude-code/locales.json
```

とする。

現行locale catalogには、

- `plugin_name`
- `skill_name`
- `description`
- `display`

がある。

CSW単独pluginを生成してきたbaselineとしては利用可能である。

ただし三Skill bundleへ拡張した後、そのuser-facing wordingを未確認のまま「review済み」と扱わない。

現在は、

```text
status = existing-baseline
review_required_for_multi_skill = true
```

とする。

これはmetadataが壊れているという意味ではない。

単独CSW向けの表現を、三Skill bundle全体の説明としてそのまま公開してよいかを未判断として残す。

## Planner result dimensions

`plan_adapter_metadata.py` はruntime状態とmetadata状態を別に出す。

### ja-JP / OpenAI

runtime:

```text
buildable
```

三Skillともruntime/package source/targetは研究上揃っている。

metadata:

```text
incomplete-for-realized
```

CSWはexistingだが、Affinity / Iterativeはplannedである。

### en-US / OpenAI

runtime:

```text
partial
```

CSWのみrealized。Affinity / Iterativeは英語runtime自体がplannedである。

metadata:

```text
complete-for-realized
```

現在realizedなCSWについてはinteractive / metered metadataが既にある。

これは「英語OpenAI suiteが完成した」という意味ではない。

runtime gapとmetadata gapを分離した結果である。

### ja-JP / Claude and Codex

runtime:

```text
buildable
```

metadata:

```text
review-required
```

既存locale catalogをbaselineとして使えるが、三Skill bundle向けuser-facing wordingのreviewが残る。

### en-US / Claude and Codex

runtime:

```text
blocked
```

Affinity / Iterative英語runtimeが未実体であるため。

metadata baseline自体は存在するが、runtimeが揃うまでbundle生成可能とは扱わない。

## Why metadata completion is not auto-generated

companion Skillのdescriptionから、OpenAI `short_description` や `default_prompt` を自動要約して埋めることはしない。

それらはhost上の利用者導線とactivation behaviorへ影響する。

特に `default_prompt` は方法の入口を実質的に規定し得るため、単純な生成補助文として扱わない。

同様にClaude/Codex bundle descriptionも、三Skillのrole分離が利用者にどう見えるべきかを確認してから決める。

## Validator boundary

`validate_research_adapter_metadata.py` は次を検査する。

- descriptor schema
- suite manifest参照
- Skill-tree distribution集合との一致
- OpenAI Skill / locale / profile集合の一致
- planned / existing stateの整合
- existing source fileと必須marker
- interactive / metered implicit invocation policy
- Claude/Codex locale catalogの必須field
- multi-Skill bundleでexisting-baselineを使う場合のreview-required保持

ただし文章品質や公開可否は判定しない。

## Still unresolved

### Companion OpenAI metadata wording

ja-JP Affinity / Iterativeについて、profile metadataそのものを設計する必要がある。

まずは既存CSWから機械的に複製せず、それぞれのroleに合うdisplay / promptを決める。

### Bundle-level description review

Claude/Codex locale bundleの名称をCSWのまま維持するか、suiteとして別名を与えるかは未決定である。

既存 `cultural-substrate-weaving-ja/en` を維持すればrelease asset互換性は高いが、Skill分離後の概念境界をどこまで名前に出すかは別判断である。

### Marketplace catalog composition

plugin manifest baselineが決まっても、root marketplaceで三Skill bundleをどの説明・tagで掲載するかは別に残る。

### GPT / Microsoft Copilot

composite agent surfacesはこのadapter metadata descriptorの対象外である。

それらはsibling Skill subtreeを直接materializeする設計ではなく、内部Method compositionの表現方法が別だからである。

## Decision

P2 packaging contract now distinguishes runtime/package readiness from host adapter metadata coverage.

次の安全な研究段階は、ja-JP companion OpenAI metadataを実際に設計して、interactive / metered双方の差を持たせたうえで、既存CSW adapterとのpaired reviewを行うことである。

Claude/Codexについては、三Skill bundle向けdescription/displayを先にレビューし、`existing-baseline` から `reviewed` へ上げられるかを判断する。

その前にproduction `scripts/build.py` をmulti-Skill化しない。

complete checkoutでの実 `make check` release gateも未通過のままである。
