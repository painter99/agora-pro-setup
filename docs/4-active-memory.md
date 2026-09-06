# Active Memory

Active Memory is compact context intended to remain available across conversations. Because it can be projected into every request, every line should justify its recurring cost.

## Good content

- current status;
- durable communication preferences;
- active priorities;
- short project anchors;
- concise memory boundaries.

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
