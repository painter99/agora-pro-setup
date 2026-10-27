# ADR-0004: Tool-call budget is enforced at prompt level

- Status: accepted (2026-10-08, operator GO)
- Supersedes: none

## Context

The application (v2.1.x line) returns tool errors to the model but imposes no
cap on tool rounds; industry practice combines round caps with retry
middleware. Unbounded retries waste tokens and can loop.

## Decision

Prompt-level budget, normative in `docs/21-tool-call-budget.md`:

- never repeat an identical failed tool call;
- after two consecutive failures of one query type, change the approach;
- after three failed rounds, report honestly and hand back;
- global budget of roughly 15 tool rounds per reply;
- error taxonomy: transient (one retry allowed), recoverable (adjust),
  structural (no retry).

## Consequences

- Enforcement is probable, not guaranteed — the same caveat as ADR-0003.
- A native per-generation budget would be guaranteed and remains a candidate
  upstream feature request (not yet filed, pending operator decision).
- Verification follows the procedure in `docs/21` (a second attempt must
  differ; honest report when the budget is exhausted).