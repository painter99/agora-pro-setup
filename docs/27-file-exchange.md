# 27 — Operator-agent file exchange (pattern)

> A reusable pattern for a deliberate file-handover layer between an operator's
> phone and a headless agent host: a shared directory tree with a strict
> directory contract, a restricted operator account, a metadata-only watcher,
> and an event-cursor discipline. Generic by design — personal specifics
> (account names, real paths, file contents) never belong in a public
> repository; they live in the operator's private memory and local config.

## 1. Purpose

The phone-orchestrated platform (docs/22) moves **commands** (shell relays) and
**alerts** (notification layer, docs/24). Files are the missing leg: photos,
documents, exports, generated artifacts that must travel between the operator's
phone and the host. Two extremes both fail:

- **Auto-sync** (continuous two-way mirroring) silently propagates everything,
  including files that were never meant to leave the phone — an anti-pattern
  (docs/22 §9).
- **Ad-hoc one-off transfers** (a manual copy per request) scale poorly, leave
  no trace, and mix "operator-provided" with "agent-produced" files in
  arbitrary places.

The exchange pattern is the middle ground: **explicit, on-command transfers
through a shared tree with fixed roles per directory** — the agent always knows
where new operator files appear, and the operator always knows where finished
results wait.

## 2. Directory contract

```text
<exchange-root>/
├── inbox/
│   ├── from-phone/    # new files uploaded by the operator; unsorted until reviewed
│   └── to-review/     # files waiting for a purpose decision
├── workspace/
│   └── <project>/     # working files per project
│       ├── current/   # approved current copies
│       └── snapshots/YYYY-MM-DD/   # immutable dated snapshots
├── archive/
│   ├── phone/photos/YYYY/MM/           # long-term, manually sorted operator files
│   ├── phone/documents/YYYY/MM/
│   ├── projects/<project>/snapshots/YYYY-MM-DD/
│   └── agent/full-exports/YYYY-MM-DD/  # may contain sensitive data — check before unpacking
├── outbox/
│   └── to-phone/<project>/             # finished files, ready for operator download
├── quarantine/        # unknown/suspicious files — never opened or unpacked automatically
└── .control/          # watcher state and logs — agent account only, hidden (dot-prefixed)
```

Rules of the contract:

- **Upload is not approval.** A file landing in `inbox/` is neither a confirmed
  backup nor approval to process; it is sorted after review.
- **Snapshots are immutable.** `snapshots/YYYY-MM-DD/` directories are written
  once and never edited in place.
- **`outbox/` is terminal.** Files there are finished products; the agent does
  not consume from it.
- **`quarantine/` is inert.** Unknown or unexpected files go there and stay
  untouched until the operator decides.

## 3. Permissions model

The pattern's core discipline is **write-in / read-out**: the operator has
exactly one writable place (the inbox), everything else is read-only, and the
control subtree is invisible to the operator. This is enforced by the
filesystem, not by convention.

| Directory | Operator (phone) | Agent (on the host) |
|---|---|---|
| `inbox/from-phone/` | **upload + manage own uploads** — the only writable place | full |
| `inbox/to-review/` | read-only | full |
| `workspace/`, `archive/` | read-only (download) | full |
| `outbox/to-phone/` | read-only (download) | full |
| `quarantine/` | read-only | full |
| `.control/` | **no access** (hidden, dot-prefixed) | full |

Mechanism (generic recipe):

- The operator account is SFTP-only: chrooted (`ChrootDirectory`), forced
  command `internal-sftp` with a restrictive umask, key-only auth, no shell,
  no TTY, no forwarding.
- The exchange tree is bind-mounted into the chroot; directories are owned by
  the agent account with a shared group; only the inbox carries the
  group-writable bit (`rwxrws---`, setgid), everything else is `r-x` for the
  group.
- Deletion outside the inbox is therefore **structurally impossible** for the
  operator — a rule that does not depend on convention or memory.
- The control subtree is dot-prefixed (`.control/`) so it does not appear in
  ordinary SFTP listings; its permissions additionally deny the operator's
  group outright.
- The agent creates subdirectories with the setgid bit so the group
  inheritance holds everywhere.
- No shared credentials between devices or people (docs/22 §3 auth baseline).

## 4. The watcher (metadata-only)

A small host-side watcher keeps an append-only record of the tree:

- Records **metadata only**: relative path, size, SHA-256 — never file content.
- **Stability check:** an upload is reported as complete only after repeated
  consistent observations; a file still changing size is marked in-progress.
- **Never mutates:** the watcher does not move, delete, open, or unpack user
  files; sorting and archiving are deliberate, verified agent actions.
- **Initial inventory baseline:** files present at watcher creation are not
  reported as new.
- Events go to an append-only JSONL log plus a state file (last inventory,
  last scan, last change ID).

### 4.1 Neutral push notifications

Stable additions are pushed to the operator's phone through the notification
layer (docs/24):

- a new stable file under `outbox/` → a neutral push (count + project label,
  never file names or contents);
- a new stable file under `quarantine/` → a high-priority alert ("requires
  review");
- notifications are deduplicated by event id (a small state file in the
  control subtree); a failed push is retried on the next scan;
- notifications fire only when an upload has stabilized (second consecutive
  observation) — unstable uploads stay silent by design.

### 4.2 Real-time event layer (inotify watch mode)

The periodic scan is the reconciliation layer; a second, event-driven layer
provides immediacy. The same watcher script gains a long-running watch mode
that uses the kernel's inotify API directly (through `ctypes`, no extra
packages) and watches the tree from the host side — exactly where the
in-process SFTP server's logging limitation (§7) does not apply.

- **Completion signals, not polling:** `close_write` and `moved_to` mean the
  content is complete; the watcher hashes the file immediately and records
  the event with the same schema as the scan, plus `origin` and `actor`
  fields.
- **Actor attribution is correlation, not proof:** an active SFTP session for
  the operator account (a process-list probe at event time) marks the event
  as `sftp`, anything else as `local`. Exact per-syscall attribution would
  require the audit subsystem and is deliberately not used.
- **The observer cannot observe itself:** the private control subtree is
  excluded from watching.
- **One log, one state, one push pipeline:** the watch mode appends to the
  same JSONL log, updates the same state file, and claims the same
  notification cursor — all under an advisory file lock shared with the
  periodic scan. A healthy watcher therefore leaves the scan nothing to
  report, and neither layer double-notifies.
- **Tiered push policy:** `outbox/` additions → default priority ("ready for
  download"); `inbox/` additions → low priority (a silent receipt
  acknowledgment); `quarantine/` → high priority. Events inside a short
  quiet window are batched into a single push. Deletions, renames, and
  workspace/archive activity are logged but never pushed.
- **The scan remains the safety net:** it catches events missed during
  watcher downtime; if it finds unnotified events while the watch service is
  supposed to be running, it raises a low-priority "watcher missed events"
  alert.

Honest limits: reads are not logged (only the audit subsystem could); an
aborted transfer still produces a completion event when the connection tears
down (the kernel closes the descriptor), so a partial size can be recorded —
the periodic scan and operator review remain the correction path; and a
watcher crash inside the batching window can lose a push (the event itself
stays in the log).

## 5. Cursor and acknowledgment discipline

The agent reads exchange events through a cursor, not by re-listing the tree:

1. Read events **after the last acknowledged event ID**.
2. Review the whole batch (open, sort, archive — as far as the autonomy rules
   allow).
3. **Only then** advance the cursor.

Listing events is not proof that the underlying files were opened or archived;
the cursor means "this batch was reviewed", nothing more.

## 6. Notification and health wiring

- The outbox and quarantine pushes (§4.1) close the awareness loop: the
  operator does not poll the tree; the phone tells them when a result is
  ready or when something needs attention.
- The host health check covers the exchange layer: tree size (the handover
  layer is not durable storage — alert over a threshold) and liveness of both
  watcher layers — the periodic timer and the real-time watch service.

## 7. Rules

1. **Nothing from the exchange tree is automatically copied into public
   repositories.** Public artifacts are committed deliberately, after a privacy
   scan, through the repository's own workflow.
2. **No secrets in the exchange tree** — no passwords, private keys, or tokens
   in plaintext; secrets belong in root-owned `600` config files (docs/24 §4).
3. **Verify before archiving:** name, size, and SHA-256 checked; nothing
   overwritten silently; on conflict, ask the operator.
4. **The host is not a backup.** Important files keep at least one independent
   copy elsewhere; the exchange tree is a handover layer, not durable storage.
5. **Sorting is a level-2 action.** Moving or archiving operator files follows
   the autonomy model (docs/22 §4): propose → approve → execute → verify, or
   stays within individually granted idempotent moves.
6. **Audit is three-layered.** Session logs record who connected, when, from
   where, with which key; the real-time event log records every content
   change within seconds (path, size, SHA-256, actor correlation); the
   periodic scan reconciles stability and checksums. Per-operation SFTP
   logging (open/read/write per file) is not provided by the in-process
   `internal-sftp` server on current OpenSSH releases; if it is ever
   required, it means switching to the standalone sftp-server binary inside
   the chroot — a deliberate maintenance burden (binary and library copies
   refreshed on every OpenSSH upgrade), adopted only for a concrete forensic
   need. File reads remain unlogged by design unless that need arises.

## 8. Anti-patterns

- Enabling continuous auto-sync instead of the explicit tree.
- Treating an upload as backup, approval, or confirmation.
- Opening or unpacking `quarantine/` content automatically.
- Storing secrets as plaintext in the exchange tree.
- Letting exchange content leak into public repos via copy-paste or scripts.
- The watcher (or the agent) silently moving, renaming, or deleting user files.
- Giving the operator account access to `.control/` or a shell.

## 9. Version coupling

The pattern depends only on stable capabilities: file access from the
operator's device (SFTP-class), shell access for the agent, and event-cursor
tools. On each major upstream release, re-validate: event tool semantics,
acknowledgment behavior, the SFTP account's permission boundaries, the
real-time watcher's kernel event interface (inotify semantics and limits),
and — noted explicitly — whether the in-process SFTP server still does not
log per-operation events (§7, audit).