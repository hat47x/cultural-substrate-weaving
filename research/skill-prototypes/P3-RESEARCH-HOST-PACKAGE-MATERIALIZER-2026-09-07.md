# P3 research host package materializer — 2026-09-07

## 目的

P2までに、三Skill × 二localeについて次の境界を別々に外部化した。

- runtime realization
- package source
- distribution target name
- Skill subtree mapping
- `SKILL.md` entry transform
- OpenAI per-Skill metadata
- Claude/Codex bundle metadata
- package-local reference closure

さらに `materialize_skill_tree.py` により、これらからSkill treeそのものをrepository外の一時領域へ実体化する境界を設けた。

P3では、その一段外側にある**package-local host metadata**までを同じ一時領域へ付加し、production builderを変更する前にhost packageの最小形状を確認できるようにする。

この段階の目的はrelease packageを作ることではない。

```text
method/runtime contract
        ↓
Skill tree materialization
        ↓
package-local host metadata
        ↓
[ここまでをresearch probeで確認]
        ↓
marketplace / README / archive / release manifest
        ↓
[まだ生成しない]
```

## Script

`research/skill-prototypes/scripts/materialize_host_package.py`

このscriptは `materialize_skill_tree.py` を再利用する。別のSkill-tree rendererを作らない。

そのため、次の安全境界を継承する。

- outputはrepository外だけ。
- 非空output directoryを上書きしない。
- subtree collisionを許さない。
- runtime/package/adapter metadata validationを通す。
- package-local reference closureを通す。
- metadata maturity不足を迂回しない。

## 対象distribution

対象はSkill treeを持つ次の三つに限定する。

- `openai_skill`
- `claude_plugin`
- `codex_plugin`

次は扱わない。

- `chatgpt_gpt`
- `microsoft_copilot`

これらは現時点ではcomposite agent realizationであり、三つのsibling Skill treeをそのままhost packageへ置く契約ではない。

## OpenAI Skill

OpenAIはstandalone per-Skill packageなので、まずSkill treeを次の形でmaterializeする。

```text
cultural-substrate-weaving/
affinity-synthesis/
iterative-inquiry-synthesis/
```

その後、指定profileについて各Skillへ、

```text
<skill>/agents/openai.yaml
```

を追加する。

profileは明示必須とする。

```text
interactive
metered
```

metadata sourceは `adapter-metadata-plan.json` のSkill × locale × profile declarationから取得する。

materialize可能なmetadata stateは、

```text
existing | prototype
```

だけである。

現在はja-JP / en-USとも、

- CSW = `existing`
- Affinity = `prototype`
- Iterative = `prototype`

なので、両locale・両profileの最小host packageをresearch上組み立てられる。

### Profile差

`interactive` と `metered` のMethod内容は分けない。

現在の差は、

```text
interactive: allow_implicit_invocation = true
metered:     allow_implicit_invocation = false
```

だけである。

host package materializerもこのsource fileをそのままcopyし、独自にprofile文面を書き換えない。

## Claude plugin

Claudeはlocale bundleとして、三Skillを次へ置く。

```text
skills/
  weave/
  affinity-synthesis/
  iterative-inquiry-synthesis/
```

そのうえで、

```text
.claude-plugin/plugin.json
```

だけを追加する。

manifest shapeは現行production `scripts/build.py` と同じ項目を使う。

```text
name
description
version
author
homepage
repository
license
```

`name` / `description` はlocale bundle metadataから取得し、`version` はrepository `VERSION` から取得する。

prototype bundleでは、既存plugin identityを維持する。

```text
ja-JP: cultural-substrate-weaving-ja
en-US: cultural-substrate-weaving-en
```

ただしdescriptionは旧単一Skillのものではなく、三Skillの責務分離を説明するresearch prototypeを使う。

## Codex plugin

Codexも同じ `skills/` treeを使い、

```text
.codex-plugin/plugin.json
```

だけを追加する。

manifest shapeは現行production builderに合わせる。

- name
- version
- description
- author
- homepage
- repository
- license
- keywords
- `skills = ./skills/`
- interface
  - displayName
  - shortDescription
  - developerName
  - category

locale keywordはproductionと同じ `ja` / `en` を使う。

ClaudeとCodexでSkill treeを別々に設計しない。host固有差はmanifestに限定する。

## Production generated artifactとの静的照合

現行production artifactを確認すると、Claude manifestとCodex manifestのfield構成はresearch materializerのrendererと一致している。

一方、description本文は一致しない。

これは意図した差である。

現行production artifactはsplit前のCSW説明を持ち、research prototypeは、

- cultural-framework exploration
- one-round affinity synthesis
- multi-round inquiry continuation

を別Skillとして説明する。

したがってこの段階で比較するのは**manifest shapeとidentity contract**であり、旧descriptionとの文字列一致ではない。

## 生成しないもの

host package materializerは次を生成しない。

- Claude marketplace catalog
- Codex marketplace catalog
- root `.agents` catalog
- README
- deployment guide
- ZIP / archive
- release manifest
- release asset
- GPT/Copilot composite artifact

OpenAIでも、各Skillの `agents/openai.yaml` より外側の配布catalogは作らない。

この境界により、research probeがproduction release pipelineの代替になることを避ける。

## Reference closure

`materialize_skill_tree._validated_inputs()` は、suite / target / adapter metadataだけでなく、

```text
validate_research_package_reference_closure.py
```

も通す。

このpreflightはhost package materializerにも継承される。

したがって、runtime entryが `references/`、`evals/`、`evidence/` などのpackage-local fileを指しているのに `package_source.files` がそれを落としている場合、host metadataを付ける前に停止する。

Makefile gateだけに依存せず、materializer単独でも同じ不整合をfail-closedにするための変更である。

## Regression fixture

`tests/test_research_host_package_materializer.py` では、complete checkout上で次を検査する予定である。

### OpenAI

ja-JP / en-US × interactive / meteredについて、

- 三Skill treeがある。
- 各Skillに `agents/openai.yaml` がある。
- profileに対応するimplicit invocation policyである。
- Claude/Codex manifestを混入しない。

### Claude

ja-JP / en-USについて、

- 三Skill treeがある。
- `.claude-plugin/plugin.json` がある。
- plugin identityとversionを保持する。
- Skill entryはexplicit invocationである。
- marketplace / Codex manifest / READMEを作らない。

### Codex

ja-JP / en-USについて、

- 三Skill treeがある。
- `.codex-plugin/plugin.json` がある。
- `skills = ./skills/` とinterface metadataを持つ。
- Claude manifest / root marketplace / READMEを作らない。

## 検証状態

現時点では、source code、metadata declaration、production manifest shapeとの静的照合まで行った。

しかしcomplete checkoutをこの実行環境で確保できず、接続済み開発端末もofflineだったため、次はまだ主張しない。

- `tests/test_research_host_package_materializer.py` の実行成功
- `tests/test_research_skill_tree_materializer.py` の実行成功
- `make research-skill-check` の成功
- `make check` の成功
- 実host package treeの生成成功

GitHub Actionsも無効である。

したがって、research host package materializerは**実装済みのpre-production probe候補**であり、実行証拠待ちである。

## Promotion boundary

production builder generalizationへ進む前に、少なくとも次を満たす必要がある。

1. complete checkoutでSkill-tree materializer testsが通る。
2. complete checkoutでhost-package materializer testsが通る。
3. `make research-skill-check` が通る。
4. materialized ja-JP / en-US packageを現行production generated packageと構造比較する。
5. 差分が、意図した三Skill splitとprototype metadataに説明できる。
6. host routing / wordingについて、prototypeからproductionへ昇格させるだけの追加証拠を得る。

それまでは `scripts/build.py` をmulti-Skill production builderへ置き換えない。

## 結論

三Skill × 二localeについて、Skill treeだけでなく**package-local host metadataまでをrepository外の一時領域で組み立てる研究境界**を追加した。

これにより、Method分離からproduction releaseへ一気に飛ばず、

```text
semantic contract
→ runtime
→ package source
→ Skill tree
→ host package shape
→ production distribution
```

という中間証拠を一段ずつ確認できる。
