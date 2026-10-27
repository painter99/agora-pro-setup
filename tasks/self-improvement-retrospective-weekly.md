# Task: weekly self-improvement retrospective

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

The weekly Reflector step of the self-improvement loop (see
`docs/29-self-improvement-loop.md`): collect signals from the last ~7 days and
propose up to 3 improvement deltas for Skills, memory, or harness scripts. The
task applies nothing — application happens in conversation with the operator,
after explicit approval.

## Schedule

Weekly (Sunday evening), before the repository-sync task.

## Reads

- the self-improvement Skill (procedure and boundaries) and the golden-task
  eval corpus from memory
- the escalation log, the eval log, previous retrospectives
- outputs of the scheduled tasks, the observability decision log and dashboard

## Workflow

1. Read the procedure and the eval corpus.
2. Collect signals: escalation triggers, eval runs, recurring corrections,
   stale Skills, memory contradictions, unresolved deltas from previous
   retrospectives, open decision-log recommendations and superseded chains,
   baseline+diff trends.
3. Evaluate and propose at most 3 deltas, each in a fixed table: id, what,
   evidence, proposed patch, risk, eval plan. Every delta gets a dated ID; a
   delta realizing a decision-log recommendation references it. Decision-log
   statuses are never changed by this task.
4. No evidence, no delta. Nothing found → the report says exactly that; never
   invent findings.
5. Save the report (dated) to the local retrospectives directory.
6. Send exactly one notification: findings count, delta count, report path.
7. Deliver a copy of the report and a refreshed copy of the eval log to the
   operator's delivery directory — the only permitted write there.

## Hard rules

- No writes to Skills or memory (read-only), no git commit or push, no
  task/loop management, no decision-log status changes.
- Shell only for reading, the report write, and the delivery copy; nothing in
  the delivery directory is moved, renamed, or deleted.
- The live report is written in the operator's language with a mechanical
  script-leak check before the write.
- An unavailable source is stated in the report and the run continues;
  uncertainty is marked, never invented.

## Delivery and notifications

- Report copy + refreshed eval-log copy to the delivery directory; exactly one
  notification with counts and path.

## Failure behavior

Failures are reported in the report and the notification; nothing fails
silently.

## Verification

Report exists, delivery copies present, notification count ≤ 1.