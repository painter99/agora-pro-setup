# Two-agent operating procedure — generic adaptation guide

This guide helps a project adopt a two-agent workflow without making the shared
contract or the project's private configuration public. Replace every angle-
bracket placeholder with a locally approved value in the private adapter; do
not commit instance values here.

## Purpose and boundaries

This guide is for projects that use a coordinating agent and a coding agent to
work across a shared project repository. It describes a reusable operating
shape, not a claim that any particular setup has been measured or validated.

Keep three layers distinct:

1. **Public process guidance:** this document explains how to adapt and run the
   process at a high level.
2. **Shared Skill contract:** `agora-goose-bridge` and Part 2 of
   [`docs/34-agora-goose-bridge.md`](34-agora-goose-bridge.md) define the
   binding dispatch rules, brief, report, modes, tiers and delegation policy.
3. **Private project adapter:** the project's private notes supply local paths,
   topology, commands, permissions, and any approved deviations.

This document is not the normative dispatch contract, a replacement for
[`docs/32-coding-workflow.md`](32-coding-workflow.md), or a publication place
for private project configuration. Follow the shared contract for dispatch
requirements and the coding workflow for the single-agent implementation loop.

## Roles and authority

- **Coordinator:** routes the work, prepares the handoff, checks returned
  artifacts, and reports to the operator.
- **Coding agent:** works only within the authorized brief, verifies its own
  changes, and returns evidence and unresolved issues.
- **Operator:** owns decisions and approvals reserved to the operator, sets or
  confirms authorization, and receives the coordinator's report.

These role descriptions are orientation only. The binding division of labour,
authority boundaries, and delegation rules are in Part 2 of
[`docs/34-agora-goose-bridge.md`](34-agora-goose-bridge.md) and the
[`agora-goose-bridge` Skill](../skills/coordination/agora-goose-bridge/SKILL.md).

## Prerequisites and session setup

Before acting on a task:

1. Read the current repository instructions, working tree, relevant files, and
   applicable checks; distinguish observed state from any earlier summary.
2. Confirm that the task's authorization is current and covers its scope. If
   authority is absent or unclear, pause and ask the coordinator to resolve it
   with the operator.
3. Load only the task-relevant shared procedures and project context. Preserve
   source boundaries when transferring context; do not include secrets or
   unrelated private material.
4. Locate and resolve the project's private adapter at
   `<private adapter location>`. Check that it matches the current project and
   task; do not infer local commands or topology from this public guide.
5. Record the selected repository, branch or workspace, output location, and
   validation route in the authorized task record.

## The seven-step task cycle

Use this as a process outline. The dispatch contract in the Skill and
[`docs/34`](34-agora-goose-bridge.md) remains authoritative for how a dispatch
is formed and governed.

1. **Intake and routing.** Clarify the requested outcome, identify the owning
   repository and artifacts, and route the work according to the shared
   delegation policy.
2. **Mode and tier.** Select the dispatch mode and impact tier using the
   authoritative contract; confirm the required authorization before proceeding.
3. **Brief.** Prepare a complete, self-contained brief from the shared
   template. Its required fields and format are defined by the authoritative
   Skill contract; this guide does not duplicate them.
4. **One dispatch.** Send the authorized brief once through the approved route.
   Continuation or a changed scope follows the shared rules; it is not an
   implicit extension of the original authorization.
5. **Verification against artifacts.** Inspect the working tree, diff, and
   reproducible check output. Treat the returned report as claims to verify,
   not as verification itself.
6. **Recording in the same authorized change.** Update only the records and
   project artifacts covered by the authorization. Keep proposed decisions
   separate from decisions made by the operator.
7. **Operator report.** Give the operator a concise, evidence-based handoff
   using the shared report contract; state verified results, proposals,
   blockers, decisions needed, and the next action.

## Record matrix

Keep each record at its adapter-defined location. The placeholders below are
examples of location fields, not prescribed repository paths.

| Record | Purpose | When written | Placeholder location |
|---|---|---|---|
| Dispatch brief | Defines the bounded task and authorization context | Before dispatch; updated only through an authorized re-brief | `<brief location>` |
| Report and transcript | Preserves the worker's return and the coordinator's separate assessment; retain the transcript when the local policy requires it | After return and verification | `<report location>`; `<transcript location>` |
| Status | Shows current state, owner, blockers, and next action | At task start and when state changes | `<status location>` |
| Progress | Captures short-lived work completed, checks run, and remaining steps | During work when continuity or handoff needs it | `<progress location>` |
| Durable decision | Records an approved decision that should survive the session | After the authorized decision is made, using the project's governance process | `<decision record location>` |
| Change log | Summarizes user-visible project changes | With the same authorized change that introduces them | `<change log location>` |

Do not turn a proposal into a durable decision without the required approval.
The project adapter identifies the canonical record for each type and prevents
competing copies from becoming independent sources of truth.

## Service topology and lifecycle interface

Describe only the roles and data flow in this public guide. The project adapter
maps them to local services and approved operations:

- The **coordinator** receives the request and creates the bounded dispatch
  artifact.
- The **dispatch channel** transfers the brief to the coding agent without
  exposing credentials or unrelated context.
- The **coding environment** reads the authorized project state, performs the
  scoped work, and returns artifacts and evidence.
- The **verification path** lets the coordinator inspect those artifacts and
  reproduce the stated checks before reporting.

The adapter defines how to check readiness and how to start, stop, and inspect
status. Use placeholders in public examples, such as `<service start command>`,
`<service stop command>`, and `<service status operation>`. Never substitute a
real service name, executable, path, endpoint, host, or credential in this
guide. A lifecycle operation is not authorization to broaden the task.

## Escalation and stop rules

Stop the affected work and return to the coordinator when any of these applies:

- required authority, repository state, or task context is missing or ambiguous;
- the requested scope changes, a protected artifact is implicated, or the
  impact tier may increase;
- the authorized turn, time, or resource budget is exhausted;
- a required check fails, cannot be reproduced, or does not cover the claim;
- the next step requires a decision reserved to the operator;
- the private adapter conflicts with observed repository state or with a
  higher-priority instruction.

Preserve the current artifacts and report what is known, what is unverified,
and what authorization or evidence is needed. Do not silently widen scope,
retry beyond the approved bounds, or treat silence as approval. Apply the
binding escalation and re-brief rules in the shared Skill and `docs/34`.

## Session checklist

- [ ] Read current instructions and inspect the working state.
- [ ] Confirm current authorization, scope, and applicable impact tier.
- [ ] Resolve the private project adapter and its revision.
- [ ] Load only relevant context and protect private or sensitive material.
- [ ] Prepare and dispatch the complete authorized brief.
- [ ] Check returned claims against the actual artifacts and checks.
- [ ] Record status, progress, decisions, and changes at their canonical
      adapter-defined locations.
- [ ] Stop and escalate any scope, authority, budget, or verification issue.
- [ ] Prepare the operator card and identify any decision still needed.
- [ ] Leave the repository and session in the authorized handoff state.

## Operator card

Keep the final handoff compact and distinguish evidence from proposals:

- **Verified:** `<artifact or check>` and the observed result.
- **Proposed:** `<proposal>`; not yet an approved decision.
- **Blocked:** `<blocker>` and the evidence or authorization needed.
- **Decisions needed:** `<operator-owned question>` or `none`.
- **Next action:** `<owner>` — `<bounded next step>`.
- **Artifact locations:** `<brief>`, `<report>`, `<transcript>`, `<changed files>`,
  and `<validation evidence>` as applicable.

The project adapter may add a local field, but must not collapse the
coordinator's assessment into the coding agent's returned proposal.

## Adapting the guide safely

Keep the public base generic. A project-specific private adapter may contain
only the local information needed to operate the workflow: topology, lifecycle
operations, paths, repository-specific checks, record locations, permissions,
and explicit deviations. Store and distribute it under the project's own
privacy and access controls; do not copy private values back into this guide.

The adapter must point to the public base revision it follows, using the
project's chosen revision identifier, and name its local owner and review
trigger. When this base changes, compare the adapter against the new revision,
review each affected mapping, and update the private adapter deliberately.
Do not assume that a public-base change automatically changes local policy.
Keep the Skill contract and Part 2 of `docs/34` authoritative for dispatch
rules; record any approved project deviation only in the private adapter and
its authorized governance record.
