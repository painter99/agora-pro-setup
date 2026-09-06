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

Import selected Markdown files from `skills/` into Agora's Saved Skills. The repository folders are only for organization; Agora uses a flat namespace. Choose the exact file and enter the flat name shown below (normally without `.md`):

| Repository file | Agora Skill name |
|---|---|
| `skills/tool-execution-contract.md` | `tool-execution-contract` |
| `skills/research/multi-source-research.md` | `multi-source-research` |
| `skills/shell/shell-and-device-operations.md` | `shell-and-device-operations` |
| `skills/memory-governance/memory-master-index.md` | `memory-master-index` |
| `skills/memory-governance/active-memory-design.md` | `active-memory-design` |
| `skills/memory-governance/memory-file-operations.md` | `memory-file-operations` |
| `skills/memory-governance/memory-tool-reference.md` | `memory-tool-reference` |
| `skills/memory-governance/memory-audits.md` | `memory-audits` |
| `skills/examples/example-project-skill.md` | `example-project-skill` |
| `skills/examples/example-learning-skill.md` | `example-learning-skill` |

Add the example Skills only when useful. Do not install `skills/README.md`, `skill-format.md`, or `skill-catalog.md` as runtime Skills; they are author documentation.

## 5. Review access and permissions

Enable Skill access only when wanted. Review Memory, web, conversation, shell, MCP, and automation permissions separately. Shell access alone does not configure a device.

## 6. Test safely

Test a normal answer, a Skill read, a harmless Memory read, a research question, a denied destructive action, and a controlled shell operation. Inspect each result.
