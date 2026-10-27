# Changelog

All notable changes to this repository are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning is semantic (MAJOR.MINOR.PATCH) and tagged. Each release records
the Agora app baseline it was maintained against.

## [Unreleased]

### Added

- `manifest.yaml` — machine-readable component inventory (source → deployment
  target) for drift detection; the privacy scan now covers YAML files too.

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