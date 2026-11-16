---
name: agora-goose-bridge
description: "Two-agent workflow between the Agora chat agent and a Goose coding agent: shared brief and proposal templates, three dispatch modes, and the decision record both agents read."
license: MIT
---

# Skill: agora-goose-bridge

## Catalog description

Two-agent workflow between the Agora chat agent and a Goose coding agent: shared brief and proposal templates, three dispatch modes, and the decision record both agents read.

## Purpose

The coordinating agent coordinates, talks to the operator and decides. The coding agent executes and proposes. This Skill defines the seam between them: what a brief must contain, which mode a dispatch uses, what the return value looks like, and where the agreed workflow is recorded, so both sides work from one contract instead of two habits.

## Load when

- work is dispatched to the coding agent;
- the operator asks what the coding agent proposed, or how the two sides divide the work;
- a dispatch mode, a brief template or the decision record changes.

## Do not load when

- the task stays inside one agent;
- a plain repository edit is done directly, without a second agent involved.

## Dependencies

- `context-management` — the brief arrives as a handoff and is verified against live sources.
- `tool-execution-contract` — inspection, approval and verification discipline for the dispatch itself.
- `model-escalation-protocol` — the model route of the dispatch and its escalation rules.
- `spec-first` — the contract of an increment, when the dispatch implements one.
- `code-review` — the independent review of a returned artifact.

## Workflow

1. Choose the mode before writing anything.

   | Mode | Question it answers | Write access | Expected return |
   |---|---|---|---|
   | `execute` | Do the agreed change | allowed inside the stated scope | changed files, commands run, test result |
   | `ideate` | What else could be done, and better | read-only | proposal with options and trade-offs |
   | `review` | Is the artifact acceptable | read-only | findings against the stated checklist |

2. Write the brief from `templates/task-brief.txt`. A brief is complete when it states: goal, scope, protected files, constraints, acceptance criteria, permitted tools, output contract, forbidden actions, stop conditions. A missing field is written down as "not applicable" with a reason, never silently dropped.

3. Dispatch. The brief is passed as a file. The dispatch names the mode, the model route and the working directory, and it runs with a bounded turn count and a bounded budget.

4. Read the return value against the output contract of `templates/proposal-report.txt`. Verify every load-bearing claim against the artifacts — the working tree, the test output, the diff — not against the report text.

5. Report to the operator in two separate blocks: what the coding agent proposed, and the assessment of the coordinating agent. The two voices are never merged, and the assessment may contradict the proposal.

6. Record the outcome in the shared workflow record when a mode, a template, a route or a division of labour changes. The record is the place both agents read next time.

## Forbidden behavior

- Never present the output of the other agent as verified fact.
- Never let the second agent decide operator approvals, merges or releases.
- Never place credentials, keys or personal data into a brief, a task file or a returned report.
- Never let both agents write to the same file in the same round.
- Never push or merge anything on the strength of a proposal alone.
- Never continue a dispatch after the operator's decision changed; re-brief instead.
- Never let a mode drift silently: an `ideate` dispatch that changed files is a failed dispatch, and is reported as such.

## Verification

- the brief carries every field of the template, or states why a field does not apply;
- the returned report satisfies the output contract;
- every claimed change is visible in the working tree, and every claimed test result is reproducible;
- the operator-facing report separates proposal and assessment.

## Output contract

The coding agent returns one report in the shape of `templates/proposal-report.txt`.
The coordinating agent turns it into an operator-facing dispatch report with three parts:

1. `Dispatched` — mode, scope, model route, artifact locations.
2. `Returned` — the returned report, quoted or summarized without silent editing. This block carries the sections of `templates/proposal-report.txt`; the coordinating agent does not rewrite them.
3. `Assessment` — what the coordinating agent verified, what it doubts, and the decision the operator still owes. The coding agent never writes this block.

## Related docs

- `docs/34-agora-goose-bridge.md` — the shared workflow record read by both agents.
- `skills/coordination/context-management/SKILL.md` — the brief construction rules this Skill relies on.
