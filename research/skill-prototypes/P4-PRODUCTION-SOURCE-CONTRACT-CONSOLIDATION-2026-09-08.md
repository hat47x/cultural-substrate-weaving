# P4 Production source contract consolidation — 2026-09-08

Status: design consolidation only; no production promotion authorization

## 目的

production inclusionレーンで検討してきた単一Skill向けdescriptor案と、active P4で進んだ三Skill production promotion designを統合し、**production sourceを表す語彙・責務境界・旧案から引き継ぐ設計意図**を一箇所に整理する。

この文書は新しい第三schemaを追加しない。

機械的な正本候補は、既存の次の二つとする。

- `P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json`
- `P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json`

それぞれのvalidatorが通ることを前提とし、本書はcross-laneの読み違いを防ぐ説明層だけを担う。

## 結論: production source modeは二種類

P4第一段階のproduction sourceは、次の二種類に固定する。

### `canonical_manifest`

現行CSWに使う。

```text
research_id: cultural-substrate-weaving
production_source:
  mode: canonical_manifest
  manifest: src/manifest.json
```

`src/manifest.json`はCSW自身のruntime source contractとして維持する。

- canonical locale
- locale description
- router
- modules / references
- knowledge groups

三Skill化のためにこれを汎用suite manifestへ変形しない。

### `locale_tree`

one-round / iterative sibling Skillに使う。

```text
production_source:
  mode: locale_tree
  root_pattern: src/skills/<installable-name>/{locale}
  runtime_entry: SKILL.md
```

builder operationは、locale tree内のruntime-relative pathを保持してpackageへcopyする。

SiblingをCSWのrouter/modules形式へ無理に変換しない。

## `explicit_files`との関係

過去のP2/P4 proseには、sibling sourceを`explicit_files`と表現した箇所がある。

現在の機械契約では、source mode名として`explicit_files`を採用しない。

`locale_tree`を採用する理由は、production canonical sourceへ昇格した後は各locale package sourceが自己完結treeとなり、個々のfile listを別metadataとして重複列挙せずともpackage closureを表せるためである。

必要なfile closure検査は別validatorで行い、source identityとfile inventoryを混ぜない。

したがって今後は次とする。

```text
source mode vocabulary:
  canonical_manifest
  locale_tree
```

古い`explicit_files`表現はhistorical design descriptionであり、production schema候補へは持ち込まない。

## 旧#300から引き継ぐもの／引き継がないもの

旧#300は、current one-Skill production stateを次の最小形で表そうとした。

```text
id + source_manifest
```

この発想から引き継ぐもの:

- production公開集合をresearch candidate集合から分離する。
- production builderがresearch suiteを自動発見しない。
- production descriptorはruntime compositionに必要な情報だけを持つ。
- research evidence / promotion rationale / maturityをproduction inputへ複製しない。

引き継がないもの:

- すべてのSkill sourceを`source_manifest`一種類へ押し込むこと。
- research IDをそのままpublic/installable nameとして扱うこと。
- current one-Skill projectionをfuture suite schemaとして暗黙拡張すること。

## 旧#301から引き継ぐもの／引き継がないもの

旧#301はread-only resolverとexact-one migration guardを提案した。

引き継ぐもの:

- resolverはsourceを解決するだけで、candidate選定やpromotion判断を行わない。
- resolverはresearch maturityを読まない。
- current one-Skill builderとの移行中は、二つ目のSkill追加が自動的にbuildへ流れないguardを置く。
- multi-Skill wiring時にguardを意図的に置き換える。

引き継がないもの:

- `source_manifest`しか扱えないresolver schema。
- exact-oneを恒久policyとして残すこと。

将来resolverは`production_source.mode`でdispatchする。

```text
canonical_manifest
  -> render runtime entry + copy manifest references

locale_tree
  -> copy locale tree preserving runtime-relative paths
```

このdispatchはP4 builder contractの`source_mode_operations`と一致させる。

## Identityを三層に分ける

production suiteでは、少なくとも次を同一視しない。

### Research identity

例:

```text
affinity-synthesis
```

これは研究上の追跡IDである。

### Public / installable name

current P4 candidate:

```text
material-led-synthesis
```

これは利用者に見えるSkill名およびproduction canonical path候補に使う。

### Distribution target name

host/distributionごとにproduction descriptorの`targets`から取得する。

CSWの例:

```text
OpenAI: cultural-substrate-weaving
Claude: weave
Codex: weave
```

したがってbuilderは、research IDからtarget名を推測しない。

Siblingで現時点のtarget名とpublic nameが一致していても、それは契約上の同一概念ではない。

## Adapter metadataとの境界

production source contractはmethod sourceを指す。

host metadataは別責務としてproduction descriptorから参照する。

- OpenAI: per-locale / per-profile metadata
- Claude/Codex: locale bundle catalog

Research prototype metadataをproduction builderが直接読まない。

Promotion時はproduction adapter pathへ移す。

## Production descriptorが持つもの

P4第一段階の薄いsuite descriptorは、概念的に次を持つ。

```text
suite identity
version / locale set
Skill research identity
public/installable name
production source contract
first-wave distribution target names
production adapter metadata source
bundle identity
release composition
```

ただし、これらをすべて一つの「Skill identity」に圧縮しない。

## Production descriptorが持たないもの

次はresearch側に残す。

```text
paired-run history
eval history
migration evidence
Living Lab event ledger
promotion rationale
unresolved ownership discussion
research maturity score / readiness boolean
```

また、promotion readinessを単一booleanへ潰さない。

## Production builderが読んではいけないもの

P4 contractどおり、runtime production build inputとして次を直接読まない。

```text
research/skill-prototypes/suite-manifest.json
research/skill-prototypes/adapter-metadata-plan.json
research/skill-prototypes/adapters/
```

Research planning artifactが存在することとproduction sourceが昇格済みであることを分離する。

## First-wave distribution境界

production source contractの第一波は次だけを対象とする。

```text
openai_skill
claude_plugin
codex_plugin
```

ChatGPT GPT / Microsoft Copilotはcomposite realizationであり、第一波builder generalizationへfull sibling Skill treeをコピーしない。

## Release shapeとの関係

Skill数が一つから三つへ増えても、第一波ではdistribution package kindを増やさない。

- OpenAI ZIP: locale/profile suiteとして内部にstandalone Skill directoryを複数持つ。
- Claude ZIP: locale plugin内部に複数Skill subtreeを持つ。
- Codex: Claude pluginの同じ`skills/` treeを再利用する。

その代わりrelease validationで内部Skill compositionを検査する。

## Promotionを開始しない条件

このsource contractが整理されたこと自体はpromotion authorizationではない。

少なくとも次が未完了なら、`src/skill-suite.json`や`src/skills/...`をproductionへ作成しない。

- complete checkout上のresearch gate
- translation source-hash refresh
- independent English review
- public installable nameの直前recheck / approval
- production adapter metadata review
- production builder / validator generalizationのartifact diff review
- release internal-composition validation

## Cross-laneでの読み方

方法論レーンは、このsource contractの都合でSkill責務やpublic nameを決めない。

production inclusionレーンは、研究prototypeがbuildableになったことだけを理由にproduction memberへ追加しない。

packageレーンは、research専用materializerを第二正本として増殖させず、単一汎用host materializerへoracleを集約する。

評価レーンは、source pathの整備をmethod effectiveness evidenceとして数えない。

## 現段階の判断

P4 production source designは次へ収束した。

```text
CSW
  internal/research id: cultural-substrate-weaving
  production source: canonical_manifest -> src/manifest.json

one-round sibling
  internal/research id: affinity-synthesis
  public candidate: material-led-synthesis
  production source: locale_tree -> src/skills/material-led-synthesis/{locale}

iterative sibling
  internal/research id: iterative-inquiry-synthesis
  public candidate: iterative-inquiry-synthesis
  production source: locale_tree -> src/skills/iterative-inquiry-synthesis/{locale}
```

この構造を、旧`id + source_manifest` v1へ後退させない。

同時に、design-only descriptorをそのままproduction inputへ昇格させない。
