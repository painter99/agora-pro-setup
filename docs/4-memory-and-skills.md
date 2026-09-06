# Memory versus Skills

## Decision rule

- If the assistant must **know** it → Saved Memory or Active Memory.
- If the assistant must **follow** it repeatedly → Skill.

| Example | Layer |
|---|---|
| "Respond in Czech" | Active Memory (preference) |
| CV / project spec / gear list | Saved Memory |
| How to run deep research | Skill `deep-research` |
| How to patch Active Memory | Skill `03-am-authority` |
| What we decided yesterday in chat | Conversation recall |

## Discovery

| What | Discovery | Load tool |
|---|---|---|
| Skills | `{skill_catalog}` (name + description) | `read_skill_file` |
| Saved Memories | Archive Index in Active Memory | `read_memory_file` |
| Active Memory | `{active_memory}` | already injected |

Do not keep a second "Module Registry" of Skills inside Active Memory. That duplicates the native catalog and goes stale.

You **may** keep a one-line reminder:

```text
Use the Skill Catalog for procedures. Read only matching Skills.
```

## Why memory governance is still a split Skill pack

The original 00–05 split exists because a single 1300-token memory bible was too expensive for "just rename a file". That reasoning still holds.

What changed in 2.1:

- install 00–05 as **Skills**, not Saved Memories;
- Decision Guide still starts at `00-master-index`;
- Skill tools are a separate family from Memory tools.

The operational rules (patch uniqueness, no silent delete, AM quotas, user-message-wins) are preserved from the original framework, not rewritten from scratch.
