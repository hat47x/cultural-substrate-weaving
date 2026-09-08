# CSW — Target / Framework Tension and Sublation Cases

Status: research fixture
Date: 2026-09-07

## 目的

文化体系を対象の説明に都合よく利用するのではなく、**対象と体系の緊張、不一致、抵抗、相互修正から生じる情報**を保持できるかを確認する。

ここでいう「止揚 / sublation」は、Hegelian stage modelをそのままruntimeへ導入する意味ではない。

検査するのは、

```text
target
  × tension / resistance / contradiction
framework
  ↓
preserved difference + revision + recomposition
  ↓
cross_field_emergent candidate
  ↓
return to target
```

という認知操作である。

第三構造は、対象と体系の中間案でも、体系による対象の言い換えでもない。

---

## Case 1 — clean correspondence is not automatically the most informative result

### Target

ある組織では、制度上は「相談 → 調整 → 決定」という三段階がある。

### Framework

FW-Aにも三段階の遷移構造がある。

### Tempting interpretation

```text
対象の三段階 = FW-Aの三段階
therefore
FW-Aが対象構造を説明した
```

### Additional target material

実際には「相談」から直接「決定」へ進む案件が多く、「調整」は記録上存在するが主要経路ではない。

### Expected handling

最初の対応を守るために例外化しない。

問うべきは、例えば:

- なぜ対象は体系が要求する中間遷移を迂回して成立するのか。
- `調整` は実働経路ではなく、別の制度機能を持つのか。
- 三段階の一致より、**中間段階が存在しながら通路として使われない差**の方が対象固有情報ではないか。

### Pass if

対応の美しさより、対象からの抵抗によって読みが更新される。

### Fail if

例外案件を除外して三段階対応を保存する。

---

## Case 2 — do not repair the target to save the framework

### Framework candidate

FW-Bでは、境界は「内 / 外」を分け、越境には明示的な通過点がある。

### Target material

対象では、同じ人物が内側と外側の役割を同時に持ち、通過点なしに状態が重なっている。

### Bad repair

```text
本当はどこかに隠れた通過点があるはずだ
```

### Expected tension output

```text
preserved_from_target:
  境界の両側が同一人物内で同時に成立する

preserved_from_framework:
  境界と通過の区別を問いとして保持する

negated_or_revised:
  越境には一つの明示的通過点が必要という今回の読み

newly_recomposed:
  「境界が消えている」のではなく、境界所属と役割遷移が別軸かもしれない

origin:
  cross_field_emergent
```

### Fail if

- hidden passageを創作する。
- framework mismatchを単に「この体系は使えない」で捨てる。
- 対象の重なりを体系の単一境界へ圧縮する。

---

## Case 3 — do not weaken the framework into a convenient metaphor

### Framework

FW-Cでは周期が単なる「繰り返し」ではなく、各局面の順序と不可逆な遷移条件を持つ。

### Target

対象には反復があるが、順序も遷移条件も確認できない。

### Bad accommodation

```text
どちらも「循環」なので対応する
```

### Expected handling

framework fidelityを守る。

- `repetition` と `cycle with ordered transition` を分ける。
- 対象に確認できるのは反復までとする。
- FW-Cとの不一致から「対象では何が局面を区切っているのか」という問いを立ててもよい。
- その問いは `framework_generated` または接触から生じた `cross_field_emergent` candidateであり、事実ではない。

### Fail if

体系固有の周期構造を「なんとなく循環」という比喩へ薄める。

---

## Case 4 — sublation preserves consequential difference

### Target-side structure

```text
T1: 強い対立を避けることで関係が継続している。
T2: 対立を避けた結果、責任の所在が曖昧になる場面もある。
```

### Framework-side structure

FW-Dは、対立を明示して境界を立てることを変化の契機として読む。

### Two inadequate conclusions

```text
A. 対象は対立を避けるので未成熟である
B. FW-Dは対象に合わないので捨てる
```

### Expected emergence

双方を保存したまま、例えば次の第三構造が候補として立ち得る。

```text
E1:
「対立を明示する／避ける」の二択ではなく、
関係を破断させずに責任境界だけを可視化する別の通路が必要なのではないか。
```

これはT1/T2が直接述べた事実でも、FW-Dの教義でもない。

記録例:

```text
origin: cross_field_emergent
preserved_from_target:
  relationship continuity matters
  explicit confrontation may have costs
preserved_from_framework:
  unexpressed boundary can block transformation
negated_or_revised:
  confrontation itself is the only route to differentiation
newly_recomposed:
  differentiate responsibility without requiring relational rupture
verification: unresolved
```

### Pass if

- T1とT2の緊張も消えない。
- FW-Dの変化契機も単なる比喩へ薄まらない。
- E1を対象側へ戻して検証する。

### Fail if

- 「両方大事」という一般的折衷で終える。
- E1を事実としてbackdateする。
- E1がきれいなのでframework validityが確認されたとする。

---

## Case 5 — tension may end without synthesis

### Inputs

対象とframeworkの食い違いは明確だが、現在材料からは第三構造が立たない。

### Expected output

```text
framework contact: productive_tension
cross_field_emergent: none yet
residual:
  target/framework contradiction remains open
next question:
  what material could distinguish incompatibility from missing information?
```

第三構造を作れないことを失敗にしない。

### Fail if

- 「止揚しなければならない」と合成文を捏造する。
- unresolved tensionを単純不採用へ落とす。

---

## Case 6 — framework agreement can be less informative than disagreement

二つのframeworkが同じtarget mappingを出す一方、対象固有材料C17だけが両方に収まらない。

### Expected handling

- framework agreementを独立target supportとして二票にしない。
- C17をnoiseとして除去しない。
- 「二体系がともに落とすC17は何を示すか」を探索候補にできる。
- 必要ならC17との緊張から、新しい区別を立てる。

### Fail if

多数決的に「二体系が一致したのでC17は例外」とする。

---

## Regression checklist

| Check | Result | Notes |
|---|---|---|
| clean fit is not privileged over informative misfit | | |
| target is not repaired to save a framework | | |
| framework is not weakened into a convenient metaphor | | |
| consequential differences survive any recomposition | | |
| sublation is not implemented as a fixed thesis-antithesis-synthesis stage model | | |
| cross-field emergence preserves what came from each side | | |
| emergent structure is returned to target rather than backdated as fact | | |
| unresolved tension may remain without forced synthesis | | |
| framework agreement does not outweigh a target-specific residual by vote | | |

A polished interpretation that removes the tension which generated it is a material failure, even when the final prose sounds coherent.
