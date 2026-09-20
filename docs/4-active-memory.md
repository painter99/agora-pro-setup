# Active Memory

Active Memory is compact context intended to remain available across conversations. Because it can be projected into every request, every line should justify its recurring cost.

## Good content

- current status;
- durable communication preferences;
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

The current user request takes precedence over stale Active Memory, but it does not bypass application permissions or safety requirements.

## Size policy

Narrative sections stay near 350 tokens. The Archive Index may grow with the
Saved Memory library — roughly 500–1000 tokens for the whole of Active Memory is
acceptable when the growth is index lines only (one line per topic group, each
with a `Load when` trigger). Index growth is the mechanism that lets a model
orient itself across many Saved Memories without reading them. File bodies,
histories, procedures, and session logs are never valid index content; if the
index no longer fits under the deployment ceiling, split it by domain and keep
only routing anchors.

---

| Layer | Contains | Typical access |
|---|---|---|
| Active Memory | compact current context and preferences | `{active_memory}` |
| Saved Memory | durable facts, decisions, histories, references | Memory tools |
| Skill | reusable instructions and workflows | `{skill_catalog}` and Skill tools |
| Conversation recall | prior discussion and transient context | conversation tools |

## Decision rule

Store information as Saved Memory when the assistant needs to know it. Store a procedure as a Skill when the assistant needs to follow it repeatedly.

A personal preference may belong in Memory. A general research method belongs in a Skill. A project specification is information and belongs in Memory or a reference file, while the project-planning method belongs in a Skill.

Do not duplicate the same content across layers without a clear reason.

## Hybrid memory-governance Skills

The repository's memory procedures are split into focused Skills under `skills/memory-governance/`:

- `memory-master-index.md` — routing and authority boundaries;
- `active-memory-design.md` — placement, quotas, and anti-patterns;
- `active-memory-authority.md` — authorization, patching, recovery, and verification;
- `memory-file-operations.md` — precise Saved Memory CRUD and patch recovery;
- `memory-audits.md` — audits, contradictions, references, and failure modes.

`tool-execution-contract.md` is the shared cross-domain safety layer. These are procedures, not personal facts. Import the files individually into Agora's flat Skill namespace; the repository subdirectory is organizational only.
