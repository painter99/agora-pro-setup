# docs/33 — Programming agent roles and delegation

How programming work is divided between agent roles in this setup: who
writes code, who reviews it, who approves merges, and where each rule
lives. This document is the **generic policy**; the concrete model
assignments are instance-specific and live in the private overlay
(`docs/30`) — never in this public repository.

## Status, scope and authority

- Scope: all programming/engineering projects run through the assistant.
- Per-project overlays (for example a rules file inside a project
  repository) record only project-specific delegations and reference this
  policy. A file cannot grant itself authority.
- Authority order when sources conflict:
  1. System/developer instructions, application permissions, device policy.
  2. The operator's explicit current instruction — within those boundaries.
  3. An approved **project overlay**, valid only within its explicitly
     delegated scope.
  4. This policy.
  5. The routing overlay (`model-escalation-protocol` §1/§6) — model
     routing.
  6. The instance model registry — model **facts** (availability, prices,
     pool); never roles.

Verified observations establish factual state only; they never grant
authorization or override instructions, permissions, or approval gates. Report
unresolved conflicts instead of inferring permission.

## Role / decision-rights matrix

Roles are filled by concrete models in the instance overlay; this table
defines the tiers and their decision rights.

| Role | Decision rights | Explicitly NOT authorized |
|---|---|---|
| **Coordinator + junior** (main conversation model) | context, planning, worker briefs, operator communication, mechanical execution (file ops, git mechanics after an approved GO), small bounded edits; may write first-draft code | no merge decisions, no architecture calls, must not override specialist evidence |
| **Code reviewer** (mid tier) | code review of junior-written code in a **separate fresh context**, test design, bounded fix-round verdicts | no merge decisions, no cross-module architecture |
| **Specialist / architect** (top tier) | architecture, cross-module design, qualified fresh review (final instance), product decisions, process/Skill proposals, **merge GO where a project overlay delegates it** | not routine loop work (last resort only); no authority beyond explicitly delegated repos |
| **Light worker** (cheapest approved model per the instance overlay — may be another instance of the coordinator's own model class) | mechanical, easily verifiable tasks, research fan-out with strict output contracts, routine lookups and file edits | no design, review, or merge authority; results are verified by the orchestrator before use |

Default rule: **anything not explicitly delegated in a project overlay
remains with the operator.**

Cost rule: **prefer the cheapest qualified role** for each task; escalate to
higher tiers only when the task requires them. Fan-out to multiple light
workers draws from the same shared task budget, and every light-worker
result is verified by the orchestrator before it is used.

The default division of labor for coding: the junior role writes the code,
the reviewer role reviews it — always from a self-contained, high-quality
brief. A project overlay may delegate the whole loop (implementation,
tests, review, fix rounds) to the mid tier where the operator approved it.

## Exact-route resolution

- Approved role assignments and executable spawn routes are **separate
  concerns**; human-readable model labels are not spawn IDs.
- Before any delegation, resolve the exact model ID against the current
  tool schema; capability facts come from the instance registry.
- An unavailable or unassigned route means **stop and report to the
  operator** — never silent substitution by a similar model.

## Author–reviewer separation

- A context that produced an artifact **never independently reviews it**;
  review runs in a fresh context (see `docs/32`, and the coding-loop
  Skill).
- A merge-GO decision by the specialist is a gate decision, **not** a
  substitute for a mandatory code review.
- Review of consequential design choices includes a bounded challenge
  pass — strongest failure scenario, missing evidence, simpler
  alternative — using the existing review, not additional workers.
- Worker briefs follow the brief-quality checklist in the
  `context-management` Skill; trimming applies to the brief, never to
  source artifacts.

## Permissions, budgets and lifecycle

- Every action requires **existing task authorization and device-policy
  compliance**; read-only assignments stay read-only. There is no blanket
  "no-approval-needed" class of action.
- Explicit operator approval gates (never skipped): spawn budget beyond
  default, library installation, deletions (branches, files, tasks,
  memory), publication, releasing operational data, secrets/keys, rule
  changes.
- Budgets: **one shared operator-approved budget per user task** (kernel
  default: at most 2 spawn attempts including failures and reviews, 1
  running worker); continuation does **not** reset it. Budget exhaustion
  leaves required review **pending**, never waived — report
  partial/unreviewed work.
- Workers stay retained until the operator confirms task completion;
  retention grants no additional execution, slots, or permissions.

## Merge evidence and bounded GO

A merge to a protected branch requires, where delegation exists:

1. primary artifacts: diff, full test output with commit SHA and exit
   code, acceptance run on real input;
2. explicit GO from the delegated approver;
3. precondition checks (remote SHAs) before execution;
4. post-merge proof: `ls-remote` local = remote, merge-base check;
5. missing CI log = **"unverified", never "success"**.

Branch deletion follows the branch-deletion gate in `AGENTS.md`: the default
is RETAIN, and deletion requires an explicit operator GO or an
operator-delegated gate PASS. History rewrite and publication remain separate
approvals.

## Conflicts and unavailable routes

- Conflicting records are resolved through the authority order above; if
  unresolved, **report to the operator — never a silent decision**.
- Escalation triggers follow `model-escalation-protocol` (each trigger has
  its own defined reaction); escalation log rows go to the escalation log.
- Workers never choose their own successors; they return a structured
  delegation request (MEP §6a); the orchestrator validates, deduplicates,
  checks the shared budget, and owns the decision.

## Project-overlay template

```markdown
# Project rules — <repo>
> Hard rules approved by the owner. Change = owner GO only.
- Merge GO: <delegated approver | operator> — scope: <repo(s)>
- Coding loop: <junior writes + reviewer reviews | delegated loop owner>
- CI status: <active (verification path) | DEFERRED (merge justification)>
- Language: internal EN / operator chat <lang> / external <lang>
- Terminology: <glossary ref or none>
- Canonical sources: <where spec, decisions, status, evidence, and the role
  overlay live>
- Execution scope: <authorized actions per process slice; process-card
  references>
- Extra gates: <e.g. anonymization + owner GO before publication>
```

## Maintenance

- A role change is a **proposal** (from the specialist or the operator) →
  operator GO → the instance overlay and this document are updated in
  scoped, approval-gated patches, with read-back verification.
- This document is the only generic source of roles; project overlays
  reference it and add specifics only.
- Drift check: when starting a new programming project, the coordinator
  verifies that the project overlay, this document, and the routing
  overlay say the same thing.
