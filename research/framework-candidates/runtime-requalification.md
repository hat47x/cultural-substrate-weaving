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

現在の`adopted` candidateは15件である。

Mīmāṃsāに続き、dependent origination（縁起）についても再資格した。旧比較ではsame-targetへFive Whys、fault-tree expansion、dependency analysis、counterfactual / intervention questionを適用し、condition-chain、upstream-condition、cessation-counterfactual、dependency-reframing、intervention-pointを再現できたためgeneral default runtimeから外した。

改訂後のdiscovery-aware基準で遡及reviewすると、ordinary post-incident practice自体がframework contact前から「どのcomponents / conditions / actions / eventsが寄与したか」「どのmitigation / corrective actionで再発を防ぐか」「変更後に何が変わるべきか」を自然に問う。tested rolling-deployment incidentでも、stale capability、heartbeat、credential state、dispatch window、queue redeliveryなどの条件群と介入後のfailure cessationへframeworkなしで到達できる。

したがってdependent originationではcapability overlapだけでなく**discovery overlap**も成立する。旧demotionをdiscovery-aware基準でも確認済みとし、`profile-ready / no-runtime`を維持する。source basis、研究profile、正例・non-activation例、ordinary capability比較、discovery-value比較、Paṭṭhāna近接比較、selection cueは保持する。

続いてclassical stasis theoryを、既存のrelease-incident target上でordinary incident / issue triageと比較した。事実、定義、評価、手続き・権限の分離、争点移動、issueごとの証拠適合は、target-languageのissue tableとreply-to-issue対応で再現できたため、旧基準ではgeneral default runtimeから外して`profile-ready`へ戻した。

しかし改訂後のdiscovery-aware基準で遡及reviewすると、このissue tableは「争点の種類を分ける」という認知jobを既に知った後のmatched specialist baselineだった。framework名もissue taxonomyも与えないgeneric incident / postmortem baselineはtimeline、impact、root cause、mitigation、roles、actionsを自然に扱う一方、fact / definition / evaluation / authorityという異なるanswer typeが同じ会話内で走っていることや、replyがissue typeを切り替えたことを必ずしも前景化しない。

stasis contactは「何を争っているのか」を先に問い、eventを認めても残るdefinition/evaluation、definitionを揃えても残るquality/procedure、そしてissue-specific evidenceとstasis-switchを露出する。この差はde-binding後にもtarget-side questionとして残る。したがってretrospective discovery-value reviewはruntime restorationを支持し、mechanical restorationも完了した。classical stasis theoryは再びdefault runtimeのadopted candidateとして利用できる。

Aristotle's four causesについても現行基準の再資格を実施した。multi-tenant rate-limiterをsame-targetとして、NASA型systems engineeringのstakeholder expectations、constraints、logical decomposition、design solution / behaviorと比較した結果、runtimeが提供していたwhy-splitting、explanation-gap、causal-category-audit、multi-cause-composition、artifact-design-probeはordinary baselineで再現された。

このため、Aristotle's four causesもgeneral default runtimeから外して`profile-ready`へ戻した。source basis、研究profile、正例・non-activation例、dependent-origination近接比較、selection cueは保持しており、explicit Aristotle / history-of-philosophy / comparative-explanation / educational useから再検討できる。

Wuxing（五行）についても、distributed-worker autoscalerのoscillationをsame-targetとして、ordinary signed causal-loop / system-dynamics analysisと比較した。生成／制約という二種類の関係、feedback loop、edgeごとのrole変化、missing link、operating stateによるrelation changeは、target-languageのdirected typed graphで再現でき、追加のtarget-side questionは残らなかった。歴史的な`sheng` / `ke`とmodern causal polarityの同一性は主張せず、tested SIer useでde-bind後の問いが重複するという限定的なruntime product boundaryとして扱う。

Wuxingについては、その後同じautoscaler targetへdiscovery-value comparisonを追加した。framework名もspecialist method名も与えないgeneric incident baselineから、oscillationという症状を手掛かりにcontroller input/output、repeated reaction、delay、retry、damping、stabilization、over-correctionへ自然に進める。Kubernetes HPAの通常資料もautoscalingをcontrol loopとして扱い、replicaのflapping / thrashingとstabilizationを標準的な運用問題として明示している。

したがってWuxingでは、matched specialist methodによる**capability overlap**だけでなく、targetと通常運用知識から同じfeedback/control jobをframework contact前に選べるという**discovery overlap**も確認できた。Huayanとは逆に、de-binding後にruntime固有のdiscovery contributionが残らない。general SIer runtime removalを改訂後のdiscovery-aware基準でも支持し、default runtimeから外して`profile-ready`へ戻した。source basis、研究profile、正例・non-activation例、ordinary capability比較、discovery-value比較、near-neighbor比較、selection cueは保持する。

なお、Mīmāṃsā、dependent origination、classical stasis theory、Aristotle's four causesの4件は、このcapability-overlap / discovery-value分離を導入する前にruntimeから降格した。classical stasis theoryは遡及reviewでdiscovery contributionが残りruntimeへ復帰した。dependent originationは遡及reviewでdiscovery overlapまで確認し、demotionを新基準でも確定した。残るMīmāṃsāとAristotle's four causesの2件は、既存比較が主としてcapability overlapを示している段階であり、**発見価値がないことまでは確定していない**。引き続きretrospective discovery-value reviewの対象とする。

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
