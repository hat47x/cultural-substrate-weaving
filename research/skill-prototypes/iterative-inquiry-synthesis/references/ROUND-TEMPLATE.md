# Iterative Inquiry Synthesis — Round Template

## Round

- **Round ID:**
- **Current inquiry / purpose:**
- **External constraints:**

## Input Delta

### New material

- 

### External exploration / epistemic handoff — when relevant

外部探索経路から来た問い、仮説、対応候補、実験結果等を次のsynthesisへ渡す場合に使う。

| Ref | Incoming status / role | Origin / operation | Target-side support | Handoff use |
|---|---|---|---|---|
| | | | | question / hypothesis / source material / context / other |

`Incoming status / role` は閉じたtaxonomyを要求しない。呼出側が `framework_generated`、`target_supported`、`cross_field_emergent`、`unresolved` 等の語彙を持つ場合は、その語彙を変換せず保持できる。web research、interview、experiment等では各経路の認識状態をそのまま記録してよい。

この欄のstatus / provenanceは**監査とhandoffのための情報**であり、one-round synthesisのgrouping geometryや独立support数へ自動変換しない。外部探索から来た仮説・correspondenceをtarget側の観察事実として渡さない。後にtarget側で独立に支持された場合は、元のoriginを消さず、何が新しく支持したかを別に記録する。

### Reopened prior artifacts

- 

### Why these prior artifacts were reopened

- 

### Touched semantic IDs when available

- Cards:
- Groups:
- Relations:
- Resonances:
- Residuals / questions:

stable IDを持つone-round synthesis artifact（例: `affinity-map`）がある場合、そのIDを再利用する。文面が似ているだけで新しいIDを大量に振り直さない。

## Synthesis Realization

- **Method / Skill:**
- **Version / ref if available:**
- **Input artifact refs:**
- **Output artifact refs:**
- **Representation / schema ref if available:**
- **External-status handoff preserved?:** yes / no / not applicable

## Structural Delta

compact notationを使う場合、次を変更操作として使える。

```text
+  newly emerged
~  changed
=  explicitly checked and unchanged
-  withdrawn / no longer supported
?  residual / unresolved remains
```

これはcardやgroupの意味分類ではない。**round間の変更状態**だけを表す。

例:

```text
+ C115 := "新材料から立った意味単位"
~ G03 := members + {C115}; label "旧表札" -> "新表札"
= G04 :: "new material checked; current label and membership still hold"
- R02 :: "withdrawn because the former direction is no longer supported"
+ R05: G03 -- G07 :: "新しく見えた関係predicate"
? Q08 :: "まだ区別できない問い"
```

### Newly emerged

- 

### Changed

- 

### Unchanged despite new material

- 

「未変更」は、触れていない構造を大量に列挙する欄ではない。今回のdeltaが実際に触れ、再検査したが意味上は変わらなかったものを記録する。

### Withdrawn / no longer supported

- 

`Withdrawn` は削除と同義ではない。過去roundの履歴を残し、現在は採用しない理由を記録する。

### Semantic vs representation delta

- **Semantic delta:** membership / label / explicit relation / resonance / residual / question の意味上の変化
- **Representation delta only:** wording normalization / ID display / renderer / line wrapping / visual layout のみの変化
- **Mixed:**

図のnode位置、Mermaidの自動layout、見栄えのための改行だけが変わった場合、それをsemantic discoveryとして数えない。

## Residuals

| Ref | Kind / description | Current state | What could reopen / clarify it |
|---|---|---|---|
| | gap / conflict / singleton / unresolved / free text | | |

`Kind` は便利な記述欄であり、閉じたtaxonomyへの分類を要求しない。

## Question Shift

- **Previous inquiry:**
- **Current inquiry:**
- **What caused the shift:**
- **What remains valid from the previous round:**

問いが変わらない場合は省略できる。

## Diagram / Projection Delta — optional

前roundと図が変わった場合だけ使う。

- **Projection:** group relationship / membership / lineage / spatial / other
- **Added visual elements:**
- **Removed visual elements:**
- **Layout-only changes:**
- **Does any visual change correspond to a semantic delta?:**
- **Projection integrity check:**

図だけに新しいrelationや包含が増えていないことを確認する。

## Continuation Boundary

- **Continue / Stop / Hand off:**
- **Reason:**
- **Possible next material or check:**
- **Requires human/domain decision?:**

## Round Handoff

次回に必要な局所情報だけを書く。

- Return to:
- Reopen when:
- Preserve incoming status / provenance for:
- Do not silently assume:
