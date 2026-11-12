# Task: daily drift watch (lite)

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

A lightweight daily detector of structural drift: git sync between the local
`main` and the remote `main`, a Skill count invariant across the repository,
the deployed Skill store and the Skills health state, and regeneration of two
observability graphs (repository graph and system-prompt evolution graph)
through validated scratch copies. Per-Skill content diffs are **not** part of
the daily run; they belong to the weekly skill-mirror-check task, which is the
authority for classifying and repairing content drift.

## Schedule

Daily, all seven days of the week (early morning).

## Reads

- the local repository clone: local `main` ref and the remote branch heads
  (`ls-remote`, no fetch, no pull)
- the repository `skills/**/SKILL.md` files (count only)
- the deployed Skill catalog (list only, no content reads)
- the Skills health state file (count recorded there)
- the repository-graph and system-prompt-history scripts (executed; read-only
  over the repository)

## Workflow

1. Git sync: compare the local `main` with the remote `main` head. If the
   remote cannot be read, record the result as unverified — never as a match.
2. Count invariant: repository `SKILL.md` count, deployed catalog count and the
   count recorded in the health state must agree. A missing source is a finding.
3. Repository graph: run the graph script with stdout redirected to a scratch
   file. Only on success, validate the scratch file (today's date, node-count
   line) and copy it to the observability snapshot; then verify the target. On
   any failure, do not copy — the previous snapshot stays.
4. System-prompt graph: the same pattern with the history script; validation
   checks non-empty output, today's date and the version-table heading.
5. Write the dated run log after steps 4 and 5, so it records their actual
   results ("in sync" only when every check passed).
6. Notification: only on a finding or an error. A run in sync sends nothing.

## Hard rules

- Writes are limited to the scratch directory, the dated run log, the two
  graph snapshots (after validation) and at most one notification.
- No Skill edits, no repository changes, no fetch, pull, push or commit, no
  task or loop management, nothing written to the delivery directory.
- The scripts are not modified without operator approval.
- Credentials, token configurations and environment files are never read.
- A check that cannot be verified is recorded as unverified, in the log and in
  the notification; silence is allowed only after a verified match.

## Delivery and notifications

- Dated run log in the local logs directory.
- At most one notification per run, only on a finding or an error (error =
  low priority).

## Failure behavior

A failed step is logged factually and reported; the run continues with the
remaining checks. A failed graph write never removes the previous snapshot.

## Verification

A run log exists for every run; notification count is at most one; no writes
outside the allowed paths; the count invariant is checked in every run.
