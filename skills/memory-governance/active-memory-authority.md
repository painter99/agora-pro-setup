# Skill: Active Memory Authority

## Catalog description

Controls authorization, patching, recovery, and verification for Active Memory changes.

## Purpose

Protect Active Memory from silent drift, unauthorized identity changes, bloat, unsafe replacement, and ambiguous recovery.

## Load when

- updating or patching Active Memory;
- deciding whether an AM change is authorized;
- recovering from corruption, duplication, or excessive size;
- changing identity, preferences, life focus, hobby anchors, model choices, or personal boundaries.

## Do not load when

- only reading Active Memory;
- editing Saved Memory without changing AM;
- answering a transient question.

## Authority model

- **User explicit:** may change any AM content.
- **Agent proactive:** may add/remove an Archive Index entry when a Saved Memory file is created/deleted, or refresh an obviously stale status date when current context clearly warrants it.
- **Agent passive:** may fix an unambiguous typo or add a missing `**Load when:**` trigger.
- **No silent substantive change:** identity, communication preferences, life focus, hobby anchors, AI model choices, and personal boundaries require explicit confirmation for the exact scope.

The current user message wins over stale or conflicting AM content.

## Decision gate

1. Identify the exact AM section and intended change.
2. Classify the change as user-explicit, allowed maintenance, or requiring confirmation.
3. Read the current AM and confirm the target text is unique.
4. Prefer a precise patch; do not use replace for ordinary edits.
5. Check sensitivity, reversibility, size, source-of-truth, and dependent references.
6. Execute only within the authorized scope.
7. Read back the affected content and verify integrity, size, references, and unrelated content.

## Patch versus replace

Use a targeted patch for ordinary edits. Full replacement is exceptional: it requires explicit approval, a verified reconstruction source, and post-write checks for section integrity, Archive Index references, token size, duplicate facts, and stale markers.

## Recovery

For an ambiguous or failed patch, stop and re-read the current AM. Widen the match only with verified surrounding context and retry once the target is unique. Never guess at missing content. If AM is fragmented or corrupted beyond patch recovery, propose a reconstruction from a verified template and obtain explicit approval before replacement.

## Sensitive data and boundaries

Do not add sensitive personal information without appropriate explicit authorization. Do not use AM as a dump for session logs, detailed workflows, tool manuals, or speculative facts. Keep durable detail in Saved Memory.

## Verification

Confirm the intended section changed, unrelated content was preserved, references remain valid, authorization matched the scope, and the resulting AM remains compact and readable.

## Output contract

Report exact AM scope, authorization basis, operation, verification, and unresolved limitation.
