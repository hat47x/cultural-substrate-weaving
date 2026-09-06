# Iterative Inquiry Synthesis — Real-task Paired Comparison 2026-09-07

Status: **same-model sequential comparative execution; not an independent, blinded, or randomized evaluation**

## Purpose

CSWからmulti-round inquiry orchestrationを分離しても、現行 `src/ja-JP/core/iteration.md` が担っている「新材料を受けて必要な場所だけを再開し、残差と次の問いを引き継ぐ」働きが失われないかを、現在進行中のKJ系技能分離そのものを実タスクとして比較する。

比較するのは最終文言の一致ではない。

- new deltaによってどこをreopenするか。
- どこを無理由に作り直さないか。
- 問い、残差、停止理由、再開条件を保持できるか。
- one-round synthesisが不要なroundを区別できるか。
- canonical runtime migrationへ進める根拠と、まだ不足する根拠を分けられるか。

同じauthoring modelがA→Bの順で適用しているため、独立性はない。BがAの出力を直接入力として使わないよう、両方とも下記の固定input snapshotだけから作成した。

---

## Fixed real-task input

### Current inquiry

> KJ系技能分離のresearch prototypeは、canonical `src/` migrationへ進める段階に入ったか。まだなら、今回のdeltaでどのgateが動き、次roundでは何を検証すべきか。

### Prior migration state

`docs/ja/maintainers/kj-split-migration-audit.md` が置く主なruntime migration gatesを、比較用handleとして次のように置く。

- `M1`: affinity-synthesis prototypeが方法fixtureを満たす。
- `M2`: 現行CSW `integration.md` と実タスクでpaired comparisonを行う。
- `M3`: narrower Affinity Mapping Skillとの委譲境界を実タスクで確認する。
- `M4`: iterative-inquiry-synthesisへ分けてもround handoffの情報損失がない。
- `M5`: CSWからLayer 1を外してもframework attributionとreturn-to-targetが壊れない。
- `M6`: Agent Skill dependency / fallback方針を決める。
- `M7`: ja-JP / en-US / translation manifest / build adapterの変更単位を決める。
- `M8`: `make check`相当の全検査を通す。

比較前の既知状態:

- affinity-synthesisにはMETHOD、fixture、authoring dry-run、real-task paired comparison、large-set retrospectiveがある。
- iterative-inquiry-synthesisにはMETHODとround templateがあるが、今回のdelta以前は独自evalが不足していた。
- canonical `src/` はまだ分離していない。
- English prototype parityは未実施。
- complete checkoutが利用できず、development-state `make check` は未実行。

### New delta

今回追加されたresearch evidenceだけをdeltaとする。

- `D1` / #275: iterative-inquiry-synthesisに9 contract fixturesを追加し、既存METHODをsuite manifestへ登録した。
- `D2` / #276: research suite manifestと実体のpath / method / skill identity整合を通常unit testへ接続した。
- `D3` / #277: 9 fixturesをsame-authoring-modelで仕様自己点検し、8件はcovered、compatible one-round synthesis不在時のfallbackだけPARTIALと記録した。
- `D4` / #278: fallbackをMETHOD I15とSKILLへ明文化し、post-fix recheckで仕様文面上はgapが閉じた。ただし実挙動は未検証。
- `D5`: complete checkout用端末はofflineのままで、`make check` は依然未実行。

### Explicit non-delta

今回の材料には次を変更する新証拠はない。

- English realization parity。
- build/validatorのmulti-skill generalization。
- CSW→Layer 2→Layer 1を通したframework attribution / return-to-targetの実行結果。
- narrower external Affinity Mapping Skillへの実routing結果。
- release validation実行結果。

---

# Arm A — Current CSW `core/iteration.md`

## A1. 材料差分を受け取る

今回のdeltaは、iterative Layer 2のmethod/eval/fallback設計に集中している。canonical runtime、English realization、build package、release executionには新しい実証結果がない。

## A2. 関係する古い残差へ戻す

今回前景へ戻すべきなのは主に次である。

- iterative handoffが情報を失わないかという `M4`。
- dependency / fallbackをどう扱うかという `M6`。
- 最終release executionの未完了を示す `M8` は、D5により未解決状態が継続していることを確認する。

`M1` / `M2` のaffinity側既存成果を今回再構築する必要はない。`M3` / `M5` / `M7` も今回のdeltaだけでは新しい判定材料がない。

## A3. 今回の問いを見る

問いは変わらない。

> canonical migrationへ進めるだけのevidenceが揃ったか。

ただし、Layer 2についての問いは「仕様を作れるか」から「実taskでhandoffを保てるか」へ一段進んだ。

## A4. 文化体系利用

このroundでは文化体系を開く必要はない。method packaging / handoff evidenceの確認であり、別の認知場を加えることで判別力が増す材料は与えられていない。

## A5. 実作業への反映

- `M4`: METHOD / fixtures / fallbackの仕様準備は進んだが、actual paired execution前なので未完了。
- `M6`: hard dependencyを置かず、compatible realization不在を未実行としてhandoffするfallback方針はresearch prototype text levelでは具体化した。ただしhost実挙動は未確認。
- `M8`: offline環境のため未完了。

したがってcanonical `src/` migrationはまだ開始しない。

次の実作業は、iterative Layer 2を実タスクへ適用し、前roundの問い、局所reopen、structural delta、残差、stop/restart情報が落ちないかを見ることである。その後にCSW→Layer 2→Layer 1のattribution handoffを確認する。

## A6. 境界・引継ぎ

終了ではなくresearch継続。

- 戻り先: `M4`, `M5`, `M6`。
- 次に確認すること: Layer 2のreal-task handoff、続いてCSWとのprovenance handoff。
- 依然保留: English parity、build generalization、complete-checkout `make check`。
- canonical sourceは現状維持。

### Arm A observation

現行CSW iterationでも、今回のdeltaを局所的に扱い、canonical migrationを早めず、次の検証へ引き継げた。

一方、変更状態を `new / changed / unchanged / withdrawn / unresolved` として明示する専用契約や、one-round synthesisを実行しなかったroundを明示する欄はないため、その情報は文章中の判断として表現された。

---

# Arm B — `iterative-inquiry-synthesis`

## B1. Round snapshot

- **Round ID:** `kj-split-eval-r1-2026-09-07`
- **Current inquiry:** KJ系技能分離はcanonical migrationへ進める段階か。
- **Input delta:** `D1`〜`D5`。
- **Reopened prior artifacts:** `M4`, `M6`, `M8`。
- **Context-only refs:** `M1`, `M2`。
- **Not reopened without new evidence:** `M3`, `M5`, `M7`。

## B2. Synthesis realization binding

**one-round synthesis: not required in this round**

今回のdeltaは、すでに外部成果物として確定したresearch evidenceとmigration gateの状態更新である。新しいraw material集合をcard/group/map/narrativeへ統合し直す必要はない。

したがって `affinity-synthesis` を儀式的に呼ばず、Layer 2のdelta / history管理だけを行う。

## B3. Structural delta

```text
+ E-IIS-EVAL := iterative-inquiry-synthesis now has its own contract fixtures and authoring dry-run
+ E-IIS-CHECK := research suite manifest drift is now covered by a normal unit-test path
~ M4 := "prototype design only" -> "method/fixture/fallback specification prepared; actual handoff execution still unverified"
~ M6 := "dependency/fallback undecided" -> "research fallback contract defined without hard dependency; host behavior still unverified"
= M8 := complete-checkout validation remains unavailable; no release evidence was added
? Q-IIS-HANDOFF := does actual Layer 2 use preserve prior inquiry, touched refs, residuals, and restart information across a real round?
? Q-CSW-HANDOFF := does CSW -> Layer 2 -> Layer 1 preserve framework attribution and return-to-target boundaries?
```

`M8` はD5が実際に触れ、再確認したが状態が変わらなかったため `=` とする。

`M3`, `M5`, `M7` は今回のdeltaが実質的に触れていないため、`=` を付けて「確認済み」に見せない。

## B4. Question shift

**No top-level question shift.**

canonical migrationへ進めるか、という問いは維持する。

局所的には `M4` の次の問いが変化した。

- previous: Layer 2の方法境界とeval fixtureを定義できるか。
- current: 実taskでround handoffを壊さず運用できるか。
- cause: D1〜D4により仕様とfixtureが準備されたため。

## B5. Continuation boundary

**Continue research; do not begin canonical source migration.**

理由:

1. `M4` は仕様上前進したが、actual executionによるhandoff loss確認がまだない。
2. `M5` のCSW attribution / return-to-target連鎖は今回未評価。
3. `M6` はtext-level fallback contractまで進んだが、routing / unavailable behaviorの実挙動は未検証。
4. `M7` のEnglish / build migration unitは未着手。
5. `M8` はcomplete checkout不在により未完了。

## B6. Next round handoff

- **Return to:** `M4` first, then `M5` / `M6` integration seam。
- **Reopen when:** same fixed migration state is handed to an actual Layer 2 execution, or a concrete CSW→Layer 2→Layer 1 artifact handoff is available。
- **Do not silently assume:**
  - specification coverage implies runtime behavior。
  - same-model paired execution implies independent reproducibility。
  - fallback text implies host routing support。
  - research prototype progress permits canonical `src/` reduction。
- **Keep in background:** `M3`, `M7`, release freeze/tag/publication until new evidence touches them。

### Arm B observation

Layer 2 prototype reached the same high-level decision as current CSW iteration while making touched-vs-untouched gates, synthesis-not-required state, structural delta, and next-round reopen conditions explicit.

---

# Paired comparison

| Check | Current CSW iteration | Iterative Inquiry prototype | Observation |
|---|---|---|---|
| Receive only new delta | yes | yes | equivalent in this task |
| Avoid full-history rebuild | yes | yes | equivalent |
| Reopen `M4` / `M6` locally | yes | explicit refs | prototype is more inspectable |
| Preserve untouched `M3` / `M5` / `M7` | yes by prose | explicit not-reopened distinction | prototype reduces false `unchanged` claims |
| Keep top-level inquiry | yes | yes + local question transition | prototype records finer change |
| Cultural framework non-use | can simply skip | external route not invoked | equivalent |
| One-round synthesis not required | implicit | explicit `not required` binding | prototype-specific clarity |
| Structural delta | prose | explicit `+ / ~ / = / ?` | prototype advantage in auditability |
| Unresolved stop / continuation | yes | explicit continuation boundary | equivalent decision, more structured handoff |
| Canonical migration decision | do not begin | do not begin | equivalent |
| Release gate restraint | preserved | preserved | equivalent |

## Information-loss check

この一件では、現行CSW iterationが必要としていた次の情報はLayer 2 prototypeにも残った。

- current inquiry。
- new material / delta。
- 関係する旧残差だけを前景へ戻すこと。
- 既存構造を無理由に全面再構成しないこと。
- 何が変わり、何が変わらなかったか。
- unresolved questions。
- 次の確認方法と戻り先。
- canonical migrationをまだ開始しない停止境界。

逆に、現行CSW固有の「必要なら文化体系を開く」「文化体系からKJへ返す」はLayer 2へ移していない。今回それを必要としなかったことは、欠落ではなく責務分離と整合する。ただし、この一件だけでは `M5` のframework attribution / return-to-targetがCSW→Layer 2→Layer 1接続で保持されるとは確認できない。

## Result

**PROVISIONAL PASS for this real-task handoff, with strong limitations.**

このsame-model paired executionでは、Layer 2へ分けたことで現行CSW iterationの基本的なround handoff情報が明白に失われた箇所は見つからなかった。また、touched-vs-untouched、synthesis realization state、structural deltaが外部成果物として明示しやすくなった。

ただし、`M4` を完全に満たしたとは扱わない。理由は次のとおり。

- 同じモデルによる逐次比較であり、独立性がない。
- 一つのreal taskだけである。
- 実際の長い履歴を別session / modelへhandoffして再開する試験ではない。
- one-round synthesisを必要とするroundではなかった。
- CSW framework attribution seamを通していない。

## Next evaluation

次は同じround templateを使い、**CSW由来のframework-generated question / correspondenceを、provenanceを保ったままLayer 2へ渡し、その後Layer 1のtarget-material synthesisへ接続するpaired case**を作る。

そこで少なくとも次を確認する。

1. `canonical cultural source != derived correspondence != target-supported finding` がLayer間で潰れない。
2. framework-generated candidateがgrouping taxonomyへ化けない。
3. Layer 1から戻ったtarget-supported resultとframework residualをLayer 2が同一状態へ潰さない。
4. 次round handoffにsource refs / derivation / unresolvedが残る。
5. compatible Layer 1 realizationが利用不能なcaseでは、#278のfallbackどおり未実行でhandoffできる。

この次のcaseを通すまでは、canonical CSW `integration.md` / `iteration.md` を接続契約へ縮小しない。
