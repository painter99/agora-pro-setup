# Skill: Memory Tool Reference

## Catalog description

Reference for Agora Memory and conversation-recall tool families.

## Purpose

Help select the correct Memory operation without confusing it with Skill tools.

## Load when

- a Memory tool name, argument, or operation order is uncertain;
- a persistent-memory permission must be checked.

## Do not load when

- no Memory or conversation tool is required.

## Dependencies

None.

## Reference

Memory tools may include:

```text
list_memory_files
read_memory_file
create_memory_file
edit_memory_file
delete_memory_file
update_active_memory
```

Conversation recall tools may include:

```text
search_conversations
list_conversations
read_conversation
```

Skill tools are a separate family:

```text
list_skill_files
read_skill_file
create_skill_file
edit_skill_file
delete_skill_file
```

## Forbidden behavior

Never route a Skill operation through Memory storage or assume a tool is available without checking the current tool set.

## Verification

Use the actual tool result and current permissions as the authority.

## Output contract

State which tool family applies and what prerequisite or permission remains.
