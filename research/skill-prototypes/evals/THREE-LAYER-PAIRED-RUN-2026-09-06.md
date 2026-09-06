# Three-layer Paired Run — CSW / Affinity / Iterative Inquiry

Date: 2026-09-06
Status: research evaluation
Evaluation type: same-model comparative authoring exercise; not an independent randomized evaluation

## Purpose

現行monolithic `cultural-substrate-weaving` が一つのSkill内部で担っている、

- cultural-framework exploration / attribution
- one-round material synthesis
- multi-round delta / reopen

を三層へ分離したとき、実運用で保持されていた意味・残差・来歴・図解・再開挙動に退行が起きないかを比較する。

比較対象:

### Baseline M — monolithic CSW

現行 `src/ja-JP` のうち主に次を一体として用いる。

- `core/principles-and-constraints.md`
- `methods/integration.md`
- `core/iteration.md`
- 必要なcultural-framework application規則

### Candidate S — split suite

- Layer 1: `affinity-synthesis`
- Layer 2: `iterative-inquiry-synthesis`
- Layer 3: `cultural-substrate-weaving`
- connection contract: `docs/ja/maintainers/csw-thin-synthesis-connection-contract.md`

最終文面の一致は要求しない。

判定軸:

1. target materialの意味・温度・具体が保持されるか。
2. framework由来候補がtarget factへ誤昇格しないか。
3. `origin` と `verification` を分離できるか。
4. 新材料が来たとき必要なartifactだけをreopenできるか。
5. derived synthesisを独立supportへ数えないか。
6. membership / relation / resonance / layoutを混同しないか。
7. narrativeがsource/mapにない因果を補わないか。
8. residual / unresolvedを消さないか。

---

# Case A — 分析系: 沖縄連載の「低抵抗 ≠ 低責任」周辺

## A0. Real baseline

既存 `affinity-synthesis/evals/PAIRED-REAL-TASK-2026-09-06.md` のCase Aを再利用する。

中心カード:

- C2334: 高圧的な説得を避け、問いと事実を置き、受け手が距離を取れる出口を残す。
- C2335: 人格全体ではなく、言い方・共有・対象の扱い等の具体的行為へ焦点を戻す。
- C2336: その場の態度変更を完了条件にせず、時間をおいた自己距離化の余地を残す。

既存paired runでは、三カードを統合したとき、

> 圧力を下げることと、責任の焦点を失うことは同じではない。

という意味が `emergent` として立ち得る一方、被害側への赦し要求を避けること、善意や信頼を先払いしないこと、謝罪・停止・是正等への接続などはC2334-C2336だけからは継承できず、周辺カードや本文との横断統合が必要と確認されている。

## A1. Added framework contact

三層接続を試すため、次のframework由来候補を追加する。

```text
F-A1
meaning:
  「即時の反応を要求しない時間差や距離が、責任回避ではなく、
   受け取ったものを自分で扱う緩衝地帯として働く場合があるのではないか」
origin: framework_generated
verification: unresolved
framework_ref: FW-A / preview-position-P
```

この追加部分はcross-layer挙動を隔離するためのfixtureであり、C2334-C2336の原カードではない。

## A2. Round 1 — Baseline M

現行monolithic CSWを厳密に適用すると、次が期待される。

1. C2334-C2336はそれぞれ異なる機能を保持したまま統合する。
2. F-A1は文化体系由来であることを消さず、target materialより高いauthorityを与えない。
3. F-A1がC2336に近くても、近接・同島・relation candidateだけで `target_supported` にしない。
4. 「低抵抗 ≠ 低責任」は三カード接触からのemergent meaningとして扱える。
5. framework contactの存在を、そのemergent meaningの独立supportとして追加計上しない。

### Baseline M candidate output

```text
G-A1:
  問いと事実を置きながら、人格全体やその場での態度変更を迫らず、
  具体的な行為へ焦点を返し、受け手が距離を取り、後から自分で
  見直せる余地を残す。

emergent:
  圧力を下げることと、責任の焦点を失うことは同じではない。

F-A1:
  origin=framework_generated
  verification=unresolved
  relation_to=G-A1 candidate / resonance
```

### Baseline M assessment

PASS.

現行CSWには、framework由来候補を対象事実へ昇格させない規則、KJ材料へ戻す規則、新材料による差分再開規則が既に存在するため、正しく適用すればcross-layer意味は保持できる。

弱点は意味そのものより**責務の所在**である。同一Skill内に統合アルゴリズム、round orchestration、framework attributionが同居するため、どの規則がどの変換を所有したかが成果物から見えにくい。

## A3. Round 1 — Candidate S

### Layer 3

F-A1を `framework_generated / unresolved` として出す。

### Layer 1

C2334-C2336とF-A1を同じ材料面で読める。ただしprovenance metadataをgrouping geometryの第一軸にしない。

安全な結果:

```text
G-A1 := {C2334, C2335, C2336}
label :=
  「問いと事実を置きながら、人格全体や即時の態度変更を迫らず、
   具体的行為へ焦点を返し、距離と後からの見直しの余地を残す」

X-A1: F-A1 ~~ G-A1
  note="framework candidate resonates with temporal-distance aspect"
```

F-A1をmembershipへ入れること自体も禁止ではないが、独立support countを増やさないことが必要である。このcaseではorigin差を監査しやすくするためsecondary resonanceとして残す。

Transformation audit:

- inherited: C2334-C2336の圧力、行為焦点、時間差。
- emergent: 「低抵抗 ≠ 低責任」。
- residual: F-A1の「緩衝地帯」というframework readingはtarget-side verification未了。

### Layer 2

Round 1 snapshotとしてG-A1 / X-A1 / F-A1の状態を保存する。

### Candidate S assessment

PASS.

Baseline Mと意味内容は実質同等で、分離後は `origin / verification / transformation provenance / realization ownership` が明示的になる。

## A4. Round 2 — derived synthesis arrives

既存の融合カードC3287のようなdownstream synthesisが比較材料へ戻ってきた場合を考える。

C3287は、C2334-C2336以外にも周辺カードや本文の監査結果を吸収した、より広い統合物である。

### Baseline M expected

正しく運用すれば、C3287をC2334-C2336と独立した新しい一次supportとして数えない。現行 `integration.md` にderivation / double-counting防止があるため、ここもPASS可能である。

### Candidate S expected

Layer 2ではC3287の到来をmaterial deltaとして記録するが、Layer 1のlineageにより `derived / wider-context synthesis` として扱う。

```text
+ D-A2 := downstream synthesis C3287
~ G-A1? := compare broader safeguards
= C2334/C2335/C2336 meaning kernels
? F-A1 verification remains unresolved unless independent target evidence is added
```

C3287がF-A1と整合することは、F-A1の独立verificationではない。

### A4 result

Candidate Sの方が、derived synthesisとindependent corroborationをartifactとして分離しやすい。

## A5. Case A comparison

| Check | Baseline M | Candidate S | Result |
|---|---|---|---|
| C2334 pressure / exit | preserved | preserved | equivalent |
| C2335 action focus | preserved | preserved | equivalent |
| C2336 time / self-distance | preserved | preserved | equivalent |
| framework origin | preservable | explicit | S clearer |
| origin vs verification | present in principle | explicit handoff state | S clearer |
| emergent meaning provenance | possible | explicit inherited/emergent/residual | S clearer |
| derived synthesis double-counting | prohibited | prohibited + lineage-friendly | equivalent / S easier to audit |
| local round reopen | required by current iteration | owned by Layer 2 | equivalent behavior |
| framework correspondence treated as evidence | prohibited | prohibited | equivalent |

### Case A decision

**PASS — no material semantic regression.**

分離の主利益は新しい意味を作ることではなく、同じ意味保存をより局所的に検査できることにある。

---

# Case B — 創作系: 『ひとりぼっちの空』の像を体系語彙へ吸収しない

## B0. Real baseline

既存paired runの実カードから、roundを二段階に分ける。

### Round 1 material

- UKJ-047: 若者が去った砂の上で、霧のように薄い「寂しい」と一緒にしばらく横たわった。
- UKJ-052: 赤子は何かをしてほしいのではなく、「この場でじっとしていたい」と頼んだ。
- UKJ-054: 食卓で泣いた子どもは身体へ溶け込み、遊びたい、楽しくしたいという薄い動きが内側に残った。
- UKJ-059: 夫婦の争いをたどった像では、温かいミルクが暗いがらんどうへ一滴ずつ溜まった。
- UKJ-063: 余白は無感覚ではなく、感じているものを埋めたり意味づけたりせず保持できる状態として描かれる。

### Round 2 delta

- UKJ-053: 暗い空間は嫌なだけではなく、少し守られている感じも含んでいた。
- UKJ-057: 小さな子は頭をなでられると腰へしがみついたが、触れた手にはちくちくする感じが残った。
- UKJ-055: うさぎは中心のテーブルへ立ちながら、目と口を点のまま保ち、薄く張りつめていた。

## B1. Added framework contact

Round 1で文化体系をpreviewした結果、次の対応候補が生じたとする。

```text
F-B1
meaning:
  「暗い空間、ミルク、余白の像を、何かを急いで満たさず保持する
   『器』の象徴として読むことはできないか」
origin: framework_generated
verification: unresolved
framework_ref: FW-B / vessel-like correspondence candidate
```

このfixtureの狙いは「器」というきれいな語が、原カードの砂、寂しさ、赤子、暗いがらんどう、一滴ずつという具体を上書きしないかを見ることである。

## B2. Round 1 — Baseline M

現行CSWを厳密に用いれば、文化体系をKJの分類軸へ固定せず、元材料へ戻すため、次のような統合が可能である。

```text
G-B1:
  何かを直すより先に、薄い感覚と一緒にその場にいられる時間がある。
  members: UKJ-047, UKJ-052, UKJ-063

G-B2:
  暗い／泣いていた内側には、すぐ満たし切らず、小さな温かさや
  遊びたい動きが少しずつ残っていく。
  members: UKJ-054, UKJ-059

F-B1:
  framework-generated correspondence candidate
  not a replacement label for G-B1/G-B2
```

PASS条件は、G-B1やG-B2を単に「器」「受容」「癒やし」へ改名しないことである。

### Baseline M assessment

PASS可能。

現行CSWにも「文化体系をKJの分類軸として機械的に固定しない」「体系由来候補を対象へ戻す」という規則があるため、正しく適用すれば像を保持できる。

ただし、同じSkill文脈内にframework interpretationとKJ表札生成が同居するため、実行AIが `F-B1 -> group label` を近道として使う危険は残る。これは現行規則違反だが、責務分離後よりも構造的に近接している。

## B3. Round 1 — Candidate S

### Layer 3

F-B1をframework candidateとして出し、target materialと区別する。

### Layer 1

先にtarget materialだけからgroupを立てる必要はないが、F-B1を分類名として先置きしてはならない。

安全なgroupingはBaseline Mと同等である。

```text
G-B1 := {UKJ-047, UKJ-052, UKJ-063}
label := 「何かを直すより先に、薄い感覚と一緒にその場にいられる時間がある」

G-B2 := {UKJ-054, UKJ-059}
label := 「暗い／泣いていた内側には、すぐ満たし切らず、小さな温かさや遊びたい動きが少しずつ残っていく」

X-B1: F-B1 ~~ G-B1
X-B2: F-B1 ~~ G-B2
```

ここで `~~` はsecondary resonanceであり、F-B1が二つのgroupのmemberまたは二票のsupportになったことを意味しない。

### Candidate S assessment

PASS.

「器」は探索候補として残るが、target-led labelを置き換えない。

## B4. Round 2 — ambivalent target material arrives

UKJ-053 / UKJ-057 / UKJ-055を新材料として追加する。

### What the delta says

- UKJ-053は暗い空間に「嫌さ」と「少し守られる感じ」が同居する。
- UKJ-057はしがみつきと、触れた手の「ちくちく」が同居する。
- UKJ-055は中心へ出る動きと、薄く張りつめた状態が同居する。

これらは「器＝安全に保持するもの」という読みを単純化させない。

### Baseline M expected

現行 `iteration.md` に従えば、既存全体を無理由に作り直さず、触れた島・残差を再検査する。

F-B1は、

> 「保持する器」

という単線的な読みから、

> 「保持されるように見える空間にも、嫌さ・ちくちく・張りつめが残り、保護と不快を一つへ均せない」

程度へ弱めるか、複数のcorrespondenceへsplitする必要がある。

### Candidate S handling

Layer 2:

```text
+ UKJ-053
+ UKJ-057
+ UKJ-055
~ G-B1?  # nearby meaning rechecked
~ G-B2?  # dark/interior imagery rechecked
~ F-B1   # framework correspondence weakened / split candidate
+ G-B3   # if grouping supports it
? UKJ-055 relation remains partly unresolved
```

Layer 1で新材料を読むと、既存paired runと同様に次の意味単位が安全である。

```text
G-B3 := {UKJ-053, UKJ-057}
label := 「近づくことや守られることの中にも、嫌さやちくちくする感覚が一緒に残る」

S-B4 := UKJ-055
label := 「中心へ出ても、うさぎはまだ薄く張りつめている」
```

F-B1はG-B3によって反証されたというより、**単線化が耐えられなくなった**と扱うのが適切である。

可能な更新:

```text
~ F-B1:
  old: 「暗い空間等を、保持する『器』として読めないか」
  new: 「保持／保護に見える像と、不快・緊張が同居する境界を、
        『器』という一語で潰さずに見られるか」
  origin: framework_generated
  verification: unresolved
```

または旧F-B1をwithdrawし、新しいframework questionへ分けてもよい。

### Narrative check

安全なB型叙述は、

- 砂の上の薄い寂しさ
- 赤子の「ここにいたい」
- 暗いがらんどうへ一滴ずつ溜まるミルク
- 暗い場所の嫌さと少し守られる感じ
- しがみつきと手のちくちく
- 中心へ出ても張りつめるうさぎ

を概念語の例示へ格下げしない。

禁止する短絡:

```text
「これらはすべて『器』が人を癒やしていく過程を表している」
```

元材料はそこまで言っていない。

## B5. Case B comparison

| Check | Baseline M | Candidate S | Result |
|---|---|---|---|
| sensory detail | preservable | preserved by Layer-1 contract | equivalent |
| ambiguous protection/discomfort | preservable | explicit residual / new group | equivalent / S clearer |
| framework word becomes group label | prohibited | structurally separated | S lower risk |
| later delta causes full restart | prohibited | Layer 2 local reopen | equivalent |
| UKJ-055 forced into existing group | prohibited | singleton retained | equivalent |
| framework reading can weaken | allowed | explicit changed/withdrawn state | S clearer |
| framework origin after rewrite | preservable | stable origin metadata | S clearer |
| diagram proximity as verification | prohibited | representation contract explicit | S clearer |
| narrative overconceptualization | prohibited | source↔map↔narrative check explicit | equivalent / S easier to audit |

### Case B decision

**PASS — no material semantic regression.**

分離後も創作材料の「土の匂い」を保持できる。むしろframework candidateをLayer 3に置き、grouping / label生成をLayer 1へ分けることで、文化体系語彙が表札へ先回りする経路を狭くできる。

---

# Cross-case result

| Regression axis | Case A | Case B | Overall |
|---|---|---|---|
| target meaning loss | none found | none found | PASS |
| source temperature loss | none material | none found | PASS |
| framework authority leak | none under contract | none under contract | PASS |
| origin / verification collapse | none | none | PASS |
| derived support double-counting | avoided | n/a | PASS |
| residual loss | avoided | avoided | PASS |
| local reopen behavior | preserved | preserved | PASS |
| stable semantic handle feasibility | yes | yes | PASS |
| map / narrative drift | controlled | controlled | PASS |
| framework vocabulary overreach | controlled | lower structural risk after split | PASS |

## Main finding

三層分離によって新しい認知能力が増えた、とはまだ言わない。

今回確認できたのは次である。

> **現行CSWがすでに持っている意味保存上の良い挙動を、Layer 1 / Layer 2 / Layer 3へ責務分離しても、二つの実材料系で再現できる。**

さらに分離後は、

- one-round synthesisの失敗
- round orchestrationの失敗
- framework attributionの失敗

を別々に観測しやすくなる。

## Cost / new risk introduced by the split

分離には利点だけでなく新しい負担もある。

1. handoff metadataが増え、短いtaskでは冗長になり得る。
2. `origin / verification / realization / stable ID` を前景化しすぎると、創作材料の読解が管理作業へ傾く。
3. Layer境界を守ること自体が目的化すると、自然な往復を阻害する。

したがって、これらは**保存・監査層では厚く、現在の注意では必要なものだけ前景化する**。

## Migration decision

**Proceed to a thin-CSW migration candidate.**

ただし、現行canonical sourceを即座に削除するのではなく、次を先に行う。

1. `methods/integration.md` からLayer 1へ移管できる節を具体的に列挙し、CSW側replacement textを作る。
2. `core/iteration.md` からLayer 2へ移管できる節を列挙し、framework-contact接続だけを残すreplacement textを作る。
3. `core/principles-and-constraints.md` はCSW固有の正本として維持する。
4. thin candidateを現行monolithic sourceと対照し、消失する独自挙動がないか最後のmigration auditを行う。
5. その後にresearch branch上でcanonical sourceを置換する。

このpaired runだけを公開releaseの妥当性証明とはしない。英語realization、build生成物、既存テスト、外部Skill互換性は別gateである。
