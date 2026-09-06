# CSW → Iterative Inquiry → Affinity Synthesis — Attribution Handoff 2026-09-07

Status: **same-authoring-model controlled cross-layer execution; not an independent model evaluation and not evidence about a real production incident**

## Purpose

CSWから分離した三層を接続したときに、文化体系・認知場から生じた問いが、Layer 2を経由してLayer 1へ渡る途中でtarget-side fact、grouping taxonomy、独立supportへ化けないかを確認する。

このcaseは、`research/human-use-gap-kj/2026-09-04-composite-framework-fields.md` の次の境界を評価用に利用する。

- 複数軸の交差は、一軸だけでは見えにくい問いを生み得る。
- CSWが作った複合場は、伝統上の既存体系とは区別する。
- 複合場から生じた問いが対象資料へ戻って生き残っても、複合場そのものが対象の実在構造になったとは言えない。

評価用のtarget materialは制御された架空ログであり、特定の実システムを記述しない。

---

## Layer 3 — CSW exploration output

### Target-side material available before framework exploration

- `T01`: ある夜、queue depthは00:58から上昇し始めた。
- `T02`: nightly batchは毎日01:00に開始する。
- `T03`: 同じbatchは直前3日にも実行されたが、同様のincidentは記録されていない。
- `T04`: incident当日のdeploymentは00:55開始、01:07完了だった。
- `T05`: 直前2回のdeploymentでは同様のincidentは記録されていない。
- `T06`: consumer restartが01:04に記録されているが、restartの原因はこの材料から分からない。

### CSW exploration

複数周期・状態軸を交差させる探索場から、次の問いが立ったとする。

`FQ01`:

> batch windowとdeployment / restart lifecycleの位相が重なるときだけ、queue上昇がincidentへ進む可能性はあるか。

### Attribution at Layer 3 exit

- **Ref:** `FQ01`
- **Status:** `framework_generated`
- **Origin:** CSW composite-field exploration
- **Operation:** independent cycle / state-axis crossing used as an exploratory cognitive field
- **Target-side support at exit:** none for an interaction effect or causal claim
- **Allowed role:** question / hypothesis / data-collection guide
- **Not allowed:** target fact, causal conclusion, grouping taxonomy, extra independent support

CSWが供給したのは問いであり、`batch × deployment` が対象の実在構造だという所見ではない。

---

## Layer 2 — incoming handoff

`ROUND-TEMPLATE.md` のexternal exploration / epistemic handoff欄へ次のように載せる。

| Ref | Incoming status / role | Origin / operation | Target-side support | Handoff use |
|---|---|---|---|---|
| `FQ01` | `framework_generated` / hypothesis | CSW composite-field exploration / cycle-state crossing | interaction effect: unsupported | question / hypothesis only |

### Round state

- **Round ID:** `cross-layer-attribution-r1`
- **Current inquiry:** incident nightのqueue上昇について、target materialから何が言え、FQ01は何を次に確認させるか。
- **Input delta:** `T01`〜`T06` + `FQ01` with status intact
- **Synthesis required:** yes
- **Bound realization:** `affinity-synthesis@0.1-research`
- **External-status handoff preserved:** yes

Layer 2は`FQ01`をtarget sourceへ書き換えず、Layer 1へ渡す。

---

## Layer 1 — Affinity Synthesis execution

### Source and lineage view

| Ref | Source provenance | Discovery route | Input status / role | Derivation / independence note |
|---|---|---|---|---|
| `T01` | target log | direct input | target observation | independent target item |
| `T02` | target schedule | direct input | target observation | independent target item |
| `T03` | target historical run record | direct input | target observation | comparison material |
| `T04` | target deployment record | direct input | target observation | independent target item |
| `T05` | target historical deployment record | direct input | target observation | comparison material |
| `T06` | target restart record | direct input | target observation + unresolved cause | restart observed; cause unknown |
| `FQ01` | CSW exploration output | composite-field exploration | `framework_generated` hypothesis | not independent target support |

### Material-led reading

`FQ01`の「二軸」を先にbucketとして置かない。まず`T01`〜`T06`が何を言うかを見る。

#### Group G01

**Members:** `T01`, `T02`, `T03`

**Candidate label:**

> incident夜にはbatch開始直前からqueueが上がったが、batch自体は他の日にもincidentなしで実行されている。

保持する差:

- queue riseは00:58から。
- batchは01:00開始。
- batch単独では同じincidentが毎回起きていない。

#### Group G02

**Members:** `T04`, `T05`, `T06`

**Candidate label:**

> incident夜にはdeploymentとconsumer restartが同じ時間帯にあるが、deployment自体は他回にもincidentなしで行われ、restart原因は未確認である。

保持する差:

- deploymentは00:55〜01:07。
- restartは01:04。
- deployment単独の再現性はない。
- restart原因は不明。

### `FQ01` treatment

`FQ01` はG01/G02のmemberにしない。

理由:

- target materialそのものではない。
- `batch × deployment/restart`という交差構造を先にgrouping geometryへすると、frameworkの問いがtarget構造へ昇格する。
- G01/G02がtarget materialだけから成立するかを先に見る必要がある。

ただしFQ01は、G01とG02を並べた後の**verification question**として有効である。

### Relational reading from target material

target materialから安全に言えるのは次までである。

- incident夜にはqueue rise、batch、deployment、restartが近い時間帯に共存した。
- batch単独、deployment単独は他回にincidentなしでも観察されている。
- restart原因は不明。

target materialだけでは次を確定できない。

- batchとdeployment/restartの位相重なりがincident原因である。
- その重なりが必要条件・十分条件である。
- consumer restartが原因か結果か。

### Cross-check

**framework-generated inputをtarget-side supportへ無言で昇格:** none

**framework-generated inputをgrouping geometryへ利用:** none

**framework-generated inputを独立supportとして計上:** none

**target-side observation newly made visible:**

> incident夜では複数のtarget-side eventsが同じ時間窓にある一方、batch単独・deployment単独には非incident例がある。

これは`T01`〜`T06`の比較から得たtarget-side synthesisであり、FQ01が真であることとは別である。

### Residual / next check

`Q01`:

> incidentあり／なしの日を複数集め、batch開始、deployment状態、restart、queue riseの時間関係を比較すると、FQ01のinteraction hypothesisを支持・反証できるか。

`Q01`の発見経路にはFQ01を残す。ただし、次のデータ収集で同じ問いへ到達したとしても、それだけでframeworkがtarget structureとして実証されたとは扱わない。

---

## Layer 2 — post-synthesis round update

### Structural delta

```text
+ G01 := target-side batch/queue timing structure
+ G02 := target-side deployment/restart timing structure
+ TS01 := target-supported synthesis that multiple events co-occurred in one time window while batch-only and deployment-only nonincident examples exist
? FQ01 := framework_generated interaction hypothesis remains unresolved
+ Q01 := verification question for repeated incident/nonincident timing comparison
```

### Epistemic transition check

`FQ01` itselfは`target_supported`へ移さない。

今回target側で支持されたのは、**同じ時間帯に複数eventが存在したことと、単独eventに非incident例があること**までである。interaction effect / causalityは未確認である。

したがってhistoryは次のように分けて残す。

- `FQ01`: origin = CSW, status = `framework_generated`, current = unresolved hypothesis
- `TS01`: origin = target synthesis, status = target-supported within supplied fixture
- `Q01`: derivation = FQ01 + target synthesis comparison, role = next verification question

### Round continuation

**Continue**, if repeated incident/nonincident timing material can be collected.

次roundで戻るもの:

- `FQ01` hypothesis
- `TS01` target-side synthesis
- `Q01` verification question
- G01/G02 handles

今回のroundを理由にCSW composite fieldをtargetの実在modelへ昇格させない。

---

## Handoff result

### Checks

| Boundary | Result | Observation |
|---|---|---|
| CSW output keeps `framework_generated` status | PASS in this controlled execution | Layer 2 input table retains it |
| Layer 2 passes origin / operation to Layer 1 | PASS | explicit handoff metadata |
| framework status becomes grouping geometry | PASS: avoided | groups arise from T01-T06 only |
| framework candidate counts as independent target support | PASS: avoided | FQ01 is not a source vote |
| target synthesis can become separately supported | PASS | TS01 is separate from FQ01 |
| later support erases framework origin | PASS: avoided | FQ01 history remains |
| next-round verification retains both origins | PASS | FQ01 / TS01 / Q01 separated |

### Concrete design finding

方法論の境界自体は既に存在していたが、cross-layer handoffを外部成果物として追えるようにするには、次のrepresentation supportが有効だった。

1. Layer 2 round templateの `Incoming status / role`, `Origin / operation`, `Target-side support`, `Handoff use`。
2. Layer 1 templateの `Input status / role` と、external exploration inputをtarget-side supportへ昇格させていないかのcross-check。

このため今回のtemplate補正は、方法の新しい認識論を追加するというより、**既存I11 / provenance invariantsをSkill分離後のinterfaceで失わないための表現補強**と位置づける。

## Decision

**CONTROLLED PASS at the Method/Skill/template interface level.**

ただしM5を完了扱いにはしない。

- same-authoring-modelである。
- target materialはcontrolled fixtureであり、live taskではない。
- independent model / host routingを通していない。
- English realizationはまだない。
- actual multi-skill package handoffはbuildされていない。

次の強い証拠は、live taskまたは別session/modelで、CSW output artifactを固定してLayer 2→Layer 1へ渡し、同じstatus separationが保持されるかを見ることである。
