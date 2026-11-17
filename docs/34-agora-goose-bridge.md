# Agora ↔ Goose Bridge

Shared workflow record between two agents that work on the same repositories:

- the **coordinating agent** (Agora chat) plans, dispatches, verifies and talks to the operator;
- the **coding agent** (Goose) executes, proposes and reviews inside an explicitly bounded scope.

This document is the single place both sides read to learn the current agreement. The
generic dispatch contract lives in the skill `agora-goose-bridge`; the
project-specific operating procedure lives in the project repository. This
document records what was decided and when.

## Division of labour

| Concern | Coordinating agent (Agora) | Coding agent (Goose) |
|---|---|---|
| Talking to the operator | yes | no |
| Planning and dispatching | yes | no |
| Editing files inside a dispatched scope | only when the dispatch says so | yes, inside the scope |
| Proposing options and trade-offs | assesses them | writes them |
| Approvals, pushes, merges | asks the operator, never decides alone | never |
| Verification of returned work | yes | reports its own observations |

## Delegation policy
The coding agent is the default route for project work. The operator is asked
only after a dispatch, or for decisions that are genuinely the operator's.
The coordinating agent is the intermediary: the operator talks to it, and the
coding agent never asks the operator directly.

| Tier | Typical work | Who authorises it |
|---|---|---|
| low | web research about the project, options analysis, documentation, tests, refactors without behaviour change, small isolated fixes | the coding agent proceeds inside the brief |
| medium | new features inside an existing module, behaviour changes without new dependencies, changes to the web UI or the live path | the coding agent proceeds; the coordinating agent confirms the brief and verifies the result |
| high | schema or contract changes, the evidence ledger or the checker, licence or ADR status, budget, hosting or publication, deletions, anything touching historical data | explicit confirmation by the coordinating agent or the operator before the dispatch starts |

A dispatch states its tier and the source of its authorisation in the brief and
in the returned report. A dispatch that crosses into a higher tier stops and is
re-briefed. A high-impact increment may be split into low and medium parts so
the groundwork can proceed while the confirmation is pending.

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
| 2026-11-16 | The operator-facing report has three named parts — `Dispatched`, `Returned`, `Assessment` — and keeps the returned proposal and the coordinating assessment as two separate voices. | A proposal is never reported as a verified fact. |
| 2026-11-17 | The coding agent is the default route for project work; the operator is asked only after a dispatch or for operator-owned decisions. | Operator instruction: research and small increments go to the coding agent first. |
| 2026-11-17 | Impact tiers decide who authorises a dispatch: low and medium proceed inside the brief, high needs explicit confirmation by the coordinating agent or the operator. | Operator instruction: the coordinating agent is the intermediary for everything around the project. |
| 2026-11-17 | The operator talks to the coordinating agent only; the coding agent never asks the operator directly and never reads silence as approval. | Operator instruction. |

## Where the project-specific procedure lives
The shared skill keeps the generic contract: the brief and report templates,
the dispatch modes and the delegation policy with impact tiers. The operating
procedure of one project — its task cycle, its record discipline, its service
topology and its stop rules — belongs to that project's repository, not here.
For the AIPT project it is `docs/collaboration-workflow.md`, read together
with the project adapter `.agents/skills/aipt-project-workflow/`. Neither side
copies the other: a change to the contract changes this repository and is
refreshed into the project copies, and a change to the project procedure
changes the project repository only.

## Rules that always apply

- No credential, key or personal datum travels in a brief, a task file or a report.
- No push, merge, release or publication happens on a proposal alone; the operator
  approves each of them explicitly.
- Two agents never write to the same file in the same round.
- When the operator changes a decision mid-flight, the dispatch stops and is re-briefed.
