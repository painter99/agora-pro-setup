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
   Respect pagination and verify the tracked pull request directly; absence
   from the open list does not prove closure or merge.
3. Diff against the previous report: new release? new commits? reactions on
   tracked issues? new or merged pull requests?
4. Classify each finding: MATERIAL (a release, a reaction to a tracked
   issue, a merged pull request) versus context (small commits, unrelated
   activity).
5. Write and read back a dated report including per-feed evidence. Update the
   pointer to the collection start only after the report is verified and all
   mandatory feeds and required comments are complete. Partial or unverified
   collection leaves the pointer unchanged.

## Hard rules
- Read-only toward all external systems; HTTP GET only, no authentication.
- No writes except the instance log directory and its pointer file.
- No edits to any repository, task, skill, or memory; no scheduled-task
  management; no user-interaction tools.
- Bounded budget: one pass, at most ~12 tool rounds; report and stop.
- Never fabricate issue or pull-request states; mark anything unreachable
  as UNVERIFIED.

## Delivery and notifications
- At most one notification attempt, including failures: material findings take
  priority; a partial run without material findings uses low priority. A fully
  verified run without material findings is silent.
- A new upstream release is a high-priority notice to the operator; it does
  not start an upgrade.

## Failure behavior
- Feed unreachable or rate-limited: retry once with a pause, then write a
  report marked INSUFFICIENT ACCESS and notify at low priority.
- Missing previous pointer: proceed with a 7-day lookback and note it.

## Verification
- Report read-back confirms the check date and per-feed results; the pointer
  advances only after a fully verified collection.
- Every claim in the report traces to a fetched feed (URL and timestamp).
