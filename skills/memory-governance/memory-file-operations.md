# Skill: Memory File Operations

## Catalog description

Safe, precise, and verifiable creation, editing, renaming, archiving, and deletion of Saved Memory files.

## Purpose

Apply the smallest reversible operation while preserving unrelated content and preventing silent data loss.

## Load when

- creating, updating, renaming, archiving, or deleting a Saved Memory file;
- checking names, duplicates, references, or stale memory.

## Do not load when

- only reading a file;
- changing an Agora Skill;
- answering a transient question without durable storage.

## Dependencies

`memory-master-index.md`, `memory-tool-reference.md`, and `tool-execution-contract.md`.

## Operation selection

- **Create:** only when the target name does not exist and the content is durable, requested, or a structured topic that would bloat Active Memory.
- **Patch:** default for an existing file when the intended change can be isolated.
- **Replace:** exceptional; use only when a full rewrite is necessary and authorized.
- **Rename/archive:** potentially disruptive; inspect dependent references and obtain authorization.
- **Delete:** irreversible; never do it automatically. Require explicit authorization and verify all references afterward.

## Workflow

1. Identify the exact target, intended scope, and reversibility.
2. List current files before creating anything. A create operation is not idempotent.
3. Read the target file before editing it.
4. Check duplicates, exact names, dependent references, and sensitive content.
5. Prefer a precise patch over a full replacement.
6. For a patch, require `old_string` to match exactly once; preserve unrelated content.
7. Execute only after the required approval and permission gate.
8. Re-read the result, verify existence/content, and check dependent references.
9. Report success, partial completion, failure, or unresolved conflict honestly.

## Patch Uniqueness Recovery

If a patch matches zero or multiple occurrences:

1. Stop; treat the result as evidence that the assumed file state is wrong or ambiguous.
2. Re-read the file in full or in the relevant slice.
3. Locate the intended occurrence and expand the match with unique surrounding context.
4. Retry once only after the target is unique.
5. If duplicated or contradictory content is revealed, surface it instead of silently choosing.

Never guess at missing text and never claim a failed patch succeeded.

## Naming and metadata

Use lowercase `snake_case.md` filenames without spaces, diacritics, path separators, `..`, or leading dots. Keep one durable topic per file. A description is metadata for discovery; it does not replace content visible to the model.

## Sensitive and irreversible operations

Do not store sensitive personal details without appropriate user authorization. Before rename, archive, delete, or full replacement, state the exact target and consequence. Afterward verify both the target state and all relevant indexes/references.

## Forbidden behavior

Do not invent files, silently delete data, overwrite when a precise patch is sufficient, expose secrets, or claim success from a tool return without reading the resulting state.

## Verification

Confirm the expected file state, preserved unrelated content, valid references, correct metadata, and coherent Active Memory routing.

## Output contract

Report the exact operation, target, authorization basis, verification performed, and any limitation.
