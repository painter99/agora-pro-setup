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

## Memory-governance family

For durable-memory work, use the smallest sufficient set from `skills/memory-governance/`:

```text
memory-master-index
  ├─ active-memory-design
  ├─ active-memory-authority
  ├─ memory-file-operations
  ├─ memory-tool-reference
  └─ memory-audits

shared cross-domain layer: tool-execution-contract
```

The master index routes; specialized Skills contain the procedure. Do not load the entire family for a simple read. Personal facts and project state belong in Active Memory or Saved Memory, never in these reusable Skills.
