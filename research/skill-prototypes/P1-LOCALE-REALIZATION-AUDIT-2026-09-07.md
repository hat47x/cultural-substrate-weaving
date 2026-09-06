# Research Skill Suite — P1 Locale Realization Audit 2026-09-07

Status: research packaging contract; production build is unchanged

## Purpose

P1のsuite manifestをP2 build/validator generalizationへ渡す前に、**suite-level locale readiness** と **skillごとの具体的なlocale realization availability** を分ける。

これまでの `suite-manifest.json` は、suite全体について次だけを表していた。

```text
ja-JP: canonical
en-US: planned
```

一方、実際のrepository stateはskillごとに異なる。

- `cultural-substrate-weaving` は現在のcanonical runtimeとしてja-JP / en-USの両方を持つ。
- `affinity-synthesis` research prototypeは、現在の一つのprototype realizationだけを持つ。英語realizationはまだない。
- `iterative-inquiry-synthesis` も同様に、現在のprototype realizationだけを持つ。英語realizationはまだない。

suite-level `en-US: planned` だけでは、CSW英語runtimeまで存在しないようにも、逆に三Skillすべて英語で生成可能なようにも読める。

P2のdistribution plannerがこの曖昧さを引き継ぐと、**target package compositionとcurrent buildabilityを混同する**。

## Contract added

各skillに `locale_realizations` を持たせる。

### affinity-synthesis

```text
ja-JP: prototype -> research/skill-prototypes/affinity-synthesis/SKILL.md
en-US: planned
```

### iterative-inquiry-synthesis

```text
ja-JP: prototype -> research/skill-prototypes/iterative-inquiry-synthesis/SKILL.md
en-US: planned
```

### cultural-substrate-weaving

```text
ja-JP: existing -> src/ja-JP/ROUTER.md
en-US: existing -> src/en-US/ROUTER.md
```

ここで `prototype` / `existing` は現在状態を説明する語であり、validatorは閉じたstatus enumを所有しない。

特別な意味を持つのは `planned` だけである。

- `planned`: realization artifactがまだ無くてもよい。
- `planned` 以外: `runtime_entry` の実体が必要。
- suiteのcanonical localeは `planned` だけにはできない。

## Suite locale vs skill realization

二つの軸は別の問いに答える。

### Suite-level locale status

> このlocaleで、suite全体を公開・比較・promotion対象として扱える段階か。

現在:

- ja-JP: canonical research line
- en-US: planned until companion skills receive reviewed English realizations

### Per-skill locale realization

> このskillについて、このlocaleで参照できる具体的runtime realization artifactが現在存在するか。

したがって、suiteの `en-US: planned` とCSW skillの `en-US: existing` は矛盾しない。

CSW英語runtimeは既に存在するが、companion skillsの英語realizationがないため、三Skill suiteとしてはまだplannedである。

## Distribution interpretation

`distribution_prototypes.*.contains` は**目標package composition**を表す。

たとえばClaude/Codexでは今後、locale bundleに次の三Skillを同梱する設計である。

```text
cultural-substrate-weaving
affinity-synthesis
iterative-inquiry-synthesis
```

しかし `contains` に三つ書かれていること自体は、そのlocaleで今すぐ三つを生成できる証拠ではない。

P2 plannerは、各 `contains` skillの `locale_realizations[locale]` を見てbuildabilityを判定する必要がある。

### Current consequence

- ja-JP research bundle: 三Skillすべてにrealizationがあるため、**layout prototypeを計画できる**。これはproduction package readinessを意味しない。
- en-US research bundle: affinity / iterative がplannedのため、**三Skill bundle generationはblocked/plannedとして扱う**。
- en-US CSW standalone/composite: 現行CSW runtimeが存在するという事実は保持する。

## Validator boundary

`validate_research_skill_suite.py` は次を検査する。

- 各skillの `locale_realizations` がsuiteのlocale集合と一致する。
- canonical localeはplanned-onlyではない。
- planned以外のrealizationには実在する `runtime_entry` がある。
- runtime entryはskill `source_root` の外へ出ない。
- canonical locale realizationのruntime entryは従来のskill-level `runtime_entry` と一致する。

validatorが判定しないもの:

- translation quality。
- method parity。
- independent evaluation readiness。
- public release readiness。
- hostがsibling skillをroutingできるか。

## Backward-compatible role of skill-level runtime_entry

schema v1ではskill-level `runtime_entry` を残す。

これはcanonical locale realizationのentryとして扱い、`locale_realizations[canonical_locale].runtime_entry` と一致させる。

P2/P3でsuite manifest schemaを更新する場合に、skill-level fieldを廃止または別構造へ移すか再検討できる。P1でproduction readerを先回りして壊さない。

## P2 handoff

次にproduction `scripts/build.py` を直接multi-skill化しない。

まずresearch-only plannerで次を計算可能にする。

1. localeごとのrealized / planned skill集合。
2. OpenAI standalone-per-skillの生成可能候補。
3. Claude/Codex locale bundleについて、target `contains` がすべてrealizedか。
4. composite GPT/Copilotについてprimary CSW realizationがあるか。
5. blocked packageについて、どのskill/locale realizationが不足しているか。

plannerがrepositoryを書き換えたりpackageを生成したりする必要はない。最初は**layout/buildability planを外部化するだけ**でよい。

この段階を経てから、現行単一Skill `build.py` のどの関数をsuite-awareへ一般化するかを決める。

## Decision

**P1 manifest now has enough locale-specific information to design a research-only distribution planner. Production build remains unchanged.**

この変更はEnglish parityを満たした証拠ではなく、むしろ現時点で不足している英語companion realizationsを機械的に区別できるようにするものである。
