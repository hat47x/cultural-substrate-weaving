# P2 ja-JP Claude/Codex bundle metadata routing review — 2026-09-07

## 目的

`P2-JA-CLAUDE-CODEX-BUNDLE-METADATA-PROTOTYPE-2026-09-07.md` で作成したja-JP bundle metadata prototypeが、三Skillの責務境界を弱めていないかauthoring-levelで点検する。

対象はplugin-level metadataの文言であり、Claude Code / Codex host上の実routing挙動ではない。

## 評価対象

prototype description:

> 文化的体系による探索、材料主導の一回統合、複数ラウンドの探索継続を、責務の異なる3つのSkillとして収録し、必要に応じてhandoffします。帰属・残差・未解決を保ち、各Skillを一つの万能手順へ混ぜません。明示呼び出し専用。

contains:

- `cultural-substrate-weaving`
- `affinity-synthesis`
- `iterative-inquiry-synthesis`

## Review boundary

このレビューでは次だけを見る。

1. 一つのSkillへ全処理を押し込む読みを強めていないか。
2. 三Skillを常に三つ連続で実行するように読めないか。
3. AffinityとIterativeの一回／複数ラウンド境界が崩れないか。
4. CSW由来のframework-generated候補がtarget-side supportへ自動昇格する読みを生まないか。
5. 複合ケースをhandoffとして扱えるか。

host selection algorithm、implicit invocation、UI表示順、実行性能は評価しない。

## Case 1 — 一回だけ異種材料を統合する

### Task

複数の記事・発言・観察メモを、先に分類体系を決めず、一回だけ材料主導でまとめたい。

### Expected route

`affinity-synthesis`

### Review

bundle descriptionには「材料主導の一回統合」が独立した役割として書かれている。

文化体系を使う必要も、複数ラウンド管理を起動する必要もない。三Skillが同じpluginに入っていることから、CSWやIterativeまで必須と読む根拠はない。

### Result

PASS at wording level.

## Case 2 — 既存統合へ新材料を追加する

### Task

前回の統合結果を保持したまま、新しい資料を追加し、影響を受ける部分だけを開き直したい。

### Expected route

`iterative-inquiry-synthesis`

必要な一回統合があれば、互換realizationとして`affinity-synthesis`へhandoffできる。

### Review

bundle descriptionの「複数ラウンドの探索継続」と「必要に応じてhandoff」は、この役割分担と整合する。

「三Skillを常に連続実行する」とは書いていない。Affinityは必要な一回統合のrealizationであり、Iterativeの代替にはならない。

### Result

PASS at wording level.

## Case 3 — 文化体系から通常分析にない問いを得る

### Task

対象資料だけでは思いつきにくい関係や問いを、文化的体系を探索資源として使って出したい。ただし対象事実へ自動昇格させたくない。

### Expected route

`cultural-substrate-weaving` / target skill `weave`

### Review

bundle descriptionでは「文化的体系による探索」が独立役割として示されている。

Affinityの材料主導統合やIterativeのラウンド管理を、framework-generated候補の証拠化手段として使うとは書いていない。既存handoff contractどおり、帰属を保ったまま次工程へ渡せる。

### Result

PASS at wording level.

## Case 4 — framework由来の問いを次ラウンドへつなぐ

### Task

CSWで生じたframework-generatedの問いを保持し、対象資料を追加調査し、次ラウンドで必要な箇所だけ再検討し、その中で材料主導の一回統合も行いたい。

### Expected route

`weave → iterative-inquiry-synthesis → affinity-synthesis`

ただしこれは必要な役割を順にhandoffする例であり、常時固定pipelineではない。

### Review

このケースでは三Skillすべてが必要になり得る。bundle descriptionの「責務の異なる3つのSkill」「必要に応じてhandoff」が最も直接的に機能する。

一方、descriptionは固定順序や自動連鎖を規定していない。問いの出所、target-side support、round delta、one-round synthesisをそれぞれ別の契約で保持できる。

### Result

PASS at wording level.

## Cross-case findings

### 1. 一つの万能Skillへ押し込む方向は見つからない

prototypeは三役割を一文へ圧縮しているが、「責務の異なる3つのSkill」と「一つの万能手順へ混ぜない」を同時に置いている。

少なくともauthoring-levelでは、全処理を`weave`へ戻す読みや、Affinityにmulti-round orchestrationまで担当させる読みは生じなかった。

### 2. handoffは固定pipelineを意味しない

Case 1とCase 3では一つのSkillだけでよい。Case 2では二層、Case 4では三層が関与し得る。

したがって「必要に応じてhandoff」は、毎回三Skillを実行する意味としては読まなかった。

### 3. attribution boundaryはmetadataだけでは完結しない

bundle descriptionに「帰属」を含めても、framework-generated / target-supported等の細かな認識状態は各Skill runtimeとhandoff contractが保持する。

metadata一文だけで証拠境界を保証したと扱ってはいけない。

### 4. explicit invocationはhost上で未観測

prototypeはexplicit invocationを宣言しているが、実package materializationもClaude/Codex host executionもまだ行っていない。

したがって「暗黙起動されない」と実証したわけではない。

## Wording issue considered

「一つの万能手順へ混ぜません」はやや設計文書寄りの表現である。

ただし現段階では、三Skill分離の誤読を防ぐ境界語として機能している。production metadataへ昇格する際には、UI上の文字数・自然さと合わせて、より肯定形の「各Skillの責務を分けたまま扱います」等へ置き換える余地がある。

このレビューではprototype文言を変更しない。

## Result

**PROVISIONAL PASS — authoring-level routing wording**

4ケースでは、bundle-level descriptionによる明確なcross-layer contamination、固定三連鎖、単一万能Skill化は見つからなかった。

ただし次の制約がある。

- same authoring model / same repository context
- 4ケースのみ
- 実Claude Code / Codex host未使用
- Skill一覧・marketplace UIとの組み合わせ未観測
- implicit/explicit invocation実挙動未観測
- en-US未実装

したがってmetadata statusは`prototype`のままとし、`reviewed`へ上げない。

## 次の実作業

P2の次候補はresearch-only package materializerである。

すでに次が外部化されている。

- locale realization
- package source boundary
- distribution target name
- Skill subtree source→target mapping
- Skill entry transform
- OpenAI per-Skill metadata prototype
- Claude/Codex bundle metadata prototype

materializerでは、これらのplanから一時treeを生成し、**production outputへ書き込まず**、path collision・missing metadata・frontmatter transform・relative reference preservationを実ファイルtreeで検査する。

これはproduction builder generalizationの前段であり、release artifactを生成したことにはしない。
