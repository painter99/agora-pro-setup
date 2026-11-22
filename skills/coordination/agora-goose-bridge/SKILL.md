---
name: agora-goose-bridge
description: "Two-agent workflow between the Agora chat agent and a Goose coding agent: shared brief and proposal templates, three dispatch modes, the swarm role assignment, the coordination budget with spend discipline, the delegation policy with impact tiers, and the decision record both agents read."
license: MIT
---

# Skill: agora-goose-bridge

## Catalog description

Two-agent workflow between the Agora chat agent and a Goose coding agent: shared brief and proposal templates, three dispatch modes, the swarm role assignment, the coordination budget with spend discipline, the delegation policy with impact tiers, and the decision record both agents read.

## Purpose

The coordinating agent coordinates, talks to the operator and decides. The coding agent executes and proposes. This Skill defines the seam between them: what a brief must contain, which mode a dispatch uses, what the return value looks like, where the agreed workflow is recorded, and which work is delegated by default, so both sides work from one contract instead of two habits.
The operator talks to the coordinating agent only. The coordinating agent is the intermediary: it routes work to the coding agent, verifies what comes back and reports it. The coding agent never asks the operator a question directly and never reads silence as approval.

## Load when

- work around the project could be dispatched to the coding agent instead of being done locally or turned into an operator question;
- work is dispatched to the coding agent, to an external research agent, or to any other delegated context;
- the operator asks what the coding agent proposed, how the swarm roles divide the work, or how the dispatch budget is counted;
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

Goose is the default route for executable work that can be performed outside Agora, including repository, project, setup, system and mechanical tasks. Manus is optional only for explicitly approved public-data research within its free-tier gates. Short conversation and essential coordinator preflight, permission checks and verification stay direct. Ask only for missing essential information, operator-owned decisions or exact-action approvals; never ask for a resolvable technical choice.

| Tier | Typical work | Who authorises it |
|---|---|---|
| low | web research about the project, options analysis, documentation, tests, refactors without behaviour change, small isolated fixes | the coding agent proceeds inside the brief |
| medium | new features inside an existing module, behaviour changes without new dependencies, changes to the web UI or the live path | the coding agent proceeds; the coordinating agent confirms the brief and verifies the result |
| high | schema or contract changes, the evidence ledger or the checker, licence or ADR status, budget, hosting or publication, deletions, anything touching historical data | explicit confirmation by the coordinating agent or the operator before the dispatch starts |

Rules:
1. Route research to Manus only when its public-data, account, request, access, retention and free-credit gates are explicitly approved and verified; otherwise use an approved Goose route when authorized, or stop and report. No private data, credentials, paid usage, repository access or unapproved connectors go to Manus.
2. Ask for essential missing information, a genuinely operator-owned decision or the approval required for the exact action; high impact alone does not transfer a delegated decision back to the operator. Coordinator confirmation is valid only within delegated authority and never replaces operator approval reserved by platform, repository or action-specific gates.
3. A high-impact increment is split into low and medium parts when that is possible, so the coding agent can do the groundwork while the confirmation is pending.
4. Every dispatch states its impact tier and the source of its authorisation in the brief and in the returned report.
5. A dispatch that crosses into a higher tier stops and is re-briefed; the tier never grows silently.
6. Do not ask the operator to choose a technical option that can be resolved within delegated authority. Never postpone a necessary approval or essential clarification merely to dispatch first.

## Swarm roles and task assignment

Every dispatched context has a fixed role and a task class; the coordinating agent owns the assignment and the verification. This swarm pattern is repository policy adopted 2026-11-20; deployment unverified; the shared workflow record (`docs/34` in the setup repository) carries the same table, and a task class not listed for a tool needs a recorded decision before its first use.

| Role | Context | Task classes | Never does |
|---|---|---|---|
| coordinator | main chat | conversation, intake, scope and approval checks, compact briefs, bounded preflight, routing, targeted verification and operator reporting | routine implementation; qualified review of substantial artifacts; merge, publication, licence, identity, billing decisions |
| builder | Goose on the `<approved light worker>` role; the `<approved specialist>` role is reserved for last-instance escalation and qualified review | specification drafting, implementation, tests, setup, system work and bounded fix rounds | asking the operator directly, Agora subagents, Goose delegate subagents outside the brief caps, worker credential or secret access unless the exact action is explicitly operator-approved under applicable platform policy, committing or pushing unless the exact action is authorized |
| qualified reviewer | separate fresh dispatch on the `<approved specialist>` role, read-only | review of a final snapshot against a stated checklist | reviewing its own authorship; implementing; deciding operator approvals |
| mechanical worker | Goose `<approved light worker>` role when approved and sufficient | record shaping, bulk edits, format fixes, short summaries | qualified review, architecture calls, Agora subagents, Goose delegate subagents outside the brief caps |
| researcher | external research agent on its free tier | bounded public-data research with sources and dates; advisory digests | repository access, credentials, publication, paid usage, connectors unless separately verified and approved |

Assignment rules:
1. Every brief names the role of the context it dispatches. A brief without a role is incomplete.
2. Parallel dispatches are allowed only with disjoint scopes and no concurrent edits to the same artifact; each counts against the same task budget.
3. Manus is optional, free-tier-only and limited to explicitly approved public-data research. Record a new use class before first use; before each dispatch verify applicable account and request restrictions, access, connectors, retention and remaining credits, and check per-task consumption after each run. Report unexpected consumption. Never assume an instruction constrains the product; no paid usage is authorized.
4. The coordinating agent verifies every returned claim against artifacts before use, regardless of which role produced it.

## Coordination budget and spend discipline

For one operator-authorized task, allow at most **six new delegated-context attempts in total**, including failed starts and independent reviews, and at most **four running delegated contexts at once**. Every Goose or Manus shell-dispatch context, including an independent reviewer and every Goose delegate subagent, counts against the same task budget; do not create Agora subagents. Goose delegate subagents are permanently allowed by default for orchestrators on the light routes within the brief caps, and every delegate counts as an attempt. A failed start counts. A review attempt that times out without a verdict counts as the same review round retried, not a new round, within the shared attempt budget. Independent review is capped at **two rounds per task** within the shared budget; if required review remains incomplete at the cap, report UNREVIEWED, never done. A continuation of the same verified context does not reset its identity or the count. Uncertain accounting means stop and report, never restart at zero. The budget is never bypassed through scheduled tasks, loops, additional providers or direct APIs.

Spend rules that travel with every dispatch:

1. **Pre-flight scope check.** Before any implementation dispatch, run a cheap coordinator-side inspection of the touched modules and their readers or validators, so a dispatch cannot fail on a foreseeable scope conflict. A pre-flight check is cheaper than a failed start.
2. **Dispatch sizing.** Size every dispatch to finish inside its time bound. A dispatch killed by its bound is paid waste, and its unfinished state must be reconciled afterwards; split work that does not fit.
3. **Brief economy.** Briefs point to files and line ranges instead of ordering full-file reads, except that required independent reviewers must read the final contents of all touched files fully; turn bounds stay low without narrowing required review coverage.
4. **Cheapest qualified route.** The `<approved specialist>` role is reserved for qualified fresh-context review and last-instance escalation; default work and mechanical execution go to the `<approved light worker>` role, as resolved by the approved routing overlay. If the route, applicable budget or permissions are unknown or unavailable, stop affected execution and report rather than doing the work in Agora.
5. **Budget classification.** The provider-side cap is a fire-drill limit, never the working budget. Apply the operator's separate lower working allocations and classify coding/projects separately from necessary setup and system work. Unknown allowance or exceeded target means stop affected work and report; private amounts stay in the instance overlay.

### Parallel dispatch isolation (worktrees, 2026-11-21)

Parallel Goose dispatches that touch the same repository MUST each run in their own worktree created via `scripts/goose-worktree.sh`, and the brief pins the worktree path as the working directory. The coordinator merges each worktree's branch per owned-file scope and removes the worktree only after the merge is verified.

## Workflow

0. Route first. Keep conversation and essential coordinator checks direct; route executable work as above. Record the impact tier and authorization; ask when essential information or an exact-action approval is missing. Never silently substitute coordinator implementation for an unavailable route.
1. Choose the mode before writing anything.

   | Mode | Question it answers | Write access | Expected return |
   |---|---|---|---|
   | `execute` | Do the agreed change | allowed inside the stated scope | changed files, commands run, test result |
   | `ideate` | What else could be done, and better | read-only | proposal with options and trade-offs |
   | `review` | Is the artifact acceptable | read-only | findings against the stated checklist |

2. Write the brief from `templates/task-brief.txt` (the template ships with the canonical Skill; a flat store copy carries the Skill text only). A brief is complete when it states: goal, scope, protected files, constraints, acceptance criteria, permitted tools, output contract, forbidden actions, stop conditions, the time bound, and the delegated-subagent rule: Goose delegate subagents are allowed within the brief caps for orchestrators on the light routes, otherwise none; Agora subagents are always forbidden. A missing field is written down as "not applicable" with a reason, never silently dropped.

3. Dispatch. The brief is passed as a file. The dispatch names the mode, the model route and the working directory, and it runs with a bounded turn count, a bounded budget and a time bound it is sized to meet.

4. Read the compact return against the output contract of `templates/proposal-report.txt`. Keep full logs outside chat under applicable access and retention rules; inspect targeted evidence for every load-bearing claim — working tree, test output, diff — rather than trusting the report. Context usage is reduced where practicable, not eliminated.

5. Report to the operator in three named parts: `Dispatched` (metadata), `Returned` (the coding agent's own words) and `Assessment` (the coordinating agent's own words). The two voices are never merged, and the assessment may contradict the proposal.

6. Record the outcome in the shared workflow record when a mode, a template, a route, a role assignment or a division of labour changes. The record is the place both agents read next time.

## Model routing and delegated subagents

The operator-approved instance policy determines legal routes and roles; route availability alone proves neither qualification nor cost. Every brief states route, role, permissions, shared attempts, review rounds and running contexts, and review reserve. An unavailable or unassigned route, unknown budget or permissions, or exhausted allowance stops affected work; report instead of silently substituting a route or implementing in Agora.

Default roles (operator decision 2026-11-21, aligned 2026-11-21/22): work, coordination and implementation use the role assigned by the approved routing overlay; the `<approved specialist>` role is reserved for last-instance escalation and independent qualified review only. Agora subagents remain forbidden. A separate qualified fresh-context Goose shell dispatch reviews every file-changing dispatch and any other required final snapshot, independently of its author, within the shared budget. Supply the artifact, goal, constraints and checklist, not the author's reasoning. Review rounds carry reviewer diversity: the `<approved specialist>` role is never the only reviewer, and the light routes participate in review rounds only under an explicit operator-directed diversity decision recorded for that case; a light-route review round is valid only through that recorded decision. The authoritative route-qualification source is the instance role policy, whose reconciliation with these records is explicitly open; nothing here generalizes light-route review qualification. If review is unavailable report UNREVIEWED, never done. Route choice never widens scope, permissions or approvals.

Delegated subagents (Goose) — canonical delegation rule (2026-11-21, operator decision): an orchestrator dispatched on an approved light-worker route may use the Goose builtin `delegate` by default within the brief caps. Subagents use approved light-worker routes for swarm opinions, mechanical fan-out and checks, with small max_turns (3-6), restricted extensions and a working directory inside the parent working directory. A subagent cannot spawn further delegates. Subagent output is evidence, never a verdict or review, and never replaces qualified fresh-context review. Every delegate counts as an attempt against the shared task budget.

## Parallel review-and-fix pipeline (2026-11-21, operator decision)

For medium and complex changes, the review pipeline recorded in the `model-escalation-protocol` Skill applies: R1 qualified review (medium-high reasoning, exhaustive findings) → fix round → R2 review → final round → closure by one delegate, whose output is a proposal only. Parallel fan-out of fix and final rounds is allowed only with disjoint file ownership; when all findings sit in one file, the fix round is a single run. Review rounds carry reviewer diversity: the specialist route is never the only reviewer, and the light routes participate in review rounds only under an explicit operator-directed diversity decision recorded for that case; route qualification is governed by the instance role policy (see above). The coordinator retains the final decision, subject to operator-owned approvals. Simpler changes keep the single review round above. This section defines the parallel-run mechanics both agents apply inside the pipeline.

- **Frozen inputs and isolation.** Before dispatch, freeze one verified base revision and one immutable context pack for the round; all runs receive identical copies, including the operator decision summary, goal, relevant review findings and ownership map. Each run works in its own isolated writable worktree/copy based on that revision, with no shared writable artifacts (including test outputs, scratch files and logs). Do not use concurrent writes to a shared checkout as a substitute for isolation.
- **Ownership and drift.** Each brief names the exact files its run alone may create or modify. A run may write only those files. If its base or supplied context differs from the frozen inputs, or it touches/changes a foreign file, it stops; that run's output is discarded as evidence and reported as a scope/drift violation. The coordinator verifies ownership and base before integrating any result.
- **Forced reasoning aid.** Every parallel fix and final-run worker assigned the `<approved light worker>` role must load the `sequential-thinking-workflow` Skill and use the sequential-thinking MCP tool; this is unconditional, not an availability-based preference, and is stated in the brief. If either required resource is unavailable, stop and report rather than running without it. This requirement does not apply to low-budget closure delegates.
- **Result block and integration.** Each run ends with exactly these labeled fields: `APPLIED` (per-file changes and evidence), `PROPOSED-NOT-APPLIED` (proposal and reason), and `UNCERTAINTIES` (or `none`). The coordinator, or a designated final delegate performing only pre-authorized mechanical integration, integrates non-conflicting in-scope artifacts and reports what was integrated. Delegate output remains evidence/proposal only; it is never a verdict or final decision. If both runs propose changes to the same file, do not auto-merge: the coordinator decides the resolution. A proposal that widens scope or permissions is rejected.
- **Budgets.** Closure runs on a low thinking budget (at most medium) for latency and has no forced sequential-thinking MCP requirement. Parallel fix/final runs may use medium to high thinking budgets while still following the forced reasoning-aid rule above. All contexts count against the shared task budget; continuation does not reset an attempt.
- **Critical infrastructure.** When the change touches authentication, secrets, deploy keys, CI, system services, exchange or gateway components, parallel fan-out is forbidden: one qualified run plus the mandatory review rounds.

## Worker system protocol (2026-11-21, operator decision)

A mandatory system protocol governs every dispatched worker so that reasoning discipline, evidence-only output and the sequential-thinking audit are uniform across routes and roles. The protocol text lives at `templates/worker-system-protocol.txt` (with a `{MIN_THOUGHTS}` placeholder).

1. Every `goose run` dispatch MUST include `--system` with the content of `templates/worker-system-protocol.txt`, with `{MIN_THOUGHTS}` substituted by the brief's minimum (typically 3–4).
2. Every `delegate` subagent call MUST receive the protocol via the delegate `context` parameter (plus task-specific constraints in `instructions`).
3. Coordinator verification of every dispatch MUST include a log audit: the count of `sequentialthinking` occurrences in the run log must be greater than or equal to the brief's minimum; a miss is a failed verification.
4. Goose-only execution rule: Agora is an observatory and communication layer only. If the Goose route is unavailable or a dispatch cannot start, the coordinator stops the affected work and reports the blocker; it NEVER performs the delegated work itself. The only resumption lever is an explicit operator appeal for the specific case.

## Forbidden behavior

- Never ask the operator a technical question that can be resolved within delegated authority; ask when essential information or exact-action approval is missing.
- Never start a high-impact dispatch without the recorded confirmation.
- Never let a dispatch grow into a higher impact tier without a fresh confirmation.
- Never start an implementation dispatch without the pre-flight scope check of the touched modules and their validators.
- Never create Agora subagents; never authorize Goose delegate subagents outside the brief caps (light-route orchestrators only, small max_turns, no further delegates, evidence-only output); never substitute coordinator execution for a blocked route.
- Never present the output of the other agent as verified fact.
- Never let the second agent decide operator approvals, merges or releases.
- Worker credential or secret access is forbidden by default; an exception requires explicit operator approval of the exact action under applicable platform policy and is never assumed. Never place credentials, keys or personal data into a brief, a task file or a returned report.
- Never let both agents write to the same file in the same round.
- Never push or merge anything on the strength of a proposal alone.
- Never continue a dispatch after the operator's decision changed; re-brief instead.
- Never let a mode drift silently: an `ideate` dispatch that changed files is a failed dispatch, and is reported as such.

## Verification

- the brief carries every field of the template, or states why a field does not apply;
- the brief states the impact tier, the source of its authorisation, the time bound and the delegated-subagent rule (Goose delegate subagents allowed within the brief caps for light-route orchestrators, otherwise none; Agora subagents always forbidden);
- a pre-flight scope check of the touched modules and their validators preceded the dispatch;
- the number of delegated contexts used on the task is within the budget, and the accounting is recorded;
- the returned report satisfies the output contract;
- every claimed change is visible in the working tree, and every claimed test result is reproducible;
- the operator-facing report separates proposal and assessment.

## Output contract

The coding agent returns one report in the shape of `templates/proposal-report.txt` (shipped with the canonical Skill, like the brief template).
The coordinating agent turns it into an operator-facing dispatch report with three parts:

1. `Dispatched` — mode, scope, model route, impact tier, authorisation source, artifact locations.
2. `Returned` — the compact returned report, quoted or summarized without silent editing; full logs remain outside chat under applicable access and retention rules. This block carries the sections of `templates/proposal-report.txt`; the coordinating agent does not rewrite them.
3. `Assessment` — what the coordinating agent verified, what it doubts, and the decision the operator still owes. The coding agent never writes this block.

## Related docs

Both references live in the shared skills repository, not inside a deployed copy
of this Skill. The canonical Skill directory is
`skills/coordination/agora-goose-bridge/` in that repository.

- `docs/34-agora-goose-bridge.md` — the shared workflow record read by both agents, including the swarm role table and the lessons from the full-cycle day.
- `docs/37-spend-observability.md` — the spend policy the budget section implements.
- `skills/coordination/context-management/SKILL.md` — the brief construction rules this Skill relies on.
- The project-specific operating procedure lives in the project repository (for a specific project: `docs/collaboration-workflow.md`), together with the project adapter under `.agents/skills/`. The generic contract stays here; the project specifics stay there.
