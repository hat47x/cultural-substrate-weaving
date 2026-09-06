# Research Skill Suite — P2 Distribution Layout Plan 2026-09-07

Status: research layout/buildability planning; no package generation performed

## Purpose

P1でskillごとのlocale realization availabilityをmanifestへ追加したため、production `scripts/build.py` をmulti-skill化する前に、現在のresearch suiteから**どのdistribution shapeを構成できるか**を機械的に計画する。

この段階の `buildable` は次だけを意味する。

> そのdistribution shapeが要求するskill/primaryについて、manifest上のlocale realization artifactが揃っている。

意味しないもの:

- packageが実際に生成・検証済みである。
- hostがsibling Skillをroutingできる。
- English method parityがある。
- adapters / marketplace metadataがmulti-skill対応済みである。
- byte budgetやrelease asset contractを満たす。
- public promotion / release readinessがある。

## Planner

`research/skill-prototypes/scripts/plan_suite_layout.py` はrepositoryを書き換えず、`suite-manifest.json` からJSON planを標準出力する。

CLIでは先に `validate_research_skill_suite.py` を通し、manifestが内部整合していなければplanを出さない。

pure `plan_suite()` はtestからsynthetic manifestを当てられるよう、package生成やfilesystem mutationを行わない。

## Distribution rules

### `standalone_per_skill`

各skillを独立artifact候補として扱う。

localeで一部skillだけrealizedなら、distribution全体は `partial` とし、各skillを `buildable` / `blocked` に分ける。

これはOpenAI Skill向けtarget shapeに使う。

### `locale_bundle`

`contains` に列挙したskillが、そのlocaleですべてrealizedしている場合だけ `buildable` とする。

一つでもplanned/missingならbundle全体を `blocked` とし、`missing_skills` を出す。

Claude/Codex向けtarget shapeに使う。

### `composite_agent_realization`

現段階では `primary` skillのlocale realization availabilityだけを見る。

`buildable` でも、companion Method Definitionが内部へ正しく組み込まれたことは意味しない。planには明示的に

> primary realization availability only; internal method-composition parity is not asserted

というscopeを残す。

ChatGPT GPT / Microsoft Copilot向けtarget shapeに使う。

### Unknown mode

未知modeをbuildableへ推測しない。`unsupported` とする。

## Current expected plan

### ja-JP

skill realization:

```text
cultural-substrate-weaving: existing
affinity-synthesis: prototype
iterative-inquiry-synthesis: prototype
```

したがってlayout availabilityは次になる。

| Distribution | Plan state | Meaning |
|---|---|---|
| OpenAI standalone-per-skill | buildable | 三Skillそれぞれにja-JP realization entryがある |
| Claude locale bundle | buildable | target contains三Skillがすべてrealized |
| Codex locale bundle | buildable | target contains三Skillがすべてrealized |
| ChatGPT GPT composite | buildable | primary CSW ja-JP realizationがあるだけを確認 |
| Microsoft Copilot composite | buildable | primary CSW ja-JP realizationがあるだけを確認 |

ここでClaude/Codex `buildable` は、**研究上のlayout inputが揃った**という意味であり、現行production `build_claude()` が三Skillを生成できるという意味ではない。

## en-US

skill realization:

```text
cultural-substrate-weaving: existing
affinity-synthesis: planned
iterative-inquiry-synthesis: planned
```

したがって:

| Distribution | Plan state | Missing / scope |
|---|---|---|
| OpenAI standalone-per-skill | partial | CSWのみbuildable、affinity/iterativeはblocked |
| Claude locale bundle | blocked | affinity-synthesis, iterative-inquiry-synthesis |
| Codex locale bundle | blocked | affinity-synthesis, iterative-inquiry-synthesis |
| ChatGPT GPT composite | buildable | primary CSW availability only |
| Microsoft Copilot composite | buildable | primary CSW availability only |

このplanにより、`distribution_prototypes.claude_plugin.contains` に三Skillが書かれていることを、英語三Skill packageが現在作れるという誤った意味へ読まなくて済む。

## Relationship to current production build

現行 `scripts/build.py` は単一Skill前提である。

### OpenAI

`build_openai()` は `config["name"]` 一つと一組のcanonical modulesから一つのSkill directoryを作る。

P2以降に必要になる変化候補:

- skillごとのruntime/source descriptorを受け取る。
- standalone targetをskill単位で反復する。
- locale realizationがplannedなら生成対象から外すかblockedとして報告する。

まだ変更しない。

### Claude

`build_claude()` は一つのplugin root内に一つの`skills/<skill_name>`を作る。

filesystem shape自体は複数Skillを置けるため、将来は同じplugin rootへ三Skillを生成する余地がある。

ただし現時点で関数を変更しない。まずresearch plannerがtarget compositionを安定して表せることを確認する。

### Codex

現行Codex manifestはpluginの`skills/` rootを参照するため、Claude側bundleがmulti-skillになれば同じdirectoryを利用できる可能性が高い。

ただしhost routing behaviorまでこのplannerは判定しない。

### ChatGPT GPT / Microsoft Copilot

現行はCSW composite agent realizationを維持する方針である。

P3でLayer 1/2をcanonical sourceへ昇格した後、composite buildがそれらMethod Definitionを内部へ取り込む構造を別途設計する。

primary CSW entryが存在するだけで、その将来compositionが完成したとは扱わない。

## Tests

`tests/test_research_skill_suite_layout.py` は少なくとも次を固定する。

- current ja-JP bundleはlayout上buildable。
- current en-US OpenAI standaloneはpartial。
- current en-US Claude/Codex bundleは二つのcompanion skill不足でblocked。
- companion英語realizationが二つとも揃えばbundleはbuildableへ変わる。
- unknown target skillはmissingとしてfail-closedに見える。
- composite primaryがplannedならblocked。
- unknown distribution modeはunsupported。

これはactual build testではない。

## P2 decision

**Production `build.py` generalizationへ入る前のlayout/buildability contractは、research plannerとして切り出せる。**

次の判断は二つに分ける。

1. 完全checkoutが復旧したら、このplanner/testを含む `make check` を実行する。
2. それ以前に進める場合でも、production buildを直接書き換えるのではなく、現行build関数とsuite planの間に必要なdescriptor contractをresearch側で設計する。

英語companion Skillを先に捏造してbundleをgreenにすることはしない。
