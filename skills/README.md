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

Import individual `SKILL.md` files (one directory per Skill) into Agora's Skills settings. The frontmatter `description` is suitable for the catalog as-is. The repository directories are for human organization; Agora manages its own normalized flat Skill store.

## Rules

- One Skill should have one primary responsibility.
- Keep catalog descriptions short and concrete.
- Do not duplicate the entire System template.
- Declare dependencies by exact Skill name (the Skill's directory name) when needed.
- State forbidden behavior and verification.
- Keep personal facts, preferences, and project state in Memory, not reusable Skills.
- Treat `skills/android-development/` as the Android/Kotlin development family (spec-first, TDD, code review); import each Skill individually.
- Treat `skills/cad-development/` as the CAD/3D part development family (spec-driven workflow for AI-assisted modeling); import each Skill individually.
- Treat `skills/communication/` as the output-quality family (language fidelity for non-English user-facing output); import each Skill individually.
- Treat `skills/memory-governance/` as the hybrid memory-procedure family; import its files individually into Agora.
- Treat `skills/reasoning/` as reusable reasoning procedures; import each Skill individually and use it proportionally.
- Treat `skills/self-improvement/` as the agent self-improvement family (retrospectives, improvement deltas, evals, harness-level improvements); import each Skill individually.
- Treat `skills/coding/` as the generic coding family (goal-based coding loop with review and anti-reward-hacking guards); import each Skill individually.
- Place a new Skill in the family matching its primary responsibility; if no family fits, create a new directory and add its Treat line to this list.
- Sequential Thinking means explicit planning and adaptive verification, not disclosure of private chain-of-thought.
- Never assume a Skill was applied before reading it.
- Do not put secrets or personal data in public example Skills.

## Examples

`skills/examples/` contains two minimal Skills (`example-learning-skill`,
`example-project-skill`) demonstrating the format from
[`skill-format.md`](skill-format.md). They are optional teaching material —
import them only when useful, and never treat them as runtime requirements.
