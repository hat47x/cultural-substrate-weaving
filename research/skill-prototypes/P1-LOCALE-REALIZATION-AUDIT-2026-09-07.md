# Research Skill Suite — P1 Locale Realization Audit 2026-09-07

Status: research packaging contract; production build is unchanged

## Purpose

P1では、**suite-level locale readiness** と **skillごとの具体的なlocale realization availability** を分ける。

この区別は、runtime artifactが存在することと、そのlocaleが独立査読・promotion・public distributionまで進んでいることを混同しないために必要である。

## Current state after bilingual draft integration

現在のrepository stateは次のとおり。

### cultural-substrate-weaving

```text
ja-JP: existing -> src/ja-JP/ROUTER.md
en-US: existing-translated -> src/en-US/ROUTER.md
```

### affinity-synthesis

```text
ja-JP: prototype -> research/skill-prototypes/affinity-synthesis/SKILL.md
en-US: translated-draft -> research/skill-prototypes/affinity-synthesis/SKILL.en.md
```

各localeに対応するMethod Definitionも存在する。

```text
ja-JP -> references/METHOD.md
en-US -> references/METHOD.en.md
```

### iterative-inquiry-synthesis

```text
ja-JP: prototype -> research/skill-prototypes/iterative-inquiry-synthesis/SKILL.md
en-US: translated-draft -> research/skill-prototypes/iterative-inquiry-synthesis/SKILL.en.md
```

こちらも各localeに対応するMethod Definitionを持つ。

## Status semantics

validatorはstatusを閉じたenumとして所有しない。

特別な意味を持つのは `planned` である。

- `planned`: realization artifactがまだ無くてもよい。
- `planned` 以外: 実在する `runtime_entry` が必要。
- Method Definitionを持つskillのrealized localeでは、locale別 `method_definition` も必要。
- canonical localeは `planned` だけにはできない。

したがって `translated-draft` は、**artifactは存在するがpromotion readinessはまだ満たしていない**状態を表す。

## Suite locale vs skill realization

二つの軸は別の問いに答える。

### Suite-level locale status

> このlocaleで、suite全体をどの成熟段階として扱うか。

現在:

- `ja-JP`: canonical research line
- `en-US`: translated-draft

英語suiteは三Skillのruntime artifactを持つが、independent human review、ancillary research materialの扱い、production multi-skill buildの一般化などがpromotion gateとして残る。

### Per-skill locale realization

> このskillについて、このlocaleで具体的に参照できるruntime realization artifactが存在するか。

現在は三Skillともja-JP / en-USの両方でartifact availabilityがある。

## Validator boundary

`validate_research_skill_suite.py` をresearch suite manifestの正本validatorとする。

現在のvalidatorは少なくとも次を検査する。

- suite schema / `research-only` status。
- 各skillの `locale_realizations` がsuite locale集合と一致する。
- canonical localeがplanned-onlyでない。
- planned以外のrealizationに実在する `runtime_entry` がある。
- Method Definitionを持つskillのrealized localeにlocale別Method Definitionがある。
- runtime / Method Definition / references / evidence / evals / checksがskill `source_root` の境界を守る。
- canonical locale realizationとskill-level `runtime_entry` / `method_definition` が一致する。
- Skill runtimeにfrontmatter `name` がある場合、`installable_name` と一致する。
- Method Definitionがdeclared referenceとして登録される。
- public research contractがhard dependencyを前提にしない。
- suite-level research assetsが実在する。
- distribution prototypeが未知skillを参照しない。

validatorが判定しないもの:

- translation qualityそのもの。
- method parityの実証。
- independent evaluation readiness。
- public release readiness。
- hostがsibling Skillをroutingできるか。

## Ownership cleanup

以前research prototype直下に置いた `validate_suite.py` の有用な検査は正式validatorへ移す。

以後、manifest shapeの正本検査を二重実装しない。planner、tests、Makefileのresearch gateは `scripts/validate_research_skill_suite.py` を共有する。

## Distribution interpretation

`distribution_prototypes.*.contains` は目標package compositionを表す。

現在、三Skillすべてに両localeのruntime artifactが存在するため、layout planner上はja-JP / en-USとも三Skill bundleを `buildable` と判定できる。

ただしここでの `buildable` は、**layoutに必要なrealization artifactが揃っている**という意味に限る。

次を意味しない。

- production `build.py` が三Skill packageを生成できる。
- marketplace / adapterがmulti-skill対応済みである。
- 英語版が独立査読済みである。
- public promotion可能である。

## Decision

**P1は「英語artifact不足を表す段階」から、「artifact availabilityとpromotion readinessを別軸で管理する段階」へ移行した。**

production buildはまだ変更しない。次のP2/P3では、このlocale realization contractを入力としてdistribution descriptorとresearch-only assemblyを安定させてから、production build一般化へ進む。
