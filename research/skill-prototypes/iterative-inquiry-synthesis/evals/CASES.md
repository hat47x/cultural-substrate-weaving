# Iterative Inquiry Synthesis — Evaluation Cases

Status: research fixtures

このfixtureはround数や特定文面を固定するためではない。multi-round orchestrationを変更したとき、差分再開・履歴保持・停止境界が壊れていないかを見る。

## Case 1 — 局所deltaで全体を作り直さない

### Prior state

```text
G01 — stable
G02 — stable
G03 — stable
R01: G01 -> G02
R02: G02 -> G03
```

### New material

C115はG02の表札とmembershipにだけ直接触れる。

### Expected handling

- G02をreopenする。
- G02変更がR01/R02へ影響するかを局所点検する。
- G01/G03が実際に影響を受けないなら、全面再clusterしない。
- G01/G03を「未変更」と大量列挙する必要もない。触れたものだけ記録する。

### Fail if

- 新カードが1枚来ただけで全カードを再カード化・再clusterする。
- 以前と文面が少し変わっただけの全groupへ新IDを振る。

## Case 2 — 全体前提を壊す反証なら広くreopenする

### Prior state

全体構造は「S1が独立資料である」という前提に強く依存している。

### New material

S1が実はS0の転載であり、独立corroborationではないと判明した。

### Expected handling

- 局所追補だけで済ませない。
- S1を独立supportとして重く使ったgroup / relation / narrativeをlineageから特定してreopenする。
- 影響範囲が全体ならglobal reopenを許容する。
- 以前のroundを削除せず、「独立性前提が崩れた」deltaとして残す。

### Fail if

- `reopen only what delta touches` を文字通り狭く読み、全体への波及を調べない。
- 逆に、何でもglobal restartにする。

## Case 3 — 新材料を確認しても構造が変わらないことは成果になり得る

### New material

C116はG04と近いが、元材料へ戻すとG04の既存表札とmembershipを修正する必要はない。

### Expected delta

```text
= G04 :: new material checked; current semantic core still holds
```

必要ならC116をG04へ追加できるが、「新しいテーマを発見した」と誇張しない。

### Fail if

- 毎round必ず新しい島・関係・洞察を作る。
- 変更がなかったことを「何もしていない」として記録から消す。

## Case 4 — renderer変更をsemantic discoveryにしない

### Prior state

G01とG02のsemantic recordは同じ。

### Round change

Mermaidの自動layoutでG01が左から上へ移動し、edge labelの改行位置も変わった。

### Expected handling

```text
Representation delta only
- node placement changed
- line wrapping changed
Semantic delta: none
```

### Fail if

- 上下配置になったため「G01がG02より上位」と解釈する。
- 見た目の近接が増えたため新Rを作る。

## Case 5 — 問いの変更で過去roundを書き換えない

### Prior inquiry

「なぜ利用が減ったか」

### New material

減少量より「誰が残ったか」の方が重要だと分かり、現在の問いが「残った人は何を支えに継続したか」へ変わる。

### Expected handling

- previous inquiryをそのまま履歴へ残す。
- current inquiryを新しく記録する。
- shiftを起こした材料を残す。
- 以前の構造のうち何がまだ利用できるかを明示する。

### Fail if

- 過去roundの問いを現在の問いへ書き換える。
- 問いが変わったことを以前のroundの「失敗」とみなす。

## Case 6 — 未解決を残して正常停止できる

### State

Q08は重要だが、現在入手できる資料では区別できない。

現在の利用目的には、Q08以外の構造で十分対応できる。

### Expected handling

- Q08とreopen conditionを残す。
- stopを正常な境界として記録する。
- gapゼロを目指して推測で埋めない。

### Fail if

- 「未解決があるから続ける」と無限round化する。
- 停止のためにQ08をもっともらしい仮説で閉じる。

## Case 7 — round数を使い切ることを目的にしない

### Configuration

最大10roundまで作業できるが、Round 4で現在の目的に十分な粒度へ達した。

### Expected handling

Round 4で停止できる。

`max rounds = 10` は使い切るべきquotaではなく、必要なら設けるhard budgetである。

### Fail if

- 10まで回さないと浅いと判断する。
- 新材料がないのに「もう一周」する。

## Case 8 — synthesis realization変更とmaterial deltaを混同しない

### Round A

同じ材料をrealization `affinity-synthesis/v0.1` で統合した。

### Round B

材料は変えず、比較のため `external-affinity-skill/x` で再統合した。

### Expected handling

- input material delta = none
- realization delta = changed
- 出力差を「世界について新しい事実が増えた」と扱わない。
- realization差で生じた構造差をpaired comparisonとして記録する。

### Fail if

- method変更による差をmaterial由来の新発見としてbankする。

## Case 9 — secondary resonanceの追加はcard複製ではない

### Prior state

C072 primary membership → G_A

### New round

別材料との接触で、C072がG_Dにも強く響くことが見えた。

### Expected delta

```text
+ X072D: C072 ~> G_D :: "newly visible resonance / not membership"
= C072 primary membership → G_A
```

### Fail if

- C072を複製してG_Dへ独立cardとして追加する。
- G_Aから自動的に移動させる。

## Case 10 — narrativeから新relationが見えても即bankしない

### Prior map

G01とG05にexplicit relationはない。

### Narrative round

文章化中に「G01がG05の前提条件なのでは」という関係候補が生じた。

### Expected handling

- narrative-generated candidateとして記録する。
- source / mapへ戻す。
- 支持されれば新Rとして追加する。
- 支持不足なら? / residualへ残す。

### Fail if

- 流暢な文章に現れた接続詞だけで新Rを確定する。

## Cross-realization comparison

実装A/Bを比較する場合は、少なくとも次を見る。

| Check | A | B | Notes |
|---|---|---|---|
| unnecessary global rebuild | | | |
| touched-artifact localization | | | |
| global contradiction propagation | | | |
| stable-ID preservation | | | |
| semantic vs representation delta | | | |
| question-shift history | | | |
| unresolved-safe stop | | | |
| no forced round count | | | |
| realization delta separated from material delta | | | |
| resonance without duplication | | | |

重大な履歴破壊やunsupported semantic promotionが一つでもあれば、平均的な読みやすさで相殺しない。
