# P4 Complete-Checkout Execution Status — 2026-09-08

Status: **blocked / not run**

## Current state

complete checkout上のcanonical command executionは、現在も完了していない。

確認済みの実行経路:

- authorized Remote Desktop target: offline
- isolated container -> GitHub: DNS resolution unavailable
- GitHub Actions: repository policy上、現在は使用しない

したがってsource/test/validatorがGitHub上に存在することやPRがmergeableであることを、command PASSとして扱わない。

## Current evidence-binding contract

2026-09-07 status recordで導入した「old PASSを新HEADへ持ち越さない」という目的は維持する。

ただし、`execution commit == current HEAD`を永続recordへ要求すると、record自身をcommitした瞬間にHEADが変わる自己参照になるため、現在のbindingは次を正とする。

- `research/skill-prototypes/P4-COMPLETE-CHECKOUT-EVIDENCE-BINDING-2026-09-08.md`

```text
prepare and commit all validation-relevant mutations
        ↓
V = clean validated commit
        ↓
run canonical commands on V
        ↓
E = one evidence-only recording child
```

Eではproduction descriptorのcomplete-checkout `status/evidence`遷移と、新しいexecution record以外を変更しない。

Eより後に別commitが入れば、Vはcurrent HEADのdirect parentでなくなるためPASSはstaleになる。

## Intended preparation

translation stateはvalidation対象treeの一部なので、execution record commitへ混ぜない。

まず:

```bash
make update-en-hashes
# inspect translation-manifest diff and bilingual semantic scope
python scripts/mark_research_translation_refresh_synchronized.py
```

を行い、必要な差分をreviewしてcommitする。

この準備commitを含むclean HEADをVとして固定する。

## Canonical execution on V

V上で次を実行する。

```bash
make update-en-hashes
python scripts/mark_research_translation_refresh_synchronized.py
make research-skill-check
make build
make check
```

`make update-en-hashes`とtranslation state helperは、準備済みV上ではidempotentでなければならない。unexpected source/manifest diffが出た場合はPASSへ進まない。

production descriptorの主要required command setは引き続き:

```text
make update-en-hashes
make research-skill-check
make build
make check
```

である。translation state helperはhash refreshとresearch gateの間の明示的state transitionであり、別のproduction gateを追加するものではない。

## Current `research-skill-check` surface — not yet executed

このstatus record作成後もresearch gateは強化されている。少なくとも現在のMakefileでは、従来のsuite/package/representation/Method parity checksに加えて次が含まれる。

- current P4 authority asset registration
- Skill-owned `checks` declaration <-> Makefile execution wiring consistency
- production promotion precondition preservation
- P4 prose plan <-> machine-readable descriptor/builder-contract consistency
- public-name projection inventory and migration contract
- host-visible adapter metadata public-identity leakage check
- production source / adapter metadata read-only planners
- `test_research_*.py` full research unit-test discovery

これらはsource上で配線済みだが、complete checkout上では**まだ一度も現行集合としてPASSしていない**。

したがって過去の局所sanity check、GitHub上の静的inspection、または旧research gateの結果が存在しても、現在の `make research-skill-check` 成功証拠には代用しない。

## PASS record requirements

全command成功時、execution recordには最低限:

```text
execution commit: <V 40-char SHA>
make update-en-hashes: PASS
translation research state transition: PASS
make research-skill-check: PASS
make build: PASS
make check: PASS
```

を残す。

recordは`research/skill-prototypes/execution/`配下へ新規作成し、Vには存在していてはならない。

そのrecordとdescriptor gate遷移だけをEへcommitする。

## Gate state

```text
translation-manifest hash refresh:       NOT RUN
translation research state transition:  NOT RUN
complete-checkout research-skill-check: NOT RUN
production build regeneration:          NOT RUN
full repository make check:             NOT RUN
production promotion authorization:     NO
```

## What remains separate

complete-checkout PASSだけでは次を満たしたことにならない。

- English independent review completion
- public/installable name immediate recheck
- real-host invocation / routing evidence
- production adapter metadata review/promotion
- production builder/validator generalization acceptance
- release internal three-Skill composition acceptance

## Reopen condition

完全checkout環境が利用可能になった時点で、binding contractに従ってpreparation -> V execution -> E evidence recordingを行う。

失敗時は失敗commandとaffected contractを記録し、PASSへ書き換えない。
