# CSW → Affinity Synthesis → Iterative Inquiry Handoff Cases

Status: research fixture
Date: 2026-09-06

## Purpose

このfixtureは、三つのSkillを分離した後も、文化体系から得たものが対象事実へ誤昇格せず、親和統合と複数round探索へ安全に受け渡せるかを確認する。

対象とする契約:

- CSW: cultural-framework exploration and attribution
- Affinity Synthesis: one-round material synthesis
- Iterative Inquiry Synthesis: multi-round delta / reopen orchestration

評価の中心は、三Skillを必ず全部使うことではない。**各Layerが自分の責務だけを持ち、境界を跨ぐときに意味・来歴・認識状態を壊さないこと**である。

---

## Case 1 — framework candidate enters synthesis as material, not authority

### Target material

```text
T1: 会議中、本人はその場では返答しなかった。
T2: 二日後、本人は指摘された具体的行為について修正案を提出した。
```

ここから直接言えるのは、返答と修正案提出の時間差があったことまでである。

### CSW output

文化体系との接触から、次の問い／対応候補が生じたとする。

```text
F1 meaning:
「即時に反応しない時間差が、拒絶ではなく、受け取ったことを内側で扱う緩衝地帯として働く場合があるのではないか」

origin: framework_generated
verification: unresolved
framework_ref: FW-A / position-P
```

### Expected Layer-1 handling

F1は親和統合の材料として読んでよい。

T1/T2と意味上近ければ、同じgroupへ置くことも、secondary resonanceを引くことも、relation candidateを立てることもできる。

しかし、次は禁止する。

```text
F1 + T1 + T2 が同じ島に入った
    therefore
「時間差は緩衝地帯だった」とtarget-supported fact化する
```

同じ島に入ることは、F1の外部検証ではない。

### Pass if

- F1の`origin=framework_generated`が保持される。
- `verification=unresolved`のままでもgroupingできる。
- cluster membership / proximity / relation projectionをcorroboration countへ変換しない。

### Fail if

- framework由来であることを理由にF1へ高い重みを置く。
- groupに入ったことを対象事実の証明にする。
- 自然言語へ言い換えた瞬間にframework originを消す。

---

## Case 2 — target evidence can verify a meaning without rewriting its origin

### Prior state

F1:

```text
origin: framework_generated
verification: unresolved
meaning: 「時間差が緩衝地帯として働く場合があるのではないか」
```

### New target-side material

後のroundで、対象本人の記録T3が得られた。

```text
T3: 「その場では頭がいっぱいで答えられなかった。二日置いたことで、何を直せばよいか考えられた。」
```

### Expected Layer-2 handling

T3をmaterial deltaとして受け取り、F1に触れる旧artifactだけをreopenする。

### Expected attribution after return-to-source

次のような二軸保持を許容する。

```text
meaning: 「この事例では、時間差が具体的な修正を考える余地として働いた」
origin: framework_generated              # 問いを生んだ経路は変わらない
verification: target_supported           # 対象側材料が独立に支えた
verification_basis: T3
```

または、対象側から別にtarget-supported cardを立て、F1とのcorrespondenceを記録してもよい。

重要なのは、**検証されたからといってF1のoriginを`target_generated`のように書き換えないこと**である。

### Fail if

- 後のT3を、F1が最初から事実だった証拠として過去roundへ遡及させる。
- T3が届いたため全materialを無理由に全面再clusterする。
- framework contact自体をT3と独立した二つ目のsupportとして数える。

---

## Case 3 — target evidence may refute the framework reading

### Prior candidate

```text
F2 meaning: 「沈黙は、内側で統合するための余白かもしれない」
origin: framework_generated
verification: unresolved
```

### New target-side material

```text
T4: 本人は後日の聞き取りで「内容は理解していたが、反論すると不利益があると思って黙った」と述べた。
```

### Expected handling

対象をF2へ合わせない。

可能な処理:

- F2をwithdraw / weakenedにする。
- 「沈黙」という観察と「余白」というframework readingをsplitする。
- 新しいtarget-supported cardを立てる。
- framework correspondenceを`not supported here`または`unresolved`へ戻す。

### Fail if

- 「本人はそう感じていても深層では余白だった」等、体系を守るために対象の発言を上書きする。
- framework native meaningを対象事実より上位の説明へ置く。

---

## Case 4 — cross-field emergence is neither source fact nor pure framework output

### Inputs

```text
T5: 対象材料では、制度上の選択肢があるにもかかわらず利用されていない。
F3: 文化体系から「境界は存在しても、通路として機能していない」という見方が生じた。
```

親和統合で別材料と配置した結果、次が初めて立ったとする。

```text
E1: 「制度上の選択可能性と、実際に通れる心理的・運用的な通路は別である」
```

### Expected attribution

E1は、T5の単なる言い換えでもF3の単純転写でもない。

必要なら:

```text
origin: cross_field_emergent
verification: partially_target_supported / unresolved
basis: [T5, F3, ...]
```

として扱う。

`cross_field_emergent`は自動的に高価値・正しいという意味ではない。

### Fail if

- E1を元資料T5が最初から述べていたことにする。
- E1をframework固有教義として扱う。
- emergenceが起きたこと自体をframeworkの妥当性証明にする。

---

## Case 5 — diagram proximity is not external validation

### Map state

- target-supported group G1
- framework-generated card F4
- F4はG1の近くへ配置され、secondary resonance X4もある。

### Expected handling

次を区別する。

```text
layout proximity     != explicit relation
secondary resonance  != membership
membership           != target verification
explicit relation    != independent corroboration
```

図を見て新しい問いが生じることは許容する。その問いは次round candidateであり、現在の事実へ昇格しない。

### Fail if

- 「図上で中心に近いので重要」と対象事実へ変換する。
- automatic layoutの位置をframework correspondenceの証拠にする。

---

## Case 6 — a later framework contact is a round delta, not a restart

### Prior state

Round 3までにG1〜G8が安定している。

### New CSW contact

別framework FW-Bのnative operationから、G6と未解決Q2にだけ触れる候補F5が生じた。

### Expected Layer-2 handling

```text
+ F5 :: framework-generated material from FW-B
~ G6? :: reopen candidate
? Q2 :: reopen candidate
= G1,G2,... :: do not enumerate unless actually checked/touched
```

G6/Q2への波及から全体前提が崩れると判明した場合だけ、reopen範囲を広げる。

### Fail if

- 新frameworkを開いたという理由だけで全cardを再統合する。
- FW-Bの候補を既存structureへ無理に割り当てる。

---

## Case 7 — framework contact can produce no useful increment

### CSW result

frameworkをpreview / probeしたが、対象側へ戻す新しい問い・対比・残差が出なかった。

### Expected handling

正常な結果として、例えば次を記録できる。

```text
framework contact: no_useful_increment
Layer-1 material delta: none
Layer-2 reopen: none
```

### Fail if

- frameworkを使った以上、何か洞察を作らなければならないと補う。
- round数やframework利用数を成果にする。

---

## Case 8 — absence of Layer 1 must not be hidden

### Environment

CSWは利用可能だが、`affinity-synthesis`も互換realizationもない。

### Expected CSW output boundary

CSWは次まで可能:

- framework exploration
- framework-generated question / candidate
- provenance / attribution
- target-side check proposal / handoff

しかし次の表現は禁止する。

```text
「KJで統合した結果…」
「親和統合によりこの島が立った…」
```

実際にそのrealizationを実行していないためである。

---

## Case 9 — absence of Layer 2 must not simulate multi-round governance

### Environment

CSW + Layer 1は利用できるが、Layer 2互換realizationがない。

### Expected handling

一回の親和統合結果と、次に確認できる残差・問い・戻り先を返すことはできる。

ただしappend-only round historyやtouched-artifact reopenを運用していないのに、multi-round contract準拠と称しない。

---

## Case 10 — method-realization comparison must not become framework evidence

同じCSW outputを二つのLayer-1 realizationで統合したところ、一方だけF6とG3のrelationを立てた。

### Expected handling

これはまずrealization差である。

- sourceへ戻す。
- relationのbasisを比較する。
- framework妥当性の追加supportとして数えない。
- paired realization comparisonとして記録する。

### Fail if

- 二つのAIのうち一つがrelationを描いたことを、対象事実またはframework妥当性の証拠にする。

---

## Cross-layer regression checklist

| Check | Result | Notes |
|---|---|---|
| framework origin preserved through Layer 1 | | |
| origin and verification remain separable | | |
| framework material gets no authority bonus | | |
| target refutation can weaken/withdraw framework reading | | |
| cross-field emergence not backdated to source | | |
| diagram proximity not treated as evidence | | |
| later framework contact handled as delta | | |
| no-useful-increment can terminate without fabrication | | |
| missing Layer 1 is honestly surfaced | | |
| missing Layer 2 is honestly surfaced | | |
| realization differences do not become world evidence | | |

A single origin/verification collapse or unsupported target-fact promotion is a material failure and must not be offset by readability or elegance elsewhere.
