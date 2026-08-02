# Active Memory Template (The Workbench)

**The most common mistake I see:** Users force their AI agent to use a tool to read a "profile file" every time a new chat starts. This wastes time, battery, and API tokens. 

**Active memory** is injected directly into the system prompt automatically by Agora. I use it to hold my "Master Profile" (who I am, how to talk to me) and my crucial **Archive Index**.

### My Ideal Active Memory Template
Copy this into your Active Memory field in Agora and customize it for yourself:

```markdown
## User Profile for Agora

> **Current Status (Date):** Write what you are currently focusing on (e.g., Traveling, learning Python, researching audio gear).

### Who I Am
- Name, Age, Location
- Contact / Important Links (GitHub, LinkedIn)

### Communication Preferences
- What I WANT: Short answers, bullet points, A/B/C options, verified facts.
- What I DO NOT WANT: Long intros ("I understand"), unsolicited advice, walls of text, hallucinations.
- Meta: Mobile priority (keep it concise, I'm reading this on a small screen).

### Archive Index (Saved Memories)
*Agent instruction: If the conversation touches on these topics, use the `read_memory_file` tool to retrieve these specific files. Each entry has a `**Load when:**` trigger — only load when conversation matches.*
- `resume_2026.md` – My complete professional history and CV. **Load when:** user asks about CV, jobs, or career-application context.
- `it_projects.md` – Overview of my tech stack, servers, and repositories. **Load when:** user asks about servers, repositories, deployment, or infrastructure.
- `hobby_audio.md` – My current audiophile setup, DACs, and EQ preferences. **Load when:** user asks about audio gear, EQ, headphones, DAC, or audiophile workflow.
- `memory-management-framework.md` – Governance for memory operations (write/update/delete, AM patches, audit cycles). **Load when:** user asks to create, update, or delete a memory file, patch Active Memory, audit memory, or when AM and a file disagree.
```

---

### Companion Resources

- **[3-quality-am-example.md](3-quality-am-example.md)** — a fully
  filled-in, anonymized example of a high-quality Active Memory.
  Use it as a reference for *how much detail* and *how to organize*
  each section.
- **[memory-management-framework.md](../frameworks/memory-management-framework.md)** —
  governance rules for when to create, update, or delete memory
  files, and how to patch Active Memory safely.
```
