# File-Based Active Memory

Current-status context lives in a **working state file** on a persistent host
that the agent reaches with file tools — **file-based active memory**
(short: file-based AM; ADR-0017, 2026-10-31). The maintained instance runs it
instead of Agora's injected Active Memory, which remains an upstream
application feature (its behavior and troubleshooting: `docs/11-troubleshooting.md`).

Why: injected Active Memory could not be verified after a write (no read-back
tool in the deployed generation), its store/view desync made patch anchors
unmatchable, and it charged token cost in every message. A host file makes
every write observable and gives chat and scheduled-task agents one storage
model.

## Good content

- current status;
- durable communication preferences and standing rules;
- active priorities;
- short project anchors;
- concise memory boundaries;
- an **Archive Index** of Saved Memory routing anchors, each with a `Load when` trigger.

## Poor content

- full Skill bodies;
- long histories;
- copied web results;
- session logs;
- complete tool manuals;
- stale or speculative facts;
- unrelated personal history.

Use Saved Memories for durable information and Skills for reusable procedures. Use conversation search for prior context that should not become permanent.

The current user request takes precedence over stale state-file content, but it does not bypass application permissions or safety requirements.

## Read/write contract

- Read before relying on the content; never reconstruct it from memory of earlier sessions.
- Patch with a unique anchor; full replacement only with explicit approval, a verified source, and a fresh backup copy first.
- **Read the file back after every write** — a write without read-back evidence is not verified.
- Keep narrative sections near 350 tokens; the Archive Index may grow with the Saved Memory library (roughly 500–1000 tokens total, index lines only); hard ceiling about 1500 tokens.
- Identity, preferences, and boundaries change only with explicit confirmation of the exact scope (`file-based-active-memory` Skill).

Procedure: `skills/memory-governance/file-based-active-memory/SKILL.md`. The instance path is instance-specific (`docs/30`) and never stored in this repository.

## Layer table

| Layer | Contains | Typical access |
|---|---|---|
| File-based active memory | compact current context and standing rules | file tools (working state file) |
| Saved Memory | durable facts, decisions, histories, references | Memory tools |
| Skill | reusable instructions and workflows | `{skill_catalog}` and Skill tools |
| Conversation recall | prior discussion and transient context | conversation tools |

## Decision rule

Store information as Saved Memory when the assistant needs to know it. Store a procedure as a Skill when the assistant needs to follow it repeatedly. Keep current status in the working state file when it should orient the next session; do not store it at all when it is transient.

A personal preference may belong in memory. A general research method belongs in a Skill. A project specification is information and belongs in Memory or a reference file, while the project-planning method belongs in a Skill.

Do not duplicate the same content across layers without a clear reason.

## Memory-governance Skills

The repository's memory procedures live under `skills/memory-governance/`:

- `memory-master-index` — routing and authority boundaries;
- `file-based-active-memory` — working-state placement, size, and R/W discipline;
- `memory-file-operations` — precise Saved Memory CRUD and patch recovery;
- `memory-audits` — audits, contradictions, references, and failure modes.

`tool-execution-contract` is the shared cross-domain safety layer. These are procedures, not personal facts. Import the files individually into Agora's flat Skill namespace; the repository subdirectory is organizational only.

## Revert trigger

If a future Agora release makes injected Active Memory verifiable (a read-back tool plus per-run freeze), the instance may re-evaluate; migration back is a single copy of the state file into Active Memory.