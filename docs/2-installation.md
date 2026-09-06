# Installation

## 1. Configure prompt templates

Open Agora's System Prompts settings and create or edit a prompt configuration.

- Use `system-prompt/1-system-template.md` for System.
- Use `system-prompt/2-user-template.md` for User.
- Use `system-prompt/3-assistant-template.md` for Assistant.

The User and Assistant templates must retain exactly one structural `Prompt` item each.

## 2. Add runtime variables

Place these explicitly in the System template:

```text
{active_memory}
{skill_catalog}
```

A variable is not necessarily available when its access setting is disabled. Confirm the current Agora version and settings.

## 3. Configure Active Memory

Copy and customize `active-memory/1-active-memory-template.md`. Keep it short. Do not copy complete Skills into Active Memory.

## 4. Install Skills

Import selected Markdown files from `skills/` into Agora's Saved Skills. Give each Skill a short catalog description. Start with:

```text
tool-execution-contract.md
multi-source-research.md
shell-and-device-operations.md
```

Add memory-governance or example Skills only when useful.

## 5. Review access and permissions

Enable Skill access only when wanted. Review Memory, web, conversation, shell, MCP, and automation permissions separately. Shell access alone does not configure a device.

## 6. Test safely

Test a normal answer, a Skill read, a harmless Memory read, a research question, a denied destructive action, and a controlled shell operation. Inspect each result.
