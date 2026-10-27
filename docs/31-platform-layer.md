# 31 — Platform layer: parameterized host units

The repository is otherwise documentation and agent-side configuration; this
directory is its only host-coupled layer: the systemd units that run the
structured tool layer and the file-exchange watcher on the build host
(docs/22 §6–7, docs/25, docs/27). The narrative walkthrough of the host itself
is docs/23; this document covers only the unit templates and their install
mapping.

## Contents

| File | Purpose |
|---|---|
| `agora-mcp.service` | FastMCP server, Streamable HTTP (docs/22 §6, docs/25) |
| `agora-mcp-seqthink.service` | sequential-thinking server behind a stdio→Streamable HTTP bridge (docs/25) |
| `agora-exchange-events.service` | exchange watcher, real-time inotify watch mode (docs/27) |
| `agora-exchange-watch.service` | exchange watcher, periodic scan mode (docs/27) |
| `agora-exchange-watch.timer` | timer driving the scan mode |
| `install-manifest.yaml` | template → target mapping + placeholder names |

## Parameterization

Every host-specific value is a `{{PLACEHOLDER}}`; the repository never contains
real ports, paths, or usernames (AGENTS.md, convention 1). Placeholder values
live in the private instance overlay (docs/30) and are substituted at install
time:

| Placeholder | Meaning |
|---|---|
| `SERVICE_USER`, `SERVICE_GROUP` | unprivileged host account that runs the services |
| `AGORA_HOME` | agent workspace root on the host |
| `SEQTHINK_PORT`, `SEQTHINK_PATH` | bridge listener port and URL path |
| `EXCHANGE_DIR` | file-exchange root |
| `TOOLS_DIR` | directory holding the watcher script |

The MCP server's bind address and port are configured in the server
code/config (docs/22 §6), not in the unit — the unit only starts it. The
templates inline `NoNewPrivileges=yes`; the maintained instance applies the
same hardening via a drop-in, which is equivalent.

## Install flow

1. Resolve placeholders (instance overlay values) into the unit files.
2. Copy each file to its target path from `install-manifest.yaml`
   (`/etc/systemd/system/`).
3. `sudo systemctl daemon-reload`.
4. `sudo systemctl enable --now` each service and the timer.
5. Verify: `systemctl is-active` and `is-enabled` per unit; listeners match the
   expected set (docs/22 §6, docs/25 §3); a test file movement lands in the
   exchange watcher's journal (docs/27 §4).

## Scope boundary (ADR-0013)

Minimal scope by decision: unit templates + install mapping + this document.
No host bootstrap script — the replication dry-run (2026-10-27) found no
blocking host-layer gaps, so bootstrap remains the documented manual procedure
(docs/23). The MCP stdio bridge stays documentation-only (ADR-0006). Instance
automation units (morning brief, calendar reminder, health check, update
reports, audio dispatch) are instance-overlay material (docs/30), not part of
the reference platform layer — they carry personal schedules by design.
Revisit the scope only with a new ADR backed by blocking-gap evidence.

## Related docs

docs/22 (platform architecture), docs/23 (bootstrap walkthrough), docs/25 (MCP
tool layer), docs/27 (file exchange), docs/30 (instance overlay),
decisions/README.md (ADR index).