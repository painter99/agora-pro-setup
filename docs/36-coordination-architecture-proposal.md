# Coordination architecture — preservation draft

> Status: PROPOSED, NOT INDEPENDENTLY REVIEWED AFTER REVISION, NOT DEPLOYED.
> An earlier independent review of the underlying instance proposal failed;
> subsequent changes have not been independently reviewed. This document records
> ideas and outstanding decisions so they can be recovered after a session loss.
> It does not authorize dispatches, spending, transfers, repository changes, or
> changes to current policy. Check live instructions and permissions first.

## Purpose and relationship to existing records

This proposal extends the working-environment case study and shared bridge in
[doc 34](34-agora-goose-bridge.md) and the project-adaptation guide in
[doc 35](35-two-agent-operating-procedure.md). It explores a lightweight
coordinator, a coding agent, and an optional external research agent; it does
not replace either document's currently applicable contract. If an existing
contract conflicts with a proposed change here, do not silently choose one:
reconcile the actual authorities before operation.

The goal is to keep the conversation compact while preserving traceable work,
explicit approvals, independently verified outcomes, and recoverable decisions.
The operator remains in control. A brief summary is not a substitute for source
artifacts, and a model's assertion is not proof that an action succeeded.

## Proposed roles and flow

```text
Operator <-> coordinator <-> coding agent <-> project artifacts
                 |              ^
                 v              |
       optional research agent -+  findings as untrusted input
```

- **Coordinator:** intake, scope and approval checks, routing, independent
  verification of material claims, concise operator handoff, and recovery.
- **Coding agent:** project-scoped research, implementation and tests inside an
  authorized brief. It reports evidence and stops at reserved decisions.
- **External research agent:** optional, bounded research using explicitly
  approved inputs. Start with public information and return sources, dates,
  limitations, and unanswered questions. No access to a live checkout,
  credentials, private data, or repository write permissions by default.
- **Qualified reviewer:** separate fresh context, independent of the author,
  when review is required by the governing policy. Research-agent output and a
  coordinator checklist are not a substitute for a qualified review.

The operator is considering recurring project research with an external agent;
this describes repeated use during development, not an approved scheduler or
an existing integration. The coding agent would verify the relevant primary
sources and triage the findings before considering a change. Direct branch
creation or publication by the research agent is a separate, unapproved option.
A ban in a prompt is not an access boundary: verify the actual connectors,
sessions, filesystem and credentials exposed to the agent before any pilot.

## Task lifecycle — proposed

1. **Intake:** state the deliverable, scope, repository, applicable policies,
   acceptance criteria and operator-reserved decisions.
2. **Preflight:** inspect actual branch, base revision and dirty state; identify
   approved routes, impact, protected paths, access, spending and review gates.
3. **Brief:** specify scope, inputs, allowed tools and writes, output and
   evidence requirements, resource limits, forbidden actions and stop conditions.
4. **Execute:** use a bounded writer; preserve the evidence and do not overwrite
   existing logs. No concurrent writers on the same artifact.
5. **Verify:** inspect the actual diff and checks, and distinguish observed
   results from worker claims. Track failed and unavailable checks honestly.
6. **Review:** when required, review an immutable final snapshot in a fresh,
   qualified context. A changed artifact is not covered by an earlier verdict.
7. **Handoff:** report proposed, edited, tested, reviewed, committed, pushed
   and merged states separately, with outstanding decisions and recovery steps.

Scope, privacy, payment, publication, destructive actions and review remain
subject to their own applicable approvals. No role, general autonomy or model
route grants an action permission.

## Open decisions and gates

### Shared delegation accounting

A previous architecture review found that the budget and one-running-worker
limit were not operationally defined across channels. Older project material
and higher-priority anti-bypass rules must be reconciled. A conservative
candidate is one task-level ledger listing every delegated context, channel,
purpose, attempted count including failures and reviews, authorization, and
running state, with a pre-dispatch check. The definition of a new context,
applicable ceilings, cross-channel enforcement, and continuation semantics are
not yet approved or implemented. No channel may be used to evade a governing
limit. Uncertain accounting or mandatory review capacity means stop and report.

### External research, privacy and cost

Before sending anything externally: identify and inspect the exact payload,
recipient, attachments and logs; confirm scope-specific approval; verify what
accounts, files and connectors the execution environment can reach. If the
access boundary or permitted data is unknown, do not transfer. Protect retained
briefs, outputs and logs under the applicable data-classification rules.

The intended experiment is to use only non-paid credits. Before any call,
verify the actual account, API versus app credit behavior, spending controls,
automatic purchase settings and a usable stop condition. A credit balance is
not by itself a proven monetary ceiling or a per-request cost measurement.
The service's compliance statements are not a substitute for inspecting the
actual account's terms and access, and neither plan quality nor route cost is
assumed without relevant evidence.

### Records and current authority

The generic process belongs in this repository. Instance model assignments,
private paths, project-specific rules, operating state and actual credentials
stay in their respective private sources of truth. Model availability and UI
settings require live verification. Preserve historical decisions as history,
not active instructions. An approved project adapter maps this proposal to its
project only after the applicable shared contracts are reconciled.

## Proposed adoption and recovery

1. Reconcile role policy, bridge, project adapters, model records and scheduled
   settings; identify remaining conflicting instructions and ownership.
2. Preserve and compare original state evidence before correcting migrated
   records; do not erase source backups to simplify the account.
3. Treat experimental dispatch tools as untrusted until independently reviewed
   and tested; documentation warnings do not technically disable them.
4. Freeze the proposal and obtain one independent qualified review of the
   final architecture package. A failed review is not a pass; keep fix rounds
   bounded and review changed material as required.
5. Define one supervised pilot: fixed revision and scope, reproducible checks,
   baseline, measurable criteria, evidence locations, owner, stop triggers and
   authorized recovery. Start with one coding writer and a separate reviewer;
   do not add external research or nested workers until the relevant boundaries
   and accounting are resolved.
6. Separately assess a public-data-only external research pilot, without live
   repository access, after privacy, credit and authorization checks. Expand only
   from observed evidence and explicit approval where required.

On interruption, inspect existing jobs, repository state and retained evidence
before retrying. Stop on scope escape, unknown access, unverified cost control,
missing review, or failed acceptance. Preserve artifacts and report the exact
state; resume or restore only under the relevant authorized recovery procedure.

## Preservation and limits

This record captures architectural intent, not a complete instance backup.
The repository's public generic documentation cannot reconstruct private
configuration, credentials, project checkouts, current task settings, or
unpublished evidence. Keep those in appropriately protected, separately
recoverable stores with a tested restoration procedure. A local uncommitted file
or an unpushed branch is not an off-device backup. Commit, push, merge and
recovery are separate operations with their own approval and verification gates.
