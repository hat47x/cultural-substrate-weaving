# ローカルLiving Lab作業領域 / Local Living Lab workspace

このREADMEを除き、このディレクトリ以下のファイルはGitの追跡対象外です。公開リポジトリへ含めるべきでない実案件のWeb Chat Living Lab記録は、原則としてここ、またはリポジトリ外に保存します。

Files under this directory are ignored by Git except for this README. Use it as the default workspace for real Web Chat Living Lab records that should not be published with the repository.

## この領域を設ける理由

実際のラウンドでは、私的なチャット、未公開原稿、顧客資料、内部設計など、公開研究リポジトリに置くべきでない情報を参照することがあります。公開側の`evals/`はスキーマと合成例を置く場所であり、実案件の記録を保存するための既定の場所ではありません。

Real rounds may refer to private chats, unpublished drafts, client material, internal design work, or other context that does not belong in a public research repository. The public `evals/` directory contains schemas and synthetic examples; it is not the default destination for real case records.

## 推奨する運用 / Recommended practice

- 実際のround / event JSONは、このディレクトリまたはリポジトリ外に保存する。
- 元の文章を記録へ複製するより、`chat:case-a-round-3`や`artifact:draft-7`のような不透明な参照を優先する。
- パスワード、アクセストークン、アカウント識別子、私的な連絡先、機密資料の本文など、秘密にすべき情報をLiving Lab記録へ入れない。
- 権限のある範囲で元資料へ戻れる対応表はローカルに保持してよいが、公開記録にその対応表を含める必要はない。
- 観測された出来事、測定値、利用者の判断、生成AIや外部評価者の解釈を、同じ記録として混ぜない。schema 0.2の`source_type`や`interpretations`を使い、後から判断の起源をたどれるようにする。
- `non_activation`は、そのラウンドで文化体系を開かなかったという状態の記録である。それだけで「使わない方がよかった」と評価しない。
- 後から公開に適した事例になった場合も、私的な原本をそのままcommitせず、匿名化した公開用の記録を別に作る。
- 意図的に公開する前には、JSON本体だけでなく、参照先の成果物にも識別情報や機密情報が残っていないか確認する。

- Keep real round/event JSON files here or outside the repository.
- Prefer opaque references such as `chat:case-a-round-3` or `artifact:draft-7` over copying source text into the record.
- Do not put passwords, access tokens, account identifiers, private contact details, confidential source contents, or other secrets into Living Lab records.
- Preserve enough local mapping to recover the referenced source when you are authorized to do so; the public record does not need that mapping.
- Keep observations, measurements, user judgments, and AI or external interpretations on separate provenance paths. Use schema 0.2 `source_type` and `interpretations` fields when later review may depend on the origin of a judgment.
- Treat `non_activation` as an activation state, not as proof that non-use was preferable.
- If a case later becomes suitable for publication, create a separate anonymized/public record rather than committing the private original.
- Before intentionally publishing any record, inspect both the JSON and every referenced artifact for identifying or confidential information.

## 成果物の来歴と対象帰還 / Artifact provenance and target return

schema 0.2の`artifact_traces`は、成果物の「良し悪し」を採点するためではなく、どの経路で生まれ、対象へ戻したあと何が残ったかを追うために使います。

- `origin`では、対象だけから生じたもの、framework由来のもの、cross-fieldで生じたもの、混合したものを区別する。
- framework由来の成果物では、`framework_refs`を残し、必要に応じて`operation_refs`とframework contactの`selection_ref`を対応させる。
- `target_return.state`は、未確認、未解決、対象側で支持、弱化、棄却、対象帰還が不適用、を区別する。支持・弱化・棄却を記録するときは`evidence_refs`を必須にする。
- `user_disposition`は、利用者が成果物を採用、修正、撤回したことが実際に観測できた場合だけ、その参照元とともに記録する。AIが利用者の判断を推測して埋めない。
- 集計値は観測記録の棚卸しであり、frameworkの勝率、有用性スコア、採用KPIとして扱わない。

`artifacts`は成果物参照の一覧を保ち、`artifact_traces`はその一部にだけ付けても構いません。追跡情報を埋めるために、本来の作業を変えたり、観測用の事例を作ったりしないでください。

In schema 0.2, `artifact_traces` records provenance and target return without turning them into a score. Framework-derived traces identify their framework provenance. Evaluated target-return states require evidence references. User disposition is recorded only when an actual user decision has an attributable source. Summary counts remain review inventory, not effectiveness metrics.

## ローカル記録の検証 / Validate local records

対応する他の記録が同じ場所にそろっていなくても、個別ファイルの形式は検査できます。

```bash
python scripts/validate_living_lab.py .living-lab/round-001.json
```

ローカルに一式そろっている場合は、IDの重複とevent→round参照まで検査できます。

```bash
python scripts/validate_living_lab.py --record-set .living-lab/*.json
```

validatorが確認するのは、記録形式と内部参照の整合です。記録内容や生成AIの解釈が正しいこと、また、その記録を公開して安全であることまでは保証しません。

Validation checks record structure and internal references only. It does not certify that an observation or interpretation is correct, or that a record is safe to publish.
