# P4 English Sibling Skill — Independent Review Packet

Date: 2026-09-07

Status: review handoff; **review not yet completed**

## 目的

`affinity-synthesis` と `iterative-inquiry-synthesis` の英語realizationは、artifactとしては存在するが `translated-draft` である。

このpacketは、production promotion gateにある **English sibling Skill realizations receive independent review** を、単なる「英文として自然か」の確認にしないための査読対象・判断基準・記録形式を定義する。

この文書を作成したこと自体は査読完了を意味しない。

## 固定査読snapshot

査読対象のruntime、Method Definition、および英語runtimeが直接参照する説明的technical assetは、次のsnapshotで具体的なblobへ固定する。

- `research/skill-prototypes/P4-ENGLISH-INDEPENDENT-REVIEW-TARGETS-2026-09-07-v2.json`
- review source commit: `f14326626563c5d8de4bcf06d9e19d9a280c826c`

旧snapshot `P4-ENGLISH-INDEPENDENT-REVIEW-TARGETS-2026-09-07.json` は、technical asset localization前の履歴として残す。上書きして現在の査読対象であったことにはしない。

査読者はbranchの「現在内容」だけを参照して完了判定しない。v2 snapshotに記録された日本語canonical blobと英語translated-draft blobを比較対象とする。

査読後にlisted blobが変更された場合、その変更を自動的に査読済みへ継承しない。新snapshotを作るか、変更blobについて明示的なdelta reviewを残す。

## 査読対象

### Layer 1 — research ID `affinity-synthesis`

Canonical Japanese:

- `research/skill-prototypes/affinity-synthesis/SKILL.md`
- `research/skill-prototypes/affinity-synthesis/references/METHOD.md`
- `research/skill-prototypes/affinity-synthesis/references/REPRESENTATION.md`

English draft:

- `research/skill-prototypes/affinity-synthesis/SKILL.en.md`
- `research/skill-prototypes/affinity-synthesis/references/METHOD.en.md`
- `research/skill-prototypes/affinity-synthesis/references/REPRESENTATION.en.md`

Language-neutral / research-only supporting assets:

- `references/affinity-map.schema.json` — shared language-neutral schema
- `references/HIERARCHY-AND-LINEAGE.md` — research/lineage note; not an English runtime dependency
- `evals/CASES.md` — regression fixture; not runtime instruction

### Layer 2 — research ID `iterative-inquiry-synthesis`

Canonical Japanese:

- `research/skill-prototypes/iterative-inquiry-synthesis/SKILL.md`
- `research/skill-prototypes/iterative-inquiry-synthesis/references/METHOD.md`
- `research/skill-prototypes/iterative-inquiry-synthesis/references/ROUND-TEMPLATE.md`

English draft:

- `research/skill-prototypes/iterative-inquiry-synthesis/SKILL.en.md`
- `research/skill-prototypes/iterative-inquiry-synthesis/references/METHOD.en.md`
- `research/skill-prototypes/iterative-inquiry-synthesis/references/ROUND-TEMPLATE.en.md`

Research-only supporting assets:

- `evals/CASES.md`
- `evals/CSW-AFFINITY-HANDOFF-2026-09-07.md`

technical assetの翻訳状態とruntime / Method Definition parityは同一条件ではない。`P4-TECHNICAL-ASSET-LOCALIZATION-2026-09-07.json` が、英語packageで直接必要なtechnical assetとresearch-only資料の区別を記録する。

## 査読者へ伝える前提

### 1. public nameとresearch IDは別

Layer 1のresearch IDは `affinity-synthesis` のまま保存する。

production installable name候補は `material-led-synthesis` である。

```text
research history / research references: affinity-synthesis
production installable candidate:       material-led-synthesis
display term:                           Affinity Synthesis
```

英語文面の査読時に、research historyをpublic nameへ一括renameしない。

Layer 2はresearch ID / production candidateとも `iterative-inquiry-synthesis`。

### 2. KJ Methodの公式Skillではない

Layer 1はKJ法、関連する質的統合、親和的整理の系譜を受けているが、公式KJ Methodの認定実装・標準実装・完全再現とは称さない。

`KJ Method` / `KJ法` はlineage説明として必要な場所に残してよいが、Skill identityへ昇格させない。

### 3. 翻訳一致ではなくrealization parityを見る

語順や直訳一致より、次の方法的不変条件が英語版でも同じ判断を生むかを見る。

representation grammarとround templateについても、文章の逐語一致ではなく、runtimeから利用したときに意味境界・監査境界が変わらないことを確認する。

## Layer 1 必須不変条件

英語版は少なくとも次を失ってはならない。

1. **material-led**
   - 既成taxonomyを先に置かない。
   - metadata / provenanceを初期grouping geometryにしない。

2. **meaning-bearing boundary**
   - 機械的な最小単位化をしない。
   - 意味の一体性を守るときは結合する。
   - observation / interpretation、confirmed / inferred等、証拠状態が変わる境界では分ける。

3. **card / group / labelは同じ意味統合核を粒度違いで使う**
   - cardingを単なるsentence splittingとして説明しない。
   - labelをcategory nameへ薄めない。

4. **source-return correction**
   - unsupported causality
   - invented interior state
   - unsupported generalization
   - polarity / evaluation shift
   - confidence / evidence-state shift
   を元材料へ戻して点検する。

5. **residual preservation**
   - singleton
   - conflict
   - opposition
   - unexplained attention
   - unresolved relation
   - gap
   を「失敗だから消す」対象にしない。

6. **gap is not fact**
   - diagram/layoutから見えた空白は探索候補であり、対象について確認済みの欠落ではない。

7. **derived material is not independent repetition**
   - repost / derivative card / same-event duplicateを独立supportとして数えない。

8. **diagram ↔ narrative round trip**
   - proseで新しく生じたrelationはsource / mapへ戻す。
   - fluent narrationがdiagramよりunsupportedに滑らかにならない。

9. **representation distinction**
   - membership
   - semantic relation
   - secondary resonance
   - layout
   を混同しない。
   - `REPRESENTATION.en.md` が、`REPRESENTATION.md` にあるrelation read-back、questionable relation candidate、projection integrityの境界を弱めていない。

10. **no fixed success counts**
    - card数、group数、gap数、isolate数を成功quotaにしない。

## Layer 2 必須不変条件

英語版は少なくとも次を失ってはならない。

1. **delta-first reopening**
   - 新材料一件で全体を自動rebuildしない。
   - ただし全体前提を壊す反証ならlineageを辿ってglobal reopenを許す。

2. **stable semantic identity**
   - 文面が少し変わるたびに全artifactへ新IDを振らない。

3. **append-only history**
   - 過去roundを現在の問い・現在の結論に書き換えない。

4. **question shift is history, not failure**
   - inquiry変更を前roundの失敗として消さない。

5. **semantic delta != representation delta**
   - renderer / layout変更を世界についての新発見にしない。

6. **realization delta != material delta**
   - Skill実装A/Bの違いで生じた出力差を、新しい外部事実としてbankしない。

7. **resonance != duplicated membership**
   - secondary resonanceが見えたときcardを複製しない。

8. **normal stop with unresolved material**
   - gapゼロ・questionゼロを停止条件にしない。
   - 現在の目的に十分なら未解決とreopen conditionを残して止まれる。

9. **round count is budget, not quota**
   - max roundsを使い切ることを成功条件にしない。

10. **Layer 2 does not silently own Layer 1**
    - material synthesisが必要ならcompatible Layer 1 realizationを利用できる。
    - hard dependencyとして特定実装を絶対条件にしない。
    - Layer 1内部アルゴリズムをLayer 2へ再複製しない。
    - `ROUND-TEMPLATE.en.md` が、handoff capsuleを一括reopen命令や自動継続命令へ変えていない。

## Cross-layer査読

英語版を個別に正しいだけで終えず、次も見る。

```text
CSW
  cultural-framework exploration / attribution / return-to-target

Layer 1
  one-round material-led synthesis

Layer 2
  multi-round delta / reopen orchestration
```

確認点:

- CSWがLayer 1のgrouping algorithmを再所有していないか。
- Layer 1が文化体系の真偽判定を所有していないか。
- Layer 2がLayer 1を内部実装として吸収していないか。
- `framework_generated` materialがgrouping上の強い票になっていないか。
- synthesis resultだけでframework validityを独立検証したことになっていないか。

## 英語表現上の注意

### `affinity`

`affinity` をQCのAffinity Diagramと完全同義であるかのように書かない。

research Skill名は歴史的事情で `affinity-synthesis` だが、production candidate `material-led-synthesis` は、単純なAffinity Mappingより広い意味統合核を示すために選んでいる。

### `evidence state` / `epistemic state`

どちらを使う場合も、単なるconfidence scoreではなく、observation / interpretation / confirmed / inferred / hearsay等の**知識状態の違いを保存する境界**として読めること。

### `gap` / `blank`

KJ lineageの「空白」に近い意味を、単なるmissing data fieldへ縮めない。

ただし英語で `blank` が不自然な箇所は `gap`, `unresolved absence`, `missing relation candidate` 等へ文脈に応じて表現してよい。

### `cover and raise`

直訳語を守ること自体より、

- sourceからcoreを取る
- sourceを一時的に伏せる
- core間から統合文を立てる
- sourceへ戻して歪みを修正する

という操作が失われないことを優先する。

## Fail conditions

次のいずれかがあれば、production-readyとは判定しない。

- 日本語canonicalにない因果・規範・success quotaを英語版が追加している。
- `KJ Method`の公式／認定実装を示唆する。
- `affinity-synthesis`を単純theme clusteringだけへ縮めている。
- provenance fieldで先に分類してからgroupingするよう読める。
- isolate / conflict / gapを失敗として除去する。
- relation / resonance / layout / membershipを英語representation grammarが混同している。
- questionable relation candidateをreturn-checkなしにexplicit relationへ昇格させる。
- Layer 2が毎round global rebuildを要求する。
- `ROUND-TEMPLATE.en.md` がcarry-forward refを自動reopen対象へ変えている。
- stop条件として未解決ゼロを要求する。
- realization差をmaterial差として扱う。
- CSW / Layer 1 / Layer 2のownershipが再混合している。
- public name projectionとresearch historyの区別が消えている。

## 査読結果の最低記録

査読者は最低限、次を返す。

```text
reviewer:
reviewer relation / independence:
review date:
review scope:

Layer 1:
  semantic parity: pass | revise | blocked
  technical asset parity: pass | revise | blocked
  major issues:
  wording-only issues:

Layer 2:
  semantic parity: pass | revise | blocked
  technical asset parity: pass | revise | blocked
  major issues:
  wording-only issues:

Cross-layer ownership:
  pass | revise | blocked
  notes:

KJ lineage / naming:
  pass | revise | blocked
  notes:

Promotion recommendation:
  ready-for-next-gate | revise-before-next-gate | blocked

Reviewed target snapshot:
Reviewed commit / blob refs:
```

`pass` は英語realizationの独立査読gateだけに対する判定であり、production promotion全体の承認ではない。

## 査読後の処理

修正が必要なら英語draftを更新し、canonical Japaneseへ意味変更が逆流していないか確認する。

英語の方が方法的に明確な表現を見つけた場合も、日本語canonicalを自動修正しない。まずmethod-level issueとして分けて検討する。

査読完了後も、次のgateは別に残る。

- complete checkout上の `make research-skill-check`
- production sourceへのpromotion
- production adapter metadataへのpromotion
- `scripts/build.py` / validatorのmulti-skill一般化
- generated-artifact diff review
- release package内部composition validation
- canonical promotion直前のpublic-name最終再確認
