# Experiment 003 Run 001 — delayed reactivation engineering trial

- experiment id: `PQ-E4-003`
- run id: `PQ-E4-003-R001`
- run date: 2026-09-14
- run type: engineering trial
- protocol: [`experiment-003-delayed-reactivation.md`](experiment-003-delayed-reactivation.md)
- protocol commit: `81bd615af9eb92d5ea87a0a0efd3b707334f3591`
- source baseline: `develop/v0.5.0@810bc4a2a2d4db66693853474021756ec0c1e615`
- visible model: GPT-5.6 Sol
- surface: ChatGPT web chat
- evaluator provenance: same AI / same conversation context
- evidence strength: low; protocol execution and self-evaluation share context

## 1. このrunで確認すること

固定済みprior snapshotへ、6週間後を模した`D01`〜`D04`だけを追加し、一度停止した調査を局所的に再開する。

このrunの時間差は合成packet上の設定であり、モデルが実際に6週間記憶を保持したことを意味しない。検査対象は、**外部snapshotからの再開契約**である。

## 2. Loaded artifacts

- `research/product-quality/experiment-003-delayed-reactivation.md`
- `research/skill-prototypes/iterative-inquiry-synthesis/SKILL.md`
- `research/skill-prototypes/iterative-inquiry-synthesis/references/ROUND-TEMPLATE.md`
- `research/skill-prototypes/affinity-synthesis/SKILL.md`

## 3. Round

- **Round ID:** `library-guide-r3-delayed`
- **Previous state:** prior Round 2 was stopped because `U01` / `Q02`を判別する材料がなく、`P01`は外部決定に残っていた
- **Current inquiry:** 初来館者の安心と行動開始を、単純な「説明量の多少」ではなく、現在地・次行動を確認できることとの関係として捉え直せるか
- **External constraint:** 案内媒体の最終選択は図書館側に残す

過去の問い`Q01`は書き換えず、prior snapshotの履歴として保持する。

## 4. Input delta

- `D01` 初来館者8名中5名が、詳しい説明より「今どこにいて、次に何をすればよいか分かると安心する」と回答
- `D02` 長文案内を変えず一行の方向表示だけを追加した観察で、初来館者の入口滞在が短くなった。小規模・長期未確認
- `D03` 外国語利用者3組中2組が、日本語案内を読まずスマートフォンで館内図を探索。理由の聞き取りなし
- `D04` 閲覧席の照明調査で、夕方の一部利用者からまぶしさの訴え

## 5. Reopened prior artifacts

### `D01` / `D02`が触れたもの

- `C01` — 入口での長い案内読解と行動開始の遅れ
- `C03` — 初来館者の不安に関する職員の見立て
- `G01` — 入口情報と行動開始の関係
- `G02` — 初来館者の安心に関する未確定構造
- `U01` — 不安の原因が説明不足かorientation不足か未判別
- `Q01` — 説明情報を増やす／減らすというprior inquiry
- `F01` — 「入口を移行の閾として扱う」というframework由来候補。新材料との方向上の近さを確認するため、来歴保持の観点から明示的に照合

### `D03`が触れたもの

- `Q02` — 外国語利用者に同じ問題構造があるか
- `P01` — 媒体の未決定事項。スマートフォン利用が観察されたため照合するが、採用判断へは昇格させない

### `D04`が触れたもの

- `C04`
- `G03`

## 6. Carried but untouched

- `C02` — 繰り返し利用者が入口案内をほとんど読まないというprior card

`C02`は`G01`の既存memberとして参照同一性を保つが、今回のdeltaは繰り返し利用者を調べていない。したがって`=`には入れない。

prior `R01`も履歴上は保持するが、新しい問いを立てるために再検査したrelationとしては扱わない。

## 7. One-round synthesis of touched material

今回のdeltaには、初来館者、外国語利用者、照明という異なる材料が含まれるため、touched subsetの意味単位化に`affinity-synthesis`の契約を参照した。

新しい意味単位を次のように置く。

- `C05` — `D01`から、初来館者8名中5名では、安心が詳しい説明量より現在地・次行動の確認可能性と結び付いて語られた
- `C06` — `D02`から、長文案内を維持したまま一行の方向表示を加えた小規模観察で、初来館者の入口滞在が短くなった。長期・一般化は未確認
- `C07` — `D03`から、観察した外国語利用者3組中2組は日本語入口案内ではなくスマートフォンで館内図を探した。理由は未確認
- `C08` — `D04`から、夕方の一部利用者に閲覧席照明のまぶしさの訴えがあった

`C05`〜`C08`は、それぞれ元の`D01`〜`D04`へ戻れる。`D03`の行動から「翻訳不足が原因」とは補っていない。

## 8. Structural delta

```text
+ C05 := 初来館者8名中5名では、安心が説明量より現在地・次行動の確認可能性と結び付いて語られた
+ C06 := 一行の方向表示追加後、小規模観察で初来館者の入口滞在が短くなった。長期効果は未確認
+ C07 := 外国語利用者3組中2組がスマートフォンで館内図を探した。理由は未確認
+ C08 := 夕方の一部利用者に閲覧席照明のまぶしさの訴えがあった
~ G01 := C06を加え、入口での情報処理と行動への移行は「説明量」だけでは捉え切れない可能性が加わった
~ G02 := C05を加え、初来館者の安心には現在地・次行動の確認可能性が関わる可能性が具体化した
~ G03 := C08を加え、照明系の別課題として局所的に更新した
~ U01 := orientation不足という区別を支持する材料が増えたが、説明不足の影響を排除できるほどには解消していない
? Q02 := 外国語利用者の一部で館内図探索は観察されたが、理由を聞いておらず同じ問題構造かは未解決
+ Q03 := 初来館者の安心と行動開始を支えるうえで、説明量とorientation cueはそれぞれどの役割を持つか
= F01 :: D01/D02と方向上の近さはあるが、最初のoriginはframework_generatedのままであり、target-side supportへ遡及変換しない
= P01 :: D03でスマートフォン利用を確認したが、媒体の採用判断は依然として図書館側の未決定事項
```

### `Q01`の扱い

prior `Q01`を`~`で別文へ上書きしなかった。

`Q01`は「説明情報を増やす／減らすことのどちらが初来館者を助けるのか」という当時の問いとして履歴に残し、`D01` / `D02`によってその二分法が粗い可能性が見えたため、現在の問いとして`Q03`を新設した。

これは「旧問いが誤りだった」と消すのではなく、**何が問いを動かしたか**を残すためである。

## 9. Semantic vs representation delta

### Semantic delta

- `C05`〜`C08`の新規材料化
- `G01` / `G02` / `G03`の局所更新
- `U01`の未解決範囲の縮小
- `Q03`の新設
- `Q02`の未解決状態に新しい観察材料を追加

### Representation delta only

- `Q01`を現在の問いとして書き換えず、Question Shiftで履歴との関係を示したこと
- `carry`をcompact notationの新記号として追加せず、未接触artifactの記述欄として表したこと

新しいMethod記号は導入していない。

## 10. Residuals

| Ref | Current state | What could clarify it |
|---|---|---|
| `U01` | 一部縮小。orientation不足を示す本人材料は得たが、説明不足の影響は未分離 | 案内量とorientation cueを分けた追加観察・聞き取り |
| `Q02` | 未解決。外国語利用者の館内図探索は観察したが理由不明 | 本人への聞き取り、言語別案内利用の観察 |
| `P01` | author/caller pendingのまま | 図書館側の目的・制約・選択基準と追加検証 |
| `U02` | `D02`の効果が小規模・短期観察に限られる | 別日・別入口・利用者層を含む再観察 |

## 11. Question Shift

- **Previous inquiry:** `Q01` 説明情報を増やす／減らすことのどちらが初来館者を助けるのか
- **Current inquiry:** `Q03` 初来館者の安心と行動開始を支えるうえで、説明量とorientation cueはそれぞれどの役割を持つか
- **What caused the shift:** `D01`が安心の内容を本人の言葉で具体化し、`D02`が長文案内を減らさなくても短い方向表示だけで行動差が生じ得ることを示した
- **What remains valid:** 入口での情報設計が行動開始へ影響し得るという`G01`の核。説明量が無関係になったとは判断していない

## 12. Provenance check for `F01`

`F01`と`D01` / `D02`には「入口を移行の場として見る」という方向上の近さがある。

しかし、今回target側に追加supportが得られたのは、

- 初来館者の一部がorientationを安心と結び付けたこと
- 一行の方向表示追加後に入口滞在が短くなったこと

である。

文化体系から生じた`F01`そのものがtarget factへ変わったわけではない。framework由来の履歴を残し、新しいtarget-side supportは`C05` / `C06`として別に保持した。

## 13. Continuation boundary

- **Decision:** Stop / hand off
- **Reason:** delayed deltaが触れた部分の局所更新は完了した。`U01`は縮小したが解消しておらず、`Q02`も理由未確認のままである。一方、現材料だけでさらにroundを回しても新しい判別は増えない
- **Possible next material:** orientation cueと説明量を分けた追加観察、外国語利用者への聞き取り
- **Requires human/domain decision?:** yes。`P01`の媒体選択、実験規模、図書館運用への採否は外部判断

残差があることだけを理由に、自動的に次roundへ進まない。

## 14. Round handoff

- **Return to:** `U01`, `Q02`, `Q03`, `P01`
- **Reopen when:** orientation cueと説明量を分ける新材料、外国語利用者本人の材料、または媒体選択に関する外部判断が届いたとき
- **Preserve provenance for:** `F01` = framework_generated; `C05` / `C06` / `C07` / `C08` = delayed target-side material
- **Do not silently assume:** orientation cueが全利用者へ有効、外国語利用者の行動原因が翻訳不足、スマートフォンが最適媒体、`F01`がtarget-supportedへ昇格した、といういずれも仮定しない

## 15. Must-pass evaluation

| Invariant | Result | Evidence |
|---|---|---|
| L1 append-only history | PASS | `Q01`とprior stop reasonを保持し、新しい`Q03`を追加した |
| L2 touched-only reopen | PASS | deltaごとにreopen理由を限定し、`C02`をcarryに残した |
| L3 stable identity | PASS | 既存`G01`〜`G03`、`U01`、`Q02`、`P01`を意味同一性の範囲で再利用した |
| L4 carry != checked | PASS | 未接触`C02`を`=`へ入れていない |
| L5 residual accounting | PASS | `U01`は縮小、`Q02`は未解決、`U02`を新規残差として分離した |
| L6 question history | PASS | `Q01`を上書きせず`Q03`を追加し、shift理由を記録した |
| L7 provenance continuity | PASS | `F01`を`framework_generated`のまま保持し、新target supportを別card化した |
| L8 authority boundary | PASS | `P01`を明示的に再検査したうえで外部決定に残した |
| L9 no false continuity | PASS | prior stop後の新roundとして記録した |
| L10 no domain self-certification | PASS | 小規模観察の限界と追加検証・外部判断を残した |

このPASS表は同一AI contextによる自己評価であり、独立測定ではない。

## 16. Diagnostic findings

### 16.1 問いのshiftをcompact deltaへ無理に押し込まない

今回、`Q01`を`~ Q01 := 新しい問い`とすると、過去に何を問うていたかが見えにくくなる。

現行Round Templateには`Question Shift`欄があるため、旧問いを履歴に残し、現在の問い`Q03`を新設する方が監査しやすかった。これは既存契約で表現できるため、Method変更は不要である。

### 16.2 stop snapshotが再開品質を支える

prior artifactだけでなく、**なぜ前回停止したか**が明示されていることで、「残差が残っていたから本当は継続中だった」と後から物語化せずに済んだ。

現行iterative-inquiry-synthesisはstop / restart reasonを既に外部化する契約を持つため、新規規則は不要である。

### 16.3 一つのdelayed deltaでも局所trackは複数になり得る

`D01` / `D02`は案内系、`D03`は外国語利用者、`D04`は照明系を触った。時間的に同時に届いたからといって、一つの大きな再構築へまとめる必要はなかった。

特に`D04`を`G03`だけへ局所反映できたことは、touched-artifact selectionの診断として有効だった。

## 17. Known confounders

- protocol作成・実行・評価を同じGPT-5.6 Sol / 同じconversation contextで行った
- 「6週間後」は合成packet上の設定であり、実時間をまたいだ記憶性能試験ではない
- source packetは合成事例で、実在図書館のdomain validationではない
- evaluatorがmust-pass invariantsを事前に知っている
- fresh restartや別surfaceでの再現性は未検証

## 18. Decision

**Decision: protocol / representation evidenceのみ追加。runtime / Method Definition変更なし。**

このrunでは、既存の`iterative-inquiry-synthesis`契約で、stop後の局所再開、stable ID、question shift、provenance、再停止まで表現できた。

次に証拠を強めるには、Run 001の出力を見ていないfresh contextで同じprior snapshotから再開し、そのartifactを別評価者がL1〜L10で読む必要がある。
