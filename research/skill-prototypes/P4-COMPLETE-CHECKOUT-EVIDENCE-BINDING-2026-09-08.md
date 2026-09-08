# P4 Complete-Checkout Evidence Binding — 2026-09-08

Status: research gate contract

## Purpose

complete-checkout execution evidenceを古いsource/testへ再利用させない一方、execution record自体をrepositoryへcommitしたことで証拠が自己無効化される矛盾を避ける。

旧contractはpassed recordについて、

```text
execution commit == current checkout HEAD
```

を要求していた。

これは古いPASSの再利用を防ぐ意図としては正しいが、repository内にPASS recordとdescriptor state transitionをcommitすると、そのcommit自身がHEADを変えるため、永続化された証拠では自己参照になる。

本contractはstale-pass防止を弱めず、**validated commitとevidence recording commitを分離する。**

## Three phases

### A. Prepare a clean validation commit

translation hash/stateを含む、command実行前に必要なrepository mutationは先に完了・review・commitする。

今回のtranslation準備では少なくとも:

```bash
make update-en-hashes
# inspect translation-manifest diff and bilingual semantic scope
python scripts/mark_research_translation_refresh_synchronized.py
```

を行い、その変更をcommitする。

このcommitを **validated commit V** とする。

V上でcommandを実行するとき、source/test/translation stateはcleanなrepository identityとして固定されていることが重要である。

### B. Execute the canonical gate on V

Vをcheckoutした状態でcanonical command setを実行する。

```bash
make update-en-hashes
python scripts/mark_research_translation_refresh_synchronized.py
make research-skill-check
make build
make check
```

最初の二つはVで準備済みならidempotentでなければならない。`make update-en-hashes`後にunexpected diffが生じた場合、Vはvalidation対象として未完成なのでPASS recordへ進まない。

全command成功後も、generated tracked artifactやsource fileにunexpected diffが残る場合はrecordしない。

execution recordの`execution commit:`にはVの40桁SHAを記録する。

### C. Record evidence in one evidence-only child commit

PASSをrepositoryへ永続化するとき、Vの直後に**一つだけevidence-only recording commit E**を作ることを許す。

Eで変更してよいものは次だけである。

1. `P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json`
   - `complete_checkout_validation.status`: `blocked-not-run` -> `passed`
   - `complete_checkout_validation.evidence`: canonical blocked record -> new execution record
   - その他のdescriptor fieldは変更しない
2. `research/skill-prototypes/execution/...`
   - Vには存在しなかった新しいPASS execution record一件

Eのfirst parentはVでなければならない。

```text
V  validated commit
|
|  all canonical commands PASS
|
E  evidence-only recording commit
```

E以後にsource、test、method、adapter、descriptor等を変更するcommit Fが入れば、

```text
V -> E -> F
```

となり、Vはcurrent HEADのdirect parentではなくなるためPASS evidenceはstaleとして拒否する。必要ならF上で再実行する。

## Why this is stricter than timestamped prose

次は証拠bindingとして使わない。

- PRがmergeableであること
- test sourceが存在すること
- observer/plannerが存在すること
- 日付が新しいこと
- human proseで「実行済み」と書かれていること

binding authorityはGit commit graph、changed path set、parent/current descriptor差分、およびexecution recordのcommand markersである。

## Allowed transient state

command成功直後、VをHEADとしたままworking treeへPASS record/descriptorを一時生成してvalidatorを確認することはできる。その場合`execution commit == current HEAD == V`である。

ただしこれは未commitのtransient stateであり、永続的なpromotion evidenceではない。repositoryへ記録する場合は上記E contractへ移る。

## Fail closed conditions

passed stateでは少なくとも次を拒否する。

- execution commitがcurrent HEADでもfirst parentでもない
- current HEADがexecution commitのdirect evidence-only childではない
- V→Eでdescriptor/evidence以外のpathが変わった
- descriptorのcomplete-checkout gate以外のfieldがV→Eで変わった
- gateのrequired command setや`production_promotion_authorized`がV→Eで変わった
- execution recordがVですでに存在していた
- evidence pathがexecution record用directory外である
- required PASS markerが欠ける

## Translation boundary

translation hash/state transitionはevidence recording commitへ混ぜない。

理由:

- translation changeそのものがvalidation対象source stateだから
- hash/stateを書き換えたtreeと、それ以前のcommitを同一execution identityにできないから

したがって、translation準備をcommitしてからVでcanonical sequenceを再実行する。

## Promotion boundary

このcontractはcomplete-checkout evidenceのidentityを保証するだけで、production promotionを単独承認しない。

English independent review、public-name直前recheck、production adapter promotion、builder/validator generalization、release internal composition、real-host behavior等の別gateは引き続き独立である。
