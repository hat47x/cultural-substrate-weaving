# Iterative Inquiry Synthesis — Round Template

Status: research candidate, English translation draft

## Round

- **Round ID:**
- **Current inquiry / purpose:**
- **External constraints:**

## Input Delta

### New material

- 

### External exploration / epistemic handoff — when relevant

Use this section when questions, hypotheses, correspondence candidates, experiment results, or other material from an external exploration route are handed to the next synthesis.

| Ref | Incoming status / role | Origin / operation | Target-side support | Handoff use |
|---|---|---|---|---|
| | | | | question / hypothesis / source material / context / other |

`Incoming status / role` does not require a closed taxonomy. If the caller uses terms such as `framework_generated`, `target_supported`, `cross_field_emergent`, or `unresolved`, preserve them without translation into a different epistemic category. Web research, interviews, experiments, and other routes may retain their own status vocabulary.

Status and provenance in this section are **audit and handoff information**. Do not automatically convert them into one-round grouping geometry or independent-support counts. Do not pass an externally generated hypothesis or correspondence as a target-side observation. If later target-side material independently supports it, preserve the original origin and record the new support separately.

### Prior synthesis handoff capsule — when supplied

Use this section when a compatible one-round synthesis provides a capsule from the previous round.

- **Prior synthesis artifact ref:**
- **Representation / schema ref:**
- **Semantic refs carried forward:**
- **Residual / reopenable anchor refs:**
- **Source refs whose provenance / incoming status must survive:**
- **Possible next check candidates received:**
- **Do not silently assume:**

This section receives **carry-forward candidates and handles for semantic identity** from the previous round.

- Do not reopen every `Semantic ref carried forward`.
- Do not automatically promote `Possible next check candidates` into this round's inquiry, search, or experiment instructions.
- The presence of a residual does not itself justify continuing another round.
- Do not convert incoming status / provenance into target-side fact.

After reading the new delta, move only the subset it actually touches into `Reopened prior artifacts` / `Touched semantic IDs` below.

### Reopened prior artifacts

- 

### Why these prior artifacts were reopened

- 

### Touched semantic IDs when available

- Cards:
- Groups:
- Relations:
- Resonances:
- Residuals / questions:

When a one-round synthesis artifact has stable IDs, for example an `affinity-map`, reuse them while semantic identity survives. Do not assign large numbers of new IDs merely because wording changed.

## Synthesis Realization

- **Method / Skill:**
- **Version / ref if available:**
- **Input artifact refs:**
- **Output artifact refs:**
- **Representation / schema ref if available:**
- **External-status handoff preserved?:** yes / no / not applicable

## Structural Delta

When compact notation is useful, these symbols may describe change operations.

```text
+  newly emerged
~  changed
=  explicitly checked and unchanged
-  withdrawn / no longer supported
?  residual / unresolved remains
```

These are not semantic categories for cards or groups. They describe **change across rounds**.

Example:

```text
+ C115 := "meaning unit raised from new material"
~ G03 := members + {C115}; label "old label" -> "revised label"
= G04 :: "new material checked; current label and membership still hold"
- R02 :: "withdrawn because the former direction is no longer supported"
+ R05: G03 -- G07 :: "newly visible relation predicate"
? Q08 :: "question the current material still cannot discriminate"
```

### Newly emerged

- 

### Changed

- 

### Unchanged despite new material

- 

`Unchanged` is not a place to enumerate large amounts of untouched structure. Record artifacts that the current delta actually touched and that were explicitly rechecked but remained semantically stable.

### Withdrawn / no longer supported

- 

`Withdrawn` does not mean deleted. Preserve the earlier round in history and record why the artifact is no longer adopted in the current state.

### Semantic vs representation delta

- **Semantic delta:** change in the meaning of membership / label / explicit relation / resonance / residual / question
- **Representation delta only:** wording normalization / ID display / renderer / line wrapping / visual layout only
- **Mixed:**

Do not count node movement, Mermaid automatic layout, or appearance-only line wrapping as semantic discovery.

## Residuals

| Ref | Kind / description | Current state | What could reopen / clarify it |
|---|---|---|---|
| | gap / conflict / singleton / unresolved / free text | | |

`Kind` is a convenient descriptive field, not a requirement to classify residuals into a closed taxonomy.

## Question Shift

- **Previous inquiry:**
- **Current inquiry:**
- **What caused the shift:**
- **What remains valid from the previous round:**

Omit this section when the inquiry did not change.

## Diagram / Projection Delta — optional

Use only when the diagram changed from the previous round.

- **Projection:** group relationship / membership / lineage / spatial / other
- **Added visual elements:**
- **Removed visual elements:**
- **Layout-only changes:**
- **Does any visual change correspond to a semantic delta?:**
- **Projection integrity check:**

Confirm that no new relation or containment exists only in the diagram.

## Continuation Boundary

- **Continue / Stop / Hand off:**
- **Reason:**
- **Possible next material or check:**
- **Requires human/domain decision?:**

## Round Handoff

Record only the local information needed next time.

- **Return to:**
- **Reopen when:**
- **Preserve incoming status / provenance for:**
- **Do not silently assume:**
