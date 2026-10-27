# Task: daily data sweep

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

Run a daily sweep over a set of external data sources through a local script,
filter new entries against operator-defined fit criteria, and surface only
entries worth the operator's attention. Silence is the correct outcome when
nothing matches.

## Schedule

Daily, early morning (before the operator's active hours).

## Reads

- the report produced by the sweep script (sources, entry ages, pre-filtered
  sections)
- the operator's fit criteria (documented in the live prompt, not here)

## Workflow

1. Run the sweep script (read-only against the external sources).
2. Read the report it produced.
3. Filter new entries against the fit criteria; keep at most 5 candidates, each
   with: name, key numbers, location, link, why it fits / what to verify.
   Ambiguous entries are questions to verify, not fits. Entries older than a
   documented age are dropped, not re-surfaced.
4. If candidates exist: send exactly one notification (default priority) with a
   compact summary and links. If none: send nothing.
5. Append one run line to the report: date, candidate count, notification state.

## Hard rules

- Read-only except one append to the report.
- No writes to memory or Skills; no task/loop creation; no printing, e-mailing,
  or sending anything on the operator's behalf.

## Delivery and notifications

- Exactly one notification per run, and only when candidates exist — no
  candidates means silence, not a "nothing found" message.

## Failure behavior

Script failure → exactly one low-priority notification with the error; no
retries within the run.

## Verification

The run line exists in the report; the notification count for the run is 0 or 1.