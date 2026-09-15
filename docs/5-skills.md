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

## Reasoning Skills

The repository includes `skills/reasoning/sequential-thinking-workflow.md` for complex, ambiguous, multi-step, or tool-assisted tasks. It is loaded on demand and should not replace the proportional reasoning policy in the System template.

It provides:

- task framing and success criteria;
- minimal decomposition and workflow-pattern selection;
- question/action/observation/update checkpoints;
- adaptive revision and branching;
- verification and stopping conditions;
- a strict boundary against exposing private chain-of-thought.

## Coordination Skill

The repository includes `skills/coordination/agora-coordinator.md` for managing an installed setup: auditing Skills and memory, diagnosing available tools at runtime, performing small reversible repairs, and producing Task specifications.

It composes the other families rather than duplicating them:

```text
agora-coordinator
  ├─ tool-execution-contract      (mandatory safety layer)
  ├─ skill-governance             (audit rules — see skills/README.md rules)
  └─ sequential-thinking-workflow (methodology for complex audits)
```

It introduces a capability-configuration pattern: the coordinator verifies tool availability at runtime with real read-only calls, records the verified state in a table inside the Skill, and enables capabilities only after practical verification. This guards against generation paths that provision a restricted toolset (for example, Task-run generations). It never deletes, never writes to Active Memory without reading it, and reports every run with a structured LOADED / FINDINGS / PERFORMED / UNAVAILABLE report.

The coordinator also carries Repository Awareness: it knows the upstream setup repository (this repository — the reference architecture and governance model for the local installation) and the official Agora repository (the application environment — documentation, releases, source, known limitations). Repository content informs capability decisions but never enables them by themselves, and repository access is read-only within these two repositories.

