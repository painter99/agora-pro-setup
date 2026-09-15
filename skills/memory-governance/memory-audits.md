# Skill: Memory Audits

## Catalog description

Finds stale, contradictory, oversized, duplicated, sensitive, or broken persistent memory and references.

## Purpose

Audit Active Memory, Saved Memories, and their relationships without silently rewriting or deleting data.

## Load when

- a full or targeted memory audit is requested;
- memory sources disagree;
- a reference is missing, stale, or points to an obsolete filename;
- Active Memory appears bloated, duplicated, or corrupted.

## Audit workflow

1. Inspect current Active Memory and list Saved Memory files.
2. Read relevant files and check identity, preferences, status markers, descriptions, references, and source-of-truth boundaries.
3. Check Active Memory size, duplicate facts, stale entries, phantom references, obsolete Skill/framework names, unauthorized sensitive data, and procedural content in memory.
4. Compare conflicting sources. Prefer the current user statement for personal facts and the newest reliable source for time-sensitive facts, but surface unresolved conflicts.
5. Classify each finding as stale, contradictory, duplicated, oversized, orphaned, sensitive, procedural misplacement, historical, or valid.
6. Separate findings, proposed corrections, performed corrections, and unresolved issues.
7. Obtain required authorization for corrections, execute the smallest safe operation, and verify each correction independently.

## Audit triggers

Run a user-initiated full audit, a change-triggered audit after a major life or project change, a bloat-triggered audit when AM approaches its limit or a file becomes unwieldy, and a periodic review when the memory layer has not been checked for an extended period.

## Failure-mode checklist

Check for AM hijack, doubletalk between AM and files, phantom references, stale status markers, unauthorized sensitive data, accidental full replacement, non-unique patch targets, duplicate source-of-truth entries, and Skills or memories pointing to obsolete filenames. Never silently choose a winner in a contradiction and never delete as part of an audit without explicit authorization.

## Verification

Re-list/read affected files, confirm references and source-of-truth, check AM size/structure, and report any unresolved issue separately.

## Output contract

Provide findings, evidence, proposed corrections, performed corrections, authorization basis, verification, and unresolved issues.
