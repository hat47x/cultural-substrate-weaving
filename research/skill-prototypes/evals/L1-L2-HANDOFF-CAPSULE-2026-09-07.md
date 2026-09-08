# Layer 1 → Layer 2 Handoff Capsule Eval — 2026-09-07

Status: research regression fixture; not evidence of production readiness

## Purpose

`affinity-synthesis` の一回統合成果物を `iterative-inquiry-synthesis` へ渡す際に、

```text
carry-forward identity
    != reopen selection
    != continuation decision
```

であることを具体例で固定する。

このfixtureは特定JSON schemaをMethod Definitionへ固定するためのものではない。Agent Skill realization / representation間のhandoffが、既存のMethod invariantsを壊していないかを見る。

## Prior one-round synthesis

前roundのsemantic recordを簡略化して次のように置く。

```text
S11 := "target-side source with provenance/status that must remain traceable"

G03["制度上は接続するが、現場の判断基準はまだ共有されていない"]
G04["別の材料群は現在の問いには直接触れていない"]

X02: C17 ~> G04 :: "G03とは別の主配置だがG04にも響く"

U04 := "統合すると消える少数事例の温度差"
Q08? := "G03と別の判断層の間に条件付きの接続があるのか"
```

前roundのoptional handoff capsule:

```json
{
  "semantic_refs": ["G03", "G04", "X02", "Q08"],
  "residual_refs": ["U04", "Q08"],
  "source_refs_to_preserve": ["S11"],
  "next_check_candidates": [
    {
      "text": "Q08を区別できる新材料が得られたら再検査する",
      "refs": ["Q08", "G03"],
      "status": "candidate"
    }
  ],
  "do_not_assume": [
    "Q08が示唆する接続はまだexplicit relationとして支持されていない",
    "S11由来の仮説的解釈をtarget-side observationとして扱わない"
  ]
}
```

## Case A — New material touches only G03 / Q08

### New delta

新資料 `S12` が、G03の表札に含まれる「判断基準の非共有」へ直接関係し、Q08を区別する具体的な条件を一つ示す。

一方、

- G04の材料群
- X02のsecondary resonance
- U04の少数事例の温度差

には新しい情報を与えない。

### Expected Layer 2 intake

```text
carried from capsule:
  G03, G04, X02, Q08, U04, S11

actually reopened after reading S12:
  G03, Q08

not reopened merely because carried:
  G04, X02, U04
```

期待条件:

- `G04` を `= unchanged` と記録しない。今回触れていないので、再検査済みとは言えない。
- `X02` を再評価しない。capsuleにあることはreopen理由ではない。
- `U04` は残差として保持するが、S12が触れていないので今roundの中心へ持ち込まない。
- `S11` のprovenance / incoming statusは保持する。
- `S12` がQ08を十分に支持する場合でも、one-round synthesis側でpredicate / direction / basis / source-return checkを通してから `R` へ昇格する。

## Case B — Residual exists, but no discriminating material exists

前round終了時に `U04` と `Q08` が残っているが、新しいsource、counterexample、constraint change、explicit revisitがない。

### Expected result

```text
continue?  no automatic continuation
reason:    residual existence alone is not a round trigger
state:     preserve U04 / Q08 as reopenable anchors
```

未解決が残ることは失敗ではない。現在判別できる材料がなければ正常停止できる。

## Case C — Representation-only change

前roundのsemantic recordは同じまま、rendererをMermaidから別のcanvas rendererへ変えた結果、G03とG04の位置・edge routing・折返しだけが変わった。

### Expected result

- semantic reopenを開始しない。
- `G03 / G04 / X02 / U04 / Q08` のIDを振り直さない。
- layout変化をstructural deltaとして数えない。
- 新しい見た目からrelation candidateに気づいた場合は、そのcandidateを `Q` としてsourceへ戻してから扱う。

## Case D — Incoming epistemic status survives handoff

`S11` に由来するものが前roundでは `hypothesis` / `framework_generated candidate` 等のstatusだったとする。

新roundで同じ内容に似たtarget-side source `S13` が見つかった。

### Expected result

- S11由来candidateのorigin/statusを履歴から消さない。
- S13を独立したtarget-side supportとして別に記録する。
- 「S13が見つかったので、S11も最初からobservationだった」と遡及的に書き換えない。
- grouping geometryをS11/S13のmetadata分類だけで決めない。

## Case E — Global contradiction

新材料 `S14` がG03だけでなく、前round全体の前提を否定する反証だった場合。

### Expected result

局所reopen原則を機械的に守ってG03だけへ閉じ込めない。

```text
local delta rule
  + global contradiction reason
    -> broader reopen is allowed
```

ただし、どこまでreopenしたかと理由を外部artifactへ残す。

## Failure examples

次は回帰失敗とする。

1. capsuleの `semantic_refs` を全件、自動で `reopened prior artifacts` へコピーする。
2. 触れていない `G04` を `= unchanged` と記録する。
3. residualが残るだけで自動的に次roundへ進む。
4. `possible next check` をuser/current inquiryの確認なしに必須検索へ変える。
5. representation-only changeをsemantic discoveryへ数える。
6. handoffを跨いだことでhypothesisをobservationへ昇格する。
7. `X02` を独立supportまたは二重membershipとして数える。
8. global contradictionなのに局所reopenへ機械的に閉じ込める。

## Pass condition

このfixtureで求めるのは、特定の文面一致ではない。

少なくとも、

- carry-forward と reopen の分離
- touched subsetの局所再開
- residualとcontinue triggerの分離
- semantic deltaとrepresentation deltaの分離
- epistemic status / provenanceの維持
- global contradiction時の広域reopen許容

が成果物から追跡可能であればよい。
