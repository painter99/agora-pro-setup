# Tool-Call Retry Discipline and Budget

Architectural remediation for a real failure mode: in long tool-heavy sessions a
model can repeat failed tool calls with unchanged parameters, burning API budget
and time without progress. As of Agora v2.1.0 (verified against upstream master
on 2026-10-08), the application returns tool errors to the model as error
results but enforces **no cap** on tool-call rounds; whether the model retries
responsibly is left entirely to the prompt layer. This document defines the
setup's retry discipline and budget policy and how it is enforced across layers.

## Problem

When a tool call fails, the path of least resistance for a model is to issue the
same call again — sometimes many times in a row. Each round costs tokens (input
context grows with every appended result), wall-clock time, and API credit. The
application-level feedback loop exists (error results reach the model), but
nothing bounds the loop. The same failure mode is documented across the agent
ecosystem as "runaway loops" and is why mainstream frameworks ship call caps by
default.

## Industry context (independent corroboration)

| Framework | Mechanism | Default |
|---|---|---|
| LangChain (DeepAgents middleware) | `ToolRetryMiddleware` (transient errors, backoff), `ToolErrorMiddleware` (error → message to model), `ToolCallLimitMiddleware` (cap per run) | max_retries 2; run_limit 200 |
| OpenAI Agents SDK | `max_turns` cap on the agent loop, `MaxTurnsExceeded` exception | 10 turns |
| Anthropic tool-use guidance | error taxonomy: transient → retry; LLM-recoverable → error result to model; runaway → cap calls | — |

All three separate **who fixes which error** (system retry vs. model adjustment
vs. human) and all three bound total calls. This setup adopts the same shape.

## The policy (normative)

Definitions:

- **Query type** — the same tool with the same intent (e.g. "patch this text",
  "fetch this page", "grep for this pattern").
- **Round (wave)** — one batch of up to two calls for the same query type.
- **Failed round** — a round in which every call failed or returned an unusable
  result.

Rules:

1. **Never repeat an identical failed call.** Read the error text first; every
   retry must differ in parameters, anchor, scope, or method.
2. **Two consecutive failed calls of one query type force an adjustment.** The
   model must stop and change the approach — different anchor or parameters,
   smaller scope, another tool, or reading the relevant documentation — before
   the next round.
3. **Three failed rounds exhaust a query type.** Report honestly what was
   attempted and why it failed, and hand the decision back to the user (or use
   `ask_user` where the installed Agora version provides it).
4. **Global reply budget.** A single reply should stay within ~15 tool-call
   rounds regardless of query type; prefer batching and slicing over many small
   calls.
5. **Terminal honesty.** When a budget is spent, the reply states what was
   verified, what failed, and what it needs to continue — it never silently
   continues and never fabricates a result.

Error taxonomy (who fixes what):

| Error type | Examples | Strategy |
|---|---|---|
| Transient | network timeout, rate limit, 5xx | one retry after a pause is acceptable |
| LLM-recoverable | bad parameters, wrong anchor, malformed JSON, tool not offered | read error, adjust, next round (rules 2–3) |
| Structural | permission denied, missing auth, tool absent, confirmation refused | no retry; report and ask |

## Enforcement split

| Layer | Owns |
|---|---|
| System template (kernel) | compact always-injected rule: never repeat an identical failed call; adjust after two consecutive failures; exhaust a query type after three failed rounds; terminal honesty |
| `skills/tool-execution-contract.md` | the detailed procedure: definitions, wave rules, error taxonomy, budget bookkeeping |
| `docs/8-tools-and-safety.md` | routing and the short rule set |
| `docs/11-troubleshooting.md` | the failure-mode entry |
| `docs/16-multi-agent-system.md` | generalization: per-agent budget controls in the future MAS layer |

Rationale: the same lesson as the memory gate (`docs/20-memory-gate.md`) — a
rule that must apply to every tool call cannot live only behind an optional
Skill lookup, but the kernel must stay compact, so the procedure detail lives in
the Skill and the rationale here.

## What the kernel cannot do today

The prompt layer makes the policy **likely**, not guaranteed. A native
per-generation tool-round budget (an opt-in setting with a sensible default,
plus a visible "budget spent" terminal state) would make it **guaranteed** and
belongs in the Agora application itself — the same status as the budget
controls proposed for the multi-agent layer in `docs/16` §12. Until such a
capability exists, this setup's enforcement is prompt-level and must be
verified by behavior (below), never assumed.

## Verification

1. Give the agent a task that produces a tool failure (for example a patch
   against text that does not exist). Confirm the second attempt differs from
   the first.
2. Confirm the agent does not exceed three rounds on one query type without
   changing the approach.
3. Confirm an exhausted budget ends in an honest report, not silence or
   fabrication.
4. Confirm the global reply budget holds in a tool-heavy task.

## Related docs

`docs/0-overview.md`, `docs/8-tools-and-safety.md`,
`docs/11-troubleshooting.md`, `docs/16-multi-agent-system.md`,
`docs/20-memory-gate.md`, `skills/tool-execution-contract.md`,
`system-prompt/1-system-template.md`.