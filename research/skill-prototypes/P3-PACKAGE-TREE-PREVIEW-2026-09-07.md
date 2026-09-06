# Research Skill Suite — P3 Package Tree Preview 2026-09-07

Status: research package-tree experiment; production build remains unchanged

## Purpose

P2でlocale realizationごとの `package_source` が定義されたため、P3ではそのdescriptorを**実際の予定package treeへ投影できるか**を検査する。

この段階でproduction `scripts/build.py` をmulti-skill化しない。

P3が確かめるのは、次の境界である。

```text
Method / runtime source
    -> package_source descriptor
    -> layout plan
    -> research-only package tree preview
    -> link / topology validation

!= production release artifact
!= host routing validation
!= public promotion
```

## Why no additional build-descriptor layer

当初、`package_source` とproduction builderの間に別のnormalized build descriptorを置く案も試した。

しかし並行研究で導入された `package_source` はすでに、packageを構成するsource boundaryを十分具体的に表していた。

- `explicit_files`: rootと相対file集合を持つ。
- `canonical_manifest`: canonical manifestとlocale rootを持つ。
- `plan_suite_layout.py`: realization availabilityとpackage sourceを同じplanへ残す。

この上に同じ情報を再包装する独自descriptorを置くと、二つのschemaを同期する必要が生じる。

そのため追加descriptor layerは採用せず、research previewを `plan_suite_layout.py` の最初のconsumerとする。

これは「一度作った実装を残す」より、責務が重なるなら削除する方を優先した判断である。

## Preview consumer

`research/skill-prototypes/build_preview.py` は次の順で動く。

1. `suite-manifest.json` を読む。
2. `plan_suite_layout.py` でlocale / skill realizationを計画する。
3. `realized == false` のinputはpreview生成しない。
4. 各realizationの `package_source.mode` で投影方法を選ぶ。
5. 一時directoryまたは明示outputへpackage treeを構築する。
6. frontmatter、Method Definition、declared source、相対linkを検査する。
7. `ORIGIN.json` にresearch-only provenanceを残す。

previewは三Skill×二locale、計6 packageを対象にする。

## `explicit_files` projection

`affinity-synthesis` と `iterative-inquiry-synthesis` に使う。

source descriptor例:

```json
{
  "mode": "explicit_files",
  "root": "research/skill-prototypes/affinity-synthesis",
  "files": [
    "SKILL.md",
    "references/METHOD.md",
    "references/REPRESENTATION.md"
  ]
}
```

### Relative structure preservation

runtime以外のfileは、`root` からの相対pathをpackage内でも維持する。

```text
source                                   preview
references/METHOD.md                  -> references/METHOD.md
evals/CASES.md                        -> evals/CASES.md
evidence/dossier.md                   -> evidence/dossier.md
```

これにより、Skill本文のprogressive referenceをflatteningで壊さない。

### Runtime canonical name

locale source上では英語runtimeが `SKILL.en.md` でも、installable packageのentryは `SKILL.md` とする。

```text
SKILL.en.md -> SKILL.md
```

これはsource identityを書き換えるのではなく、配布面のcanonical entry nameへのprojectionである。元sourceは `ORIGIN.json` に残す。

## `canonical_manifest` projection

CSWは既存 `src/manifest.json` を再利用する。

preview builderは別のmodule listを持たない。

- manifestのrouterを読む。
- manifestのmodulesを読む。
- locale rootからmoduleを取得する。
- current production OpenAI/Claude shapeと同様に、routerのmodule linkをpackage `references/` へ書き換える。

これによりresearch suiteのためだけにCSW source正本を複製しない。

## Locale boundary

英語realizationが存在することと、英語の全research materialが翻訳済みであることは別である。

### Affinity Synthesis en-US

package sourceは現在次に限定する。

```text
SKILL.en.md
references/METHOD.en.md
references/REPRESENTATION.md
references/affinity-map.schema.json
```

日本語Method、template、lineage noteを自動同梱しない。

`REPRESENTATION.md` は共有technical assetであり、日本語説明を英語runtimeの追加instructionとして扱わない。

### Iterative Inquiry Synthesis en-US

```text
SKILL.en.md
references/METHOD.en.md
references/ROUND-TEMPLATE.md
```

`ROUND-TEMPLATE.md` は英語Skill本文で日本語research templateであることを明示している。英語runtimeのMethod Definitionを置き換えない。

## Validation boundary

P3 preview checkは少なくとも次を確認する。

- 6 packageが構築対象になる。
- installable packageに `SKILL.md` がある。
- frontmatter `name` がinstallable nameと一致する。
- `ORIGIN.json` の `research_only` がtrueである。
- explicit sourceとして宣言したfileが期待pathへ存在する。
- locale Method Definitionがpackage内に存在する。
- package内Markdownのrelative linkが解決する。

formal suite validator側では、生成前に次を止める。

- package root escape。
- missing source file。
- runtime entryがexplicit sourceから抜ける。
- locale Method Definitionがpackage sourceから抜ける。
- canonical manifestのrouterとruntime entryが食い違う。
- canonical manifestのmodule sourceが欠ける。
- research metadataとして追跡されていないfileをexplicit packageへ混ぜる。

## What this does not prove

previewが通っても次は未証明である。

- OpenAI / Claude / Codexが三Skillを期待どおりroutingする。
- ChatGPT GPT compositeへLayer 1/2が正しく内包される。
- Microsoft Copilotでfull sibling method parityがある。
- English translation / method parityが独立査読済みである。
- token / byte budgetがproduction targetで成立する。
- release package contractを満たす。

## Promotion consequence

P3の結果が安定し、実行環境でresearch gateを通せた後に初めて、production build一般化の候補を検討する。

その際も、いきなり全surfaceをmulti-skill化しない。

候補順序は次のように分けられる。

1. standalone-per-skill出力を持つsurface。
2. multi-skill filesystemを自然に持てるClaude/Codex bundle。
3. sibling invocationを前提にできないcomposite agent surface。

各surfaceでsource topologyとhost capabilityは別に検証する。

## Decision

**P3では、新しいdescriptor schemaを増やさず、P2 `package_source` をresearch package treeへ直接投影する。**

`build_preview.py` をその最初のconsumerとして使い、relative structure、locale boundary、Method Definition、link topologyをrelease buildから隔離したまま検査する。

次のgateは、実行環境でこのpreviewを含む `make research-skill-check` を実行し、静的設計ではなく実際のpackage treeで不整合を潰すことである。
