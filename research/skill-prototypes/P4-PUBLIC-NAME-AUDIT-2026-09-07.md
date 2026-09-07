# P4 Public Name Audit — 2026-09-07

Status: naming recommendation for production promotion; research IDs remain unchanged

## 目的

Layer 1 / Layer 2を独立Skillとして公開する前に、

- KJ法®との誤認
- 親和図法・Affinity Mappingとの関係
- Agent Skill ecosystemでの名称衝突
- 生成AI向けMethodとして何を名前に出すか

を再確認する。

この監査だけでrenameを実施しない。

complete-checkout gate、独立査読、production source promotionと同時に大規模renameを行うことを避けるため、**public installable nameを確定してからproduction canonical sourceへ昇格する**。

## KJ法という名称

川喜田研究所の現在の公式案内では、`KJ法®` は株式会社川喜田研究所の登録商標と明示されている。

また公式説明では、狭義のKJ法を概ね、

```text
ラベル
  -> グループ編成
  -> 図解
  -> 叙述
```

という一ラウンドの過程として説明し、複数ラウンドの累積利用を広義のKJ法の文脈で説明している。

本research suiteはこの系譜を重要な参照として保持するが、

- AI向けprovenance補正
- epistemic seam
- source-return audit
- secondary resonance
- renderer-independent representation
- delta-based reopening

等を独自に加えている。

したがってpublic Skill名を `kj-method` とするのは避ける。

KJ法はMethod Definition / evidence上の**系譜**として明記し、公式KJ法の完全再現や認定Skillとは称しない。

## 現在のLayer 1 working name

```text
affinity-synthesis
```

表示名:

```text
Affinity Synthesis
親和統合
```

この名前には長所がある。

- bottom-up groupingとの関係が分かりやすい
- Affinity Mapping / Affinity Diagramの利用者が概略を推測しやすい
- 「図」だけでなく、意味単位・表札・関係・叙述まで含むので `synthesis` が妥当

一方、production installable nameとしては衝突余地が見つかった。

## GitHub / Agent Skill ecosystemの確認

2026-09-07時点のGitHub検索では、`transformteamsg/dx-harness` の公開Skillが、research synthesis / analysisの呼び出し先として次を明示している。

```text
use affinity-synthesis or insight-writer
```

現行default branchのtree上では、`affinity-synthesis/SKILL.md` という実体までは確認できなかったが、少なくとも**同名Skillを予定・参照している公開ecosystemが存在する**。

したがって、`affinity-synthesis` を「空いているinstallable name」とは扱わない。

なお一般Web上では、Affinity Mapping / Affinity Diagramを行うAgent SkillやUser Research Synthesis Skillが既に多数存在する。

この領域で単純に `affinity-*` を名乗ると、UX interview clustering専用Skillと誤認される可能性もある。

## 候補比較

### 1. `material-led-synthesis`

現時点の第一候補。

GitHub exact searchでは同名Skillを確認できなかった。

長所:

- 「分類体系を先に置かず、材料に構造を語らせる」というMethodの中心を表す
- interview / UX領域へ限定されない
- 事実資料、観察、創作断片、文化体系由来候補等を同じ意味境界原理で扱える
- KJ法やAffinity Diagramの公式再現を名乗らない
- 生成AI向けに追加したsource-return / residual保持とも整合する

弱点:

- grouping / affinityという操作が名前だけでは見えにくい
- `material` が英語話者に「物質・素材」と読まれる余地がある

ただしSkill descriptionとdisplay nameで補える範囲と判断する。

候補:

```text
installable name: material-led-synthesis
display name:      Affinity Synthesis
Japanese display:  親和統合
```

または、より方法の性質を前面に出す場合、

```text
display name: Material-Led Synthesis
Japanese display: 素材主導の親和統合
```

も可能である。

### 2. `material-led-affinity-synthesis`

GitHub exact searchで同名を確認できなかった。

長所:

- material-ledとaffinityの両方を明示できる
- 既存Affinity Mappingとの系譜的近さも伝わる

弱点:

- installable nameとして長い
- `affinity-synthesis` collisionを完全には心理的に回避しにくい
- 名前に説明を詰め込みすぎる

第二候補とする。

### 3. `source-led-synthesis`

GitHub exact skill-name collisionは確認できなかったが、一般Webでは `source-led synthesis` が文献・証拠ベース研究の一般表現として既に使われている。

本Methodの材料は公的sourceだけではない。

- raw observation
- experiential fragment
- creative image
- question
- contradiction
- cultural-framework-generated candidate

も扱う。

そのため `source-led` はevidence synthesisへ意味を狭める可能性があり、第一候補にはしない。

### 4. `affinity-integration`

一般Web / GitHubではCRM等の「Affinity integration」という別意味が既に存在する。

方法名としても `integration` はCSWの旧 `integration.md` と混同しやすい。

採用しない。

### 5. `affinity-synthesis`

research working IDとしては維持可能。

ただしproduction installable nameとしては、公開ecosystemで同名参照が見つかったため第一候補から外す。

## 日本語名称

### 「親和図法」

既存の一般的な語として理解されやすいが、本Method全体を表すには少し狭い。

本Methodは、

```text
意味単位化
親和的な束ね
表札
多段統合
関係図解
叙述
元材料への戻し検査
残差保持
```

を含む。

また、既存のAffinity Diagram Skillと同じ簡略化手順だと誤認される可能性がある。

### 「親和統合」

現時点では表示名として適切。

- 親和的な集約を示す
- 図だけに限定しない
- `KJ法`を名称として占有しない
- 一回の統合MethodというLayer 1境界に合う

必要なら説明上、

```text
親和統合 — 素材主導の一回統合
```

と補足する。

## Layer 2

現在のworking name:

```text
iterative-inquiry-synthesis
```

2026-09-07時点のGitHub exact searchでは直接衝突を確認できなかった。

また名前が、

- repeated full regenerationではない
- inquiryをラウンド間で継続する
- synthesis artifactを差分再開する

という役割を概ね表している。

現時点ではproduction候補名を維持する。

ただし公開前にもう一度registry / GitHub検索を行う。

## 推奨

### Research branch

現時点ではrenameしない。

```text
affinity-synthesis
iterative-inquiry-synthesis
```

をstable research IDとして維持する。

理由:

- eval / representation / package / metadata / testsが大量にこのIDを参照している
- complete-checkout gate前にrename churnを入れると、方法検証と名称変更の失敗を区別しにくい

### Production promotion時

第一候補:

```text
research id:        affinity-synthesis
production name:    material-led-synthesis
display:            Affinity Synthesis / 親和統合
```

Layer 2:

```text
production name: iterative-inquiry-synthesis
```

production suite descriptorは `source id` と `installable name` を別fieldとして持てるようにする。

これによりresearch historyをrenameせず、公開packageだけ衝突回避できる。

## Promotion gate

production canonical source作成前に次を再確認する。

1. `material-led-synthesis` の最新GitHub / Skill registry衝突。
2. `iterative-inquiry-synthesis` の最新衝突。
3. display name `Affinity Synthesis` が同一host上で混同を生まないか。
4. KJ法®を公式再現と誤認させないdescription / lineage disclaimer。
5. 日本語「親和統合」が既存一般技法を独占する印象にならないか。

## 現時点の結論

```text
KJ法      -> lineageとして保持、public Skill名にはしない
親和図法  -> 参考語・既存技法名として扱う
親和統合  -> 日本語displayの第一候補
Affinity Synthesis -> display候補として維持
material-led-synthesis -> production installable name第一候補
affinity-synthesis -> research IDとして維持
iterative-inquiry-synthesis -> production候補名を維持
```

この分離により、系譜への敬意、既存Skill ecosystemとの衝突回避、生成AI向けMethodの独自境界を同時に保ちやすい。
