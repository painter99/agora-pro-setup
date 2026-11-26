# ST-Enforcement Process Card

Process card for the deterministic sequential-thinking (ST) enforcement gate on
dispatched Goose runs. It documents what the gate enforces, what it cannot do,
the wrapper interface, the audit rules, and the failure and rollback model.
This card is generic and public; the instance wrapper path, endpoint and
schedule live in the private instance overlay (see `docs/30`).

## What the gate enforces

Every dispatched Goose shell run (including scheduled and review dispatches)
must execute through the approved ST-enforcement wrapper. The wrapper:

1. injects the sequential-thinking extension flag and the worker system
   protocol into the run;
2. runs a fail-closed preflight probe before the run starts;
3. audits the structured event stream produced by the run.

The audited invariants are:

- paired successful tool calls (a failed call is never counted as use);
- the `load_skill` call for the sequential-thinking workflow Skill is issued
  before the first sequential-thinking call, and its paired result is valid and
  successful; parallel tool issuing is accepted by design;
- the dispatch-specific canary token appears in the first thought (injected by
  the wrapper, never fabricated by the agent);
- at least the configured minimum number of thoughts is present, and every
  thought has at least 40 non-whitespace characters;
- non-empty final assistant text follows the tool calls.

## What the gate cannot do

- It does not block actions in Agora chat: the gate covers Goose shell
  dispatches only, and pre-action blocking applies at the wrapper boundary.
- It does not guarantee reasoning quality. It verifies process evidence
  (calls, ordering, canary, minimum length), not that the reasoning is sound.
- Delegates remain instruction-level: the wrapper constrains how a run is
  observed and accepted, it does not grant new authority to the worker.

## Wrapper interface (generic)

The coordinator's shell dispatch path calls the wrapper instead of the direct
runner. The wrapper takes the same dispatch arguments plus its own
configuration (extension flag, protocol file, canary token, thresholds), and
returns an exit code plus a ledger record:

| Signal | Meaning |
|---|---|
| exit 0 with a matching ledger `RESULT` record | dispatch accepted |
| exit 2 | fail-closed enforcement stop (preflight or audit miss) |
| missing ledger evidence | treated like a failure: failed dispatch |

Failures are loud: a fail-closed stop is reported in the terminal report and
the affected work stops; it is never retried through the direct route.

## Audit rules

- Count structured paired calls from the audit record, never prose occurrences
  of a tool name in run logs.
- Only successful paired calls count; one half of a pair is not use. Any failed ST call fails the run.
- The first thought must contain the exact canary token value as a substring.
- Audit state is written to an append-only ledger alongside the run log; the
  ledger, not memory or chat claims, is the acceptance evidence.

## Run supervision architecture (final, fix10–14)

The deployed wrapper (`scripts/st-enforce/` in this repository, deployed copy
reviewed and smoke-tested) supervises the run as follows:

- **Watchdog**: a watchdog thread is armed first, at wrapper start, with an
  absolute deadline of `timeout-sec + 30` seconds (an absolute deadline armed
  first removes the race between the watchdog and the audit path). At the
  deadline it terminates the child process group and forces the run to a
  terminal failure; no signal handler or masking is needed because none exists.
- **SIGCHLD restore**: at startup, an inherited ignored `SIGCHLD` is restored
  to the default disposition (`SIG_DFL`) so child processes remain waitable;
  restoration failure is fail-closed (exit 2).
- **Single teardown owner**: the watchdog is the only teardown owner. It sends
  SIGTERM to the child process group, allows a 5-second grace period, then
  SIGKILL, reaps the direct child, kills the sentinel, and only then retires
  the child slot (an `ESRCH` probe under the watchdog lock).
- **Group-identity sentinel**: the child leader is never reaped before an
  attached sentinel process has joined the group; the unreaped leader PID
  prevents numeric group reuse while the sentinel holds the group through
  TERM, the grace period, and KILL. Only after all group signals and sentinel
  reaping may the slot be retired.
- **Terminal-record dedup**: terminal ledger records are committed at most
  once per run (deduplicated), and the committed record is read back from the
  ledger and reconciled before success is reported.
- **Outer exception boundary**: the whole run is wrapped in an outer exception
  boundary; any uncaught failure is reported as a sanitized failure with
  exit 2 (fail-closed), never silently swallowed.
- **Canary and minimum thoughts**: canary-substring and minimum-thoughts
  enforcement is unchanged (see "What the gate enforces").

## Documented limits

The following are outside the wrapper's guarantee and require external
supervision or operator awareness:

- external SIGTERM/SIGINT delivered to the wrapper or the child can bypass
  cleanup and terminal reconciliation;
- SIGKILL of the wrapper, storage loss, unrecoverable process failures, and
  orphaned grandchildren are out of scope; external supervision remains
  necessary;
- the group-identity sentinel is in-process protection: an externally killed
  sentinel, escaped descendants, resource exhaustion, or an external signal
  killing the wrapper defeat it;
- sentinel startup may itself block; a failure there is reported as a
  sanitized failure with exit 2 and may require reconciliation.

## Rollout and deployment status

- Status: **deployed on the instance (2026-11-26)** after a fix10–14
  architecture simplification, with the test suite green (186 tests) and an
  independent review chain R11–R15 with the final verdict PASS-with-notes
  (LOW findings applied). The audited, reviewed implementation is mirrored
  byte-identical in `scripts/st-enforce/` in this repository; its fixtures are
  marked UNVERIFIED there.
- Rollout of any future configuration change of the instance dispatch path is
  a configuration change, not a repository change.

## Rollback

Stop new dispatches if rollback is needed. Rollback requires explicit operator
authorization; it must not bypass the gate. Keep the gate intact for in-flight
runs until they finish or are stopped and recorded as failures. Resume dispatches
only through an authorized, functioning enforcement gate.

## References

- Two-agent bridge contract: `docs/34-agora-goose-bridge.md` and the
  `agora-goose-bridge` Skill (`skills/coordination/agora-goose-bridge/`).
- Workflow procedure: the `sequential-thinking-workflow` Skill and
  `docs/14-sequential-thinking-workflow.md`.
