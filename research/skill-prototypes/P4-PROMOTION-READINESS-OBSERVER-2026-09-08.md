# P4 Promotion Readiness Observer v4 — 2026-09-08

Status: research observation contract; does not authorize production promotion

## 目的

production promotion前の証拠を一つの`ready=true/false`へ潰さず、由来・強さ・authorityを分けたまま観測する。

このobserverは既存authorityを読むだけで、promotion判断や未記録のcommand結果を成功認定しない。

## v4の18観測軸

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
12. read-only production source content projection
13. read-only production adapter metadata promotion planning
14. production builder design + checked-out file presence
15. production validator design + checked-out file presence
16. planned production inclusion descriptor presence
17. release internal composition design + validator source
18. real-host invocation / routing evidence

## v3からの追加

### Production source projectionをsource contractへ潰さない

P4では、research `package_source.files`からfuture `locale_tree`へのmappingだけでなく、宣言済みcontent transformをメモリ上で適用するpreviewが追加された。

previewは、Layer 1 frontmatterのinstallable identity、Layer 2の明示installable Skill参照、research sibling filesystem path、English package-local `.en.md`参照、target filename normalization等をproduction候補本文へ投影して検査する。

```text
source contract design
  != content projection preview

content projection preview
  != production source mutation

preview/test source present
  != durable preview execution record
```

observerは`production_source_contract`と`production_source_projection`を別軸にする。

### Adapter metadata promotionも別軸にする

OpenAI sibling metadataのproduction pathへのpromotion planと、Claude/Codex bundle wordingのproduction catalogへのprojection planも、source content projectionとは別責務である。

```text
adapter metadata prototype
  -> read-only promotion plan
  -> review / approval
  -> production metadata mutation
```

observerはplanner/test fileの存在を観測するが、metadata review完了やproduction mutationを推測しない。

### `unexecuted`より`execution-unrecorded`を使う

`research-skill-check`の一つの呼出しでは、observerより前にvalidator/plannerが実行されてobserverへ到達する場合がある。

そのためsourceが存在するだけの状態を機械的に`unexecuted`と断定しない。一方、observerは前段commandの結果を入力として受け取らず、永続的なexecution recordも持たない。

```text
contract / test source present
  -> ...present-execution-unrecorded

dedicated complete-checkout execution record
  -> execution authority
```

「同じmakeがここまで到達した」という事実を、observer自身のreadiness authorityへ変換しない。

### Release compositionもdesignとvalidator sourceを分離する

release composition planに加えて専用validator/testがchecked-out branchに存在する場合は、`design-and-validator-present-execution-unrecorded`まで観測する。

これはrelease validation PASSでもrelease packaging authorizationでもない。

## Authority境界

### prose sniffingをauthorityにしない

paired-runの証拠種別は、本文中の任意substringを探して分類しない。`THREE-LAYER-PAIRED-RUN-2026-09-06.md`自身が持つ`Evaluation type:`行を自己記述metadataとして読む。

### test関数名を意味coverageの正本にしない

CSW tension / sublationについては、fixtureとregression test fileがchecked-out treeに存在することまでを観測する。特定の英語文言やPython test関数名をsubstring検索して「この不変条件が検査済み」と認定しない。

### production source内の関数名から実装済みを推測しない

builder / validatorについて、内部symbolを探してgeneralization実装済みとは判定しない。

observerが記録するのは、design contractが存在するか、contractが指すproduction fileがchecked-out treeに存在するかまでである。

```text
design contract present
  + production file present
  != generalized implementation proven
  != generated-artifact parity
  != test PASS
```

### planned production descriptor pathを推測しない

production inclusion descriptorはlegacy filenameをhard-codeせず、builder contractの`production_files.planned_suite_descriptor`を読む。

### current authorityの世代管理をobserverへ複製しない

complete-checkout status、binding contract、public-name recheck evidence、English review packet / target snapshot / technical-asset localization、将来のcompleted reviewについて、current authorityの選択はproduction descriptorを正本とする。

`scripts/validate_research_current_p4_assets.py` は、descriptorが現在指しているauthority fileが存在し、suite research assetとして登録されていることを検査する。過去のdated packetやstatus recordはresearch historyとして残してよい。

observerはこのcurrent-authority registryを再実装せず、descriptor pointerが指す状態だけを観測する。

## 観測軸に含めないmeta-gate

research gateには、promotion evidenceそのものではなく、**evidence / contractを読む仕組みが壊れていないことを検査するmeta-gate**がある。

現在少なくとも次をこの分類に置く。

- `validate_research_current_p4_assets.py`
  - current authority pointerとsuite登録の整合。
- `validate_research_declared_checks.py`
  - Skill-owned `checks`宣言と`research-skill-check`実行配線の双方向整合。
- `validate_research_production_plan_consistency.py`
  - machine-readable descriptor / builder contractとP4 maintainer proseの整合。
- `validate_research_promotion_preconditions.py`
  - production descriptorのpromotion precondition最低集合の保持。
- complete-checkout evidence binding validator
  - execution evidenceが許されたvalidation treeへ結びつくこと。

これらを19番目以降のreadiness observationへ増やさない。

```text
more gate plumbing
  != more promotion evidence

validator/test source present
  != promotion readiness improved
```

meta-gateが失敗すればobserverの出力やpromotion contractを信用できないためresearch gate全体は失敗すべきだが、meta-gateが増えたこと自体をpromotion evidenceの増加として数えない。

## 非合成

```text
translation hash synchronization
  != independent English review

same-model comparative run
  != independent review

fixture/test source present
  != durable test PASS

Method parity checker declared
  != durable checker PASS

source contract
  != content projection preview

content projection preview
  != production source mutation

adapter promotion plan
  != metadata review completion

design + production file present
  != generalized implementation proven

package materialization
  != real-host invocation/routing evidence

release validator source
  != release validation PASS

static repository state
  != complete-checkout command execution

meta-gate coverage
  != substantive promotion evidence
```

reportには`ready` / `promotion_ready` booleanを置かない。全observationは`production_promotion_authorized=false`、最上位`authorization.issued=false`とする。

## current-state第二正本にしない

observerはPR lifecycleや別branchの進捗を手入力しない。

- execution gate → P4 production-suite descriptor / execution record
- translation refresh → dedicated translation status JSON
- public name / English review → P4 descriptorと各evidence authority
- current P4 authority registration → descriptor + current-P4 asset validator
- Method parity check → suite manifestのdeclared checks
- production source contract → P4 descriptor
- source projection → dedicated preview + regression source
- adapter metadata promotion → dedicated planner + regression source
- production mechanics / inclusion path → builder contract
- release composition → release plan + dedicated validator/test source
- gate wiring / prose consistency / precondition integrity → suite-level meta-validators

別PRに実装が存在しても、checked-out branchに無ければ`not-observed-in-this-branch`とする。

## research-skill-checkへの接続

observer plannerを`research-skill-check`からread-only実行する。

observerより前段のvalidator/plannerが同じcommand chainで成功していても、その成功をobserver report内へ自動転記しない。durable execution authorityが必要なものは、complete-checkout execution record等の専用証拠へ委ねる。

Skill-owned checkについてはsuite manifestを宣言正本とし、`validate_research_declared_checks.py`がMakefileとの双方向配線を検査する。suite-level meta-validatorはSkill-owned evidence軸には数えない。

complete-checkout PASSは古いexecution recordを新しいHEADへ持ち越さない。binding contractとcomplete-checkout validatorがvalidation treeとの結びつきを管理し、observerはその状態を再判定しない。

## 境界

- canonical sourceを変更しない
- production build / validationを変更しない
- production artifactを変更しない
- public nameを変更しない
- current PR stateを複製しない
- promotion authorizationを発行しない

## 結論

**promotion readinessはscoreではなく異質な証拠集合である。source projectionやadapter metadata promotionのように設計より一段具体化したprobeが増えても、それらをproduction mutation・review完了・execution PASSへ無言で昇格させない。さらに、gate wiringやcontract consistencyの改善そのものを新しいpromotion evidenceとして数えない。**
