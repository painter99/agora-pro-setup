# Installation

## 0. Prerequisites

- The Agora app (current release from F-Droid) on an Android device.
- A copy of this repository (clone or download).
- To validate the repository with `scripts/check.sh`: python3, git, and bash — standard on Linux and macOS development machines.

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

Import selected Markdown files from `skills/` into Agora's Saved Skills. The repository folders are only for organization; Agora uses a flat namespace.

The Agora Skill name is the file name without the `.md` extension — for example `skills/research/multi-source-research.md` imports as `multi-source-research`, and `skills/android-development/android-dev-tdd.md` imports as `android-dev-tdd`. Add a short description when importing; that description is what `{skill_catalog}` shows.

Every file under `skills/` is a Skill except the author documentation — `skills/README.md`, `skill-catalog.md`, and `skill-format.md`; do not install those as runtime Skills. For a suggested installation order, see "Recommended first Skills" in `README.md`. Example Skills are optional.

## 5. Review access and permissions

Enable Skill access only when wanted. Review Memory, web, conversation, shell, MCP, and automation permissions separately. Shell access alone does not configure a device.

## 6. Test safely

Test a normal answer, a Skill read, a harmless Memory read, a research question, a denied destructive action, and a controlled shell operation. Inspect each result.
