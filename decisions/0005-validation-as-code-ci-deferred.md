# ADR-0005: Validation lives in the repository as code; CI deferred

- Status: accepted (2026-10-27, operator GO)
- Supersedes: none

## Context

Format compliance and privacy checks were previously run as ad-hoc local
scripts that were not part of the repository; a replicating agent could not
run them, and compliance could silently drift.

## Decision

`scripts/check.sh` is the mandatory pre-commit validation gate: Skill format
compliance (10 required sections, order, code fences excluded),
personal-identifier scan (Markdown and YAML), and relative link integrity.
Conventions and the entry point are documented in `AGENTS.md`. Continuous
integration is deliberately deferred: the repository is docs-only, and a
lightweight lint gate remains a pending decision.

## Consequences

- Checks are reproducible by any agent without infrastructure.
- Until CI is enabled, enforcement depends on discipline; `AGENTS.md`
  convention 2 makes the gate explicit for agents.
- New mechanical conventions extend `scripts/` instead of prose-only rules.
- A check that never failed is unproven: new checkers get a negative test
  (a planted violation must be detected) before they are trusted.