# 外部Skill機能の採否ログ — 第1巡

作成日: 2026-09-06

対象prototype:

- `research/skill-prototypes/affinity-synthesis/`
- `research/skill-prototypes/iterative-inquiry-synthesis/`

このログは、外部Skillを一式コピーせず、機構・realization・packagingを分けて比較した最初の採否記録である。

## 1. `think-affinity-mapping`

Source:
https://github.com/product-on-purpose/thinking-framework-skills/tree/main/skills/think-affinity-mapping

### Adopt — cluster before naming

**外部の良さ:** theme名を先に作ると、その名前が磁石になって異質なitemまで引き寄せるため、まずclusterを作り後で名付ける。

**ローカル照合:** 現行KJ系の「束が揃う前に表札を書かない」と一致する。

**採用先:** `affinity-synthesis/SKILL.md`

### Adopt — explicit anti-trigger

**外部の良さ:** `When NOT to Use` が明示され、issue tree等の近接Skillとの境界が分かる。

**ローカル照合:** 現行 `integration.md` は方法内部は強いが、Skill ecosystemでの非適用境界が弱かった。

**採用先:** `affinity-synthesis/SKILL.md`

### Adapt — outlier / parking lot

**外部の良さ:** clusterに入らないitemを消さない。

**ローカル照合:** 現行の孤立カード保持と一致するが、`parking lot` は一時的に脇へ置くニュアンスが強い。

**採用:** `singleton / residual` としてより強く保持する。

### Adapt — traceability

**外部の良さ:** 各themeからsource itemへ戻れる。

**ローカル照合:** 現行はsource provenance / discovery route / derivationまで区別する。

**採用:** traceabilityを保持しつつ、来歴モデルはローカル側を維持する。

### Adopt — label can launder weak grouping

**外部の良さ:** confident theme nameがweak clusterを発見のように見せる危険を明示する。

**ローカル照合:** 表札の可搬性検査と補完関係にある。

**採用先:** Quality Checklist。

### Adopt — evidence dossier separation

**外部の良さ:** runtime Skillから系譜・根拠・限界を分ける。

**採用先:** `evidence/dossier.md`

### Reject — hard small-item anti-trigger

少数材料でも、意味境界や両義性を扱う必要があれば親和統合コアは意味を持つ。件数だけでは止めない。

### Reject as default — theme size / weight

多数性はsalienceの一情報だが、独立support・重要性・真実性と同じではない。派生二重計上とも衝突するため標準欄にしない。

## 2. `synthesis-frameworks`

Source:
https://github.com/slgoodrich/agents/tree/main/plugins/ai-pm-copilot/skills/synthesis-frameworks

### Adapt — actively inspect disconfirming material

**外部の良さ:** confirmation biasへの対抗として、反証的な材料を探す。

**境界:** `affinity-synthesis` は外部検索を所有しないため「新しい反証証拠を検索する」までは行わない。

**採用:** 入力済み材料の中で、現在の表札・構造に合わないcardを意図的に再確認する。追加検索はLayer 2へ渡す。

### Adopt — contradiction is signal, not cleanup target

現行の対立保持と一致する。独立Skillのruntime instructionでも明示する。

### Adopt — never fabricate quotations

生成AI固有の重要なquality gateとして採用済み。直接引用が必要なら元材料に存在する文だけを引用する。

### Adopt — progressive detailed references

Agent Skills仕様とも整合する。詳細なMethod、Template、Eval、Evidenceを必要時ロードへ分けた。

### Reject — universal atomic extraction

「一観察一sticky」を普遍規則にすると、意味の一体性を壊す。meaning-bearing unitを優先する。

### Reject — fixed theme count / coding count

数に合わせて構造を作る危険があるため標準化しない。

### Reject — recommendation as synthesis completion

材料統合とdomain recommendation / decisionを分ける。必要なら呼び出し側Skillへ渡す。

## 3. `Interview Synthesis`

Source:
https://github.com/SkillMedev/skills/blob/main/skills/interview-synthesis/SKILL.md

### Adapt — independent support awareness

**外部の良さ:** 一人の参加者から複数quotesがあっても、複数の独立data pointとして扱わない。

**一般化:** participant単位へ固定せず、source / event / derivation lineageを見て独立性を判断する。

**採用先:** `No false independent repetition` invariant。

### Reject as universal — minimum interview count / saturation rule

インタビュー調査固有のheuristicであり、汎用親和統合コアへは持ち込まない。

### Reject as universal — fixed insight formula

User type / behavior / because / but形式はUX researchには有用だが、創作、政策資料、技術調査等には過剰制約となる。

## 4. `think-concept-mapping`

Source:
https://github.com/product-on-purpose/thinking-framework-skills/tree/main/skills/think-concept-mapping

### Adapt — relation should be inspectable

**外部の良さ:** 線を引くだけでなく、関係が何かを明示することで曖昧な連結を減らす。

**ローカル適応:** A型的配置では、すべての関係を命題化することを必須にしない。ただし因果・対立・時間等を主張するなら、何を意味する線かを明示できるようにする。

### Adapt — questionable link / missing link inspection

空白探索と相性がよい。ただしmissing linkを「本来あるはずの事実」とみなさず、次に確かめる問いへ留める。

### Reject — concept nodes as mandatory input unit

材料を早期に概念語へ変換すると土の匂いを失うため標準にはしない。

## 5. `think-evidence-vs-inference-sort`

Source:
https://github.com/product-on-purpose/thinking-framework-skills/tree/main/skills/think-evidence-vs-inference-sort

### Adopt at boundary — explicit audit can be delegated

完成した主張の監査としては有用。必要なら親和統合後に別Skillとして呼べる。

### Reject inside grouping — evidence/inference/assumption as first geometry

カード内容より先にclaim taxonomyを置くと、KJ系の意味距離を変える可能性がある。

ローカル側ではepistemic seamを保持するが、それを初期clusterの先験分類軸にはしない。

## 6. Agent Skills specification

Source:
https://agentskills.io/specification

### Adopt — progressive disclosure

- metadataは軽くする。
- `SKILL.md` は起動後に必要なruntime instructionsへ集中する。
- Method / Evidence / Template / Evalを別referenceへ分ける。

### Adopt — name is descriptive and discoverable

公開名は系譜ブランドより、Agentが「何をするSkillか」を判断できる記述性を優先する。

現時点の作業名:

- `affinity-synthesis`
- `iterative-inquiry-synthesis`

## 7. 第1巡でprototypeへ追加すべき残差

比較の結果、prototypeに追加確認する項目:

1. 入力済み材料の中から、現在の表札・構造に反するcardを意図的に再確認する。
2. 頻度・cluster sizeは、独立support・重要性・truthと同一ではないと明示する。
3. 材料を弱める／ぼかす／行為者を落とす変換も、戻し検査の対象として明示する。
4. relation mappingでは、主張する関係の意味を後から検査できるようにする。

これらを小差分としてruntime prototypeへ反映した後、fixture dry-runへ進む。
