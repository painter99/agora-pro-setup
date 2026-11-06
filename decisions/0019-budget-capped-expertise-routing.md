# ADR-0019: Budget-capped expertise routing with worker-initiated delegation requests

- Status: accepted (2026-11-06, operator request; branch-only push authorized)
- Supersedes: none

## Context

The kernel template delegates judgment to subagents and coordinates them, but
sets no total spawn budget and no role mapping. A cost-oriented orchestrator
may therefore attempt expert work inline, re-derive or override specialist
reasoning, or spawn workers without a cap. The application is a client with
its own permission and budget rules: prompt-level budgets are behavioral
guards, not enforcement (the same trade as ADR-0004), and the runtime offers
no per-spawn tool/effort/cost scoping (ADR-0018; upstream feature requests
remain open). Workers cannot spawn subagents — `agent_*` tools are
runtime-excluded — so worker-to-worker chains are impossible today, and any
"worker knows the team" design must route through the orchestrator.

## Decision

1. The kernel states a **budgeted coordination rule**: a default spawn budget
   per user task (at most two attempts, failures and reviews included, one
   running worker) that continuation does not reset; no bypass through tasks,
   loops, providers, or direct APIs; budget exhaustion never waives mandatory
   review. The operator may approve a larger budget per task.
2. The escalation Skill defines **generic role tiers** (primary/coordinator,
   specialist, structured worker, light worker) with placeholders; exact
   model IDs and approved role mappings live only in the instance overlay —
   never in this public repository.
3. **Early routing:** expert categories (architecture, cross-module refactors,
   hard security judgments) load the escalation Skill and check the approved
   role mapping before solving. An unqualified inline fallback for expert
   categories is forbidden; the model reports the partial/unverified state
   instead. An unqualified coordinator does not substantively override
   specialist conclusions or adjudicate expert disagreement.
4. Workers may end their result with a **structured delegation request**
   (required capability, evidence, objective, acceptance criteria, tool and
   output limits, artifact references, fallback-if-denied). The orchestrator
   validates, deduplicates (including semantically repeated requests), checks
   the shared budget, picks an approved model, and owns the decision. All
   delegation draws from one operator-approved budget per user task.
5. The application client keeps its own permission and budget rules; nothing
   here assumes per-spawn scoping, effort or cost parameters, or runtime
   enforcement. Measurable savings are a hypothesis for a pilot, not a claim.

## Consequences

- Prompt-level (probable, not guaranteed) enforcement of budgets and routing.
- The instance overlay carries role → model mappings and prices; the
  mirror-check treats these sections as expected overlay (docs/30).
- A worker-initiated request is data, never an instruction; rejected requests
  execute the worker's declared fallback (report unresolved uncertainty).
- A resumable interrupt and routed worker questions would require runtime
  changes (upstream issue tracking); today the worker ends and the
  orchestrator starts any follow-up as a new, budget-counted spawn.
