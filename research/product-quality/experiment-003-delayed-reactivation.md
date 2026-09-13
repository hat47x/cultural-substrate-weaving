# Experiment 003 — delayed reactivation

- experiment id: `PQ-E4-003`
- program: E4 — delayed reactivation
- status: protocol fixed before engineering Run 001
- protocol date: 2026-09-14
- source baseline: `develop/v0.5.0@810bc4a2a2d4db66693853474021756ec0c1e615`
- primary requirements: PQ-01, PQ-05, PQ-06, PQ-11, PQ-12

## 1. 問い

一度停止した調査・統合が、時間を置いて届いた新材料によって再開されるとき、前回までの理解を全面再生成せず、**新材料が実際に触れた意味構造だけを局所的に再開できるか**を確認する。

特に次を調べる。

1. 過去roundの問い・残差・stop reasonを後から書き換えないか。
2. stable semantic IDを、意味上の同一性が残る範囲で再利用できるか。
3. 未接触artifactを再検査済みの`=`として扱わないか。
4. 後着材料が旧残差を解いた場合、何が解け、何が残ったかを区別できるか。
5. 問いが変わる場合、旧問いを消さず、何が問いを動かしたかを追跡できるか。
6. 一度停止したことを失敗とみなさず、再開理由を新しい材料との接触として説明できるか。

この実験は、長期間の記憶保持性能そのものを測定するものではない。時間経過を模した**外部snapshotからの再開契約**を検査する。

## 2. 固定prior snapshot

対象は、小規模な公共図書館が初来館者向けの館内案内を見直している事例とする。

前回までの調査は2roundでいったん停止した。以下を、その時点で保存された外部artifactとして扱う。

### 2.1 Prior inquiry

> 初来館者が迷わず利用を始められるようにするには、説明情報を増やすべきか、減らすべきか。

### 2.2 Stable semantic artifacts

- `C01` — 初来館者の一部は、入口の長い案内を読む間に館内へ進めず、最初の行動開始が遅れる。
- `C02` — 繰り返し利用者の多くは、入口案内をほとんど読まず目的の棚へ向かう。
- `C03` — 職員は「説明を減らしすぎると、初来館者が不安になる可能性がある」と述べている。これは職員の見立てであり、初来館者本人への確認は不足している。
- `C04` — 閲覧席の照明については別調査が進んでおり、案内情報量との関係は現時点で確認されていない。
- `F01` — 文化体系を使った探索から、「入口を説明の集積点ではなく、館内へ移るための閾として扱う」という候補が生じた。`framework_generated`であり、対象側の独立supportではない。

### 2.3 Groups / relations

- `G01` — 「入口で情報を受け取ることが、行動開始と競合する場合がある」
  - members: `C01`, `C02`
- `G02` — 「初来館者には、情報量とは別に安心を支える何かが必要かもしれない」
  - members: `C03`
- `G03` — 「閲覧環境に関する別系統の課題」
  - members: `C04`
- `R01` — `G01 -> Q01` :: 「案内情報量と行動開始の関係を再検討させる」

`F01`は`G01`の独立supportとして数えない。探索上の候補として別に保持する。

### 2.4 Residuals / questions

- `U01` — 初来館者の「不安」が、説明不足によるものか、現在地・次行動が分からないことによるものかを区別できていない。
- `Q01` — 説明情報を増やす／減らすことのどちらが初来館者を助けるのか。
- `Q02` — 外国語利用者に同じ問題構造があるかは未調査。
- `P01` — 紙、サイン、スマートフォン、スタッフ案内のどれを採るかは図書館側の未決定事項。

### 2.5 Stop snapshot

前roundは次の理由で停止した。

- `U01`を判別できる初来館者本人の材料がない。
- `Q02`に答える外国語利用者の観察・聞き取りがない。
- `P01`は分析Methodが独立決定する事項ではない。
- 現材料だけでroundを続けても、意味のある構造変化を生む根拠がない。

stop reason:

> **Stop — 現在の問いをさらに判別できる新材料がなく、残差を残したまま一度閉じる。**

## 3. Delayed delta — 6週間後

前roundから6週間後に、次の材料だけが追加されたものとする。

- `D01` 初来館者8名への短い聞き取りで、5名が「詳しい説明がほしい」というより、「今どこにいて、次に何をすればよいか分かると安心する」と答えた。
- `D02` 入口の長文案内を変えず、主要ゾーンへ向かう一行の方向表示だけを追加した小規模観察では、初来館者が入口付近で立ち止まる時間が短くなった。サンプルは少なく、長期効果は未確認である。
- `D03` 外国語利用者3組の観察では、2組が日本語の入口案内を読まず、スマートフォンで館内図を探していた。理由の聞き取りは行っていない。
- `D04` 閲覧席の照明調査では、夕方の一部利用者からまぶしさの訴えがあった。案内情報量との関係を示す材料はない。

## 4. 実行指示

`iterative-inquiry-synthesis`または同じMethod Definitionを満たすcompatible realizationを使い、prior snapshotを上書きせず、新しいroundを追加する。

必要な場合だけcompatible one-round synthesisを使う。使わなかった処理を実行済みと称しない。

実行artifactには少なくとも次を外部化する。

1. current inquiry
2. delayed delta
3. reopened prior artifacts / touched semantic IDs
4. なぜそれらだけを再開したか
5. structural delta
6. carried but untouched artifacts
7. residuals
8. question shift
9. continuation boundary
10. 次roundへのhandoff

## 5. Must-pass invariants

- **L1 append-only history** — prior inquiry、prior artifact、stop reasonを後から書き換えない。
- **L2 touched-only reopen** — `D01`〜`D04`が実際に触れるprior artifactだけをreopenする。
- **L3 stable identity** — 意味上の同一性が残るartifactを、文言差だけで無理由に新IDへ振り直さない。
- **L4 carry != checked** — 未接触artifactを`=`（explicitly checked and unchanged）へ入れない。単なる持越しは`carry`等として区別する。
- **L5 residual accounting** — `U01`や`Q02`が解消・縮小・変形した場合、何が変わり、何がまだ未解決かを示す。
- **L6 question history** — 問いが変わる場合、旧`Q01`を消さず、新しい問いとの関係とshiftの原因を残す。
- **L7 provenance continuity** — `F01`を、後着target materialが似た方向を示したという理由だけで、最初からtarget-supportedだったものへ履歴改変しない。
- **L8 authority boundary** — `P01`を新材料から自動決定しない。
- **L9 no false continuity** — 6週間の経過を「継続中の同一round」と偽らず、停止後の再開として記録する。
- **L10 no domain self-certification** — この材料だけから、図書館案内として専門的に最適・全利用者に有効等を認証しない。

## 6. Diagnostic observations

must-passとは別に、次を見る。

- `U01`が、単純な「情報量」問題から「orientation / reassurance」問題へ変形するか。
- `Q01`を上書きせず、新しい問いを立てる方が自然か。
- `D03`が`Q02`を解くのではなく、観察対象を具体化する材料として働くか。
- `D04`が`G03`へ触れる一方、案内系のgroupを無理に再構築しないか。
- `F01`と`D01`/`D02`の方向が近くても、framework agreementを独立supportとして二重計上しないか。
- prior snapshotだけから再開する際の説明負荷。

これらを総合点にはしない。

## 7. Failure localization

failureがあれば、最初に崩れた場所を次から特定する。

1. prior snapshot interpretation
2. touched-artifact selection
3. one-round synthesis handoff
4. structural delta representation
5. question shift / continuation boundary
6. provenance / authority handling

upstream failureを下流で重複して数えない。

## 8. Run progression

### Run 001 — engineering trial

このprotocolを固定した後、同じconversation contextで実行して記録形式とfailure surfaceを確認する。

同一context自己評価であるため、passしても独立したbehavioral reliabilityの証拠とは扱わない。

### Run 002 — fresh restart

Run 001の出力を見ていないfresh contextへ、prior snapshot、delayed delta、現行Methodだけを渡す。評価は別contextまたは人間reviewへ分離する。

Run 001/002で同じfailureが再現した場合は、最小fixture化を検討する。

## 9. 結果から変更へ進む条件

- 既存Method契約で正しく扱えるが記録が曖昧なら、protocol / fixture / representationを直す。
- 既存Method契約では防げない再現failureがある場合だけ、Method変更候補にする。
- 単発passをproduction promotionやrelease readinessの根拠にしない。

この実験の目的は、時間を置いた再開でも「全部をもう一度考える」のではなく、**過去を保存したまま、今の材料が触れた意味だけを再び開けること**を検証可能にすることである。
