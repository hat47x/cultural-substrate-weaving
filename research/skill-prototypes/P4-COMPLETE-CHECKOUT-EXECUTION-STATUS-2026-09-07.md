# P4 Complete-Checkout Execution Status — 2026-09-07

Status: **blocked / not run**

## Purpose

production promotion gateにあるcomplete-checkout validationについて、設計・静的inspectionと実際のrepository command executionを混同しないため、現在の実行状態を明示する。

## Intended commands

今回のCSW canonical bilingual変更ではtranslation-manifestのbyte-level hash更新も必要である。完全なcheckoutでは、主要gate commandに加えてtranslation research stateの明示的な遷移を行う。

```bash
make update-en-hashes
# inspect translation-manifest diff and bilingual semantic change
python scripts/mark_research_translation_refresh_synchronized.py
make research-skill-check
make build
make check
```

production descriptor上の主要required command setは引き続き、

```text
make update-en-hashes
make research-skill-check
make build
make check
```

である。`mark_research_translation_refresh_synchronized.py` は新しいproduction gateではなく、最初のcommandとresearch gateの間にある**research state transition**である。

`make update-en-hashes` は英訳本文を生成する処理ではない。現在の日本語canonical bytesを `i18n/translation-manifest.json` のsource hashへ正規のrepository scriptで反映する。

その後、diffを確認したうえでstate-transition helperを実行する。helperはhashを更新せず、全tracked hashが同期済みで、今回の英語semantic markerが残っている場合だけ `P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.json` を `synchronized` へ進める。

この順序により、hash更新だけをもってreview済みと扱うことも、pending stateのままresearch checkを通そうとすることも防ぐ。

必要なproduction promotion段階へ進んだ後は、generated artifact diffとrelease-internal composition validationも別途確認する。

## 2026-09-07 current execution state

このセッションではcomplete checkout上のcommand executionを完了できていない。

確認した実行経路:

- authorized remote desktop execution target: currently offline
- current containerからpublic repositoryを新規cloneする経路: external network / DNS access unavailable
- GitHub Actions: repository policy上、現在は使用しない

したがって、GitHub上でsource / tests / validatorsを更新できていることを、`make research-skill-check` が成功した証拠として扱わない。

## 2026-09-08 addendum — newly added Layer 2 checks

Layer 1 → Layer 2 handoff再設計とexternal iterative-research Skill比較により、repository source上では次を追加した。

- `iterative-inquiry-synthesis/evidence/dossier.md`
- Method Definition I16: carry-forward state is not reopen or continuation authority
- English Method DefinitionへのI15復元
- `evals/CASES.md` Case 10
- `evals/HANDOFF-CARRY-FORWARD-RECHECK-2026-09-08.md`
- `iterative-inquiry-synthesis/scripts/check_method_parity.py`
- suite validator上のLayer 2 promotion-relevant evidence登録要件
- `tests/test_research_skill_suite.py` のnegative regression
- `Makefile` の `research-skill-check` へのLayer 2 Method parity check接続

また、unit test側に残っていた英語Layer 1 packageの旧 `references/REPRESENTATION.md` 期待値を、現在のmanifestに合わせて `references/REPRESENTATION.en.md` へ修正した。

これらは**source-level changeであり、実行成功の証拠ではない**。特に、新しくMakefileへ配線したMethod parity checkと更新したsuite unit testsは、complete checkout上ではまだ一度も実行していない。

## 2026-09-08 addendum — declared-check wiring and stale-pass prevention

research gateの構造監査から、次の二つの追加リスクを閉じた。

### Skill-owned check declaration / execution drift

`suite-manifest.json` の各Skillに `checks` を宣言しても、従来はMakefileへ自動配線されなかった。そのため、manifestへcheckを追加しても `make research-skill-check` が実行しない、またはMakefileへ直書きしたSkill-owned checkがmanifestへ登録されない、というdriftが起こり得た。

repository source上では次を追加した。

- `scripts/validate_research_declared_checks.py`
- `tests/test_research_declared_checks.py`
- `make research-skill-check` へのmeta-validator接続

契約は次である。

```text
manifest-declared Skill check
    <=>
research-skill-check direct execution
```

suite-level validatorやplannerはこの双方向契約の対象外であり、Skill source root配下のcheckだけをmanifestの正本と照合する。

isolated sanity checkでは、現在相当のrecipeはerrorなし、Layer 2 parity check行削除はmissing、未登録Skill-owned checkの直書きはunregisteredとして検出した。ただしこれはrepository全体のtest実行ではない。

### Old passed evidence must not survive a new HEAD

従来のcomplete-checkout validatorは、`status: passed` のexecution recordに40桁SHAを要求していたが、そのSHAが現在のcheckout HEADと同じかまでは確認していなかった。

これを修正し、passed状態では次を要求する。

```text
execution commit == current checkout HEAD
```

したがって、research gateやtestを変更した後に、以前のcommitで作ったPASS recordをそのまま再利用することはできない。

対応unit testでは、同一SHAを受理し、stale SHAとcurrent HEAD不明を拒否するfixtureを追加した。これもcomplete checkout上ではまだ実行していない。

## 2026-09-08 addendum — promotion preconditions and locale-tree package purity

production migration準備をさらに静的監査し、次のdriftを閉じた。

### Promotion preconditions are now machine-checked

`P4-PRODUCTION-SUITE-DESCRIPTOR-PROTOTYPE.json` の `promotion_preconditions` を単なる説明配列として放置せず、最低必須集合を検査するvalidatorを追加した。

- `scripts/validate_research_promotion_preconditions.py`
- `tests/test_research_promotion_preconditions.py`
- `make research-skill-check` への接続

最低必須条件には、complete-checkout research gate、current HEADとのPASS evidence一致、public-name再確認、英語sibling独立査読、production adapterへの昇格、builder/validator一般化、release内部三Skill composition等を含む。

### Production name projection drift in maintainer plan

production descriptor / builder static planではLayer 1公開候補が `material-led-synthesis` である一方、古いpromotion planに `affinity-synthesis` production path例が残っていたため修正した。

再発防止として、`P4-PUBLIC-NAME-PROJECTION-INVENTORY.json` にpromotion planを監査対象として追加し、次を行う。

- `material-led-synthesis` production source / adapter pathをrequired markerにする。
- `affinity-synthesis` production source / adapter pathをforbidden markerにする。
- `validate_research_public_name_projection_inventory.py` がforbidden markerを検出する。
- unit testでstale production path再侵入を負例化する。

research ID `affinity-synthesis` 自体はresearch history / research artifactで保持し、production identityとの区別を壊さない。

### `locale_tree` is now a package-closed production source boundary

promotion planに残っていた古い `explicit_files` source-mode記述を、現在のdescriptor / builder contractと同じ `locale_tree` へ統一した。

machine-readable contractでは次を固定した。

```text
src/skills/<public-name>/<locale>/
    = package-closed source tree

copy_scope       = entire_locale_tree
exclusion_filter = none
```

具体的な追加・更新:

- `P4-PRODUCTION-BUILDER-GENERALIZATION-CONTRACT.json`
  - `locale_tree_source_package_purity: true`
  - sibling production sourceは `locale_tree`
  - builderはresearch-only exclusion filterを持たない
- `scripts/validate_research_production_builder_contract.py`
  - descriptor sibling source modeの `locale_tree` 固定
  - package-purity validation flag / invariantの固定
- `tests/test_research_production_builder_contract.py`
  - `explicit_files` rollback、purity flag削除、exclusion-filter invariant削除を負例化
- `scripts/validate_research_production_plan_consistency.py`
  - machine-readable descriptor / contractを正本としてpromotion planのsource-mode proseを照合
- `tests/test_research_production_plan_consistency.py`
  - stale `explicit_files` sentence、old production path、package-closed marker欠落を負例化
- `plan_production_builder_generalization.py`
  - locale-tree projectionへ `copy_scope: entire_locale_tree`, `package_closed: true`, `exclusion_filter: none` を外在化
- `REFERENCE-CLASSIFICATION.md`
  - research/eval artifactであっても、locale Skillがoptional progressive referenceとして明示参照する場合はpackage supportになり得ることを明文化

Layer 1 Japaneseの `evals/CASES.md` / `evidence/dossier.md` はJapanese Skillから直接progressive referenceされるためpackage closureへ含める。一方、Layer 1 EnglishやLayer 2 dossierへ日本語research supportをlocale parityの名目で自動copyしない。

これらも**設計・source-level regressionの追加であり、complete checkout execution結果ではない**。

## What has been checked without claiming command execution

GitHub repository source上では、少なくとも次の契約を静的に更新・確認した。

- research/public production name projection
- public-name current collision recheck evidence
- English independent review packet / pinned blob target snapshot
- English independent review gate validator
- English runtime technical-asset localization contract and tests
- target/framework tension and cross-field emergence runtime contract
- tension/sublation regression fixture and ownership boundary
- research gateへのvalidator接続
- translation refresh pending scope / English markers / state transitionを保持するmachine-readable contract
- Layer 1 → Layer 2 carry-forward / reopen / continuation separation
- Layer 2 external-loop mechanism adoption/rejection evidence
- Japanese / English Layer 2 Method I1〜I16 static parity check source
- manifest-declared Skill checkとresearch gate executionの双方向wiring contract
- passed complete-checkout evidenceとcurrent HEADの一致要求
- promotion preconditionsの最低必須集合
- production-name projectionのstale-path negative guard
- `locale_tree` production sourceのpackage-closed / whole-tree-copy契約
- localeごとのruntime reference closureに基づくresearch-support package inclusion境界

これはPython execution、translation hash refresh、translation state transition、generated artifact regeneration、test discovery成功を意味しない。

## Gate state

```text
translation-manifest hash refresh:          NOT RUN after latest CSW canonical changes
translation research state transition:     NOT RUN
complete-checkout research-skill-check:    NOT RUN
Layer 2 Method parity check:               NOT RUN in complete checkout
declared-check wiring validator:           NOT RUN in complete checkout
promotion-precondition validator:          NOT RUN in complete checkout
production-plan consistency validator:     NOT RUN in complete checkout
locale-tree package-purity regressions:    NOT RUN in complete checkout
updated research unit tests:               NOT RUN in complete checkout
stale-pass HEAD binding tests:             NOT RUN in complete checkout
production build regeneration:             NOT RUN after latest research changes
full repository make check:                NOT RUN after latest research changes
production promotion authorization:        NO
```

## Reopen condition

完全なrepository checkoutを持つ実行環境が利用可能になった時点で、上記手順を実行する。

失敗した場合は結果を隠さず、失敗command、error、affected contractを記録して修正する。

成功した場合も、このrecordを上書きして最初から成功していたことにはしない。新しいexecution resultを追加し、実行したcommit SHAとcommand set、およびtranslation state transitionを明示する。
