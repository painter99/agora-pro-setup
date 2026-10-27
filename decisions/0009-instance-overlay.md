# ADR-0009: Instance overlay — public generic base, private localized instance

- Status: accepted (2026-10-27, operator GO)
- Supersedes: none

## Context

One public repository cannot carry personal context; one private instance
cannot serve other agents or users. Both needs are real: replication by other
agents (public layer) and daily operation (private layer). Until now the
relationship between the two was implicit practice, not a documented rule.

## Decision

Adopt the two-layer instance overlay pattern (`docs/30-instance-overlay.md`):
this repository is the generic base (English, anonymized, checked); the live
setup is a private instance (localized, personalized). Imports flow from base
to instance and keep a derivable shape; exports to the base are deliberate
generalizations gated by the privacy scan and operator GO.

## Consequences

- Dual-layer maintenance cost is accepted and bounded by the derivation
  discipline (diffable shapes, import records).
- Layer drift is covered by the scheduled maintenance pass.
- The pattern is itself replicable: it is documented here, not implicit.