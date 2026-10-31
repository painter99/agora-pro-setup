# Task: weekly self-improvement retrospective

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

The weekly Reflector step of the self-improvement loop (see
`docs/29-self-improvement-loop.md`): collect signals from the last ~7 days and
propose up to 3 improvement deltas (plus at most 2 structural deltas from the
full Skills audit) for Skills, memory, or harness scripts. The
task applies nothing — application happens in conversation with the operator,
after explicit approval.

## Schedule

Weekly (Sunday night), before the skill-mirror-check and
repository-sync tasks.

## Reads

- the self-improvement Skill (procedure and boundaries) and the golden-task
  eval corpus from memory
- the escalation log, the eval log, previous retrospectives
- outputs of the scheduled tasks, the observability decision log and dashboard
- the Skills health state (full-audit baseline and last verdicts)
- the live task inventory (name, schedule, enabled state, model, prompt), when
  a task-listing tool is available

## Workflow

1. Read the procedure and the eval corpus, plus the Skills health state file.
2. Collect signals: escalation triggers, eval runs, recurring corrections,
   stale Skills, memory contradictions, unresolved deltas from previous
   retrospectives, open decision-log recommendations and superseded chains,
   baseline+diff trends, and the outcomes of deltas applied at least 7 days
   ago (helpful/harmful/neutral, appended to the eval log as `OUTCOME:`
   notes).
3. Evaluate and propose at most 3 signal deltas, each in a fixed table: id,
   what, evidence, proposed patch, risk, eval plan. Every delta gets a dated
   ID; a delta realizing a decision-log recommendation references it.
   Decision-log statuses are never changed by this task. A procedure
   performed 2–3 times in the same shape is a Skill candidate: propose it as
   a new Skill (format template, eval plan, trigger-precision check).
4. Full Skills audit (whole catalog every run): review every Skill against
   the skill-governance checklist (dependencies resolve, catalog description
   matches content, missing links, duplications and contradictions, stale
   content) plus the skill-evaluation questions (trigger precision,
   capability-uplift vs. encoded-preference, necessity) and a reduction lens
   (KEEP / MERGE / RETIRE verdicts with evidence and impact on dependents).
   Output: at most two additional structural deltas, marked `STRUCTURAL:`.
   Read-only toward Skills.
5. No evidence, no delta. Nothing found → the report says exactly that; never
   invent findings.
6. Save the report (dated) to the local retrospectives directory.
7. Send exactly one notification: findings count, delta count, report path.
8. Deliver a copy of the report and a refreshed copy of the eval log to the
   operator's delivery directory — the only permitted write there.
9. Self-review of this task's own prompt against the just-finished run: stale
   or renamed tools, steps that degraded or failed, budget overruns,
   contradictions, duplication. At most one `SELF:` delta; it may change only
   procedural aspects (tool names, step order, budgets, report format) — the
   permission scope (read/write boundaries, approval gates, hard rules) may
   only be tightened, never widened, and a widening SELF delta is invalid.
   "No self-delta" is a valid result.
10. Task audit (when a task-listing tool is available): map every live task
    (name, schedule, enabled state, model, prompt) and compare against the
    task cards, the night schedule, and the Skills catalog; findings form the
    `task-drift` category (card↔instance drift, ghost tasks, schedule
    collisions, tool-name drift in prompts). Read-only; corrections are
    proposals — application happens only after operator approval.

## Hard rules

- No writes to Skills or memory (read-only), no git commit or push, no
  task/loop management, no decision-log status changes.
- The task audit is read-only: tasks are listed and read, never created,
  deleted, or modified. Personal data seen in task prompts never reaches the
  repository; card porting stays with the repository-sync task (anonymized).
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