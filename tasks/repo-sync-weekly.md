# Task: weekly repository sync

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

Autonomously mirror the current reality of the agent stack (Skills,
documentation) into the public reference repository, under a standing operator
authorization. Everything committed is English, anonymized, and generic;
personal facts stay in local memory.

## Schedule

Weekly (Sunday night), after the retrospective and the mirror-check tasks.

## Reads

- local memory files with repository conventions and workflow gotchas
- the component inventory (manifest.yaml) and the task-card directory
- the self-improvement Skill and the local eval/retrospective logs
- the repository itself (pull, directory listing, the skill-format spec)

## Workflow

1. Read conventions and gotchas; map stack reality (skill catalog, logs, task
   list where available).
2. Map the repository: pull with fast-forward only, list directories, read the
   format specification.
3. Find up to 5 changes the repository does not reflect (a new or changed
   Skill without a current repository version, a new pattern without
   documentation, stale docs, a task card that no longer matches the live
   task instance). Every change needs evidence; without evidence, no change.
4. Manifest drift check: compare manifest.yaml against the actual tree
   (existence, glob counts) and against the deployed stack (components
   without repository coverage); update the inventory in the same change as
   the component it describes.
5. Repository-graph snapshot: rebuild the oriented graph of the repository
   (docs, Skills, task cards, decision records, scripts; edges from relative
   links, Skill dependencies, card-to-live-task bindings when a task-listing
   tool is available, and supersede chains) and overwrite the local
   observability artifact in the agent's log directory — it is never
   committed.
6. Write the English, anonymized, generic versions (Skills follow the
   skill-format spec).
7. Run ./scripts/check.sh and require exit 0 before the commit (hard `&&`);
   a failure = fix the change or drop the affected file, and note it in the
   run report.
8. Run the identifier scan over every changed file (names, projects, hardware,
   models, local paths, notification topics, ...). A hit = drop that file and
   note the drop in the run report.
9. Stage exactly the intended files; whitespace check; review the staged diff.
10. Commit with the repository identity; push to the default branch; verify
    the push (status + remote heads).
11. Verify the content actually arrived on the remote, and that the CI check
    run for the pushed head commit finished with conclusion=success.
12. Exactly one notification when something was synced (files, commit hash,
    state). No change = no commit, no push, no notification.

## Hard rules

- Scope: documentation, Skills, and task-card directories only; the inventory
  (manifest.yaml) and CHANGELOG.md are updated in the same change as the
  component they describe. No code, no CI workflows, no system-prompt
  templates, no decision records, no file deletion, no force-push, no history
  rewrite, no secrets or personal data.
- The repository-graph snapshot and the run report are local artifacts (the
  agent's log directory) — never committed to the repository.
- The repository is English, anonymized, generic — always.
- Uncertainty is marked, never invented; a missing proof means no change.
- A failed push is never retried with force; it is reported factually.
- No task/loop management; no notifications beyond the single one.

## Delivery and notifications

- Exactly one notification when something was synced; silence when nothing
  changed.

## Failure behavior

Every failure is reported factually; nothing fails silently.

## Verification

Remote content check (`git show`), CI-run check via the public API,
local/remote sync status.