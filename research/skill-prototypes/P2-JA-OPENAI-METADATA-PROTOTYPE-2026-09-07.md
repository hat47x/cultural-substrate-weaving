# Research Skill Suite — ja-JP Companion OpenAI Metadata Prototype Review 2026-09-07

Status: research metadata prototype; not production adapter approval

## Purpose

`adapter-metadata-plan.json` では、ja-JPのAffinity / Iterative runtimeは存在する一方、OpenAI用 `agents/openai.yaml` 相当metadataを未設計として `planned` に残していた。

P2の次段階として、二つのcompanion Skillについてinteractive / metered双方のmetadata prototypeを作る。

ここでの目的は「OpenAI向け文面を完成させる」ことではない。

次を先に確認する。

1. Skillの役割境界がdefault promptでも保たれるか。
2. CSWの文化体系探索をcompanionへ誤って持ち込まないか。
3. Affinityがmulti-round orchestrator化しないか。
4. IterativeがLayer 1のgrouping / labelingを自前実装するpromptにならないか。
5. interactive / metered差がinvocation policy以外へ不要に広がらないか。

## Prototype location

production `adapters/` は変更しない。

research-only sourceとして次へ置く。

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

`prototype` は、

- source fileが存在する。
- validatorを通す対象である。
- production adapterとして採用済みではない。
- wording reviewやhost実挙動確認が残る。

という状態である。

## Affinity Synthesis metadata

### Display

```text
親和統合 — 日本語
```

### Short description

```text
異種の材料を先に分類せず、一回の統合として意味単位・束・関係・残差を立ち上げる
```

### Default prompt

```text
元材料の来歴と認識状態を保ち、先に分類体系を置かず、一回の親和統合として意味単位・束・関係・残差を立ち上げてください。
```

### Boundary review

このpromptは、

- 一回の統合であることを明示する。
- 材料より先にtaxonomyを置かない。
- provenance / epistemic statusを保持する。
- card/group/relation/residual相当の外部成果物へ向かう。

一方、次を要求しない。

- 次roundの問いを決める。
- 再収集を開始する。
- 文化体系を適用する。
- framework-generated candidateを作る。
- domain decisionを行う。

したがってLayer 1の範囲に留まっている。

## Iterative Inquiry Synthesis metadata

### Display

```text
反復探索統合 — 日本語
```

### Short description

```text
新材料が触れた箇所だけを再開し、統合結果・残差・問いをラウンド間で追跡する
```

### Default prompt

```text
前ラウンドを上書きせず、新材料が触れた箇所だけを再開し、必要な一回統合は利用可能な互換realizationへ委ね、残差・次の問い・停止理由を追跡してください。
```

### Boundary review

このpromptは、

- 前roundを上書きしない。
- touched regionだけをreopenする。
- 一回統合を互換realizationへ委ねる。
- residual / next inquiry / stop reasonを追跡する。

一方、次を要求しない。

- 自分でcard groupingを行う。
- 自分でlabeling algorithmを再実装する。
- 文化体系を適用する。
- gapを必ず埋める。
- 固定round数を完了条件にする。

したがってLayer 2 orchestratorの範囲に留まっている。

## Comparison with current CSW OpenAI metadata

現行CSWのdefault promptは、

```text
領域固有手法の基準線を置き、文化的体系とKJ法による増分だけを対象側で検証してください。
```

である。

これはCSWの役割に合っている。

しかし同じpromptをcompanionへ流用すると、

- Affinityへ文化体系探索を持ち込む。
- IterativeへCSW固有のframework-generated increment検証を持ち込む。
- 三Skill分離後も旧単一Skillの責務を各Skillへ複製する。

ことになる。

今回のprototypeでは、CSWのdefault promptを基礎templateとしてコピーしていない。

各SkillのMethod / roleから必要最小限の入口だけを作った。

## Interactive vs metered

二profileでinterface文面は同一とする。

差は、

```text
interactive: allow_implicit_invocation = true
metered:     allow_implicit_invocation = false
```

だけである。

これは現行CSW adapterのprofile差と同じ構造である。

現段階では「meteredだから短いpromptにする」「interactiveだから手順を増やす」等の二重Method化を行わない。

profile policyと方法論を混同しないためである。

## Validator / planner change

OpenAI metadata statusを、

```text
planned | prototype | existing
```

の三状態へ広げる。

### `planned`

sourceなし。

### `prototype`

research sourceあり。existingと同じ構文・marker・profile policy検査を受けるが、production採用済みとは扱わない。

### `existing`

現行production adapter source。

coverage plannerでは、ja-JP OpenAIを、

```text
runtime_state      = buildable
metadata_coverage  = prototype-for-realized
```

とする。

内訳:

```text
CSW       = existing
Affinity  = prototype
Iterative = prototype
```

これにより「metadata sourceが全Skill分存在する」と「production adapterが全Skill分完成している」を区別できる。

## What this review does not prove

このreviewはsame-authoring-sessionでの設計確認であり、独立したhost evaluationではない。

まだ確認していないもの:

- OpenAI Skill UI上でのdisplay/descriptionの実際の見え方。
- implicit invocationが各Skillの責務境界に沿って働くか。
- default promptが自然利用で過剰起動・過小起動を起こさないか。
- Metered profileで期待する利用境界になるか。
- 英語companion metadata parity。

したがって `prototype` のままとする。

## Next evidence

次に価値があるのは、metadata文面を増やすことではなく、同じ短いタスク群に対して、

- CSW
- Affinity
- Iterative

のどれを入口として選ぶべきかをpairedで点検することである。

特に、

1. 一回だけ異種資料を束ねるタスク。
2. 前roundへ新資料を追加するタスク。
3. 文化体系から通常分析にない問いを供給するタスク。
4. 2と3が連携するが、帰属を混ぜてはいけないタスク。

を使えば、metadataがSkill routingの境界を弱めていないか確認できる。

## Decision

ja-JP companion OpenAI metadataは `planned` から `prototype` へ進められる。

ただしproduction `adapters/openai-skill/` へ移さず、P2 research treeに保持する。

production builder generalization、generated artifact更新、release asset変更はまだ行わない。

complete checkoutでの実 `make check` release gateも未通過のままである。
