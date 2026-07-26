# Translation review policy

- `ja-JP` is the semantic canonical locale.
- Every translated file keeps the same relative path as the canonical file.
- Translation must preserve function, conditions, exceptions, and stopping rules rather than merely matching words.
- A change to a canonical file makes the corresponding translation stale until its recorded source hash is updated.
- Machine-assisted translation may be used for a draft. Public claims of authoritative equivalence require independent human review.
- Improvements discovered in another language should be proposed back to the canonical Japanese source before being propagated to all locales.
