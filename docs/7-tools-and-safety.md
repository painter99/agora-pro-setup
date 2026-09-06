# Tools and safety

See also Skill `tool-execution-contract` and `04-tool-reference-card`.

## Before

- exact operation and target
- correct tool family (Memory ≠ Skill ≠ shell)
- permissions and device confirmation
- inspect before edit

## After

- inspect actual output
- success vs partial vs durable-job vs failure
- dependent references
- honest limitations

## Retry

Retry transient failures a limited number of times.

Do not retry permission, authentication, invalid arguments, missing structure, or destructive ops.

## Approval before

- delete / irreversible modify
- secrets
- publish / send / purchase
- system-altering commands
- material legal, medical, financial, employment, or safety actions

State exact action, scope, and risk. "Help me with git" is not approval to force-push `main`.
