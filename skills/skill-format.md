# Skill Format

Use this structure for every reusable Agora Skill.

## Required sections

1. `# Skill: <name>`
2. `## Catalog description`
3. `## Purpose`
4. `## Load when`
5. `## Do not load when`
6. `## Dependencies`
7. `## Workflow`
8. `## Forbidden behavior`
9. `## Verification`
10. `## Output contract`

## Discovery

The native `{skill_catalog}` is the primary discovery layer for Agora Skills. The catalog contains the file name and short description. The internal `Load when` section is secondary validation and documentation; it cannot be the initial trigger because the file must be read first.

## Authority

A Skill cannot override the System template, the current user request, Agora permissions, approval gates, or observed tool output.

## Size

Keep a Skill focused. Split large procedures when they become difficult to route or verify. Move stable factual material into Saved Memory or a reference file.
