# Changelog

All notable changes to this repository are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning is semantic (MAJOR.MINOR.PATCH) and tagged. Each release records
the Agora app baseline it was maintained against.

## [Unreleased]

### Added

- `skill-mirror-check` Skill + weekly task card — verifies that deployed local
  Skills match the repository source of truth (fresh read + diff per Skill,
  classified as content drift / expected overlay / cosmetic); prevents
  instance drift from being misattributed to repository text and triggering
  nonsense repository fixes.

- Two previously local-only Skills published: `skill-governance` and
  `llm-model-evaluation` — closes dangling dependencies in `agora-coordinator`
  and `self-improvement-loop`.

- `memory-tool-reference` Skill published — ported from the local instance,
  reformatted to the SKILL.md layout, and wired into memory routing
  (`memory-master-index` Dependencies, `tool-execution-contract` Domain
  routing).

### Changed

- `aps-upgrade`: repository-first flow for Skill text changes — the setup
  repository is the source of truth; the local instance imports repository
  versions and re-applies the personal overlay (docs/30). Runtime verification
  of new app behavior still precedes any Skill text change.

- `model-escalation-protocol`: Load-when narrowed — the first bullet now
  requires a preventive T7 condition (irreversible action, multi-file
  refactor, 3+ mutually dependent unknowns, money/publication/career) or an
  already-fired trigger; routine multi-step tasks are covered by
  `sequential-thinking-workflow` + `tool-execution-contract` alone
  (D-20261028-04; dogfood eval pending).

### Fixed

- Dependency and format consistency across Skills: `.md` suffixes in
  `self-improvement-loop` Dependencies, prose Dependencies sections
  (`multi-source-research`, `sequential-thinking-workflow`), self-referencing
  description prefixes (`language-fidelity`, `model-escalation-protocol`),
  missing cross-links (`agora-coordinator` → memory audit routing,
  `github-release-workflow`/`cad-spec-driven-workflow` →
  `shell-and-device-operations`), and extended Domain routing in
  `tool-execution-contract`.

- `memory-file-operations`: restored the Saved Memory file taxonomy
  (living topic file / session log / hybrid / buffer with write triggers) that
  was lost during generalization; the local instance relies on it for
  session-log naming and living-file maintenance.

- Broken external MADR link in `decisions/README.md` — now points to the
  official project page (https://adr.github.io/madr/). External URLs are not
  covered by `check_links.py`; they are covered by the quarterly replication
  dry-run.

- Skills deep-audit fixes (2026-10-28): `docs/5` coordinator composition
  diagram updated to the current six dependencies (stale "local instance
  Skill" note removed; peer dependency cycles documented as intentional);
  `tool-execution-contract` Domain routing further extended by
  `language-fidelity`, `model-escalation-protocol`, `llm-model-evaluation`,
  and `aps-upgrade`; description capitalization (`language-fidelity`,
  `model-escalation-protocol`), `memory-master-index` H1 title,
  chronological Sources order in `github-release-workflow`, and a trimmed
  catalog description for `self-improvement-loop`.

## [1.2.0] - 2026-10-27

P2 milestone: SKILL.md layout, CI gate, platform layer, replication golden task.

### Added

- `.github/workflows/check.yml` — CI gate running `scripts/check.sh` on push
  to `main` and pull requests; least privilege, no secrets (ADR-0010,
  supersedes the CI deferral in ADR-0005).
- Skills migrated to the Agent Skills (`SKILL.md`) layout: one directory per
  Skill under `skills/`, YAML frontmatter (`name`, `description`, `license`)
  plus the existing 10-section body (ADR-0011); `check_format.py` now
  validates frontmatter, naming rules, and description consistency.
- ADR-0012 — the repository remains public; sensitive material belongs to the
  private instance overlay, not this repository.
- `agora-coordinator` Skill now routes systemic findings (repeated failures,
  drift patterns) into the self-improvement loop as evaluated deltas instead
  of ad-hoc direct edits.
- `platform/` — parameterized host-level systemd unit templates (MCP server,
  sequential-thinking bridge, exchange watcher service + timer) with an
  install manifest and `docs/31` (ADR-0013, minimal scope per the dry-run
  gate); the privacy scan now covers `.service` and `.timer` files.
- Golden task: a quarterly replication dry-run (fresh-agent simulation over a
  clean clone) is now a scheduled task; card in `tasks/` (docs/29).

### Fixed

- Stale Skill references after the SKILL.md migration (`docs/5`, `docs/20`,
  `docs/21`, `docs/28`) and CI-era drift: README status line, `docs/29`
  verification step, `tasks/repo-sync-weekly` card, and the
  `github-release-workflow` Skill now reflect the CI gate; the coordinator
  Skill capability table was re-verified against runtime.
- Kernel Skill naming: the System template memory gate and the `docs/20`
  normative text now quote repository-layout Skill names (directory names, no
  `.md` suffix), consistent with the import rule in `docs/2`; the `docs/5`
  naming note explains store suffix differences (both forms resolve in the
  maintained instance — verified 2026-10-27). Replication dry-run GAP-2.
- `manifest.yaml`: glob sources carry machine-checkable `files` counts
  (inventory v3) and a new `check_inventory.py` enforces them in `check.sh` —
  the inventory no longer drifts in prose (replication dry-run GAP-1).
- `docs/2` and README: tool names quoted by the kernel gate are documented as
  app-version-coupled, with import-time re-verification guidance.

## [1.1.0] - 2026-10-27

P1 milestone: validation, inventory, and decision records complete.

### Added

- `manifest.yaml` — machine-readable component inventory (source → deployment
  target) for drift detection; the privacy scan now covers YAML files too.
- `decisions/` — architecture decision records (MADR-lite): 8 seeded ADRs
  (add-on-layer policy, docs numbering, kernel rules, tool-call budget,
  validation-as-code, MCP transport, inventory, task cards) + format index.
- `docs/30-instance-overlay.md` + ADR-0009 — instance overlay pattern:
  public generic base ↔ private localized instance, derivation and export
  rules, privacy gates.

### Fixed

- `docs/2-installation.md`: added a prerequisites section (python3/git/bash for repository validation); replaced the stale partial Skill table with the flat-name rule (file name without `.md`), so the document no longer drifts when Skills are added.
- `AGENTS.md`: documented the validation prerequisites.

## [1.0.0] - 2026-10-27

First tagged release: the governance layer as of `main` @ `dfae1bc`.

### Added

- `AGENTS.md` — agent-facing entry point: precedence rule, repository map,
  mandatory conventions, validation entry point.
- `scripts/check.sh` — one-command validation: Skill format compliance,
  personal-identifier scan, relative link integrity.
- `CHANGELOG.md` — this file; versioning policy (semantic version tags).

### Compatibility

- Maintained against Agora app releases from F-Droid; current app baseline is
  the v2.1.x line (see `docs/22-platform-architecture.md`, §6).