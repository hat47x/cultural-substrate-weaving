# Production Skill-set projection — 2026-09-07

## 目的

research上でSkill realizationが存在することと、production配布物へ含めることを分離した状態から、production側が必要とする最小のSkill集合だけを表現する。

この段階ではcompanion Skillをproductionへ昇格しない。`affinity-synthesis` と `iterative-inquiry-synthesis` は、他レーンで名称・責務境界・handoff・評価を継続検討しているresearch candidateのままとする。

## 他レーンとの協調境界

現在の他レーンでは、次の判断を維持している。

- KJ系の一回統合と複数ラウンドの探索継続をCSWから分離する方向は有力である。
- `affinity-synthesis` / `iterative-inquiry-synthesis` は現時点のworking nameであり、公開最終名とはみなさない。
- CSW → Iterative → Affinityのhandoffでは、`framework_generated` 等のprovenanceとepistemic statusをtarget-side supportへ無言で昇格させない。
- 現行canonical `src/ja-JP/methods/integration.md` と `src/ja-JP/core/iteration.md` は、handoffとpaired evaluationが十分になるまで縮小しない。
- ja-JP companion prototypeがpackage可能でも、それだけではproduction昇格条件を満たさない。
- en-US companion realizationはplanned / blockedのままであり、production parityを主張しない。

このレーンは上記判断を上書きしない。production側には、他レーンで昇格判断が確定したSkillだけを受け入れる薄い境界を用意する。

## Production descriptor が所有するもの

`src/skill-set.json` は次の二つだけを所有する。

1. productionに含めるSkillのidentity
2. そのSkillのproduction source manifestへの参照

現在は次だけである。

```json
{
  "schema": "csw.production-skill-set/v1",
  "skills": [
    {
      "id": "cultural-substrate-weaving",
      "source_manifest": "src/manifest.json"
    }
  ]
}
```

## Production descriptor が所有しないもの

次は既存の正本・adapter・host metadataに残し、`src/skill-set.json`へ複製しない。

- locale一覧
- canonical locale
- router path
- module / reference一覧
- Skill description
- OpenAI display / prompt / invocation policy
- Claude / Codex plugin name, display, description
- host別target Skill name
- research maturity (`prototype`, `candidate`, `blocked` 等)
- promotion gateの評価結果
- handoff contractの内容

これらをdescriptorに再掲すると、既存の `src/manifest.json`、adapter metadata、research suiteとの間に複数正本が生じるためである。

## 二つの検証面

### 1. Production 単独検証

`scripts/validate_production_skill_set.py` はresearch treeを読まない。

検査するのは次だけである。

- schema
- Skill集合が空でないこと
- Skill idの一意性
- descriptor entryが `id` と `source_manifest` 以外を所有しないこと
- `source_manifest` がrepository内の `src/` 配下を指すこと
- manifestの `name` がSkill idと一致すること
- manifestがlocaleとcanonical localeを持つこと

これによりproduction releaseはresearch treeがなくても自分の公開境界を説明できる。

### 2. Research → production 射影検証

`research/skill-prototypes/scripts/validate_production_projection.py` は、research inclusion planとproduction Skill-setを比較する。

- `production_state = included` のSkillだけがproduction descriptorに現れる。
- `candidate` / `blocked` はproductionに漏れない。
- research inclusion decisionが指したmanifestとproduction source manifestが一致する。

したがって、

```text
research realization exists
        !=
research production_state = included
        !=
production Skill-set member
```

という三段階を保つ。

## Build との接続はまだ行わない

本段階では `scripts/build.py` は `src/skill-set.json` を読まない。

理由は、production builderのgeneric writer / validatorのrefactorと、production inclusion decisionの検証が別PRとしてまだ並行しているためである。descriptorを追加しただけでbuild outputを変えると、mechanical refactorと公開集合変更の原因を分離できなくなる。

まずproduction descriptor自身を `make check` の契約へ入れる。その後、generic writer / validatorが統合された段階で、現在のCSW一つだけをdescriptor経由で解決しても生成物がbyte不変になることを次のgateとする。

## Companion promotion の前提

このdescriptorへcompanion Skillを追加する前に、少なくとも次を別レーンの判断と照合する。

- 公開Skill名がworking nameのままでよいか
- one-round / multi-round / cultural-frameworkの責務境界が安定しているか
- CSW → Iterative → Affinityのprovenance handoffが十分に評価されているか
- canonical `integration.md` / `iteration.md` の縮小範囲が確定しているか
- fallback時に未実行のsynthesisを実行済みと誤認しないか
- ja-JPのpackage / adapter metadataがprototypeからproduction review済みへ進んでいるか
- en-US realization parityを要求するか、localeごとの公開を認めるか
- hostごとのrouting / invocation behaviorが実環境で確認されているか
- 完全checkout上の `make check` とgenerated artifact parityが通っているか

これらは `src/skill-set.json` が所有する情報ではなく、追加判断のgateである。

## 現段階の結論

production Skill-set descriptorは、将来のmulti-Skill化を先取りしてcompanionを公開する仕組みではない。

**現在公開しているものを最小のidentity/source contractとして明示し、他レーンで昇格判断が確定したときだけ公開集合を一箇所で変更できるようにする境界である。**

そのため、現時点のproduction memberは `cultural-substrate-weaving` 一つだけとする。
