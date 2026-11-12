# Task: monthly repository architecture audit

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

A read-only architecture audit of the whole setup repository as one system:
cross-layer consistency between README, overview, agent entry point and
manifest; documentation structure; system-prompt template size and growth;
Skill family structure; task-card coverage; and complexity. The audit
produces a report with at most five change candidates, each with evidence and
an effort/benefit estimate. Every candidate is a proposal awaiting operator
approval. The report is the architectural input for the weekly
self-improvement retrospective.

## Schedule

Monthly, according to the stored schedule of the live task. The day-of-month
and day-of-week combination is not verified; the task must not infer the
exact run date or treat a cron expression as proof that a run completed.

## Reads

- the repository clone: working-tree state, current branch, `HEAD` log entry,
  directory listings, manifest, agent entry point, README and overview
- the decision log of the observability task (read-only)
- the Skills health state and the system-prompt history graph (read-only)
- the task inventory snapshot, with its age stated; the live task listing when
  such a tool is available
- pending-delta notes in the local retrospectives directory, when present

## Workflow

1. Context: list the previous audit reports and read the newest one for trends;
   do not repeat findings already closed.
2. Preflight, fail-closed: check the working-tree status and the current
   branch. A fast-forward pull on `main` runs only when both checks succeed,
   the tree is clean and the branch is exactly `main`. In every other case no
   pull is attempted and the audit states the age of the local state.
3. Architecture audit (whole repository): cross-layer consistency, sampled
   claim checks against the real tree, documentation numbering and links,
   template size and monthly growth, Skill family structure (structure only;
   content audit belongs to the retrospective), task-card coverage against the
   live listing, and complexity by layer.
4. Budget: a bounded number of tool rounds; truncated content is marked
   unverified rather than audited. Every finding needs evidence (file, line or
   command output). No evidence, no finding.
5. Report: unique run ID, collection date and time with time zone, run mode
   (manual, scheduled or not determined). Final status is COMPLETE (the
   prescribed scope was covered), PARTIAL (usable, with named gaps) or FAILED
   (no usable audit). Save only as a new file; never overwrite an existing
   report. Include a "Handoff for the retrospective" section with source IDs,
   existing decision-log references, evidence, limits and the decision needed.
6. Delivery: verify the saved report by reading it back in full and comparing
   identity and content (checksum recommended). Copy it to the delivery
   directory as a new file only after that verification. Report save, copy and
   notification states separately; never report delivery that was not verified.
7. Notification: at most one attempt per run, including errors (default
   priority; low priority with the error and the actual save and delivery
   state).

## Hard rules

- Read-only toward the repository and the system. The only permitted repository
  change is a fast-forward pull under the preflight above. No commits, pushes,
  file edits, deletions, Skill or memory writes, or task/loop management.
- Writes are limited to the audit report directory, the delivery directory
  (one copy of a verified report) and at most one notification.
- Decision-log statuses are never changed by this task.
- Credentials, token configurations and environment files are never read.
- Nothing is invented; unavailable sources are stated and the run continues.

## Delivery and notifications

- Report in the local audit directory; verified copy in the delivery directory.
- One notification per run, with finding and candidate counts, run ID and the
  real report path.

## Failure behavior

Preflight or pull failures are reported with the actual repository state.
Unreadable or unverifiable sections are listed as gaps, which can make the
status PARTIAL or FAILED. Save or delivery failures are reported separately and
no unverified copy is delivered.

## Verification

A report with a run ID and collection time exists; the delivered copy matches
the saved report; notification count is at most one; no writes outside the
allowed paths.
