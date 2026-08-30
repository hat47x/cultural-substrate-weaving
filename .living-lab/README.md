# Local Living Lab workspace

Files placed under this directory are ignored by Git except for this README. Use it as the default workspace for real Web Chat Living Lab records that should not be published with the repository.

## Why this directory exists

Real rounds may refer to private chats, unpublished drafts, client material, internal design work, or other context that does not belong in a public research repository. The public `evals/` directory contains schemas and synthetic examples; it is not the default destination for real case records.

## Recommended practice

- Keep real round/event JSON files here or outside the repository.
- Prefer opaque references such as `chat:case-a-round-3` or `artifact:draft-7` over copying source text into the record.
- Do not put passwords, access tokens, account identifiers, private contact details, confidential source contents, or other secrets into Living Lab records.
- Preserve enough local mapping to recover the referenced source when you are authorized to do so; the public record does not need that mapping.
- If a case later becomes suitable for publication, create a separate anonymized/public record rather than committing the private original.
- Before intentionally publishing any record, inspect both the JSON and every referenced artifact for identifying or confidential information.

## Validate local records

Individual files can be checked without requiring their related records to be present:

```bash
python scripts/validate_living_lab.py .living-lab/round-001.json
```

To check a locally complete set, including duplicate IDs and event-to-round references:

```bash
python scripts/validate_living_lab.py --record-set .living-lab/*.json
```

Validation checks structure and internal references only. It does not certify that a record is safe to publish.
