# Task: quarterly replication dry-run

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

Quarterly replication audit of this repository: a scheduled agent run simulates
a fresh external agent seeing the repository for the first time (clean HTTPS
clone, no local memory or Skills) and walks the installation path. The golden
task measures whether the repository stays replicable over time (docs/29,
golden-task eval; the first manual run on 2026-10-27 is the baseline).

## Schedule

Quarterly (first day of January, April, July, October, night window; exact time is instance-specific).

## Reads

- the repository only: a fresh HTTPS clone (no SSH keys, no local memory,
  no Skill catalog — the run simulates an agent without this stack)

## Workflow

1. Fresh clone over HTTPS into a scratch directory.
2. Read, in order: AGENTS.md → README.md → docs/0-overview.md →
   docs/2-installation.md → docs/30-instance-overlay.md.
3. Walk the docs/2 installation path step by step; for each step verify that
   referenced files exist, app-independent commands run in the clone, and
   instructions are unambiguous. Where an external agent would get stuck,
   record a gap: step, description, severity (blocking/minor).
4. Run `./scripts/check.sh` in the clone; a non-zero exit is a gap.
5. Verify a sample of relative links in docs/ and a sample of AGENTS.md claims
   against the actual tree; verify external URLs in docs/ respond (they are
   not covered by the link checker).
6. Write the report (dated file name) to the local dry-run log directory:
   what was done, gaps found (with evidence), what worked cleanly, top
   recommendations. "No gap found" is a valid result.
7. Exactly one notification: gap counts (blocking/minor) + report path.

## Hard rules

- Read-only on the system except the scratch clone and the dry-run log
  directory. No pushes, no changes to the repository checkout, no installs.
- No reading of local memory or Skills — the run simulates an agent without
  this stack.
- Every gap needs concrete evidence (file, line, missing file); nothing is
  invented.
- No task/loop management; no notifications beyond the single one.

## Failure behavior

Every failed step is recorded in the report; nothing fails silently.

## Verification

The report exists with the mechanical self-check passed; the notification was
sent (or its absence explained in the report).