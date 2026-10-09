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

## 6. Multi-person extension

When other people join the setup, give each person **their own instance on their own
device** rather than accounts on a shared server: isolation is inherent, personalization
is a per-person template of skills and memory, and no shared infrastructure is required.
Add shared services (storage, media, vault) only when a concrete demand appears
(trigger-based provisioning). If shared compute is ever used: one active orchestrator per
host, per-person keys, resource limits, and no shell access for non-admins.

## 7. Anti-patterns

- Port-forwarding the host or exposing services publicly "just in case".
- Self-hosted CI runners on public repositories (untrusted forks could execute code).
- Auto-sync services enabled by default; prefer explicit, on-command transfers.
- Shared credentials between devices or people.
- Letting a personal decision log, schedule, or device inventory leak into a public repo.
- Assuming continuous monitoring: an episodic agent sees nothing between wake-ups.

## 8. Version coupling

The pattern depends only on stable app capabilities (shell relays, memory, skills,
automation). On each major upstream release, re-validate: task scheduling behavior,
durable-job semantics, image viewing, and the licensing terms that apply to bundled
skills.