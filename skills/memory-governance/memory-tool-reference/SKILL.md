---
name: memory-tool-reference
description: "Reference for the Agora Memory, conversation-recall, and Skill tool families: expected tool names, family boundaries, and authority rules."
license: MIT
---

# Skill: Memory Tool Reference

## Catalog description

Reference for the Agora Memory, conversation-recall, and Skill tool families: expected tool names, family boundaries, and authority rules.

## Purpose

Help select the correct Memory, conversation-recall, or Skill operation without confusing tool families, and name the expected interface when exact tool names or arguments are uncertain.

## Load when

- a Memory, conversation-recall, or Skill tool name, argument, or operation order is uncertain;
- a persistent-memory permission must be checked;
- routing between Memory, conversation-recall, and Skill tool families is unclear.

## Do not load when

- no Memory, conversation-recall, or Skill tool is required;
- the required tool is already visible in the current tool definitions and no family question is open.

## Dependencies

- `memory-master-index` — routing between memory layers;
- `memory-file-operations` — Saved Memory file operations;
- `file-based-active-memory` — working state file placement, size, and R/W discipline;
- `tool-execution-contract` — shared inspection and verification contract.

## Workflow

1. Identify the operation family: Saved Memory file, working state file, conversation recall, or Skill.
2. Check the current tool definitions — they are the authority; this reference lists the expected interface, not a guarantee.
3. Select the smallest tool that performs the operation.
4. Check permissions and the confirmation policy before any write or destructive call.
5. Route the procedure to the domain Skill (`memory-file-operations`, `file-based-active-memory`); this reference does not replace them.
6. Verify the result by reading back the affected state.

### Expected tool families

Memory tools may include:

```text
list_memory_files
read_memory_file
create_memory_file
edit_memory_file
delete_memory_file
update_active_memory
```

An instance may disable injected Active Memory and keep a file-based working
state file instead; `update_active_memory` then remains unused (see
`file-based-active-memory`).

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

The wording "may include" is deliberate: the current generation's tool list and the official Agora user manual override this reference whenever they differ.

## Forbidden behavior

- Never route a Skill operation through Memory storage or vice versa.
- Never assume a tool is available without checking the current tool set.
- Never treat this reference as overriding observed tool output or the current tool definitions.

## Verification

Use the actual tool result and current permissions as the authority; confirm the selected family matches the operation before executing.

## Output contract

State which tool family applies, which tool was selected, and what prerequisite or permission remains.