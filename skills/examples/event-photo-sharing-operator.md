# Skill: event-photo-sharing-operator

## Catalog description

Operate a self-hosted event photo-sharing app (Memtly) at a one-off event: QR uploads, kiosk slideshow, offline LAN, day-D runbook, failure ladder.

## Purpose

Run a private, self-hosted photo wall at a single event (wedding, party, reunion) with zero development: guests scan a QR code and upload photos from their phones, a tablet shows a live slideshow, and the hosts receive the complete album afterwards. The Skill keeps the operator role sane — a short morning setup, then the system runs unattended — and makes sure new information lands in the right project file instead of a chat log.

## Load when

- Planning or operating a one-off event photo wall (QR uploads, guest gallery, kiosk slideshow).
- Deploying or configuring Memtly (formerly WeddingShare) via Docker Compose.
- Preparing an event-day runbook, dry run, dress rehearsal, or change freeze.
- Questions about guests on Wi-Fi without internet, iOS Wi-Fi Assist behavior, or Wi-Fi QR codes on a LAN.

## Do not load when

- Building a custom photo app (this Skill deploys existing software; it forbids development).
- General event planning with no photo-sharing component.
- Immich/Nextcloud/Ente deployments — different stacks; use their own documentation.

## Dependencies

`memory-master-index.md` before any write to project files (memory gate). A project file set (hub, artifacts, checklists) in Saved Memory; see Repository / context awareness.

## Workflow

1. Read the project hub file (status, open items, timeline), then the artifacts file (compose, settings, QR syntax, day-D runbook) and/or checklists as the topic requires.
2. When the user brings a new fact (venue answer, client decision, test result), record it in the matching project file through the memory gate: patch, do not rewrite; verify by re-reading.
3. Day D morning (operational authority = printed runbook): power → router on → laptop wired (IP = DHCP reservation) → `docker compose up -d` → `docker compose ps` → self-test with own phone (Wi-Fi QR → gallery QR → upload → photo visible) → tablet kiosk on stand → cards on tables → MC briefing (30-second announcement) → verify the backup timer (`systemctl list-timers | grep backup`).
4. Then autopilot: review off, backup timer (rsync to USB every 30–60 min), tablet auto-refresh (idle refresh ~5 min), `restart: always`. The operator stays a guest; check the tablet only in passing.
5. Failure ladder (a non-technical helper can execute it from the laminated runbook): ① `docker compose restart` → ② reboot laptop (Docker and timer start themselves) → ③ power-cycle the router → ④ still nothing: guests keep shooting as at any event; cards stay; nothing is lost.

## Forbidden behavior

- No development, no image upgrades, and no setting changes during the change freeze (T-1 week) and on day D.
- Never use `DATABASE_SYNC_FROM_CONFIG` (destructive settings reset).
- Never allow HEIC; keep allowed file types `.jpg,.jpeg,.png,.mp4,.mov`.
- Never run destructive Docker commands over event data (`docker volume rm`, `docker system prune`, `down -v`).
- Wi-Fi SSID/password never with `\ ; , :` characters (Wi-Fi QR escaping); laptop always wired to the router; client isolation off.
- Never publish guest photos publicly without consent; do not reveal the surprise to guests before day D.
- Do not discuss technical details with the event's principal (host/couple) — "I handle the tech" is the whole sentence; do not recruit a techie among guests.

## Verification

- Day D: test upload visible in the gallery; `docker compose ps` = running; backup timer listed; tablet slideshow running; a new photo appears within ~5 minutes.
- Dry run / dress rehearsal: every checklist item checked; notes recorded in the artifacts file; unresolved items moved to open items in the hub file.
- After every memory write: re-read the result and verify cross-references in the hub.

## Output contract

- Status: OK / WARNING / BLOCKER, what was done, evidence (command output, re-read file, checked checklist item), and next steps with owner and date.
- For new facts: which project file they were recorded in and what changed.

## Repository / context awareness

- Project hub file — main routing (status, open items, timeline); always read first.
- Artifacts file — compose template, admin settings, Wi-Fi QR syntax, table card, day-D runbook (authority on day D), handover plan.
- Checklists file — purchase list, dry run, dress rehearsal, change freeze, day D morning, after the event.
- Authority: System template and current user request > this Skill > project files; on day D the printed runbook is the operational authority.

## Related docs

- Memtly documentation: https://docs.memtly.com (setup, settings, gallery configuration).
- Docker Hub: https://hub.docker.com/r/memtly/memtly (pin the release tag for an upcoming event).