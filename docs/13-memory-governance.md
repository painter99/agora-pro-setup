# Memory Governance

This repository uses a hybrid procedure architecture for Agora memory work. The goal is to keep reusable instructions in Skills while keeping personal and project information in Active Memory or Saved Memory.

## Layer model

```text
System template
  = permanent authority, safety, routing, and tool-use rules
Active Memory
  = compact current context injected into every request
Saved Memory
  = durable personal/project information and long-form references
Conversation recall
  = prior discussion and transient context
Skills
  = reusable procedures, frameworks, decision rules, and checklists
```

A Skill does not become authoritative merely because it was loaded. The System template, current user request, application permissions, and approval policy remain higher authority.

## Hybrid Skill family

Import these Markdown files individually into Agora's native Skills. Agora exposes a flat namespace; the repository folders are only for human organization.

| Skill | Role |
|---|---|
| `memory-master-index.md` | Entry router; selects the correct layer and specialized procedure. |
| `active-memory-design.md` | Decides what belongs in Active Memory and controls size/duplication. |
| `active-memory-authority.md` | Controls authorization, patch versus replace, recovery, and verification for AM. |
| `memory-file-operations.md` | Handles precise Saved Memory creation, patching, rename/archive, and deletion gates. |
| `memory-tool-reference.md` | Separates Memory, Skill, and conversation tools; live tool output wins. |
| `memory-audits.md` | Audits stale data, contradictions, references, duplication, bloat, and failure modes. |
| `tool-execution-contract.md` | Shared inspection, approval, retry, and verification contract for all tool domains. |

## Routing examples

- **Where should a durable fact go?** Read `memory-master-index`, then `active-memory-design` if placement is unclear.
- **Patch a Saved Memory file:** Read `memory-file-operations`; add `memory-tool-reference` only if tool arguments are uncertain.
- **Change Active Memory:** Read `active-memory-design` and `active-memory-authority`.
- **Audit the memory layer:** Read `memory-audits`, plus the relevant placement/operation Skill for approved corrections.
- **Use a tool:** Read `tool-execution-contract` and the domain-specific Skill before acting.

## Non-negotiable invariants

1. Inspect current state before editing.
2. Use the smallest valid operation; prefer a unique patch over full replacement.
3. A patch target must match exactly once. On zero or multiple matches, re-read and recover; never guess.
4. Deletion, rename, full replacement, secret access, publication, and other irreversible/high-risk operations require explicit authorization for the exact scope.
5. Re-read and verify every write, plus dependent references.
6. Never claim success from a tool return alone.
7. Do not copy personal facts into reusable public Skills.
8. Do not silently resolve contradictions; surface them and preserve uncertainty.

## Why the hybrid design

The earlier memory-management material provided valuable operational detail: unique patch recovery, explicit AM authority, replacement/recovery gates, reference audits, and failure-mode handling. The current design keeps those controls but distributes them across focused Skills instead of storing a monolithic framework as personal Saved Memory. This improves progressive disclosure, reduces recurring context cost, and keeps procedures separate from information.

## Installation checklist

- Import the seven relevant files into Agora Skills, preserving each exact filename and catalog description.
- Ensure `{active_memory}` and `{skill_catalog}` are present in the System template.
- Keep personal facts in Active Memory/Saved Memory, not in the repository's generic Skills.
- Test harmless scenarios: read, unique patch, failed/non-unique patch, AM authorization, audit report, and a blocked delete.
- Review the actual tool output and enabled permissions; this documentation never outranks live application behavior.
