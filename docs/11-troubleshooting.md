# Troubleshooting

## Skill does not load

Check Skill access, the saved file, short catalog description, exact flat name, `{skill_catalog}` in System, and whether the model actually called `skill_read`.

## Wrong memory layer is used

Facts and durable context belong in Memory. Reusable procedures belong in Skills. Check `memory-master-index` and do not route Skill CRUD through Memory tools.

## User dates are missing

Put the Send Date and Send Time widgets around the single Prompt block in **User**. Do not recreate Prefix/Suffix.

## Active Memory is missing

Place `{active_memory}` in **System** and check Access Active Memory. Custom templates do not receive hidden Active Memory text.

## Shell fails

Check selected device, authentication, host-key policy, confirmation setting, and durable `job_id`. Stop retrying structural or permission failures.

After an app upgrade, an SSH device may require re-pinning its host key (the trust-and-pin step in the shell settings); adding a new client key does not resolve the `HostKey has been changed` error — a client key is a client identity, not a host-key pin. Verify the server fingerprints from an independent transport before re-accepting.

## Repeated failed tool calls

The model repeats a failed call with unchanged parameters, or loops on the same query type. The setup's retry discipline lives in `docs/21-tool-call-budget.md` and `tool-execution-contract`: never repeat an identical failed call, adjust after two consecutive failures, exhaust a query type after three failed rounds. If the model breaks this rule, tighten the System-template sentence — prompt-level enforcement is not guaranteed; a native per-generation budget would be (see `docs/16` §12).

## Provider 402 errors

A model-provider 402 has two distinct causes that must not be conflated:

- **Credit/max-tokens exhaustion** — the provider error names insufficient credits or an exhausted token budget. Structural blocker: stop, record the verbatim error text and the route it came from; no identical retry, no automatic fallback, no further spawns. Route, limits, and keys are changed only by the operator within the approved budget; never display secret values. Verify partial artifacts of the interrupted work independently before continuing.
- **Prompt tokens limit exceeded** — the request exceeded the model's context window. Diagnostic path: reduce input size (smaller read batches, split large files) before the next attempt; this signature alone is not evidence of an account-credit problem.

Do not infer the cause from the HTTP status code alone — keep the exact provider message and the route. Observed 2026-11-09: two subagent workers in one run ended with a credit/max-tokens 402 after partial work; their outputs were used only after content review, and the remaining steps were completed by a replacement worker.

## Unsupported research claim

Load `multi-source-research` for multi-source work, fetch pages rather than trusting snippets, surface conflicts, and state `LIMITED EVIDENCE` when appropriate.
