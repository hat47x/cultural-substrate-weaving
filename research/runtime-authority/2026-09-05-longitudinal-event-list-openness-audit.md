# 長期event一覧の開放性監査

## 対象

`core/iteration.md` と `governance/governance-and-records.md` にある長期event ledgerのevent種別一覧を監査する。

現行JAでは、次の9種が同じ順で並ぶ。

- `question_shift`
- `search_shift`
- `kj_reconfiguration`
- `artifact_adoption`
- `artifact_withdrawal`
- `decision_change`
- `delayed_reactivation`
- `repeated_transfer`
- `framework_contact_change`

この監査で問うのは、これら9種の有用性ではない。現在の文面が、9種を閉じた完全分類として読む必要があるかである。

## 現行の役割

`core/iteration.md` は、長期の周回で何が後まで働いたかを、一つの点数へ潰さず出来事として追うためにeventを用いる。

`governance/governance-and-records.md` は、同じevent語彙を長期event ledgerの記録形式として持ち、評価や解釈を観測された出来事から分離する。

両者とも、event名そのものへ「有用だった」「害があった」「適切だった」のような評価を埋め込まないという観察優先の境界を持つ。

## 履歴

### 1. `4771053…`: 遅延周回の導入時は自然言語観察

`4771053cf8bbddbbf43c120a9ec06198345394b9`（Carry unresolved KJ material across delayed rounds）は、後から届く資料で以前の残差を再開できるようにし、長期では次のような変化を見るようにした。

- 以前の問いが後の資料収集を変えたか
- 孤立していた材料が後から別のまとまりを作ったか
- 外部化した構造が成果物や判断へ採用されたか

この段階の変更理由は、遅延周回で何が後まで働いたかを見失わないことであり、固定event taxonomyを定義することではなかった。

### 2. `e713de3…`: governance側のevent名は実際に追加・置換された

`e713de30061b2f2253de8a218165459702d7606a`（governance: separate observed events from attributed judgments）では、既存event一覧に対して次の変更が行われた。

- `artifact_withdrawal` を追加
- `useful_nonuse` を削除
- `harm_detected` を削除
- `framework_contact_change` を追加

同時に、「有用だった」「害だった」といった評価をevent名へ埋め込まず、観測された出来事と判断主体・根拠を分ける方針が明文化された。

つまり、この変更自身がevent語彙を可変な観察語彙として扱っている。9種を完全分類として固定したという履歴ではない。

### 3. `189ea0b…`: iteration側も同じ観察優先語彙へ追随

`189ea0b324745874f351c90ff464658f6af571a7`（core: keep longitudinal events observation-first）では、`core/iteration.md` のevent一覧へ同じ追加・置換を行い、governance側と揃えた。

この変更の主眼も、eventを評価語ではなく「何が起きたか」を表す語彙へ戻すことだった。9種の網羅性を比較実験や外部典拠で確定した記録ではない。

## 問題

現行文は、

- `必要に応じて、次のeventを記録する。`
- `長期案件では...出来事だけを残す。` の直後に9種を列挙

という形であるため、実装者が9種を許可リストとして扱う余地がある。

しかし、履歴上はevent名が追加・置換されており、長期案件で対象固有の出来事が生じた場合に、それを既存9種へ無理に押し込む必要はない。

閉じた語彙として扱うと、たとえば対象固有の重要な変化を既存event名へ近似し、来歴上の差を失う可能性がある。これは、対象固有性と観察優先の方針に反する。

## 維持すべきもの

次は変更しない。

- 現行9種のevent名
- `iteration.md` と `governance-and-records.md` の語彙整合
- event名は「何が起きたか」を表し、価値評価を埋め込まないという境界
- 評価・解釈を残す場合は判断主体と根拠を分けること
- event ledgerをKPIや自己評価点へ変えないこと
- `retrospective / prospective` の観測区別

また、`activation.md` の利用状態語彙や `principles-and-constraints.md` の帰属ラベルは、この監査の対象にしない。これらは他モジュールから参照される基礎状態語彙であり、event例の列挙とは役割が異なる。

## runtime改定方針

最小変更として、両モジュールのevent一覧が代表例であり非網羅であることだけを局所的に明示する。

例:

- iteration JA: `必要に応じて、次のようなeventを記録する。`
- governance JA: event一覧の直前または直後で、対象固有の観測eventを追加できることを明示

ENも同じ意味へ同期する。

新しいevent種別は追加しない。固定回数、採否、停止、成功条件も追加しない。

## 結論

現行9種は、長期変化を観察するための有用な標準語彙として維持する価値がある。一方、履歴上それ自体が追加・置換されており、9種を閉じた完全分類として扱う根拠は確認できない。

したがって、runtimeでは **標準event語彙を残しつつ、対象固有の出来事を同じ観察原則で追加できる開いた一覧へする** のが、長期event ledgerの由来と現行のdecision-authority / provenance方針に整合する。
