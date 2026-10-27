# ADR-0007: Component inventory (manifest.yaml) is the drift anchor

- Status: accepted (2026-10-27, operator GO)
- Supersedes: none

## Context

Drift between this repository and the deployed setup was detected manually.
Cloud agentic-AI operational guidance requires a versioned source of truth
plus scheduled comparison for behavioral configuration (prompts, tool
permissions, decision boundaries); prose-only documentation cannot serve as
that anchor.

## Decision

`manifest.yaml` lists every deployable component with its source path and
deployment target. Inventory updates happen in the same change as the
component (`AGENTS.md` convention 7). A maintenance pass compares the
inventory against the actual repository tree (existence, counts) and against
the deployed setup, and refreshes `last_verified`.

## Consequences

- Drift becomes mechanically detectable instead of anecdotal.
- The inventory itself must stay current: a stale inventory is a false
  source of truth, so its `last_verified` date is part of the check.
- Reference-only material is listed with `target: none` and is not compared
  against a deployment.