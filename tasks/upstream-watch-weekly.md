# Upstream Watch — Weekly

## Purpose
Track changes in the upstream application repository (releases, commits,
issue reactions, open pull requests) and report material deltas, so the
instance-side upgrade and feature-request posture stays current without
manual ad-hoc checks.

## Schedule
Weekly, once per week (the instance sets the exact slot); read-only.

## Reads
- Upstream releases feed (latest release and its assets)
- Upstream commit history since the previous check
- Status of tracked feature requests and bug reports (open/closed, new comments)
- Open pull requests awaiting maintainer review

## Workflow
1. Read the previous report and its pointer (last check date, last seen head).
2. Query the upstream feeds with plain read-only HTTP GETs; no credentials.
3. Diff against the previous report: new release? new commits? reactions on
   tracked issues? new or merged pull requests?
4. Classify each finding: MATERIAL (a release, a reaction to a tracked
   issue, a merged pull request) versus context (small commits, unrelated
   activity).
5. Write a dated report into the instance log directory, including an
   explicit "no changes" statement when nothing moved, and update the
   pointer for the next run.

## Hard rules
- Read-only toward all external systems; HTTP GET only, no authentication.
- No writes except the instance log directory and its pointer file.
- No edits to any repository, task, skill, or memory; no scheduled-task
  management; no user-interaction tools.
- Bounded budget: one pass, at most ~12 tool rounds; report and stop.
- Never fabricate issue or pull-request states; mark anything unreachable
  as UNVERIFIED.

## Delivery and notifications
- Notify only when a MATERIAL finding exists; otherwise stay silent
  (bounded notification budget, same pattern as the mirror check).
- A new upstream release is the highest-priority trigger: it starts the
  instance upgrade procedure.

## Failure behavior
- Feed unreachable or rate-limited: retry once with a pause, then write a
  report marked INSUFFICIENT ACCESS and notify at low priority.
- Missing previous pointer: proceed with a 7-day lookback and note it.

## Verification
- Report exists with the check date and per-feed results; pointer matches.
- Every claim in the report traces to a fetched feed (URL and timestamp).
