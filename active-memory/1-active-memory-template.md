# Active Memory Template (The Workbench)

**The most common mistake:** forcing the agent to tool-read a "profile file" at the start of every chat. That wastes time, battery, and tokens.

**Active Memory** is injected into the System template through `{active_memory}`. Use it for the compact master profile and an **Archive Index of Saved Memories** — not for Skill bodies.

Skills are discovered by Agora's native `{skill_catalog}`. Do **not** duplicate every Skill into Active Memory. You may keep one short reminder that Skills exist.

Copy the block below into Agora Active Memory and customize it.

```markdown
> **Status (YYYY-MM-DD):** [What you are focusing on right now.]

### Who I Am
- Name, location
- Important public links if needed (GitHub, etc.)

### Communication Preferences
- What I WANT: short answers, verified facts, A/B/C options when choosing.
- What I DO NOT WANT: long intros, unsolicited lectures, walls of text, invented certainty.
- Meta: mobile-first — keep it readable on a small screen.

### Current Focus
- Active projects (anchors only — details live in Saved Memories)
- Current constraints

### Archive Index (Saved Memories)
*If the conversation matches a trigger, use Memory tools to read that file. Each entry needs a concrete **Load when:** line.*
- `resume.md` — professional history. **Load when:** CV, jobs, or career-application context.
- `project_notes.md` — project facts and decisions. **Load when:** that named project is discussed in substance.

### Runtime Notes
- Discover reusable procedures through the native Skill Catalog, not this index.
- Read a Skill with `read_skill_file` only when the catalog description matches the task.
- Current user instructions override stale Active Memory.
- Do not store every session detail here.
```

### Companion resources

- [`2-active-memory-example.md`](2-active-memory-example.md) — filled-in fictional example
- [`../skills/memory-management/00-master-index.md`](../skills/memory-management/00-master-index.md) — memory governance Skills
- [`../docs/4-memory-and-skills.md`](../docs/4-memory-and-skills.md) — Memory vs Skills
