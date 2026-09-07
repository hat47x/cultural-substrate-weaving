# P4 Release Internal Composition Plan — 2026-09-07

Status: design-only; production package/release scripts remain unchanged

## 目的

三Skill promotion後もrelease ZIPの種類を不用意に増やさず、既存distribution packageの内部構成だけを厳密にするための将来contractを定める。

```text
same package kind
  != same internal Skill count
  != same old monolithic description
```

この文書は現行release artifactへ適用しない。production builder generalization後に `scripts/validate_release.py` へ移す候補contractである。

## OpenAI Skill package

既存package kindを維持する。

```text
openai-interactive
openai-metered
```

各locale / profile ZIPのrootには、三つのstandalone Skill directoryが必要になる。

production候補名を使う場合の期待構成:

```text
cultural-substrate-weaving/
  SKILL.md
  references/...
  agents/openai.yaml

material-led-synthesis/
  SKILL.md
  references/...
  agents/openai.yaml

iterative-inquiry-synthesis/
  SKILL.md
  references/...
  agents/openai.yaml
```

### 必須条件

- directory名と各 `SKILL.md` の `name:` が一致する。
- interactiveでは3 Skillすべてのmetadataが `allow_implicit_invocation: true`。
- meteredでは3 Skillすべてが `allow_implicit_invocation: false`。
- Layer 1のpackage-local referencesがclosureしている。
- Layer 2のpackage-local referencesがclosureしている。
- CSWはthin ownershipを維持し、Layer 1/2を自分で実行済みと称しない。

### 禁止

- research pathへの参照。
- `affinity-synthesis` research IDが、production name確定後もinstallable directoryとして残ること。
- sibling SkillをCSW references配下へ埋め込み、一Skill packageに見せること。

## Claude plugin package

既存locale plugin identityを維持する。

```text
cultural-substrate-weaving-ja
cultural-substrate-weaving-en
```

期待Skill tree:

```text
plugins/<plugin_name>/
  .claude-plugin/plugin.json
  skills/
    weave/
      SKILL.md
      references/...
    material-led-synthesis/
      SKILL.md
      references/...
    iterative-inquiry-synthesis/
      SKILL.md
      references/...
```

三つの `SKILL.md` は、現行明示呼び出しpolicyを維持する場合、

```text
disable-model-invocation: true
```

を一度だけ持つ。

plugin manifestの `name` / `version` / `author` / `homepage` / `repository` / `license` は現行identityを維持し、`description` はsplit-aware bundle wordingへ置換する。

## Codex

新しいrelease ZIP kindは作らない。

CodexはClaudeと同じlocale plugin directoryの `skills/` を参照し、

```text
.codex-plugin/plugin.json
```

を追加する現行構造を維持する。

したがってCodex側で検査すべき主な点は、

- `skills = ./skills/`
- 同じ三Skill subtreeが存在する
- plugin identity / display identityを維持する
- split-aware descriptionを使う

ことである。

## ChatGPT GPT / Microsoft Copilot

第一波のinternal three-Skill composition検査には含めない。

両者はcomposite realizationであり、standalone Skill subtreeをpackage内部へ並べる契約ではない。

Microsoft Copilotは現在の限定embedded material-synthesis fallbackを維持する。三Skill promotionを理由にfull Layer 1/2をコピーしない。

## Release validatorへ将来追加する検査

production promotion後の `scripts/validate_release.py` では、既存のZIP安全性・再現性検査に加えて、少なくとも次を確認する。

### OpenAI ZIP

```text
expected top-level Skill dirs
  = {
      cultural-substrate-weaving,
      material-led-synthesis,
      iterative-inquiry-synthesis
    }
```

各directoryに `SKILL.md` と `agents/openai.yaml` が存在する。

### Claude ZIP

locale plugin directory配下の `skills/` に、

```text
{
  weave,
  material-led-synthesis,
  iterative-inquiry-synthesis
}
```

が過不足なく存在する。

### Codex manifest

Claude package sourceと同じplugin tree内の `.codex-plugin/plugin.json` が `skills: ./skills/` を宣言し、そのtreeが上記三Skillを持つ。

## package filename

第一波では既存release package filenameを維持する。

```text
cultural-substrate-weaving-openai-interactive-<locale>-v<version>.zip
cultural-substrate-weaving-openai-metered-<locale>-v<version>.zip
cultural-substrate-weaving-claude-plugin-<locale>-v<version>.zip
```

`cultural-substrate-weaving` はこの場合、単一Skill名ではなくsuite / distribution familyの既存publication identityとして扱う。

これが利用者に誤解を生むかは、production promotion前のREADME / marketplace reviewで確認する。

## Research-side evidence

現在のresearch host-package materializerは、production名ではなくstable research IDをtarget名として使用している。

これは意図的である。

```text
research validation of method/package mechanics
  precedes
public-name projection
```

production candidate `material-led-synthesis` へのprojectionは、P4 production descriptorでのみ表し、complete-checkout research gate前にresearch fixturesを大量renameしない。

## Promotion sequence

```text
research Skill tree / host package tests PASS
        ↓
public name final check
        ↓
production canonical source promotion
        ↓
production target projection uses material-led-synthesis
        ↓
production build emits three-Skill distribution packages
        ↓
release validator checks internal composition
```

## 現時点の判断

- package kindは増やさない。
- OpenAIは一つのprofile ZIP内に三standalone Skillを置く。
- Claude/Codexは既存locale plugin identityの中に三Skill subtreeを置く。
- public Layer 1 nameはproduction promotion時にのみprojectionする。
- GPT/M365 compositeは第一波のtree compositionから外す。
- production release validationへ移すのは、complete-checkout P3 gate通過後とする。
