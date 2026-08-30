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

### Autonomous Framework Gates (hard rules for the agent)

*These gates are NON-NEGOTIABLE. The agent executes them BEFORE the
matching action, without waiting for the user to ask. They are checked
against the INTENT of the task, not the user's literal wording.*

- **Memory Gate:** BEFORE any memory tool call (`create_memory_file`, `edit_memory_file`, `delete_memory_file`, `update_active_memory`) → FIRST `read_memory_file` on `00-master-index.md` and follow its Decision Guide. No exceptions. After the operation, verify: file exists/deleted + Archive Index consistent.
- **Research Gate:** BEFORE any task requiring 2+ web sources (verify, compare, find data, prices, facts — even if the user just says "find X" or "check Y") → FIRST `read_memory_file` on `deep-research-framework.md` and follow its 3-phase workflow.
- **End-of-task check:** if either gate applied, state in one line whether the framework was loaded and followed.

### Archive Index (Saved Memories)
*Agent instruction: If the conversation touches on these topics, use the `read_memory_file` tool to retrieve these specific files. Each entry has a `**Load when:**` trigger — only load when conversation matches.*
- `resume_2026.md` – My complete professional history and CV. **Load when:** user asks about CV, jobs, or career-application context.
- `it_projects.md` – Overview of my tech stack, servers, and repositories. **Load when:** user asks about servers, repositories, deployment, or infrastructure.
- `hobby_audio.md` – My current audiophile setup, DACs, and EQ preferences. **Load when:** user asks about audio gear, EQ, headphones, DAC, or audiophile workflow.
- `memory-management/00-master-index.md` – Master index for memory governance (modular split). **Load when:** creating, updating, or deleting a memory file, patching Active Memory, auditing memory, or when AM and a Saved Memory disagree. For sub-topics, follow the Decision Guide to load the right specialized file (01–05).
```

---

### Companion Resources

- **[3-quality-am-example.md](3-quality-am-example.md)** — a fully
  filled-in, anonymized example of a high-quality Active Memory.
  Use it as a reference for *how much detail* and *how to organize*
  each section.
- **[memory-management-framework.md (modular split)](memory-management/)** — comprehensive governance for Active Memory + Saved Memories. Six specialized files: a master index plus dedicated files for file operations, AM anatomy, AM authority, tool reference card, and audit/failure modes. Start with `00-master-index.md` (Decision Guide), then load only the file relevant to the current operation — saves ~50% tokens vs. loading one big file.
```
