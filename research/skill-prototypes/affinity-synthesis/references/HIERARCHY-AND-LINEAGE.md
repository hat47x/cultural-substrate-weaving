# Recursive Grouping and Lineage Projection

Status: research candidate

## 1. Why this layer exists

親和統合では、カードから一次の島を作って終わるとは限らない。

一次の島同士から、さらに上位の意味単位が立つことがある。また、A型的な関係配置からB型的な叙述へ移った後、その文章がどのカード・島・関係から立ったかを戻して確かめる必要がある。

この文書は、その二つを表現層で扱う。

- **recursive grouping** — card / lower group を、さらに higher-order group のmemberにできる。
- **lineage projection** — source → card → group → higher group / relation → narrative の来歴を、必要な解像度で表示する。

方法の目的は深い階層を作ることではない。材料から上位の意味単位が立たなければ、一層のままでよい。

## 2. Recursive grouping

### 2.1 Group can contain cards or groups

```text
G01["一次表札"] := {C001, C002, C003}
G02["別の一次表札"] := {C004, C005}

G10["上位表札"] := {G01, G02}
```

必要ならcardとlower groupを同じ上位groupへ置くこともできる。

```text
G11["上位表札"] := {G01, G02, C019}
```

これは「G01/G02/C019は同じ種類である」という分類宣言ではない。現在の統合粒度で、それらが共同して一つの意味単位を成立させるというmembershipである。

### 2.2 No forced depth

- 最終group数を固定しない。
- 上位階層数を固定しない。
- すべての一次groupを必ず上位groupへ入れない。
- 二つの上位系列へ綺麗に入らない重要groupを、どちらかへ無理に押し込まない。

上位groupへ入らないものが、より上の全体groupへ直接参加してもよい。

### 2.3 No membership cycles

次は禁止する。

```text
G10 := {G11}
G11 := {G10}
```

上位統合は可逆的に辿れるDAGとして保持する。循環はsemantic relationで表すのであって、membershipで表さない。

### 2.4 Higher-order membership is not an explicit relation

```text
G10 := {G01, G02}
```

から、次を自動生成しない。

```text
R?: G01 -> G02
```

同じ上位groupに入ることと、二つのgroup間に方向・因果・緊張・条件等のrelationがあることは別である。

逆に、relationがあるから同じ上位groupへ入るとも限らない。

## 3. Canonical label and display label

上位表札は長くなりやすい。

意味の正本と図表示を分ける。

```json
{
  "id": "G10",
  "label": "材料の意味を保持する完全な上位表札",
  "display_label": "図用の短い表札",
  "members": ["G01", "G02"]
}
```

`display_label` はprojection用であり、短縮された語をcanonical `label`へ逆流させない。

## 4. Narrative lineage

### 4.1 Narrative is an auditable output artifact

B型的な文章化を、図の外にある追跡不能な最終文章にしない。

必要な場合、監査可能な叙述単位を `narratives` として保持する。

```json
{
  "id": "N01",
  "text": "図解を読んで立った叙述単位",
  "display_label": "図用短縮",
  "basis": ["G10", "R03"],
  "state": "supported after return-to-source"
}
```

`narrative` は必ずしも一文一命題へatomic化しない。B型文章の流れを壊さない範囲で、「この部分は何を根拠に書かれたか」を戻せる監査単位にする。

### 4.2 Narrative basis is provenance, not proof count

`basis` が3件あるから3票の独立supportがある、とは読まない。

`basis` は叙述がどの意味構造を読んで立ったかを辿るhandleである。独立性はsource lineage側で別に監査する。

### 4.3 Emergent prose is allowed

叙述によって新しい関係や意味が生じることは禁止しない。

ただし、次を分ける。

- map / sourceから継承したもの
- 文章化で新しく立ったもの
- 文章化へ入り切らなかった残差

新しく立った意味は、sourceが最初から述べていた意味へ遡及させない。

## 5. Multi-zoom projection

大規模な材料では、一枚の図へ全情報を載せない。

### Zoom 1 — overview

主に表示するもの:

- higher-order groups
- leaf groups
- group間のexplicit relations
- root-level residual / question

cardsは数だけ表示してよい。

```text
G_A | 14 cards
G_B | 20 cards
...
       ↓ higher-order membership
G_SERIES_1
G_SERIES_2
       ↓
G_ROOT
```

### Zoom 2 — island detail

一つのleaf groupを開く。

表示するもの:

- group canonical / display label
- member cards
- secondary resonance
- preserved differences
- nearby explicit relations
- 必要ならsource refs

「この表札にこのcardが本当に載るか」を確認するためのprojectionである。

### Zoom 3 — focused lineage

一つのrelation / narrative / residual / questionから逆向きに辿る。

```text
source
  ↓
card
  ↓
leaf group
  ↓
higher group
  ↓
relation
  ↓
narrative
```

標準ではcardをleaf group単位でcollapsed表示してよい。

### Zoom 4 — full lineage

機械監査や局所的な深掘りでのみ全card/sourceを展開する。

人間向けoverviewとして常用しない。

## 6. Rendering contract

### Hierarchy projection

`render_hierarchy.py` はhigher-order membershipだけを正本から描く。

optional `--with-relations` を付ける場合も、membershipとsemantic relationを異なるlabel / visual channelで出す。

- `higher-order membership / not semantic relation`
- `Rxx | relation | <display label>`

線種だけへ意味を預けない。

### Lineage projection

`render_lineage.py` は `--focus <ID>` から来歴を逆向きに辿る。

- `--detail groups`: leaf groupの直接cardを `N cards collapsed` として畳む。
- `--detail cards`: cardとsource refまで展開する。

collapsed表示はsemantic recordからcardを削除しない。

## 7. Large-set lesson

114-card規模の実作業由来構造で試験すると、全cardを一度にlineage展開する表示は急速に過密になった。

一方、leaf group単位で畳めば、higher-order structureと叙述来歴を保ったまま大幅に表示量を下げられた。

ここから、固定の「N枚以上は禁止」をMethod Definitionへ置くのではなく、realization側で次を優先する。

1. semantic recordは厚く保持する。
2. 現在の問いに必要なprojectionだけを開く。
3. overviewではcardを畳む。
4. 戻し検査時だけ対象島を開く。
5. full lineageは監査用途へ限定する。

これは `保存は厚く、現在の注意は薄く` を表現層へ適用したものとみなせる。

## 8. Failure cases

- higher-order membershipを因果矢印として読む。
- 上位表札を作るために、どの系列にも入らない重要groupを強制分類する。
- 上位groupへ入れた瞬間に下位groupの表札・差・lineageを消す。
- `display_label` の短さをcanonical meaningへ逆流させる。
- narrativeをsourceの単なる言い換えと扱い、emergent meaningを監査しない。
- full lineageを常時表示し、情報量を深さと取り違える。
- collapsed表示を「省略されたcardは分析から削除された」と解釈する。
