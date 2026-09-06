# 親和統合の表現書式 — 既存Skill照合記録

作成日: 2026-09-06

## 目的

`affinity-synthesis` の方法内容だけでなく、group / label / relation / diagramをどの書式で外在化するかについて、既存Agent Skillの良い実装を比較し、取り込んだ点と取り込まなかった点を記録する。

書式を借りることと、そのSkillの方法論上の前提を丸ごと採用することを区別する。

## 1. Research Synthesis系

参照例:
https://github.com/SkillMedev/skills/blob/main/skills/research-synthesis/SKILL.md

### 良かった点

Themeを単なるtopic wordではなく、共有する意味を表すsentenceとして書く。

例の形式:

```text
Theme: "Remote teams ship faster but report weaker belonging."
  - source item
  - source item
```

これはKJ系の「表札を分類名にしない」という要請と相性がよい。

### 取り込み

- group `label` はcanonicalな意味文として保持する。
- 図で長すぎる場合だけ `display_label` を別に置く。
- `display_label` をcanonical labelへ逆流させない。

### 取り込まない点

- atomic claimを普遍的入力単位としない。
- confidence / evidence weightをgrouping geometryの既定軸にしない。
- synthesisからrecommendationへ自動進行しない。

## 2. Concept Map系

参照例:
https://github.com/bajpainaman/solve/blob/main/frameworks/concept-map.md

### 良かった点

一つの図だけで完結させず、次を別々に持つ。

- Mermaid raw diagram
- concept inventory table
- edge inventory table
- edge source / evidence
- downstream analysis

特にedge inventoryで `from / edge / to / source` を外在化する設計は、図だけに意味を預けない点で有用。

### 取り込み

親和統合では次を分離した。

```text
semantic record
  ├─ group inventory
  ├─ relation inventory
  ├─ residual / question inventory
  └─ diagram projections
```

relationは図の線ではなく、semantic record側にcanonical natural-language predicateを持つ。

### 取り込まない点

- controlled edge vocabularyをKJ系relationの閉じたtaxonomyにしない。
- すべてのnodeをexactly one semantic clusterへ強制しない。
- node/edge densityを意味の深さ・重要度へ変換しない。
- contradictionが必ず一定数存在するという数値規則を置かない。

## 3. Mermaid Diagram系

参照例:
https://github.com/mgranberry/mermaid-diagram-skill/blob/main/SKILL.md

### 良かった点

- diagram typeを目的から選ぶ。
- 図は単なるcard gridではなく、relation / flow / hierarchyを見せる。
- large diagramを複数zoomへ分ける。
- source生成で終わらずrenderして目視確認する。
- line crossing、label clipping、reading orderを検査する。

### 取り込み

親和統合ではdiagramを目的別projectionへ分けた。

- group relationship map
- membership map
- recursive hierarchy map
- focused lineage map
- spatial map

100+ cardを一枚のMermaidへ詰め込まない。

### 取り込まない点

外部Skillにある推奨node数等をMethod Definitionの固定上限にはしない。

可読性のための分割はrealization / renderer側のheuristicとする。

Mermaidはautomatic layoutなので、KJ系A型で距離・空白・中心／周縁そのものを保持したい場合の唯一の正本にはしない。

## 4. Excalidraw系

参照例:
https://github.com/diegosouzapw/awesome-omni-skills/tree/main/skills/excalidraw-studio

### 良かった点

- node / connection / hierarchyを先にstructured extractionする。
- diagram自体がmachine-readable JSONである。
- elementごとに座標を持てる。
- editable artifactとして後から人間が配置を動かせる。

### 取り込み

現在はExcalidraw形式そのものを正本にせず、`affinity-map`側へnormalized layout coordinatesを持てるようにした。

```json
"layout": {
  "projection": "spatial-map",
  "positions": {
    "G01": {"x": 0.18, "y": 0.42}
  }
}
```

このrecordから現在はSVGへ投影できる。将来Excalidraw / interactive canvasへ変換しても、semantic record側は変えない。

### 取り込まない点

- pixel coordinateをsemantic relationにしない。
- renderer固有のshape / color / fontをMethod Definitionへ入れない。
- Excalidraw JSONを親和統合の唯一の保存形式にしない。

## 5. 今回固まった表現分離

既存Skill比較を通して、少なくとも次を分離した方がよいと判断した。

```text
canonical semantic record
  card
  group
  higher-order group
  explicit relation predicate
  secondary resonance
  residual / question
  narrative + basis
  provenance / derivation
        ↓
projection labels
  display_label
        ↓
renderer projections
  Mermaid topology
  Mermaid hierarchy
  focused lineage
  free-position SVG
  future Excalidraw / interactive canvas
```

重要なのは、下流rendererの制約を上流semantic recordへ逆流させないことである。

## 6. 既存Skillを今後取り込むときの判定

新しいSkillやgraph表現を比較する場合、次の順で見る。

1. **Method-level value** — 材料の意味統合そのものを改善するか。
2. **Representation-level value** — group / relation / lineageをより損失少なく記述できるか。
3. **Renderer-level value** — 可読性、編集性、可搬性を改善するか。
4. **Packaging-level value** — progressive disclosure、template、eval、evidence管理を改善するか。

Representation / renderer上の長所だけを採用するとき、そのSkillのtaxonomy、scoring、fixed thresholdsまで一緒に持ち込まない。

## 現時点の結論

既存Skillは、KJ由来コアを置換するものとしてだけでなく、**外在化の文法・図の分割・監査可能な成果物設計の参照源**として有用である。

`affinity-synthesis` はその長所を取り込みつつ、意味の正本をrenderer非依存に保つ方向で進める。
