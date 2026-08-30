# v39 DeepSeek API検証の記録と現行方法論への帰属

- Status: Historical validation / partially diagnostic
- Date: 2026-08-29
- Scope: fresh-context API evaluation
- Runtime under test: v39 cognitive-effect harness
- Generator: DeepSeek v4-pro
- Judge: DeepSeek v4-flash

## この記録の目的

この文書は、v39のAPI検証を、現在の方法論の「有効性を証明した結果」または「無効性を証明した結果」として扱うためのものではない。

何を実際に測ったのか、どこで失敗したのか、どの所見を現行スキルへ帰属できるのか、どの所見は実験装置、単発run、モデル条件の側に残すべきなのかを記録し、同じ誤読や同じ実験コストを繰り返さないことを目的とする。

## v39で比較した条件

主比較は次の二条件だった。

- **B1 representation-only**: 文化体系の資料を読めるが、体系固有の操作は行わない。
- **T1 native-enactment**: 同じ資料を読み、さらに体系固有の操作を行う。

したがって主比較`T1 - B1`が測っていたのは、文化体系を利用すること一般ではない。**一回のfresh contextの中で、native enactmentを追加したときの局所的な差**である。

v39ではT1をcontract-validにするため、少なくとも一つの`native_operation`を実行することが事実上必須だった。この点は、現在の通常利用とは異なる重要な条件である。

## Stage Cの事前登録判定

24 held-out cases、3条件、3反復を基礎とするStage Cでは、主比較は支持されなかった。

- `T1 - B1` blind target-outcome core mean: **-0.2807677469**
- case bootstrap 95% CI: **[-0.4039351852, -0.1572788066]**
- exact case-level sign p: **0.0015438795**
- preregistered support decision: **NOT SUPPORTED**

guardrail / dimensionのうち、特に悪化が大きかったのは次である。

- `non_forcing`: **-0.5675154**
- `provenance_cleanliness`: **-0.5046296**
- `target_fidelity`: **-0.1967593**

`target_fidelity`は、事前登録したnoninferiority guardrailそのものは通過したが、平均差は負だった。

stratum別のcore差もすべて負だった。

- null/simple: **-0.438786**
- stress: **-0.294496**
- writing: **-0.135159**
- general: **-0.254630**

そのため、「null caseで無理に文化体系を開いたことだけ」が負の結果をすべて説明するわけではない。

## Stage Pで得られた補助所見

小規模pilotのStage Pでも、主比較は負だった。

- `T1 - B1`: **-0.289969**

さらに補助比較では、

- `B1 - B0`: **-0.209722**
- `T1 - B0`: **-0.499691**

という結果だった。

ただしStage Pは5ケースだけの診断的pilotであり、これらをconfirmatoryな効果量として扱わない。

`B1 - B0`が負だったことからは、native enactmentを行う前でも、厚いframework representationを作業コンテキストへ入れるだけでanchoringが生じる可能性を仮説として考えられる。Stage Cの公開解析では、同じ比較を確定していない。

## routing auditを加えた後の診断

Stage Cでは、非nullケースについて原則として、構造適合度の高いfield二つとseeded field-opening一つを選んでいた。null/simpleケースでは適合scoreがすべて0であり、三候補すべてがseeded openingだった。

72 field-cellをrouting理由と対応させると、全体ではseeded openingの悪化が大きかった。一方、null/simpleを除くと、

- structural fit: 約 **-0.234**
- seeded field-opening: 約 **-0.217**

となり、ほぼ同程度に負だった。

したがって、

> seeded openingだけを削れば、現行の強制native enactmentが有効になる

とは結論できない。

一方で、structural fitが高い一部のwriting caseには、正方向のcellもあった。このことからは、fit scoreだけでなく、体系由来の構造を対象事実として主張するのか、それとも構成上の道具として使うのかというusage modeの違いが重要である可能性も考えられる。

ただし、このfield別・case別の所見はpost-hocであり、確認的な結果として扱わない。

## 実験装置側で見つかった問題

### 1. 強制enactment

T1では、適合が弱い場合や、「使わないこと」の方が対象に忠実な場合であっても、`native_operation`を行う必要があった。

この条件は、現在の`非発動 / 限定適用 / 全体適用`という方法論よりも強い。そのため、v39の負の結果を、そのまま「文化体系を使うこと一般の害」と読むことはできない。

### 2. blind leakageの可能性

匿名化処理では、構造化された`framework_origin`や`native_operation`を除去していた。しかし、自由記述の`productive_delta`には、`Eight-trigram sweep`のようなfield固有語が残る例があった。

outcome judgeは`productive_delta`も読んでおり、rubricではframework-as-evidence、forced mapping、unnecessary complexityを罰する。

そのため、実際に起きていたforcingへの評価と、「この出力はT1らしい」と推測しやすい報告形式へのペナルティが、一部混ざっていた可能性がある。

これはStage Cの負の結果そのものを無効にするものではない。ただし、その効果量を純粋なnative cognitionの因果効果と解釈することは難しくなる。

### 3. schema負荷

Stage Cでは11件のcontract-invalid returnがあり、診断時の内訳はB0 8、B1 1、T1 2だった。

B0の多くは、本来禁止されている`native_operation`を出力したことによる。全条件へ共通の大きなschemaを見せること自体が、B0にもfield-operation vocabularyを誘発した可能性がある。

通常利用の方法論へ、このtelemetry上の負荷を持ち込まない。

## 現行スキルへ帰属した変更

v39の結果をそのまま規則化するのではなく、現行スキルの二つの中核能力に必要な範囲だけを帰属した。

### 1. 遅延したKJ周回

PR #6では、次の周回を直後に行う必要はないことを明示した。結論だけでなく、未解決の問い、孤立した意味単位、保留した関係も持ち越し、新しい資料が届いたときには、前回の束を正解として固定せずに再開する。

これは、v39の単発runでは測りにくかった、本来のラウンド式KJの時間軸を方法論へ明示した変更である。

### 2. framework application depthの限定

PR #7では、frameworkを採用するかどうかと、どこまで深く適用するかを分けた。

frameworkを採用しても、全要素、全解釈語、全遷移を使い切る義務はない。対象側の問いに必要な層と範囲だけを適用し、増分がなければ、空いた位置や未使用操作を埋めるためだけに範囲を広げない。

これは、v39で見られたforcingの問題を、現行の非発動、限定適用、全体適用という既存設計に沿って、必要最小限だけ方法論へ帰属した変更である。

### 3. 長期dogfood評価

KJ Atlas dogfoodの評価プロトコルでは、通常AI / +skill × 通常チャット / KJ Atlasの比較と、探索、意味保持、根拠、反証、再訪、停止などの制御を分けて観測する。

実験結果はskill、caller / domain context、KJ Atlas、model / experimentへ帰属する。帰属できない場合は、方法論の正本を変更しない。

## 現時点ではスキルへ追加しないもの

v39だけを根拠に、次を静的規則へ追加しない。

- 特定fieldを禁止または優遇する固定ranking。
- fit scoreの固定threshold。
- DeepSeek固有のJSON / schema対策。
- blind judge用telemetry。
- writing / software / researchなど、domain固有の品質基準。
- すべての通常利用へ適用する複雑なprovenance分類schema。
- B1 representationの有害性を確定事実とする規則。

これらは、追加の実課題や比較結果が得られるまで、研究・実験側へ保持する。

## 今後の優先順位

当面は、APIで大量の局所比較を繰り返すよりも、実課題の長期ラウンドで次を観察する。

1. 以前に生じた問いが、後の資料探索を実際に変えたか。
2. 未解決または孤立していた材料が、後からKJ構造を組み替えたか。
3. 文化体系を使わない、または限定して使う判断が、過剰適用を避けたか。
4. 文化体系から得た構造が、対象へ戻した後にも残り、実成果へ採用されたか。
5. 異なる実課題で、同じ方法上の増分や失敗が繰り返し現れたか。

これらが安定して観察された後に、必要な部分だけをfresh-context比較へ切り出す。

## 現時点の判定

v39は、`cultural-substrate-weaving`全体の有効性試験ではない。

より狭く、

> **厚いframework representationに加えて、少なくとも一つのnative operationを、一回のfresh-context runの中で強制した場合の局所試験**

として保存する。

その条件ではB1よりT1が悪く、特にforcingとprovenanceに問題が見られた。この負の結果はそのまま保持する。

同時に、本スキルの中心であるラウンド式KJ、遅れて届く資料、未解決事項の再活性化、実成果への長期的な採用については、この実験だけでは十分に測れていない。
