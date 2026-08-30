# ローカルLiving Lab作業領域 / Local Living Lab workspace

このREADMEを除き、このディレクトリ以下のファイルはGitの追跡対象外です。公開リポジトリへ含めるべきでない実案件のWeb Chat Living Lab記録は、原則としてここ、またはリポジトリ外へ保存します。

Files under this directory are ignored by Git except for this README. Use it as the default workspace for real Web Chat Living Lab records that should not be published with the repository.

## この領域を設ける理由

実際のラウンドでは、私的なチャット、未公開原稿、顧客資料、内部設計など、公開研究リポジトリへ置くべきでない情報を参照することがあります。公開側の`evals/`はスキーマと合成例を置く場所であり、実案件の記録を保存する既定の場所ではありません。

Real rounds may refer to private chats, unpublished drafts, client material, internal design work, or other context that does not belong in a public research repository. The public `evals/` directory contains schemas and synthetic examples; it is not the default destination for real case records.

## 推奨する運用 / Recommended practice

- 実際のround / event JSONは、このディレクトリまたはリポジトリ外へ保存する。
- 元の文章を記録へ複製するより、`chat:case-a-round-3`や`artifact:draft-7`のような不透明な参照を優先する。
- パスワード、アクセストークン、アカウント識別子、私的な連絡先、機密資料の本文など、秘密にすべき情報をLiving Lab記録へ入れない。
- 権限のある範囲で元資料へ戻れる対応表はローカルに保持してよいが、公開記録へその対応表を含める必要はない。
- 後から公開に適した事例になった場合も、私的な原本をそのままcommitせず、匿名化した公開用の記録を別に作る。
- 意図的に公開する前には、JSON本体だけでなく、参照先の成果物にも識別情報や機密情報が残っていないか確認する。

- Keep real round/event JSON files here or outside the repository.
- Prefer opaque references such as `chat:case-a-round-3` or `artifact:draft-7` over copying source text into the record.
- Do not put passwords, access tokens, account identifiers, private contact details, confidential source contents, or other secrets into Living Lab records.
- Preserve enough local mapping to recover the referenced source when you are authorized to do so; the public record does not need that mapping.
- If a case later becomes suitable for publication, create a separate anonymized/public record rather than committing the private original.
- Before intentionally publishing any record, inspect both the JSON and every referenced artifact for identifying or confidential information.

## ローカル記録の検証 / Validate local records

対応する他の記録が同じ場所にそろっていなくても、個別ファイルの形式は検査できます。

```bash
python scripts/validate_living_lab.py .living-lab/round-001.json
```

ローカルに一式そろっている場合は、IDの重複とevent→round参照まで検査できます。

```bash
python scripts/validate_living_lab.py --record-set .living-lab/*.json
```

validatorが確認するのは、記録形式と内部参照の整合です。その記録を公開して安全かどうかまで保証するものではありません。

Validation checks structure and internal references only. It does not certify that a record is safe to publish.
