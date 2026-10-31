# Task: daily drift watch (lite)

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

A fast daily detector of drift between the three Skills layers: the public
repository (source of truth for Skill texts), the deployed Skill store, and
the checked-out repository clone on the host. It complements the weekly
skill-mirror-check task, which remains the authority for classifying drift
direction and repairing it; this task only detects that something differs,
before the weekly window closes. Layers covered: repository ↔ deployed store ↔
remote `main` vs. local `main`.

## Schedule

Daily (early morning), Monday–Saturday; Sunday is covered by the weekly
mirror-check run.

## Reads

- the deployed Skill store (catalog list and per-Skill content reads)
- the repository checkout, its `skills/**/SKILL.md` files
- remote branch heads and the local `main` ref (`ls-remote`, no fetch)
- the Skills health state file (count invariant)

## Workflow

1. Count and hash: list the deployed Skills, write each content copy to a
   scratch directory, hash both sides and diff them.
2. Compare counts: deployed Skills == repository `SKILL.md` files == the count
   recorded in the Skills health state.
3. Compare `main`: remote branch head vs. the locally checked-out `main`.
4. Classify: everything identical → silence; any difference (content drift,
   count mismatch, branch mismatch) → exactly one notification with the
   finding and the run log path. Cosmetic-only differences are still
   reported — the weekly mirror-check classifies them.
5. Write the dated run log (findings, or "in sync") to the local logs
   directory.

## Hard rules

- Read-only except: the scratch directory, the dated run log, and at most one
  notification. No Skill edits, no repository changes, no fetch/pull/push, no
  task management.
- Silence is the expected result; a finding or an error each sends at most one
  notification (error = low priority).
- A difference that does not reproduce on re-read is a transcription artifact:
  re-read before reporting any drift.
- Failures are reported in the run log; nothing fails silently.

## Delivery and notifications

- Dated run log in the local logs directory; at most one notification, only on
  a finding or an error.

## Failure behavior

A failed step (unreadable skill, failed diff) is logged factually and
reported; the run continues with the remaining checks.

## Verification

Run log exists for every run; notification count ≤ 1; no writes outside the
scratch and log paths; the count invariant checked in every run.