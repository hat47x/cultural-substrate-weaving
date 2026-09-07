# Host-package parity oracle absorption — 2026-09-07

## 目的

OpenAI専用probeとClaude/Codex専用probeで得た有用な検査観点を、active research branchの単一 `materialize_host_package.py` へ集約します。

専用materializerを二本残すのではなく、**強いoracleだけを汎用経路のtestへ移植し、host packageの実行経路を一つに保つ**ことが目的です。

## 汎用経路がすでに持つもの

active branchの汎用host materializerは、すでに次を持っています。

- OpenAI / Claude / Codexの一つのmaterialization entry point
- ja-JP / en-USの両locale
- OpenAI interactive / metered profile
- Claude / Codex plugin manifest生成
- repository外outputのみ許可
- staging directoryで完成させてからfinal outputへrename
- metadata生成途中で失敗した場合のstaging cleanup
- 既存の空output directoryがある場合もfailure後に空のまま保持

したがって、専用probeのfinal-output直接write実装は移植しません。

## 今回吸収したoracle

### OpenAI profile parity

interactive / meteredについて、`agents/openai.yaml`を除く各Skill treeのfile集合とbyte列が一致することを要求します。

これにより、profile policy差がmethod contentへ漏れることを検出できます。

### OpenAI metadata source parity

materialized `agents/openai.yaml` が、`adapter-metadata-plan.json` に宣言されたsourceとbyte-identicalであることを要求します。

metadata wordingをmaterializer側で再生成・再解釈しません。

### Claude / Codex shared-tree parity

同じlocaleについて、Claude materializationとCodex materializationの `skills/` subtreeがfile集合・byte列とも一致することを要求します。

host差はplugin manifestへ閉じ、method treeを分岐させません。

### Declared bundle wording / VERSION parity

materialized Claude/Codex manifestについて、その時点で`adapter-metadata-plan.json`が宣言するbundle metadataのplugin identity / description / display wordingと、repository `VERSION` 由来versionが一致することを要求します。

bundle metadataが`prototype`の間は`prototype_source`を、`reviewed`へ昇格した後はproduction locale catalogを読むため、test自身が特定のmaturityへ固定されません。

## 吸収しないもの

専用probeに含まれていた時点依存のlocale readiness前提は移植しません。

companion英語版を特定のmaturityへ固定するtestは、owning research branchでrealizationが進むと古くなります。current readinessの正本はsuite manifest / adapter metadata planとし、cross-surface parity testは、状態が進んでも成立するinvariantだけを持ちます。

## #295 / #296との関係

この変更により、#295 / #296から長期的に残す価値の高いoracleは汎用経路へ吸収できます。

```text
専用probeの知見
  -> generic host materializer testsへ核融合

専用materializer実装
  -> 恒久経路にはしない
```

本変更が取り込まれた後は、#295 / #296をそのまま恒久経路として統合する必要はありません。必要ならtemporary research evidenceとしてretirement条件を明示し、より単純にはsupersededとして整理できます。

## 境界

この変更はtest/auditだけです。

- canonical `src/` は変更しません。
- production `scripts/build.py` は変更しません。
- adapter metadata sourceは変更しません。
- generated production artifactは変更しません。
- production promotion readinessは判定しません。
- 公開Skill名は確定しません。

完全checkout上の実testは、利用可能な実行環境で別途確認します。実行していない検証を成功扱いしません。
