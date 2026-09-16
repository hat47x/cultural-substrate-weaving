# E6 natural-work utility / overhead — evidence extraction protocol

- experiment id: `PQ-E6-007`
- program: E6 — natural-work utility / overhead
- protocol date: 2026-09-16
- source baseline: `develop/v0.5.0@da7fbd0f9d1fb300c8a03dee074446eb3aeba4f8`
- primary requirements: PQ-10、関連してPQ-03、PQ-04、PQ-07、PQ-11、PQ-12
- status: protocol / evidence-extraction audit; natural-work run未実施

## 目的

E6では、CSWや分離したMethodが**実際の仕事の中で何を残したか**と、方法適用・観測が**本来の仕事にどの程度の負荷を加えたか**を読む。

ただし、品質観測のために仕事を作らない。記録を埋めるために利用者へ追加操作を要求せず、自然な作業の中ですでに生じたartifact、Living Lab round / event、利用者の判断、明示的に残った測定だけを証拠にする。

このprotocolを作成しているrepository保守作業そのものを、E6の`natural_work`事例として数えない。

## 現行Living Labから得られる証拠

schema 0.2では、`natural_work` roundから少なくとも次へ戻れる。

- `task.source_refs` — 元の仕事・材料への参照
- `artifacts` — 作業後に残った成果物
- `residuals` — 解消されず残った事項とその来歴
- `reopening_conditions` — 後から再開する条件
- `interpretations` — user / ai / external / mixed / unknownを区別した解釈
- `framework_contacts` / `activation_scope` — 何をどの範囲で使ったか。ただし有効性KPIではない

event schema 0.2では、自然に観測されたときに次の変化を記録できる。

- `artifact_adoption` / `artifact_withdrawal`
- `decision_change`
- `delayed_reactivation`
- `repeated_transfer`
- `question_shift` / `search_shift` / `kj_reconfiguration`

各eventは`prospective / retrospective`を区別し、`evidence_refs`を必須とする。

一方、数値の`measurements`はround schemaの`paired_check.comparison`に置かれており、`natural_work`へ必須化されていない。この境界をE6でも維持する。

## E6で読む5つの証拠面

### 1. 成果物へ残った変化

見ること:

- CSW / Method適用後に、実際の成果物へ何が残ったか
- 後で採用・撤回・修正されたものは何か
- 方法説明だけが増え、成果物へ何も戻らなかったか

優先する証拠:

- artifact ref
- `artifact_adoption` / `artifact_withdrawal` event
- 元成果物と更新後成果物の確認可能な差分

AIが「役に立った」と解釈しただけでは、成果物へ残った変化の観測にしない。

### 2. 利用者の判断・訂正・撤回

見ること:

- 利用者が候補を採用、修正、差し戻し、撤回したか
- 方法の適用範囲を縮小・停止したか
- AI解釈と利用者判断が食い違ったか

利用者の判断は`source_type: user`として扱い、AIによる推定へ置き換えない。

### 3. 残差の後日の再利用

見ること:

- 前roundで残したresidualが、後日の材料や問いによって再び使われたか
- 再開条件が、実際の局所再開に役立ったか
- 未解決事項を残したこと自体を失敗扱いしていないか

証拠がある場合、`delayed_reactivation`や`repeated_transfer`と元round / artifactへの参照を結ぶ。

### 4. 観測可能なoverhead

E6でのoverheadは、**実際に観測できた追加負荷だけ**を記録する。

例:

- 方法適用のために増えた明示的なやり取り数
- 記録作業に要した時間が、時計・ログ・利用者申告などで明示的に残っている
- 方法上の説明や帳票のために発生した追加操作
- 利用者が「記録が重い」「方法説明が作業を妨げた」と明示した判断

次はoverheadの測定値にしない。

- Living Lab eventの件数
- framework contact数
- activation / non-activation件数
- AIが会話を見て推定した所要時間
- retrospectiveに正確な根拠なく復元したターン数や時間

**測定がないことは`0`ではなく`not measured`である。**

### 5. 解釈

観測から「なぜ役立った／重かったか」を読む場合、その記述はinterpretationとして来歴を付ける。

- user judgment
- AI interpretation
- external review
- mixed interpretation

これらをartifact deltaや数値measurementと同一視しない。

## thin extraction sheet

既存recordを変更せず、評価時に必要な場合だけ次の薄いworksheetを使う。これはLiving Lab schemaの追加正本ではなく、E6評価者の作業メモである。

```text
work_ref:
source_round_ids:
source_event_ids:
observation_mode: prospective / retrospective / mixed

artifact_delta:
  observation:
  evidence_refs:

user_response:
  observation:
  evidence_refs:

residual_reuse:
  observation:
  evidence_refs:

overhead:
  added_explicit_interactions: <integer | not measured>
  logging_time: <duration | not measured>
  other_observed_burden:
  measurement_source_refs:

interpretations:
  - source_type:
    statement:
    evidence_refs:

known_limits:
```

空欄を埋めるために追加質問をしない。元のrecordにない精密な値を後付けしない。

## must-pass invariants

### U1 — natural-work integrity

観測のためだけに新しい仕事、追加round、追加framework利用を作らない。

### U2 — no forced measurement

`natural_work`へ`paired_check`相当のmeasurement blockを必須化しない。

### U3 — missing is not zero

明示的な測定がないoverheadを`0`と扱わない。

### U4 — count is not utility

event件数、framework contact数、activation件数を有用性や負荷の代理KPIにしない。

### U5 — provenance separation

観測、測定、利用者判断、AI / external interpretationを分離する。

### U6 — artifact return

有用性を主張する場合、可能な範囲で実際の成果物・判断・残差再利用のいずれかへ戻れる証拠を示す。

### U7 — retrospective honesty

retrospective observationはそのままretrospectiveとし、当時測っていない時間・turn数を精密な値として復元しない。

### U8 — user correction priority

利用者による採用・撤回・訂正を、AI自己評価で上書きしない。

### U9 — no method self-certification

CSW / Method自身の説明だけで領域成果物の品質を認定しない。

### U10 — no automatic method change

一件のnatural-work成功・失敗から、runtime / Method Definition / promotionを自動変更しない。

## 初回runの開始条件

E6 Run 001は、**別の本来目的で行われた自然作業**に、評価可能なLiving Lab recordまたはartifact参照が有機的に残ったときに始める。

最低限必要なのは次である。

1. 本来の仕事を示す参照
2. 実際に残ったartifactまたは判断への参照
3. 観測のprovenance
4. E6評価が後付けである場合、そのretrospective性

追加やり取り数や記録時間は、明示的に観測されている場合だけ使う。これらがなくてもE6のartifact / judgment / residual観測は行えるが、overheadについては`not measured`とする。

## schema変更へ進む条件

現時点ではLiving Lab schema 0.2、event schema 0.2、validatorを変更しない。

新しいfieldを検討するのは、実際のnatural-work runで次を満たした場合に限る。

1. 同種の重要な証拠gapが複数回生じる。
2. 既存の`artifacts`、event、`interpretations`、opaque refsでは十分に表現できない。
3. 追加fieldを記録する負荷が、得られる観測価値に見合う。
4. optional fieldではなく必須化する必要性を別途説明できる。

まず研究用worksheetで足りるなら、schemaへ昇格させない。

## このprotocolで証明しないこと

- CSWの有効性を単一スコアで証明しない。
- CSW利用時と非利用時の因果差をnatural-work一件から推定しない。
- 記録がない負荷を「負荷なし」としない。
- eventが多いことを成果としない。
- natural-workをrelease gate件数へ変換しない。
- このrepository作業をE6の実利用例として水増ししない。

## 現時点の判断

**protocol only / no Living Lab schema change / no synthetic natural-work run.**

現行schemaには、成果物・残差・再開・利用者/AI等のinterpretation provenanceを残す基盤がすでにある。overheadの精密測定を毎回要求するとQ7 / PQ-10そのものを損なうため、まず自然に残る証拠を薄く読む。
