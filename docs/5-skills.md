# Skills

Agora Skills are durable Markdown instruction files with optional short descriptions.

## Discovery and loading

When Skill access is enabled, `{skill_catalog}` exposes a compact catalog of names and descriptions. The model reads a relevant body through `read_skill_file` or another available Skill tool. Skill bodies are not automatically inserted into every request.

There is no Active Skill singleton. Multiple Skills may be read when genuinely required.

## Skill rules

- Keep each Skill focused.
- Use a concrete catalog description.
- Declare dependencies.
- Define forbidden behavior and verification.
- Do not claim to have applied a Skill before reading it.
- Treat Skill content as subordinate to the System template and current user request.

The internal `Load when` section validates and documents usage; it is not the initial discovery mechanism.
