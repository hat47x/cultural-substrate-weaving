# framework loading depthの長期観察

- Status: Research protocol / no runtime rule change
- Date: 2026-08-30
- Related: `v39-deepseek-api-validation.md`, `kj-atlas-cognitive-coevolution.md`

## 目的

v39 Stage Pでは、補助比較として`B1 representation-only - B0 domain/KJ = -0.209722`だった。

これは、体系固有の操作を実行する前に、**厚い文化体系資料をworking contextへ読み込むこと自体がanchoringや過剰適用を生む可能性**を示す仮説として保持されている。ただしStage Pは5ケースの診断的pilotであり、Stage Cで同じ比較は確定していない。

現行runtimeにはすでに、

- 非発動／限定適用／全体適用
- 「現在の判断に必要なファイルだけを読む」
- 限定適用では直接必要な参照一つから始める
- 一括読み込みを避ける
- frameworkの採用と適用深度を分ける

という制御がある。

したがって現時点では、`index → preview → full`のような新しい静的階層を方法論へ追加しない。まず、**実課題で実際にどの程度の資料を読んだとき、何が増え、何が歪んだか**を長期的に観察する。

## 観察単位

一つのframework適用機会について、必要な場合だけ次を残す。

### 1. 発動状態

- `none`：文化体系を使わなかった。
- `limited`：特定の問い・層・検査だけに限定した。
- `full`：複数の構造探索とKJ統合を組み合わせた。

これは現行`core/activation.md`の三段階に対応する。

### 2. 実際に読んだ範囲

ファイル数をKPIにはしない。代わりに、どの種類の情報までworking contextへ入ったかを記録する。

- `selection_only`：体系候補・用途・不採用条件だけを見た。
- `application_rule`：割当・反転・代替・除去等の適用手続きまで読んだ。
- `framework_detail`：個別体系の要素・象意・歴史的対応等を外部資料から詳しく読んだ。
- `multiple_frameworks`：複数体系の詳細を同一ラウンドで読んだ。

現行repositoryでは個別体系の厚いdossierを静的層に持たないため、`framework_detail`は主に動的に取得した外部資料を指す。

### 3. 読み込み前の対象側snapshot

frameworkを詳しく読む前に、少なくとも次を短く残す。

- 現時点の問い
- 対象側で確認できている事実・関係
- 未解決・矛盾・孤立
- 既にあるdomain/KJ baseline

これは後から、framework語彙によって問題設定自体が置き換わったかを見るための比較点になる。

### 4. 読み込み後に増えたもの

次を区別する。

- 新しい対象側の問い
- 新しい調査先
- 新しい関係候補
- 反証条件
- 実成果へ採用された構造
- 単なるframework内部の説明

「説明量が増えた」こと自体は増分とみなさない。

### 5. anchoring / captureの兆候

次のどれかが見られたら記録する。

- framework語彙が対象側の語彙より前景化した。
- frameworkの位置を埋めるためだけの探索が始まった。
- 対象に無い因果・段階・周期を暗黙に補った。
- 最初のframework解釈に反する材料の扱いが弱くなった。
- 別frameworkへ変えても同じ対象側所見に戻らず、体系ごとに説明だけが増えた。
- removal check後に主要所見が残らなかった。

### 6. useful nonuse / early stop

次の場合も有効な観察として残す。

- frameworkを読まない方が明瞭だった。
- selectionだけで候補を棄却できた。
- application ruleまで読んだが、詳細資料へ進む必要がなかった。
- 詳細を読んだ後、増分が無く対象へ戻った。

「使わなかった」ことを失敗扱いしない。

## 長期で見る差

loading depthの価値は、その場の文章だけでなく後続ラウンドで見る。

### delayed question value

浅い適用または深い適用から生じた問いが、後の新資料を拾う能力を変えたか。

### delayed anchoring

一度導入したframework語彙が、後のKJ束や検索対象を不必要に固定し続けなかったか。

### reconfiguration

後の資料によって、framework由来の束を自然に壊し、組み替えられたか。

### artifact adoption

frameworkを除去した後にも残る構造が、実際の設計・文章・判断へ採用されたか。

## KJ Atlas dogfoodでの使い方

既存の4arm比較を増やして5arm、6armへ膨らませない。

Arm B/Dで文化体系を使った場合に、この文書のloading metadataを**補助観察**として残す。

これにより、

- skillを使ったかどうか
- KJ Atlasを使ったかどうか

という主比較を維持しながら、同じskill arm内で「どの深さまで読んだか」を後から診断できる。

loading depthは実験者が均等に割り当てる処置ではなく、現行runtimeがそのケースで実際に選んだ深さとして記録する。したがって、深さ別の単純平均を因果効果とは扱わない。

## 方法論変更への昇格条件

次のような所見が複数の異なる実課題で再現するまで、loading hierarchyを静的runtime規則へ追加しない。

### より浅い読み込みを規則化する候補

- 詳細framework資料を読む前の問いだけで十分な成果が繰り返し得られる。
- 詳細loading後にforcing/provenance lossが繰り返し増える。
- early stopの方が後のKJ再編や対象固有性を保つ。

### より深い読み込みを正当化する候補

- 詳細資料を読まない条件では生じなかった対象側の問い・反証・構造が繰り返し生じる。
- その所見がremoval check後にも残り、実成果へ採用される。
- 後続ラウンドでもframework captureではなく対象理解として再利用される。

## 現時点で変更しないもの

この観察だけを理由に、次を`src/<locale>/`へ追加しない。

- 固定の`index / preview / full`階層。
- 「一度に読むファイルはN件まで」のような固定上限。
- 特定frameworkの禁止・優遇。
- token量を認知品質の代理指標とする規則。
- B1 representation一般を有害とみなす規則。

## 現時点の判定

現行runtimeはすでに「必要な参照だけを読む」「限定適用から始める」「増分が無ければ停止する」という選択的loadingを含んでいる。

次に必要なのは新しい規則ではなく、**その選択が実課題でどのように働き、どの深さで有用な増分またはanchoringが起きるかを記録すること**である。
