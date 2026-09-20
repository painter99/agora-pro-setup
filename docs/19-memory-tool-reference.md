# Memory Tool Reference

Reference documentation for the Agora Memory, Skill, and conversation-recall tool families. This is **not a Skill**: it contains no reusable procedure to execute, only names, arguments, and invariants. The procedures live in `skills/memory-governance/`.

Moved out of `skills/memory-governance/memory-tool-reference.md` on 2026-09-20 because a static reference table does not belong in the Skill Catalog (see `docs/4-active-memory.md` and `skills/skill-format.md`).

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

## Related docs

- `docs/13-memory-governance.md` — layer model and non-negotiable invariants.
- `docs/4-active-memory.md` — Active Memory scope and limits.
- `docs/8-tools-and-safety.md` — shared tool safety contract.
