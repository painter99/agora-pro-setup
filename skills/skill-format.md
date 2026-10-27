# Skill Format

Use this structure for every reusable Agora Skill. It extends the earlier
10-section baseline with three optional sections so the template also matches
real installed Skills (for example the coordination family), without making
them mandatory for small Skills.

## SKILL.md packaging (Agent Skills standard)

Every Skill is a directory `skills/<family>/<skill-name>/` containing a
`SKILL.md` file — the open [Agent Skills](https://agentskills.io/specification.md)
layout. The `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: skill-name
description: "One compact sentence shown in skill catalogs; mirrors the Catalog description."
license: MIT
---
```

- `name` follows the Agent Skills naming rules (lowercase letters, digits,
  hyphens; no leading/trailing/consecutive hyphens) and must equal the
  directory name.
- `description` (max 1024 characters) must be identical to the body's
  `## Catalog description` text; `scripts/check_format.py` enforces both.
- The 10 required sections stay in the Markdown body below the frontmatter.
- Keep `SKILL.md` under 500 lines; move stable factual material out of the
  Skill instead of growing it.
- Cross-Skill references use the Skill name (the directory name), for example
  `tool-execution-contract`, not a file name.

## Required sections

1. `# Skill: <name>`
2. `## Catalog description` — one compact sentence; this is what `{skill_catalog}` shows.
3. `## Purpose` — what problem the Skill solves.
4. `## Load when` — concrete triggers for reading the body.
5. `## Do not load when` — explicit anti-triggers to prevent overloading.
6. `## Dependencies` — other Skills by exact Skill name (the directory name), or "None".
7. `## Workflow` — ordered, executable steps.
8. `## Forbidden behavior` — actions the Skill must never take.
9. `## Verification` — how completion is confirmed.
10. `## Output contract` — the exact shape of the final report or answer.

## Optional sections

Add only when they carry real weight; an empty section is worse than none.

- `## Hard limits` — per-run budgets: maximum file edits, Task specifications,
  delegation depth, retry counts. Use for coordination or write-capable Skills.
- `## Repository / context awareness` — which external references define the
  Skill's environment and their authority order. Use when the Skill depends on
  documented external state.
- `## Related docs` — pointers to repository documentation that explain the
  surrounding layer (for example `docs/8-tools-and-safety.md`). Use for Skills
  that implement a documented architecture layer.

## Discovery and authority

- The native `{skill_catalog}` is the primary discovery layer; the catalog shows
  the Skill name and `Catalog description`.
- The internal `Load when` section is secondary validation and documentation.
- A Skill cannot override the System template, the current user request, Agora
  permissions, approval gates (see `docs/17-permission-model.md`), or observed
  tool output.

## Size and placement

- Keep a Skill focused; split large procedures when routing or verification
  becomes difficult.
- Move stable factual material into Saved Memory or a reference file.
- Domain-specific Skills follow the same template plus the domain-package
  pattern in `docs/18-domain-routing.md`.

## Example skeleton

```markdown
---
name: example-name
description: "One sentence shown in the Skill Catalog."
license: MIT
---

# Skill: example-name

## Catalog description
One sentence shown in the Skill Catalog.

## Purpose
...

## Load when
- ...

## Do not load when
- ...

## Dependencies
- `tool-execution-contract` (or None)

## Workflow
1. ...

## Forbidden behavior
- ...

## Verification
- ...

## Output contract
- ...
```
