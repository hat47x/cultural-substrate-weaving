# Rasa — 表現／受容の発見価値と自然なUXレビュー

Status: 2026-10-18 desk requalification / unreviewed hypothesis; **not an independent first-pass or efficacy observation**.

## 固定対象と比較上の制約

対象は[既存の正例](../worked-examples/rasa-expression-reception.md)と同じ、業務アプリケーションの大量明細入力後の保存失敗画面である。画面は赤く、唯一の「OK」ボタンと「入力に誤りがあります。最初からやり直してください。」という文だけを表示する。

この説明から、実際に入力が消失した、利用者が責められたと感じた、保存処理に特定の原因があった、とは結論できない。元の画面例に含まれるタイミング、色、文面、唯一のボタンを通常側の分析から隠さない。

## A — 体系接触前の通常分析

初回依頼が「保存失敗画面をレビューする」なら、UX/usability/error recoveryは自然な出発点である。強い普通手法には次が含まれる。

- エラーが発生した操作と対象入力を利用者が識別できるか。
- 入力が保持されるか、どの復旧操作を案内すべきか。
- 赤い全面表示や表示のタイミングが必要以上の中断・負担を生まないか。
- 「あなたの入力が誤り」と断定する前に、システム／ネットワーク起因との違いを確認できるか。
- 初回利用者と熟練者で、情報の必要性や実際の復旧行動がどう違うか。

Nielsen Norman Groupのerror-message guidelinesは「目立つこと」「文言と復旧支援」「入力や作業への配慮」を扱う。また *Hostile Patterns in Error Messages* は時機尚早のエラーや攻撃的な提示・不要な妨害を問題化する。これらはRasaの後から選ばれた弱い代用品ではなく、**この対象の種類から接触前に選べる既存の専門方法**である。

したがって、既存正例の「不安になるかもしれない」「作業が失われたように受け取るかもしれない」等は、普通のUX調査でも自然に問える仮説である。利用者が実際にそのように感じたという観測はない。

## B — Rasa接触で変わり得る問い

Rasaの歴史的な中心は芸術表現／演者と観客の美的経験であり、現代のUIでの一般的な「ユーザー感情」分類ではない。CSWは、表現内容、要素の構成、受け手との遭遇、受容経験を**異なる検討対象**として仮に開く。

- 文が示す「入力誤り」と、タイミング・赤色・選択肢の構成が生む受け止め方は、別の問いか。
- 表示直前の作業負荷や入力の蓄積と、表示構成を掛け合わせて調査しているか。
- 同じ画面について異なる受け手の立場を比較するには、どの記録・観察が必要か。

しかしこれらの問いをUI上でde-bindすると、普通のUX review、contextual inquiry、usability studyとかなり重なる。**問いをRasaから発想できることだけでは、独自の新規発見の証拠とならない。**

## C — 能力重複と、接触前に選ばれたかを区別する

| 対象に戻る問い | 事前の普通のUX入口 | Rasa接触 | 現在の扱い |
| --- | --- | --- | --- |
| 誤りと原因を正確に説明するか | エラー回復の基本確認 | 表現と経験の区別 | 重複 |
| 赤い全面表示やOKのみの負担 | disruptiveness・visibility・user effortの確認 | 表現要素の構成 | 重複 |
| 作業を失ったと思うか | 利用者インタビュー／復旧行動観察 | 受け手の経験を仮説化 | 重複、受容は未観測 |
| 熟練／初心者で経験が違うか | audience / user segment調査 | counter-receiver | 重複、受容は未観測 |
| 芸術的な味わいとしてのrasaが成立するか | UI障害には直接の事実ではない | 歴史的・美学的な問い | 対象へ強制しない |

後から選んだ専門方法が一致したという能力重複と、**最初からその方法を選んでいたか**は別の証拠である。ただし今回の対象はエラー画面という明確なUX課題なので、通常側の自然選択には根拠がある。これは文献と題材に基づく机上判断であり、独立回答の実測ではない。

## D — 撤回・非活性化と再開

[機械的な503障害の非適用例](../worked-examples/rasa-non-activation.md)では、人に届く表現／受容が対象にないため使わない。本例でもUXレビューが最初から同じ問いを挙げるなら、余分な文化的語彙を追加せず使わない。

再開に必要なのは、同じ固定材料を使った無接触の初回レビュー原文、別に記録したRasa接触後の問い、その差分について利用者理解・復旧行動など対象側資料による支持・反証である。別種の芸術・コミュニケーション事例の検討もあり得るが、**対象を後から変えてこの画面での追加発見を証明したことにはしない**。

## 文化・研究の境界

- Nāṭyaśāstra由来のRasaと、Abhinavaguptaらによる後の展開を混同しない。
- rasa / bhāvaを「画面を見た個人の一時的な気分」と同一視しない。
- 芸術的な美的経験を、あらゆるUXや一般心理学の普遍法則にしない。
- 個人の心理状態、罪悪感、失望、憤りを画面構成だけから推定・診断しない。

### 文献

- Natalia Lidova, *Rasa in Indian Aesthetics*, Oxford Bibliographies, 2026-06-26: https://academic.oup.com/reference/62382/reference-article-abstract/566568637
- Cambridge Core, *The Alchemy of Rasa in the Performer–Spectator Interaction*: https://www.cambridge.org/core/journals/new-theatre-quarterly/article/abs/alchemy-of-rasa-in-the-performerspectator-interaction/AAE15994E99A99227CAA627A2DB31777
- Nielsen Norman Group, *Error-Message Guidelines* (2023): https://www.nngroup.com/articles/error-message-guidelines/
- Nielsen Norman Group, *Hostile Patterns in Error Messages* (2022): https://www.nngroup.com/articles/hostile-error-messages/
- Nielsen Norman Group, *10 Usability Heuristics for User Interface Design*: https://www.nngroup.com/articles/ten-usability-heuristics/

**Disposition:** **large ordinary capability overlap, plausible ex-ante discovery overlap, not independently observed**. Keep `rasa` `adopted` with `discovery_hypothesis.evidence_state=unreviewed_hypothesis`. This document is neither a retention finding nor a demotion authorization.
