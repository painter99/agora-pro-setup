---
name: process-design
description: "Design and document repeatable, safe, and stable processes: specification-first workflow, process card template, verification gates, loud failure, rollback, and rendering of an external one-page methodology artifact."
license: MIT
---

# Skill: Process Design

## Catalog description

Design and document repeatable, safe, and stable processes: specification-first workflow, process card template, verification gates, loud failure, rollback, and rendering of an external one-page methodology artifact.

## Purpose

Turn ad-hoc procedures into repeatable, safe, and stable processes. A process that nobody can repeat is not a process: each procedure is designed as a specification with verifiable steps, an audit trail, and a recovery path. The skill also defines how to render the methodology as a one-page external artifact (for example for a job application or a client), derived from the same source so the two never diverge.

## Load when

- designing a new automated or semi-automated process (sweep, sync, report, delivery);
- converting an ad-hoc procedure that "works when I do it" into a documented, repeatable one;
- reviewing an existing process for safety, stability, or auditability gaps;
- preparing an external one-page methodology artifact derived from this methodology.

## Do not load when

- executing a one-off task with no reuse expected (verification discipline alone is covered by `tool-execution-contract`);
- maintaining or auditing Skills themselves (see `skill-governance`);
- scheduling recurring agent work (the scheduled-loops pattern is covered by docs/28; this skill designs the process such a task runs).

## Dependencies

- `tool-execution-contract` — verification, approval, and retry discipline for every step and tool call.

## Workflow

### 1. Frame before building

Write the specification before any implementation: trigger, inputs, outputs, owner, frequency, and failure modes. If the specification cannot state what "done" and "failed" look like, the process is not ready to build.

### 2. Decompose into idempotent steps

Each step is a script, flow, or documented command — never unrecorded manual clicking. A step is idempotent when running it twice yields the same state as running it once. Non-idempotent steps must be explicitly marked and gated.

### 3. Verify after every step

Each step defines its own check: row counts, checksums, control sums, a test run on dummy data, or a comparison against a baseline. A tool call or exit code 0 is not proof of success; the check is.

### 4. Gate irreversible actions

Anything destructive, irreversible, published, or spent requires a dry-run first, a backup or rollback path, and explicit approval bound to the exact scope. Structure beats agreement: prefer permissions and separation (test environment, read-only default, quarantine) over promises.

### 5. Make failure loud

Two distinct failure classes need two distinct detectors:

- "did not run at all" — a watchdog or health check on schedule or liveness;
- "ran but wrong" — step-level verification results in a log, with alerting on anomalies.

Silent success is the most dangerous state: a process that stops running must be noticed without a human remembering it.

### 6. Record state and audit trail

Keep a state file (what has been seen or processed), an append-only event log (what changed, when, with checksums), and versioned artifacts with backups before overwrites. The trail must allow reconstructing what happened and when.

### 7. Document as a process card

Capture the process in a process card (template below) stored next to the process. The card is the contract: update it in the same change as the process, or it drifts.

```text
# Process card: <name>
Trigger:      what starts it (schedule, event, manual)
Owner:        who is responsible
Frequency:    how often it runs
Inputs:       sources and where access lives (reference, never the secret itself)
Steps:        1..n — each idempotent, with the expected output
Verification: per-step checks plus the end-to-end check
Rollback:     how to undo or restore
Logs/state:   where state, logs, and artifacts live
Known risks:  top failure modes and their mitigations
```

### 8. Review cycle

On a regular cadence or after an incident: retrospective, proposed delta, approval, patch, then verification that the change actually improved the process. A process that never gets reviewed drifts from reality.

### 9. External rendering

When the methodology itself must be shared (job application, client, team), derive a one-page artifact from the same principles: audience language, no internal paths, no secrets, no personal data beyond what the recipient may see, generic examples. Run an identifier/privacy scan before sharing. Keep the external artifact derivable from this skill so the two never diverge.

## Forbidden behavior

- Never present an unverified run as success; never skip the per-step check.
- Never execute an irreversible step without dry-run, rollback path, and approval.
- Never store secrets, credentials, or personal identifiers in logs, cards, or shared artifacts.
- Never let the process card drift from the implementation; update both in one change.
- Never build a process whose failure modes are unknown — frame first.

## Verification

- Design stage: specification reviewed, failure modes listed, dry-run on dummy data passed.
- Runtime: per-step checks pass, the end-to-end check passes, and the watchdog confirms the run happened.
- Documentation: process card matches the implementation (updated in the same change); external artifact passes the identifier scan and fits one page.

## Output contract

- A specification and a process card for the designed process, with evidence of the dry-run.
- For a run: verification results, not just completion claims.
- For an external artifact: one page, audience language, scan-clean, traceable to this methodology.

## Related docs

- `docs/28-update-observability.md` — observability pattern for scheduled agent work (this skill designs the process; docs/28 measures it).
- `docs/29-self-improvement-loop.md` — the review cycle (step 8) as a formal loop.