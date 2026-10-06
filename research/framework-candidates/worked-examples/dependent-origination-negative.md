# Dependent origination non-activation example

Status: negative example / runtime requalification support

## Target

A batch export has three explicit steps:

```text
generate file
  -> compress file
  -> upload file
```

The first step fails with a reproducible disk-full error. Compression never starts. Freeing disk space and rerunning the export succeeds.

The target already contains:

- a verified prerequisite relation;
- a verified intervention;
- a verified downstream recovery.

## Why the framework should not be activated

There is no unresolved upstream condition question.

Applying a dependent-origination pass would only restate:

- file generation requires writable storage;
- when writable storage is unavailable generation stops;
- when storage is restored generation resumes.

Those distinctions are already explicit in the target logs and ordinary debugging process.

## Correct CSW result

Use the direct operational finding:

> insufficient writable storage prevented file generation; restoring capacity allowed the pipeline to continue.

Do not activate dependent origination merely because the target contains a dependency or a sequence.

Reopen broader conditional analysis only if:

- the failure recurs after storage recovery;
- multiple independent conditions appear;
- the observed intervention does not produce the expected cessation;
- a component assumed to be independent turns out to depend on hidden state.

## Boundary

Non-activation says nothing about the historical or philosophical importance of dependent origination.

It means only that the target has already done the cognitive work that the framework would otherwise prompt.
