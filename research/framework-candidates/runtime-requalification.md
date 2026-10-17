# Runtime framework requalification audit

Status: research governance / non-ranking / non-demotion

## Purpose

CSWのFramework Registryでは、新しい`profile-ready`候補に対して、

- source basis;
- structural core;
- positive target-return fixture;
- negative / non-activation fixture;
- de-binding;
- ordinary / no-framework baseline;
- near-neighbor differentiation;

を段階的に厳しく確認するようになった。

一方、runtimeに既に採用されているframeworkには歴史的経緯があり、現在の`adopted`契約は主にruntime materializationとselection cueの存在を確認する。したがって、新規候補だけが現在の厳しい基準を受け、既存採用がそのまま既得権化する非対称が起こりうる。

この監査は、その非対称を可視化するための**来歴監査**である。

frameworkの有効性、優劣、適合度、真偽を判定しない。証拠欄が空いていることを、frameworkが弱い・誤っている・削除すべきだという結論へ変換しない。

## Audit surface

`framework_corpus_contract.py --audit-adopted` は、各`adopted` candidateについて次を確認する。

1. **profile**
   - 現行の構造核、系譜境界、native operation、de-bindingを再読できる研究profileがRegistryから参照されているか。
2. **positive target-return fixture**
   - framework contactから対象へ戻ったとき、何が残るかを具体例で追えるか。
3. **non-activation fixture**
   - frameworkを使わない方がよい条件、途中で止める条件が具体例で追えるか。
4. **ordinary / no-framework baseline comparison**
   - 通常の分析・設計・レビューで同じ問いが出ないかを比較した記録があるか。
5. **discovery-value comparison**
   - framework出力を見た後のspecialist-method一致だけでなく、framework contact前の通常入口から同じ認知operationへ到達できたかを比較した記録があるか。
6. **near-neighbor comparison**
   - 似た認知operationを持つ既存frameworkとの差を同じtargetまたは比較可能な条件で説明できるか。

監査結果には`evidence_gaps`を出すが、score、rank、recommendation、automatic demotionは出さない。

## 能力重複と発見価値を分ける

ordinary baseline比較には、少なくとも二つの異なる問いがある。

1. **capability overlap**
   - framework contactから得た問い・区別を、通常の専門手法でも再現できるか。
2. **discovery value**
   - その専門手法をまだ選んでいない状態から、frameworkなしで同じ認知operationへ到達できるか。

前者だけで「frameworkは不要」と結論しない。

frameworkの出力を見た後で、それに最も似た専門手法を探せば、かなりの確率で同じ操作を再現できる。これは能力の重複を示すが、CSWの本質価値である「現在の理解では出にくい問い・区別・関係・構成との出会い」を否定しない。

したがって再資格では、比較対象を次のように分ける。

- **generic / ex-ante baseline**: framework contact前のtarget記述と通常の汎用分析だけで何が出るか。
- **matched specialist baseline**: framework contact後のoperationを再現できる既知の専門手法があるか。
- **discovery-value comparison**: generic baselineからそのspecialist baselineを自然に選べたか、またはframework contactが初めてその認知仕事を露出したか。
- **near-neighbor comparison**: 他のframework固有operationと混同していないか。

matched specialist baselineは、原則としてtarget構造や事前に利用可能だった標準手法から選ぶ。framework出力を見た後で初めて選んだ手法は、その選定経路を明示し、能力重複の証拠として扱っても、発見価値が無いことの証拠にはしない。

runtime retentionは「世界に同等の手法が存在しないこと」を要求しない。通常の入口からは出にくい認知operationを、文化体系との接触が低い選定負荷で開き、target-return後にも有用な差が残るなら、そのdiscovery contributionを採用根拠として記録できる。

## Structured requalification metadata

再資格根拠を明示する候補は、既存の

- `profile_path`;
- `worked_example_paths`;
- `negative_example_paths`;

に加えて、任意の`runtime_requalification`を持てる。

```json
{
  "runtime_requalification": {
    "ordinary_baseline_comparison_paths": [
      "research/framework-candidates/comparisons/example-vs-ordinary-baseline.md"
    ],
    "discovery_value_comparison_paths": [
      "research/framework-candidates/comparisons/example-discovery-value.md"
    ],
    "near_neighbor_comparison_paths": [
      "research/framework-candidates/comparisons/example-vs-neighbor.md"
    ]
  }
}
```

このmetadataは「採用済みであることの証明」ではない。後から同じ判断を再読できるようにするための参照である。

## Current Registry snapshot

2026-10-06の最初の監査時点では、Registry上の`adopted` candidateは19件だった。その後、Mīmāṃsāを現行基準で再資格し、ordinary policy / requirements reviewがtested de-bound operationsを再現したため、general runtimeから外して`profile-ready`へ戻した。

現在の`adopted` candidateは13件である。

儒家の役割・礼（Confucian role/li）もdiscovery-aware基準で再資格した。通常のRACI・承認記録によって「ownerという肩書き」と実際の承認権限の不一致はframework接触前から検出できるため、これは保持理由としない。またFeldman/Pentlandのorganizational routines（ostensive/performative）を意図的に選べば、定型的な会議の型と実際のやり取りを比較できるため、unique analytic capabilityとも主張しない。

一方、仮想の定例リリース会議で、正式な相談・承認権限は整っているのに、lead engineerの推薦後に行う「異議はありますか」が、発言順序と反復された関係の中で実質的に締めの合図になっていないかという問いは、通常の事故・責任分担reviewで必ずしも開かれない。role/li contactは同じ文言の意味が**行為される型と関係位置**によって変わる可能性を仮説として露出する。この問いを録音・関係者の解釈・前後比較・代替仮説へ戻せる場合に限りruntime保持を支持する。因果や沈黙の動機は未検証であり、歴史的な身分序列を規範として持ち込まない。human-factors / routine reviewがex-anteに同じ問いをすでに開いていればnon-activationとする。

証拠は `research/framework-candidates/comparisons/confucian-role-li-vs-ordinary-raci-routines.md`、`research/framework-candidates/comparisons/confucian-role-li-discovery-value.md`、`research/framework-candidates/comparisons/huayan-vs-confucian-role-ritual.md`、正負fixtureへ分離した。比較は定性的な机上レビューであり、blind efficacyや実組織の因果効果を主張しない。

Mīmāṃsāに続き、dependent origination（縁起）についても再資格した。旧比較ではsame-targetへFive Whys、fault-tree expansion、dependency analysis、counterfactual / intervention questionを適用し、condition-chain、upstream-condition、cessation-counterfactual、dependency-reframing、intervention-pointを再現できたためgeneral default runtimeから外した。

改訂後のdiscovery-aware基準で遡及reviewすると、ordinary post-incident practice自体がframework contact前から「どのcomponents / conditions / actions / eventsが寄与したか」「どのmitigation / corrective actionで再発を防ぐか」「変更後に何が変わるべきか」を自然に問う。tested rolling-deployment incidentでも、stale capability、heartbeat、credential state、dispatch window、queue redeliveryなどの条件群と介入後のfailure cessationへframeworkなしで到達できる。

したがってdependent originationではcapability overlapだけでなく**discovery overlap**も成立する。旧demotionをdiscovery-aware基準でも確認済みとし、`profile-ready / no-runtime`を維持する。source basis、研究profile、正例・non-activation例、ordinary capability比較、discovery-value比較、Paṭṭhāna近接比較、selection cueは保持する。

続いてclassical stasis theoryを、既存のrelease-incident target上でordinary incident / issue triageと比較した。事実、定義、評価、手続き・権限の分離、争点移動、issueごとの証拠適合は、target-languageのissue tableとreply-to-issue対応で再現できたため、旧基準ではgeneral default runtimeから外して`profile-ready`へ戻した。

しかし改訂後のdiscovery-aware基準で遡及reviewすると、このissue tableは「争点の種類を分ける」という認知jobを既に知った後のmatched specialist baselineだった。framework名もissue taxonomyも与えないgeneric incident / postmortem baselineはtimeline、impact、root cause、mitigation、roles、actionsを自然に扱う一方、fact / definition / evaluation / authorityという異なるanswer typeが同じ会話内で走っていることや、replyがissue typeを切り替えたことを必ずしも前景化しない。

stasis contactは「何を争っているのか」を先に問い、eventを認めても残るdefinition/evaluation、definitionを揃えても残るquality/procedure、そしてissue-specific evidenceとstasis-switchを露出する。この差はde-binding後にもtarget-side questionとして残る。したがってretrospective discovery-value reviewはruntime restorationを支持し、mechanical restorationも完了した。classical stasis theoryは再びdefault runtimeのadopted candidateとして利用できる。

Aristotle's four causesについても旧基準では、multi-tenant rate-limiterをsame-targetとしてNASA型systems engineeringのstakeholder expectations、constraints、logical decomposition、design solution / behaviorと比較し、why-splitting、explanation-gap、causal-category-audit、multi-cause-composition、artifact-design-probeを再現できたためgeneral default runtimeから外した。

改訂後のdiscovery-aware基準で遡及reviewすると、engineered-system design自体がframework contact前からstakeholder outcomes、technical requirements / constraints、logical architecture、design solution、behavior / failure mechanismを分けて扱う。tested rate-limiterでも、backend protection、premium burst entitlement、resource constraints、token-bucket structure、refill/configuration mechanismへ四原因なしで自然に到達できる。

したがってAristotle's four causesでもcapability overlapだけでなく**discovery overlap**が成立する。歴史的なaitiaと現代systems engineeringの概念的同一性は主張せず、tested SIer designでtarget-side cognitive jobが重なるというproduct boundaryとしてdemotionを新基準でも確定する。

Wuxing（五行）についても、distributed-worker autoscalerのoscillationをsame-targetとして、ordinary signed causal-loop / system-dynamics analysisと比較した。生成／制約という二種類の関係、feedback loop、edgeごとのrole変化、missing link、operating stateによるrelation changeは、target-languageのdirected typed graphで再現でき、追加のtarget-side questionは残らなかった。歴史的な`sheng` / `ke`とmodern causal polarityの同一性は主張せず、tested SIer useでde-bind後の問いが重複するという限定的なruntime product boundaryとして扱う。

Wuxingについては、その後同じautoscaler targetへdiscovery-value comparisonを追加した。framework名もspecialist method名も与えないgeneric incident baselineから、oscillationという症状を手掛かりにcontroller input/output、repeated reaction、delay、retry、damping、stabilization、over-correctionへ自然に進める。Kubernetes HPAの通常資料もautoscalingをcontrol loopとして扱い、replicaのflapping / thrashingとstabilizationを標準的な運用問題として明示している。

したがってWuxingでは、matched specialist methodによる**capability overlap**だけでなく、targetと通常運用知識から同じfeedback/control jobをframework contact前に選べるという**discovery overlap**も確認できた。Huayanとは逆に、de-binding後にruntime固有のdiscovery contributionが残らない。general SIer runtime removalを改訂後のdiscovery-aware基準でも支持し、default runtimeから外して`profile-ready`へ戻した。source basis、研究profile、正例・non-activation例、ordinary capability比較、discovery-value比較、near-neighbor比較、selection cueは保持する。

Mīmāṃsāについても最後に遡及discovery-value reviewを行った。tested deployment policy / runbookは自然言語のnormative textであり、ordinary requirements practice自体がframework contact前からrequirement segmentation、one-subject/one-predicate、modifier / exception scope、explicit assumptions、ambiguity、consistency、conflict reviewを自然に要求する。二つのfixtureでMīmāṃsāからde-bindしたprescriptive-unit、syntactic attachment、semantic fit、explicit-vs-supplied、norm-conflict decompositionへframeworkなしで到達できた。

したがってMīmāṃsāでもcapability overlapだけでなく**discovery overlap**が成立し、旧demotionをdiscovery-aware基準でも確定した。

これにより、capability-overlap / discovery-value分離を導入する前に降格した4件の遡及reviewは完了した。結果は一律ではない。

- classical stasis theory: discovery contributionが残りruntimeへ復帰;
- dependent origination: discovery overlapを確認しdemotion確定;
- Aristotle's four causes: discovery overlapを確認しdemotion確定;
- Mīmāṃsā: discovery overlapを確認しdemotion確定。

旧基準降格について、未確認のretrospective discovery-value debtは現在0件である。

Hadith isnād / matnについても、現在のCSW product structureを基準に再資格した。policy claimがmeeting note、chat、summaryへ転載・変形されるsame-targetでは、W3C PROV型のderivation / quotation / revision graphでbranch / convergenceとvariantを表現でき、C2PA型のprovenance boundaryも「来歴が検証可能であること」と「内容が真であること」を分離する。

さらに重要なのは、CSW core自身がframework selection前から、同一資料の転載・派生を独立支持として数えないこと、発見経路と証拠源の独立性を分けること、framework-generated materialを独立したtarget-side supportなしにtarget_supportedへ上げないことを要求している点である。

このためhadithの高いproduct relevanceは否定しないが、その最重要operationはすでにalways-on coreへ吸収済みであり、default runtime frameworkとしては**capability overlapとdiscovery overlapの両方**が成立する。一般runtimeからのdemotionを支持し、mechanical demotionも完了した。歴史的・宗教的・比較source-criticism用のresearch candidateとして保持する。

Nyāya five-member inferenceについてもdiscovery-aware基準で再資格した。matched specialist baselineとしてToulmin型のclaim / grounds / warrant / backing / qualifier / rebuttalを用いると、argument-unfolding、reason-rule-separation、example/counterexample、application audit、inference-gap detectionの多くを再現できる。したがってunique formal capabilityだけではruntime保持を説明できない。

一方、framework名もargument-mapping手法も与えないgeneric incident / RCA baselineは、root cause、evidence、contributing factors、reproduction、elimination、corrective actionを自然に扱うものの、「観察された理由」「その理由から結論へ進む一般化」「その一般化が今回の対象に適用できるか」を独立した三つの検査点として必ずしも外在化しない。別事例で成立したR + C → failureという関係を、C未確認の現在targetへそのまま移すような推論飛躍が残り得る。

Nyāya contactはこのreason → generalized relation → target applicationの橋を低い選定負荷で露出し、de-binding後にも具体的な検査質問として残す。したがってruntime保持を支持する。ただしdirect interventionで因果がすでに十分確かめられている場合や、target自身がwarrant/application/counterexampleを明示している場合はnon-activationとする。

Catuṣkoṭi（四句分別）についても同じ基準で再資格した。yes/noのmigration statusをsame-targetとして見ると、binary defectを認識した後であればordinary requirements / state reviewがscope分割、multi-state、not-applicable、aggregation ruleでde-bound outputを再現できる。このためunique representationを保持理由にはしない。

一方、generic ex-ante reviewは曖昧さを解消し、正しいscope・predicate・state modelへ整える方向へ進みやすく、修正前のbinary frameに対してboth / neitherを意図的に当て、「どのhidden dimensionでPとnot-Pが共存するか」「どこでpredicate自体が適用不能か」を先に露出することまでは必須ではない。Catuṣkoṭi contactは、この残差をstate modelへ回収する前に見える形にする。

したがってruntime保持を支持する。ただしmixed / not-applicable / scope / aggregationがtarget側ですでに明示されている場合や、validなbinary decisionを単に曖昧化するだけになる場合はnon-activationとする。

ジャイナ七分法（anekāntavāda / syādvāda）についても、四句分別との名称差を採否の根拠にせず再資格した。固定対象を①read/write/batch/out-of-scopeが混在するmigration status、②internal p95とmobile p99で評価が異なるAPIの「速い」という主張、とした。条件付き述定・視点回転・矛盾分解はtarget-side outputとして有用だが、ordinary requirements / performance reviewもframework接触前からscope、actor、metric、time、assumption、acceptance condition、N/Aを要求する。Cucumber/GherkinのGiven/When/Thenもpreconditionとobservable outcomeを明示する。

`indescribability` 由来の残差についても、tested tasksではnot-applicable、未定義述語、根拠不足の集約を分ける通常手法で保持でき、新規のtarget-side questionが観察されない。したがってcapability overlapに加え、限定した定性的なdiscovery overlapを記録し、general default runtimeからのdemotionを**支持**する。機械的除去も完了し、`profile-ready / no-runtime`として歴史的な七分法・系譜・言表不能性を保持する。blind experimentは未実施であり、新たなtargetで通常手法や四句分別からは出ない視点・表現上の発見が示されれば再検討する。

Huayan（華厳）は、改訂後のdiscovery-aware基準で再資格した最初のruntime保持例となる。canonical Account統合案をsame-targetとして見ると、bounded-context DDD、context mapping、architecture viewpoints、change-impact analysisを組み合わせたmatched specialist baselineは、Huayanからde-bindしたrole-defined identity、context-role re-identification、perspective-through-node、integration-with-differenceを高い割合で再現できる。

しかしframework contact前のgeneric architecture reviewは、ownership、duplication、API、consistency、migration、availability、cost等を自然に扱えても、「同じAccountというidentity自体がcontaining wholeによって成立しているのではないか」「統合後もどの差異を残すべきか」という認知仕事を必ずしも開かない。Huayan contact後にその問いが露出すると、DDDが適切な検証・実装手法として選びやすくなる。

したがってHuayanの保持根拠はunique formal capabilityではなく、**通常入口からは開きにくい認知jobを低い選定負荷で露出し、target-return後にも具体的なarchitecture decisionとして残すdiscovery contribution** に置く。これは、再資格監査がdemotionだけでなくruntime retentionも同じ証拠原則で説明できる最初の例である。

Mīmāṃsā demotion前に`profile_path`がRegistryに記録されていたadopted candidateは次の9件だった。

- `llull-ars`
- `nyaya-five-member-inference`
- `confucian-role-ritual`
- `shinto-threshold-purification`
- `tibetan-buddhist-mandala`
- `classical-stasis-theory`
- `hadith-isnad-matn`
- `mimamsa-hermeneutics`
- `marshallese-wave-navigation`

最初の監査時点では、次の10件がRegistry metadata上`profile_path`を持たなかった。dependent origination、Aristotle's four causes、Wuxingは再資格でprofileを追加したため、現在この未整備群に残るのは7件である。

- `yijing`
- `tzolkin`
- `rasa`
- `huayan`
- `sankhya`
- `catuskoti`
- `jain-sevenfold-predication`

最初の監査時点では、19件すべてについてcandidate metadataに`worked_example_paths`、`negative_example_paths`、`runtime_requalification`が記録されていなかった。

Mīmāṃsāではこれらを構造化して再資格した結果、監査上のevidence gapを解消したうえでruntime維持を支持しない結論になった。これは監査が「採用を守るための証拠集め」ではなく、採用撤回も含む品質管理であることを示す最初のケースである。

他の候補についてmetadataが空いていることは、「正例・負例・比較研究が存在しない」という意味ではない。既存profileや過去のresearch documentに相当する材料があっても、現在のRegistry entryから構造化された再資格根拠として辿れない、という意味である。

## Requalification order

raw framework countや文化圏では順序を決めない。

最初の再資格対象は、次の観点で選ぶ。

- runtimeで使われる頻度や中心性が高い;
- ordinary analysisとの重複可能性が高い;
- 近接frameworkとの境界が現在のruntime選定へ影響する;
- target-returnやnon-activationの境界が不明瞭だと誤用が大きい;
- 既存研究材料を再利用して低コストで再資格できる。

一つのframeworkを再資格するときも、採用維持を前提にしない。ただし、matched specialist baselineが同じoperationを再現したことだけで除外を決めない。そのspecialist methodをframework contact前に選べたか、generic analysisだけで同じ問いが立ったかを別に確認する。

capability overlapに加えてdiscovery contributionも残らない場合は、research referenceへの後退やruntimeからの除外を正当な結果として扱う。逆に、generic baselineや近接frameworkでは出にくい問い・区別・構成がframework contactから生じ、target-return後にも残れば、その差をruntime採用根拠として明示する。

## Product value

この監査の目的は、既存runtimeを大きく見せることではない。

```text
historically adopted
  -> modern evidence made explicit
  -> ordinary baseline challenged
  -> near-neighbor boundary checked
  -> runtime contribution restated or withdrawn
```

という経路を作り、Registry全体に同じ品質原則を適用することである。

これにより、framework追加数ではなく、**通常手法では供給しにくい認知operationをruntimeが実際に保持していること**を、後から再読できる形へ近づける。


## 2026-10-12：ラサ論の再資格に向けた比較資料

ラサ論について、実際の観察結果と混同しない構成例を追加した。

- [表現と受け手の経験を分ける例](worked-examples/rasa-expression-reception.md)：業務画面の保存失敗を題材に、表示内容・画面構成・受け手の立場・経験の仮説を分離する。
- [使わない判断の例](worked-examples/rasa-non-activation.md)：人向け通知が対象にない障害切り分けでは、この体系を使わず技術的な検証を続ける。
- [通常の画面設計レビューとの比較](comparisons/rasa-vs-ordinary-ui-review.md)：体系との接触前から通常の設計レビューを選べる対象であり、能力の重複と発見価値を分けて扱う。

この追加によって、台帳上の具体例・非適用例・通常手法比較の参照は埋まった。ただし比較は独立した実行や利用者観察ではなく、発見価値を支持する証拠には数えない。したがって `discovery_hypothesis` は `unreviewed_hypothesis` を維持し、採用・降格も行わない。

次の判断には、初回の通常レビューと体系接触後の出力を独立に記録し、体系なしでは生じにくい問いが対象へ戻って残るかを検証する必要がある。

## 2026-10-17：Llull後期Arsの能力重複と発見仮説の分離

Llull後期Arsについて、既存の正例・非適用例・近接体系比較に加え、同じ要件レビュー対象に対する二つの資料をRegistryへ結び付けた。

- [通常の要件レビュー／組合せテストとの能力比較](comparisons/llull-ars-vs-ordinary-combinatorial-review.md)：同じ三軸を通常のcombinatorial testingや決定表で交差できるため、組合せ生成をLlull固有の分析能力として主張しない。
- [接触前の方法選択と発見仮説](comparisons/llull-ars-discovery-value.md)：generic requirements reviewの時点で組合せ法が自然に選ばれるかを、体系接触後の再現可能性とは別の問いとして残す。

資料参照は揃ったが、独立した初回レビュー、業務上の実測、追加の発見の有無は未確認である。**ファイル参照の充足は発見価値の受理ではない**。採用状態は `adopted`、発見仮説は `unreviewed_hypothesis` のままとし、保持・降格の結論を追加しない。

## 2026-10-17：神社参拝の境界・清めの暫定比較

神社参拝の境界・準備・中心行為・退出の操作について、既存の本番変更の構成例を通常のchange controlと比較した。

- [非適用例](worked-examples/shinto-threshold-non-activation.md)：変更管理で境界・準備・復旧を扱えている場合や、対象に境界がない場合には活性化しない。
- [能力比較](comparisons/shinto-threshold-vs-ordinary-change-control.md)：通常の変更管理も体系接触前から承認、準備、実行、検証、復旧を扱う。
- [発見価値の机上検討](comparisons/shinto-threshold-discovery-value.md)：本番変更という対象だけから通常手法を選べるため、追加発見の根拠は未取得。
- [近接体系との比較](comparisons/shinto-threshold-vs-rites-of-passage-and-mandala.md)：歴史・構造上の違いを、対象での効果と混同しない。

神社本庁による現代の参拝案内と、國學院大學が区別する手水・修祓等を一つの普遍的手順へ統合しない。宗教上の清めをシステムの認可・衛生の事実へ移さない。

これは資料の整備と定性的な机上監査にとどまる。独立した初回レビュー・実務上の観測は未取得で、採用状態 `adopted` と発見仮説 `unreviewed_hypothesis` を維持する。

## 2026-10-17：Marshallese wave navigation の強い通常手法との再比較

既存の分散処理障害の仮想正例（Q-A、S-B、P-X、S-C、retry振動、zone latency）に対し、一般的な静的グラフではなく**初回から自然に選べるSRE troubleshooting / distributed tracing / observability**を比較対象とした。

- [通常の障害調査との能力比較](comparisons/marshallese-vs-ordinary-observability.md)：五つのde-bound操作はいずれも通常手法と大きく重なる。静的図とlive tracesの差や異常の相関は、対象情報に最初から含まれている。
- [体系接触前の発見可能性](comparisons/marshallese-discovery-value.md)：同じ対象から通常手法を自然に選ぶ可能性が強い。独立した初回レビューは未取得のため、discovery overlapの実測や採用判断ではない。
- [非適用例](worked-examples/marshallese-wave-navigation-negative-boundary.md)：通常のobservabilityが既に同じ問いを扱う場合、および実質的な経路構造のない作業には活性化しない。
- [近接航法伝統](comparisons/marshallese-vs-vaeakau-taumako.md)：文化間の違いをソフトウェアでの認知作用の追加価値と混同しない。

公開のSmithsonian資料、Genzによる航海者や航海学校の差異を越えて、非公開の実践知や統一的な航法体系を推測しない。特に実際の航行・安全判断には使用しない。

Registry上は `adopted`、`adoption_hold: living-tradition-sensitive`、`discovery_hypothesis.evidence_state: unreviewed_hypothesis` を維持。机上の能力重複から直ちに降格せず、独立した比較や対象資料に戻した検証を別工程として残す。

## 2026-10-18：Sāṅkhyaの生成層・観測位置の暫定再資格

固定した架空の注文成功率ダッシュボード（表示低下、gateway counterとの差、event→分類→集計→filter、10:00の分類変更、部署別表示差）で、古典Sāṅkhyaに由来する生成系列・観照側の分離という認知操作を評価した。

- [正例](worked-examples/sankhya-layer-observer.md)では、対象側の検証可能な質問へ戻し、25 tattvaや三guṇaを対象の構成原理に強制しない。
- [非適用例](worked-examples/sankhya-non-activation.md)では、通常のdata lineage・metric definitionで十分な場合に体系を開かない。
- [能力比較](comparisons/sankhya-vs-ordinary-data-lineage-review.md)では、ETL/data lineage・SREの普通の技法が同じ対象への問いをほぼ再現できる。
- [発見価値の机上検討](comparisons/sankhya-discovery-value.md)では、同じ対象の与件だけから通常技法の自然選択が想定でき、体系追加による発見の実測証拠はない。
- [近接比較](comparisons/sankhya-vs-dependent-origination-and-huayan.md)では、生成層、条件介入、関係により成立する同一性の重点を分ける。
- [無接触レビューの固定入力](trials/sankhya-dashboard-target-v1.json)を追加した。初回レビューの独立回答は未取得。

IEPとGRETILの古典文献を出典とするが、puruṣaをダッシュボード閲覧者と同一視せず、宗教・形而上学の理論をデータ計測の事実へ移さない。

採用状態は `adopted`、`discovery_hypothesis.evidence_state` は `unreviewed_hypothesis` を維持する。記録の完全性が改善したことと、独立した発見価値が証明されたことは別である。

## 2026-10-18：Rasaの発見価値を通常UXレビューと照合

既存のRasaの仮想UI保存失敗画面を固定し、表現／構成／受け手の経験を分ける認知操作が、**通常のエラー回復・ユーザビリティレビュー**でどこまで事前に開かれるかを整理した。

- [正例](worked-examples/rasa-expression-reception.md)と[非適用例](worked-examples/rasa-non-activation.md)は既存のものを維持した。
- [通常のUXとの能力比較](comparisons/rasa-vs-ordinary-ui-review.md)は、入力保持、エラー原因、復旧、色・時機・文面・受け手を最初から扱えることを示す。
- [接触前の発見価値](comparisons/rasa-discovery-value.md)では、Nielsen Norman Groupのerror-message guidanceなどの強い普通手法を基準に、通常入口からの重複を明示した。独立した初回レビュー・利用者観察は未取得である。
- [序破急との近接比較](comparisons/rasa-vs-jo-ha-kyu-and-ordinary-reception.md)は、受容経験と展開の緩急という異なる問いを整理し、文化由来の構造差をruntimeでの発見有効性に直結させない。
- [体系名を伏せた固定入力](trials/rasa-save-error-target-v1.json)は元のエラー画面の与件と未知事項を保持する。独立回答は未取得。

Nāṭyaśāstraの美的rasaと、現代の利用者が抱く一時的な不快感・心理状態は同一視しない。実測の受け手の反応がない限り仮説に留める。

この研究で記録したのは強い普通手法との**能力重複と初回選択可能性**であり、追加発見の実測でもruntimeの降格決定でもない。Registryは `adopted`、`unreviewed_hypothesis` を維持する。
