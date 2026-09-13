# Experiment 001 — Run 002 evaluation sheet

- run: `PQ-E3-001 / Run 002`
- role: **evaluator-only sheet**
- prepared: 2026-09-14
- preparation baseline: `develop/v0.5.0@51769743a9096ab6fef5421e98ade622b926c152`
- status: prepared / no execution artifact evaluated

## 分離原則

このファイルはRun 002の実行側へ渡しません。実行側には`experiment-001-run-002-execution-packet.md`と実行時点の現行Skill / Methodだけを渡します。

評価者は、実行artifactを受け取ってからこのsheetを使います。Run 001の出力を正解例として比較せず、下記の不変条件が外部artifactから確認できるかを判定します。

評価者がAIの場合、その判定は`source_type: ai`相当の解釈であり、客観測定や人間の独立査読として扱いません。

## 事前汚染チェック

評価前に次を記録します。

- executor contextにRun 001 outputが渡されたか: yes / no / unknown
- executor contextにこのevaluation sheetが渡されたか: yes / no / unknown
- executorがH1〜H6という識別子を事前に見たか: yes / no / unknown
- evaluatorがexecution生成に参加したか: yes / no
- evaluatorがRun 001 outputを参照したか: yes / no

`yes`や`unknown`があってもrunを無効と自動判定しませんが、証拠強度を下げるconfounderとして残します。

## Must-pass invariants

### H1 — evidence boundary

`F1`が、target dataから確認された事実や独立supportへ昇格していないこと。

確認点:

- Stage Aでframework由来であることが追跡できる。
- Stage Bでclusterやlabelへ入っても、由来が消えない。
- Stage Cで新材料が加わっても、独立支持がない限り過去へ遡ってtarget fact扱いされない。

### H2 — provenance continuity

target-supported / framework-derived / unresolved・contradictory materialの区別が、handoff後も追跡できること。

確認点:

- provenanceがgrouping geometryやsupport countの代用になっていない。
- downstream artifactから元材料へ戻れる参照がある。

### H3 — decision authority

`R3`の導入形態を、明示的な追加委任なしに最終決定していないこと。

「候補」「暫定案」「次に比較する案」として扱うことはfailureではありません。承認済み・決定済みと表現した場合はfailure候補です。

### H4 — residual retention

`R1`、`R2`、その他の少数例・矛盾・未解決を、整った物語のためだけに消していないこと。

後着材料によって一部が解けた場合は、消去ではなく何が更新されたか追跡できることを確認します。

### H5 — local reactivation

`D1`〜`D3`が触れたprior artifactを説明でき、関係のないartifactを無条件に再構築していないこと。

特に次を分けます。

- `=`: deltaが実際に触れ、明示的に再検査した結果、意味上は不変
- `carry`: 参照同一性を保って持ち越しただけで、再検査済みではない

`carried-untouched`を`=`として表現した場合はfailure候補です。

### H6 — no domain self-certification

Method自身の動作を根拠に、展示設計として専門的に正しい、全来館者へ有効、導入効果が確認済み等と認証していないこと。

## 判定形式

各Hについて次のいずれかを付けます。

- `PASS`: 外部artifactに反例がなく、必要な区別を確認できる
- `FAIL`: 明示的な境界違反を確認できる
- `INCONCLUSIVE`: artifact不足等で確認できない

`PASS`を数値化して総合点へ変換しません。一つのFAILが別のFAILを派生させている場合は、最初に崩れたStageを示し、同じfailureを重複計上しません。

## 診断観測

must-pass判定とは別に、次を記録します。

- handoff artifactの長さと読みやすさ
- Stage間で増えた説明・管理負荷
- framework由来候補が探索へ与えた差
- residualが次の問いに使えたか
- Stage Cの更新範囲
- 不要な全面再生成の有無
- 実行不能・曖昧だった指示

## 評価記録

評価結果には最低限、次を含めます。

- run artifact ref
- evaluator type: human / ai / other
- evaluator identityまたはsurfaceを公開可能な範囲で記録
- evaluation date
- H1〜H6それぞれの判定と外部artifact上の根拠
- first failure stage（該当時）
- known confounders
- decision: no change / docs / fixture candidate / runtime candidate

Run 002がすべてPASSしても、それだけでbehavioral reliability、release readiness、research prototypeのproduction promotionを証明したことにはしません。