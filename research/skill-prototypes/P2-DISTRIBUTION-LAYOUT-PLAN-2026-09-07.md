# Research Skill Suite — P2 Distribution Layout Plan 2026-09-07

Status: research layout/buildability planning; production multi-skill build remains unchanged

## Purpose

P2では、P1のlocale realization contractを使って、production `scripts/build.py` をmulti-skill化する前に、**どのdistribution shapeが現在のartifact集合から構成可能か**を機械的に計画する。

ここでの `buildable` は次だけを意味する。

> そのdistribution shapeが要求するskill/primaryについて、manifest上のlocale realization artifactが揃っている。

意味しないもの:

- production packageが実際に生成・検証済みである。
- hostがsibling Skillをroutingできる。
- translation / method parityが独立査読済みである。
- adapters / marketplace metadataがmulti-skill対応済みである。
- byte budgetやrelease asset contractを満たす。
- public promotion / release readinessがある。

## Planner

`research/skill-prototypes/scripts/plan_suite_layout.py` はrepositoryを書き換えず、`suite-manifest.json` からJSON planを標準出力する。

CLIでは正本validator `scripts/validate_research_skill_suite.py` を先に通す。manifestが内部整合していなければplanを出さない。

pure `plan_suite()` はsynthetic manifestをtestから与えられるため、package生成やfilesystem mutationを行わない。

## Distribution rules

### `standalone_per_skill`

各skillを独立artifact候補として扱う。

一部skillだけrealizedならdistribution全体は `partial`、すべてrealizedなら `buildable` とする。

OpenAI Skill向けtarget shapeに使う。

### `locale_bundle`

`contains` に列挙したskillが、そのlocaleですべてrealizedしている場合だけ `buildable` とする。

一つでもplanned/missingならbundle全体を `blocked` とし、`missing_skills` を出す。

Claude/Codex向けtarget shapeに使う。

### `composite_agent_realization`

現段階では `primary` skillのlocale realization availabilityだけを見る。

`buildable` でも、companion Method Definitionが内部へ正しく組み込まれたことは意味しない。planには

> primary realization availability only; internal method-composition parity is not asserted

というscopeを残す。

ChatGPT GPT / Microsoft Copilot向けtarget shapeに使う。

### Unknown mode

未知modeをbuildableへ推測しない。`unsupported` とする。

## Current expected plan

### ja-JP

```text
cultural-substrate-weaving: existing
affinity-synthesis: prototype
iterative-inquiry-synthesis: prototype
```

### en-US

```text
cultural-substrate-weaving: existing-translated
affinity-synthesis: translated-draft
iterative-inquiry-synthesis: translated-draft
```

したがってartifact availabilityだけを見るcurrent planは両localeで次になる。

| Distribution | ja-JP | en-US | Scope |
|---|---|---|---|
| OpenAI standalone-per-skill | buildable | buildable | 各Skillにruntime artifactがある |
| Claude locale bundle | buildable | buildable | target三Skillのartifactが揃う |
| Codex locale bundle | buildable | buildable | target三Skillのartifactが揃う |
| ChatGPT GPT composite | buildable | buildable | primary CSW availabilityのみ |
| Microsoft Copilot composite | buildable | buildable | primary CSW availabilityのみ |

この表は**production build readiness表ではない**。

特にen-USの `translated-draft` は、artifact availabilityとしてはrealizedだが、independent reviewを終えたという意味ではない。

## Production implementation status remains separate

`suite-manifest.json` のdistribution prototypeには `implementation_status` を別に持たせる。

現在:

- OpenAI standalone-per-skill: `planned-production-generalization`
- Claude locale bundle: `planned-production-generalization`
- Codex locale bundle: `planned-production-generalization`
- ChatGPT GPT: `planned-composite-refresh`
- Microsoft Copilot: `implemented-limited-composite-adapter`

これにより、plannerの `buildable` とproduction実装状態を同じstateへ押し込まない。

## Relationship to current production build

現行 `scripts/build.py` は単一CSW Skillを中心に組み立てる。

### OpenAI

将来必要になる変化候補:

- skillごとのruntime/source descriptorを受け取る。
- standalone targetをskill単位で反復する。
- locale realizationをdescriptorから選ぶ。
- research-only / translated-draft / public-readyの状態をpackage生成可否と混同しない。

### Claude / Codex

plugin filesystemは複数Skillを置けるため、同一locale bundleへ三Skillを配置する余地がある。

ただしhost routing behavior、marketplace metadata、生成物validationまでplannerは判定しない。

### ChatGPT GPT / Microsoft Copilot

composite surfaceは、sibling Skillを別artifactとして呼び出せることを前提にしない。

ChatGPT GPTはcompanion Method Definitionを内部へどう取り込むかを別途設計する。

Microsoft Copilotは現在、限定composite adapterとして最小限のmaterial-synthesis fallbackだけを自己完結させ、full sibling-method parityを主張しない。

## Tests

`tests/test_research_skill_suite_layout.py` は現在、少なくとも次を固定する。

- current ja-JP / en-USはartifact availability上、三Skill standalone/bundleともbuildable。
- `translated-draft` はbuildable artifactであってpromotion-readyを意味しない。
- 一つのcompanion realizationを `planned` に戻すとOpenAIはpartial、Claude/Codex bundleはblockedになる。
- unknown target skillはmissingとしてfail-closedに見える。
- composite primaryがplannedならblocked。
- unknown distribution modeはunsupported。

## Research preview assembly

`build_preview.py` はplannerとは別の役割を持つ。

planner:

> manifestだけからtarget shapeのartifact availabilityを計算する。

preview assembly:

> 実際にresearch-only package treeを一時構築し、frontmatter、Method Definition、references、相対リンク等を検査する。

この二つを分離することで、layout planが通っただけでpackage assemblyも通ったと誤認しない。

## P2 decision

**P2は、両localeでlayout inputが揃った状態へ進んだ。次の不足はartifactそのものではなく、production distribution descriptor/build generalizationとpromotion reviewである。**

次はproduction `build.py` を直接全面改造するのではなく、現行build関数とsuite planの間に入るdescriptor contractをresearch側で定義し、research-only assemblyで三Skill×二localeを安定して再現できることを先に確認する。
