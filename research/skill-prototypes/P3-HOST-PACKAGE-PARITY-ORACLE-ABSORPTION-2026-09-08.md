# P3 Host Package Cross-Surface Parity Oracle — 2026-09-08

Status: research validation design; does not authorize production promotion

## 目的

research host-package materializerが、hostごとの外周差を加えてもSkill tree semanticsとdeclared metadata authorityを壊さないことをcross-surfaceで観測する。

oracle自身がhost readinessやpromotion readinessの第二正本を持たないことを重視する。

## Identity境界

次の三つを同一視しない。

```text
research identity
public / installable identity
distribution target name
```

特にSkill directory名をresearch IDとして固定しない。

oracleはsuite manifestの

`locale_realizations[locale].package_targets[distribution].skill_name`

をmaterializerと同じtarget-name authorityとして読む。

これにより、たとえばCSWが

```text
OpenAI: cultural-substrate-weaving
Claude/Codex: weave
```

となる場合も、oracle側でresearch IDからtarget名を再推測しない。

## Locale readinessを第二正本にしない

suiteにlocaleが存在するだけではhost-materializableと扱わない。

対象localeは、そのdistributionについて少なくとも、

- runtime realizationが`planned`ではない
- package target nameが宣言済み
- materializer自身が受理するmetadata maturity

を満たすものだけとする。

OpenAI profile集合とaccepted metadata statesも`materialize_host_package.py`から再利用する。

## Oracle

### OpenAI profile parity

interactive / meteredの間で、各Skillの`agents/openai.yaml`を除くSkill treeがbyte-identicalであることを確認する。

profile差をSkill content差へ漏らさない。

### OpenAI metadata source parity

materialized `agents/openai.yaml`が、adapter metadata planで宣言されたsourceとbyte-identicalであることを確認する。

### Claude / Codex shared Skill tree

同一localeで両hostがmaterializableな場合、

- declared Skill target集合が一致する
- `skills/` subtreeがbyte-identicalである

ことを確認する。

host manifest外周の違いをSkill semanticsの違いへ変換しない。

### Bundle wording / version parity

Claude / Codexのdeclared bundle metadataについて、

- plugin name
- description
- display

の整合を確認し、materialized manifestのversionがrepository `VERSION`に追随することを確認する。

## このoracleがしないこと

- public/installable nameを決めない
- locale readinessを固定一覧で持たない
- metadata maturityを独自定義しない
- dedicated host materializerを増やさない
- canonical `src/`を変更しない
- production builder / validatorを変更しない
- generated artifactを変更しない
- real-host invocation / routing behaviorを推測しない
- oracle sourceの存在をexecution PASSへ変換しない
- promotion authorizationを発行しない

## current activeへの再構成

current active `research/kj-skill-delegation-v0.5`のhost materializerは、

- `OPENAI_PROFILES`
- `READY_OPENAI_METADATA`
- `READY_BUNDLE_METADATA`
- `package_targets[distribution].skill_name`
- `materialize_host_package()`

を引き続き提供している。

そのためoracleはこれらのauthorityを再利用し、current activeへ意味変更なしで再構成できる。

## 検証境界

GitHub Actionsや完全checkout executionが無い場合、test sourceが存在してもPASSとは扱わない。

このoracleは、将来complete checkout上でhost materialization regressionを実行するためのcontractであり、production promotion authorizationそのものではない。

## 結論

**host差はhost外周で表現し、Skill tree identity・content・declared metadata authorityはdistribution targetとmaterializerの正本から導く。oracle自身が新しいreadiness正本を作らない。**