# Changelog

All notable changes to this repository are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning is semantic (MAJOR.MINOR.PATCH) and tagged. Each release records
the Agora app baseline it was maintained against.

## [Unreleased]

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

### Fixed

- Stale Skill references after the SKILL.md migration (`docs/5`, `docs/20`,
  `docs/21`, `docs/28`) and CI-era drift: README status line, `docs/29`
  verification step, `tasks/repo-sync-weekly` card, and the
  `github-release-workflow` Skill now reflect the CI gate; the coordinator
  Skill capability table was re-verified against runtime.
- Instance-facing normative texts (System template memory gate, `docs/20`)
  quote the deployed instance naming (`.md` catalog names); a naming note in
  `docs/5` explains repository layout vs. instance store naming.

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