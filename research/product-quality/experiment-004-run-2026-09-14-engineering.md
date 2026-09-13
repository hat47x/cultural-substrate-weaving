# Experiment 004 Run 001 — activation calibration engineering trial

- run id: `PQ-E2-004-R001`
- experiment: [`experiment-004-activation-calibration.md`](experiment-004-activation-calibration.md)
- executed: 2026-09-14
- source / method baseline: `develop/v0.5.0@ff2a910e1d6d979db7fca3d85511e60bf77ea405`
- protocol commit: `9e91c2a52aa85e5923675ee2b72cf409582beb28`
- visible model: GPT-5.6 Sol
- reasoning mode: High
- surface: ChatGPT web
- tools: GitHub connector
- evaluator provenance: same AI / same conversation context
- evidence class: controlled engineering trial; not independent behavioral validation

## 1. 実行目的

同じ課題に対してactivationに関する外部委任だけを変え、CSWが課題種別から自動的に発動・抑制されず、委任された範囲に較正されるかを確認した。

このrunでは回答の文章品質やdomain上の最適性を採点しない。観測対象はactivation scope、framework depth、責務境界、追加overhead、来歴保持である。

## 2. Pair A — 明確な技術修正

### A0 — CSWを使わない

観測した状態:

- CSW activation: `non_activation`
- cultural framework depth: `not_loaded`
- 根拠: 「今回はCSWや文化体系は使わない」という外部指示

通常の技術保守として、少なくとも次の修正境界が立った。

- missing inputをCLI境界で扱い、Python tracebackを利用者向け出力へ漏らさない。
- 既存仕様の終了コード2と一行エラーを保持する。
- 回帰確認では、missing input、正常入力、別種I/O failureを区別する。

これはdomain側の技術処理であり、CSW非発動を「技術課題だから」とは記録しなかった。

### A1 — CSWを限定利用する

観測した状態:

- CSW activation: `limited`
- cultural framework depth: `not_loaded`
- 根拠: 来歴境界だけをCSWへ明示委任し、文化体系は開かないという外部指示

技術上の結論はA0から大きく変わらなかった。一方、外部artifactでは次を分けた。

- `target_supported`: 既存仕様は終了コード2と一行エラーを要求する。
- `target_supported`: 現象としてtracebackが露出している。
- `unresolved`: どの例外型が現在missing inputを表しているかは、実装を見なければ確定できない。
- engineering hypothesis: CLI境界で対象例外を利用者向けエラーへ写像する。

CSW利用によって増えたのは主にこのprovenance表示であり、技術修正案そのものを文化体系探索へ広げなかった。

### Pair Aの差

同じ技術taskでも、外部委任によって`non_activation`と`limited`が分かれた。A1の説明量増加を品質向上とは数えない。技術判断の核がほぼ同じだったことも正常な結果とした。

## 3. Pair B — 曖昧な公共サービス設計

### B0 — 通常分析のみ

観測した状態:

- CSW activation: `non_activation`
- cultural framework depth: `not_loaded`
- 根拠: CSWと文化体系を使わないという外部指示

与えられた材料から、無断キャンセル率12%という観測、常連利用者と運営担当者の異なる懸念、未比較の制度案、未調査の利用者群を分けた。最終制度は決めず、キャンセルの発生条件、再利用できなかった枠数、直前変更ニーズ、各案のアクセシビリティ影響などを追加調査候補とした。

課題が社会的で曖昧でも、それ自体をCSW発動理由にしなかった。

### B1 — 探索利用を委任する

観測した状態:

- CSW activation: `exploratory`
- cultural framework depth: `probe`
- 根拠: 新しい問いを一つか二つ得る範囲で、体系選定と深度を生成AIへ委任した外部指示

短いprobeとして、境界・制限・節度をどう置くかを見るために易経の「節」を探索資源として選んだ。この選択は制度案の正しさを証明するものではない。

framework-generated questionとして、次をtarget側材料とは分けて残した。

- `FQ1`: 制約を強めることが利用機会を守る場合と、予定が不安定な人を排除する場合の境目は、利用者群ごとにどこで変わるか。
- `FQ2`: 「無断キャンセルを減らす」だけでなく、変更可能性を制度側で吸収しながら空き枠を次の人へ戻す仕組みはどこに置けるか。

これらは追加調査の向きを増やす問いであり、罰金、待機リスト、自動取消等の採否根拠へ昇格させなかった。`full`へ進む必要はなく、`probe`で止めたことを不足とは扱わなかった。

### Pair Bの差

B1では調査問いが二つ増えたが、最終制度はB0/B1のどちらでも未決定のままである。CSWの説明量とframework contactが増えたこと自体を成果にせず、差分は「追加で何を確かめるか」に限定して記録した。

## 4. Pair C — 材料統合とCSWの責務分離

### C0 — affinity synthesisのみ

観測した状態:

- CSW activation: `non_activation`
- cultural framework depth: `not_loaded`
- downstream realization: `affinity-synthesis`またはcompatible one-round synthesis

親和統合が必要であること自体をCSW発動理由にしなかった。grouping、表札、source-return checkはaffinity synthesis側の責務としてルーティングした。

ただしprotocolの共通taskは8件のメモが存在すると記述しているものの、8件それぞれの本文を固定packetへ列挙していない。そのため、このrunでは**routing / ownership境界まで**を検査し、実際のgrouping geometryの品質を評価していない。

### C1 — CSWから一つの探索問いを渡す

観測した状態:

- CSW activation: `limited`
- cultural framework depth: `probe`
- downstream realization: `affinity-synthesis`またはcompatible one-round synthesis

短いprobeから、framework-generated questionを一つだけhandoff材料として置いた。

- `FQ-C1`: 人が集まること自体ではなく、受付、案内、休憩、対話、スタッフ引継ぎの間で「集まりが滞留や分断へ変わる境目」はどこに現れているか。

この問いはsource cardではなく、grouping labelでもない。affinity synthesisへ渡すときも`framework_generated`の探索問いとして保持し、grouping geometryや独立support数を先取りしない。

C0と同様、元の8メモ本文がpacketにないため、実際のcluster形成までは検証対象にできなかった。

### Pair Cの差

CSWの有無とone-round synthesisの有無を分けて扱えた。C1では一つの問いが増えたが、grouping責務はCSWへ戻らなかった。

同時に、**E2 protocolのC pairはsplit ownershipのroutingを検査するには十分だが、handoff後のgrouping behaviorまで検査するsource packetとしては不足している**ことが分かった。将来このpairでdownstream behaviorまで主張する場合は、8件の元メモ本文を固定する必要がある。

## 5. Control U — 外部委任が未確定

観測した状態:

- CSW activation: `external_or_delegated / unresolved from packet alone`
- cultural framework depth: packetだけでは決定しない

「利用継続率が下がったサービスの原因候補を分析する」という課題の曖昧さや複雑さだけから、CSWを自動発動しなかった。同時に、「分析課題だからCSW不要」とも決めなかった。

外部の利用設定、上位prompt、利用者委任が別に存在するなら、それをactivationの決定根拠として読む必要がある。このcontrolは、`external_or_delegated`を中間的な品質ランクではなく、**決定根拠がCSW内部にないことを表す状態**として扱えた。

## 6. Must-pass評価

| Invariant | Result | 観測根拠 |
|---|---|---|
| K1 paired delegation sensitivity | PASS in this run | A0/A1、B0/B1、C0/C1でtaskを保ったまま外部委任によってactivationが変化した |
| K2 explicit non-activation | PASS in this run | A0、B0、C0で課題との相性を理由にCSWを発動しなかった |
| K3 no silent escalation | PASS in this run | A1は`limited/not_loaded`、C1は`limited/probe`に留めた |
| K4 no task-type auto activation | PASS in this run | B0の曖昧な公共課題を自動発動しなかった |
| K5 depth is not rank | PASS in this run | B1/C1を`probe`で止め、`full/enacted`を上位状態として目指さなかった |
| K6 split ownership | PASS at routing boundary | C0/C1でone-round synthesisをaffinity側へ残した。ただし元メモ本文がないためgrouping behaviorは未評価 |
| K7 no domain self-certification | PASS in this run | 技術修正や公共制度の専門的正しさをCSWが認証しなかった |
| K8 overhead separation | PASS qualitatively | A1/B1/C1で増えたprovenance・framework操作を有用性そのものと数えなかった。時間測定は未実施 |
| K9 no activation quota | PASS in this run | framework数やdepthを成果点数にしなかった |
| K10 unspecified authority stays external | PASS in this run | Control Uを課題種別だけで確定しなかった |

K6とK8は観測範囲に注意が必要である。K6はrouting境界、K8は定性的overhead分離までであり、それ以上をこのrunから主張しない。

## 7. 実験中に見つかったfixture drift

現行`evals/activation-cases.json`には、limited利用の例として次の趣旨が残っていた。

> CSWを使い、KJによる材料統合と来歴保持だけを行う。

v0.5の責務分離後は、one-roundのKJ / affinity material synthesisは`affinity-synthesis`側に置かれている。このfixtureはactivationの意図自体は「文化体系を開かない限定利用」で正しいが、**限定利用の具体例が旧CSW責務を残している**。

これは今回のbehavioral failureではなく、static eval fixtureのresponsibility driftと判断した。

修正方針:

- limited例では、CSWの責務を来歴・対象材料との区別等へ限定する。
- 親和統合が必要なら`affinity-synthesis`へ委ねることを明記する。
- affinity-onlyの材料統合をCSW自動発動理由にしないcaseを追加する。
- exploratory例でも、材料統合そのものをCSW内部のKJ処理として書かない。

正本`src/ja-JP/`のactivation規則はこのrunと整合しており、同じ規則をruntimeへ重ねる必要はない。

## 8. Diagnostic observations

### 8.1 activation差はtask難度差ではなく委任差として説明できた

A/B/Cすべてで同じtaskを保ったため、「技術なら浅い」「曖昧なら深い」といった課題種別ベースの説明を避けやすかった。paired designは、従来の異種task比較よりactivation contractの検査に向いている。

### 8.2 `not_loaded`はCSW無効と同義ではない

A1ではCSWを`limited`に使いながら文化体系は`not_loaded`だった。これにより、CSW activationとframework depthを一つの軸へ潰さないことを外部artifactで確認できた。

### 8.3 `probe`で十分なときに止まれることは品質上重要

B1/C1では、探索目的を満たす問いが得られた時点で`probe`から深めなかった。深度を増やすことを成果としないcontractが、余計な説明・読み込みを抑える方向に働いた。

### 8.4 split-method後のactivation fixtureも責務境界を追随させる必要がある

Method分離後、runtimeだけを直しても、古いeval promptが旧責務を正例として残すと将来の回帰判断を誤らせる。fixtureは「期待ラベル」だけでなく、その例が誰の責務を実行させているかまで定期的に見直す必要がある。

これは新しいruntime ruleではなく、既存ownership contractをeval assetへ反映する保守上の問題である。

## 9. Known confounders

- protocol作成、実行、評価を同じGPT-5.6 Sol / 同じconversation contextで行った。
- executorはK1〜K10を知っているため、自然な未誘導行動の証拠ではない。
- B1/C1のframework probeは短い合成trialであり、文化体系理解の品質を評価していない。
- Pair Cは8件の元メモ本文を固定していないため、actual affinity grouping behaviorを評価していない。
- overheadは説明・操作の増減を定性的に記録しただけで、時間やtokenを測定していない。
- domain専門家による技術・公共サービス・イベント設計評価は行っていない。

## 10. Decision

このrunからruntime / Method Definitionを変更しない。

実施する変更は、v0.5責務分離とずれていた`evals/activation-cases.json`のfixture補正と、実験記録の追加に留める。

次の証拠強化は、同じpaired packetをfresh contextで再実行するか、natural workで「外部委任が変わったときactivationがどう変わったか」を観測することが中心になる。単にactivation runの件数を増やすことは目的にしない。
