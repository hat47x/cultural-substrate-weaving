# 既存Agent Skillの比較・吸収プロセス

作成日: 2026-09-06

## 目的

KJ法由来／親和統合系の独自Skillを設計するとき、既存Skillを「採用するか、自作するか」の二択にしない。

既存Skillには、方法内容だけでなく、起動条件、非適用条件、成果物契約、品質検査、エビデンス記述、テンプレート、eval設計など、Agent Skillとして成熟した実装上の工夫がある。

本プロセスは、それらを系統的に比較し、方法の核を壊さないものだけを取り込むための手順を定める。

## 原則

### 方法系譜とSkill実装を分ける

あるSkillの手順が採用できなくても、そのSkillの `When NOT to Use`、output contract、quality checklist、evidence dossier構造などは採用できる場合がある。

逆に、見た目が近い手順でも、こちらのmethod invariantsを壊すなら取り込まない。

### 名前ではなく機構を比較する

`KJ`, `Affinity Mapping`, `Qualitative Synthesis`, `Thematic Analysis` などの名称一致を採否理由にしない。

比較単位は、何を入力とし、どの認知操作を行い、何を保持・捨象し、何を成果物として出すかである。

### 吸収は差分として記録する

外部Skillの記述を丸ごとコピーしない。

取り込む候補ごとに、次を記録する。

- source skill / version / commit
- candidate mechanism or packaging feature
- why it may help
- which local invariant it touches
- expected benefit
- plausible harm / regression
- evaluation fixture
- decision: adopt / adapt / reject / defer

ライセンスや帰属条件が必要な場合は別途確認する。

## Step 1: Discovery

比較対象を複数系統から集める。

優先するもの:

- Affinity Mapping / Affinity Diagramming
- qualitative synthesis
- interview / research synthesis
- concept / relationship mapping
- evidence / inference audit
- iterative / recursive research workflows
- Agent Skill authoring frameworks with strong eval practice

同名Skillだけを探さない。類似機構を別名で実装しているものも対象にする。

## Step 2: Capability decomposition

各Skillを、最低限次の軸で分解する。

| 軸 | 見るもの |
|---|---|
| Trigger | いつ起動するか |
| Anti-trigger | いつ使わないか |
| Input contract | 何を入力とみなすか |
| Unit formation | 項目・カード・claim等をどう作るか |
| Grouping / integration | 何を基準に統合するか |
| Labeling | theme / label / synthesisをどう立てるか |
| Relation mapping | 束同士の関係を扱うか |
| Narrative | 図やテーマから文章へ移るか |
| Back-check | 元材料へ戻る検査があるか |
| Residuals | outlier / gap / conflictをどう扱うか |
| Provenance | 元材料追跡をどう保持するか |
| Epistemic boundary | fact / inference等の境界をどう扱うか |
| Iteration | 次ラウンドへの戻りがあるか |
| Output artifact | 成果物を何と定義するか |
| Quality gate | 自己検査をどう行うか |
| Evidence discipline | 方法の有効性をどこまで主張するか |
| Eval assets | examples / fixtures / negative casesの有無 |

## Step 3: Local invariant check

候補を現行のmethod invariantsへ当てる。

特に次を壊さないこと。

- meaning-bearing unit を機械的atomicityへ戻さない。
- provenance metadata を最初の意味距離にしない。
- observation / interpretation 等の epistemic seam を潰さない。
- derived material を independent repetition として数えない。
- singleton / tension / unresolved を強制的にテーマへ収容しない。
- fluent synthesis によって元材料にない因果・内面・一般化を加えない。
- diagram と narrative の片方だけを正本化しない。

## Step 4: Feature classification

外部Skillの長所を三種類に分ける。

### A. Method-level adoption

認知操作そのものとして採用する候補。

例:

- `cluster before naming`
- source itemへの戻り検査
- outlierを消さない

採用にはmethod fixtureでの検証を要求する。

### B. Realization-level adoption

Agent Skillとしての実行しやすさを改善するが、方法定義は変えないもの。

例:

- `When to Use / When NOT to Use`
- step numbering
- concise operational language
- referencesの段階的ロード
- model向けnegative instructions

method definitionではなくSkill realizationへ入れる。

### C. Packaging / governance adoption

Skillの保守品質を高めるもの。

例:

- evidence dossier
- output template
- quality checklist
- example / counterexample
- eval negative cases
- evidence tier / transferred-evidence disclosure

これは積極的に取り込んでよいが、外部Skill独自の数値基準や評価尺度をそのままコピーしない。

## Step 5: Candidate test

候補を一つずつ、小さな差分としてfixtureへ当てる。

最低限、次を比較する。

- source fidelity
- overfragmentation
- overcompression
- premature taxonomy
- invented causality / interior state / generalization
- epistemic seam preservation
- singleton / conflict preservation
- derivation double-counting
- provenance round-trip
- diagram ↔ narrative consistency
- low-capability modelでの再現性

改善が一つあっても、別の重要なinvariantを悪化させるならそのまま採用しない。

## Step 6: Adopt / Adapt / Reject / Defer

### Adopt

方法境界と矛盾せず、fixtureでも改善する。ほぼそのまま考え方を導入できる。

### Adapt

良い機構はあるが、こちらのmethod invariantsに合わせて意味を変える必要がある。

### Reject

目的や停止条件が異なり、取り込むと方法を別物にする。

### Defer

有望だが一次資料、ライセンス、評価材料等が不足する。

決定理由を残す。

## `think-affinity-mapping` から現時点で取り込みたいもの

参照:
https://github.com/product-on-purpose/thinking-framework-skills/tree/main/skills/think-affinity-mapping

### Adopt / Adapt候補

1. **Cluster before naming**
   - 現行の「束が揃う前に表札を書かない」と一致する。
   - Skillの起動文とquality checklistでも明示する。

2. **明確な When to Use / When NOT to Use**
   - 現行KJ_TECHNIQUEは方法の姿勢は強いが、他Skillとどう使い分けるかが弱い。
   - 独立Skillでは必須にする。

3. **Outliersを成果物に残す**
   - 現行の孤立カード保持と一致する。
   - `parking lot` という語をそのまま正本語彙にはせず、singleton / residualとして明示する。

4. **Theme/item traceabilityを成果物契約に含める**
   - 現行のprovenance設計と整合する。
   - ただし「代表例だけ」ではなく、必要時に全カードへ戻れることを維持する。

5. **Named theme が weak grouping を laundering し得るという警告**
   - 現行の「表札が分類名へ逃げる」検査とよく補完する。
   - `coherence` を検査観点として取り込む価値がある。

6. **Evidence dossierをSkill本文から分離する構造**
   - 方法論上の主張、系譜、一次／二次資料、AIへの transferred evidence を別ファイルで管理する。
   - 公開Skillの本文を根拠説明で肥大化させない。

7. **AI利用についてhuman evidenceからの移転であることを明示する**
   - 生成AI版のKJ／親和統合は直接の実証が乏しい。AI向けに再構成した部分と原方法を区別する。

8. **Template / Example / Checklist の分離**
   - method definitionと具体的な出力形式を分離し、必要なときだけロードする。

### そのままは取り込まないもの

1. **少数項目なら停止する固定基準**
   - KJ由来の統合は少数の強い材料でも意味がある場合がある。適用可否を件数だけで決めない。

2. **theme size / weight を標準成果物とすること**
   - 多数性はsalienceの一情報ではあるが、真実性・重要性とは別。派生・転載の二重計上問題もある。
   - 必要な用途でのみオプションとして扱う。

3. **全入力をdiscrete comparable unitへ先に均すこと**
   - 意味の一体性を壊すatomic化につながり得る。

4. **clustered theme mapを唯一の最終成果とすること**
   - 親和統合コアでは、関係配置と叙述、および相互検証までを扱う。

## 更新サイクル

公開後も、類似Skillを定期的に比較する。ただし「新しいSkillが出た」というだけで方法を変更しない。

外部Skillから新しい候補を取り込む場合は、必ずこの順にする。

```text
external observation
  ↓
feature candidate
  ↓
local invariant review
  ↓
fixture / paired evaluation
  ↓
adopt / adapt / reject / defer
  ↓
method definition or realization change
```

単一の好例から方法正本へ直接promoteしない。CSW Living Labで採用している「観察と正本変更を分ける」考え方を、外部Skill学習にも適用する。