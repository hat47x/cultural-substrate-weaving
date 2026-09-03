# KJ Atlasの統合意味論を方法論正本へ逆流させないための境界

更新日: 2026-09-03  
状態: Maintainer observation / no runtime change

## 目的

KJ Atlasでは、`AI-MERGE-SEMANTICS-01`において、カード統合支援を04ステップによる近接カードの整理と、核融合法による意味核の統合に分けて扱う計画が具体化された。

この動きはcultural-substrate-weavingと関係するが、**KJ Atlasでの製品実装を、そのまま本リポジトリの方法論正本へ移す理由にはしない。** 本書は、dogfoodの共進化記録として両者の境界を明確にする。

## KJ Atlasで具体化されたもの

KJ Atlas側では、次のような製品契約が検討されている。

- 近接した類似カードを整理する提案と、複数カードから意味核を立てる提案を区別する。
- 保留、明示的な対立・矛盾、異なる認識上の位置づけを、統合提案より優先して保護する。
- 元カード、出典、残差、統合系譜へ戻れる状態を維持する。
- AIはproposal-onlyとし、人間の承認なしに元カードを不可逆に消さない。

これらはKJ Atlasという外部表象・製品が、方法上の考え方をUI / API / provenanceへどう実現するかという**Realizationの具体化**である。

参照:

- `hat47x/kj-atlas:01_Plans/issues/issue-AI-MERGE-SEMANTICS-01-define-card-merge-semantics.md`
- `hat47x/kj-atlas:01_Plans/cross-repo/2026-09-03-kj-merge-method-boundary.md`

## 本リポジトリの正本との関係

`src/ja-JP/methods/integration.md`は、材料から意味単位を立てる操作として、境界を決める、核を抜く、伏せて立てる、戻して照合する、という方法上の境界を扱っている。また、異論・残差・出所・証拠状態を失わず、枚数削減そのものを目的化しないことを重視している。

一方、KJ Atlasの`mergeMethod`、API response field、UI上の採否、`repOf` / `canonicalId` / `mergedIntoCardId`等は、方法論一般ではなく製品固有の実現方式である。

したがって現時点では、次を行わない。

- KJ AtlasのAPI語彙を`src/<locale>/`の一般手順へ持ち込む。
- KJ Atlasで二つの方法を実装したことだけを、方法論の効果検証とみなす。
- 04ステップ型／核融合法型の利用割合を、方法論の品質KPIにする。
- KJ Atlasの製品制約を、他の利用環境にも必要な一般規則へ昇格させる。

## dogfood帰属ゲート

KJ Atlasの統合支援を実際に使った結果は、既存の`kj-atlas-cognitive-coevolution.md`の帰属ゲートに従って扱う。

### KJ Atlas側へ帰属する例

- UI / APIが元カードや残差を保持できない。
- proposal-onlyの境界が崩れる。
- 系譜が追えず、統合結果から元カードへ戻れない。
- 製品固有のguardが不足して、保留や対立を誤って統合する。

### 方法論側の変更候補になり得る例

- 製品実装を変えても、同じ統合上の欠陥が複数の異なる課題で再現する。
- 戻し照合や残差保持など、`integration.md`の方法規則自体が不足していることが対象側の証拠から示される。
- KJ Atlas以外の実践でも同じ欠陥が再現し、caller固有の問題では説明できない。

単一ケースで問題が出ても、まず製品・caller・model・実験条件を切り分ける。帰属できない場合は正本を変更せず、未決として残す。

## SOZA / TEIへの波及

今回のKJ Atlas変更は、SOZAのMethod Definition自体を変えるものではない。SOZAではMethod Definition / Realization / Applicationが分離されているため、必要ならKJ Atlasの具体的な統合支援をRealizationまたはApplicationのArtifactとして参照できる。

TEIについても、現時点ではCapability / Binding / Runtimeの契約変更を生じさせない。

このため、本リポジトリからSOZA / TEIへ追加実装を要求しない。相手側でsource / residual / lineageの表現欠落や、Capability化の具体的要件が観測された場合にだけ対応を起こす。

## 現在の判定

2026-09-03時点では、**runtimeの方法論正本は変更しない。**

KJ Atlasの04ステップ／核融合法の具体化は、外部製品でのRealizationとして観察対象に加える。そこから方法論固有の増分または欠陥が複数ケースで再現した場合にだけ、`src/<locale>/`への最小変更を検討する。

これはKJ Atlasとの連携を弱める判断ではない。製品実装、方法論、意味契約を同一視せず、それぞれの正本へ適切に帰属させるための境界である。
