# P4 Promotion Readiness Observer v3 — 2026-09-08

Status: research observation contract; does not authorize production promotion

## 目的

production promotion前の証拠を一つの`ready=true/false`へ潰さず、由来・強さ・authorityを分けたまま観測する。

このobserverは既存authorityを読むだけで、promotion判断や未実行検証の成功認定を行わない。

## v3の観測軸

1. complete checkout command execution
2. translation source-hash refresh state
3. public-name collision recheck
4. English independent review
5. method split comparative evaluation
6. Method Definition parity check declaration
7. cross-layer handoff fixture
8. CSW-specific tension / sublation regression source
9. generic host-package materialization contract
10. cross-surface host byte-parity oracle
11. production source contract design
12. production builder design + checked-out file presence
13. production validator design + checked-out file presence
14. planned production inclusion descriptor presence
15. release internal composition design
16. real-host invocation / routing evidence

## v2からの重要な変更

### prose sniffingをauthorityにしない

paired-runの証拠種別は、本文中の任意substringを探して分類しない。

`THREE-LAYER-PAIRED-RUN-2026-09-06.md` 自身が持つ `Evaluation type:` 行を自己記述metadataとして読み、その値をreportへ残す。

```text
self-described evidence metadata
  -> observe

arbitrary prose wording
  -> do not use as machine authority
```

自然な文章修正で証拠種別が変わる構造を避ける。

### test関数名を意味coverageの正本にしない

CSW tension / sublationについては、fixtureとregression test fileがchecked-out treeに存在することまでを観測する。

特定の英語文言やPython test関数名をsubstring検索して「この不変条件が検査済み」と認定しない。意味coverageはfixture/test自身と実行結果の責務であり、observerはその代行をしない。

### production source内の関数名から実装済みを推測しない

builder / validatorについて、`def write_skill_tree(` 等の内部symbolを探してgeneralization実装済みとは判定しない。

observerが記録するのは、

- design contractが存在するか
- contractが指すproduction fileがchecked-out treeに存在するか

までである。

```text
design contract present
  + production file present
  != generalized implementation proven
  != generated-artifact parity
  != test PASS
```

実装完了のclaimは専用validator・artifact diff・command execution等の強い証拠へ委ねる。

### planned production descriptor pathを推測しない

production inclusion descriptorはlegacy filenameをhard-codeせず、`P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json` の `production_files.planned_suite_descriptor` を読む。

## Method Definition parity

active research branchではLayer 2のja/en Method Definition parity checkerがsuite manifestの`checks`へ登録され、`research-skill-check`にも配線されている。

observerはそのdeclared check fileの存在を別軸で観測するが、complete checkout上で未実行なら`declared-checks-present-unexecuted`までに留める。

## 非合成

```text
translation hash synchronization
  != independent English review

same-model comparative run
  != independent review

fixture/test source present
  != test PASS

Method parity checker declared
  != checker PASS

design + production file present
  != generalized implementation proven

package materialization
  != real-host invocation/routing evidence

static repository state
  != complete-checkout command execution
```

reportには`ready` / `promotion_ready` booleanを置かない。全observationは`production_promotion_authorized=false`、最上位`authorization.issued=false`とする。

## current-state第二正本にしない

observerはPR lifecycleや別branchの進捗を手入力しない。

- execution gate → P4 production-suite descriptor / execution record
- translation refresh → dedicated translation status JSON
- public name / English review → P4 descriptorと各evidence authority
- Method parity check → suite manifestのdeclared checks
- production design → P4 builder/source/release contracts
- production file path → builder contract
- production inclusion path → builder contract

別PRに実装が存在しても、checked-out branchに無ければ`not-observed-in-this-branch`とする。

## research-skill-checkへの接続

plannerを`research-skill-check`からread-only実行する。

`blocked-not-run`、`pending`、`fixture-only`、`design-only`、`unclassified`、`unobserved`は有効なresearch stateであり、それだけではcommand failureにしない。

authority file欠落やJSON構造破損など、観測そのものが成立しない場合のみplannerを失敗させる。

## 境界

- canonical sourceを変更しない
- production build / validationを変更しない
- production artifactを変更しない
- public nameを変更しない
- current PR stateを複製しない
- promotion authorizationを発行しない

## 結論

**promotion readinessはscoreではなく異質な証拠集合である。observer自身も、文章表現や内部symbolを新しいauthorityへ変えず、既存authorityの強さを超えてclaimしない。**
