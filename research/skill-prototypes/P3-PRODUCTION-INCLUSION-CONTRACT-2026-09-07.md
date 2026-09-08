# P3 Production Skill inclusion contract — 2026-09-07

## 目的

三Skill suiteのresearch prototypeが揃ってくると、次の二つを混同しやすくなる。

1. **research realizationが存在する**
2. **production artifactへ含めることを決定した**

この二つは別である。

特にja-JPでは現在、`affinity-synthesis`と`iterative-inquiry-synthesis`のruntime prototype、package source、target naming、host metadata prototypeまで存在する。

しかし、それだけでproduction builderが二Skillを出力してよいとはしない。

そこで`production-inclusion-plan.json`をresearch側に置き、**production publication boundaryそのものを明示的な状態として観察する。**

このfileはまだproduction builderの入力ではない。

## Current state

### Cultural Substrate Weaving

```text
production_state: included
ja-JP: included
en-US: included
production_source: src/manifest.json
```

これは現在のrelease lineが既に公開・生成している状態を記述する。

### Affinity Synthesis

```text
production_state: candidate
ja-JP: candidate
en-US: blocked
production_source: null
```

ja-JP realizationが存在しても`candidate`のままである。

en-US realizationはsuite manifest上`planned`なので`blocked`とする。

### Iterative Inquiry Synthesis

Affinityと同じく、

```text
production_state: candidate
ja-JP: candidate
en-US: blocked
production_source: null
```

とする。

## State semantics

### `included`

現在のproduction publication boundaryへ入っている。

Skill-levelで`included`ならproduction source contractが必要であり、locale realizationもresearch suite上`planned`だけではいけない。

### `candidate`

方法・realization・package probe等が研究対象として存在し得るが、production sourceをまだ所有しない。

`package_targets`やadapter metadata prototypeが研究側に存在しても、この状態を自動で`included`へ変えない。

### locale `blocked`

Skill-levelではcandidateだが、そのlocale realization自体がまだ`planned`である。

現在のen-US companion二Skillが該当する。

`blocked`は品質が低いという評価ではなく、production inclusionを検討するためのruntime realizationがまだないという状態である。

## Why candidate Skill has no production_source

candidateへproduction source pathを先に与えると、builder側が

> sourceがあるので生成可能

と解釈しやすくなる。

research sourceは既にsuite manifestが所有しているため、production inclusion planへ重複して持たせない。

production sourceを持てるのは`included`だけとする。

これにより、

```text
research source exists
    ≠
production source assigned
```

を構造として保つ。

## Validator

`scripts/validate_research_production_inclusion.py`は次を検査する。

- inclusion planのSkill集合がresearch suiteと一致する。
- `included / candidate`以外のSkill状態を許さない。
- included Skillにはproduction sourceがある。
- candidate Skillはproduction sourceを主張しない。
- locale集合がsuite locale集合と一致する。
- candidateのrealized localeは`candidate`、planned localeは`blocked`である。
- included Skillのlocale realizationがplanned-onlyではない。
- canonical manifest型production sourceは実在し、Skill identity / locale / router entryと整合する。
- 少なくとも一つのproduction included Skillがある。

このvalidatorはpromotionを決定しない。

## Important negative guarantee

次の情報だけではpromotionしない。

- ja-JP prototypeが存在する。
- eval caseがpassした。
- package materializerがtreeを作れる。
- host metadata prototypeがある。
- target nameが決まっている。
- builderがgeneric化された。
- validatorがgeneric化された。

これらは必要な準備や証拠になり得るが、production inclusionそのものではない。

## Promotion event

将来companion Skillをproductionへ含める場合は、少なくとも状態変化を明示する。

```text
candidate
  ↓ explicit promotion decision
included
```

そのとき初めてproduction sourceを割り当てる。

同時に、

- production builder入力
- production validator対象
- host metadata maturity
- locale availability
- release/package contract

を同期させる。

一つだけ先に変えない。

## Relation to P3 writer / validator refactors

#297 / #298で進めているmechanical refactorは、このinclusion判断を所有しない。

```text
production inclusion contract
        ↓ enabled set
writer   ───────── validator
```

という形を将来作るため、先にwriter / validatorをartifact単位へ分けている。

現段階ではproduction codeはまだこのresearch inclusion planを読まない。

## Why this remains under research/

production descriptorの最終schemaはまだ確定していない。

特にcompanion昇格時には、

- canonical source layout
- locale translation policy
- host metadata正本
- package target naming

をどのdescriptorが所有するかを決める必要がある。

その判断前に、このprototype fileをproduction正本へ昇格しない。

まず「research candidateとproduction includedを分ける」という状態契約だけを検証する。

## Next step

この境界が安定した後は、production descriptorへ何を移すべきかを決める。

有力なのは、production descriptorを巨大なsuite manifestにせず、

- inclusion state
- production source contractへの参照

を中心に薄く保ち、host固有metadataは既存adapter正本へ残す構成である。

これならresearch suiteのpackage設計をそのままproductionへ複製せずに済む。

## 結論

**prototypeが完成に近づくほど、production inclusionは暗黙にしない。research realizationと公開判断の間に明示的な状態境界を置き、sourceを持つことと公開することを分離する。**
