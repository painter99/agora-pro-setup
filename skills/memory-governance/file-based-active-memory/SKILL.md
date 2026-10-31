---
name: file-based-active-memory
description: "Content policy and read/write discipline for the working state file that replaces injected Active Memory (file-based active memory)."
license: MIT
---

# Skill: File-Based Active Memory

## Catalog description

Content policy and read/write discipline for the working state file that replaces injected Active Memory (file-based active memory).

## Purpose

Keep the current-status layer compact, current, and verifiable when injected Active Memory is disabled: a single working state file on a persistent host, read and written through file tools with mandatory read-back verification.

## Load when

- reading or writing current status, priorities, standing rules, or the Archive Index;
- deciding whether content belongs in the working state file, Saved Memory, or nowhere;
- verifying a state-file write or recovering from a failed write.

## Do not load when

- creating or editing Saved Memory files (use `memory-file-operations`);
- only reading the state file with no write or placement question;
- purely transient conversation context.

## Dependencies

- `memory-master-index` — layer routing;
- `memory-file-operations` — Saved Memory operations;
- `tool-execution-contract` — shared inspection and verification contract.

## Workflow

1. Read the state file before relying on its content; never reconstruct it from memory of earlier sessions. The instance path lives in the instance overlay/System template (docs/30) — never in this repository.
2. Classify the change: current status, standing rule, Archive Index line, durable fact, or transient.
3. Route: durable facts and histories → Saved Memory (`memory-file-operations`); procedures → Skills; transient → no write; current status, standing rules, and index anchors → the state file.
4. Patch with an exact, unique anchor. Full replacement is exceptional: explicit approval, a verified reconstruction source, and a fresh backup copy first.
5. Back up before any full replacement: copy the file to the instance state backup directory with a date suffix.
6. Read the file back after every write and verify: intended change present, unrelated content preserved, size budget respected, index lines valid.
7. Keep the file within budget — narrative sections near 350 tokens; the Archive Index may grow with the Saved Memory library (one line per topic group with a `Load when` trigger); hard ceiling about 1500 tokens; split by domain if it outgrows.
8. Report the exact operation, evidence (read-back), authorization basis, and unresolved limits.

## Forbidden behavior

- Never change identity, communication preferences, life focus, model choices, or personal boundaries in the state file without explicit confirmation of the exact scope.
- Never use full replacement without explicit approval, a verified source, and a fresh backup.
- Never store session logs, tool manuals, copied external content, speculative facts, or duplicated Saved Memory bodies in the state file.
- Never claim a write is verified without a read-back.
- Never put the state-file path or personal identifiers into the public repository (ADR-0017).

## Verification

Read-back confirms the intended change, preserved unrelated content, valid index references, respected size budget, and authorization matching the scope.

When a status bullet that references a detail source is migrated or rewritten, verify it against the referenced detail source before writing; never propagate a status line forward on the strength of a read-back alone (observed failure 2026-10-31: a stale status bullet was migrated verbatim into the working state file while the referenced Saved Memory file held the current truth).

## Output contract

Report the exact change, evidence (read-back), authorization basis, and any pending items or limits.