# CSW — 親和統合／反復探索との最小接続契約

作成日: 2026-09-06
Status: research candidate

## 目的

KJ法由来の材料統合技能と、複数roundの探索管理をCSWから分離した後、`cultural-substrate-weaving` に何を残すかを明示する。

この文書は、現行 `methods/integration.md` と `core/iteration.md` をすぐ削除する指示ではない。独立Skillの回帰確認が済んだ後に、CSW側をどこまで薄くできるかを見る移管契約である。

## 1. 三層の責務

### Layer 1 — Affinity Synthesis

所有する:

- meaning-bearing card boundary
- epistemic seam
- grouping / bundle
- label / higher-order integration
- primary placement / secondary resonance
- relational structure
- diagram ↔ narrative round-trip
- source return check
- inherited / emergent / residual transformation audit
- representation grammar / lineage / diagram projections

CSWはこれらの内部アルゴリズムを再定義しない。

### Layer 2 — Iterative Inquiry Synthesis

所有する:

- material delta
- touched-artifact reopen
- local / global reopen distinction
- stable artifact IDs across rounds
- question shift
- semantic delta vs representation delta
- append-only round history
- residual / reopen condition
- continue / stop / handoff reason

CSWは「新材料が来るたびに既存KJをどう再編するか」を独自に再実装しない。

### Layer 3 — Cultural Substrate Weaving

所有する:

- cultural frameworkを開く必要があるかの判断支援
- framework index / preview / native operation / depth の管理
- framework固有構造を薄めずに扱うこと
- framework-generated / cross-field-emergent / unresolved の帰属保持
- frameworkから得た問い・対比・対応候補を対象側へ戻すこと
- target-supportedへ昇格できるのは対象側材料で独立に支えられた部分だけ、という境界
- 文化体系の利用量・複雑さを成果KPIにしないこと
- no-load / preview-only / no-useful-increment 等を正常結果として扱うこと

## 2. 最小接続契約

CSWがLayer 1 / Layer 2と接続するとき、最低限次だけを要求する。

### C1. Framework output is attributed before synthesis

文化体系から返すものには、その由来が追跡できるようにする。

少なくとも必要に応じて次を区別する。

- `framework_generated`
- `cross_field_emergent`
- `unresolved`

対象側資料により独立確認された後だけ `target_supported` と区別できる。

この帰属はgrouping geometryを先に決めるための分類軸ではなく、後から元へ戻るためのepistemic / provenance informationである。

### C2. Framework output enters synthesis as material, not authority

文化体系から得た問い、仮説、対比、対応候補、構成案を、親和統合へ投入してよい。

ただし、文化体系がその対応を示したという理由だけで、既存cardより強い票・独立support・事実扱いを与えない。

体系内の整合は、対象側のcorroborationではない。

### C3. Synthesis may correct the framework reading

親和統合や後続材料が、文化体系から得た対応候補に合わない場合、対象を体系へ合わせない。

- correspondence candidateを弱める
- splitする
- withdrawする
- unresolvedへ戻す
- framework自体の選択を見直す

ことを許容する。

CSWの目的は文化体系を当てることではない。

### C4. New framework contact is a round delta

後のroundで別の文化体系、別の位置、別のnative operationから新しい候補が出た場合、過去の全材料を自動的に再生成しない。

Layer 2へ、

- 新しく得た材料／問い
- 由来
- 触れる可能性のある旧artifact
- framework contactの変更

をdeltaとして渡す。

reopen範囲の決定はLayer 2の契約へ委ねる。

### C5. Returned synthesis keeps framework attribution visible

親和統合後に自然な文章へ変わっても、framework-generatedな意味を対象由来へ遡及させない。

体系語彙を外したことと、対象証拠が増えたことを同一視しない。

必要なら次を同時に保持する。

```text
meaning: 自然言語の統合結果
origin: framework-generated / cross-field-emergent
verification: target-supported / unresolved
```

固定schemaを要求するものではない。

### C6. Representation does not become framework evidence

親和統合の図上で、framework由来cardとtarget由来cardが近接した、同じ島に入った、relationが立ったということ自体を、文化体系の妥当性の独立証拠としない。

図解は統合結果のprojectionであり、frameworkの外部検証器ではない。

### C7. No compatible synthesis realization means no false claim of execution

`affinity-synthesis` または互換realizationが導入されていない環境では、CSWは次まで実行できる。

- framework exploration
- question / hypothesis / correspondence candidate generation
- attribution preservation
- target-side verification request / handoff

ただし、KJ／親和統合を実行していないのに「KJで統合した」「親和統合済み」と称しない。

同様にLayer 2がなければ、multi-round delta orchestrationを実行済みとは称しない。

## 3. 現行ファイルの移管表

### `methods/integration.md`

ほぼLayer 1へ移管できる。

移管対象:

- カード化
- 核を抜く／伏せて立てる／戻して照合
- 束ね
- 表札
- 配置
- 叙述
- provenance / discovery route / derivation
- double-counting防止
- singleton / conflict / gap
- A/B相互検証

CSWへ残すのは、文化体系由来候補を親和統合へ渡す際の帰属境界だけでよい。

### `core/iteration.md`

大部分をLayer 2へ移管できる。

移管対象:

- material delta
- touched residual reopen
- existing islandを無理由に壊さない
- question shift
- append-only history
- stop / restart condition

CSWへ残すのは、`framework_contact_change` と、文化体系から得たものを由来を保ってround deltaへ渡す接続だけでよい。

### `core/principles-and-constraints.md`

これはCSW固有の正本として残す。

特に残す:

- 二重の忠実性
- 帰属の原則
- `target_supported / framework_generated / cross_field_emergent / unresolved`
- 対象固有性
- 保存と注意の分離
- 可能性と採用の分離
- 認知・価値・事実の分離
- 静的価値／抑制規則の高い正当化閾値

## 4. 将来のCSW runtimeに残す最小文面候補

独立Skillが安定した後、CSWのKJ接続部は概ね次の程度まで薄くできる。

```text
## 材料統合との接続

対象材料の親和統合が必要な場合は、利用可能なら `affinity-synthesis`
または同じMethod Definitionを満たすcompatible realizationへ委ねる。

文化体系から得た問い・仮説・対比・対応候補は、由来を保った材料として渡す。
それ自体をtarget-supportedな観察事実や独立supportへ昇格させない。

統合結果が文化体系の読みを支持しない場合は、対象を体系へ合わせず、
correspondenceを修正・撤回・unresolved化できる。

複数roundの再開・差分管理が必要な場合は、利用可能なら
`iterative-inquiry-synthesis` またはcompatible realizationへ委ねる。
新しいframework contactはround deltaとして渡し、新材料だけを理由に全体を再構築しない。

compatible realizationが利用できない場合は、探索候補と帰属を保持して返す。
実行していない親和統合・反復統合を実行済みとは記述しない。
```

この文面は接続契約であり、Layer 1 / Layer 2の手順をCSWへ複製しない。

## 5. 移行順序

1. Layer 1 representation / semantic regressionを継続する。
2. Layer 2 delta-reopen evalを継続する。
3. CSWと独立Skillを同一taskでpaired runする。
4. 現行 `integration.md` / `iteration.md` にしか存在しない有用挙動がないか確認する。
5. その後にCSW canonical sourceを薄くする。
6. build / validatorをmulti-skill化する。
7. 独立Skillの公開名・商標表記・英語realizationを再確認してから公開する。

## 6. 判断

現段階では、CSW側のKJ実装を削除する準備はかなり進んだが、まだ削除しない。

残すべき核は「KJを使うこと」ではなく、

> **文化体系から来たものを、対象の事実と混同せず、材料統合と反復探索へ戻せること**

である。

これを接続契約として固定できれば、CSWは文化体系探索へ集中し、親和統合と反復探索は独立して改善・置換できる。
