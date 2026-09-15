# Skill: Memory Tool Reference

## Catalog description

Selects Agora Memory and conversation-recall tools using current tool definitions and verified outputs.

## Purpose

Prevent confusion between Memory, Skill, and conversation tool families and prevent documentation from outranking live tool behavior.

## Load when

- a Memory tool name, argument, mode, or operation order is uncertain;
- a persistent-memory permission must be checked;
- a tool result conflicts with this reference.

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

## Verification

State the tool family used, actual tool result, prerequisite or permission that remains, and any mismatch between this reference and live behavior.
