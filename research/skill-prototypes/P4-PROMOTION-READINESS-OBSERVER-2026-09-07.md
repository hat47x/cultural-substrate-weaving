# P4 Promotion Readiness Observer — 2026-09-07

Status: research observation contract; does not authorize production promotion

## 目的

三Skill構造のresearchが進むにつれ、promotion前に必要な証拠は一種類ではなくなった。

現在のrepositoryには、少なくとも次が混在する。

- complete checkoutでcommandを実行したかというexecution gate
- public installable nameのcollision recheck
- English sibling realizationのindependent review
- same-model comparative evaluation
- handoff regression fixture
- repository外host-package materialization contract
- byte-parity oracle
- production builder / validatorのdesign contract
- production builder / validatorの実装状態
- production source contractのdesign
- release internal compositionのdesign
- 実host上のrouting / invocation evidence

これらを一つの`ready=true/false`へ潰すと、fixtureをexecution evidenceとして扱ったり、同一modelのpaired runを独立評価として扱ったり、packageを生成できることを実host確認と混同したりしやすい。

そこで `plan_promotion_readiness.py` は、**既存authorityを読むだけのobserver** とする。

## Observerがしないこと

このplannerは次を行わない。

- production promotionを承認しない。
- blockersの数からscoreを作らない。
- PR open/merged stateをrepository内へ複製しない。
- research evidenceをproduction manifestへ昇格しない。
- fixtureの存在を評価実施済みと扱わない。
- test fileの存在をtest PASSと扱わない。
- design contractの存在をproduction実装済みと扱わない。
- package prototypeの存在を実host routing evidenceと扱わない。

reportには意図的に`ready` / `promotion_ready` booleanを置かない。

全observationは `production_promotion_authorized=false` を持ち、最上位`authorization.issued`も常にfalseである。

## 主な観測項目

### complete_checkout_execution

P4 production-suite descriptorの `complete_checkout_validation` をそのままauthorityとする。

現在が `blocked-not-run` なら、その状態を変更せず報告する。静的inspectionを実行成功へ変換しない。

### public_name_recheck

P4 descriptorのrecheck evidenceと各Skillの`public_name_status`を観測する。

collision recheckは時点依存のevidenceであり、単独のpromotion authorizationではない。

### english_independent_review

P4 descriptorの `pending / completed` をそのまま報告する。

review packetやpinned target snapshotの存在からcompletionを推測しない。

### method_split_evaluation

`THREE-LAYER-PAIRED-RUN-2026-09-06.md` が明示するevaluation typeを保持する。

same-model comparative authoring exerciseは `same-model-evidence-present` とし、independent evaluationへ言い換えない。

### cross_layer_handoff

`CSW-HANDOFF-CASES.md` と `L1-L2-HANDOFF-CAPSULE-2026-09-07.md` はregression fixtureとして扱う。

pass/fail条件が具体的でも、それ自体をproduction-readiness evidenceとは扱わない。

### host_package_materialization / cross_surface_host_parity

汎用 `materialize_host_package.py` とtests、cross-surface parity oracleの存在を観測する。

存在してもexecution recordがなければ `*-unexecuted` とし、complete-checkout gateを代替しない。

### production_source_contract

P4 production-suite descriptorのproduction source modeを観測する。

research descriptorが`design-only`なら、そのまま`design-only`として報告する。

### production_builder_generalization / production_validator_generalization

ここは**designとimplementationを分離して観測する**。

active research branchには `P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json` があり、future production builder / validatorのsource-mode operation、distribution topology、validation requirementを設計している。

一方、design contract自身は `status=design-only` / `production_promotion_authorized=false` であり、`scripts/build.py` / `scripts/validate.py`の変更そのものではない。

observerは therefore:

```text
design contract present
+
production helper implementation probe
```

を別dimensionとして保持する。

- designだけなら `design-only`
- mechanical helperだけなら `mechanical-generalization-present-unexecuted`
- 両方あってもexecution recordがなければ `design-and-mechanical-implementation-present-unexecuted`

とし、`PASS`にはしない。

### production_inclusion_descriptor

`src/skill-set.json`がchecked-out branchに存在するかだけを観測する。

別branch/PRにあるものをcurrent branchのproduction stateとして複製しない。

### release_internal_composition

release composition planとP4 `release_shape`があれば`design-only`として観測する。

generated release validation resultとは区別する。

### real_host_behavior

このobserverは、現時点ではcanonicalな実host execution evidence authorityを宣言しない。

したがってpackage prototypeやmetadata testからrouting/invocation確認を推測せず、`unobserved`とする。

## Current-state第二正本にしない

このobserverの重要な性質は、current stateを別JSONへ手入力しないことである。

```text
execution state
  -> P4 complete-checkout gate

English review state
  -> P4 English review gate

public-name evidence
  -> P4 descriptor / recheck evidence

method evaluation type
  -> evaluation record自身

production builder design
  -> P4 builder generalization contract

production mechanics implementation
  -> checked-out production source
```

observerはこれらをその場で読む。

そのため、cross-surface oracleやmechanical refactorが後から同じbranchへ取り込まれれば、observationは`not-observed`から`present-unexecuted`へ自然に変わる。一方、実行記録がなければ`PASS`にはならない。

## `research-skill-check` への接続

planner自体を `research-skill-check` から実行する。

この接続はpromotion gateを閉じるためではない。blocked / pending / fixture-only / design-only / unobservedは有効な研究状態であり、それだけでcommand failureにはしない。

plannerが失敗するのは、authority fileを読めない、期待する構造が壊れた等、**観測そのものが成立しない場合**である。

## 次段階

このobserverを使うと、不足している証拠を「全部未完成」と一括りにせず選べる。

例えば実host behaviorが`unobserved`であるなら、次に設計すべきものはpackage materializerの追加ではなく、hostごとのexecution evidence contractである。

builder designが`design-only`でmechanical implementationが未観測なら、方法論判断を先取りせずにproduction mechanics側の統合を待てる。

## 結論

**promotion readinessは一つのscoreではなく、異なる由来と強さを持つ証拠集合として観測する。observerはそれを見えるようにするが、意味上のpromotion判断を代行しない。**
