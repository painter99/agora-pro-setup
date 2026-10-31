# ADR-0017: File-based active memory replaces injected Active Memory

- Status: accepted (2026-10-31, operator GO)
- Supersedes: none

## Context

Injected Active Memory failed in the maintained instance: the store and the
runtime view desynchronized (patch anchors unmatchable), writes could not be
verified by reading back (no read tool for Active Memory in the deployed
generation), and the block charged its token cost in every message.
Scheduled-task agents never received Active Memory anyway, so the chat and
task paths already diverged.

## Decision

- The current-status layer is a **working state file on a persistent host**,
  named **file-based active memory** (short: file-based AM). Read and written
  with file tools; patch is the default operation; every write is verified by
  reading the file back; a fresh backup precedes any full replacement.
- The maintained instance disables the app's injected Active Memory. The
  kernel sentence routes current-status writes to file tools and names the
  `file-based-active-memory` Skill.
- Skills `active-memory-design` and `active-memory-authority` are retired;
  their invariants (size policy, patch versus replace, authority bands) move
  into `file-based-active-memory` and stay enforced by the kernel gate.
- The `active-memory/` templates are removed from the repository; the content
  remains recoverable from git history.
- The state-file path and content are instance-side (docs/30); they never
  enter this public repository.

## Consequences

- Every write becomes verifiable; the unverifiable-write failure class is
  gone.
- The hot layer is no longer automatically injected — discovery depends on
  the kernel pointer sentence; that trade is accepted.
- Task agents are unaffected (they never received injected Active Memory).
- If a future Agora release makes injected Active Memory verifiable (a
  read-back tool plus per-run freeze), the instance may re-evaluate;
  migration back is a single copy operation.