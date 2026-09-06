# Research Skill Suite — 参照資料の役割分類

Status: research contract

この文書は、`affinity-synthesis` / `iterative-inquiry-synthesis` / thin `cultural-substrate-weaving` の分離研究において、**何がAgent runtimeの実行契約で、何が研究・検証・表現上の補助資料なのか**を区別する。

目的は、英語realizationを追加したときに、日本語の研究記録が未翻訳であるという理由だけで英語runtimeが不完全になることを避ける一方、未翻訳資料を英語runtimeの暗黙の指示として扱わないことである。

## 1. Runtime contract

Agentがそのlocaleで方法を実行するために必要な規範的内容。

### cultural-substrate-weaving

- `src/ja-JP/ROUTER.md` と参照される日本語runtime modules: semantic canonical runtime
- `src/en-US/ROUTER.md` と対応runtime modules: English translated runtime

### affinity-synthesis

- Japanese research runtime: `affinity-synthesis/SKILL.md`
- Japanese Method Definition: `affinity-synthesis/references/METHOD.md`
- English research runtime: `affinity-synthesis/SKILL.en.md`
- English Method Definition: `affinity-synthesis/references/METHOD.en.md`

### iterative-inquiry-synthesis

- Japanese research runtime: `iterative-inquiry-synthesis/SKILL.md`
- Japanese Method Definition: `iterative-inquiry-synthesis/references/METHOD.md`
- English research runtime: `iterative-inquiry-synthesis/SKILL.en.md`
- English Method Definition: `iterative-inquiry-synthesis/references/METHOD.en.md`

英語runtimeは、未翻訳の日本語research proseを追加指示として読むことを前提にしない。英語版 `SKILL.en.md` と `METHOD.en.md` の範囲で中核契約が自己完結することを優先する。

## 2. Optional technical / representation assets

方法の実行を補助するが、Method Definitionそのものではない。

例:

- `affinity-synthesis/references/REPRESENTATION.md`
- `affinity-synthesis/references/HIERARCHY-AND-LINEAGE.md`
- `affinity-synthesis/references/affinity-map.schema.json`
- `affinity-synthesis/references/TEMPLATE.md`
- `iterative-inquiry-synthesis/references/ROUND-TEMPLATE.md`
- representation renderer / validator scripts

これらは、表現・交換・監査・作業効率のためのassetである。

- JSON schemaやnotationのように実質的に言語非依存な部分はlocale間で共有してよい。
- 日本語説明を含むassetは、英語runtimeがそれを理解していることを前提にしない。
- 英語利用者にそのassetを直接使わせる場合は、必要箇所を英訳するか、英語runtime内に必要契約を埋め込む。
- representation変更だけでMethod Definitionを変更したことにしない。

## 3. Evidence / lineage material

方法の由来、既存Skill比較、一次・二次資料調査、KJ系譜の持越し判断など。

例:

- `affinity-synthesis/evidence/`
- maintainer review documents
- external-skill comparison records

これは**方法の根拠や設計判断を監査する研究資料**であり、Agentが毎回読むruntime instructionではない。

英訳は公開説明や外部査読には有益だが、英語Skillを実行するための必須依存にはしない。

## 4. Evaluation fixtures / application records

実装・realizationがMethod Definitionの不変条件を保つか検査するための資料。

例:

- `affinity-synthesis/evals/`
- `iterative-inquiry-synthesis/evals/`
- cross-layer paired runs
- representation scale checks

これらは**方法の妥当性や回帰を検査するためのfixture / record**であり、通常runtimeの作業手順ではない。

ただし公開promotionでは、少なくとも重要fixtureが英語realizationにも適用可能かを確認する。fixture本文をすべて英訳することと、英語realizationが同じ不変条件を満たすことは別の条件である。

## 5. Migration / maintainer material

分離前後の責務移動、削除監査、生成物同期、release判断などの開発資料。

例:

- `research/skill-prototypes/migration/`
- `docs/ja/maintainers/`

Agent runtimeへ読み込ませない。過去の移行判断を現在のMethod Definitionより上位の規則として扱わない。

## 6. Locale parityの扱い

locale parityを一つのbooleanへ潰さない。

少なくとも次を別に見る。

1. **CSW runtime parity** — `src/ja-JP` と `src/en-US` の責務・意味対応。
2. **Sibling Skill runtime parity** — `SKILL.md` / `SKILL.en.md` が同じMethod境界を実行できるか。
3. **Method Definition parity** — `METHOD.md` / `METHOD.en.md` が同じ不変条件を保持するか。
4. **Technical asset localization** — template / representation prose等が対象localeで直接利用可能か。
5. **Research-material localization** — evidence / eval / migration文書の翻訳状態。
6. **Independent review** — 翻訳が意味を保つことを独立に確認したか。

1〜3が揃っても、4〜6が未完であれば `translated draft` として扱える。逆に、研究記録を大量に英訳してもruntime / Method Definitionの意味対応が崩れていればparityとはしない。

## 7. Public promotion rule

公開Skillまたはmulti-skill distributionへ昇格する前に、少なくとも次を満たす。

- runtime contractが対象localeで自己完結する。
- Method Definitionが対象localeで追跡できる。
- runtimeが必要とするtechnical assetは対象localeで使用可能、または言語非依存である。
- untranslated research-only materialを、実行に必要なKnowledge / instructionsとして暗黙依存させない。
- 同じ重要regression fixtureをlocale間で適用できる。
- independent review未実施なら、その状態を明示し、査読済みと称しない。

この分類は、翻訳量を増やすための規則ではない。**実行契約・方法定義・表現技術・研究根拠を混同しないための境界**である。
