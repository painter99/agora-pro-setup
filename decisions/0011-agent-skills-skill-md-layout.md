# ADR-0011: Skills use the Agent Skills (SKILL.md) layout

- Status: accepted
- Date: 2026-10-27

## Context

Skills were flat Markdown files (`skills/<family>/<skill-name>.md`) with a
custom 10-section format. The open [Agent Skills](https://agentskills.io/specification.md)
standard (originated by Anthropic, adopted by a growing set of agent tools)
defines a Skill as a directory with a `SKILL.md` file: YAML frontmatter
(`name` matching the directory, `description`, optional `license`) plus a
Markdown body. Aligning with the standard makes the Skill library portable
across skills-compatible agents instead of readable only by this setup.

The Agora application consumes its own local flat Skill store and does not
read this repository, so the layout change has no runtime impact on the
deployed instance; it affects only the reference repository and the import
instructions.

## Decision

Adopt the Agent Skills layout fully (no dual format):

- One directory per Skill: `skills/<family>/<skill-name>/SKILL.md`.
- `SKILL.md` carries YAML frontmatter — `name` (equals the directory name,
  Agent Skills naming rules), `description` (identical to the body's
  `## Catalog description` text), `license: MIT` — and the existing
  10-section body below the frontmatter.
- Cross-Skill references use the Skill name (the directory name), not a
  file name.
- `scripts/check_format.py` validates frontmatter, naming rules, the
  description/body consistency, the 10 sections, and rejects stray Markdown
  files under `skills/`.
- Import instructions (`docs/2-installation.md`, `README.md`,
  `skills/README.md`) reference the new layout.

A dual format (keeping flat copies alongside `SKILL.md` directories) was
rejected: duplicated content drifts apart, which is the exact failure mode
this repository's observability discipline exists to prevent.

## Consequences

- The Skill library is consumable by Agent Skills-compatible tooling.
- The 10-section format remains the body convention and stays enforced.
- The local Agora instance imports `SKILL.md` content unchanged; its flat
  store and Czech localizations are separate instances (see ADR-0009).
- `check_format.py` gained frontmatter checks; CI runs them on every push.