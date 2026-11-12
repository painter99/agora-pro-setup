# Task: weekly repository sync

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

Prepare a local topic-branch proposal reflecting the current reality of the
agent stack (Skills, documentation, task cards) in the reference repository.
Publication and merge require separate operator action and approval. Everything committed is English, anonymized, and generic;
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
2. Verify clean `main`, local and remote refs and absence of an outstanding
   proposal before a fast-forward-only pull; otherwise stop without switching,
   stashing or resetting. Record the base and map the repository.
3. Find up to 5 changes the repository does not reflect (a new or changed
   Skill without a current repository version, a new pattern without
   documentation, stale docs, a task card that no longer matches the live
   task instance). Every change needs evidence; without evidence, no change.
4. Manifest drift check: compare manifest.yaml against the actual tree
   (existence, glob counts) and against the deployed stack (components
   without repository coverage). Inventory and changelog are outside this
   task's write scope; report required changes rather than making them.
5. Graph snapshots are owned by the daily drift-watch task; do not regenerate
   them here.
6. Create a unique local topic branch from the verified base and write the
   English, anonymized, generic versions (Skills follow the format spec).
7. Run ./scripts/check.sh and require exit 0 before the commit (hard `&&`);
   a failure = fix the change or drop the affected file, and note it in the
   run report.
8. Run the identifier scan over every changed file (names, projects, hardware,
   models, local paths, notification topics, ...). A hit = drop that file and
   note the drop in the run report.
9. Stage exactly the intended files; whitespace check; review the staged diff.
10. Commit with the repository identity. Do not push, open a PR or merge.
11. Verify the complete diff, allowed paths and anonymization. Save a local
    patch and run report, record base and commit, and return to unchanged main
    only if safe. Remote CI for the unpublished commit is NOT RUN.
12. At most one notification when a proposal is prepared; no change means no
    commit, push or notification.

## Hard rules

- Scope: documentation, Skills, and task-card directories only. Inventory and
  CHANGELOG changes are reported for operator handling, never made by the task.
  No code, CI workflows, system-prompt templates, decision records, file
  deletion, push, PR, merge, history rewrite, secrets or personal data.
- The full patch and run report are local artifacts — never committed.
- The repository is English, anonymized, generic — always.
- Uncertainty is marked, never invented; a missing proof means no change.
- A failed push is never retried with force; it is reported factually.
- No task/loop management; no notifications beyond the single one.

## Delivery and notifications

- At most one notification for a prepared local proposal; silence when nothing
  changed.

## Failure behavior

Every failure is reported factually; nothing fails silently.

## Verification

Verify the complete local diff, base and commit, branch state and local checks.
Unpublished remote content and CI are not claimed as verified.