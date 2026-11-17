# ADR-0021: Skill licensing and provenance records
- Status: accepted 2026-11-17 (operator instruction)
- Supersedes: none
## Context
Skills ported into this repository carried per-skill `LICENSE.txt` files and
provenance/origin sections, and some Skills recorded their own version history
under a `## Sources` heading. This duplicated licensing information, blurred
the boundary between genuine external adoption and internal history, and made
the Skill directories noisy.
## Decision
- Licensing is expressed exactly once: the repository-root `LICENSE` plus the
  `license: MIT` frontmatter field required by `skills/skill-format.md`.
  Per-skill licence files are not used.
- A `## Sources` section records only genuine adoption of external material
  (third-party Skills, external references). A Skill's own version history is
  not a Sources section; it belongs to `CHANGELOG.md` and git history.
## Consequences
New Skills must not ship a `LICENSE.txt` or a self-history Sources section.
`scripts/check.sh` validates format but does not enforce this rule; it is
normative here. Removed content remains recoverable from git history.
