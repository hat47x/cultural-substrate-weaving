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
5. **near-neighbor comparison**
   - 似た認知operationを持つ既存frameworkとの差を同じtargetまたは比較可能な条件で説明できるか。

監査結果には`evidence_gaps`を出すが、score、rank、recommendation、automatic demotionは出さない。

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
    "near_neighbor_comparison_paths": [
      "research/framework-candidates/comparisons/example-vs-neighbor.md"
    ]
  }
}
```

このmetadataは「採用済みであることの証明」ではない。後から同じ判断を再読できるようにするための参照である。

## Current Registry snapshot

2026-10-06の最初の監査時点では、Registry上の`adopted` candidateは19件だった。その後、Mīmāṃsāを現行基準で再資格し、ordinary policy / requirements reviewがtested de-bound operationsを再現したため、general runtimeから外して`profile-ready`へ戻した。

現在の`adopted` candidateは18件である。

Mīmāṃsāに続き、dependent origination（縁起）についても現行基準の再資格を実施した。same-targetでFive Whys、NASA型のfault-tree expansion、通常のdependency analysis、counterfactual / intervention questionと比較した結果、現在runtimeが提供するcondition-chain、upstream-condition、cessation-counterfactual、dependency-reframing、intervention-pointの各操作はordinary baselineで再現された。

このため、dependent originationもgeneral SIer runtime retentionを支持しない研究判断まで進んでいる。現時点のこの文書段階では機械的なruntime removalとは分離しており、source basis、研究profile、正例・non-activation例、Paṭṭhāna近接比較は保持する。

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

次の10件は、現時点のRegistry metadataでは`profile_path`を持たない。

- `yijing`
- `wuxing`
- `tzolkin`
- `dependent-origination`
- `rasa`
- `huayan`
- `sankhya`
- `catuskoti`
- `jain-sevenfold-predication`
- `aristotle-four-causes`

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

一つのframeworkを再資格するときも、採用維持を前提にしない。ordinary baselineと同じoperationしか残らなければ、research referenceへの後退やruntimeからの除外を正当な結果として扱う。

逆に、baselineや近接frameworkでは出ない問い・区別・構成が残れば、その差をruntime採用根拠として明示する。

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
