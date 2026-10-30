# Task: weekly skill mirror check

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

Weekly verification that the deployed local Skills match the repository source
of truth (procedure: `skills/coordination/skill-mirror-check/SKILL.md`). Silent
divergence makes instance behavior get misattributed to repository text and
triggers nonsense repository "fixes"; this check catches drift within a week
and classifies it before anything is edited.

## Schedule

Weekly, Sunday night (between the retrospective and the repository-sync
tasks).

## Reads

- the Skill `skill-mirror-check` (procedure and classification rules);
- the local Skill catalog and every local Skill file (fresh reads);
- the repository checkout: `skills/**/SKILL.md`.

## Workflow

1. Read the Skill `skill-mirror-check`; follow its workflow.
2. Fresh-read every local Skill, write verbatim working copies to a scratch
   directory, and `diff` each against its repository file.
3. Classify every difference: content drift (blocking) / expected overlay /
   cosmetic.
4. Write the dated report to the local mirror-check log directory; exactly one
   notification with the summary line and report path.
5. On drift, determine the direction before any repair:
   - Repository clearly the newer truth (a recent repository change was never
     imported) → repair = re-import the repository version into the local
     store, patched in place; this proceeds on the operator's standing
     authorization (2026-10-28) and is recorded in the report with diff
     evidence.
   - Local version genuinely newer → do not import; propose a repository port
     through the standard branch workflow (operator GO required).
   - Ambiguous direction → report the diff and wait for the operator.
   No repair is ever silent: every applied repair is recorded in the report
   with its evidence and authorization basis.

## Hard rules

- Read-only on Skills and the repository: no edits, no deletes, no pushes, no
  task/loop management. Standing exception (operator authorization
  2026-10-28): on confirmed content drift with the repository clearly newer,
  the repository version may be imported into the local store in place (never
  a wholesale delete+re-import), recorded with diff evidence; repository
  ports and ambiguous directions stay behind operator GO.
- Writes only to: the scratch directory, the mirror-check log directory, and
  one notification.
- A difference that does not reproduce on re-read is a transcription artifact,
  not drift — re-read before reporting.
- Overlay areas (coordinator capability table; escalation stack/routing
  tables) are expected differences, not drift.

## Failure behavior

Every failed read or diff is recorded in the report; nothing fails silently.
A missing repository checkout is a blocking finding (the check cannot run).

## Verification

The report exists with a per-Skill classification covering the whole catalog;
the notification was sent (or its absence explained in the report).