# External Skill Format Adoption Audit — 2026-09-07

Status: research evidence / realization-format audit

## Purpose

`affinity-synthesis` の方法核を既存Skillへ置き換えるのではなく、既存公開Skillの**成果物書式・監査UI・Skill packaging上の長所**を選別して取り込む。

今回比較した主対象:

- product-on-purpose `think-affinity-mapping`
- product-on-purpose `think-concept-mapping`

方法論の系譜や妥当性評価とは別に、Agent Skillとして「何をどう出力すれば人間と別agentが検査しやすいか」を見る。

## 1. Affinity Mappingから採用したもの

### 1.1 Cluster before naming

既にLayer 1 runtimeへ採用済み。

分類名を先に作らず、材料の訴えを先に読む。

### 1.2 Traceability

既にsource/card/group lineageとして強化済み。

外部Skillの「themeへsource itemを追跡できる」という長所を、こちらではさらに source provenance / discovery route / derivation / independence まで分ける。

### 1.3 Explicit outliers

外部Skillの `outliers / parking lot` は、こちらの singleton / residual / unresolved と整合する。

ただし「駐車場」という一時保留だけにせず、後のroundで再開可能なsemantic artifactとして扱える。

### 1.4 Reader-facing summary above detail

2026-09-07に標準templateへ採用。

外部Skillは詳細theme tableの前に短い summary を置き、読者がそこで全体像を把握できる。

こちらでは先入観形成を避けるため、同じ構造をそのまま前処理には使わず、

```text
full synthesis / return-check
        ↓
reader-facing overview projection
```

として**最後に生成する**。

summary-only readerにも singleton / conflict / unresolved / borderline relation が見えるようにする。

### 1.5 When to Use / When NOT to Use, output contract, evidence dossier

方法核ではなくAgent Skill realization品質として採用済み。

## 2. Affinity Mappingから採用しなかったもの

### 2.1 Fixed small-item cutoff

「十数件以下なら使わない」のような固定閾値は採用しない。

少数でも意味境界・証拠状態・対立を丁寧に統合する必要があれば適用できる。

### 2.2 Theme weight H/M/L as default semantic field

採用しない。

- group size != truth
- repetition != independent support
- importanceは問い・目的・文脈で変わる
- 少数・singletonが決定的な反証であることもある

標準overviewには `Member count` を記述値として置けるが、truth / importance / independent supportを意味しないと明示する。

### 2.3 Representative items as substitute for full lineage

採用しない。

読者向けoverviewではanchor refsを置けるが、それはnavigation用であり、完全membership / lineageの代替ではない。

## 3. Concept Mappingから採用したもの

### 3.1 Relation proposition read-back

2026-09-07にRepresentation Grammarへ採用。

Concept Mappingの強みは、強いsemantic linkを単なる線で残さず、source-link-targetを一文として読み返すことで曖昧なrelationを露出させる点にある。

こちらでは固定concept-node methodへ変換せず、**明示的な `R` relationだけ**について、

```text
source meaning unit + predicate + target meaning unit
```

を監査時に一文として読み返す。

確認対象:

- directionとpredicateが噛み合うか
- 因果・意図・一般化・責任方向を補っていないか
- basisへ戻って支持できるか
- stateが過剰に強くないか

read-back文はcanonical semantic fieldへ重複保存する必須値ではなく、監査操作である。

### 3.2 Questionable propositions

Concept Mappingの `questionable propositions` は、こちらでは既存`R`のread-back auditとして採用する。

支持できなければ:

- stateを弱める
- relationを修正する
- withdrawする
- まだ気になるなら`Q`へ戻す

### 3.3 Missing links / gaps

「関係がありそうだが未確認」という気づきを、確定edgeとしては採用しない。

こちらでは:

```text
Q07? := "G02 と G05 の間に接続があるか"
```

のようなquestionable / missing relation candidateとして保持する。

`Q`はrelation assertionではない。

## 4. Concept Mappingから採用しなかったもの

### 4.1 All nodes as concepts / noun phrases

採用しない。

材料の具体・身体感覚・出来事・発話・場面を早期にconceptへ縮約すると、KJ系の「土の匂い」を失う。

### 4.2 Every connection must be a directed proposition

採用しない。

こちらでは:

- membership
- explicit relation
- secondary resonance
- layout

を別物として保持する。

空間的な近接・離隔、secondary resonance、上位group membershipは必ずしも命題ではない。

### 4.3 Cross-links are inherently highest-value

採用しない。

別clusterをまたぐrelationが重要な場合はあるが、cross-clusterであること自体をimportanceへ変換しない。

### 4.4 Fixed relation vocabulary

採用しない。

`causes / depends on / constrains ...` 等は例にはできるが、relation predicateを固定taxonomyへ押し込めない。

## 5. Resulting output stack

現在のLayer 1成果物は次の順で読める。

```text
Reader-facing Overview  ← 完了後に生成するprojection
        ↓
Group / Relation inventories
        ↓
Diagram projection(s)
        ↓
Narrative synthesis
        ↓
Return / cross-check
        ↓
Full cards / lineage / residual audit
```

保存上の正本順序を意味しない。reader-facing viewとaudit detailを分けるための閲覧順である。

semantic source of truthは引き続き、sourceへ戻れるcard/group/relation/residual/lineage recordである。

## 6. Key non-import rule

既存Skillから借りるのは、

- inspection affordance
- output readability
- explicit failure visibility
- progressive disclosure

である。

既存Skill固有のmethod assumptionsを、書式を通じて無言で輸入しない。

特に:

```text
format convenience
    != epistemic rule
    != grouping geometry
    != evidence weight
```

を維持する。

## Current conclusion

既存Skillの書式比較により、Layer 1は次の点で改善した。

- summaryを詳細と分離しつつresidualを残す
- relationを読める命題として監査できる
- questionable relationとmissing-link suspicionを問いとして保持できる
- outlier / singletonを消さない
- traceabilityをsourceまで辿れる

一方、固定weight、全relation命題化、cross-link重要度、concept-first abstractionは導入しない。
