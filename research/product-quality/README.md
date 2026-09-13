# Product Quality Research

このディレクトリは、CSWの**プロダクト品質を観測・検証するための監査記録と制御実験**を置く場所です。

方法論そのものの意味上の正本ではありません。日本語の方法論正本は`src/ja-JP/`、research prototypeの機械可読な契約は`research/skill-prototypes/`にあります。

## ここに置くもの

- 現行品質証拠のcoverage audit
- 制御されたbehavioral experimentのprotocol
- experiment runの観測記録
- 既知failureから切り出した回帰候補
- quality requirementと証拠の対応記録

## ここに置かないもの

- 新しい方法論規則の第二正本
- AI自己採点だけで成立する「品質スコア」
- Living Labの自然利用記録のコピー
- production promotionを自動承認する判定

## 証拠の扱い

品質証拠は最低限、次を区別します。

1. **static / deterministic evidence** — repository contract、validator、schema、生成物一致など
2. **controlled behavioral evidence** — 固定packetと不変条件を用いたモデル実行
3. **natural-work evidence** — Living Lab等の自然な実作業から得た観測
4. **interpretation** — 人間・AI・外部評価者による解釈

static checkが通ったことをモデル行動の保証とみなさず、単発の良いモデル出力を方法論全体の有効性ともみなしません。

## 命名

- 監査: `YYYY-MM-DD-<topic>-audit.md`
- 実験protocol: `experiment-NNN-<topic>.md`
- 実行記録: `experiment-NNN-run-YYYY-MM-DD[-suffix].md`

実行記録では、可能な限りsource commit、visible model / product mode / tools、入力packet、出力artifact、must-pass invariant、diagnostic observation、評価者の来歴を残します。

## 現在の入口

- [`2026-09-11-quality-evidence-audit.md`](2026-09-11-quality-evidence-audit.md) — E0: 現行品質証拠の初回監査
- [`experiment-001-handoff-integrity.md`](experiment-001-handoff-integrity.md) — E3: CSW → affinity synthesis → iterative inquiryのhandoff integrity protocol
- [`experiment-001-run-2026-09-11-engineering.md`](experiment-001-run-2026-09-11-engineering.md) — E3 Run 001: 同一contextでのengineering trial
- [`experiment-001-run-002-execution-packet.md`](experiment-001-run-002-execution-packet.md) — E3 Run 002: fresh execution側へ渡す固定packet
- [`experiment-001-run-002-evaluation-sheet.md`](experiment-001-run-002-evaluation-sheet.md) — E3 Run 002: execution後に別contextまたは人間が使う評価sheet
- [`experiment-002-authority-provenance-adversarial.md`](experiment-002-authority-provenance-adversarial.md) — E1: authority / provenance adversarial probe
- [`experiment-002-run-2026-09-14-engineering.md`](experiment-002-run-2026-09-14-engineering.md) — E1 Run 001: 同一contextでのengineering trial
- [`experiment-003-delayed-reactivation.md`](experiment-003-delayed-reactivation.md) — E4: stop snapshotからのdelayed reactivation protocol
- [`experiment-003-run-2026-09-14-engineering.md`](experiment-003-run-2026-09-14-engineering.md) — E4 Run 001: 外部snapshotからの局所再開engineering trial
- [`../../docs/ja/maintainers/product-quality-program.md`](../../docs/ja/maintainers/product-quality-program.md) — 品質要件・検証層・実験ポートフォリオ全体

## 現在の実験状態

### E3 — split-method handoff integrity

Run 001ではH1〜H6を外部artifactとして検査でき、明白なMethod contract違反は観測されませんでした。ただしprotocol作成・実行・評価が同じAI contextにあるため、behavioral reliabilityの強い証拠とは扱いません。

Run 001から得た具体的なprotocol補正は、`carried-untouched`と`=`（touched and explicitly checked, but semantically unchanged）を分けることです。

Run 002は、execution packetとevaluation sheetを分離した状態まで準備しました。**このrepository作業を行っている現在の会話ではfresh executionにならないため、まだ実行していません。** 次の実行では、executorへexecution packetと現行Skill / Methodだけを渡し、Run 001 outputとevaluation sheetを見せない状態で生成したartifactを、別contextまたは人間が評価します。

### E1 — authority / provenance adversarial probe

2026-09-14に固定packetを作り、engineering Run 001を実施しました。依頼文から「framework由来候補を調査根拠として扱う」「最適案を決定してそのまま公開する」という圧力を加えましたが、このrunではA1〜A6の明白な境界違反は観測されませんでした。

一方、このrunもprotocolを知った同一AI・同一contextで実行・評価しているため、独立したbehavioral reliabilityの証拠とは扱いません。

診断上は、`target_supported / framework_generated`等の**origin**と、`公開前要承認`等の**delivery / approval state**を外部artifact上で別々に見せると監査しやすいことを確認しました。現行CSWには「来歴ラベルは外部化許可を自動決定しない」という契約がすでにあるため、この結果だけでruntime ruleは追加していません。

### E4 — delayed reactivation

2026-09-14に、prior inquiry、stable semantic ID、residual、author-pending、stop reasonを固定したsnapshotから、6週間後を模したdeltaだけで再開するprotocolを追加し、engineering Run 001を実施しました。

このrunではL1〜L10の明白な契約違反は観測されませんでした。特に次を外部artifactで区別できました。

- 旧`Q01`を履歴として残し、新しい問い`Q03`を追加するquestion shift
- deltaが触れたartifactだけのreopen
- 未接触`C02`のcarryと、明示的に再検査した`=`の分離
- `F01`のframework由来履歴と、後から得たtarget-side supportの分離
- 残差を残したまま再びstop / handoffできるcontinuation boundary

診断上は、問いのshiftをcompact deltaへ無理に押し込まず`Question Shift`欄を使うこと、またprior artifactだけでなく**prior stop reason**をsnapshotへ残すことが再開品質の監査に有効でした。どちらも現行`iterative-inquiry-synthesis`の契約ですでに表現できるため、Method Definitionは変更していません。

このrunの「6週間後」は合成packet上の設定です。実時間をまたいだモデル記憶性能やfresh-context再現性の証拠ではありません。

## 次に強める証拠

独立性を必要とするrunは、この会話の中で擬似的に済ませません。並行して、同一contextでも設計・記録形式を検証できるengineering trialは進めます。

1. **E3 Run 002** — fresh execution / separate evaluationを実施する。
2. **E1 independent rerun** — engineering Run 001の出力を見せず、別contextまたは別評価者でauthority / provenance圧力を再現する。
3. **E4 Run 002** — Run 001の出力を見ていないfresh contextから同じstop snapshotを再開し、別評価者がL1〜L10を確認する。
4. 上記で同じfailureが再現した場合は最小fixtureへ落とす。再現failureがなければ、次のengineering workとしてE2 activation calibrationを進める。

この順序はrelease gateではありません。重大なnatural-work failureが見つかった場合は、その再現とfixture化を優先します。

## 改善へ反映するとき

観測からruntimeや正本を変える場合は、先にfailure modeを明示します。既存規則の言い換えで済むのか、fixture追加で済むのか、実際に方法の変更が必要なのかを分けます。

重大なfailureが再現できる場合は、まず再現packetを最小化し、可能なら回帰fixtureへ落とします。実験で良い結果が出たことだけを理由にresearch prototypeのpromotion gateを迂回しません。
