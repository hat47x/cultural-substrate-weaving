# プロダクト品質を育てるための要件・設計・実験プログラム

- 策定日: 2026-09-11
- 対象基準: `develop/v0.5.0@f4370bea759fcb83a4eeae352b325f8feaea39d5`
- 位置づけ: CSWと分離中のMethod群を、方法論としてだけでなく利用可能なプロダクトとして前進させるための品質プログラム
- 境界: この文書は方法論の第二正本ではない。方法の意味は`src/ja-JP/`、research prototypeの契約は`research/skill-prototypes/`を正本とする

## 1. 目的

現在のリポジトリには、方法論の意味上の正本、多言語同期、生成物、token budget、release check、Living Lab、research prototypeのpromotion gateなど、多くの検証資産がある。一方で、これらはそれぞれの局所的な契約を強く守る反面、**利用者が触れるプロダクト全体として何を品質とみなし、どの証拠がどの品質要求を支えるのか**を一枚に結んでいない。

このプログラムでは、次を目的とする。

1. 「壊れていない」だけでなく、「境界を守りながら実際に使える」ことを品質要件へ落とす。
2. 静的契約、モデル行動、自然な実利用を混ぜず、それぞれに適した検証を設計する。
3. CSW、`affinity-synthesis`、`iterative-inquiry-synthesis`の分離が、分割そのものを目的化せず、実際の引き渡し品質を高めているか確認できるようにする。
4. 単発の良い出力やAI自己評価を、プロダクト改善の根拠として過大評価しない。
5. 失敗を再現可能なfixtureへ落とし、修正後に同じ欠陥が戻らないようにする。

プロダクト品質を単一スコアへ圧縮しない。品質は、異なる失敗様式を持つ複数の軸として扱う。

## 2. 品質モデル

### Q1. 意味・権限境界の完全性

方法が意図した意味を保持し、AIが著者の決定権を奪わないこと。

- 文化体系由来の候補を、対象側の独立した支持なしに事実へ昇格させない。
- 来歴ラベルを、採用・発話・公開・停止の自動許可として使わない。
- 利用範囲、読み込み深度、停止、採否、公開・行動への反映をCSW自身が独立決定しない。
- 領域固有の正確性・品質基準をCSWの自己評価で代替しない。

主な証拠: `src/ja-JP/`、`evals/semantic-retention.json`、正本validator、行動試行。

### Q2. 発動・読み込みの較正

必要なときに必要な範囲だけ使え、使わないことや浅く使うことも正常な状態として扱えること。

- 課題種別だけで自動発動・抑制しない。
- `probe / preview / full / enacted`を成果の序列にしない。
- 固定の体系数、round数、full depthを完了条件にしない。
- 過剰適用によって対象固有の具体や領域手法を押し流さない。

主な証拠: activation契約、`evals/activation-cases.json`、paired behavioral probe、Living Lab。

### Q3. 認知上の有用性と対象への帰還

説明量を増やすだけでなく、問い、探索先、区別、関係、成果物、判断へ追跡可能な変化を生み得ること。

- framework agreementの数を成果にしない。
- 不一致・抵抗から情報が生まれる余地を保つ。
- 第三構造や止揚を成功quotaにしない。
- 生成・構成で使う構造資源と、対象事実を区別する。

主な証拠: `governance/evaluation.md`、controlled probe、Living Labのartifact delta。

### Q4. 材料保持・KJ統合の完全性

変換後も元材料へ戻れ、意味の一体性と証拠状態を同時に守れること。

- 行為者、留保、反証、孤立、矛盾を表札の簡潔さのために落とさない。
- 類似性だけで過統合しない。
- 分割によって文脈や土の匂いを失わない。
- 図解・叙述・元材料を往復できる。

主な証拠: `affinity-synthesis`のMethod Definition、representation check、behavioral fixture。

### Q5. Method間handoffの完全性

thin-CSW化によって責務が分かれても、必要な意味・来歴・残差が境界で脱落しないこと。

- CSWから材料統合へ渡すとき、framework由来とtarget側支持を区別できる。
- affinity synthesisからiterative inquiryへ渡すとき、採用済み成果だけでなく残差・未解決事項・戻り先を保持できる。
- 後続roundは全体を無条件に再構築せず、touched artifactを局所的に再開できる。
- handoff先が上流の決定権を奪わない。

主な証拠: split ownership check、handoff contract、end-to-end behavioral experiment。

### Q6. 時間をまたぐ更新可能性

後から届く材料、人間の訂正、ツール結果によって以前の理解を必要な範囲だけ更新できること。

- 古い判断を固定しない。
- 残差と再開条件を保持する。
- 後日の撤回・変形・再利用を履歴から消さない。
- 新材料と無関係な領域まで毎回再構築しない。

主な証拠: `core/iteration.md`、iterative inquiry prototype、longitudinal Living Lab。

### Q7. 利用者負荷と操作可能性

品質向上のための観測・帳票・方法実行が、本来の仕事より重くならないこと。

- 記録のために自然な作業を止めない。
- 必須帳票や固定roundを安易に増やさない。
- 重要な境界判断は後から追える一方、通常利用では不要な内部情報を要求しない。
- 誤適用した場合に縮小・撤回できる。

主な証拠: task completion timeや介入回数などの局所測定、利用者判断、Living Lab。

### Q8. プラットフォーム間の意味的同等性

OpenAI Skill、Claude Code、ChatGPT GPT、Microsoft 365 Copilot等で、パッケージ形式が異なっても中核境界が変質しないこと。

- プラットフォーム制約による省略を明示する。
- 同じ品質要求を満たせないsurfaceを、完全対応と表示しない。
- 生成物差分が方法論の意味差へ変わらない。

主な証拠: adapters、generated artifacts check、cross-platform behavioral probe。

### Q9. 多言語同期と翻訳品質

英語版が日本語正本と同期し、hash同期だけでなく意味上の境界も維持すること。

- source hashが一致する。
- authority、provenance、evidence boundaryのような高リスク語義を独立に確認する。
- research prototypeの英語版は、独立査読前にproduction-readyとみなさない。

主な証拠: translation manifest、review snapshot、English review gate。

### Q10. 生成・配布・releaseの再現性

正本とadapterから同じ手順で成果物を再生成でき、手編集による分岐を防ぐこと。

- generated artifactが追跡可能である。
- release packageの構成が宣言と一致する。
- production/research境界が崩れない。
- public identity、version、branch contractが一貫する。

主な証拠: `make check`、`make release-check`、production/research validators。

### Q11. 観測と評価の来歴

観測された差、測定値、利用者判断、AI解釈を分離し、品質判断の根拠を後からたどれること。

- AIの自己採点を客観測定として扱わない。
- `non_activation`やevent件数を有効性KPIにしない。
- retrospective / prospectiveを区別する。
- 実験結果が方法変更を自動承認しない。

主な証拠: Living Lab schema 0.2、研究記録、実験報告。

### Q12. 回帰可能性と改善の可逆性

欠陥が見つかったとき、再現fixtureを残し、修正が別の境界を壊していないことを確認できること。

- bugfixには可能な限り再現ケースを伴わせる。
- 新しい静的ルールは、既存規則の言い換えではなく実際の失敗様式に対応させる。
- 行動改善が確認できなければ、文言追加を撤回・縮小できる。
- research prototypeからproductionへ昇格するときは、promotion gateを迂回しない。

## 3. 品質要件

品質要件は、release gateにできるものと、行動証拠を必要とするものを分ける。

| ID | 要件 | 最低限必要な証拠 | release blocking |
|---|---|---|---|
| PQ-01 | 対象事実とframework由来候補の証拠境界を保持する | static contract + adversarial probe | static違反はYes、behavior未測定はNo |
| PQ-02 | 著者・呼出側の決定権をAIが独立に置換しない | semantic retention + behavioral probe | static違反はYes |
| PQ-03 | 固定体系数・固定depth・固定roundを完了条件にしない | source contract + probe | Yes |
| PQ-04 | 発動・非発動・限定利用を勝敗へ変換しない | activation contract + Living Lab provenance | Yes for contract |
| PQ-05 | Method間handoffで来歴・残差・未解決事項を失わない | end-to-end handoff experiment | production promotion時に必須候補 |
| PQ-06 | 後続roundが局所再開できる | longitudinal experiment | promotion判断材料 |
| PQ-07 | 領域固有品質をCSW評価で代替しない | source contract + domain fixture | Yes |
| PQ-08 | platform差が中核境界差へ変わらない | generated checks + cross-platform probe | package contractはYes、behaviorは段階導入 |
| PQ-09 | 日本語正本と英語版の同期・意味境界を守る | hash + independent review | Yes |
| PQ-10 | 実利用の観測負荷が本作業を圧迫しない | overhead measurement + user judgment | No。改善判断材料 |
| PQ-11 | 観測・測定・評価の来歴を分離する | schema/validator + audit | Yes for recorded research assets |
| PQ-12 | 既知の失敗をfixture化し、修正後の回帰を検出する | regression fixture | 既知重大欠陥ではYes |

`release blocking`を一律に増やさない。モデル行動は非決定的であり、単発のbehavioral probeを厳格なrelease gateにすると、false positive/negativeの両方を増やす。最初は診断用のevidence planeとして運用し、十分に安定した局所不変条件だけを将来gate化する。

## 4. 品質検証の三層設計

### Layer A — 決定論的contract check

対象:

- repository / branch / version contract
- source・translation整合
- generated artifact
- package/release composition
- schema・JSON structure
- research / production boundary
- split ownership / projection / promotion gate

特徴:

- 同じcommitから同じ結果が得られる。
- failureは原則としてrelease blockingにできる。
- モデルが実際に規則へ従うかは証明しない。

現行では`make check`、`make release-check`、`make research-skill-check`がこの層をかなり厚く担っている。

### Layer B — 制御されたbehavioral probe

対象:

- authority boundary
- evidence/provenance boundary
- activation calibration
- material retention
- Method間handoff
- delayed reactivation
- platform behavior parity
- known regression

特徴:

- 入力資料、依頼、利用可能なskill、モデル表示、実行順を記録する。
- 必須不変条件と診断観測を分ける。
- 一つの総合点ではなく、failure modeごとに読む。
- AI評価者を使う場合も`source_type: ai`相当の来歴を保持する。
- baselineとの差を方法の因果効果と即断しない。

### Layer C — natural-work Living Lab

対象:

- 実際の執筆・調査・設計・分析で何が残るか
- user adoption / correction / withdrawal
- 後日の再利用・撤回・再開
- 観測負荷
- controlled probeでは見えない長期副作用

特徴:

- 通常は`natural_work`。
- 観測のために仕事を作らない。
- event数やframework contact数をKPIにしない。
- 一件の成功・失敗を静的ルールへ直結させない。

この三層を混ぜないこと自体を品質設計の一部とする。

## 5. 実験ポートフォリオ

### E0 — 品質証拠カバレッジ監査

目的: 現行リポジトリの各品質要求に、どの証拠があり、どこが未測定かを棚卸しする。

- 種別: repository audit
- baseline: `develop/v0.5.0`の現状
- 出力: evidence matrix、次実験の優先順位
- 状態: 2026-09-11に初回実施。`research/product-quality/2026-09-11-quality-evidence-audit.md`を参照

### E1 — authority / provenance adversarial probe

目的: モデルが便利な結論へ急ぐ圧力の下でも、著者決定権と証拠境界を守れるかを見る。

ケースには、次を意図的に混ぜる。

- target側で支持された材料
- frameworkからのみ生じた魅力的な仮説
- 利用者が採否を未決定の候補
- 「最適案を決めてそのまま公開して」という過剰委任に見える曖昧な文言

必須不変条件:

- framework-only候補をtarget factへ昇格しない。
- provenance labelから公開許可を推論しない。
- 実際に委任された範囲を超えて最終決定しない。

### E2 — activation calibration paired check

目的: CSWを常に深く読むことが品質向上ではないことを、異なる課題型で確認する。

ケース群:

- 明確な技術修正
- 曖昧な設計問題
- 文化体系が探索に使える調査
- KJ統合だけで足りる材料整理

観測:

- activation scope
- framework loading depth
- 余計な手順・説明の増加
- 実際の成果物差分

固定の「正しいactivationラベル」を大量に作るより、明白な境界ケースから始める。

### E3 — split-method handoff integrity

目的: CSW → affinity synthesis → iterative inquiryの分離が、来歴・残差・戻り先を失わせていないか確認する。

第一優先で実施する。具体的なpacketは`research/product-quality/experiment-001-handoff-integrity.md`に置く。

必須不変条件:

- framework由来とtarget支持をhandoff後も区別できる。
- affinity統合で孤立・矛盾・未解決事項を都合よく消さない。
- iterative roundで、新材料と無関係な成果物を無条件に再構築しない。
- 後続Methodがauthor decisionを自動確定しない。

### E4 — delayed reactivation

目的: 数round後に届いた新材料が古い残差へ触れたとき、局所的に再開できるか確認する。

同一session内の即時追記だけでなく、引継ぎpacketから再開する条件も含める。

### E5 — cross-platform semantic parity

目的: 同じsource snapshotと同じtask packetを、複数surfaceで実行し、中核不変条件の差を見る。

比較対象は文章の一致率ではなく、PQ-01〜PQ-07の境界違反とする。Microsoft 365のように能力制約があるsurfaceでは、制約を欠陥と混同しない。

### E6 — natural-work utility / overhead

目的: 実作業で成果物や判断に何が残り、観測・方法適用の負荷がどの程度かを見る。

追加で記録し得る測定:

- 方法適用のために増えた明示的なやり取り数
- 利用者が差し戻した説明・候補
- 後で再利用された残差
- 成果物へ残った変更

これらを総合スコアにはしない。

### E7 — known-failure regression

実利用やprobeで重大な欠陥が見つかったとき、その入力を匿名化・合成して最小fixtureへ落とす。修正前に再現し、修正後に同じ失敗様式が消えたことを確認する。

## 6. 実験の実施契約

behavioral experimentでは、最低限次を残す。

1. **experiment id / source commit**
2. **quality requirement under test**
3. **fixed source packet**
4. **task prompt**
5. **loaded skill/method and version**
6. **visible model / product mode / tools**
7. **observed output artifact**
8. **must-pass invariants**
9. **diagnostic observations**
10. **measurement provenance**
11. **user / AI / external interpretation provenance**
12. **known confounders**
13. **decision: no change / docs / fixture / runtime candidate**

同じモデルを使った別チャットは「独立した人間評価」ではない。比較AIを使う場合はAI由来の解釈として残す。

## 7. 実験結果から変更へ進む条件

### 文書・fixtureだけを変える

- 誤読しやすいが方法の意味自体は既に正しい。
- 操作上の説明不足で、正本ルールの追加は不要。
- 既知の境界を回帰fixtureへ固定すれば十分。

### runtime method変更候補にする

少なくとも次を満たす。

- 実際のfailure modeまたは反復する不足を説明できる。
- 既存規則の単なる言い換えではない。
- 変更によって守る不変条件が明確である。
- 修正前後を比較できるケースがある。
- 領域固有手法の責任をCSWへ取り込んでいない。

### production promotion候補にする

research split-methodでは、上記に加えて既存promotion gate、translation review、public identity、builder/packaging contract、complete-checkout evidenceをすべて通す。行動実験が良かったという理由でpromotion gateを迂回しない。

## 8. 優先順位

現時点では、追加機能より次の順を優先する。

1. **E3 split-method handoff integrity** — v0.5.0の構造変更そのものが価値を損なっていないかを最優先で確認する。
2. **E1 authority / provenance adversarial probe** — 誤ると成果物の信頼性へ直接影響する。
3. **E4 delayed reactivation** — 長期利用という狙いに直結する。
4. **E2 activation calibration** — 過剰適用と不必要な負荷を抑える。
5. **E5 cross-platform parity** — production surfaceが増える前に差を把握する。
6. **E6 Living Lab** — 上記の制御試行を実利用の長期観測で読み直す。

この順序は件数目標ではない。重大な実利用failureが見つかった場合は、E7を最優先へ割り込ませる。

## 9. 実装方針

短期では新しい大規模evaluation frameworkを作らない。既存の`evals/`、`research/`、Living Lab、unittest、repository validatorを使い、必要になった最小の機械可読契約だけを追加する。

具体的には次の順で進める。

1. E0監査を基準線として保存する。
2. E3の固定source packetとmust-pass invariantsを文書化する。
3. まず一回のengineering trialを実行し、実験記録の不足を洗い出す。
4. 記録形式が安定してから、必要なら`evals/`へmachine-readable scenario contractを追加する。
5. failureが再現した場合だけtest/validatorへ昇格させる。
6. 行動試行の件数を増やすこと自体を目標にしない。

これにより、評価基盤を作る作業がプロダクト本体より重くなることを避ける。

## 10. このプログラムの成功条件

成功とは、スコアが上がることではない。次が継続して可能になる状態をいう。

- 変更前に、どの品質要求を改善する変更なのか言える。
- 変更後に、どの証拠で改善・非改善・副作用を判断するか言える。
- 方法の意味、モデル行動、実利用結果を混同しない。
- failureが再現fixtureとして蓄積される。
- 分離したMethod間で意味と来歴が失われない。
- platformや言語が増えても中核境界を追跡できる。
- 観測や評価のために本来の作業が圧迫されない。

プロダクト品質は、規則を増やすことではなく、**重要な不変条件を少ない規則で守り、実際の失敗から学び、必要なところだけを可逆的に改善できること**として育てる。
