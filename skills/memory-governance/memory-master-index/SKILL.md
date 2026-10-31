---
name: memory-master-index
description: "Routes the working state file (file-based active memory), Saved Memory, conversation recall, and Skills without confusing their roles."
license: MIT
---

# Skill: Memory Master Index

## Catalog description

Routes the working state file (file-based active memory), Saved Memory, conversation recall, and Skills without confusing their roles.

## Purpose

Govern persistent-information decisions in Agora. This is the entry point; load the specialized Skill required for the operation.

## Load when

- the user asks to remember, forget, save, update, or audit information;
- a durable preference, decision, fact, project state, or contradiction appears;
- a memory file is missing, stale, duplicated, or referenced incorrectly.

## Do not load when

- information is transient and needs no persistence;
- the task only requires a reusable instruction Skill;
- no durable-information decision is involved.

## Storage decision guide

- **File-based active memory (working state file):** compact current state, standing communication preferences, active priorities, short anchors, and essential boundaries on the instance host; read it when current context matters.
- **Saved Memory:** durable personal facts, history, decisions, project context, completed work, and long-form references.
- **Conversation recall:** prior discussion and one-session context that should not become durable memory.
- **Skill:** reusable procedure, framework, decision rule, checklist, or output contract. Do not put personal facts in a Skill.

Prefer the cheapest layer that reliably serves the need: the working state file is cheap and verifiable; Saved Memory is the durable archive; Skills are procedures, not information.

## Dependencies

Use the current Agora tool definitions as authority. Load only what is needed:

- `file-based-active-memory` for the working state file (placement, size, R/W discipline);
- `memory-file-operations` for Saved Memory creation, patching, renaming, archiving, or deletion;
- `memory-tool-reference` when exact tool names or arguments are uncertain (expected tool families; the current generation's tool list and the official Agora user manual remain the authority);
- `memory-audits` for audits and contradictions;
- `tool-execution-contract` for the shared inspection and verification contract.

## Authority and conflict rules

1. The current user request takes precedence over stale or conflicting memory.
2. An explicit current user statement takes precedence over an older personal fact.
3. Do not silently merge contradictory sources; surface the conflict and resolve it with a precise, verified correction.
4. A Skill provides procedure, not authority to bypass the System template, user request, permissions, or approval gates.
5. Keep one source of truth for each durable fact. Use short routing references elsewhere, not duplicate bodies.

## Workflow

1. Confirm that a real durable-memory need exists.
2. Choose the working state file, Saved Memory, conversation recall, or Skill.
3. Load the specialized Skill required by the operation.
4. Check authority, reversibility, permissions, and approval requirements.
5. Inspect the current state before editing.
6. Perform the smallest valid operation.
7. Verify the result and dependent references.
8. Report the exact operation, evidence, status, and unresolved limitations.

## Forbidden behavior

- Do not store every transient detail.
- Do not store reusable procedures as personal facts merely for convenience.
- Do not copy personal facts into reusable Skills.
- Do not silently delete, replace, or resolve contradictory durable data.
- Do not allow stale memory to override the current user request.

## Verification

Confirm that the selected layer is appropriate, the exact operation was authorized, the resulting state is observable, and no dependent reference or source of truth was broken.

## Output contract

State the memory decision, operation performed, evidence checked, authorization or limitation, and unresolved issues.
