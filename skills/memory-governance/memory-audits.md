# Skill: Memory Audits

## Catalog description

Finds stale, contradictory, oversized, duplicated, or broken persistent memory.

## Purpose

Audit Active Memory, Saved Memories, and their references.

## Load when

- an audit is requested;
- memory sources disagree;
- a reference is missing or stale;
- Active Memory appears bloated or corrupted.

## Do not load when

- performing a routine read with no inconsistency;
- auditing Skills rather than Memory.

## Dependencies

`memory-master-index.md` and `active-memory-design.md`.

## Workflow

Check current identity and preferences, registry or reference validity, duplicate facts, stale status, oversized Active Memory, missing descriptions, and unresolved contradictions. Surface conflicting sources. Prefer the current user statement for personal facts and the newest reliable source for time-sensitive facts. Never silently choose a winner.

## Forbidden behavior

Do not hide conflicts, perform an unapproved full replacement, or treat a failed patch as successful.

## Verification

Report findings separately from corrections and verify every correction independently.

## Output contract

Provide findings, evidence, proposed corrections, performed corrections, and unresolved issues.
