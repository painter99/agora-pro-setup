# ADR-0022: Controlled Git operations adopted as the goose-git-ops Skill
- Status: accepted 2026-11-21 (operator decision)
- Supersedes: none
## Context
`docs/38` proposed controlled Git operations for coding agents (controller,
fresh gate context, authorization service, isolated broker, immutable
snapshots, durable audit) and `docs/39` drafted the matching `goose-git-ops`
Skill. Both carried a PROPOSAL/DRAFT status granting no authority. The
operator decided the workflow will be used going forward and approved its
adoption into the setup.
## Decision
- Adopt `skills/shell/goose-git-ops` as the project Skill for requesting
  authorized Git operations. `docs/38` remains the design reference and
  `docs/39` the draft of record.
- The broker/authorization infrastructure described in `docs/38` is not yet
  implemented or verified: the Skill operates in **advisory mode only**.
  Direct commit/push/merge through the established routes stays subject to
  the existing rules (`github-release-workflow`, operator approval gates).
- Adoption grants no credentials, no new permissions, and no authority to
  bypass platform protections or operator approval gates.
## Consequences
- Component counts change: 36 SKILL.md files, 23 decision records.
- Non-advisory use requires the broker path to be implemented and its
  isolation independently demonstrated first; until then the Skill is
  process discipline, not a security boundary.
