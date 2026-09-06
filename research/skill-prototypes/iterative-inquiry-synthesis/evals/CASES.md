# Iterative Inquiry Synthesis — Contract Cases

Status: research fixture; no empirical result is implied

このfixtureは、`references/METHOD.md` の不変条件を、後続のprototype evaluationで同じ入力へ繰り返し当てられる形へ落としたものです。

ここでは「このSkillが有効だった」という結果を記録しません。各caseについて、**prior state / new delta / required external behavior / invalid behavior** を定義します。実際のmodel runやpaired comparisonでは、出力がこの契約をどこまで満たしたかを別記録へ残します。

## 共通判定軸

すべてのcaseで、少なくとも次を確認します。

- roundを全面再開始ではなく差分として扱う。
- 触れたartifactと、触れていないartifactを区別する。
- old structureを保存すること自体を成功条件にしない。
- semantic deltaとrepresentation-only deltaを混同しない。
- 使用したone-round synthesis realizationを追跡できる。
- residual / unresolvedを消すために推測を事実化しない。
- stop / continue / handoff理由を外部から説明できる。
- private chain-of-thoughtではなく、外部成果物だけを履歴へ残す。

---

## Case 1 — 局所deltaは局所reopenする

### Invariants

I1, I2, I4, I13

### Prior state

- `G01`: 「利用開始時の迷い」 — `C01`, `C02`
- `G02`: 「継続後の手応え」 — `C03`, `C04`
- `R01`: `G01 -> G02` の時間的推移candidate
- `Q01`: 「開始前の迷いを減らした要因は何か」

### New delta

`C05`: 開始前の説明文を読んだことで不安が一部減った、という新しい観察が追加された。

`C05` は `G01` と `Q01` に直接関係するが、`G02` の内容には新しい情報を与えない。

### Required external behavior

- `G01` / `Q01` をreopen対象として示す。
- `G02` を無理由に再構成しない。
- `G01` のmembershipやlabelが変わる場合は `~` として差分を示す。
- `G02` を実際に再検査した場合だけ `=` として「触れたが変わらない」を記録できる。
- stable IDが意味上継続するなら `G01`, `Q01` を維持する。

### Invalid behavior

- 新材料が来たという理由だけで全card/group/relationへ新IDを振る。
- `G02` の表札を、今回のdeltaと無関係に言い換えて「新しい構造」と数える。
- `C05` だけから `R01` の因果を確定する。

---

## Case 2 — global contradictionでは広いreopenを許す

### Invariants

I2, I3, I4

### Prior state

- `G10`: 「遅延の主因は外部承認待ち」
- `G11`: 「内部実装は予定どおり進行」
- `R10`: `G10` が全体遅延を説明する中心relationとして採用中

### New delta

一次資料が見つかり、外部承認は予定どおり完了していた一方、内部実装がその後2週間停止していたことが確認された。

### Required external behavior

- 今回は局所追補だけでは足りない理由を明示し、`G10`, `G11`, `R10` を広くreopenする。
- 旧構造を履歴から削除せず、現在採用できない要素は `-` または弱化として残す。
- 新しいgroup / relationが必要なら、旧IDとのderivationを残す。
- 「既存を安易に壊さない」を理由に反証を旧groupへ押し込まない。

### Invalid behavior

- 旧構造を守るため、一次資料を例外扱いして中心relationを維持する。
- 以前のroundが存在しなかったかのように履歴を書き換える。
- 全体を再生成しただけで、何が反証によって変わったかを示さない。

---

## Case 3 — question shiftを版管理する

### Invariants

I6, I9

### Prior state

- previous inquiry: 「どの案を採用すれば実装時間を最小化できるか」
- 現在までの材料はA案/B案の工数比較を中心に統合されている。

### New delta

利用部門から「導入後に現場が自力で変更できること」が必須条件として追加された。

### Required external behavior

- current inquiryを、たとえば「実装時間と運用時の自律変更可能性を両立する案はどれか」へ更新できる。
- previous inquiryを履歴上そのまま残す。
- 問いを変えた外部条件を記録する。
- 旧roundの工数比較のうち、現在も有効な部分を明示する。

### Invalid behavior

- 過去roundの問いを新しい問いで上書きし、当初の比較目的を消す。
- 問いが変わったことを「前roundが失敗だった」と自動評価する。
- 新必須条件を受けても、工数だけの旧問いを固定stageとして維持する。

---

## Case 4 — unresolvedを残した正常停止

### Invariants

I5, I7, I8

### Prior state

- `Q20`: 二つの証言の食い違いが未解決。
- 追加資料候補として非公開議事録の存在が示唆されている。

### New delta

現時点では議事録へアクセスできず、他に独立した確認源も見つからない。

### Required external behavior

- `Q20` をunresolvedとして保持する。
- 「現時点で取得できる材料では判別できない」をstop reasonにできる。
- reopen条件として、議事録入手や別の独立証拠の出現を残せる。
- gapが残っていても正常停止として扱う。

### Invalid behavior

- 完了感を作るため片方の証言を推測で採用する。
- `gap == 0` にするため `Q20` を削除する。
- 新材料がないのにround数を増やすこと自体をcontinue理由にする。

---

## Case 5 — synthesis realization切替をmaterial deltaと混同しない

### Invariants

I10, I4

### Prior state

- Round 3では `affinity-synthesis@0.1-research` を使用。
- 同一入力集合から `G30`, `G31`, `R30` が得られている。

### New delta

材料は追加されていない。ただし比較目的で、Round 4では別のcompatible synthesis realizationを同じ入力へ適用する。

### Required external behavior

- 使用realizationが変わったことを明示する。
- 出力差が出ても、material changeによる差と断定しない。
- semantic differenceがある場合、「realization差の影響を含む比較対象」として分離して記録する。
- prior snapshotを保持する。

### Invalid behavior

- realization変更を記録せず、新しい表札やrelationを新材料由来の発見とみなす。
- 同じ入力を別modelで処理しただけで「時間とともに構造が変化した」と扱う。

---

## Case 6 — representation-only deltaをsemantic discoveryへ昇格させない

### Invariants

I14

### Prior state

semantic record:

- `G40`: members `C41`, `C42`
- `G41`: members `C43`, `C44`
- `R40`: `G40 -- G41` 「相互に制約する」

projectionはMermaidで描画されている。

### New delta

renderer更新により、`G40` が図の左から上へ、`G41` が右から下へ移動した。edge routingも変わった。semantic record自体は変更されていない。

### Required external behavior

- representation-only deltaとして記録する。
- nodeの上下位置を階層、因果、優先度へ変換しない。
- semantic recordに変化がないなら、新relationを追加しない。
- 見た目から新relation candidateに気づいた場合は、候補として材料とsemantic recordへ戻して検査する。

### Invalid behavior

- 「上に来たから上位概念になった」とみなす。
- edgeの曲がり方をrelation changeとして数える。
- diagram diffだけを根拠に `+ R41` を確定する。

---

## Case 7 — stable IDは同一性を保ち、splitではderivationを残す

### Invariants

I13, I9

### Prior state

- `G50`: label「利用時のためらい」, members `C51`, `C52`, `C53`

### New delta A

新材料 `C54` が入り、labelが「利用開始時のためらい」へ微修正されるが、groupの核と既存membershipの意味上の同一性は維持される。

### Required behavior A

- `G50` を維持し、`~ G50` としてlabel/membership差分を記録できる。
- 微修正だけで `G51` を新設しない。

### New delta B

その後、`C51`, `C54` は「操作への不安」、`C52`, `C53` は「周囲の評価への不安」という別々の意味核を持つことが追加材料で明確になった。

### Required behavior B

- splitが必要なら新しいgroup IDsを立てる。
- 新groupが `G50` から派生したことを記録する。
- `G50` の過去round履歴を削除しない。

### Invalid behavior

- Aの段階で単なる文言変更を理由に全IDを振り直す。
- Bの段階でID継続を優先し、異なる意味核を一つのgroupへ押し込む。

---

## Case 8 — 外部探索routeの認識状態を保持する

### Invariants

I11, I5

### Prior state

- `Q60`: 「この対立は役割境界の違いから生じているのか」
- 対象側材料だけでは未判別。

### New delta

外部のcultural framework探索から、「境界の内外」という対応候補と追加質問が生成された。ただし対象側の新観察はまだない。

### Required external behavior

- framework由来のcorrespondence / questionであることを保持する。
- `Q60` の次の確認先として利用できる。
- target-supported findingへ自動昇格させない。
- 次roundで対象材料が得られたとき、そこで初めてsupport状態を再評価する。

### Invalid behavior

- 文化体系が示した対応を「対象の構造が確認された」と書く。
- 同じframework内の別表現を独立した対象証拠として二重計上する。

---

## Case 9 — one-round synthesisをLayer 2が再実装しない

### Invariants

Relationship to Affinity Synthesis / Realization boundary

### Prior state

新しい材料集合 `M70` があり、one-round meaning integrationが必要である。

### New delta

compatible `affinity-synthesis` realizationが利用可能である。

### Required external behavior

- Layer 2はcurrent inquiry、reopened refs、input delta、realization binding、round後のstructural deltaとcontinuation boundaryを扱う。
- grouping / labeling / return-checkの内部手順はcompatible realizationへ委ねる。
- 受け取ったartifact refs / residualsをround snapshotへ接続する。

### Invalid behavior

- Layer 2側で独自の別grouping algorithmを追加し、どちらが正本か分からなくする。
- realizationを呼んだかどうかを記録せず、「統合した」とだけ書く。

---

## 後続evaluationで記録するもの

各実行記録は、fixture本文を直接「合格」に書き換えません。別ファイルへ次を残します。

- case id
- model / realization / version
- input refs
- output refs
- required behaviorごとのobserved / not observed / unclear
- invalid behaviorの有無
- representation-only差の有無
- evaluator interpretation
- unresolved evaluation questions

単一model・単一runの成功をMethod Definitionの妥当性証明にはしません。fixtureは、paired comparisonやrealization差し替え時に同じ境界を再確認するための基準です。
