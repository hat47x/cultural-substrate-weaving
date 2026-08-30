# ローカルLiving Lab作業領域 / Local Living Lab workspace

このREADMEを除き、このディレクトリ配下のファイルはGitの追跡対象から外している。公開リポジトリへ含めるべきでない実案件のWeb Chat Living Lab記録は、原則としてここ、またはリポジトリ外へ保存する。

Files under this directory are ignored by Git except for this README. Use it as the default workspace for real Web Chat Living Lab records that should not be published with the repository.

## この領域を設ける理由

実際のラウンドは、私的なチャット、未公開原稿、顧客資料、内部設計、その他公開研究リポジトリへ置くべきでない文脈を参照しうる。公開側の `evals/` はスキーマと合成例を置く場所であり、実案件記録の既定保存先ではない。

Real rounds may refer to private chats, unpublished drafts, client material, internal design work, or other context that does not belong in a public research repository. The public `evals/` directory contains schemas and synthetic examples; it is not the default destination for real case records.

## 推奨運用 / Recommended practice

- 実際のround/event JSONは、このディレクトリまたはリポジトリ外へ保存する。
- 元文章を記録へ複製するより、`chat:case-a-round-3` や `artifact:draft-7` のような不透明な参照を優先する。
- パスワード、アクセストークン、アカウント識別子、私的な連絡先、機密資料の本文その他の秘密情報をLiving Lab記録へ入れない。
- 権限がある範囲で元資料へ戻れる対応表はローカルに保持してよいが、公開記録側へその対応表を含める必要はない。
- 後から公開に適した事例になった場合も、私的原本をそのままcommitせず、別の匿名化・公開用記録を作る。
- 意図的に公開する前には、JSON本体だけでなく、参照先の成果物にも識別情報や機密情報が残っていないか確認する。

- Keep real round/event JSON files here or outside the repository.
- Prefer opaque references such as `chat:case-a-round-3` or `artifact:draft-7` over copying source text into the record.
- Do not put passwords, access tokens, account identifiers, private contact details, confidential source contents, or other secrets into Living Lab records.
- Preserve enough local mapping to recover the referenced source when you are authorized to do so; the public record does not need that mapping.
- If a case later becomes suitable for publication, create a separate anonymized/public record rather than committing the private original.
- Before intentionally publishing any record, inspect both the JSON and every referenced artifact for identifying or confidential information.

## ローカル記録の検証 / Validate local records

対応する他の記録が同じ場所に無くても、個別ファイルの形式は検査できる。

```bash
python scripts/validate_living_lab.py .living-lab/round-001.json
```

ローカルに一式揃っている場合は、ID重複とevent→round参照まで検査できる。

```bash
python scripts/validate_living_lab.py --record-set .living-lab/*.json
```

validatorが確認するのは形式と内部参照であり、その記録が公開して安全かどうかを保証するものではない。

Validation checks structure and internal references only. It does not certify that a record is safe to publish.
