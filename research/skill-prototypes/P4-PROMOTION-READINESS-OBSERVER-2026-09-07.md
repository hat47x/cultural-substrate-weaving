# P4 Promotion Readiness Observer — 2026-09-07

Status: research observation contract; does not authorize production promotion

## 目的

production promotion前の証拠を一つの`ready=true/false`へ潰さず、由来・強さ・authorityを分けたまま観測する。

このobserverは既存authorityを読むだけで、意味上のpromotion判断を代行しない。

## 観測軸

v2では次の15軸を分離する。

1. complete checkout command execution
2. translation source-hash refresh state
3. public-name collision recheck
4. English independent review
5. method split comparative evaluation
6. cross-layer handoff fixture
7. CSW-specific tension / sublation ownership evidence
8. generic host-package materialization contract
9. cross-surface host byte-parity oracle
10. production source contract design
11. production builder generalization
12. production validator generalization
13. checked-out production inclusion descriptor
14. release internal composition design
15. real-host invocation / routing evidence

## 新しく分離した二つの証拠面

### translation_refresh_state

`P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.json`をauthorityとし、statusをそのまま観測する。

`pending-review-hash-refresh`ならpendingのまま報告し、hashを静的に推測・手入力しない。`synchronized`へ進んでも、それはsource trackingの同期でありEnglish independent reviewやcomplete-checkout executionの代替ではない。

```text
translation hash refresh
  != independent English review
  != make check PASS
  != production promotion authorization
```

### csw_tension_ownership_evaluation

`CSW-TENSION-EMERGENCE-CASES.md`と`test_research_tension_emergence.py`を観測する。

この証拠面が守るのは、主に次の方法論境界である。

- framework fitを成功条件そのものにしない
- unresolved tensionを正常な結果として認める
- generic Affinity / Iterative layersへ止揚・Aufhebungの所有を移さない
- CSW evaluationで止揚をsuccess quotaにしない

fixture/testが存在しても実行記録がなければ`fixture-and-ownership-regression-present-unexecuted`までとする。

## 重要な非合成

```text
same-model paired run
  != independent review

handoff fixture
  != executed evaluation

tension ownership regression
  != host readiness

translation hash synchronization
  != translation review

test/oracle present
  != test PASS

builder design contract present
  != production implementation

package materialization
  != real-host invocation/routing evidence
```

reportには`ready` / `promotion_ready` booleanを置かない。全observationは`production_promotion_authorized=false`、最上位`authorization.issued=false`とする。

## current-state第二正本にしない

observerはPR lifecycleや別branchの進捗を手入力しない。

- execution gate → P4 production-suite descriptor
- translation refresh → dedicated translation status JSON
- public name / English review → P4 descriptorと各evidence authority
- method evidence → evaluation/fixture自身
- production design → P4 builder/source/release contracts
- production implementation → checked-out `scripts/build.py` / `scripts/validate.py`
- production inclusion → checked-out `src/skill-set.json`

別PRに実装があっても、checked-out branchに存在しなければ`not-observed-in-this-branch`とする。

## research-skill-checkへの接続

plannerを`research-skill-check`からread-only実行する。

`blocked-not-run`、`pending`、`fixture-only`、`design-only`、`unobserved`は有効なresearch stateであり、それだけではcommand failureにしない。authority file欠落や構造破損など、観測自体が成立しない場合だけplannerを失敗させる。

## 境界

- canonical sourceを変更しない
- production build / validationを変更しない
- production artifactを変更しない
- public nameを変更しない
- current PR stateを複製しない
- promotion authorizationを発行しない

## 結論

**promotion readinessは一つのscoreではなく、異なる由来と強さを持つ証拠集合である。方法論上の緊張保持、翻訳source tracking、package/build mechanics、実host behaviorを互いの代用品にしない。**
