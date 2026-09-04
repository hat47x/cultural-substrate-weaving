# OpenRouter free-tierで境界ケースを実行する手順

## 目的

この文書は、`research/empty-self-boundary-cases/` の既存ケースや、自然な実作業から生じた限定的な回帰確認を、OpenRouterの無料枠で実行するときの補助手順である。

新しいベンチマーク体系を作るための文書ではない。Web Chatで行ってきた検査と同じく、元材料、生成時の条件、raw output、後からの解釈を分け、必要な問いだけを確かめるために使う。

無料枠を温存すること自体を目的にはしない。一方で、無料枠があるからという理由だけでケースを増やしたり、API呼び出し回数を成果指標にしたりもしない。

## 使う条件

OpenRouter APIは、たとえば次のような問いが自然な実作業から生じた場合に使う。

- 同じ入力を複数モデルへ与えたとき、どの差がモデル差として現れるかを見たい。
- promptや追加指示の差だけを切り分けたい。
- Web ChatとAPI実行で、読み方やroutingに違いが出るかを確かめたい。
- Routerが案内しているreferenceへ、モデルが実行時に到達するかを見たい。
- 修正した方法について、限定的な回帰確認が必要になった。

これらの問いがない場合、APIを使うこと自体を作業目的にしない。

## 秘密情報の扱い

APIキーは実行環境の環境変数だけで扱う。

```text
OPENROUTER_API_KEY
```

次へは書かない。

- source code
- Issue / PR
- Markdown文書
- run record
- raw output
- shell historyへ残すコマンド文字列
- commit
- デバッグログ

APIキーの値そのものを、生成AIへ入力しない。

## paid fallbackを使わない

この研究では、**有料モデルや有料fallbackへ自動的に移らないこと**を前提にする。

モデルを固定して比較する場合は、その時点で無料提供されていることを公式のモデル一覧で確認し、明示的なfree model slugを指定する。

`openrouter/free` は、利用可能なfreeモデルからルーティングする用途には便利だが、実際に選ばれるモデルが変わり得る。そのため、同一モデルを固定した比較条件には使わない。

探索的に `openrouter/free` を使った場合は、応答に記録された実際のモデル名をrun recordへ残す。

複数モデルfallbackを指定する場合も、**指定候補がすべてfreeであると確認できる場合に限る**。条件比較では、fallback自体が解釈を難しくするため、原則として一つの明示モデルを使う。

## 追加課金を伴う機能を既定で使わない

OpenRouterでは、free modelを使っていても、Web検索などの追加機能に別料金が発生する場合がある。

境界ケース検査では、必要性が確認できない限り、次のような追加機能を付けない。

- Web検索plugin
- `:online` などWeb検索を有効にする指定
- 有料providerへのfallback
- 課金を伴う追加tool / plugin

外部検索が課題そのものに必要な場合は、API比較と検索条件を同時に変えず、何を比較したいのかを先に分ける。

## モデルの選び方

### 同じ条件を繰り返す場合

一つの明示的なfree model slugを固定する。

モデル名だけでなく、実行日時も記録する。free modelは提供終了、provider変更、rate limit変更などがあり得るためである。

### 複数モデルを見る場合

モデル間で勝敗を付けるのではなく、同じ入力に対して**どの読みの差が現れたか**を見る。

たとえば、

- 元材料にない因果を足したか。
- 未確定性を残したか。
- 仮説を元材料と別の来歴に置いたか。
- 必要なreferenceへ到達したか。
- 慎重さが判断回避へ変わったか。

をモデルごとに記録する。

「Aモデルは3勝、Bモデルは2勝」のような総合順位にはしない。

## API requestの基本形

OpenRouterのChat Completions APIを使う場合の最小形は、概ね次のようになる。

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d @request.json
```

`request.json` には、その実行条件で必要な情報だけを置く。

```json
{
  "model": "<verified-free-model-slug>",
  "messages": [
    {
      "role": "user",
      "content": "<case input and only the instructions allowed for this condition>"
    }
  ]
}
```

APIキーを `request.json` に入れない。

モデル名、parameter、system message、tool指定などを変更した場合は、条件差としてrun recordへ残す。

## 生成側へ見せるもの

Web Chatと同じ境界を使う。

原則として生成側へ見せてよいのは、

1. 対象ケースの `input.md`。
2. 現行CSWを通常どおり使うなら、その課題で本来読む文書。
3. 比較条件で追加すると事前に決めた指示。

だけである。

生成前に次を見せない。

- `reference.md`
- `run-record-template.md`
- このAPI実行手順
- ケースの狙いを説明するREADME
- 後から得られた利用者補正

検査したい境界をpromptへ先に書けば、検査ではなく答え合わせになる。

## 条件間でそろえるもの

比較するときは、意味のある差だけを変える。

たとえばprompt差を見たい場合は、

- 同じmodel slug
- 同じinput
- 同じ主要parameter
- 同じtool有無

を保ち、追加指示だけを変える。

モデル差を見たい場合は、inputと指示を保ち、model slugだけを変える。

完全な再現性を主張しない。provider側の更新、sampling、routing、rate limitなど、こちらで固定できない要素がある。

## raw outputを先に保存する

API応答を得たら、解釈や要約を始める前にraw responseまたは少なくとも生成本文を保存する。

run recordには、raw outputへの参照と、次を残す。

- 実行日時
- requestしたmodel slug
- 応答で確認できた実モデル名
- HTTP status
- free-tierとして実行したこと
- fallbackの有無
- tool / pluginの有無
- 主要parameter
- request inputへの参照

rate limit、model unavailable、provider error、network errorなどで応答を得られなかった場合は、**生成結果の失敗として扱わない**。

たとえばDNS失敗でAPIへ到達しなかったなら、記録できるのは「API到達前に終了した」という実行環境上の事実までである。

## 出力後の検証

出力を保存してから `reference.md` を開く。

`run-record-template.md` に沿って、

- 元材料として保たれたもの。
- 新しく生じた意味。
- 来歴を失った混入。
- ケース固有の差。
- 逆方向の歪み。
- 条件間で変わった箇所。

を確認する。

routing確認ではさらに、

- どのreferenceを使ったか。
- 使わなかったreferenceが、課題上ほんとうに必要だったか。
- referenceへ到達しなかったことがsource不足なのか、routingなのか、モデル差なのか。

を分ける。

## free-tierの残量について

日次・週次・月次などの無料枠、rate limit、提供モデルは外部サービス側で変わり得る。

固定値をこの研究文書へ焼き込まず、実行時点の公式情報とAPI応答を確認する。

無料枠が尽きた場合は、paid fallbackへ移らず、その時点で停止する。後で再開する必要があるかは、研究上の問いがまだ残っているかで判断する。

## 正本へ反映するとき

APIで一度差が出ただけでは `src/` を変更しない。

少なくとも、

- 同型の問題が自然な実作業でも確認できるか。
- モデル固有の差ではないか。
- 現行正本にすでに同じ能力がないか。
- routingや読み込み順の問題ではないか。
- 修正した場合に逆方向の歪みを生まないか。

へ戻る。

APIは、考える代わりに判定を委ねるためではなく、**切り分けに必要な追加材料を得るため**に使う。

## 公式情報

実行時には、OpenRouterの最新の公式Request Builder、モデル一覧、free model router、pricingを確認する。endpoint、free model、rate limit、追加機能の料金は将来変わり得るため、この文書より公式情報を優先する。
