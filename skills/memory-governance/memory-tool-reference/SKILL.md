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
memory_list
memory_read
memory_create
memory_edit
memory_delete
```

From v2.2.0 no Active Memory update tool exists. An instance may disable
injected Active Memory and keep a file-based working state file instead (see
`file-based-active-memory`).

Conversation recall tools may include:

```text
conversation_search
conversation_list
conversation_read
```

Skill tools are a separate family:

```text
skill_list
skill_read
skill_create
skill_edit
skill_delete
```

Canonical names (v2.2.0+): built-in tools use the short `memory_*`/`skill_*`/`task_*`/`conversation_*`/`shell_*` forms; texts written before v2.2.0 quote legacy `*_file`-style names for the same families — new texts use canonical forms and verify against the live tool list.

The wording "may include" is deliberate: the current generation's tool list and the official Agora user manual override this reference whenever they differ.

## Forbidden behavior

- Never route a Skill operation through Memory storage or vice versa.
- Never assume a tool is available without checking the current tool set.
- Never treat this reference as overriding observed tool output or the current tool definitions.

## Verification

Use the actual tool result and current permissions as the authority; confirm the selected family matches the operation before executing.

## Output contract

State which tool family applies, which tool was selected, and what prerequisite or permission remains.