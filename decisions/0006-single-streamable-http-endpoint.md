# ADR-0006: One Streamable HTTP endpoint per MCP server; legacy SSE retired

- Status: accepted (2026-10-25, operator GO)
- Supersedes: none

## Context

An early MCP setup exposed both a Streamable HTTP endpoint and a legacy SSE
fallback behind a reverse proxy. The SSE path was a second surface to harden
and monitor with no remaining client need.

## Decision

Retire the legacy SSE transport: the serving unit is disabled and removed and
the reverse-proxy path is closed. Keep exactly one Streamable HTTP endpoint
per MCP server. Verification: no listener remains on the retired path, a
negative connection test is refused, and end-to-end tool calls succeed on the
remaining endpoints.

## Consequences

- Smaller attack surface and one health story per server.
- Transport choice is documented per server (`docs/25`).
- New MCP servers default to Streamable HTTP; a second transport is added
  only with an explicit decision.