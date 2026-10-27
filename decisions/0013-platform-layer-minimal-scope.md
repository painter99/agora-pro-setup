# ADR-0013: platform layer — minimal scope

- Status: accepted (2026-10-27, per the pre-agreed dry-run gate)

## Context

The P2 plan gated the platform-layer scope on the replication dry-run: blocking
host-layer gaps would justify a host bootstrap script; a clean run would not.
The dry-run (2026-10-27, fresh-agent simulation over a clean HTTPS clone) found
zero blocking gaps — the installation path is walkable end-to-end without
host-level automation.

## Decision

Minimal scope: parameterized systemd unit templates for the MCP server, the
sequential-thinking bridge, and the exchange watcher (real-time service, scan
service, timer), plus an install manifest mapping templates to targets, and
`docs/31`. No host bootstrap script. The MCP stdio bridge remains
documentation-only (ADR-0006). All host-specific values are placeholders
resolved from the private instance overlay (ADR-0009).

## Consequences

- Host setup stays a documented manual procedure (docs/23, docs/31) —
  acceptable for a single-host reference architecture.
- The units are placeholders-only, so the repository stays free of ports,
  paths, and hostnames (convention 1); the privacy scan covers `.service` and
  `.timer` files.
- A bootstrap script would need a new ADR with blocking-gap evidence;
  otherwise it stays deferred (over-engineering gate).