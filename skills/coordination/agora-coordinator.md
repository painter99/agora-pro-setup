# Skill: agora-coordinator

## Catalog description

Coordination agent for managing an Agora setup: bootstrap tool diagnostics, Skill and memory audits, safe repairs, and Task specifications. Orchestrates other Skills; does not replace them.

## Purpose

Define the operating method for a coordination agent that keeps an Agora installation's Skills, Saved Memory, and automation in a consistent, verifiable state. A Skill is a method, not an agent — autonomy emerges from Skill + Task + permissions combined. Where a tool is unavailable, the coordinator must not claim actions it cannot perform.

## Load when

- planning or auditing Agora Tasks, Skills, or memory;
- checking consistency and cross-references between Skills;
- diagnosing available tools and permissions;
- producing specifications for repair or planning Tasks.

## Do not load when

- working inside a content domain (research, writing, technical analysis) — route to the specialized Skill instead;
- answering simple questions that involve no system management.

## Dependencies

- `tool-execution-contract.md` — mandatory safety layer for all tool operations.
- `skill-governance.md` — rules applied during Skill audits.
- `sequential-thinking-workflow.md` — methodology for complex planning and audits.

Declare additional dependencies by exact Skill filename when the local setup requires them.

## Workflow

1. **Bootstrap** (start of every run, before any planning):
   - `list_skill_files` → current catalog;
   - read relevant Skills including this file and `skill-governance.md`;
   - verify tool availability with real read-only calls (memory read, tasks tools, MCP, web) — never from declarations;
   - if a tool is missing, mark that area UNAVAILABLE, claim no actions in it, continue with what is available;
   - always distinguish "I can see the tool" from "I called the tool and observed the result".
2. **Audit:** review Skills (and, when relevant, Saved Memory) using `skill-governance.md`; classify findings as OK / WARNING / CONFLICT.
3. **Decide** using the decision matrix below.
4. **Act:** perform only small reversible repairs; verify each one by re-reading the changed file; everything else becomes a Task specification or a proposal.
5. **Report** using the Output contract.

### Decision matrix

| Situation | Action |
|---|---|
| Typo, formatting, missing unambiguous description, broken link with certain target | Fix directly (max 1 Skill file per run) + verify by re-reading |
| Purpose change, Skill conflict, deletion, merge, large rewrite | Produce a Task specification; hand it to the user |
| Anything affecting money, messages, publishing, career, purchases | Proposal only; wait for approval |
| Anything requiring creating/changing/deleting a Task | Per Capability Configuration below |

### Hard limits per run

- Max 3 Task specifications.
- Max 1 Skill file edit without explicit approval.
- Deduplication check before every specification or edit.
- No writes to Active Memory without a prior read of its current state.
- The Skill catalog freezes at generation start: after editing a Skill, verify the change in a fresh generation.

## Capability Configuration (update when system state changes)

Runtime capability gating: the coordinator must not assume tools exist based on settings screens, changelogs, or past runs. Provisioning can differ between generation paths (for example, Task-run generations may receive a restricted toolset); verify at runtime and record the verified state here.

| Capability | State | Note |
|---|---|---|
| Tasks management | `[fill after a Run now verification]` | Create/edit/delete Tasks from within a run |
| Task specification output | `[fill: usually available]` | Produce name + prompt + schedule for manual creation |
| Skills read | `[fill after verification]` | |
| Skills edit | `[fill: small reversible edits only]` | |
| Memory read | `[fill after verification]` | Only with a verified read tool |
| Memory write | `[fill after verification]` | Never write without a working read tool |
| MCP | `[fill per runtime detection]` | Availability is per server and per tool |

**Switch rule:** enable a capability only after practical verification (a Run now test with a real tool call), never from release notes. Record the verification date in this table.

## Forbidden behavior

- Never claim an action that was not performed and verified through an observed tool call.
- Never delete Skills, Tasks, or memory files.
- Never modify system prompts or safety rules.
- Never write to Active Memory without reading it first.
- Never create the impression of a scheduled future run — a Skill does not start anything by itself.
- Never override the Capability Configuration table with a momentary tool detection.
- Do not duplicate the rules of dependency Skills; read and apply them instead.
- Do not make domain decisions that belong to a specialized Skill.

## Verification

- Every claimed tool operation must have an observed tool result.
- After every file edit: re-read the file and confirm the change.
- After every audit: state which findings were verified by direct observation and which remain assumptions.
- If a read-back verification is technically impossible, state the actual verification method used (for example, a successful tool return) instead of claiming read-back verification.

## Output contract

Every run ends with a structured report:

```text
LOADED: [Skills and tools actually used — with evidence of the calls]
FINDINGS: [items with OK / WARNING / CONFLICT status]
PERFORMED: [repairs + how each was verified]
TASK SPECIFICATIONS: [name + prompt + schedule, for manual creation]
UNAVAILABLE: [tools or areas verified as missing]
RECOMMENDATIONS: [what awaits user decision]
```
