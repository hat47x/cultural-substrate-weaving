# 兄弟リポジトリとの意味の対応 — 帰属の規律、来歴ラベル、Living Labの記録

- Status: Maintainer cross-repository note / informative only / no runtime change
- Date: 2026-09-27
- Related: `kj-atlas-cognitive-coevolution.md`, `kj-atlas-merge-semantics-boundary.md`, `research/skill-prototypes/REFERENCE-CLASSIFICATION.md`（付録A）, `docs/ja/experiments/web-chat-living-lab.md`

## この文書の位置づけ

hat47xの兄弟リポジトリでは、CSWの帰属の規律と来歴ラベルを、自分たちの記録の読み方や比喩の扱いに取り入れる動きが出てきた。とくにSEI Cognition（`hat47x/sei-cognition`）は、製品群全体の「判断の意味論」を翻訳するための対応表を提案しており、その中にCSWの行も含めている。

本書は、この動きをCSWの側から追えるように残す保守者向けの記録である。ここに書く対応はすべて参考情報であり、次のことは変えない。

- CSWの方法論正本`src/<locale>/`と、来歴ラベルの意味。ラベルの定義は`src/ja-JP/core/principles-and-constraints.md`の「来歴ラベル」節にある。
- CSWと兄弟製品のあいだに依存関係がないこと。関係が深いことは、必須の依存を意味しない。
- 兄弟製品の意味については、それぞれのリポジトリが正本であること。

また、兄弟リポジトリの記録をCSWの有効性の証拠としては扱わない。兄弟リポジトリがCSWの語彙で比喩を分類したことも、CSWのSkillファイルを取得して検証したことも、CSWを対象へ適用した記録ではない。

## 名称の変更

- KJ Atlasは、`hat47x/sui-sensemaking`（SUI Sensemaking）へ改名された。SUI側のADR-0083（2026-09-11にAccepted）が記録している。改名の目的はKJ法の商標を製品名から外すことにあり、SUI側ではKJ法を出典として言及するだけにとどめている。
- SOZA（綜座）は、`hat47x/sei-cognition`（SEI Cognition）へ改名された。SEI側の記録によれば、改名は2026-09-11である。

本リポジトリの`kj-atlas-*.md`は、書いた時点の名称のまま残す。`kj-atlas-merge-semantics-boundary.md`にある「SOZA」は現在のSEI Cognitionを、「KJ Atlas」は現在のSUI Sensemakingを指す。凍結したcommit hashは、リポジトリ名が変わっても同じcommitを指す。

## 1. 兄弟リポジトリが帰属の規律を比喩の扱いに使っている

SEIのブランド文書（`hat47x/sei-cognition:product/vision/SEI_BRAND_WORLD_SOURCE.md`）は、易経の卦などの象徴を製品群に使いながら、§17に「比喩から型やfieldを直接作らない」という停止線を置いている。これは、文化体系から出た構造を対象側の証拠と分けるCSWの規律と同じ形をしている。

さらにSEIでは、SEIを製品群の「神経系の頂点」とみなす設計言語を評価し、比喩から出た問いには「比喩由来」の印を付けて、対象で確かめるまでは設計の根拠にしないという扱いが提案されている。CSWの言葉でいえば、この設計言語から出た問いは`framework_generated`であって、`target_supported`ではない。あわせて、ブランド文書の停止線を神経系の比喩にも広げ、そこでCSWの帰属の規律を参照すると明記する変更も提案されている。「神経系の頂点」という言い方は内部の設計言語にとどめる。ブランドの視覚表現には、もともと巨大なAI brainやcommand centerを中心に置かない方針がある（同ブランド文書 §7）。

この評価記録（`hat47x/sei-cognition:product/value/SEI_FAMILY_APEX_VALUE_REVIEW.md`）と停止線を広げる変更は、2026-09-27時点では、sei-cognitionの未mergeブランチ`docs/family-apex-backflow-20260927`にしかない提案である。

CSWの側で押さえておく境界は次のとおりである。

- 兄弟リポジトリがCSWの規律を読み方の約束として借りることと、CSWを実行することは別である。比喩をどう分類するかはそれぞれのリポジトリが判断し、その正本もそれぞれが持つ。
- この借用を、CSWの有効性や採用の証拠として数えない。Living Labの観測にも加えない。
- CSWの側から兄弟リポジトリへ、ラベルの付け方を求めない。
- SUI Sensemakingにも、製品群の位置づけを整理した文書へCSWの行を加え、CSWが何を所有し、何を所有しないかを示す提案がある（SUIの未mergeブランチ`docs/family-apex-backflow-20260927`）。CSWの所有範囲は本リポジトリの`AGENTS.md`が正本であり、食い違う場合は`AGENTS.md`に従う。

## 2. 来歴ラベルとSEIの意味の対応

SEIの対応表では、CSWの来歴ラベルと著者の採否を、SEIの一般的な意味へ次のように翻訳する案が示されている。SEIは各製品の意味を一つに統合するのではなく、翻訳する立場をとる。

| CSWでの記述 | SEIでの読み | 保つべき境界 |
|---|---|---|
| `target_supported` | 対象側の証拠に支えられたObservation | 対象側の資料・観察・反証への参照を残す。SEI側でAssuranceへ自動的に格上げしない |
| `framework_generated` | 出所（どの文化体系を、どの深さまで読み込んで生じたか）を付けたHypothesis / Interpretation | 体系語を外しても成り立つことを、対象側の証拠とみなさない |
| `cross_field_emergent` | 接触から創発したHypothesis | 対象側と体系側の両方への来歴を残す。`target_supported`へ読み替えない |
| `unresolved` | Unknown | 判断がまだ置かれていないことを、否定の事実に変えない（Unknown ≠ No） |
| 著者の採否 | 著者のDecision | 採否を決めるのは、著者か、スキルの外で判断を委ねられた主体である |

この対応を読むときは、次を守る。

- **ラベルは、採用も公開も許可しない。** これはCSWの正本がすでに定めていることで、SEIの対応表でも変えてはならない点として挙げられている。あるラベルから別のラベルへ移っても、採用、発話、外部化、公開の許可にはならない。
- 読み替えは一方向である。SEIのHypothesisがすべてCSWから来るわけではないので、SEIの型からCSWのラベルを逆に導かない。
- 文化体系から生じた材料は、SEIの側でも重みや権威の上乗せを受けない。うまく束にまとまったというだけで`target_supported`にはしないという`AGENTS.md`の境界は、翻訳した後も保つ。
- 対象と体系の緊張が解けないまま残ったとき、それを無理に`cross_field_emergent`へ回収しないのがCSWの規律である。そうした緊張をSEIの側でConflictとして保つ読み方があり得るかどうかは、未決の問いとして残す。
- CSWには、SEIの記録を出力する仕組みはなく、その予定もない。`src/`は変えない。

SEIの対応表（`hat47x/sei-cognition:product/definition/SEI_FAMILY_SEMANTIC_MAP.md`）も、2026-09-27時点では、sei-cognitionの未mergeブランチ`docs/family-apex-backflow-20260927`にしかない。一方、Observation、Hypothesis、Unknown、Decisionといった型は、SEIの現行の`sei.semantic-interchange`契約（`hat47x/sei-cognition:contracts/interchange/SEI_SEMANTIC_INTERCHANGE_v1alpha1.md`）に例として挙がっている。

## 3. Method DefinitionとRealizationの対応

CSWの研究suiteは、Method Definition、Agent Skillとしての実現、適用記録、評価fixtureを分けている。これとSEIの`sei.cognitive-method`が分けるDefinition・Realization・Applicationとの対応は、[`REFERENCE-CLASSIFICATION.md`の付録A](../../../research/skill-prototypes/REFERENCE-CLASSIFICATION.md)にまとめた。

SEIはすでに、CSWの日本語版`weave` Skillのファイルを取得して検証し、Method Realizationとして固定している。ただし、LLM上ではまだ実行していない。

## 4. 未決の問い：Living Labの記録を`sei.semantic-interchange`へ任意に書き出せるか

Living Labのschema 0.2（`evals/living-lab-round.schema.json`と`evals/living-lab-event.schema.json`）は、来歴の異なる記述を別々の経路に置いている。

- 直接の観察：eventの`observation`と`evidence_refs`、paired checkの`comparison.observed_differences`
- 測定：`comparison.measurements`（`label`、`value`、`source_ref`）
- 利用者の判断：`source_type: user`を持つ`sourced_statement`
- AIや外部の解釈：`source_type: ai`または`external`を持つ`sourced_statement`

この分け方は、観察、推奨、判断、根拠を分けるSEIの考え方に近い。そこで、これらの記録を、必要なときだけ一方向に書き出して`sei.semantic-interchange`へ渡せるか、という問いが立つ。現時点では、次のような読み方を候補として置くにとどめる。

| Living Labの記録 | SEIでの読み方の候補 | 注意 |
|---|---|---|
| 直接の観察 | Observation | 誰が観察したのかをSEIの側でどう区別するかは、まだ決まっていない |
| 測定 | 測定値と出典を持つObservation | Living Labの件数や分布はKPIではない。集計を、方法が有効だという観測に変えない |
| 利用者の判断 | 利用者に帰属する記述。採否の決定である場合に限りDecision | 「役に立った」という判断と、採用するという決定を同じものにしない |
| AIの解釈 | 出所を付けたHypothesis / Interpretation | AI評価者の結論は、測定でも利用者の判断でもない。Assuranceにしない |
| `residuals` | Unknown、またはQuestion | 残差を、片づいたものとして扱わない |
| `reopening_conditions` | 判断に結び付いている場合の見直し条件 | 判断のない記録に、判断を補わない |

次の点は、変えずに保つか、未決のまま残す。

- **schemaは今は変えない。** `evals/`のschemaに、SEI向けのfieldを足さない。
- 非公開の記録は`.living-lab/`かリポジトリの外に置き、公開してよい記録だけを`research/living-lab/observations/`に置いている。書き出しによって、この境界を越えない。SEIの契約も、Envelopeに入れられることと共有してよいことを区別している。
- `activation_scope: non_activation`は、その回に文化体系を開かなかったという記録である。書き出した先で、有用か無用かの判断に変えない。
- 書き出しを誰が受け持つか（CSWの研究用ツールか、SEI側のadapterか、呼び出し側か）は決めていない。いずれにしても、CSWのruntimeには置かない。

少なくとも次のいずれかが起きたときに、この問いを開き直す。

1. SEIの側で、観察の出所の区別（人による観察、AIの生成、AIの要約など）や、`sei.semantic-interchange`の安定化が進んだとき。観察の出所を区別する案は、2026-09-27時点ではSEIの未mergeブランチ上の提案である。
2. CSWとSUI Sensemakingの比較（`kj-atlas-cognitive-coevolution.md`）や、一つの実際の判断を製品群の複数の製品で扱うdogfoodの中で、Living Labの記録をSEIで読み直す具体的な必要が生じたとき。
3. 公開してよい記録だけを使い、来歴の分離を失わずに書き出せることを示せる見込みが立ったとき。

## 本書で行わないこと

- `src/<locale>/`の変更と、来歴ラベルの意味の変更
- `evals/`のschemaの変更
- 兄弟製品への依存の宣言と、SEIの記録を出力する機能の追加
- 兄弟リポジトリの記録や提案を、CSWの有効性の証拠として扱うこと
- 兄弟リポジトリの未mergeの提案を、採用済みのものとして扱うこと
