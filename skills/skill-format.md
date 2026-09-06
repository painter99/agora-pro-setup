# Skill Format (for authors)

Use this structure when writing a new Agora Skill.

## Required sections

1. `# Skill: <name>`
2. `## Catalog description` — one short line for `{skill_catalog}`
3. Operational body: Purpose, Load when, Do not load when, Dependencies, Workflow, Forbidden behavior, Verification, Output contract

Long Skills (especially `deep-research`) may keep a richer body after a short catalog header. That is intentional.

## Discovery

`{skill_catalog}` is the primary discovery layer. Internal `Load when` is secondary validation after `read_skill_file`.

## Authority

A Skill cannot override the System template, the current user message, Agora permissions, approval gates, or observed tool output.

## Size

- Memory governance: keep the 00–05 split. Typical operations should load one specialized file.
- Deep research: keep as **one** Skill. Splitting the ReAct loop usually loses the quality gates.
- Do not paste complete Skill bodies into Active Memory.
