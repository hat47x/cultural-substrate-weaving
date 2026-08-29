# v39 DeepSeek API検証の記録と現行方法論への帰属

- Status: Historical validation / partially diagnostic
- Date: 2026-08-29
- Scope: fresh-context API evaluation
- Runtime under test: v39 cognitive-effect harness
- Generator: DeepSeek v4-pro
- Judge: DeepSeek v4-flash

## この記録の目的

この文書は、v39のAPI検証を現在の方法論の「有効性証明」または「無効性証明」として扱うためのものではない。

目的は、何を実際に測ったか、何が失敗したか、どの所見を現行スキルへ帰属できるか、どの所見は実験装置・単発run・モデル条件へ残すべきかを記録し、同じ誤読や同じ実験コストを繰り返さないことである。

## v39で比較したもの

主比較は次の二条件だった。

- **B1 representation-only**: 文化体系の資料を読めるが、体系固有の操作は実行しない。
- **T1 native-enactment**: 同じ資料を読み、さらに体系固有の操作を実行する。

したがって主比較 `T1 - B1` は、文化体系を保持すること一般ではなく、**一回のfresh contextの中でnative enactmentを追加する局所効果**を測った。

v39ではT1をcontract-validにするため、少なくとも一つの`native_operation`を実行することが事実上必須だった。これは現在の通常利用とは異なる重要な条件である。

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

`target_fidelity`は事前登録のnoninferiority guardrail自体は通過したが、平均差は負だった。

stratum別のcore差もすべて負だった。

- null/simple: **-0.438786**
- stress: **-0.294496**
- writing: **-0.135159**
- general: **-0.254630**

したがって「null caseへ無理に文化体系を開いたことだけ」が負結果の全てを説明するわけではない。

## Stage Pの補助所見

小規模pilotのStage Pでも、主比較は負だった。

- `T1 - B1`: **-0.289969**

さらに補助比較では、

- `B1 - B0`: **-0.209722**
- `T1 - B0`: **-0.499691**

だった。

ただしStage Pは5ケースの診断的pilotであり、これらをconfirmatoryな効果量として扱わない。

`B1 - B0`が負だったことは、native enactment以前に、厚いframework representationをworking contextへ入れるだけでもanchoringが生じる可能性を示す仮説として保持する。Stage Cの公開解析では同比較を確定していない。

## routing auditを加えた後の診断

Stage Cでは、非nullケースについて原則として、構造適合度の高いfield二つとseeded field-opening一つを選んでいた。null/simpleケースでは適合scoreがすべて0であり、三候補すべてがseeded openingだった。

72 field-cellをrouting理由と結び付けると、全体ではseeded openingの悪化が大きかったが、null/simpleを除くと、

- structural fit: 約 **-0.234**
- seeded field-opening: 約 **-0.217**

となり、ほぼ同程度に負だった。

したがって、

> seeded openingだけを削れば、現行の強制native enactmentが有効になる

とは結論できない。

一方、高いstructural fitの一部のwriting caseでは正方向のcellもあった。これは「fit scoreだけでなく、体系由来の構造を対象事実として主張するのか、構成上の道具として使うのか」というusage modeの違いが重要である可能性を示す。

このfield別・case別所見はpost-hocであり、確認的結果として扱わない。

## 実験装置側の問題

### 1. 強制enactment

T1では、適合が弱い場合や「使わないこと」が忠実な場合にも`native_operation`が必要だった。

この条件は、現在の`非発動 / 限定適用 / 全体適用`という方法論より強い。したがってv39の負結果を、そのまま「文化体系を使うこと一般の害」と読むことはできない。

### 2. blind leakageの可能性

匿名化処理は構造化された`framework_origin`や`native_operation`を除去していたが、自由記述の`productive_delta`には、`Eight-trigram sweep`等のfield固有語が残る例があった。

outcome judgeは`productive_delta`も読んでおり、rubricはframework-as-evidence、forced mapping、unnecessary complexityを罰する。

したがって、実際のforcingと、T1であることを推測しやすい報告形式へのペナルティが一部混ざった可能性がある。

これはStage Cの負結果を無効にするものではないが、効果量を純粋なnative cognitionの因果効果と解釈することを弱める。

### 3. schema負荷

Stage Cでは11件のcontract-invalid returnがあり、診断時の内訳はB0 8、B1 1、T1 2だった。

B0の多くは、本来禁止される`native_operation`を出力したことによる。全条件へ共通の大きなschemaを見せること自体が、B0へfield-operation vocabularyを誘発した可能性がある。

通常利用の方法論へ、このtelemetry負荷を持ち込まない。

## 現行スキルへ帰属した変更

v39の結果を直接規則化せず、現行の二つの中核能力に必要な範囲だけを帰属した。

### 1. 遅延したKJ周回

PR #6で、次の周回は直後でなくてよいこと、結論だけでなく未解決の問い・孤立した意味単位・保留した関係を持ち越し、新資料が届いた時に前回の束を正解として固定せず再開することを明示した。

これはv39の単発runでは測りにくかった、本来のラウンド式KJの時間軸を方法論へ明示する変更である。

### 2. framework application depthの限定

PR #7で、frameworkの採用と適用深度を分離した。

frameworkを採用しても、全要素・全解釈語・全遷移を使い切る義務はない。対象側の問いに必要な層と範囲だけを適用し、増分がなければ、空いた位置や未使用操作を埋めるためだけに範囲を広げない。

これはv39のforcing所見を、現行の非発動・限定適用・全体適用という既存設計に沿って最小限帰属した変更である。

### 3. 長期dogfood評価

KJ Atlas dogfoodの評価プロトコルでは、通常AI / +skill × 通常チャット / KJ Atlasの比較と、探索・意味保持・根拠・反証・再訪・停止等の制御を分けて観測する。

実験結果はskill、caller/domain context、KJ Atlas、model/experimentへ帰属し、帰属不能なら方法論正本を変更しない。

## 現時点でスキルへ追加しないもの

v39だけを根拠に、次を静的規則へ追加しない。

- 特定のfieldを禁止または優遇する固定ranking。
- fit scoreの固定threshold。
- DeepSeek固有のJSON/schema対策。
- blind judge用telemetry。
- writing / software / research等のdomain固有品質基準。
- 全ての通常利用での複雑なprovenance分類schema。
- B1 representationの有害性を確定事実とする規則。

これらは、追加の実課題または比較結果が得られるまで研究・実験側へ保持する。

## 今後の優先順位

当面は、APIで大量の局所比較を繰り返すことより、実課題の長期ラウンドで次を観察する。

1. 以前に生じた問いが、後の資料探索を実際に変えたか。
2. 未解決・孤立した材料が、後からKJ構造を組み替えたか。
3. frameworkを使わない、限定して使う判断が過剰適用を避けたか。
4. framework由来の構造が、対象へ戻した後に実成果へ採用されたか。
5. 異なる実課題で同じ方法上の増分または失敗が再現したか。

これらが安定して観察された後に、必要な部分だけfresh-context比較へ切り出す。

## 現時点の判定

v39は、`cultural-substrate-weaving`全体の有効性試験ではない。

より狭く、

> **厚いframework representationに加えて、少なくとも一つのnative operationを一回のfresh-context run内で強制したときの局所試験**

として保存する。

その条件では、B1よりT1が悪く、特にforcingとprovenanceに問題が出た。この負結果は保持する。

同時に、本スキルの中心であるラウンド式KJ、遅延した資料到着、未解決の再活性化、実成果への長期採用については、この実験だけでは十分に測れていない。