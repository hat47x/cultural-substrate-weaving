# P2 OpenAI host package materializer — 2026-09-07

## 目的

research suiteでは、ここまでに次を分離してきた。

- Skill / locale realization
- package source boundary
- distribution target name
- source → target Skill subtree mapping
- Skill entry transform
- OpenAI per-Skill / per-profile metadata
- repository外へのSkill-tree materialization

`materialize_skill_tree.py` により、OpenAI向けの三Skill subtreeそのものは一時領域へ実体化できる。

ただしproduction OpenAI packageはSkill treeだけではなく、各Skill packageに

```text
agents/openai.yaml
```

を持つ。さらに現行distributionには、

```text
interactive
metered
```

の二つのprofileがあり、Skill本文は同じでもimplicit invocation policyが異なる。

production `scripts/build.py` をmulti-Skill化する前に、このhost-level compositionまでresearch側で実ファイルtreeとして確認する。

## Script

`research/skill-prototypes/scripts/materialize_openai_packages.py`

## 出力境界

出力先はrepository外の空directoryに限定する。

productionの次のpathへは書き込まない。

- `dist/`
- `plugins/`
- `.agents/`
- `.claude-plugin/`
- `research/`配下の生成物

したがって、このmaterializerを実行してもproduction build artifactは変わらない。

## 構成

ja-JPでは現在、三Skillすべてにruntime realizationとOpenAI metadataがある。

```text
output/
  interactive/
    cultural-substrate-weaving/
      SKILL.md
      references/...
      agents/openai.yaml
    affinity-synthesis/
      SKILL.md
      references/...
      evals/...
      evidence/...
      agents/openai.yaml
    iterative-inquiry-synthesis/
      SKILL.md
      references/...
      agents/openai.yaml

  metered/
    cultural-substrate-weaving/
    affinity-synthesis/
    iterative-inquiry-synthesis/
```

Skill subtreeは既存の`materialize_skill_tree.py`を使う。OpenAI host materializerが別のSkill rendererを持つことはしない。

## Metadata source

各`agents/openai.yaml`は`adapter-metadata-plan.json`が宣言したsourceをbyte copyする。

### Cultural Substrate Weaving

既存production adapterを使う。

```text
adapters/openai-skill/<locale>/openai.interactive.yaml
adapters/openai-skill/<locale>/openai.metered.yaml
```

### Affinity / Iterative

ja-JPではresearch prototype metadataを使う。

```text
research/skill-prototypes/adapters/openai-skill/ja-JP/<skill>/openai.interactive.yaml
research/skill-prototypes/adapters/openai-skill/ja-JP/<skill>/openai.metered.yaml
```

materializerはdescriptionやdefault promptを再生成しない。metadata wordingの正本はdescriptorが指すsource fileに置く。

## Profile invariant

interactive / meteredで変えてよいのはhost metadataであり、Skill method treeではない。

回帰testでは、各Skillについて`agents/openai.yaml`を除く全ファイルを比較し、interactive / metered間でbyte一致することを要求する。

metadataについては、descriptorが指すsourceとのbyte一致を要求する。

現在のpolicyは次のまま保持する。

```text
interactive: allow_implicit_invocation: true
metered:     allow_implicit_invocation: false
```

このmaterializerはprofile policyを設計し直さない。

## Partial locale

en-USでは現時点で、

```text
cultural-substrate-weaving: existing
affinity-synthesis: planned
iterative-inquiry-synthesis: planned
```

である。

通常実行ではpartial packageを拒否する。

`allow_partial=True`を明示したresearch probeの場合だけ、現在realizedしているCSWをinteractive / meteredそれぞれへ実体化できる。

これは英語suiteがbuildableまたはrelease-readyであることを意味しない。

## Fail-closed boundary

次ではmaterializationを拒否する。

- repository内output
- non-empty output
- invalid suite / package / adapter metadata contract
- runtime subtreeがblocked
- partial runtimeを明示許可していない
- realized SkillのOpenAI metadataが`existing`または`prototype`でない
- metadata sourceがない、またはrepository外を指す
- materialized Skill subtreeが見つからない

## Tests

`tests/test_research_openai_package_materializer.py`では少なくとも次を固定する。

1. ja-JPで3 Skill × 2 profile = 6 packageができる。
2. OpenAI Skill entryに`disable-model-invocation`を入れない。
3. interactive / meteredのSkill tree本体はbyte一致する。
4. packaged `agents/openai.yaml`はdeclared sourceとbyte一致する。
5. interactive / meteredのimplicit invocation policyが保持される。
6. en-US partialは明示しない限り拒否する。
7. 明示partialではCSWだけを2 profileへ作る。
8. repository内outputを拒否する。

## 何をまだ意味しないか

この段階では、次を主張しない。

- OpenAI hostが三Skillを意図どおりroutingする。
- companion metadataがproduction-reviewedである。
- generated `dist/`がmulti-Skill化された。
- release packageが作成できる。
- canonical CSWからKJ / iterative責務を除去してよい。
- en-US companion realizationが完成した。

特にinteractive implicit invocationの実routingはhost executionによる別評価が必要である。

## PR #294との関係

PR #294は、research Skill-tree materializerが既存ja-JP CSW `skills/weave/`をbyte-for-byteで再現するgateを追加する。

このOpenAI host materializerはその次のcomposition boundaryを扱うが、PR #294の実測成功を代替しない。

二つを分けることで、

```text
Skill renderer parity
        ↓
OpenAI host package composition
        ↓
production builder generalization
```

の順に証拠を積める。

## 次の段階

このmaterializerとテストを完全checkout上で通した後、OpenAI production builderのgeneralizationでは、次の最小変更を比較できる。

1. Skill treeの生成はresearchで検証したsource / transform contractへ寄せる。
2. profile loopはSkill method treeを再生成せず、同じtreeへprofile metadataを組み合わせる責務として分離する。
3. CSW既存adapterのbyte内容を変えない。
4. companion metadataはprototypeのまま、production昇格判断とbuild mechanicsを分ける。

Claude/Codex bundleについては、OpenAIとは別にplugin-level manifest / marketplace / READMEのcompositionをresearch側で実体化してからproductionへ進む。

## 結論

**P2 research suiteは、OpenAIについてSkill subtree planningだけでなく、profile metadataを含むhost package候補までrepository外で実体化できる段階へ進む。**

これはproduction migrationそのものではなく、production migrationで壊してはならないpackage topologyとmetadata provenanceを、先に実ファイルtreeとして固定するための中間証拠である。
