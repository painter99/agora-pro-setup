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

Tool names quoted inside the System template (for example `skill_read` in the memory gate) must match the installed app version. They were verified against the maintained instance on 2026-10-31 (app v2.2.x, canonical `memory_*`/`skill_*` names); if your app version renamed tools, adjust the quoted names at import time.

## 2. Add runtime variables

Place the Skill Catalog explicitly in the System template:

```text
{skill_catalog}
```

A variable is not necessarily available when its access setting is disabled. Confirm the current Agora version and settings. The maintained instance runs file-based active memory instead of the injected `{active_memory}` (see `docs/4`); an operator preferring the injected feature keeps that variable instead.

## 3. Configure file-based active memory

Create the working state file on a persistent host the agent reaches with file tools, and put its path into the System pointer sentence (see `docs/4`). Keep it short; do not copy complete Skills into it. The instance path is instance-specific (`docs/30`) and never committed to this repository.

## 4. Install Skills

Import selected `SKILL.md` files from `skills/` into Agora's Saved Skills. The repository folders are only for organization; Agora uses a flat namespace.

Each Skill lives in the Agent Skills layout — one directory per Skill containing a `SKILL.md` (frontmatter + body), see `skills/skill-format.md`. The Agora Skill name is the Skill directory name — for example `skills/research/multi-source-research/SKILL.md` imports as `multi-source-research`, and `skills/android-development/android-dev-tdd/SKILL.md` imports as `android-dev-tdd`. The frontmatter `description` is what `{skill_catalog}` shows; keep it identical to the body's `## Catalog description` (the format check enforces this).

Every `SKILL.md` under `skills/` is a Skill; the author documentation — `skills/README.md`, `skill-catalog.md`, and `skill-format.md` — is not a Skill and must not be installed as one. For a suggested installation order, see "Recommended first Skills" in `README.md`.

## 5. Review access and permissions

Enable Skill access only when wanted. Review Memory, web, conversation, shell, MCP, and automation permissions separately. Shell access alone does not configure a device.

## 6. Test safely

Test a normal answer, a Skill read, a harmless Memory read, a research question, a denied destructive action, and a controlled shell operation. Inspect each result.

Host-level services (MCP servers, exchange watcher) are a separate, optional layer: see `docs/31-platform-layer.md` and the host walkthrough in `docs/23`.
