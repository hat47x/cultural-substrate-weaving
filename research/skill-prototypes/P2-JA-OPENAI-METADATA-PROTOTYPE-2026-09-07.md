# Research Skill Suite — ja-JP Companion OpenAI Metadata Prototype Review 2026-09-07

Status: research metadata prototype; not production adapter approval

## Purpose

`adapter-metadata-plan.json` では、ja-JPのAffinity / Iterative runtimeは存在する一方、OpenAI用metadataをproduction未採用として分離管理する。

P2の次段階として、二つのcompanion Skillについてinteractive / metered双方のmetadata prototypeを作り、次を確認する。

1. Skillの役割境界がdefault promptでも保たれるか。
2. CSWの文化体系探索をcompanionへ誤って持ち込まないか。
3. Affinityがmulti-round orchestrator化しないか。
4. IterativeがLayer 1のgrouping / labelingを自前実装するpromptにならないか。
5. interactive / metered差がinvocation policy以外へ不要に広がらないか。

## Prototype location

production `adapters/` は変更しない。

```text
research/skill-prototypes/adapters/openai-skill/ja-JP/
  affinity-synthesis/
    openai.interactive.yaml
    openai.metered.yaml
  iterative-inquiry-synthesis/
    openai.interactive.yaml
    openai.metered.yaml
```

`adapter-metadata-plan.json` ではこれらを `prototype` として参照する。

`prototype` は、source fileが存在しvalidator対象である一方、production adapterとして採用済みではなく、wording reviewやhost実挙動確認が残る状態である。

## Affinity Synthesis metadata

Display:

```text
親和統合 — 日本語
```

Short description:

```text
異種の材料を先に分類せず、一回の統合として意味単位・束・関係・残差を立ち上げる
```

Default prompt:

```text
元材料の来歴と認識状態を保ち、先に分類体系を置かず、一回の親和統合として意味単位・束・関係・残差を立ち上げてください。
```

このpromptは一回の統合、material-led boundary、provenance / epistemic status、residual外部化を要求する。一方、次roundの問い、再収集、文化体系適用、framework-generated candidate、domain decisionは要求しない。

したがってLayer 1の範囲に留まる。

## Iterative Inquiry Synthesis metadata

Display:

```text
反復探索統合 — 日本語
```

Short description:

```text
新材料が触れた箇所だけを再開し、統合結果・残差・問いをラウンド間で追跡する
```

Default prompt:

```text
前ラウンドを上書きせず、新材料が触れた箇所だけを再開し、必要な一回統合は利用可能な互換realizationへ委ね、残差・次の問い・停止理由を追跡してください。
```

このpromptは前round非破壊、touched region reopen、一回統合の委任、residual / next inquiry / stop reason追跡を要求する。一方、自前のcard grouping / labeling、文化体系適用、gap強制充足、固定round数は要求しない。

したがってLayer 2 orchestratorの範囲に留まる。

## Comparison with current CSW OpenAI metadata

現行CSWのdefault promptは、領域固有手法、文化的体系、KJ法由来増分の対象側検証を含む。これをcompanionへコピーすると旧単一Skill責務が再複製される。

今回のprototypeでは既存CSW promptをtemplateとして流用せず、各SkillのMethod / roleから必要最小限の入口だけを作った。

## Interactive vs metered

二profileでinterface文面は同一とする。

```text
interactive: allow_implicit_invocation = true
metered:     allow_implicit_invocation = false
```

profile policyと方法論を混同しないため、metered用にMethodを短縮したりinteractive用に手順を追加したりしない。

## State model

OpenAI metadata statusは次の三状態とする。

```text
planned | prototype | existing
```

- `planned`: sourceなし。
- `prototype`: research sourceあり。構文・marker・profile policy検査対象だがproduction未採用。
- `existing`: production adapter source。

ja-JP OpenAI coverageは現在、

```text
runtime_state     = buildable
metadata_coverage = prototype-for-realized
```

内訳は、

```text
CSW       = existing
Affinity  = prototype
Iterative = prototype
```

である。

## What this review does not prove

このreviewはsame-authoring-sessionであり独立host evaluationではない。

未確認:

- OpenAI Skill UI上の実表示。
- implicit invocationのrouting精度。
- default promptの自然利用時の過剰起動・過小起動。
- Metered profileの実利用境界。
- en-US companion metadata parity。

したがってstatusは `prototype` のままとする。

## Decision

ja-JP companion OpenAI metadataはresearch `prototype` として保持する。production `adapters/openai-skill/`、production builder、generated artifact、release assetはまだ変更しない。
