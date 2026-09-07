# P2 research Skill-tree materializer — 2026-09-07

## 目的

P2で次の契約をread-only plannerとして外部化した。

- skill / locale realization
- package source boundary
- distribution target name
- source → target subtree mapping
- Skill entry frontmatter transform
- OpenAI per-Skill metadata coverage
- Claude/Codex bundle metadata coverage

次の段階として、これらのplanから**実ファイルtreeを一時領域へ組み立てられるか**を確認する。

production builderをgeneralizeする前に、path mappingやfrontmatter transformが机上のJSONだけでなくファイルtreeとして整合するかを観察するためのpre-production probeである。

## Script

`research/skill-prototypes/scripts/materialize_skill_tree.py`

## 書込み境界

materializerはoutput rootがrepository内にある場合、必ず拒否する。

したがって次には書き込めない。

- `dist/`
- `plugins/`
- `.agents/`
- `.claude-plugin/`
- `research/`配下を含むrepository内の任意path

output rootはrepository外の空directory、またはまだ存在しないpathでなければならない。

既存の非空directoryも上書きしない。

## 対象distribution

Skill subtreeを実体化する次の三つだけを扱う。

- `openai_skill`
- `claude_plugin`
- `codex_plugin`

次は対象外である。

- `chatgpt_gpt`
- `microsoft_copilot`

これらは現時点でcomposite agent realizationであり、research suiteはsibling Skill tree materializationを宣言していない。

## Materialization inputs

実行前に次のvalidatorを通す。

- research suite manifest
- package target contract
- adapter metadata contract

さらにresearch gateでは、runtime entryが参照するpackage-local fileが `package_source.files` に閉じていることをreference-closure validatorで確認する。

その後、次を組み合わせる。

1. `plan_skill_subtrees.py`
   - source → target path
2. `plan_skill_entry_transforms.py`
   - `SKILL.md` frontmatter/render policy
3. `plan_adapter_metadata.py`
   - runtimeとadapter metadataのmaturity

## Metadata gate

### OpenAI

materialize対象となるrealized Skillについて、metadata stateが次のどちらかである必要がある。

- `existing`
- `prototype`

`planned`や`runtime-blocked`はmaterialize-readyとはしない。

現在はja-JP / en-USとも、CSWが`existing`、Affinity / Iterativeが`prototype`である。三Skill runtimeも両localeでbuildableなので、OpenAI Skill treeは日英とも通常モードでmaterialize可能である。

### Claude/Codex

locale bundle metadataが次のどちらかである必要がある。

- `prototype`
- `reviewed`

`existing-baseline`から導かれる`review-required`は、三Skill bundleのmetadataとしてはmaterialize-readyにしない。

現在はja-JP / en-USともbundle-specific research prototypeがあるため、Claude/Codex Skill treeも両localeでmaterialize可能である。

ただし、metadata sourceが`prototype`である限り、production-approvedとは扱わない。

## Entry transform

### Companion Skills

`explicit_files`のruntime entryはprototype frontmatterを読み、distribution target名へ`name`を正規化する。

ja-JPではsource entryが `SKILL.md`、en-USでは `SKILL.en.md` だが、package側のentry名はいずれも `SKILL.md` とする。

- OpenAI: `disable-model-invocation`なし
- Claude/Codex: `disable-model-invocation: true`

### Cultural Substrate Weaving

CSWはresearch用rendererを新設しない。

production `scripts/build.py` の `skill_frontmatter()` と `scripts/common.py` の `replace_router_links()` を再利用し、既存canonical build semanticsと同じrender boundaryを使う。

これによりresearch materializerが別のCSW adapter仕様を発明することを避ける。

## Relative structure

entry以外のexplicit filesはsource root相対pathをそのままtarget Skill rootへ保持する。

ja-JP Affinityの例:

```text
affinity-synthesis/
  SKILL.md
  references/METHOD.md
  references/REPRESENTATION.md
  references/TEMPLATE.md
  references/affinity-map.schema.json
  evals/CASES.md
  evidence/dossier.md
```

en-USでは英語runtime / Method Definitionを使うため、たとえば次を保持する。

```text
affinity-synthesis/
  SKILL.md                 # source: SKILL.en.md
  references/METHOD.en.md
  references/REPRESENTATION.md
  references/affinity-map.schema.json
```

IterativeもlocaleごとのMethod Definitionと `references/ROUND-TEMPLATE.md` を保持する。

CSW modulesは既存`src/manifest.json`の`skill_reference`へ従い、両localeとも `references/00-...`〜`10-integration.md` へ写像する。

## Current regression expectations

### OpenAI — ja-JP / en-US

両localeで三つのstandalone treeを生成する。

```text
cultural-substrate-weaving/
affinity-synthesis/
iterative-inquiry-synthesis/
```

各`SKILL.md`に`disable-model-invocation`は付けない。

英語側でもpackage entry名は`SKILL.md`へ正規化するが、英語Method Definitionは `references/METHOD.en.md` として保持する。

### Claude/Codex — ja-JP / en-US

両localeで次のshared Skill treeを生成する。

```text
skills/
  weave/
  affinity-synthesis/
  iterative-inquiry-synthesis/
```

三つの`SKILL.md`に`disable-model-invocation: true`を一度だけ付ける。

これにより、英語metadataが揃った後もClaude/Codexのexplicit invocation policyがlocaleによって変わらないことを検査できる。

## `allow_partial` の位置づけ

`allow_partial=True` はruntime/subtree不足を意図的に観察するためのresearch例外であり、metadata maturity gateを迂回する機能ではない。

現在の日英Skill-tree distributionsはruntime/package/metadataが揃っているため、通常のregression expectationではpartial materializationを使わない。

将来、一部localeや一部Skillを再び`planned`へ戻す研究変更が入った場合でも、metadata不足を`allow_partial`で無視してはならない。

## まだ生成しないもの

このmaterializerは次を生成しない。

- OpenAI `agents/openai.yaml`
- Claude `.claude-plugin/plugin.json`
- Codex `.codex-plugin/plugin.json`
- marketplace catalogs
- README
- GPT/Copilot composite files
- ZIP
- release manifest
- release asset

したがって「host packageが完成した」とは扱えない。

adapter metadata prototypeはmaterialization可否のgateとして参照するが、このscript自体はmetadata fileをoutputへ書き出さない。

## 失敗時の扱い

次ではfail-closedにする。

- invalid research manifest / metadata contract
- target collision
- blocked subtree
- partial subtreeを明示許可していない
- adapter metadata maturity不足
- missing source
- output path escape
- duplicate target
- unsupported entry transform
- non-empty output root
- repository内output root

## 検証境界

unit test fixtureでは、ja-JP / en-US × OpenAI / Claude / CodexのSkill treeを通常モードでmaterializeする期待値へ更新した。

ただし、現在の実行環境ではcomplete repository checkoutを確保できず、接続済み開発端末もofflineである。そのため、実 `make research-skill-check` / `make check` 成功はまだ主張しない。

adapter metadataについては、source・descriptor・validator contractを静的に整合させた。materializer自体の実ファイルtree生成は、complete checkoutでのunit testをpromotion gateとして残す。

## 次の段階

materializerが実checkout上でunit testを通った後、次を比較できる。

1. research materialized ja-JP / en-US CSW subtree と現行production generated subtree
2. companion Skill subtreeのfrontmatter / relative reference / locale identity
3. production builder generalization時に必要な最小共通関数
4. host metadata materializerをSkill tree materializerへ接続するか

この比較まではproduction builder置換やrelease asset変更へ進まない。

## 結論

P2 research contractから、ja-JP / en-US双方のSkill subtreeを**repository外の一時領域だけへ**実体化できる条件を設計上そろえた。

これにより、read-only planからproduction migrationへ直接飛ばず、bilingualな実ファイルtreeを中間証拠として挟める。
