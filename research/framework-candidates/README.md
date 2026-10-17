# Cultural Framework Candidate Research

Status: research-only

このディレクトリは、CSWが参照する文化体系の量と質を増やすための候補化・資料化レーンである。

現行runtimeのsystem-selectionは複数の体系名を探索アンカーとして持つが、個別体系の厚い資料層はまだ限定的である。ここでは、体系名を増やすこと自体ではなく、異なる認知operationを安全に供給できる体系を、sourceと系譜差を保ったままSkill候補へ育てる。

## 目的

増やしたいのは次の三つである。

1. operation diversity
   - position / vacancy / relation / transition / cycle / boundary / scale / practice / counter-view等、異なる認知仕事を開けること。
2. framework fidelity
   - 体系固有の構造を、一般的な自己啓発語彙や後世の混成対応表へ薄めないこと。
3. target returnability
   - framework由来の候補を対象側の問い・観察・反証・試行へ戻せること。

体系数、ファイル数、読書量、対応表の件数は、それ自体では品質指標にしない。

## 候補化の段階

固定の採用スコアは置かない。代わりに、資料状態を次のように区別する。

- anchor-only
  - 候補想起の名称だけがある。
- sourced-candidate
  - 構造核を確認できる一次資料・学術資料・標準資料がある。
- profile-ready
  - 構造核、operation、系譜差、誤用境界を短いprofileへ落とせる。
- skill-candidate
  - 実際のCSW operationとして使うためのprofileとsource boundaryが揃った。
- adopted
  - framework dossierがruntime/packageへ採用された。独立した別Skillとして公開済みという意味ではない。

この段階は価値順位ではない。たとえば、宗教的・医療的文脈が強い体系は認知的に豊かでも、誤用境界を十分に書けるまで研究段階に留める。

## 候補を選ぶ観点

### 構造型の差を優先する

同じ「7項目」「5分類」のような表面的な要素数ではなく、体系が何を操作できるかを見る。

- 離散位置・組合せ
- 対立・補位置
- 生成／抑制など複数relation
- 周期・位相
- 複数周期の結合
- 経路・network
- 条件連鎖と切断
- 中心／周辺・上下・層
- 実践・注意方向
- aesthetic reception
- counter-view / reversal

### sourceの種類を分ける

最低でも、可能な範囲で次を区別する。

- primary / classical text
- scholarly reference
- institutional standard
- living-tradition educational source
- modern popular synthesis

後の層を使うほど、どこまでが古典的構造でどこからが近代的再構成かを明示する。

## runtimeへ入れないもの

候補段階では次をruntime ruleへ昇格させない。

- 特定体系の優遇順位
- 「N体系使えば十分」といったcoverage条件
- framework名だけからの自動routing
- 文化体系の主張を対象事実へ変換する規則
- 医療・心理・宗教上の主張の事実認定
- 後世の対応表を古典構造として固定すること

## Registry-0 boundary

現時点のRegistry-0は新しい重複データベースを作らず、次の既存artifactを一つの境界として扱う。

- `cognitive-operation-inventory.json`
  - framework identity、readiness、native primitive、cognitive operation、selection cue、source、misuse boundary、artifact pathのmachine-readable正本。
  - 各体系の`discovery_hypothesis`は、通常の入口が見落としやすい認知作業の仮説と、その判定状態（未検証／発見価値の記録／重複の記録）を持つ。適合度や順位ではない。
- `framework-corpus-contract.md` / `scripts/framework_corpus_contract.py`
  - sourced/profile/runtime materializationの品質下限。
- `scripts/framework_selection_workspace.py inspect`
  - 一体系について、source全文、構造、operation、cue、do-not-assume、正負fixture、profile/runtime/source packetを同時に再取得するread-only view。
- 同toolの `recall / shortlist / contrast / worksheet / review / audit-map`
  - candidateをrankせず、missing cognitive functionから候補を思い出し、near-neighbor差とnon-activationを外在化し、target-return後のprovenanceを監査する操作面。

Registry-0は文化そのものの正本ではない。文献・系譜・研究資料からCSWが利用できる範囲を明示した**CSW側の表現**である。readinessやsource数をfit scoreへ変換せず、`adopted`も「この対象へ適合する」という意味にはしない。

この境界により、体系数が増えてもモデル記憶から暗黙にframeworkを再構成する割合を下げ、activation前に「何を見せる体系か」「何を仮定してはいけないか」「どの資料へ戻れるか」を同じ場所で確認できる。

## 現在の入口

- cognitive-operation-inventory.json
- coverage-map.md
- first-wave-2026-10-01.md
- second-wave-2026-10-01.md
- third-wave-2026-10-01.md
- fourth-wave-2026-10-01.md
- fifth-wave-2026-10-02.md
- sixth-wave-2026-10-02.md
- seventh-wave-2026-10-02.md
- eighth-wave-2026-10-02.md
- ninth-wave-2026-10-02.md
- tenth-wave-2026-10-02.md
- eleventh-wave-2026-10-02.md
- twelfth-wave-2026-10-02.md
- thirteenth-wave-2026-10-02.md
- fourteenth-wave-2026-10-02.md
- fifteenth-wave-2026-10-02.md
- sixteenth-wave-2026-10-03.md
- seventeenth-wave-2026-10-05.md
- eighteenth-wave-2026-10-05.md
- nineteenth-wave-2026-10-05.md
- worked-examples/ 以下のtarget-return例
- comparisons/ 以下のnear-neighbor / comparative collapse test
- portfolio-qualitative-audit-2026-10-01.md
- near-neighbor-differentiation-2026-10-01.md
- crossing-value-2026-10-08.md（採用中核での交差の価値と一般化）
- runtime-requalification.md（実行時採用の再資格と比較資料）
- trials/README.md（Llullの体系接触前レビュー入力と未評価の原記録の扱い。独立レビュー結果は未取得）
- framework-corpus-contract.md（候補の資料品質と採用段階の規約）
- profiles/ 以下の各体系profile
- source-packets/ 以下のpre-profile資料層

### 採用状態を確認する

採用・研究段階の現在値は `cognitive-operation-inventory.json` を正本とする。複数チャットで採用・降格・研究が並行するため、ここには体系の固定一覧や件数を複製しない。

一覧は、リポジトリのルートから次のように取得する。

```sh
python research/framework-candidates/scripts/framework_selection_workspace.py registry-snapshot research/framework-candidates/cognitive-operation-inventory.json
```

表示されるのは段階ごとの体系識別子・件数と、現時点で実行時に利用可能な体系の識別子である。表示順は台帳の記載順であって、適合度や推奨順位ではない。

個別体系の資料、使いどころ、使用してはならない前提は `inspect` で確認する。

```sh
python research/framework-candidates/scripts/framework_selection_workspace.py inspect research/framework-candidates/cognitive-operation-inventory.json huayan
```

`adopted` は体系が実行時資料として取り込まれている状態を表すだけで、その対象に適しているとは限らない。`profile-ready` は十分な資料を備えた研究候補であり、採用済みと同義ではない。現在の採用判断と、通常の分析による再発見可能性の検討については [実行時採用の再資格](runtime-requalification.md) を参照する。

### 研究を進める際の境界

文化体系の数を増やすこと自体は目標にしない。類似した体系を評価するときは [近接候補の差分](near-neighbor-differentiation-2026-10-01.md) と `comparisons/` の具体例を参照し、対象へ戻したときに独自の問いが残るかを検討する。

また、体系に触れてから類似の通常手法を見つけられることと、**体系に触れる前からその手法を自然に選べること**を区別する。広範な順位付けや単純な効果比較は行わず、具体的な対象での発見価値、通常手法との重複、使用しない判断、文化・医療・宗教上の境界を記録する。

研究候補はそのまま実行時へ昇格させない。資料の整備、比較例、反例、対象側の検証を経て、必要な場合にだけ個別に採用を判断する。
