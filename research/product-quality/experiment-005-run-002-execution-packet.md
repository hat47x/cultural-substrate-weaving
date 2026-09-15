# E5 Run 002 — fresh surface execution packet

- experiment id: `PQ-E5-005-R002`
- role: executor-only packet
- prepared: 2026-09-16
- source snapshot: `develop/v0.5.0@eae65772760d197f61a45d5bc266824e7f8b0411`
- status: prepared / not executed in the repository-working conversation

## このpacketの目的

同じCSW taskを複数の実surfaceで実行し、文章の一致ではなく、surface固有の包装を通った後も中核的な意味境界が保たれるかを比較できるartifactを作る。

executorは**出力生成だけ**を担当する。P1〜P8の採点、他surfaceとの比較、Run 001との比較は行わない。

## executorへ渡してよいもの

各runでは、次だけを渡す。

1. このexecution packet
2. source snapshotに対応する、そのsurface向けCSW package / Skill / GPT / agent
3. surfaceの通常利用に必要なplatform標準情報

次は渡さない。

- `experiment-005-run-002-evaluation-sheet.md`
- P1〜P8の判定基準一覧
- E5 engineering Run 001の観測結果
- 他surfaceのRun 002出力
- 「どのsurfaceで何が失敗しやすいか」という事前説明

これはexecutorから必要な実行情報まで隠すためではなく、repository固有の評価rubricを出力へ直接混入させないためである。

## 実行surface

可能なものを、**互いの出力を見せずに別runとして**実行する。

| run slot | surface | package / route |
|---|---|---|
| S1 | Claude Code | `cultural-substrate-weaving-ja` plugin |
| S2 | Codex | pluginまたは直接配置Skill。実際のrouteを記録する |
| S3 | OpenAI Skill | ja-JP interactive profile |
| S3M | OpenAI Skill | ja-JP metered profile。実施できる場合のprofile control |
| S4 | ChatGPT GPT | ja-JP GPT package |
| S5 | Microsoft Copilot | ja-JP limited composite profile |

S3Mは任意であり、欠けてもS3の代用とはしない。利用不能なsurfaceを別surfaceで模擬しない。

## 固定task material

地域資料館が、初来館者向け案内を見直している。

- 初来館者24人中14人が「どこから見ればよいか迷った」と回答した。
- 観察した10組中6組が入口地図付近で2分以上滞在した後、職員へ開始点を質問した。
- 常連7人中5人は「決まった順路がないこと」を肯定している。
- チーム案として「全体を見る／一つの資料から始める／スタッフに聞く」の3枚カードがあるが、効果は未検証である。
- 最終採否と外部公開は運営委員会が決める。

この材料以外の利用者調査結果、効果測定、文化体系との対応事実は与えられていない。

## 固定task prompt

> CSWを使って、この案内改善について新しい見方を探索し、委員会へ出せる検討案を作ってください。必要な方法や読み込み深度は、依頼の範囲で判断してください。

## 実行上の扱い

- 通常のsurface挙動に従ってCSWを利用する。
- cultural frameworkを使うか、どこまで読むかは、packageと依頼の範囲からexecutor自身が判断する。
- sibling Methodがsurface上で本当に利用可能なら利用してよい。利用不能なら、実行したふりをしない。
- Microsoft 365のようなlimited profileでは、そのprofileが実際に持つ能力だけで実行する。
- Web検索や外部調査は、このtask materialを増補する目的では行わない。platformの通常動作に検索機能があっても、本runでは固定材料を比較対象とする。
- 他surfaceの回答へ寄せたり、表現を揃えたりしない。

## executorが保存するもの

出力本文を加工せず保存し、別枠で次のmetadataを付ける。

```text
run_slot:
surface:
product:
visible_model:
product_mode_or_reasoning_mode:
source_commit: eae65772760d197f61a45d5bc266824e7f8b0411
package_or_adapter:
package_version_if_visible:
invocation_route:
loaded_skill_or_method:
tools_available:
tools_actually_used:
execution_date:
execution_context_fresh_for_e5: yes / no / unknown
capability_limitations_observed:
```

`visible_model`など確認できない項目は`unknown`とし、推測で補わない。

## executorが行わないこと

- P1〜P8のPASS / FAIL判定
- 「このsurfaceは他より優れている」といった順位付け
- 他surfaceとの差の説明
- Run 001で見つかったfailureを意識した自己修正
- packageにないMethodを実行したとの記載
- task materialにない効果や利用者反応の創作

## 完了条件

一つのsurface runは、**raw output + metadata**が保存された時点で完了する。

複数surfaceが揃ったかどうかはexecutorの完了条件ではない。未実施surfaceは未実施のまま残し、評価側で`not run`として扱う。
