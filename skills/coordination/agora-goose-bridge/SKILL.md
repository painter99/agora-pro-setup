---
name: agora-goose-bridge
description: "Two-agent workflow between the Agora chat agent and a Goose coding agent: shared brief and proposal templates, three dispatch modes, the delegation policy with impact tiers, and the decision record both agents read."
license: MIT
---

# Skill: agora-goose-bridge

## Catalog description

Two-agent workflow between the Agora chat agent and a Goose coding agent: shared brief and proposal templates, three dispatch modes, the delegation policy with impact tiers, and the decision record both agents read.

## Purpose

The coordinating agent coordinates, talks to the operator and decides. The coding agent executes and proposes. This Skill defines the seam between them: what a brief must contain, which mode a dispatch uses, what the return value looks like, where the agreed workflow is recorded, and which work is delegated by default, so both sides work from one contract instead of two habits.
The operator talks to the coordinating agent only. The coordinating agent is the intermediary: it routes work to the coding agent, verifies what comes back and reports it. The coding agent never asks the operator a question directly and never reads silence as approval.

## Load when

- work around the project could be dispatched to the coding agent instead of being done locally or turned into an operator question;
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

## Delegation policy

The coding agent is the default route for project work. Dispatch first, ask the operator later.

| Tier | Typical work | Who authorises it |
|---|---|---|
| low | web research about the project, options analysis, documentation, tests, refactors without behaviour change, small isolated fixes | the coding agent proceeds inside the brief |
| medium | new features inside an existing module, behaviour changes without new dependencies, changes to the web UI or the live path | the coding agent proceeds; the coordinating agent confirms the brief and verifies the result |
| high | schema or contract changes, the evidence ledger or the checker, licence or ADR status, budget, hosting or publication, deletions, anything touching historical data | explicit confirmation by the coordinating agent or the operator before the dispatch starts |

Rules:
1. Research about the project is dispatched before the operator is asked anything. A question that a dispatch can answer is not an operator question.
2. The operator is asked only when the impact is high, when the decision is genuinely the operator's, or when a dispatch already produced the evidence that frames the question.
3. A high-impact increment is split into low and medium parts when that is possible, so the coding agent can do the groundwork while the confirmation is pending.
4. Every dispatch states its impact tier and the source of its authorisation in the brief and in the returned report.
5. A dispatch that crosses into a higher tier stops and is re-briefed; the tier never grows silently.
6. The operator is never asked to choose between options that a dispatch has not yet produced.

## Workflow

0. Route first. Before asking the operator anything, decide whether the coding agent can do the work: research, options analysis and low or medium increments are dispatched by default. Record the impact tier in the brief.
1. Choose the mode before writing anything.

   | Mode | Question it answers | Write access | Expected return |
   |---|---|---|---|
   | `execute` | Do the agreed change | allowed inside the stated scope | changed files, commands run, test result |
   | `ideate` | What else could be done, and better | read-only | proposal with options and trade-offs |
   | `review` | Is the artifact acceptable | read-only | findings against the stated checklist |

2. Write the brief from `templates/task-brief.txt` (the template ships with the canonical Skill; a flat store copy carries the Skill text only). A brief is complete when it states: goal, scope, protected files, constraints, acceptance criteria, permitted tools, output contract, forbidden actions, stop conditions. A missing field is written down as "not applicable" with a reason, never silently dropped.

3. Dispatch. The brief is passed as a file. The dispatch names the mode, the model route and the working directory, and it runs with a bounded turn count and a bounded budget.

4. Read the return value against the output contract of `templates/proposal-report.txt`. Verify every load-bearing claim against the artifacts — the working tree, the test output, the diff — not against the report text.

5. Report to the operator in three named parts: `Dispatched` (metadata), `Returned` (the coding agent's own words) and `Assessment` (the coordinating agent's own words). The two voices are never merged, and the assessment may contradict the proposal.

6. Record the outcome in the shared workflow record when a mode, a template, a route or a division of labour changes. The record is the place both agents read next time.

## Model routing and delegated subagents

The coding agent runs on a route chosen per dispatch. Which route is legal for which phase, and which
routes exist at all, is decided by the operator-approved role policy of the instance — this Skill
carries the procedure, not the route list, so the two sides never disagree about who may run what.

Rules that travel with every dispatch:

1. **The brief states the route and the role.** A dispatch that does not say which route runs it and
   under which role is incomplete; the coding agent uses the route it was given and never switches.
2. **The route set is small and fixed.** A route that is unavailable or unassigned is reported to the
   operator; it is never silently replaced by a similar model, and a missing route never becomes a
   reason to skip the review step.
3. **The author never reviews its own artifact.** A dispatch that changes files is reviewed by a
   SEPARATE dispatch in a fresh context, which receives the artifact, the goal, the constraints and
   the review checklist — not the author's reasoning.
4. **Delegated subagents are permitted only when the brief says so.** The brief names the
   sub-analyses, the numerical cap and the boundaries (no scope widening, no approvals, no merges, no
   operator questions). A delegated subagent inherits the parent's prohibitions and its model
   inheritance is not assumed to differ from the session's.
5. **A delegated subagent's output is evidence, not a verdict.** It may not stand in for the
   independent gate review, and it may not decide operator approvals.
6. **Route choice never widens scope.** A stronger route is not a licence for a larger task, a
   different acceptance criterion or an unapproved action.

## Forbidden behavior

- Never ask the operator a question that a dispatch could answer first.
- Never start a high-impact dispatch without the recorded confirmation.
- Never let a dispatch grow into a higher impact tier without a fresh confirmation.
- Never present the output of the other agent as verified fact.
- Never let the second agent decide operator approvals, merges or releases.
- Never place credentials, keys or personal data into a brief, a task file or a returned report.
- Never let both agents write to the same file in the same round.
- Never push or merge anything on the strength of a proposal alone.
- Never continue a dispatch after the operator's decision changed; re-brief instead.
- Never let a mode drift silently: an `ideate` dispatch that changed files is a failed dispatch, and is reported as such.

## Verification

- the brief carries every field of the template, or states why a field does not apply;
- the brief states the impact tier and the source of its authorisation;
- the returned report satisfies the output contract;
- every claimed change is visible in the working tree, and every claimed test result is reproducible;
- the operator-facing report separates proposal and assessment.

## Output contract

The coding agent returns one report in the shape of `templates/proposal-report.txt` (shipped with the canonical Skill, like the brief template).
The coordinating agent turns it into an operator-facing dispatch report with three parts:

1. `Dispatched` — mode, scope, model route, impact tier, authorisation source, artifact locations.
2. `Returned` — the returned report, quoted or summarized without silent editing. This block carries the sections of `templates/proposal-report.txt`; the coordinating agent does not rewrite them.
3. `Assessment` — what the coordinating agent verified, what it doubts, and the decision the operator still owes. The coding agent never writes this block.

## Related docs

Both references live in the shared skills repository, not inside a deployed copy
of this Skill. The canonical Skill directory is
`skills/coordination/agora-goose-bridge/` in that repository.

- `docs/34-agora-goose-bridge.md` — the shared workflow record read by both agents, and the case study of the two-agent working environment (Part 1).
- `skills/coordination/context-management/SKILL.md` — the brief construction rules this Skill relies on.
- The project-specific operating procedure lives in the project repository (for the AIPT project: `docs/collaboration-workflow.md`), together with the project adapter under `.agents/skills/`. The generic contract stays here; the project specifics stay there.
