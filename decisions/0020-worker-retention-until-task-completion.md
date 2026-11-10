# ADR-0020: Retain worker context until operator-confirmed task completion

- Status: accepted (2026-11-10, operator GO)
- Supersedes: none

## Context

Deleting a completed worker immediately after its result has been verified
loses its conversation context even when further work is expected. Starting a
new worker requires a new brief and consumes another spawn attempt. Conversely,
retaining workers can occupy limited slots, preserve stale assumptions, and
retain task data longer. A previously involved worker is not a substitute for
an independent fresh-context review.

## Decision

1. The system template retains workers until the operator confirms that the
   overall user task is complete; earlier release requires explicit operator
   authorization. Before deletion, capture the relevant result, material
   caveats, and evidence references.
2. Retention does not expand execution permissions, available slots,
   concurrency, or the task's approved spawn budget. If a retained worker
   occupies a slot needed for authorized work, the operator chooses whether
   to release it or defer the new spawn; there is no silent eviction.
3. Before resuming a retained worker, refresh relevant decisions, constraints,
   and changed state, and recheck its assignment and permissions. A worker
   involved in producing an artifact cannot independently review it; required
   independent review uses a separate fresh context.
4. Worker retention is a prompt-level policy, subject to the application
   client's actual lifecycle, permission, and slot behavior. It does not
   guarantee that continuation or context retention is supported by a runtime.

## Consequences

- Continuations can reuse prior context without a new spawn when supported.
- Slot pressure and longer retention of task data require explicit operator
  decisions; the system must not silently exceed its limits.
- Retained context can become stale, so continuation requires an update and
  reinspection of relevant state.
- Mandatory independent review and the delegation budget remain in force.
