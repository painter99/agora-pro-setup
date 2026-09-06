# Skill: Memory Governance

## Catalog description

Routes Active Memory and Saved Memory decisions without confusing them with Skills.

## Purpose

Govern persistent information operations in Agora.

## Load when

- the user asks to remember, forget, save, update, or audit information;
- a durable preference, decision, fact, project state, or contradiction appears;
- a memory file is missing, stale, or referenced incorrectly.

## Do not load when

- information is transient;
- the task only requires a reusable instruction Skill;
- no durable information operation is needed.

## Dependencies

Use Agora Memory tools when available. Load `active-memory-design.md` for placement decisions and `memory-file-operations.md` for file CRUD.

## Workflow

1. Confirm that a real durable-memory need exists.
2. Decide between Active Memory, Saved Memory, conversation recall, and a Skill.
3. Check authority and approval requirements.
4. Inspect the current state before editing.
5. Perform the smallest valid operation.
6. Verify the result and relevant references.
7. Report success, partial completion, failure, or unresolved conflict.

## Forbidden behavior

- Do not store every transient detail.
- Do not store reusable procedures as personal facts merely for convenience.
- Do not silently delete or replace durable memory.
- Do not allow stale memory to override the current user request.

## Verification

Confirm that the selected memory layer is appropriate and that every performed write is observable and accurate.

## Output contract

State the memory decision, operation performed, evidence checked, and any approval or limitation.
