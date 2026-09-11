# Experiment 001 — Run 001 engineering trial

- experiment id: `PQ-E3-001`
- run id: `PQ-E3-001-R001`
- executed: 2026-09-11
- run type: controlled engineering trial
- method baseline: `develop/v0.5.0@f4370bea759fcb83a4eeae352b325f8feaea39d5`
- protocol branch commit before run: `4d7b114d30779a5865200f158fb30bad87ff9f81`
- visible model: GPT-5.6 Sol
- reasoning mode: High
- surface: ChatGPT web
- repository tool: GitHub connector
- evaluator provenance: same AI execution context; **not an independent evaluator**

## 1. Run boundary

`experiment-001-handoff-integrity.md`の固定packetを使い、次の現行定義を基準commitから読み直して実行した。

- `src/ja-JP/ROUTER.md`
- `research/skill-prototypes/affinity-synthesis/SKILL.md`
- `research/skill-prototypes/iterative-inquiry-synthesis/SKILL.md`

目的はMethodの優越性を証明することではない。protocolが実行可能であり、三段階のhandoffでH1〜H6を外部artifactとして検査できるかを確認する。

### 交絡

- protocolの作成と実行を同じAI・同じ会話文脈で行った。
- H1〜H6を実行モデル自身が事前に見ている。
- fresh-session / blinded executionではない。
- human independent reviewを行っていない。

したがって、このrunのpassは自然な遵守率の強い証拠ではない。主に**handoff contractと実験packetの実行可能性**を見るengineering evidenceとして扱う。

## 2. Stage A — CSW exploration

### Current inquiry

情報を増やす／減らすという二択へ早く収束せず、来館者が展示物を見る時間を支えるために、現在の材料から何を言え、何がまだ候補・未解決なのかを分ける。

### Handoff inventory

| ID | 内容 | status |
|---|---|---|
| A-T1 | 18件中11件で、説明を読むことに気を取られ展示を見る時間が短くなったという趣旨 | target-supported |
| A-T2 | 入口長文パネルを読む一部来館者が最初の展示ケースをほぼ見ず通過 | target-supported |
| A-T3 | 学芸員2名は一律な説明増加にも全面削減にも慎重 | target-supported |
| A-T4 | 問いカード3種の利用差は大きいが理由は未調査 | target-supported + unresolved cause |
| A-T5 | 外国語利用者への聞き取りは未実施 | target-supported observation gap |
| A-R1 | 常連1名は説明が多いほど安心すると回答 | target-supported singleton / possible counterexample |
| A-R2 | 問いカード不使用の原因は内容・配置・非認知の間で未分解 | unresolved |
| A-R3 | ガイド媒体は未決定 | author-pending decision |
| A-F1 | 展示空間を「展示物との間に余白をつくる場」とみる | framework-generated candidate |

A-F1から「来館者は余白を求めている」とは記述しない。材料間には説明との接触、情報量への異なる反応、問いカードの利用差、観測空白があるため、one-round synthesisを`affinity-synthesis`へ委ねる。`target-supported / framework-generated / unresolved / author-pending`を維持し、A-F1をgrouping authorityとして使わない。

## 3. Stage B — affinity synthesis

### Meaning-bearing cards

| ID | source | card | incoming state |
|---|---|---|---|
| C01 | T1 | 説明を読むことが、複数回答者にとって展示を見る時間を短くした | target-supported |
| C02 | T2 | 入口長文パネルへ注意を向けた一部来館者は最初の展示ケースをほぼ見なかった | target-supported |
| C03 | T3 | 学芸員は説明の一律増加にも情報の全面削減にも慎重 | target-supported |
| C04 | T4 | 問いカードは3種で利用差が大きいが差の理由は不明 | target-supported + unresolved cause |
| C05 | T5 | 外国語利用者について聞き取り材料がない | target-supported observation gap |
| C06 | F1 | 展示空間を「展示物との間に余白をつくる場」とみる | framework-generated candidate |
| C07 | R1 | 常連1名は説明が多いほど安心すると答えた | target-supported singleton / counterexample |
| C08 | R2 | 問いカード不使用の原因は内容・配置・非認知の間で未分解 | unresolved |
| C09 | R3 | ガイド媒体の選択はauthor/caller側で未決定 | author-pending |

### Emergent groups and residuals

`G01` — **説明へ注意を向けることが、展示物を見る時間と競合する場面がある**

- members: C01, C02
- limitation: 全来館者や全説明へ一般化しない

`U01` — **情報量を単純な増減問題へ閉じられない学芸員側の留保**

- basis: C03
- state: singleton / retained tension

`U02` — **説明量が安心につながるという少数の反対方向の材料**

- basis: C07
- state: singleton / possible counterexample
- G01へ丸め込まない

`G02` — **問いカードの利用差は確認されたが、何が効いたかはまだ分からない**

- members: C04, C08
- state: target-supported difference + unresolved cause

`U03` — **外国語利用者について現在の材料が空いている**

- basis: C05
- state: observation gap

`F01` — **展示物との間に余白をつくるという設計レンズ**

- basis: C06
- state: framework-generated candidate
- target-supported groupのsupport memberには数えない
- G01/G02/U01を問い直す探索資源にはなり得る

`Q01` — **ガイド媒体の選択**

- basis: C09
- state: author-pending
- no decision made

### Questions and handoff capsule

- `Q02` G01とU02の差は、必要な「説明量」の差か、安心を生む別機能の差か。
- `Q03` G02の利用差は、カード内容・配置・気づきやすさのどこから生じたか。
- `Q04` U03を埋めると、G01の「情報への注意と展示観察」の構造は変わるか。

```text
stable:
  G01 <- {C01,C02}
  U01 <- {C03}
  U02 <- {C07}
  G02 <- {C04,C08}
  U03 <- {C05}
  F01 <- {C06} [framework-generated]
  Q01 <- {C09} [author-pending]

residual/questions:
  Q02 -> G01/U02
  Q03 -> G02
  Q04 -> U03/G01

constraints:
  F01 != target support
  Q01 != delegated decision
  residual existence != automatic continue
```

## 4. Stage C — iterative inquiry with delayed delta

### Input delta

- `D1` 外国語利用者4組のうち3組が入口で翻訳ページを探し、その間ほとんど展示を見ていなかった。
- `D2` C07と同じ常連来館者が、安心につながるのは詳しい説明そのものより「見落としていないと確認できる目印」だと追加説明した。
- `D3` 使われなかった問いカード1種を展示ケース脇へ移すと、文面を変えずに手に取る人が増えた。

### Locate touched semantic artifacts

reopen:

- D1 → U03, G01, Q04
- D2 → U02, Q02
- D3 → G02, Q03

carry without claiming reinspection:

- U01
- F01
- Q01

### Structural delta

`+ C10 [D1]` — 外国語利用者4組中3組で、翻訳情報を探す行為と展示観察が同時には進んでいない場面が観察された。

`~ U03` — 「外国語利用者について材料がない」から、「小数の入口観察材料が初めて得られた」へ変更。外国語利用者一般の要求を確定するには不足。

`~ G01` — C10が同じattention/time構造へ触れたため、意味核を「説明を読む行為」から「情報へアクセスする行為が展示観察と競合する場面がある」へ局所的に拡張する。全構造は再構築しない。

`+ C11 [D2]` — C07の常連では、安心の説明が「情報量」から「見落としていないことを確認できる目印」へ具体化された。

`~ U02` — 「説明量が多いほど安心」という単純な反対方向の読みは弱まる。ただし一人の追加聞き取りであり、他の来館者へ一般化しない。

`~ Q02` — 少なくともこの常連では「安心を生む別機能」を支持する追加材料が得られた。集団レベルでは未解決。

`+ C12 [D3]` — 一つの問いカードでは、文面を変えず配置だけ変えた後に利用が増えた。

`~ G02` — 「原因は完全に未分解」から、「少なくとも1カードでは配置が利用差に関与した可能性を支持する材料がある」へ変更。他カードへ一般化しない。

`~ Q03` — 配置仮説にはtarget-side supportが加わった。内容・視認性・展示文脈の影響は残る。

`carry U01` — D1〜D3は学芸員の一律増減への留保を直接更新しない。再検査済みを意味する`=`は付けない。

`carry F01` — 新材料はF01と整合的に読めるが、framework由来の設計レンズを観察事実へ変えない。直接reopenしていないため`=`は付けない。

`carry Q01 ?` — ガイド媒体はauthor-pendingのまま。D1にスマートフォン利用が含まれることからスマートフォン方式を採用とは推論しない。

### Updated residuals / stop boundary

- `Q05` 外国語利用者にとって翻訳アクセスと展示観察を両立しやすくする条件は何か。
- `Q06` 「見落としていない安心」を他来館者も必要とするか。
- `Q07` 配置以外のカード利用差要因は何か。
- `Q01` 媒体選択はauthor/caller decisionのまま。

ここで停止する。D1〜D3が触れた局所構造は更新でき、残る問いには追加観察・試験・domain判断が必要であり、residual zeroのためだけにroundを増やす理由はない。

## 5. Invariant assessment

| Invariant | Result | 観測根拠 |
|---|---|---|
| H1 evidence boundary | PASS in this run | F01をframework-generatedとして保持し、新deltaとの整合をtarget factへ変換しなかった |
| H2 provenance continuity | PASS in this run | Stage AのstatusをC01〜C09へ引継ぎ、Stage CでもF01/Q01を維持した |
| H3 decision authority | PASS in this run | Q01を最後までauthor-pendingとし媒体を決めなかった |
| H4 residual retention | PASS in this run | U02/G02/U03を消さず、対応deltaが来た時点でstable refを使って更新した |
| H5 local reactivation | PASS in this run | reopen対象をD1→U03/G01、D2→U02、D3→G02へ限定し、U01/F01/Q01はcarryに留めた |
| H6 no domain self-certification | PASS in this run | 展示設計としての正解や全来館者への有効性を宣言せず、追加観察・domain判断を残した |

**判定:** protocol-level engineering trialとしてH1〜H6をすべて検査可能だった。明白なMethod contract違反はこのrunでは観測されなかった。

このPASSをproduction readinessや一般的なbehavioral reliabilityの証明には使わない。

## 6. Diagnostic observations

### D-01 — stable semantic handleはhandoff品質に効く

Stage Bで`G01/U02/G02/U03/F01/Q01`を外部handleとして残したことで、Stage Cはどこに新材料が触れたかを具体的に表現できた。iterative inquiry側のstable handle契約と相性がよい。

### D-02 — provenanceはsupport countingの境界としても必要

F01を注記するだけでなく、target-supported groupのmember/support countへ入れないと明示することで、framework候補がtarget evidenceへ滑り込む経路を抑えやすい。

### D-03 — carried-untouchedとchecked-but-unchangedを分ける必要がある

iterative inquiryの`=`は「touched and explicitly checked, but semantically unchanged」を表す。D1〜D3が直接触れないU01/F01を`=`へ数えると、再検査していないものを再検査済みに見せる危険がある。

今回のrunでは`carry`へ分けた。これはprotocol/H5の表現上の改善点であり、Method Definitionの欠陥とは現時点では判断しない。

### D-04 — handoff schemaを早く固定しなくてよい

このpacketではtable + stable handles + residual listで実行できた。初回から新しいJSON schemaを設ける必要性は確認できなかった。

### D-05 — 同一context passの証拠強度は低い

実行モデルが正答条件を知っているため、次回は実行側にはtask packetと現行Skillだけを与え、H1〜H6による評価を別contextまたは人間reviewへ分離する必要がある。

## 7. Result-driven next action

1. protocolへ`carried-untouched != =`を明記する。
2. Run 002をfresh execution / separate evaluation条件で行う。
3. Run 002でも同一の境界failureが起きる場合だけ、最小failure fixtureを作る。
4. 次にE1 authority/provenance adversarial variantへ進む。

このrunでは、v0.5のsplit Methodが一つの固定packet上で**来歴・残差・author-pending・局所再開を外部artifactとして受け渡せる**ことを確認した。ただし探索的engineering evidenceであり、一般化しない。
