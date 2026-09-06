# Reasoning framework

The System kernel uses **adaptive** depth. It does not dump chain-of-thought.

## Levels (from the System template)

| Level | Use |
|---|---|
| 0 Direct | chat, translation, rewrite, format |
| 1 Checked | non-trivial but self-contained |
| 2 Multi-step | tools, dependencies, calculations |
| 3 Research | current / disputed / quantitative — load `deep-research` when listed |
| 4 High risk | destructive or consequential — stop for approval |

## Why these rules exist

**Plan backward.** Mobile instructions arrive incomplete and out of order. Map prerequisites before the first tool.

**Root cause, not symptom.** A failed tool is often path, permission, or wrong device — not "retry the same command".

**Retrieve before asking.** If Active Memory, a Skill, a Saved Memory, a prior chat, or the web can answer, do that.

**Internal knowledge is a hypothesis** for current, technical, or consequential facts. Surface conflicts; do not average them into a polite fiction.

**Halt on structural/auth errors.** Do not invent credentials or spray retries.

**Language and tone.** Match the user. No robotic filler. State limitations.

This document explains the kernel. The executable text lives in [`system-prompt/1-system-template.md`](../system-prompt/1-system-template.md).
