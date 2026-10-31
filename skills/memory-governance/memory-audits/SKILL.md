---
name: memory-audits
description: "Finds stale, contradictory, oversized, duplicated, sensitive, or broken persistent memory and references."
license: MIT
---

# Skill: Memory Audits

## Catalog description

Finds stale, contradictory, oversized, duplicated, sensitive, or broken persistent memory and references.

## Purpose

Audit the working state file (file-based active memory), Saved Memories, and their relationships without silently rewriting or deleting data.

## Load when

- a full or targeted memory audit is requested;
- memory sources disagree;
- a reference is missing, stale, or points to an obsolete filename;
- the working state file appears bloated, duplicated, or corrupted.

## Do not load when

- a single known Saved Memory edit with no cross-layer consistency question;
- answering a transient question from conversation context;
- routine reading of memory with no audit intent.

## Dependencies

- `memory-master-index`
- `file-based-active-memory`
- `memory-file-operations`
- `tool-execution-contract`

## Workflow

### Audit workflow

1. Inspect the working state file and list Saved Memory files.
2. Read relevant files and check identity, preferences, status markers, descriptions, references, and source-of-truth boundaries.
3. Check working-state size, duplicate facts, stale entries, phantom references, obsolete Skill/framework names, unauthorized sensitive data, and procedural content in memory.
4. Compare conflicting sources. Prefer the current user statement for personal facts and the newest reliable source for time-sensitive facts, but surface unresolved conflicts.
5. Classify each finding as stale, contradictory, duplicated, oversized, orphaned, sensitive, procedural misplacement, historical, or valid.
6. Separate findings, proposed corrections, performed corrections, and unresolved issues.
7. Obtain required authorization for corrections, execute the smallest safe operation, and verify each correction independently.

### Staleness scoring

Quantify staleness instead of judging it by feel. Derive each file's age from
its own date markers (header dates, dated sections, last-verified notes); a
file without any date marker counts as stale by default. Classes: fresh
(≤ 30 days), aging (31–90), stale (> 90). Staleness is a finding, not a
verdict: report it with a verify / refresh / archive recommendation, never
correct it silently, and remember the current user request still outranks
stale content.

## Audit triggers

Run a user-initiated full audit, a change-triggered audit after a major life or project change, a bloat-triggered audit when the working state file approaches its limit or a file becomes unwieldy, and a periodic review when the memory layer has not been checked for an extended period.

## Failure-mode checklist

Check for state-file hijack, doubletalk between the working state and files, phantom references, stale status markers, unauthorized sensitive data, accidental full replacement, non-unique patch targets, duplicate source-of-truth entries, and Skills or memories pointing to obsolete filenames. Never silently choose a winner in a contradiction and never delete as part of an audit without explicit authorization.

## Forbidden behavior

- Never silently choose a winner in a contradiction; surface unresolved conflicts.
- Never delete or rewrite memory as part of an audit without explicit authorization.
- Never perform corrections beyond the smallest safe authorized operation.
- Never report a correction as verified without reading the result back.

## Verification

Re-list/read affected files, confirm references and source-of-truth, check working-state size/structure, and report any unresolved issue separately.

## Output contract

Provide findings, evidence, proposed corrections, performed corrections, authorization basis, verification, and unresolved issues.
