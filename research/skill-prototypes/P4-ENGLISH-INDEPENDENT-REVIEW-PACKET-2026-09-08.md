# P4 English Sibling Skill — Independent Review Packet Refresh

Date: 2026-09-08

Status: review handoff; **review not yet completed**

## 目的

2026-09-07の独立査読packetで定義した査読基準を維持したまま、査読対象blobだけをcurrent Layer 2 Method Definitionへ更新する。

このrefreshを作成したこと自体は査読完了を意味しない。

## 固定査読snapshot

Reviewed target snapshot:
`research/skill-prototypes/P4-ENGLISH-INDEPENDENT-REVIEW-TARGETS-2026-09-08-v3.json`

review source commit: `6a9118cd71959dcebaf09e64f235d650eb2e1ff8`

v3は`P4-ENGLISH-INDEPENDENT-REVIEW-TARGETS-2026-09-07-v2.json`をsupersedeする。v2を上書きせず、旧snapshotはresearch historyとして保持する。

v2から変わったreview targetはLayer 2 Method Definitionのja/en blobだけである。Layer 1 runtime / Method / representation grammar、Layer 2 runtime / round templateはv2と同じblobを固定している。

## 査読基準の正本

substantive review criteriaは次の既存packetを引き続き用いる。

`research/skill-prototypes/P4-ENGLISH-INDEPENDENT-REVIEW-PACKET-2026-09-07.md`

特に次の節・境界は変更しない。

- representation grammarとround template
- Layer 1 必須不変条件
- Layer 2 必須不変条件
- Cross-layer査読
- KJ lineage / naming
- technical asset parity:
- production promotion全体の承認ではない

査読者は2026-09-07 packetの判断基準を読み、**blob比較対象だけv3 snapshotへ置き換える**。

## v3で再確認するLayer 2差分

Layer 2 Method Definitionでは、carry-forward stateをreopen authorityやcontinuation authorityへ変換しない境界、missing realization、handoff後のepistemic status保持等が後続監査で明確化された。

査読では少なくとも次を確認する。

- Japanese / English Method Definitionが同じI1〜I16 invariant surfaceを持つこと。
- carry-forward candidatesを一括reopen命令へ変えていないこと。
- residual / possible-next-checkを自動continuation authorityへ変えていないこと。
- compatible Layer 1 realizationが無い場合に未実行synthesisを実行済みと主張しないこと。
- framework-generated question / hypothesis / correspondenceのincoming epistemic statusをtarget-side factへ昇格させないこと。
- Layer 2がLayer 1 grouping algorithmを再所有していないこと。

## 査読結果の最低記録

reviewer:

reviewer relation / independence:

review date:

review scope:

Layer 1:

- semantic parity: pass | revise | blocked
- technical asset parity: pass | revise | blocked
- major issues:
- wording-only issues:

Layer 2:

- semantic parity: pass | revise | blocked
- technical asset parity: pass | revise | blocked
- major issues:
- wording-only issues:

Cross-layer ownership:

- pass | revise | blocked
- notes:

KJ lineage / naming:

- pass | revise | blocked
- notes:

Promotion recommendation:

- ready-for-next-gate | revise-before-next-gate | blocked

Reviewed target snapshot:

Reviewed commit / blob refs:

`pass`は英語realizationの独立査読gateだけに対する判定であり、production promotion全体の承認ではない。

## 変更後の扱い

査読開始後にv3 listed blobが変わった場合、その変更を自動的に査読済みへ継承しない。新snapshotを作るか、変更blobについて明示的なdelta reviewを残す。

translation source-hash同期、complete-checkout execution、public-name直前recheck、production builder/validator generalization、real-host behaviorはこの査読とは別gateである。
