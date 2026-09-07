# Production Skill-set projection — 2026-09-07

## 目的

research 上で Skill realization が存在することと、production 配布物へ含めることを分離した状態から、production 側が必要とする最小の Skill 集合だけを表現する。

この段階では companion Skill を production へ昇格しない。`affinity-synthesis` と `iterative-inquiry-synthesis` は、他レーンで名称・責務境界・handoff・評価を継続検討している research candidate のままとする。

## 他レーンとの協調境界

現在の他レーンでは、次の判断を維持している。

- KJ 系の一回統合と複数ラウンドの探索継続を CSW から分離する方向は有力である。
- `affinity-synthesis` / `iterative-inquiry-synthesis` は現時点の working name であり、公開最終名とはみなさない。
- CSW → Iterative → Affinity の handoff では、`framework_generated` 等の provenance と epistemic status を target-side support へ無言で昇格させない。
- 現行 canonical `src/ja-JP/methods/integration.md` と `src/ja-JP/core/iteration.md` は、handoff と paired evaluation が十分になるまで縮小しない。
- ja-JP companion prototype が package 可能でも、それだけでは production 昇格条件を満たさない。
- en-US companion realization は planned / blocked のままであり、production parity を主張しない。

このレーンは上記判断を上書きしない。production 側には、他レーンで昇格判断が確定した Skill だけを受け入れる薄い境界を用意する。

## Production descriptor が所有するもの

`src/skill-set.json` は次の二つだけを所有する。

1. production に含める Skill の identity
2. その Skill の production source manifest への参照

現在は次だけである。

```json
{
  "schema": "csw.production-skill-set/v1",
  "skills": [
    {
      "id": "cultural-substrate-weaving",
      "source_manifest": "src/manifest.json"
    }
  ]
}
```

## Production descriptor が所有しないもの

次は既存の正本・adapter・host metadata に残し、`src/skill-set.json`へ複製しない。

- locale 一覧
- canonical locale
- router path
- module / reference 一覧
- Skill description
- OpenAI display / prompt / invocation policy
- Claude / Codex plugin name, display, description
- host 別 target Skill name
- research maturity (`prototype`, `candidate`, `blocked` 等)
- promotion gate の評価結果
- handoff contract の内容

これらを descriptor に再掲すると、既存の `src/manifest.json`、adapter metadata、research suite との間に複数正本が生じるためである。

## 二つの検証面

### 1. Production 単独検証

`scripts/validate_production_skill_set.py` は research tree を読まない。

検査するのは次だけである。

- schema
- Skill 集合が空でないこと
- Skill id の一意性
- descriptor entry が `id` と `source_manifest` 以外を所有しないこと
- `source_manifest` が repository 内の `src/` 配下を指すこと
- manifest の `name` が Skill id と一致すること
- manifest が locale と canonical locale を持つこと

これにより production release は research tree がなくても自分の公開境界を説明できる。

### 2. Research → production 射影検証

`research/skill-prototypes/scripts/validate_production_projection.py` は、research inclusion plan と production Skill-set を比較する。

- `production_state = included` の Skill だけが production descriptor に現れる。
- `candidate` / `blocked` は production に漏れない。
- research inclusion decision が指した manifest と production source manifest が一致する。

したがって、

```text
research realization exists
        !=
research production_state = included
        !=
production Skill-set member
```

という三段階を保つ。

## Build との接続はまだ行わない

本段階では `scripts/build.py` は `src/skill-set.json` を読まない。

理由は、production builder の generic writer / validator の refactor と、production inclusion decision の検証が別 PR としてまだ並行しているためである。descriptor を追加しただけで build output を変えると、mechanical refactor と公開集合変更の原因を分離できなくなる。

まず production descriptor 自身を `make check` の契約へ入れる。その後、generic writer / validator が統合された段階で、現在の CSW 一つだけを descriptor 経由で解決しても生成物が byte 不変になることを次の gate とする。

## Companion promotion の前提

この descriptor へ companion Skill を追加する前に、少なくとも次を別レーンの判断と照合する。

- 公開 Skill 名が working name のままでよいか
- one-round / multi-round / cultural-framework の責務境界が安定しているか
- CSW → Iterative → Affinity の provenance handoff が十分に評価されているか
- canonical `integration.md` / `iteration.md` の縮小範囲が確定しているか
- fallback 時に未実行の synthesis を実行済みと誤認しないか
- ja-JP の package / adapter metadata が prototype から production review 済みへ進んでいるか
- en-US realization parity を要求するか、locale ごとの公開を認めるか
- host ごとの routing / invocation behavior が実環境で確認されているか
- 完全 checkout 上の `make check` と generated artifact parity が通っているか

これらは `src/skill-set.json` が所有する情報ではなく、追加判断の gate である。

## 現段階の結論

production Skill-set descriptor は、将来の multi-Skill 化を先取りして companion を公開する仕組みではない。

**現在公開しているものを最小の identity/source contract として明示し、他レーンで昇格判断が確定したときだけ公開集合を一箇所で変更できるようにする境界である。**

そのため、現時点の production member は `cultural-substrate-weaving` 一つだけとする。
