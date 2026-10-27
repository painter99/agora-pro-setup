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

Weekly (Sunday evening).

## Reads

- local memory files with repository conventions and workflow gotchas
- the self-improvement Skill and the local eval/retrospective logs
- the repository itself (pull, directory listing, the skill-format spec)

## Workflow

1. Read conventions and gotchas; map stack reality (skill catalog, logs, task
   list where available).
2. Map the repository: pull with fast-forward only, list directories, read the
   format specification.
3. Find up to 5 changes the repository does not reflect (a new or changed Skill
   without a current repository version, a new pattern without documentation,
   stale docs). Every change needs evidence; without evidence, no change.
4. Write the English, anonymized, generic versions (Skills follow the
   skill-format spec).
5. Run the identifier scan over every changed file (names, projects, hardware,
   models, local paths, notification topics, ...). A hit = drop that file and
   note the drop in the run report.
6. Stage exactly the intended files; whitespace check; review the staged diff.
7. Commit with the repository identity; push to the default branch; verify the
   push (status + remote heads).
8. Verify the content actually arrived on the remote, and — for a docs-only
   repository — that no CI run was triggered.
9. Exactly one notification when something was synced (files, commit hash,
   state). No change = no commit, no push, no notification.

## Hard rules

- Scope: documentation and Skills directories only. No code, no CI workflows,
  no system-prompt templates, no file deletion, no force-push, no history
  rewrite, no secrets or personal data.
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