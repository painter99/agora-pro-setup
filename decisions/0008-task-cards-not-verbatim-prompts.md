# ADR-0008: Scheduled tasks are documented as cards, not verbatim prompts

- Status: accepted (2026-10-27, operator GO)
- Supersedes: none

## Context

Task prompts contain personal context; the public repository must stay
anonymized. The application's task mechanics are upstream behavior that this
repository must not duplicate (ADR-0001).

## Decision

`tasks/` contains genericized cards — purpose, schedule shape, constraints,
and outputs — with an explicit disclaimer that cards are not the original
prompts. Live task instances exist only in the application and are maintained
separately.

## Consequences

- Public documentation stays privacy-safe.
- Card-to-instance drift is possible; the repository maintenance policy
  (`docs/29`, §5) covers keeping cards aligned with reality.
- A card never substitutes for the live prompt when judging agent behavior.