# Tools and Safety

Use `tool-execution-contract` as the operational Skill. This page explains the universal gate.

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

## Approval required before

- delete or irreversible modification;
- secret or credential access;
- publication, sending, purchasing, or external release;
- system-altering commands;
- materially consequential legal, medical, financial, employment, or safety decisions.

State exact action, exact scope, and relevant risk. A general request for help is not authorization for an irreversible action.
