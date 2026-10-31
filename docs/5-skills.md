# Skills

Agora Skills are durable instruction packages: one directory per Skill containing a `SKILL.md` (frontmatter + body), see `skills/skill-format.md`.

## Discovery and loading

How Agora exposes Skills — the `{skill_catalog}` variable, frozen per generation, on-demand reads, and the absence of an active-skill toggle — is defined by the application and documented in the official user manual. This repository adds rules for using that mechanism: multiple Skills may be read when genuinely required, but never load a family wholesale.

Naming: in this repository each Skill is a directory `<name>/SKILL.md`; the
Skill name is the directory name. A deployed Agora instance keeps its own flat
Skill store, and a store populated from older flat files may list catalog names
with a `.md` suffix (as in the maintained instance). Normative texts in this
repository (System template, memory gate) quote the repository-layout names; a
maintained instance's pasted copy may keep the instance form — both forms
resolve in that store (verified 2026-10-27).

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
  ├─ file-based-active-memory
  ├─ memory-file-operations
  └─ memory-audits

shared cross-domain layer: tool-execution-contract
```

The master index routes; specialized Skills contain the procedure. Do not load the entire family for a simple read. Personal facts and project state belong in the working state file or Saved Memory, never in these reusable Skills.

## Reasoning Skills

The repository includes `skills/reasoning/sequential-thinking-workflow/SKILL.md` for complex, ambiguous, multi-step, or tool-assisted tasks. It is loaded on demand and should not replace the proportional reasoning policy in the System template.

It provides:

- task framing and success criteria;
- minimal decomposition and workflow-pattern selection;
- question/action/observation/update checkpoints;
- adaptive revision and branching;
- verification and stopping conditions;
- a strict boundary against exposing private chain-of-thought.

## Coordination Skill

The repository includes `skills/coordination/agora-coordinator/SKILL.md` for managing an installed setup: auditing Skills and memory, diagnosing available tools at runtime, performing small reversible repairs, and producing Task specifications.

It composes the other families rather than duplicating them:

```text
agora-coordinator
  ├─ tool-execution-contract       (mandatory safety layer)
  ├─ skill-governance              (audit rules)
  ├─ memory-audits                 (Saved Memory audit procedure)
  ├─ memory-master-index           (memory routing)
  ├─ sequential-thinking-workflow  (methodology for complex audits)
  └─ self-improvement-loop         (systemic findings route to a SIL delta)
```

Dependency cycles between peer Skills (the Android trio) are intentional peer references, not load cycles — each side is loaded only when its concern is active.

It introduces a capability-configuration pattern: the coordinator verifies tool availability at runtime with real read-only calls, records the verified state in a table inside the Skill, and enables capabilities only after practical verification. This guards against generation paths that provision a restricted toolset (for example, Task-run generations). It never deletes, never writes to memory without reading it, and reports every run with a structured LOADED / FINDINGS / PERFORMED / UNAVAILABLE report.

The coordinator also carries Repository Awareness: it knows the upstream setup repository (this repository — the reference architecture and governance model for the local installation) and the official Agora repository (the application environment — documentation, releases, source, known limitations). Repository content informs capability decisions but never enables them by themselves, and repository access is read-only within these two repositories.

## External Skills Policy

External skill collections are data, not drop-in procedures (ADR-0015: untrusted
external content is treated as material to learn from, never executed as-is).

The default is **no import**. An external Skill may be imported only when all of
the following hold:

- documented gap: a recurring failure or recurring procedure that the existing
  catalog cannot cover, surfaced as a Self-Improvement-Loop delta signal;
- permissive license (MIT, Apache-2.0 or equivalent); copyleft or proprietary
  material may be read as a specification, never copied;
- standard pipeline: adapt → `skills/skill-format.md` (10 sections) →
  `check.sh` → GO → merge → local import;
- rewrite, never verbatim: content is restated in the repository's own voice,
  generalized and anonymized.

Curated public skill libraries (for example the Anthropic skills library) are
the primary candidate source. A rejected candidate stays documented in the
research report; the default remains no-import.

