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

### Claude/Codex

locale bundle metadataが次のどちらかである必要がある。

- `prototype`
- `reviewed`

`existing-baseline`から導かれる`review-required`は、三Skill bundleのmetadataとしてはmaterialize-readyにしない。

これにより、en-US companion runtimeを将来追加してもsingle-Skill時代のmetadataを無言で三Skill bundleへ流用できない。

## Entry transform

### Companion Skills

`explicit_files`の`SKILL.md`はprototype frontmatterを読み、distribution target名へ`name`を正規化する。

- OpenAI: `disable-model-invocation`なし
- Claude/Codex: `disable-model-invocation: true`

### Cultural Substrate Weaving

CSWはresearch用rendererを新設しない。

production `scripts/build.py` の `skill_frontmatter()` と `scripts/common.py` の `replace_router_links()` を再利用し、既存canonical build semanticsと同じrender boundaryを使う。

これによりresearch materializerが別のCSW adapter仕様を発明することを避ける。

## Relative structure

entry以外のexplicit filesはsource root相対pathをそのままtarget Skill rootへ保持する。

例:

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

Iterativeも`references/METHOD.md`と`references/ROUND-TEMPLATE.md`を保持する。

CSW modulesは既存`src/manifest.json`の`skill_reference`へ従い、`references/00-...`〜`10-integration.md`へ写像する。

## Partial probe

en-US OpenAIは現時点でCSWだけexisting、companion二Skillはplannedである。

通常materializationは`partial`を拒否する。

`allow_partial=True`を明示したresearch probeだけ、現在realizedしているCSW subtreeを生成できる。

これは「en-US suiteがbuildable」という意味ではない。

Claude/Codexは、たとえpartialを明示してもbundle metadataが`review-required`のため拒否する。

## Current regression expectations

### ja-JP OpenAI

三つのstandalone treeを生成する。

```text
cultural-substrate-weaving/
affinity-synthesis/
iterative-inquiry-synthesis/
```

各`SKILL.md`に`disable-model-invocation`は付けない。

### ja-JP Claude/Codex

```text
skills/
  weave/
  affinity-synthesis/
  iterative-inquiry-synthesis/
```

三つの`SKILL.md`に`disable-model-invocation: true`を一度だけ付ける。

### en-US OpenAI

通常はpartialのため拒否する。

明示的partial probeでは`cultural-substrate-weaving/`だけを生成する。

### en-US Claude/Codex

runtime不足に加えbundle metadataもproduction baselineのreview-required状態なので、partial probeでもmaterializeしない。

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

このPRではunit testを追加するが、complete checkoutが利用できないため実`make check`成功を主張しない。

GitHub Actionsも意図的に無効である。

## 次の段階

materializerが実checkout上でunit testを通った後、次を比較できる。

1. research materialized ja-JP CSW subtree と現行production generated subtree
2. companion Skill subtreeのfrontmatter / relative reference
3. production builder generalization時に必要な最小共通関数
4. host metadata materializerをSkill tree materializerへ接続するか

この比較まではcanonical migrationやproduction builder置換へ進まない。

## 結論

P2 research contractからSkill subtreeを**repository外の一時領域だけへ**実体化する境界を設計した。

これにより、read-only planからproduction migrationへ直接飛ばず、実ファイルtreeを中間証拠として挟める。
