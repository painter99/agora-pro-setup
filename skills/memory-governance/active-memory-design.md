# Skill: Active Memory Design

## Catalog description

Keeps always-available Active Memory compact, current, useful, and separate from Skills and Saved Memory.

## Purpose

Decide what deserves recurring context cost and where all other durable information belongs.

## Load when

- deciding whether content belongs in Active Memory;
- reviewing Active Memory size or structure;
- separating current context from Saved Memory, conversation recall, or Skills;
- repairing duplicate or oversized Active Memory.

## Allocation rules

- **Active Memory:** dynamic current state, standing communication preferences, active priorities, short project/hobby anchors, and essential memory boundaries.
- **Saved Memory:** durable personal facts, history, completed work, project context, static specifications, and long-form references.
- **Conversation recall:** ephemeral session details, proposals, and unresolved one-session work.
- **Skills:** reusable procedures, frameworks, decision rules, checklists, and output contracts. Never duplicate personal facts in them.

Prefer the cheaper archival layer over Active Memory when both can serve the purpose. Keep Active Memory near a practical target of about 350 tokens and below the 1500-token hard limit unless the current Agora deployment documents different limits.

## Design rules

1. Keep one current-status section; do not create parallel status blocks.
2. Prefer short routing anchors with precise `**Load when:**` triggers over copied file bodies.
3. Keep long histories, detailed specifications, static references, complete workflows, and dormant information in Saved Memory.
4. Do not use Active Memory as a tool manual, session log, research dump, or Skill registry.
5. Separate current facts from durable facts; stale status must be refreshed or moved.
6. The current user request takes precedence over stale Active Memory, but does not bypass permissions or safety rules.
7. Active Memory is plain injected context, not a Skill or system prompt.

## Workflow

1. Inspect the current Active Memory and relevant Saved Memory files.
2. Classify each item: current, durable, transient, procedural, duplicate, stale, sensitive, or speculative.
3. Keep only high-value current anchors and durable standing preferences in Active Memory.
4. Move durable detail to an appropriate Saved Memory file; move procedures to a Skill; leave transient details in recall.
5. Check size, duplication, source-of-truth, and reference validity.
6. Obtain authority for any substantive AM change, then patch and re-read the result.

## Anti-patterns

Do not place full Skill bodies, tool manuals, copied web results, session logs, speculative facts, duplicate file bodies, or unrelated history in Active Memory. Do not silently change identity, preferences, life focus, or personal boundaries.

## Dependencies

`memory-master-index.md` for routing and `active-memory-authority.md` before an AM change.

## Verification

Check that Active Memory is compact, current, readable, free of duplicated long-form content, and that every routing reference is valid and useful.

## Output contract

Recommend the destination for each reviewed item, identify content to remove or move, and distinguish proposed from performed changes.
