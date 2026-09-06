# KJ系技能分離 — 移管監査

作成日: 2026-09-06

Status: research migration map; runtime source not yet changed

## 目的

現行 `src/ja-JP/methods/integration.md` と `src/ja-JP/core/iteration.md` に混在する責務を、次の三層へ割り当てる。

1. `affinity-synthesis`: 一回の材料統合。
2. `iterative-inquiry-synthesis`: 複数roundの差分・再開・停止管理。
3. `cultural-substrate-weaving`: 文化体系を認知場として探索へ投入し、由来と帰属を保って対象へ返す。

この文書は「似た文章を別Skillへコピーする」ためではない。**どこを一つの正本にし、どこを接続契約だけへ縮めるか**を決めるための監査である。

## A. `integration.md` の移管

| 現行責務 | 移管先 | CSW側に残すもの | 判定 |
|---|---|---|---|
| KJ法・親和図法・質的統合法の系譜説明 | affinity-synthesis evidence / METHOD | 外部Skillとの接続説明だけ | 移管 |
| 断片を分類対象ではなく訴えとして聴く | affinity-synthesis | 対象により自分の読みを修正可能にする一般姿勢はCSW coreにも残り得る | 分有するが文面重複は避ける |
| 流暢な言い換えによる上書き警告 | affinity-synthesis | 文化体系語彙による上書き防止というCSW固有形だけ | 一般形を移管 |
| 理由の言えない注意を残す | affinity-synthesis | 文化体系由来の違和感ならprovenanceを保持 | 移管 |
| 対立・両義性を早期に均さない | affinity-synthesis | framework-generated対立の帰属だけ | 移管 |
| カードを弱めた場合の損失記録 | affinity-synthesis | 文化体系由来候補のde-binding等はCSW | 一般形を移管 |
| カード化・表札化・上位統合は同じ意味統合核 | affinity-synthesis METHOD | なし | 完全移管 |
| 意味の一体性 vs 証拠状態の境界 | affinity-synthesis METHOD | CSW固有seam: canonical source vs derived correspondence | 一般形を移管 |
| 核を抜く→伏せる→立てる→戻す | affinity-synthesis realization | なし | 完全移管 |
| 元にない因果・内面・一般化・評価方向・確度変更の検査 | affinity-synthesis | framework attribution誤昇格の検査だけCSW | 一般形を移管 |
| source provenance / discovery route / derivation | affinity-synthesis METHOD | cultural source / correspondence / routing authority の固有来歴 | 共通基盤は移管、CSW拡張を残す |
| provenanceをgrouping geometryにしない | affinity-synthesis | cultural frameworkをKJ分類軸にしない、という接続契約 | 移管＋接続 |
| 派生・転載の二重計上防止 | affinity-synthesis | framework-derived candidateの派生関係 | 一般形を移管 |
| 束ねる / singleton保持 | affinity-synthesis | なし | 完全移管 |
| 表札 | affinity-synthesis | なし | 完全移管 |
| 配置 / 空白 | affinity-synthesis | 文化体系が空白を埋めたと誤認しない契約 | 一般形を移管 |
| 叙述 / Map↔Narrative戻し | affinity-synthesis | CSW成果物へ反映するときのattribution | 一般形を移管 |
| 一回の統合後、次に何を調べるか | iterative-inquiry-synthesis | 文化体系を探索経路として選ぶ部分のみCSW | 分離 |

## B. `core/iteration.md` の移管

| 現行責務 | 移管先 | CSW側に残すもの | 判定 |
|---|---|---|---|
| 基本単位をroundとして扱う | iterative-inquiry-synthesis | CSWはround内のoptional exploration route | 移管 |
| 新材料差分を受け取る | iterative-inquiry-synthesis | なし | 移管 |
| 関係する古い残差だけreopenする | iterative-inquiry-synthesis | framework correspondence residualも同じ契約へ乗せる | 移管 |
| 今回の問いを見る | iterative-inquiry-synthesis | 文化体系が問いを生んだ場合の由来 | 移管＋attribution |
| 必要なら文化体系を開く | CSW | activation / preview / full 等 | CSW固有 |
| 文化体系から生じた問い・仮説をKJへ返す | CSW→iteration/affinity bridge | attribution vocabulary | CSW接続契約 |
| 実作業へ採用する | caller/domain | CSWは採否決定権を所有しない | 外へ出す |
| round境界・残差・再開条件 | iterative-inquiry-synthesis | なし | 移管 |
| 新材料が来ただけで既存島を壊さない | iterative-inquiry-synthesis + affinity-synthesis | なし | 汎用化 |
| 古い残差を背景化/reopen | iterative-inquiry-synthesis | framework residualも同じ契約へ載せる | 移管 |
| 問いと確認方法を次材料へつなぐ | iterative-inquiry-synthesis | framework内導出と対象側証拠を混同しない点はCSW | 移管＋固有seam |
| event記録 | generic governance / iterative realization | `framework_contact_change`だけCSW vocabulary | 要再配置 |
| 現状把握→問題提起→本質追及… | iterative-inquiry-synthesisの任意question lens | KJ coreからは外す | 移管 |
| 収束と再開 | iterative-inquiry-synthesis | 文化体系利用量を完了条件にしない点はCSWにも残す | 移管＋接続 |

## C. CSWに残る固有核

分離後のCSWは「KJ法と文化体系を組み合わせる巨大Skill」ではなく、次に集中する。

### C1. Cultural framework as cognitive field

文化的・哲学的・伝統的体系を答えや分類器ではなく、対象へ別の位置・関係・状態・遷移・周期・境界を問い返す認知場として使う。

### C2. Activation and progressive loading

`not_loaded / probe / preview / full / enacted` 等、体系をどこまで開くかを扱う。

### C3. Attribution boundary

少なくとも次を混同しない。

```text
canonical cultural source
    != derived correspondence
    != exploration routing authority
    != target-supported finding
```

### C4. Return to target

framework-generatedな問い・対応・構成候補を、そのまま対象所見へ昇格させず、対象材料へ返す。

### C5. Multi-framework exploration

複数体系の利用、体系間の緊張、候補想起、探索／帰属利用の区別を扱う。

### C6. Specialized cultural/body domains

Taiheki等、CSW固有のframework moduleを必要に応じて扱う。

## D. CSW Router の将来形

現行Routerは「二つの能力を組み合わせる」として、文化体系探索とKJ統合を同じSkill内部能力としている。

分離後は次の形へ変える候補が自然である。

```text
cultural-substrate-weaving
  owns:
    cultural-framework exploration
    activation / attribution / return-to-target

  may call:
    affinity-synthesis
    iterative-inquiry-synthesis
    domain skill / research tool
```

CSWが他Skillを必須dependencyにするか、利用可能なら委譲し不在時は最小fallbackを持つかは、paired evaluation後に決める。

## E. まだruntime sourceを削らない理由

現段階では `src/` を変更しない。

理由:

1. prototype realizationが実タスクで現行 `integration.md` と同等以上に意味を保存できるか未比較である。
2. Layer 1 / Layer 2へ分けたことで、旧 `integration.md` 内の暗黙の往復が失われる可能性がある。
3. CSWが独立Skillへの依存をどう宣言するかはAgent Skill実装ごとの差がある。
4. 日本語正本だけ先に削ると、既存adapter / translation / build contractを壊す。

したがって次のゲートを通過後にruntime分離へ進む。

## F. Runtime migration gates

- [ ] affinity-synthesis prototypeが方法fixtureを満たす。
- [ ] 現行CSW `integration.md` と実タスクでpaired comparisonを行う。
- [ ] narrower Affinity Mapping Skillとの委譲境界を実タスクで確認する。
- [ ] iterative-inquiry-synthesisへ分けてもround handoffの情報損失がない。
- [ ] CSWからLayer 1を外しても、framework attributionとreturn-to-targetが壊れない。
- [ ] Agent Skill dependency / fallback方針を決める。
- [ ] ja-JP / en-US / translation manifest / build adapterの変更単位を決める。
- [ ] `make check`相当の全検査を通す。

## G. 重要な設計原則

分離後も次を守る。

> **KJ法の名前を避けるために方法を薄くしない。**

> **生成AI向け拡張をKJ法そのものへ遡及帰属しない。**

> **Skillを分けるために認知操作まで別物に分断しない。**

Layer 1内部では、カード化・表札化・上位統合は同じ意味統合核として保つ。Layer 2はその核を複数roundで呼び出すだけであり、別の意味統合アルゴリズムを再実装しない。
