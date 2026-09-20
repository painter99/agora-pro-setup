# Skill: Memory Tool Reference

## Catalog description

Selects Agora Memory and conversation-recall tools using current tool definitions and verified outputs.

## Purpose

Prevent confusion between Memory, Skill, and conversation tool families and prevent documentation from outranking live tool behavior.

## Load when

- a Memory tool name, argument, mode, or operation order is uncertain;
- a persistent-memory permission must be checked;
- a tool result conflicts with this reference.

## Do not load when

- the tool name, arguments, and operation are already unambiguous;
- the task involves no Memory, Skill, or conversation-recall tool;
- Active Memory content decisions are the only question (use `active-memory-design.md`).

## Dependencies

- `memory-master-index.md` (routing)
- `memory-file-operations.md` (Saved Memory CRUD)
- `active-memory-authority.md` (AM changes)
- `tool-execution-contract.md` (safety layer)

## Authority rule

The current tool definitions and actual tool output are authoritative. This document is a routing reference, not a guarantee that every listed tool or argument is enabled in a given Agora deployment.

## Expected Memory tools

```text
list_memory_files
read_memory_file
create_memory_file
edit_memory_file
delete_memory_file
update_active_memory
```

## Expected conversation-recall tools

```text
search_conversations
list_conversations
read_conversation
```

## Separate Skill tools

```text
list_skill_files
read_skill_file
create_skill_file
edit_skill_file
delete_skill_file
```

Do not route Skill operations through Memory storage or assume availability without checking the current tool set.

## Invariants

- Read/list before editing or creating.
- Use the smallest operation that satisfies the request.
- For a precise file patch, `old_string` must be unique; do not substitute a full replacement casually.
- `content` is the replacement/new content for the selected operation; do not assume incompatible operation fields are interchangeable.
- `description` is metadata and does not replace file content.
- After every write, re-read or otherwise inspect the resulting state.

## Workflow

1. Confirm the tool family needed: Memory, Skill, or conversation recall.
2. Check the live tool definitions for names, arguments, and modes; do not assume availability.
3. List or read the current state before any write.
4. Choose the smallest operation that satisfies the request (patch over replace).
5. For patches, verify `old_string` uniqueness before submitting.
6. Execute, then re-read or inspect the resulting state.
7. Report the family used, the actual result, and any mismatch with this reference.

## Forbidden behavior

- Never route Skill operations through Memory storage.
- Never assume a listed tool or argument is enabled without checking the live tool set.
- Never substitute a full replacement for a precise patch without authorization.
- Never claim a write succeeded without inspecting the resulting state.
- Never treat this reference as higher authority than live tool definitions or output.

## Verification

State the tool family used, actual tool result, prerequisite or permission that remains, and any mismatch between this reference and live behavior.

## Output contract

- Tool family and exact tool/operation used.
- State inspected before the write and state verified after it.
- Any mismatch between this reference and live tool definitions, plus remaining permission or prerequisite.
