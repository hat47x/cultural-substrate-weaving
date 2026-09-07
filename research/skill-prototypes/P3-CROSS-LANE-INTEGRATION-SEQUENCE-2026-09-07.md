# CSW改善 cross-lane integration sequence — 2026-09-07

## 目的

CSW改善では、方法論の責務分離、research prototype、package topology、production builder/validator、production inclusion、Living Lab評価が複数レーンで並行して進んでいる。

並行作業そのものは有効だが、各レーンで「次へ進める」ことと、productionへ昇格してよいことは同義ではない。本書では、現在の作業を意味上の依存関係に沿って整理し、他レーンの未完了判断をproduction都合で先取りしない統合順序を定める。

## 現在の方法論側の共通前提

2026-09-07時点では、次を共通前提とする。

- KJ系技能をCSW本体から分離する方向は有力である。
- 一回の材料統合を担う `affinity-synthesis` と、複数roundの探索継続を担う `iterative-inquiry-synthesis` は research prototype として存在する。
- 上記名称はworking nameであり、公開最終名とはまだ扱わない。
- CSWは文化的体系による探索、体系由来候補の帰属、対象側への戻しを中心責務として残す方向で検討する。
- CSW → Iterative → Affinityのhandoffでは、framework由来候補のprovenance / epistemic statusを保持し、target-side supportへ無言で昇格させない。
- `iterative-inquiry-synthesis` は compatible one-round synthesis が必要なのに利用できない場合、その処理を未実行のままstop / handoffできる。
- canonical `src/ja-JP/methods/integration.md` と `src/ja-JP/core/iteration.md` は、分離後のhandoffと評価が十分になるまで縮小しない。
- ja-JP companion prototypeがpackage可能であることは、production readyを意味しない。
- en-US companion realizationはplannedのままであり、locale parityは未確定である。

## 統合グループA — research parity / package probes

対象:

- #294 `validation: research CSW subtree parityを固定する`
- #295 `research: OpenAI host package materializerを追加する`
- #296 `research: Claude/Codex plugin core materializerを追加する`

### 性質

これらはresearch materializerとpackage候補を扱い、canonical `src/`、production `scripts/build.py`、production generated artifactを変更しない。

そのため、方法論側で公開名やcanonical責務移動が未確定でも、比較的独立して統合できる。

### 統合条件

- 完全checkoutで新規unit testが実行できること。
- #294では既存ja-JP CSW subtreeのbyte parityが実測で通ること。
- #295/#296ではrepository外materializationが意図した境界で動作すること。
- prototype metadataをproduction reviewedと誤記しないこと。

### 推奨順

```text
#294
  ↓
#295  #296
```

#295と#296はhost surfaceが異なるため、#294通過後は互いに強い順序依存を持たない。

## 統合グループB — production mechanical refactor

対象:

- #297 `refactor: production Skill-tree writerをhost非依存にする`
- #298 `refactor: production Skill validationをartifact単位へ切り出す`

### 性質

公開Skill数、canonical method、host metadataを変えず、production内部のmechanicsだけを一般化する。

この二つはKJ分離の方法論判断をproductionへ持ち込まないため、方法論レーンと並行して進められる。

### 統合条件

- 完全checkout上の`make check`を実行する。
- `generated-artifacts-check`で既存生成物に意図しない差分が出ないこと。
- `tests/test_build.py`の現行「plugin内Skill数=1」境界を維持すること。
- validation report schema / token budget semanticsを変えないこと。

### 推奨順

#297と#298は独立しているが、説明上は writer → validator の順が理解しやすい。

```text
#297
  ↓
#298
```

ただし、片方の統合がもう片方をproduction promotionへ自動的に進める理由にはならない。

## 統合グループC — production inclusion boundary

対象:

- #299 `research: production Skill inclusion境界を明示する`
- #300 `research: production Skill-setを最小descriptorへ射影する`
- #301 `research: production Skill-set resolver parity gateを追加する`

### 性質

ここでは「作れるSkill」と「productionに含めるSkill」を明示的に分ける。

現在のproduction memberは `cultural-substrate-weaving` 一つだけであり、Affinity / Iterativeはcandidateのままとする。

### 依存順

```text
#299
  ↓
#300
  ↓
#301
```

#300は#299上、#301は#300上のstacked PRとして作成している。

### 統合手順

1. #299をdevelopへ統合する。
2. #300のbaseをdevelopへ付け替えるか、#299統合後のdevelopへrebaseして差分を確認する。
3. #300を統合する。
4. #301について同じ処理を行う。

stacked PRを親より先にdevelopへ直接取り込まない。

## グループ間の推奨順

production出力を変えない範囲では、次を推奨する。

```text
A: research parity/package probes
        ↓
B: production mechanical refactor
        ↓
C: production inclusion boundary
```

厳密なコード依存ではA/Bの一部を並行統合できるが、レビュー上はこの順の方が、

1. research側で予定形を観測する
2. production mechanicsを出力不変で一般化する
3. inclusion判断を外在化する

という因果を追いやすい。

## ここで止める境界

A〜Cをすべて統合しても、次はまだ行わない。

- production descriptorへのAffinity / Iterative追加
- `scripts/build.py`のmulti-Skill output有効化
- Claude/Codex marketplace文面の三Skill化
- release ZIPへのcompanion追加
- canonical `integration.md` / `iteration.md` の削減
- CSW ROUTERからKJ/iteration責務を削除
- en-US companionの公開

これらは別のpromotion phaseである。

## 方法論レーンから必要なpromotion input

production multi-Skill wiringへ進む前に、少なくとも次を他レーンと照合する。

### 名称

- `affinity-synthesis`を公開名として採用するか。
- `iterative-inquiry-synthesis`を公開名として採用するか。
- 「KJ法」という一般名を過度に代表する名称になっていないか。
- 既存のAffinity Mapping系Skill等との役割差が利用者に説明可能か。

### 責務

- one-round material synthesisとmulti-round orchestrationの境界が安定しているか。
- CSW固有のframework exploration / attributionがcompanion側へ漏れていないか。
- Iterative側へgrouping algorithmを複製していないか。
- Affinity側へ文化体系由来の意味づけを埋め込んでいないか。

### Handoff

- `framework_generated`等のstatusがhandoff後も保存されるか。
- target-supported findingとの二重計上を防げるか。
- compatible synthesis不在時を「実行済み」と誤認しないか。
- delayed reactivation / residual / untouched regionを保持できるか。

### 評価

- same-authoring-session fixtureだけでなく、独立性の高い実タスク評価が増えているか。
- Layer 1が本当に必要になるroundを含むか。
- 長期session handoffを含むか。
- useful nonuse / stoppingが評価できるか。
- Living Labの観察を単発scoreへ還元していないか。

### Locale / host

- en-US realizationをどの時点で要求するか。
- locale単位の段階公開を認めるか。
- OpenAI interactive/metered metadataがproduction review済みか。
- Claude/Codex bundle metadata / README / marketplaceが三Skill構成としてreview済みか。
- 実hostでinvocation / routing behaviorを確認したか。

## Production wiring開始条件

次の全体像が揃って初めて、production descriptorに二つ目のSkillを追加する変更を検討する。

```text
method boundary stable enough
        +
handoff/fallback evidence acceptable
        +
public naming decision
        +
production metadata review
        +
generic writer/validator integrated
        +
current CSW parity verified
        +
package/release validators prepared
        +
full checkout make check available
```

この時点では、#301のlegacy single-Skill parity gateが意図的に失敗する。その失敗を、multi-Skill wiring PRで置き換える。

## 現在の結論

各レーンは次の役割で協調する。

- 方法論レーン: 何を別Skillとして成立させるかを決める。
- 評価/Living Labレーン: 分離が実タスクで何を保ち、何を失うかを観察する。
- package researchレーン: hostごとの予定形をproduction外で検証する。
- production mechanicsレーン: 公開集合を変えずにwriter/validatorを一般化する。
- production inclusionレーン: 方法論側の判断を先取りせず、公開集合の境界を明示する。

**production inclusionレーンは、他レーンで確定していない意味上の判断を代行しない。方法論レーンは、production mechanicsの都合だけでcanonical分離を急がない。**
