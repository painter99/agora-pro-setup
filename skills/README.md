# Agora Skills

This directory contains generic Markdown instructions intended for Agora's native Saved Skills library.

## Skill model

A Skill is a durable, user-owned instruction file with a name and optional short description. Agora exposes a compact catalog through `{skill_catalog}` when Skill access is enabled. The model reads a relevant Skill body on demand through `read_skill_file`.

There is no Active Skill singleton. Do not create an `active_skill.md`, an active-Skill toggle, or a parallel Skill execution pipeline.

## Skill versus Memory

- Skill: how to perform a recurring task.
- Saved Memory: information about a person, project, decision, or reference subject.
- Active Memory: compact context injected into requests.

## Installation

Import individual Markdown files into Agora's Skills settings. Give each Skill a short description suitable for the catalog. The repository directories are for human organization; Agora manages its own normalized flat Skill store.

## Rules

- One Skill should have one primary responsibility.
- Keep catalog descriptions short and concrete.
- Do not duplicate the entire System template.
- Declare dependencies by exact Skill filename when needed.
- State forbidden behavior and verification.
- Keep personal facts, preferences, and project state in Memory, not reusable Skills.
- Treat `skills/memory-governance/` as the hybrid memory-procedure family; import its files individually into Agora.
- Treat `skills/reasoning/` as reusable reasoning procedures; import each Skill individually and use it proportionally.
- Sequential Thinking means explicit planning and adaptive verification, not disclosure of private chain-of-thought.
- Never assume a Skill was applied before reading it.
- Do not put secrets or personal data in public example Skills.
