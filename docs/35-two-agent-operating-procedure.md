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

This outline shows the shape of a dispatch from intake through operator
handoff. Each step also identifies the local information the private adapter
must supply; the named contract sections hold the binding rules.

1. **Intake and routing.** Clarify the outcome, owning repository, and relevant
   artifacts. The adapter supplies local ownership and routing context.
   Binding delegation and routing rules are in the Skill's **Delegation policy**
   and Part 2 of [`docs/34`](34-agora-goose-bridge.md), **Delegation policy**.
2. **Mode and tier.** Identify the kind of work and its impact category. The
   adapter supplies any local route or permission mapping. The Skill's
   **Workflow** and **Delegation policy**, and Part 2 of [`docs/34`](34-agora-goose-bridge.md),
   **Dispatch modes** and **Delegation policy**, define mode selection and
   authorization.
3. **Brief.** The brief captures the bounded work in a self-contained handoff.
   The adapter supplies local paths, protected artifacts, constraints,
   validation route, and output location. Required fields and dispatch setup
   are in the Skill's **Workflow** and Part 2 of [`docs/34`](34-agora-goose-bridge.md),
   **Brief and report contract**.
4. **Dispatch.** The brief travels through the project's approved channel with
   the local execution route and bounds supplied by the adapter. The Skill's
   **Workflow** and **Forbidden behavior**, and Part 2 of [`docs/34`](34-agora-goose-bridge.md),
   **Delegation policy**, govern dispatch, continuation, and re-briefing.
5. **Artifact verification.** The coordinator's inspection concerns the
   returned work, working tree, diff, and check evidence. The adapter supplies
   access paths and reproducible local check commands. Verification rules are
   in the Skill's **Workflow** and **Verification**, and Part 2 of
   [`docs/34`](34-agora-goose-bridge.md), **Brief and report contract**.
6. **Recording.** The record set follows the authorized work and its
   governance path. The adapter supplies canonical record locations, owners,
   and local retention conventions. Recording rules are in the Skill's
   **Workflow**, and Part 2 of [`docs/34`](34-agora-goose-bridge.md),
   **Decision log** and **Where the project-specific procedure lives**.
7. **Operator handoff.** The handoff summarizes the state of the work and the
   questions or next actions it leaves. The adapter supplies the destination
   and any local fields. The Skill's **Output contract** and Part 2 of
   [`docs/34`](34-agora-goose-bridge.md), **Brief and report contract**, define
   the report form.

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

For the binding rules on recording outcomes and operator-owned approvals, use
the Skill's **Workflow** and **Forbidden behavior**, and Part 2 of
[`docs/34`](34-agora-goose-bridge.md), **Decision log**. The project adapter
identifies the canonical record for each type and prevents competing copies
from becoming independent sources of truth.

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

The private adapter should let participants recognize situations that may need
escalation, including:

- missing or ambiguous authority, repository state, or task context;
- a scope change, a protected artifact becoming implicated, or a possible
  impact-tier increase;
- an exhausted authorized turn, time, or resource budget;
- a required check that fails, cannot be reproduced, or does not cover the
  claim;
- a next step that depends on an operator-reserved decision;
- a conflict between the private adapter, observed repository state, or a
  higher-priority instruction;
- an absent or unclear operator response.

For the binding response to these situations, use the Skill's **Workflow**,
**Delegation policy**, **Forbidden behavior**, and **Verification**, and Part 2
of [`docs/34`](34-agora-goose-bridge.md), **Delegation policy** and **Brief and
report contract**. The adapter supplies local escalation contacts, artifact
locations, and evidence routes.

## Session checklist

- [ ] Read current project instructions and inspect the working state.
- [ ] Resolve the private project adapter and note its revision.
- [ ] Confirm the adapter supplies local paths, permissions, validation routes,
      record locations, and any approved deviations.
- [ ] Load task-relevant context with its provenance and access boundaries.
- [ ] Identify the adapter-defined locations for the brief, report/transcript,
      status/progress records, decisions, and change log.
- [ ] Prepare the operator handoff with artifact locations and validation
      evidence; note any local fields the adapter adds to the operator card.
- [ ] For binding requirements on authorization, dispatch, verification,
      recording, escalation, stop conditions, and report format, use the named
      sections of the shared Skill and Part 2 of [`docs/34`](34-agora-goose-bridge.md).

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
