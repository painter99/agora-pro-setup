# Dispatch spend observability and budget discipline

Status: operating policy adopted 2026-11-20 after a real near-miss; generic
record, no instance identifiers. This document describes what happened, the
policy that now governs paid dispatches, and the observability loop that keeps
the policy honest. It complements the dispatch contract in
[`docs/34-agora-goose-bridge.md`](34-agora-goose-bridge.md) and the tool-call
budget in [`docs/21-tool-call-budget.md`](21-tool-call-budget.md): doc 21 bounds
*attempts*; this document bounds *money*.

## 1. What happened

A single day of multi-dispatch work — one specification dispatch, one failed
implementation start, two interrupted implementation dispatches, one
implementation completion, and two full independent review rounds — consumed
nearly the entire hard budget that the operator had placed on the provider API
key. The cap had been set as a fire-drill limit under the assumption that
normal work would never approach it. Three structural causes, all visible in
retrospect:

1. **No spend visibility.** The delegation budget counted dispatch *attempts*,
   never money. Nothing logged tokens per request, so nobody could have
   reported cumulative spend even in principle.
2. **Route selection by capability, not by cost.** Every dispatch of the day,
   including ones that were mostly mechanical, ran on the most expensive
   approved route because that route also held the review qualification.
3. **Waste modes were unpriced.** A dispatch killed by a time bound, a start
   that fails on a foreseeable scope conflict, and an extra review round all
   cost real money while counting as ordinary process.

## 2. The policy

- **Two numbers, kept separate.** The provider-side hard cap exists for
  emergencies and must never be treated as a working budget. The working
  budget is a separate, lower daily target for paid dispatches; when the
  target is exceeded, work stops and the operator is told — the cap is never
  the information channel.
- **Cheapest sufficient route.** The specialist route is reserved for
  qualified fresh-context review and genuinely complex implementation.
  Mechanical work, record shaping, bulk edits and short summaries go to the
  light route or are done coordinator-side without a dispatch.
- **Brief economy.** Briefs point to files and line ranges instead of ordering
  full-file reads; turn bounds are kept low; every brief states its cost
  ceiling (this field already exists in the bridge brief template).
- **Pre-flight scope checks.** Before any implementation dispatch, the
  coordinator verifies with cheap local inspection (grep the touched modules
  and their readers/validators) that the declared file scope can actually
  carry the change. A dispatch that fails on a foreseeable scope conflict is
  paid waste.
- **Dispatch sizing.** A dispatch is sized so that its time bound does not
  kill it mid-run; a killed dispatch is paid waste. Long work is split into
  commits-sized dispatches instead of one long run.
- **Free capacity first.** Public-data research goes to a free-tier external
  research agent before any paid dispatch. Each new use class of the external
  agent is recorded before first use, and its per-task credit consumption is
  checked after every run (see [`docs/34`](34-agora-goose-bridge.md) Part 1
  for the product case study).

## 3. The observability loop

Spend is managed exactly like a development feedback loop:

1. **Track.** The local forward proxy records one JSON line per request:
   timestamp, path, status, model, byte counts, and the token usage extracted
   from the response (input, output, cached, reasoning). Response bodies are
   not persisted and the API key is never logged. A small stdlib aggregator
   prints per-day, per-model token totals.
2. **Analyze.** After each substantial task — and periodically regardless —
   the coordinator reviews spend per task and per route and looks for named
   outliers: killed dispatches, failed starts, expensive routes on mechanical
   work, context that grew across turns.
3. **Improve.** Each finding becomes a small, measured change — a route
   demotion, a leaner brief pattern, a lower turn bound, an earlier split
   point — and the next period's numbers show whether it helped. Changes to
   approval gates or permissions are never made by this loop; they stay with
   the operator.

## 4. Honest limits

- Token counts are measured; **money is not**. Per-token prices for the
  deployed routes were not verified at adoption time, so the aggregator
  reports tokens and computes cost estimates only from an operator-supplied
  price table. A token report already exposes the structural outliers; the
  price table only rescales them.
- The proxy sees only traffic that flows through it. A dispatch path that
  bypasses the proxy is invisible to this loop; adding one requires an
  operator decision, not a silent shortcut.
- Usage extraction depends on the upstream response format. A format change
  degrades the log to byte counts, which still supports the loop, just more
  coarsely.
