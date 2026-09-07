# P2 ja-JP Claude/Codex bundle metadata prototype — 2026-09-07

## 目的

P2で三Skillのpackage subtree・entry transform・adapter metadata coverageまで分離したため、ja-JPのClaude/Codex locale bundleについて、既存CSW単体向けmetadataをそのまま流用せず、三Skill収録時のplugin-level metadata prototypeを作る。

この記録はproduction adapter更新ではない。host上の実挙動、marketplace掲載、release readinessも評価しない。

## 現在の前提

ja-JPでは次の三Skill realizationがresearch上存在する。

- `cultural-substrate-weaving` / target `weave`
  - 文化的体系から構造候補・問い・対応を供給し、対象側へ戻して検証する。
- `affinity-synthesis`
  - 材料主導の一回統合を担当する。
- `iterative-inquiry-synthesis`
  - 複数ラウンドの問い・差分・再開・停止を管理し、必要な一回統合を互換realizationへ委ねる。

Claude/Codexは現行production pluginで同じ `skills/` treeを共有するため、三Skillを同一locale pluginへ収録する予定である。一方、既存 `adapters/claude-code/locales.json` のdescriptionはCSW単体を前提としている。

## Prototype metadata

research source:

`research/skill-prototypes/adapters/claude-codex/ja-JP/bundle-metadata.json`

prototypeでは次を維持する。

- plugin name: `cultural-substrate-weaving-ja`
- display: `Cultural Substrate Weaving — 日本語`
- explicit invocation
- contains:
  - `cultural-substrate-weaving`
  - `affinity-synthesis`
  - `iterative-inquiry-synthesis`

説明文は次の境界を明示する。

1. 三つは責務の異なるSkillである。
2. 必要に応じてhandoffする。
3. 帰属・残差・未解決を保持する。
4. 三つを一つの万能手順へ混ぜない。

## なぜplugin名を変えないか

この段階ではdistribution identityの変更ではなく、既存locale pluginへcompanion Skillを収録する場合のmetadata境界を検証している。

そのため `cultural-substrate-weaving-ja` を維持する。新しいsuite名へのrenameは、marketplace identity、upgrade path、公開文書、release asset名まで巻き込む別の判断であり、このprototypeから自動導出しない。

## なぜdisplayを変えないか

同様に、`Cultural Substrate Weaving — 日本語` を暫定維持する。

ただしこれはproduction wordingが確定したという意味ではない。三Skill bundleとして利用者に十分明確かは、host上での表示面・発見導線・Skill一覧との組み合わせを見て再評価する必要がある。

## Metadataとroutingを分ける

このprototypeは「pluginに何が収録されているか」を説明する。

次のことはまだ決めない。

- ある依頼に対してどのSkillを自動選択するか。
- `weave` がAffinity/Iterativeを自動起動するか。
- AffinityからIterativeへ自動昇格するか。
- 三Skillを常に連続実行するか。

OpenAI metadata routing reviewでは、複合ケースは一つの万能Skillへ押し込まずhandoffで扱う方針がprovisional passだった。Claude/Codex bundle metadataも同じ責務分離を壊さない必要がある。

## Validator boundary

`validate_research_adapter_metadata.py` はbundle prototypeについて次だけを検査する。

- prototype sourceが存在する。
- schema / locale / statusが一致する。
- plugin name / display / descriptionが空でない。
- `contains` がsuite manifestのbundle compositionと一致する。
- invocation policyがexplicitである。
- existing production catalogのplugin nameを維持する。
- multi-Skill bundleではreview-requiredを外さない。

文言品質やhost挙動はvalidatorで判定しない。

## Coverage planner

ja-JP Claude/Codexは `prototype` と表示する。

en-USはcompanion runtime自体がplannedのため、既存single-Skill locale catalogを `review-required` baselineとして維持する。

これにより、次を混同しない。

- runtime subtreeが存在すること
- plugin-level metadata prototypeがあること
- production wordingがreviewedであること
- host上でroutingが期待どおり動くこと
- release可能であること

## 今回まだ検証していないこと

- Claude Code上のSkill発見・表示・明示呼び出し挙動
- Codex plugin上のSkill一覧・interface表示
- 三Skillbundle説明が実際のUIで長すぎないか
- plugin identityをCSW名のまま維持すべきか
- bundle-level descriptionから個別Skill routingへの誤誘導が起きないか
- en-US companion metadata parity
- production builder generalization
- generated artifact freshness
- `make check` / `make release-check`

## 次の実作業

1. 同じ4種類程度のrouting taskを使い、bundle-level descriptionが三Skillの責務境界を歪めないかauthoring-level reviewする。
2. 問題がなければja-JP bundle metadataを`prototype`のまま保持し、host executionで観察可能になるまで`reviewed`へ上げない。
3. その後、research-only package materializerへ進むか、production builder generalizationへ進むかをmigration gateに照らして判断する。

## 結論

ja-JP Claude/Codex三Skill bundleについて、既存plugin identityを保ちながら三Skillの独立責務とhandoffを説明するmetadata prototypeを定義できる。

ただし、これはproduction metadataの承認ではない。**三Skillを同じpluginに収録することと、三Skillを一つの方法へ混ぜることは別である。** この境界を保持したまま、次はrouting wording reviewへ進む。
