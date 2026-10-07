# Medieval renga linked-verse negative example

Status: hypothetical / research-only

## Target

production障害で、特定API requestの直後に同じdatabase transactionが失敗し、監査log、trace、DB error codeがすべて同じ一意なconstraint violationを示している。

目的は、再現条件を固定し、原因を確認し、patchとregression testを作ることである。

## Why the framework should not be forced

この段階では探索方向を広げるより、同一のevidence chainを切らずに収束することが重要である。

renga由来のthematic releaseを強制すると、

- DB constraintから認証へ移る
- 認証からnetworkへ移る
- networkから組織運用へ移る

といった、証拠で支えられていない論点移動を「多様性」と誤認する可能性がある。

直前と接続していても、移動する必要がない局面はある。

## Correct result

non-activationとする。

通常の障害分析で、

1. failing transactionを再現する
2. constraint violationの入力条件を特定する
3. 修正する
4. regression testを固定する

へ進む。

## Stop condition

renga contactを開始していた場合も、次のいずれかで停止する。

- 一つの原因仮説が複数の独立Evidenceで強く支持された
- callerが収束・決定段階へ移った
- shift後の候補がtarget-side Evidenceへ戻れない
- 新しい候補が「違う話題」であること以外の価値を持たない
- correction costが探索増分を上回る

多様性が不要な局面で、多様性を方法論上の義務にしない。
