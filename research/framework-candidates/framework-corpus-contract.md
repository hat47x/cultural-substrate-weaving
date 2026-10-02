# Framework corpus readiness contract

Status: research quality contract / not an efficacy benchmark

文化体系の候補数を増やすとき、readiness名だけが先行しないための最低契約を定める。

## sourced-candidate / profile-ready / adopted 共通

少なくとも次を持つ。

- names
- structural_primitives
- cognitive_operations
- useful_for
- do_not_assume
- 2件以上のsource。各sourceは kind / title / url を持つ。

この条件は体系の有効性を意味しない。モデル記憶だけで構造を補わず、候補を再確認できる最小資料面を固定する。

## profile-ready

共通条件に加え、次を必須にする。

- 実在する `profile_path`
- 通常言語から候補想起できる `selection_cues` を2件以上
- 正のtarget-return例を示す `worked_example_paths`
- 適用すべきでない条件を示す `negative_example_paths`
- profile本文の source basis
- operationの明示
- target-return questions
- de-binding

profile-readyは「採用に近い」という順位ではない。体系固有の構造をモデル記憶で再構成せず、探索候補として再利用できる状態を表す。

## adopted

共通条件に加え、次を必須にする。

- 実在する `runtime_path`
- `selection_cues` を2件以上

runtime採用には、別途lineage・variant・non-license境界が必要である。このスクリプトはその意味内容を自動判定しない。

## worked exampleの役割

正例は、その体系固有の操作が文化固有語を外した後も対象へ問いを返せることを示す。

負例は、形式が当てはまりそうに見えても対象側の構造が支えない場合に、体系適用を止められることを示す。

いずれも効果スコアではない。

## 実行

```bash
python research/framework-candidates/scripts/framework_corpus_contract.py
```

readiness契約は体系の品質下限を守るために使う。候補の優劣、採用順位、fit scoreには使わない。
