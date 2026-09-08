# Research Skill Suite — 参照資料の役割分類

Status: research contract

この文書は、`affinity-synthesis` / `iterative-inquiry-synthesis` / thin `cultural-substrate-weaving` の分離研究において、**何がAgent runtimeの実行契約で、何が研究・検証・表現上の補助資料なのか**を区別する。

目的は、英語realizationを追加したときに、日本語の研究記録が未翻訳であるという理由だけで英語runtimeが不完全になることを避ける一方、未翻訳資料を英語runtimeの暗黙の指示として扱わないことである。

## 1. Runtime contract

Agentがそのlocaleで方法を実行するために必要な規範的内容。

### cultural-substrate-weaving

- `src/ja-JP/ROUTER.md` と参照される日本語runtime modules: semantic canonical runtime
- `src/en-US/ROUTER.md` と対応runtime modules: English translated runtime

CSWでは、対象と文化体系の一致だけでなく、不一致・抵抗・相互修正から第三構造が生じるかを見る原則もruntime contractに属する。これは一般的なLayer 1 synthesis algorithmではなく、文化体系との接触と帰属を所有するCSW固有の認知契約である。

### affinity-synthesis

- Japanese research runtime: `affinity-synthesis/SKILL.md`
- Japanese Method Definition: `affinity-synthesis/references/METHOD.md`
- English research runtime: `affinity-synthesis/SKILL.en.md`
- English Method Definition: `affinity-synthesis/references/METHOD.en.md`

Layer 1はmaterial-led one-round synthesisを所有するが、CSW固有の`target-framework tension / sublation`を方法上の必須原理として所有しない。

### iterative-inquiry-synthesis

- Japanese research runtime: `iterative-inquiry-synthesis/SKILL.md`
- Japanese Method Definition: `iterative-inquiry-synthesis/references/METHOD.md`
- English research runtime: `iterative-inquiry-synthesis/SKILL.en.md`
- English Method Definition: `iterative-inquiry-synthesis/references/METHOD.en.md`

英語runtimeは、未翻訳の日本語research proseを追加指示として読むことを前提にしない。英語版 `SKILL.en.md` と `METHOD.en.md` の範囲で中核契約が自己完結することを優先する。

## 2. Optional technical / representation assets

方法の実行を補助するが、Method Definitionそのものではない。

### affinity-synthesis

- `affinity-synthesis/references/REPRESENTATION.md`
- `affinity-synthesis/references/REPRESENTATION.en.md`
- `affinity-synthesis/references/HIERARCHY-AND-LINEAGE.md`
- `affinity-synthesis/references/affinity-map.schema.json`
- `affinity-synthesis/references/TEMPLATE.md`
- representation renderer / validator scripts

英語runtimeは `REPRESENTATION.en.md` を直接参照する。`affinity-map.schema.json` は言語非依存assetとしてlocale間で共有する。

### iterative-inquiry-synthesis

- `iterative-inquiry-synthesis/references/ROUND-TEMPLATE.md`
- `iterative-inquiry-synthesis/references/ROUND-TEMPLATE.en.md`

英語runtimeは `ROUND-TEMPLATE.en.md` を直接参照する。

これらは、表現・交換・監査・作業効率のためのassetである。

- JSON schemaやnotationのように実質的に言語非依存な部分はlocale間で共有してよい。
- 日本語説明を含むassetは、英語runtimeがそれを理解していることを前提にしない。
- 英語利用者にそのassetを直接使わせる場合は、必要箇所を英訳するか、英語runtime内に必要契約を埋め込む。
- representation変更だけでMethod Definitionを変更したことにしない。
- technical assetの翻訳状態は `P4-TECHNICAL-ASSET-LOCALIZATION-2026-09-07.json` で追跡する。

## 3. Evidence / lineage material

方法の由来、既存Skill比較、一次・二次資料調査、KJ系譜の持越し判断など。

例:

- `affinity-synthesis/evidence/`
- `iterative-inquiry-synthesis/evidence/`
- maintainer review documents
- external-skill comparison records

Layer 2の `iterative-inquiry-synthesis/evidence/dossier.md` は、autoresearch / autonomous-research-loop / systematic-search系Skillとの比較から、goal、append-only ledger、recovery、evidence refs、stop boundary等を選択的に採用し、mandatory scalar metric、autonomous-until-budget、universal search backlog等をMethod不変条件にはしない判断を残す。

これは**方法の根拠や設計判断を監査する研究資料**であり、Agentが毎回読むruntime instructionではない。

ただし、**research / evaluation artifactであることと、packageへ絶対に含めないことは同義ではない**。あるAgent Skill realizationが、そのartifactを「必要時だけ読むprogressive support」として `SKILL.md` から直接参照する場合、そのlocaleではpackage reference closureを満たすために同梱してよい。これはそのartifactをMethod Definitionへ昇格させることも、毎回読むruntime instructionへ変えることも意味しない。

現在の具体例は次である。

- Layer 1 Japanese: `SKILL.md` が `evals/CASES.md` と `evidence/dossier.md` をoptional progressive referenceとして直接参照するため、research packageでは同梱する。
- Layer 1 English: `SKILL.en.md` は日本語eval/evidenceを参照しないため、それらをlocale parityの名目で自動同梱しない。
- Layer 2 Japanese / English: external-loop comparison dossierはMethod設計のresearch evidenceとしてsuite manifestで追跡するが、runtime Skillから参照しないためpackage dependencyにはしない。

したがって、package inclusionはartifact分類だけで決めず、**そのlocale realizationの明示的runtime reference closure**と合わせて決める。

英訳は公開説明や外部査読には有益だが、英語Skillを実行するための必須依存にはしない。

## 4. Evaluation fixtures / application records

実装・realizationがMethod Definitionの不変条件を保つか検査するための資料。

例:

- `affinity-synthesis/evals/`
- `iterative-inquiry-synthesis/evals/`
- cross-layer paired runs
- representation scale checks
- `evals/CSW-TENSION-AND-SUBLATION-CASES-2026-09-07.md`

`CSW-TENSION-AND-SUBLATION-CASES-2026-09-07.md` は、文化体系を都合のよい説明へ使わず、対象との不一致・抵抗から情報が立つこと、第三構造を強制しないこと、Layer 1へ弁証法的stage modelを移さないことを検査するsuite-level fixtureである。

これらは**方法の妥当性や回帰を検査するためのfixture / record**であり、通常runtimeの作業手順ではない。

ただし公開promotionでは、少なくとも重要fixtureが英語realizationにも適用可能かを確認する。fixture本文をすべて英訳することと、英語realizationが同じ不変条件を満たすことは別の条件である。

## 5. Migration / maintainer material

分離前後の責務移動、削除監査、生成物同期、release判断などの開発資料。

例:

- `research/skill-prototypes/migration/`
- `docs/ja/maintainers/`
- `P4-CSW-TENSION-TRANSLATION-STATUS-2026-09-07.md`

Agent runtimeへ読み込ませない。過去の移行判断を現在のMethod Definitionより上位の規則として扱わない。

translation status記録は、英語本文が存在することと、`i18n/translation-manifest.json` のbyte-level source hashが更新済みであることを混同しないためのmaintainer recordである。

## 6. Locale parityの扱い

locale parityを一つのbooleanへ潰さない。

少なくとも次を別に見る。

1. **CSW runtime parity** — `src/ja-JP` と `src/en-US` の責務・意味対応。
2. **Sibling Skill runtime parity** — `SKILL.md` / `SKILL.en.md` が同じMethod境界を実行できるか。
3. **Method Definition parity** — `METHOD.md` / `METHOD.en.md` が同じ不変条件を保持するか。
4. **Technical asset localization** — representation grammar / round template等が対象localeで直接利用可能か。
5. **Research-material localization** — evidence / eval / migration文書の翻訳状態。
6. **Independent review** — 翻訳が意味を保つことを独立に確認したか。
7. **Translation-manifest hash parity** — canonical Japanese bytesと英訳追跡manifestが現在のsourceへ同期しているか。

Method Definition parityについては、numbered invariant surfaceの静的checkを補助的に使える。これは重要節の欠落を検出するが、自然な英訳や意味の独立査読を代替しない。

1〜4が揃っても、5〜7が未完であれば `translated draft` として扱える。逆に、研究記録を大量に英訳してもruntime / Method Definitionの意味対応が崩れていればparityとはしない。

## 7. Public promotion rule

公開Skillまたはmulti-skill distributionへ昇格する前に、少なくとも次を満たす。

- runtime contractが対象localeで自己完結する。
- Method Definitionが対象localeで追跡できる。
- runtimeが必要とするtechnical assetは対象localeで使用可能、または言語非依存である。
- untranslated research-only materialを、実行に必要なKnowledge / instructionsとして暗黙依存させない。
- 同じ重要regression fixtureをlocale間で適用できる。
- independent review未実施なら、その状態を明示し、査読済みと称しない。
- canonical Japaneseを変更した場合、translation-manifestのsource hashを正規の更新scriptで再計算する。

この分類は、翻訳量を増やすための規則ではない。**実行契約・方法定義・表現技術・研究根拠を混同しないための境界**である。
