# KJ Atlas Case 001 長期継続チャット観察lane

- Status: Prospective observational companion / not an experimental arm
- Date started: 2026-08-30
- Related target case: `hat47x/kj-atlas` Case 001 — KJ Atlasの存在目的と一次利用仕事
- Related: `kj-atlas-cognitive-coevolution.md`, `framework-loading-depth-observation.md`, `v39-deepseek-api-validation.md`

## 目的

KJ Atlas Case 001のA〜D比較とは別に、長く継続している実作業チャットの中で、`cultural-substrate-weaving`の問い・残差・KJ再編が時間をまたいでどう働くかを観察する。

このlaneは比較実験のarmではない。

長期チャットはすでに、

- v39 API検証の結果
- その診断から生じた方法改訂
- KJ Atlasの価値仮説やdogfoodの来歴
- 過去ラウンドの未解決事項

を知っている。また、`cultural-substrate-weaving`自身も`develop/v0.3.0`上で更新され続ける。

したがって、このlaneから「skillの因果効果」を推定しない。観察するのは、**どの問い・残差・適用判断が後の実作業へ実際に残ったか**である。

## A〜Dとの分離

Case 001のA〜Dは、同一snapshotと独立contextを使う比較条件である。

この長期laneは、次の理由からA〜Dへ数えない。

1. prior contextが大量にある。
2. method snapshotが固定されない。
3. 実験運営者が既存仮説を知っている。
4. 新しいGitHub資料や実装変更が自然に流入する。
5. ユーザー自身の判断・問いも時間とともに変化する。

長期laneで有用なパターンが見つかった場合だけ、必要な部分を後でfresh-context比較へ切り出す。

## 対象

Case 001と同じ中心問いを参照する。

> KJ Atlasは、既存のAIチャット、ホワイトボード、質的分析ツール、文書/issue管理では十分に満たしにくい、どの利用仕事のために存在するべきか。現在の設計・実装・dogfoodは、その価値をどこまで実現し、何をまだ実証できていないか。

ただし、長期laneではこの問いだけに固定しない。後続の資料によって、問いそのものが変形・分岐・縮小することを許す。

## 各重要ラウンドで残す最小記録

毎メッセージ記録しない。KJ構造、方法判断、実成果が変わったときだけ残す。

### `round_ref`

その時点の日時または識別子。

### `method_ref`

そのラウンドで実質的に使っていた`cultural-substrate-weaving`のcommitまたはbranch。

methodが途中で変わった場合、変更前後を同一条件として扱わない。

### `new_material`

新しく入ったGitHub資料、実装、検証結果、利用者観察、外部資料。

### `reactivated_residual`

以前は結論にならなかった問い・孤立・矛盾のうち、今回の新材料で再び意味を持ったもの。

### `framework_use`

- `none`
- `limited`
- `full`

必要なら`framework-loading-depth-observation.md`のloading metadataも付ける。

### `kj_change`

以前のまとまりがどう維持・分解・再編されたか。

### `artifact_or_decision`

issue、ADR、実装、調査計画、文書、採否など、実際に何が変わったか。

### `nonuse_or_harm`

使わない方がよかったframework、途中で止めた理由、対象を歪めた操作。

### `reopen_condition`

何が来たら次に再開するか。

## 長期laneで特に観察するもの

### 1. delayed question value

以前に生じた問いが、後の資料で初めて有用になったか。

その場では答えにならなくても、後の資料を拾う受容器として働いたなら記録する。

### 2. KJ reconfiguration

新材料が、既存の束へ単に追加されるだけでなく、以前の束や表札を壊して別の構造を作ったか。

### 3. artifact adoption

長期探索から生じた所見が、実際のissue、ADR、実装、文書、検証計画へ変換されたか。

### 4. useful nonuse

文化体系を使わない、または限定して止める判断が、対象固有性や作業速度を守ったか。

### 5. delayed framework capture

一度導入した文化体系の語彙・関係が、後の資料を不必要に同じ型へ読み続けさせていないか。

### 6. method evolution

観察結果によってskill自身が変わった場合、その変更が後のケースで本当に役立ったか。

「方法が変わったから結果が良くなった」と自己証明しない。変更後も失敗・不採用を同じように残す。

## このチャットで既に存在するretrospective材料

prospective開始前の履歴には、少なくとも次がある。

- whole-field / native-enactmentを厚くする方向への発展。
- v39で強制native enactmentの負結果が得られたこと。
- 単発API検証からラウンド式KJの長期観察へ重点を移したこと。
- `develop/v0.3.0`で遅延KJ周回とbounded framework applicationを方法論へ取り込んだこと。
- Stage P `B1 - B0`を確定規則にせず、loading depthの観察課題として残したこと。

これらは後付けのretrospective材料であり、成功率や因果効果の計算には使わない。

## prospective開始点

この文書を`develop/v0.3.0`へ統合した時点以降を、長期laneのprospective期間とする。

最初に開いた観察問いは次である。

1. `limited`適用は、`full`適用より対象固有性を保ちながら有用な問いを残せるか。
2. frameworkを詳しく読まない判断が、後のKJ再編を柔らかく保つか。
3. 文化体系由来の問いが、数ラウンド後のGitHub資料・実装・第三者利用結果を拾う能力を変えるか。
4. 過去の残差が再活性化したとき、前回の表札を正解として固定せず組み替えられるか。
5. 長期laneから生じた方法変更が、独立したCase 001 A〜Dまたは後続Case 002/003でも必要と確認されるか。

## skill変更への帰属

このlaneだけで`src/<locale>/`を変更しない。

方法変更候補は、少なくとも次を確認する。

- 長期laneで具体的な実害または実用増分が観察された。
- 同じ問題が別の実課題、または独立比較でも再現する。
- caller/domain/product固有の問題ではなく、二つの中核能力に属する。
- 最小変更で直せる。
- 変更後に元ケースと異なるケースへ戻して回帰を確認できる。

## 現時点の判定

この長期laneの価値は、A〜Dより高い点数を出すことではない。

> **一度の回答では見えない、問いの遅延効果、未解決の再活性化、KJ構造の再編、実成果への採用、使わない判断の学習を、実作業を続けながら観察すること**

にある。

因果比較と長期改善を分離することで、比較の厳密さを守りながら、本来のラウンド式KJが持つ時間軸も失わない。
