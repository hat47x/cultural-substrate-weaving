# 材料統合との接続

多数・異種の材料から、既存の分類軸を先に置かずに構造を立ち上げる必要があるときに読む。

この文書は親和統合そのものを実装しない。CSWは文化体系探索と帰属保持を担当し、材料統合の内部手順は専用Method / compatible realizationへ委ねる。

## 責務境界

対象材料の親和統合が必要な場合は、利用可能なら `affinity-synthesis` または同じMethod Definitionを満たすcompatible realizationを用いる。

材料統合側へ委ねるもの:

- meaning-bearing card boundary
- epistemic seam
- grouping / higher-order grouping
- label / 表札
- singleton / conflict / residual
- relational structure
- membership / relation / secondary resonance / layoutの区別
- source return check
- inherited / emergent / residual transformation audit
- diagram ↔ narrative check
- provenance / derivation lineageと二重計上防止

CSWはこれらの内部アルゴリズムを独自に再実装しない。

## 文化体系から渡すもの

文化体系から生じた問い、仮説、対比、対応候補、構成候補は、由来を保った材料として親和統合へ渡してよい。

必要に応じて少なくとも次を区別できるようにする。

- `framework_generated`
- `cross_field_emergent`
- `unresolved`
- 対象側材料で独立に支えられた場合の `target_supported`

この帰属情報はgrouping geometryの第一軸ではない。後から対象・文化体系・接触由来を区別して戻るための情報である。

文化体系由来候補は、文化体系が示したという理由だけでtarget materialより強い票、独立support、事実statusを持たない。

体系内の整合、親和統合での同島、図上の近接、secondary resonance、explicit relationの成立は、それだけでは対象側の独立corroborationにならない。

### 緊張から生じた第三構造を渡すとき

`cross_field_emergent` な候補だけを、完成した統合文として単独で渡さない。

可能な範囲で、少なくとも次の三者を追跡できるようにする。

```text
target_side_tension:
framework_side_claim_or_operation:
cross_field_candidate:
```

必要ならさらに、

```text
preserved_from_target:
preserved_from_framework:
negated_or_revised:
newly_recomposed:
```

を持たせる。

これはLayer 1に弁証法や文化体系処理を実装させるためではない。**第三構造が何との緊張から生じたのかを失わず、親和統合がその緊張自体も材料として扱えるようにするため**である。

Layer 1は、`cross_field_candidate` を特権的な上位表札として扱わない。対象側の抵抗、体系側の読み、第三候補を必要に応じて別々のmeaning-bearing unitとして保持し、そこから改めて材料主導で統合する。

## 統合結果を受け取る

親和統合から結果が返ったら、CSWは少なくとも次を混同しない。

1. 対象材料から支持された意味。
2. 文化体系から来た問い・対応候補。
3. 両者の接触で新しく立った意味。
4. まだ帰属・確度・有用性を置けない残差。

自然な文章へ統合され、体系語彙が外れた場合も、framework由来の意味を対象材料が最初から述べていたことへ遡及させない。

必要なら、意味内容と由来・検証状態を別に保持する。

```text
meaning: <統合後の自然言語>
origin: framework_generated | cross_field_emergent | target-side material lineage
verification: target_supported | unresolved | other explicit state
```

固定schemaではない。

第三構造が親和統合の中でさらに変化した場合も、元のtarget/framework tensionへ戻れるlineageを残す。統合後の文が滑らかになったことを理由に、緊張の履歴を削除しない。

## 文化体系の読みを修正できる

親和統合または後続の対象材料が文化体系由来の対応候補を支えない場合、対象を体系へ合わせない。

- correspondenceを弱める
- splitする
- withdrawする
- unresolvedへ戻す
- 別のframework contactへ開き直す

ことを許容する。

CSWの目的は、文化体系を対象へ当てはめ切ることではない。

不一致によって体系の読みが修正された場合、その修正自体が探索上の情報になり得る。体系が「外れた」という一語だけで捨てず、何を前提にした読みが対象によって崩れたかを必要に応じて残す。

## compatible realizationがない場合

`affinity-synthesis` またはcompatible realizationが利用できない環境では、CSWは次まで行える。

- framework exploration
- framework-generated question / hypothesis / correspondence candidate
- attribution / provenance preservation
- target-side verification question
- handoff materialの整理

ただし、実行していないKJ／親和統合を「実行済み」と記述しない。

単純な要約・固定分類で代用した場合も、それを親和統合と称しない。

## 最小handoff

材料統合へ渡すときは、現在のtaskに必要な範囲で次を含める。

- synthesis subject / current purpose
- target-side material refs
- framework-generated / cross-field candidatesとその由来
- cross-field candidateが緊張から生じた場合のtarget/framework双方の参照
- 既知のresidual / conflict / unresolved
- 監査上必要なprovenance / derivation

全履歴を毎回複製する必要はない。

## CSW固有の正本

この接続より上位の原則は `core/principles-and-constraints.md` に置く。

特に次はCSW側に残す。

- 二重の忠実性
- 帰属の原則
- 対象と体系の緊張から生じる第三構造の来歴
- 対象固有性
- 保存と現在の注意の分離
- 可能性と採用の分離
- 認知・価値・事実の分離

材料統合Methodの内部手順をCSWへ再複製しない。
