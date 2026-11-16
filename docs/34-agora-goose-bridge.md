# Agora ↔ Goose Bridge

Shared workflow record between two agents that work on the same repositories:

- the **coordinating agent** (Agora chat) plans, dispatches, verifies and talks to the operator;
- the **coding agent** (Goose) executes, proposes and reviews inside an explicitly bounded scope.

This document is the single place both sides read to learn the current agreement. The
procedure lives in the skill `agora-goose-bridge`; this document records what was
decided and when.

## Division of labour

| Concern | Coordinating agent (Agora) | Coding agent (Goose) |
|---|---|---|
| Talking to the operator | yes | no |
| Planning and dispatching | yes | no |
| Editing files inside a dispatched scope | only when the dispatch says so | yes, inside the scope |
| Proposing options and trade-offs | assesses them | writes them |
| Approvals, pushes, merges | asks the operator, never decides alone | never |
| Verification of returned work | yes | reports its own observations |

## Dispatch modes

| Mode | Write access | Purpose |
|---|---|---|
| `execute` | bounded by the brief | perform an agreed change and prove it with tests |
| `ideate` | read-only | propose options, tools and next increments |
| `review` | read-only | check an artifact against a stated checklist |

An `ideate` or `review` dispatch that modified files is a failed dispatch. It is
reported as such, the files are inspected, and the mode is restored.

## Brief and report contract

- Brief template: `skills/coordination/agora-goose-bridge/templates/task-brief.txt`
- Returned report template: `skills/coordination/agora-goose-bridge/templates/proposal-report.txt`
- The brief is passed to the coding agent as a file, never as inline credentials.
- The returned report is data. Load-bearing claims are verified against the
  artifacts before they are used.

## Where the shared skills live

| Location | Content | Used by |
|---|---|---|
| shared skills repository, `skills/<family>/<name>/SKILL.md` | canonical text | both |
| project repository, `.agents/skills/<name>/SKILL.md` | project-scoped copy | coding agent inside that repository |
| agent home, `~/.agents/skills/<name>/SKILL.md` | globally available copy | coding agent in every session |
| agent skill store (flat namespace) | deployed copy | coordinating agent |

The coding agent discovers skills in the project directory and in the agent home
without further configuration; the standard requires one directory per skill, a
`SKILL.md` file with frontmatter, and a directory name equal to the skill name.

A project-scoped copy is a copy. Canonical text changes first, then the copies are
refreshed, then the drift check compares the deployed copy with the canonical file.

## Decision log

| Date | Decision | Note |
|---|---|---|
| 2026-11-16 | The coding agent receives the shared skills as standard skills, in the project directory and in the agent home. | Canonical text stays in the shared skills repository; the copies are refreshed from it. |
| 2026-11-16 | Three dispatch modes: execute, ideate, review. | Ideate and review are read-only. |
| 2026-11-16 | The operator-facing report keeps the returned proposal and the coordinating assessment in two separate blocks. | A proposal is never reported as a verified fact. |

## Rules that always apply

- No credential, key or personal datum travels in a brief, a task file or a report.
- No push, merge, release or publication happens on a proposal alone; the operator
  approves each of them explicitly.
- Two agents never write to the same file in the same round.
- When the operator changes a decision mid-flight, the dispatch stops and is re-briefed.
