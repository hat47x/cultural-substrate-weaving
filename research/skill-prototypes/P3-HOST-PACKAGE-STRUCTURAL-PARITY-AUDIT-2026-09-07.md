# P3 Host Package Structural Parity Audit — 2026-09-07

Status: research-only structural audit; production builder remains unchanged

## 目的

research host-package materializerが、現行production packageから必要な構造的identityを失わず、同時にthin-CSW / three-Skill split後の責務説明へ移れるかを確認する。

ここでいうparityは全文一致ではない。

```text
preserve structural identity
  != preserve stale monolithic wording
  != claim production readiness
```

現行generated artifactには、CSW自身がKJ統合を所有していた時点のdescriptionが残っている。その文言まで一致させると、今回の責務分離を逆流させる。

したがって本監査では、

1. 維持すべきpackage identity
2. split後に意図的に変更すべき意味説明
3. まだresearch materializerが生成しないsurface

を分けて扱う。

## 対象

### Production baseline

```text
plugins/cultural-substrate-weaving-ja/.claude-plugin/plugin.json
plugins/cultural-substrate-weaving-ja/.codex-plugin/plugin.json
plugins/cultural-substrate-weaving-en/.claude-plugin/plugin.json
plugins/cultural-substrate-weaving-en/.codex-plugin/plugin.json
```

### Research bundle metadata

```text
research/skill-prototypes/adapters/claude-codex/ja-JP/bundle-metadata.json
research/skill-prototypes/adapters/claude-codex/en-US/bundle-metadata.json
```

### Research materializer

```text
research/skill-prototypes/scripts/materialize_host_package.py
```

## Claude plugin — 保持する構造

research materializerは、現行production `build_claude()` と同じ主要fieldを生成する。

```text
name
version
author.name
homepage
repository
license
```

localeごとのplugin identityも維持する。

```text
ja-JP = cultural-substrate-weaving-ja
en-US = cultural-substrate-weaving-en
```

`version` はresearch metadataへ複製せず、repository `VERSION` を読む。

`author / homepage / repository / license` もMethodやSkill runtimeへ移さず、host package manifestの責務として保持する。

## Codex plugin — 保持する構造

Claude側の共通fieldに加えて、次を維持する。

```text
keywords
skills = ./skills/
interface.displayName
interface.developerName = hat47x
interface.category = Productivity
```

locale short keywordも現行builderと同じ規則を再利用する。

```text
ja-JP -> ja
en-US -> en
```

`interface.displayName` は既存locale identityを維持する。

```text
ja-JP = Cultural Substrate Weaving — 日本語
en-US = Cultural Substrate Weaving — English
```

## 意図的に一致させないもの

### description

現行production generated artifactのdescriptionは、分離前のmonolithic ownershipを表している。

概念的には次の説明である。

```text
cultural-framework exploration
  + KJ integration owned by the same CSW package
```

research bundle prototypeは、これを次へ置き換える。

```text
cultural-framework exploration
one-round material-led synthesis
multi-round inquiry continuation
```

ただし三つを一つの万能手順へ融合せず、別Skillとして収録し、必要時にhandoffする。

したがって次は**意図的なsemantic delta**である。

```text
Claude plugin.description
Codex plugin.description
Codex interface.shortDescription
```

この差を「production baselineとの不一致」として修正してはならない。

## `contains` と invocation policy

research bundle metadataには、production single-Skill catalogにはなかった次の情報を持つ。

```text
contains:
  - cultural-substrate-weaving
  - affinity-synthesis
  - iterative-inquiry-synthesis

invocation_policy = explicit
```

`contains` はresearch package compositionの監査用metadataであり、そのままClaude/Codex plugin manifestへ未知fieldとして書き込まない。

`invocation_policy = explicit` は各Skill entryのfrontmatter transformへ反映し、Claude/Codexの三Skillすべてに `disable-model-invocation: true` を一度だけ付ける。

## OpenAI Skill

CSWについては既存production adapter metadataをそのままsourceとして再利用する。

```text
adapters/openai-skill/<locale>/openai.interactive.yaml
adapters/openai-skill/<locale>/openai.metered.yaml
```

Affinity / Iterativeにはproduction comparatorがまだ存在しないため、research-only prototype sourceを使用する。

```text
research/skill-prototypes/adapters/openai-skill/<locale>/...
```

したがってOpenAI側では、

- CSW metadata: existing source reuse
- sibling metadata: prototype introduction

という二種類のprovenanceを混同しない。

## Transaction boundary

host-package materializerは最終outputへ直接書かず、repository外のstaging directoryへSkill treeとhost metadataを構築する。

成功した場合だけfinal outputへrenameする。

後段metadata生成が失敗した場合は、

- 不完全なfinal packageを残さない
- staging残骸を削除する
- 呼び出し前から存在した空final directoryは空のまま保つ

ことをcontractとする。

これはrelease atomicityの実装ではない。research evidenceとして不完全treeを完成品と誤認しないための境界である。

## まだ比較対象にしないもの

research host-package materializerは、次を生成しない。

```text
marketplace catalog
README
ZIP / archive
release manifest
release validation report
release asset
ChatGPT GPT composite package
Microsoft Copilot composite package
```

そのため現時点のparity auditから、production package全体の再現性やrelease readinessを導いてはならない。

## 判断

現段階では、production builder generalization時に保持すべき境界を次のように置く。

```text
保持する:
  plugin identity
  version source
  author / repository / license
  Skill path convention
  display identity
  host manifest structure

置き換える:
  monolithic KJ ownershipを前提としたdescription

追加する:
  sibling Skill trees
  sibling OpenAI metadata
  split-aware bundle description

まだ生成しない:
  marketplace / archive / release surfaces
```

この監査は、research materializerのfile-tree unit testsがcomplete checkout上で通ることを代替しない。

## 次のgate

1. `make research-skill-check` をcomplete checkoutで実行する。
2. host-package materializerの日英OpenAI / Claude / Codex testsを通す。
3. materialized packageの主要manifest fieldを現行generated artifactと比較する。
4. description差がsplit ownershipに沿った意図的deltaであることを再確認する。
5. その後にだけproduction builder generalizationの最小差分を設計する。
