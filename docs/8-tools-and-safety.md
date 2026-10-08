# Tools and Safety

Use `tool-execution-contract` as the operational Skill. This page explains the universal gate. For memory-specific work, route through `memory-master-index` and load only the relevant memory-governance Skill.

## Before a tool call

- identify exact operation, target, and device;
- confirm the correct family: Memory, Skill, web, conversation, file, shell, MCP, or automation;
- check availability, permissions, confirmation policy, and approval requirements;
- inspect current state before editing.

## After a tool call

- inspect actual output;
- confirm what changed;
- distinguish success, partial completion, background/durable job, and failure;
- check dependent state and references;
- report important limitations.

## Failed-call discipline and budget

Never repeat an identical failed tool call. Full policy and rationale:
[`docs/21-tool-call-budget.md`](21-tool-call-budget.md). The short rules:

- read the error text before any retry; every retry must differ in parameters,
  anchor, scope, or method;
- two consecutive failed calls of one query type force an approach change
  before the next round;
- three failed rounds exhaust a query type — report what was attempted and ask
  the user instead of continuing;
- keep a single reply within ~15 tool-call rounds; batch and slice instead.

## Approval required before

- delete or irreversible modification;
- secret or credential access;
- publication, sending, purchasing, or external release;
- system-altering commands;
- materially consequential legal, medical, financial, employment, or safety decisions.

State exact action, exact scope, and relevant risk. A general request for help is not authorization for an irreversible action.
