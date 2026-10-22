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
└── control/           # watcher state and logs — agent account only
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

| Role | Access | Mechanism |
|---|---|---|
| Agent (on the host) | full read/write on the whole tree | the host account that owns the tree (shell transport, docs/22) |
| Operator (from the phone) | read/write on the exchange tree, **no** access to `control/` | dedicated restricted SFTP account, group-based |

- The operator account is **not** the agent's account and has no shell.
- `control/` (watcher state) is reachable only by the agent account.
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

## 5. Cursor and acknowledgment discipline

The agent reads exchange events through a cursor, not by re-listing the tree:

1. Read events **after the last acknowledged event ID**.
2. Review the whole batch (open, sort, archive — as far as the autonomy rules
   allow).
3. **Only then** advance the cursor.

Listing events is not proof that the underlying files were opened or archived;
the cursor means "this batch was reviewed", nothing more.

## 6. Notification wiring

Placement of a finished file into `outbox/to-phone/` is wired to the
notification layer (docs/24): a short, **neutral** push ("1 file ready in
`<project>` outbox") — no file names or contents that would leak context
through a push relay.

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

## 8. Anti-patterns

- Enabling continuous auto-sync instead of the explicit tree.
- Treating an upload as backup, approval, or confirmation.
- Opening or unpacking `quarantine/` content automatically.
- Storing secrets as plaintext in the exchange tree.
- Letting exchange content leak into public repos via copy-paste or scripts.
- The watcher (or the agent) silently moving, renaming, or deleting user files.
- Giving the operator account access to `control/` or a shell.

## 9. Version coupling

The pattern depends only on stable capabilities: file access from the
operator's device (SFTP-class), shell access for the agent, and event-cursor
tools. On each major upstream release, re-validate: event tool semantics,
acknowledgment behavior, and the SFTP account's permission boundaries.