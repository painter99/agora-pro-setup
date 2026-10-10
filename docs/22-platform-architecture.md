# 22 — Phone-Orchestrated Coding Platform (architecture pattern)

> A reusable pattern for running a personal AI coding platform from a phone:
> a cloud LLM as the brain, the Agora app as the hands, and a dedicated x86_64
> Linux host as the workspace. Generic by design — personal specifics (hardware
> models, project names, schedules, household details) never belong in a public
> repository; they live in the operator's private memory and project docs.

## 1. Pattern summary

```text
            ┌───────────────────────────────┐
            │  LLM PROVIDER (cloud)         │
            │  brain: reasoning + planning  │
            └───────────────▲───────────────┘
                            │ HTTPS API
┌───────────────────────────┴───────────────────────────┐
│  OPERATOR PHONE — Agora app                           │
│  hands: tool execution + state                        │
│  ├─ local sandbox (on-device Linux, light JVM tasks)  │
│  ├─ memory + skills (durable state, routing)          │
│  └─ shell devices (relay: SSH / Conch)                │
└──────────┬─────────────────────────────┬──────────────┘
           │ SSH (LAN / VPN)             │ Conch (LAN / VPN)
┌──────────▼─────────────────────────────▼──────────────┐
│  BUILD HOST — x86_64 Linux, headless                  │
│  workspace: toolchain, repos, containers, jobs        │
└───────────────────────────────────────────────────────┘
```

Rules of the pattern:

- The brain never reaches the host directly; every action is a tool call relayed by the app.
- The host is reachable only from the LAN or a private VPN — never port-forwarded.
- The agent is **episodic**: wake → act → report → sleep. It observes only when it looks.

## 2. Why a separate build host

Mobile sandboxes are convenient but bounded: CPU architecture (parts of the Android
toolchain, e.g. aapt2, ship x86_64-only), RAM pressure, and process lifetime (on some
sandbox runtimes detached processes do not survive a tool call). A small always-available
x86_64 Linux machine removes all three limits and keeps the phone responsive.

**Stateless principle:** keep the host reproducible — sources in git, toolchain and caches
re-downloadable. A stateless host needs no backups and no uptime guarantees; downtime
costs convenience, not data. Introduce durable storage only deliberately, and back it up
from the day it exists.

### Where the workspace lives — operator's choice

The workspace does not have to be one specific kind of machine. The pattern works with
any reachable x86_64 Linux; **the choice between them belongs to the operator**, and the
same platform can migrate between them later:

| Option | Fits when | Trade-offs |
|---|---|---|
| Owned idle machine (laptop/desktop) | interactive builds, no public services, minimal cost | availability depends on the household; no public reachability |
| Small cloud VM | 24/7 availability or public services wanted; no spare hardware | monthly cost; identity/KYC requirements vary by provider |
| Hybrid | stateless builds on the owned machine + a small VM only for what truly needs 24/7 or public reachability | two hosts to keep configured (config-as-code helps) |

Decision rule: start with the cheapest option that covers the **actual** need, and add
infrastructure only when a concrete requirement appears — not speculatively.

## 3. Host baseline (generic)

| Area | Baseline |
|---|---|
| OS | current stable minimal Linux, headless, SSH server only |
| Toolchain | distro JDK (verify against the project's build plugins) + SDK under `/opt` |
| Filesystem | ext4 + `noatime`; periodic TRIM |
| Memory | zram instead of disk swap on RAM-rich hosts; size the build heap to real RAM |
| Firewall | default-deny incoming; SSH and job-server ports from LAN/VPN only |
| Auth | key-only SSH; per-machine deploy keys; no shared credentials |
| Remote | mesh VPN (Tailscale-class) instead of port forwarding |
| Jobs | Conch for durable background jobs and image viewing; plain SSH for interactive work |
| Power | BIOS auto-power-on; battery charge threshold if the host is a laptop |

## 4. Autonomy model

```text
LEVEL 1 — OBSERVE (default)
  scheduled or on-demand sweep: disk, memory, SSD wear, failed units,
  container state, pending updates → compact report, no mutations

LEVEL 2 — PROPOSE (default for any change)
  exact command + expected effect → explicit approval → execute → verify

LEVEL 3 — ACT (whitelist)
  individually granted idempotent operations (service restart, cache prune),
  each logged to an append-only journal on the host
```

**Command allowlist.** At levels 2–3 every mutating command must match an explicit
allowlist (or be individually approved on the operator's phone). Destructive operations —
package removal, service disablement, firewall changes, volume deletion — are never
allowlisted; they always require per-action approval. The allowlist lives on the host,
is version-controlled, and is reviewed on every change.

Safety rails (all levels): per-device confirmation policy; no secret **values** in agent
context (names and paths only); tool-call budget discipline (`docs/21`); a hard cap on
blind retries before switching to diagnosis; destructive actions always behind explicit
approval (`docs/17`).

## 5. State contract (for episodic agents)

```text
WHERE STATE LIVES
├── app memory   → durable facts, decisions, session logs
├── git repos    → code, specs, playbooks, this document
└── host files   → runtime state (clones, caches, stacks, journals)

WAKE-UP PROCEDURE
1. read injected active memory
2. route via skills → load the relevant durable context
3. read runtime state from the host (git status, service state, ...)
4. act within the granted autonomy level, verify results
5. write back only durable changes (memory gate, docs/20)
```

**Pre-flight discovery.** Before every action set, observe the environment — memory and
swap, disk free, SSD wear indicators, failed services, container state, network
reachability between host and operator device, pending updates. Never assume state from
the previous session; the discovery result is part of every report.

**Append-only mutation journal.** Every system change is appended to a journal file on
the host — one line per action: timestamp, actor, command, result. Append-only (no
edits; rotation by size). The journal is the first runtime artifact a wake-up reads
after memory, and it complements (not replaces) git history for configuration.

**Transactional config edits.** Before editing a critical configuration file (e.g.
under `/etc`): create a timestamped `.bak` copy, apply the change, verify (config test,
service restart), and keep the rollback command ready. If the connection drops
mid-edit, the next wake-up detects the `.bak` and either completes or reverts the
change — a half-applied configuration is never left behind.

## 6. Structured tool layer (MCP)

A raw shell is the bootstrap transport, not the only interface. Once the host is stable,
a structured tool layer — the Model Context Protocol — can sit on top:

**App capabilities (verified in source, app v2.1.x):** the MCP client speaks
**Streamable HTTP** (protocol 2025-11-25 with fallbacks) and legacy **SSE**
(2024-11-05); endpoints must be `http`/`https`; **custom headers** are supported for
authentication; there is **no stdio transport** — MCP servers run remotely on the host,
never on the phone.

**Official ecosystem (verified 2026-10):** `modelcontextprotocol/python-sdk` (the
official Python SDK) and `modelcontextprotocol/servers` (official reference servers,
including a filesystem server for precise text-diff edits that protect against
token-bloat rewrites). Caution: verify every component on GitHub before adoption —
project briefings can contain hallucinated names (a draft in this project cited two
shell-guard servers that do not exist).

**Deployment pattern:** MCP servers run on the host, bound to LAN/VPN only; auth via
headers; the shell-guard role (command allowlist) is enforced by the confirmation
policy and the allowlist pattern in §4 — adopt a third-party guard server only after
verifying its maintenance status.

**Open question (resolve at integration):** app-side credential guards may refuse auth
headers over plain `http`. Preferred solution: TLS certificates issued by the mesh VPN
(MagicDNS-style internal names with automated Let's Encrypt issuance) — trusted HTTPS
inside the private network, no self-signed certificates, no public exposure. Fallback:
run MCP without auth headers over the encrypted VPN link, if the app permits.

## 7. Bootstrap sequence (chicken-and-egg)

The first contact with a clean host is always plain shell — MCP servers cannot install
themselves. Standard sequence, each step proposed (level 2) before execution:

```text
OS install (headless, SSH only) → add as SSH device → firewall (LAN-only)
  → toolchain (JDK + SDK) → clone repos → smoke test (build + tests)
  → measure the interaction loop → durable-job server (Conch)
  → only then: structured tool layer (MCP, §6)
```

The bootstrap itself is the first live exercise of the autonomy model: propose,
approve, execute, verify, journal.

## 8. Multi-person extension

When other people join the setup, give each person **their own instance on their own
device** rather than accounts on a shared server: isolation is inherent, personalization
is a per-person template of skills and memory, and no shared infrastructure is required.
Add shared services (storage, media, vault) only when a concrete demand appears
(trigger-based provisioning). If shared compute is ever used: one active orchestrator per
host, per-person keys, resource limits, and no shell access for non-admins.

## 9. Anti-patterns

- Port-forwarding the host or exposing services publicly "just in case".
- Self-hosted CI runners on public repositories (untrusted forks could execute code).
- Auto-sync services enabled by default; prefer explicit, on-command transfers.
- Shared credentials between devices or people.
- Letting a personal decision log, schedule, or device inventory leak into a public repo.
- Assuming continuous monitoring: an episodic agent sees nothing between wake-ups.
- Adopting tooling from unverified names in briefings; every component is checked on
  its upstream source first.

## 10. Version coupling

The pattern depends only on stable app capabilities (shell relays, memory, skills,
automation, remote MCP transports). On each major upstream release, re-validate: task
scheduling behavior, durable-job semantics, image viewing, MCP transport and auth
behavior, and the licensing terms that apply to bundled skills.