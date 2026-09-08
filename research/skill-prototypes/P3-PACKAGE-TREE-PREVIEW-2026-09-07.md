# Research Skill Suite — P3 Package Tree Preview 2026-09-07

Status: research package-tree experiment; production build remains unchanged

## Purpose

P2で packaging contract を次の四層へ分離した。

```text
locale realization
  -> package_source
  -> package_targets
  -> Skill subtree mapping
  -> Skill entry transform
```

P3では、これらのread-only planを経たsourceをresearch-only temporary treeへ実際に投影し、relative structureとlink topologyを確認する。

production `scripts/build.py` はまだmulti-skill化しない。

## No duplicate descriptor schema

途中で別のbuild descriptor / package-tree plannerを置く案も試したが、責務がP2 plannerと重なったため削除した。

正本は次とする。

- realization/source/target metadata: `suite-manifest.json`
- layout readiness: `plan_suite_layout.py`
- source→target path: `plan_skill_subtrees.py`
- host Skill-entry policy: `plan_skill_entry_transforms.py`

P3 previewはこれらと矛盾しない実treeを検査するconsumerであり、新しいmethod/package schemaの正本にはしない。

## Bilingual runtime entry projection

ja-JP sibling source:

```text
SKILL.md -> SKILL.md
```

en-US sibling source:

```text
SKILL.en.md -> SKILL.md
```

subtree planではsource identityとtarget-relative pathを両方保持する。

このため英語source filenameを日本語sourceへ寄せたり、package側に `SKILL.en.md` を要求したりしない。

## Copy vs render

subtree mappingはoperationを保持する。

### Explicit sibling Skill

```text
operation = copy
```

ただしentry bodyをhost surfaceへ出すときは `plan_skill_entry_transforms.py` のfrontmatter policyを適用できる。

### Canonical CSW

```text
ROUTER.md -> SKILL.md
operation = render_runtime_entry
```

CSW routerについてresearch側に第二のrendererを作らず、production migration時も既存canonical builder renderを正本にする。

modulesは `copy` として `references/<skill_reference>` へ写る。

## Distribution topology

OpenAI standalone:

```text
cultural-substrate-weaving/
affinity-synthesis/
iterative-inquiry-synthesis/
```

Claude / Codex locale bundle:

```text
skills/weave/
skills/affinity-synthesis/
skills/iterative-inquiry-synthesis/
```

現在は日英ともartifact/source/target metadataが揃うため、read-only topologyは両localeで計画できる。

これはproduction bundle生成や英語promotion readinessを意味しない。

## Generic preview

`build_preview.py` はhost-specific release packageではなく、三Skill×二localeのgeneric research packageをtemporary directoryへ組み立てる。

確認対象:

- `SKILL.md` entryが存在する
- installable nameが一致する
- locale Method Definitionが存在する
- explicit fileの相対構造が保持される
- CSWはcanonical manifest/module集合を再利用する
- relative Markdown linkが解決する
- `ORIGIN.json` に `research_only: true` を残す

host-specific OpenAI/Claude/Codex treeの正確なpath・entry policyはP2 subtree/entry plan側を正本とする。

## Locale boundary

英語 `translated-draft` はartifact availabilityを表し、独立査読済みを意味しない。

Affinity en-US package sourceは現在、英語runtime/Methodと共有technical assetへ限定する。日本語Methodや全research recordを暗黙同梱しない。

Iterative en-USでは `ROUND-TEMPLATE.md` が日本語research templateであることをSkill本文上で明示し、英語Method Definitionの代わりにはしない。

## What P3 does not prove

- actual production package build
- host routing behavior
- OpenAI agent metadata parity
- Claude/Codex plugin / marketplace metadata parity
- ChatGPT GPT composite Method composition
- Microsoft 365 full sibling-method parity
- independent English review
- token / byte budget
- release readiness

## Next boundary

`plan_skill_entry_transforms.py` の次に残るのはhost adapter metadataである。

特に、

- OpenAI `agents/openai.yaml`
- Claude `.claude-plugin/plugin.json`
- Codex `.codex-plugin/plugin.json`
- locale plugin README / marketplace metadata

について、bundle-level metadataとSkill-level metadataを分ける必要がある。

ただしcomplete execution environmentでresearch gateを通すまではproduction builder一般化を急がない。

## Decision

**P3 previewはP2のsource/target/subtree/entry-transform contractをdogfoodする検査層であり、第五のpackage schemaを追加しない。**
