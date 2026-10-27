# ADR-0003: Always-applicable rules live in the kernel, not only in Skills

- Status: accepted (2026-10-20, reinforced 2026-10-25 after a production failure)
- Supersedes: none

## Context

The Skill Catalog is discovery, not execution: a rule that lives only behind
an optional Skill lookup never fires when the Skill is not loaded. The memory
gate existed as a Skill-only rule and demonstrably did not fire until its
core was stated in the System template. A later production failure
(2026-10-25) added a second lesson: kernel wording must name the exact tool
family, because a Skill name read with the wrong tool family fails silently.

## Decision

Rules that must hold in every conversation are stated in the System template,
compactly and with exact tool names. Skills may elaborate on kernel rules but
never carry the only copy of one.

## Consequences

- The kernel stays small but normative.
- Kernel wording changes are behavior-bearing: they need the same care as
  code changes and a verification pass after deployment.
- Two kernel rules exist today: the memory gate and the tool-call budget.