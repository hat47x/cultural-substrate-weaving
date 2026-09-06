# 親和統合コアと反復統合の分離案

作成日: 2026-09-06

## 背景

CSWからKJ法由来の技能を分離する検討では、二つの異なる責務が一つの `integration.md` に同居している。

1. 一組の材料をカード化し、親和的に束ね、表札・関係配置・叙述へ統合し、元材料へ戻して検査する認知操作。
2. その統合結果に現れた空白、孤立、対立、未解決を次の情報収集や問いへ戻し、複数ラウンドで全体像を育てるオーケストレーション。

前者はKJ法／親和図法／質的統合法の系譜に強く属する。後者は、生成AIが大量の材料を持続的に扱い、検索・追加採取・再統合を安価に反復できる時代に合わせた拡張として理解した方が境界が明瞭になる。

したがって、公開Agent Skillとしても二層へ分ける案を第一候補とする。

## Layer 1: 親和統合コア

### 作業名

日本語: **親和統合コア**

英語候補: **Affinity Synthesis Core** / installable name candidate: `affinity-synthesis`

`親和図法` / `affinity-diagramming` そのものとは呼ばない。親和図法は一般に、カードを親和性でまとめ、図として構造化する方法として理解される。一方、このコアは図解後の叙述と、図解・叙述・元材料の相互検証まで含むため、`diagram` では射程が狭い。

`親和統合` はここでの記述的な作業名であり、既存の確立した一般名称であると主張しない。公開時には、KJ法・親和図法・質的統合法との系譜と差分を明示する。

### 責務

一回の統合ラウンドを完結させる。

```text
source material
  ↓
meaning-bearing cards
  ↓
affinity grouping / integration
  ↓
labels / higher-order units
  ↓
relational diagram
  ↓
narrative synthesis
  ↕
source / diagram / narrative cross-check
  ↓
residuals: singleton / tension / gap / unresolved
```

### 不変条件

- 先験的な分類体系を置かない。
- カードは機械的な最小断片ではなく、意味の生命を保つ単位とする。
- 意味の一体性を守るための結合と、証拠状態を守るための分割を同じ境界判定として扱う。
- カード化、表札化、上位統合では同じ意味統合コアを粒度を変えて使う。
- 束が揃う前に表札を固定しない。
- 元材料に無い因果、人物内面、一般化、評価方向、確度変更等を戻し検査する。
- source provenance と discovery route を分ける。
- 派生物や転載を独立反復として二重計上しない。
- 孤立、対立、曖昧さを早期に均さない。
- 図解から叙述し、叙述で生じた新しい関係を図解と元材料へ戻す。

### この層が所有しないもの

- 次ラウンドを実施するかどうか。
- 追加検索や資料収集の戦略。
- 問いを現状把握から本質追及、構想等へ切り替える進行管理。
- 文化体系を探索へ投入する判断。
- domain-specific recommendation / decision / action。

この分離により、親和統合コアは一回の認知変換として閉じる。

## Layer 2: 反復統合オーケストレーション

### 作業名

日本語候補:

- **反復統合**
- **反復探索統合**
- **循環型統合探索**

英語候補:

- **Iterative Synthesis**
- **Iterative Inquiry Synthesis**
- **Recursive Material Synthesis**

現時点の第一候補は、日本語 **反復探索統合**、英語 **Iterative Inquiry Synthesis** とする。

理由は、単に同じ要約を繰り返すのではなく、一回の統合から生じた `gap / conflict / singleton / unresolved question` を次の inquiry へ戻し、材料自体を増補・修正してから再統合するためである。

### 責務

複数ラウンドを管理する。

```text
Question / inquiry target
        ↓
material collection
        ↓
Affinity Synthesis Core
        ↓
structure + residuals
        ↓
What is still unknown / weak / contradictory?
        ↓
new question / new material / verification
        ↓
Affinity Synthesis Core
        ↓
...
```

各ラウンドでは、同じ親和統合コアを再利用する。ラウンドごとに別の統合アルゴリズムを持たない。

### ラウンド記録

最低限、次を外部から追跡できる形で残す。

- round identifier
- inquiry question / purpose
- input material references
- core method realization used
- produced cards / groups / map / narrative references
- residuals / gaps / conflicts
- next-round trigger
- 前ラウンドから何が変わったか

private chain-of-thought は保存しない。保存するのは外部から意味のある成果物と変化である。

### 次ラウンドを開始する条件

機械的な「必ずNラウンド」にはしない。

次のような外部から確認可能な理由がある場合に続行する。

- 空白が新しい情報収集先を示した。
- 対立する材料を判別する追加資料が得られる可能性がある。
- 孤立カードが新しい問題系を示している。
- 叙述化によって、図解へ戻すべき未検証関係が生じた。
- 新しい材料が入り、既存の束・表札・関係が変わる可能性がある。
- inquiry question が変化した。

### 停止条件

「空白がゼロになるまで」は採用しない。未知は常に残り得る。

次のいずれかで停止できる。

- 現在の問いに対して、追加ラウンドが実質的な構造変化を生まなくなった。
- 残差はあるが、現在取得できる材料では解けないことが明示できた。
- 利用目的に必要な粒度へ到達した。
- 次に進むにはdomain decision / human value judgment / external actionが必要になった。
- 追加探索の費用が、期待される認知上の改善を上回る。

## Layer 3: Cultural Substrate Weaving

CSWはLayer 1を所有しない。また、Layer 2の一般的な反復制御すべてを所有しない。

CSWの固有責務は、反復探索の途中で文化的・哲学的・伝統的体系を**認知場として接触させること**に限定する。

```text
Iterative Inquiry Synthesis
        ↓ optional exploration route
Cultural Substrate Weaving
        ↓
question / contrast / residual / correspondence candidate
        ↓
back to target material
        ↓
Affinity Synthesis Core
```

文化体系から得た対応は観察事実へ昇格させず、対象へ戻して検証する。この境界はCSWに残す。

## 既存 Affinity Mapping Skill との関係

`think-affinity-mapping` 等の既存Skillは、Layer 1のうち次の範囲をよく実装している。

- cluster before naming
- bottom-up grouping
- outlier preservation
- source-item traceability
- theme coherence check
- explicit deliverable template

依頼が「多数の既存項目を創発テーマへ束ねる」だけなら、既存Affinity Mapping Skillへ委ねる。

ただしLayer 1全体には、意味境界の分割／結合、核融合法的統合、戻し検査、証拠状態の継ぎ目、図解と叙述の往復があるため、現時点では既存Affinity MappingをLayer 1全体の realization とみなさない。

将来、外部SkillがLayer 1のmethod definitionとevaluation fixturesを満たせば、独自 realization を置換できる。

## 命名上の意味

この二層分離を採用すると、公開名へKJ法全体を背負わせる必要がなくなる。

- `affinity-synthesis` は、KJ法／親和図法系譜を受け継ぐ一回の材料主導統合を指す。
- `iterative-inquiry-synthesis` は、そのコアを生成AIが複数ラウンドで運用する拡張を指す。
- `cultural-substrate-weaving` は、反復探索へ文化体系を導入する専門Skillとして残る。

これにより、歴史的系譜、商標上の慎重さ、英語圏での理解性、生成AI時代の新規性を一つの名前へ無理に詰め込まずに済む。