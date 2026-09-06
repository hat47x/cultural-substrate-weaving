# Research Skill Suite — P2 Package Source Descriptor Audit 2026-09-07

Status: research packaging contract; production build remains unchanged

## Purpose

P2 distribution layout plannerは、各localeでSkill realizationが存在するかまでは判定できるようになった。

しかし `runtime_entry` が一つ存在するだけでは、実際のpackageを組み立てるための入力として不十分である。

たとえば `affinity-synthesis/SKILL.md` はprogressive referenceとして次を案内する。

- Method Definition
- Representation Grammar
- output template
- machine-readable schema
- evaluation / counterexample cases
- evidence dossier

`SKILL.md`だけをstandalone artifactへコピーすると、それらの相対参照がpackage内で失われる。

一方、現行Cultural Substrate Weavingは別の構造を持つ。`src/manifest.json` がrouter、locale、modules、skill reference名、knowledge groupsを既に所有しており、production `scripts/build.py` はこのmanifestを正本として各配布面を生成している。

この二種類を無理に一つのflat file listへ変換せず、locale realizationごとにpackage sourceの読み方を宣言する。

## Package source modes

### `explicit_files`

prototype companion Skillのように、runtime entryと少数のprogressive referenceをsource treeからそのまま相対構造を保って同梱できる場合に使う。

```json
{
  "mode": "explicit_files",
  "root": "research/skill-prototypes/iterative-inquiry-synthesis",
  "files": [
    "SKILL.md",
    "references/METHOD.md",
    "references/ROUND-TEMPLATE.md"
  ]
}
```

`files` は `root` 相対である。

validatorは次を要求する。

- rootがskill `source_root` 内にある。
- filesがrootからescapeしない。
- filesが実在する。
- 重複がない。
- locale realizationのruntime entryがfilesへ含まれる。

このmodeは「列挙したfileだけが方法上重要」という意味ではない。packageを組み立てる際のsource boundaryを表す。

### `canonical_manifest`

現行CSWのように、既存のcanonical source manifestがruntime/module集合を所有している場合に使う。

```json
{
  "mode": "canonical_manifest",
  "manifest": "src/manifest.json",
  "locale_root": "src/ja-JP"
}
```

validatorは少なくとも次を確認する。

- manifest / locale rootがskill source root内にある。
- manifestが対象localeを宣言する。
- manifest routerとlocale realization runtime entryが一致する。
- manifestのmodule sourceがlocale root内に実在する。

既存production source contractをresearch suite用に複製せず、参照して利用する。

## Current descriptors

### Affinity Synthesis / ja-JP

package source:

```text
SKILL.md
references/METHOD.md
references/REPRESENTATION.md
references/TEMPLATE.md
references/affinity-map.schema.json
evals/CASES.md
evidence/dossier.md
```

ここでは、Skill本文からprogressive referenceとして到達するruntime-facing materialを保持する。

全research eval、全example、authoring scriptをpackageへ入れるという意味ではない。

### Iterative Inquiry Synthesis / ja-JP

package source:

```text
SKILL.md
references/METHOD.md
references/ROUND-TEMPLATE.md
```

Layer 1はhard dependencyではないため、Affinity tree全体をIterative standaloneへ埋め込まない。

今回の監査で、Iterative `SKILL.md` のProgressive Referencesが

```text
sibling prototype ../affinity-synthesis/
```

というfilesystem配置を前提にしていることを発見した。

これはOpenAI等のstandalone-per-skill targetと、`hard_dependency: false` の方法境界に合わない。

そこで表現を、

> 利用可能な場合はcompanion Skill `affinity-synthesis` のMethod Definition / representation contractを参照する。sibling filesystem pathの存在は前提にしない。

へ変更した。

方法上の依存関係は変えていない。package topologyだけを方法契約へ漏らさない修正である。

### Cultural Substrate Weaving / ja-JP and en-US

両localeとも `canonical_manifest` を使う。

```text
manifest: src/manifest.json
locale_root: src/<locale>
```

CSWをcompanion prototypeと同じexplicit file listへ写し直さない。現行 `src/manifest.json` を唯一のmodule集合正本として維持する。

## Research metadata vs package source

suite manifestには既に次のresearch metadataがある。

- `references`
- `evidence`
- `evals`

これらと `package_source` は別の問いに答える。

### Research metadata

> どのMethod Definition、evidence、evaluation recordが、このresearch candidateの監査・根拠・履歴を構成するか。

### Package source

> このlocale realizationを一つのruntime package inputとして扱う場合、どのsource boundaryから何を取得するか。

したがって全evalをpackage sourceへ入れる必要はなく、逆にruntime-facing schemaがresearch `references` の分類方法だけから自動的に同梱されるとも限らない。

今回、Affinity `references` metadataにも `REPRESENTATION.md` と `affinity-map.schema.json` を登録し、存在するreference artifactを明示した。

## Planner consequence

`plan_suite_layout.py` の `realized` は今後、少なくとも次を同時に要求する。

1. statusがplannedではない。
2. runtime entryが宣言される。
3. package source descriptorが宣言される。

したがってruntime entryだけを追加してpackage inputが定義されていないSkillを、layout上buildableとは数えない。

planner outputにもpackage sourceを残す。後続のresearch builderは、このplanからsource modeを選べる。

ただしplannerの `buildable` は依然として以下を意味しない。

- packageが実生成済み。
- generated link check済み。
- host routingが確認済み。
- English method parityがある。
- release asset contractを満たす。

## Why production build is still unchanged

この段階では `scripts/build.py` をmulti-skill化しない。

まず必要なのは、production関数へ渡せるsource descriptorが安定しているかを見ることである。

次に安全に進められる研究段階は、repositoryを書き換えないpure planner/rendererで、descriptorから**予定package tree**を計算することである。

例:

```text
OpenAI ja-JP
  affinity-synthesis/
    SKILL.md
    references/...
    evals/CASES.md
    evidence/dossier.md

  iterative-inquiry-synthesis/
    SKILL.md
    references/...
```

CSWについては既存buildのtarget namingをそのまま参照し、research builderが別の正本を作らない。

## Decision

**P2 now has an explicit source boundary between “a realization exists” and “the files needed to construct its runtime package are known.”**

次はdescriptorからpackage tree planを生成し、relative reference preservationとtarget collisionを静的に確認する。

その結果が安定するまで、canonical `src/` のKJ分離、production `build.py` のmulti-skill化、公開asset変更には進まない。
