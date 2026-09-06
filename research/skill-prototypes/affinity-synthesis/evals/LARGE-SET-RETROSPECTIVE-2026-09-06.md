# Affinity Synthesis — 114-card Large-set Retrospective 2026-09-06

Status: **retrospective compatibility audit; not a blind rerun**

対象:
`ひとりぼっちの空_第二部_KJラウンド3D_114枚再統合・A型仮図_v1.md`

## 1. Why this audit

小ケースでは `affinity-synthesis` prototypeが意味単位、両義性、singleton、戻し検査を保持できた。

次に、現行KJ運用が114枚規模で実際に行った仕事を、分離後のMethod Definitionで表現できるかを見る。

既存結果をすでに読んでいるため、同じモデルで114枚を「blindに再KJした」評価ではない。現在の成果物を構造監査する。

## 2. Mechanical inventory check

Round 3Dの10島 A-J から `U001`〜`U114` を抽出して確認した。

- total placements: **114**
- unique card IDs: **114**
- missing U001-U114: **0**
- duplicate placements: **0**

したがって、このroundでは全カードがちょうど一つの主島へ配置されている。

これは整合した成果物である一方、`singletonがゼロだから成功／失敗`とは判定しない。現行Method Definitionの `Residual is not failure` と同様、singleton数を機械的評価値にしない。

## 3. Existing round already satisfies major Layer 1 invariants

### Cluster before naming

Round 3Dは、以前の12島を正解として保持せず114枚を再配置し、文化体系名、人物役割、七話、セフィロトを伏せてカードの訴えだけで表札を立てた。

これはprototypeの `cluster before naming` と一致する。

### Meaning-bearing labels

10島の表札は単純なカテゴリ名になっていない。

- A: 身体は「もっと」より先に、ここまでの量を知っている
- B: 器の口は相手側にあり、善意でも勝手に開けることはできない
- C: 力は消すのではなく、鞘と倫理を得て初めて遠くまで持ち運べる
- D: 言葉は正解を言うためでなく、切れた間にもう一度道を通す
- E: 背負うことは愛や使命とよく似た顔をして現れ、自分の羽まで削らせる
- F: 過去から未来へ進むには、水と人を運びながら形を変えられる乗り物が要る
- G: 休んだ場所から生まれたものは、自分を削らず他者へ渡せる形へ育つ
- H: 持続する中心は最大出力ではなく、自然に続く配置をつくる
- I: 二つは同じにならず、仮面も来歴も含めて一つの器に入る
- J: 器を得た後も、生活量と世界への影響は測り直し続けなければならない

いずれも島内部の動き・緊張を持つ。

### Return to source

各島に「表札を元材料へ戻したときの読み」があり、表札を分類名として置くだけでなく構成カードへ戻している。

prototypeの `return to source` は、この現行実践を短いSkill contractとして保持できている。

### Relational structure

10島は後段で二つの運動系列として配置される。

- 水: A → F → G → J
- 器: B → C → H → I
- D / Eが両系列を接続・緊張させる

ここでも「水＝感情」と一義化しないなど、関係図を固定symbol taxonomyへ変えない補正がある。

### Narrative / next projection

全体表札、人物化の条件、舞台原型、文化体系probeの優先度、次roundへ進む順序まで続く。

このうち、10島→関係構造→全体表札までがLayer 1、人物・舞台・framework probe・次round管理はLayer 2 / CSW / domain designへ分けられる。

## 4. Important large-set issue: one placement does not mean one meaning relation

機械監査では114枚が各1島にだけ配置されている。

しかし内容上、いくつかのカードは主島以外にも自然な響きを持つ。

例:

- U018「『有言実行』と言われ、約束のあとに力が返ってきた」
  - 主配置 A: 身体容量・力の戻り
  - secondary resonance D: 言葉が切れた間を通し直す

- U026「謝罪すると、薄かった子どもが腕にしがみついてきた」
  - 主配置 A: 身体反応
  - secondary resonance D: 謝罪と言葉による修復

- U072「妻が話し終えるまで待ち、夫は嫌そうでもホットミルクを運んだ」
  - 主配置 A: 待つ／身体へ温かいもの
  - secondary resonance D: 話し終えるまで待つ
  - secondary resonance G/H: 小さな生活行為・持続配置

- U057「大樹に小屋を作る前にも、はしごを掛ける前にも木へ聞いた」
  - 主配置 G: 育てる／作る
  - secondary resonance B: 内側へ入る前に聞く

このような多義性は、カードを複製して複数島へ数えるとfalse repetitionになる。一方、一つの島だけへ固定すると二次的な関係が見えにくくなる。

## 5. AI-era realization candidate: primary placement / secondary resonance

生成AI向けrealizationでは、必要な場合のみ次を区別する案が有力である。

### Primary placement

そのroundのworking geometryで、カードが最も強く寄る一つの束。

### Secondary resonance

カードを複製せず、別のgroup / relationにも響くことをcross-linkとして記録する。

```text
U072
  primary → A
  resonates → D, H
```

重要:

- secondary resonanceはカードの複製ではない。
- cluster sizeを増やさない。
- independent supportを増やさない。
- primary placementを必ず一つ持つこと自体もMethod Definitionの絶対条件にはしない。配置の都合があるrealizationで使う補助表現とする。

これはKJ法原典の固定手続きとして遡及帰属しない。大量・反復可能・graph表現可能なAI環境で、意味の多義性と二重計上防止を両立させる実装候補である。

## 6. Inherited / emergent / residual audit on the 114-card result

### Inherited

各島の具体カードと、そこから直接戻せる運動。

例:
- Bの「開ける前に聞く」「外側はよいが内側は嫌」「餌は受け取るが撫でられたくない」。
- Iの「きれい／眩しい」「白／ピンク」「仮面／自然な姿」。

### Emergent

複数島を配置した後に立つ、より大きな構造。

- `水` と `器` を二つの運動系列として読む。
- 器を「閉じ込めるもの」でなく、量・入口・鞘・移動・異質性・流出を扱う機能として読む。
- Dを水路、Eを「水が器を追い越す」緊張として読む。
- 全体表札を立てる。

これらは有用な創発であり禁止しない。ただし、各Uカードが最初から「水／器理論」を語っていたと書き換えない。

### Residual

現行成果物にも残っている。

- 人物へ島をまだ割り振らない。
- 舞台を実在地へ即決しない。
- 文化体系probeを後段へ送る。
- 水を単一の象徴へ固定しない。

`未決定であること` が次roundの材料条件を守っている。

## 7. Does the shorter prototype lose the listening stance?

静的比較では、現時点で重大な欠落は見つからない。

現行 `integration.md` の長い傾聴比喩が担っていた実行上の効果は、prototypeで次へ分解されている。

- cluster before naming
- meaning-bearing unit
- label as advocacy rather than class name
- source return
- disconfirming-card recheck
- temperature / scene / bodily detail preservation
- inherited / emergent / residual audit

したがって、比喩文を短くしたこと自体が方法核の消失にはなっていない。

ただし、低能力モデルで同じ効果が出るかは未検証である。必要ならreferenceに「listening stance」の長い説明を残し、runtime Skillからprogressive loadする方が、全モデルへ長文を常時読ませるよりよい可能性がある。

## 8. New prototype changes justified by this audit

### Candidate A — optional secondary resonance

採用候補。Method coreではなくAgent Skill realizationの補助機能として入れる。

### Candidate B — group coherence should identify borderline members

各表札の戻し検査時に、

> このカードはこのgroupの表札へ本当に答えているか。それともsecondary resonanceとして置いた方が意味を保てるか。

を見る。

### Candidate C — zero singleton is not a failure

114枚がすべて一つの主島へ配置されても、それ自体では失敗判定しない。ただし、全カードが綺麗に収まった場合ほどborderline membershipを再確認する。

## 9. Decision

**Large-set retrospective: PASS with realization-level refinement.**

Layer 1分離を止める問題は見つからなかった。

次にprototypeへ入れる価値があるのは、`primary placement / secondary resonance` と、戻し検査時のborderline-member checkである。

Runtime CSW sourceの削減は、dependency / fallback設計と、この refinement のfixture追加後に行う。
