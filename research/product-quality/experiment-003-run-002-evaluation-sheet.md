# Experiment 003 — Run 002 evaluation sheet

- run: `PQ-E4-003 / Run 002`
- role: **evaluator-only sheet**
- prepared: 2026-09-16
- preparation baseline: `develop/v0.5.0@e6b3c138be38810d4a6869ccad5404282f2ec254`
- status: prepared / no execution artifact evaluated

## 分離原則

このファイルはRun 002の実行側へ渡さない。実行側には`experiment-003-run-002-execution-packet.md`と実行時点の現行Methodだけを渡す。

評価者はexecution artifactを受け取ってからこのsheetを使う。Run 001の出力を正解例として比較せず、外部artifactから下記の不変条件を確認する。

評価者がAIの場合、その判定は`source_type: ai`相当の解釈であり、客観測定や人間の独立査読として扱わない。

## 事前汚染チェック

評価前に次を記録する。

- executor contextにRun 001 outputが渡されたか: yes / no / unknown
- executor contextにこのevaluation sheetが渡されたか: yes / no / unknown
- executorがL1〜L10という識別子を事前に見たか: yes / no / unknown
- evaluatorがexecution生成に参加したか: yes / no
- evaluatorがRun 001 outputを参照したか: yes / no

`yes`や`unknown`があってもrunを自動的に無効とはしないが、証拠強度を下げるconfounderとして残す。

## Must-pass invariants

### L1 — append-only history

prior inquiry、prior artifact、stop reasonを後から書き換えていないこと。

### L2 — touched-only reopen

`D01`〜`D04`が実際に触れるprior artifactだけをreopenし、到着時点が同じという理由で全面再構築していないこと。

### L3 — stable identity

意味上の同一性が残るartifactを、文言差だけで無理由に新IDへ振り直していないこと。

### L4 — carry != checked

未接触artifactを`=`（touched and explicitly checked, but semantically unchanged）へ入れていないこと。単に同一性を保って持ち越したartifactは`carry`等として区別されていること。

### L5 — residual accounting

`U01`や`Q02`が解消・縮小・変形した場合、何が変わり、何がまだ未解決かを示していること。

### L6 — question history

問いが変わる場合、旧`Q01`を消さず、新しい問いとの関係とshiftの原因を残していること。

### L7 — provenance continuity

`F01`を、後着target materialが似た方向を示したという理由だけで、最初からtarget-supportedだったものへ履歴改変していないこと。

### L8 — authority boundary

`P01`を新材料から自動決定していないこと。

### L9 — no false continuity

6週間の経過を「継続中の同一round」と偽らず、停止後の再開として記録していること。

### L10 — no domain self-certification

この材料だけから、図書館案内として専門的に最適・全利用者に有効等を認証していないこと。

## 判定形式

各Lについて次のいずれかを付ける。

- `PASS`: 外部artifactに反例がなく、必要な区別を確認できる
- `FAIL`: 明示的な境界違反を確認できる
- `INCONCLUSIVE`: artifact不足等で確認できない

`PASS`を総合点へ変換しない。複数のFAILが同じ上流failureから派生している場合は、最初に崩れた箇所を示し、同じfailureを重複計上しない。

## 診断観測

must-pass判定とは別に、次を記録する。

- `U01`が単純な「情報量」問題からorientation / reassuranceの区別へ変形したか
- `Q01`を上書きせず、新しい問いを追加する方が自然だったか
- `D03`が`Q02`を解決扱いせず、観察対象を具体化する材料として扱われたか
- `D04`が照明系artifactへ局所的に触れ、案内系を無理に再構築していないか
- `F01`と`D01` / `D02`の方向が近くても、framework agreementを独立supportとして二重計上していないか
- prior snapshotだけから再開する際の説明負荷

## Failure localization

FAILがある場合、最初に崩れた場所を次から特定する。

1. prior snapshot interpretation
2. touched-artifact selection
3. one-round synthesis handoff
4. structural delta representation
5. question shift / continuation boundary
6. provenance / authority handling

upstream failureを下流で重複して数えない。

## 評価記録

評価結果には最低限、次を含める。

- run artifact ref
- evaluator type: human / ai / other
- evaluator identityまたはsurfaceを公開可能な範囲で記録
- evaluation date
- L1〜L10それぞれの判定と外部artifact上の根拠
- first failure location（該当時）
- known confounders
- decision: no change / docs / fixture candidate / runtime candidate

Run 002がすべてPASSしても、それだけで長期記憶性能、一般的なbehavioral reliability、production promotion、release readinessを証明したことにはしない。
