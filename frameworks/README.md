# Agent Frameworks

This directory contains **agent skills** — structured prompts that
the AI agent loads on demand via `file_read` to perform a specific
class of tasks. They are stored in Agora's **Saved Memories** and
referenced from the **Archive Index** in Active Memory.

---

## 📲 Installation Guide

For each skill in this directory:

1. **Open Agora** → top-right menu → **Saved Memories**
2. Tap the **`+`** button → **Add File**
3. **Copy the entire content** of the skill file from GitHub
4. **Name it in Agora exactly as the filename** (e.g.
   `deep-research-framework.md`)
5. **Open Agora** → top-right menu → **Active Memory**
6. In your **Archive Index**, add the entry shown in the skill's
   `INSTALLATION` header (each skill file includes the exact line
   to paste)
7. **Save**. The agent will now `file_read` the skill automatically
   when a matching topic comes up in conversation.

**Tip:** the trigger keywords in the Archive Index entry are what
the agent uses to decide *when* to load the skill. Be specific —
"load on every conversation" defeats the purpose.

---

## How Agent Skills Work

A skill is a *progressive disclosure* mechanism: it lives in long-term
storage, costs zero tokens until needed, and is loaded by the agent
only when the conversation topic matches the trigger.

In practice:

1. Save the file in Agora's Saved Memories (e.g. as
   `deep-research-framework.md`).
2. Add a single line to your Active Memory's Archive Index, like:

   ```text
   - `deep-research-framework.md` – Multi-source web research
     workflow. **Load when:** user asks for a deep dive, market
     analysis, model comparison, or fact-check needing 2+ sources.
   ```

3. The agent sees the trigger keyword (e.g. "deep dive"), runs
   `file_read` on the file, and applies the framework for the rest
   of the conversation.

## Design Principles

- **One skill = one class of task.** Don't try to make a "do
  everything" prompt.
- **Triggers, not summaries.** Archive Index entries should say
  *when* to load the skill, not *what* the skill contains.
- **Token budget.** Keep the skill body compact. Empirical research
  shows a performance cliff around 1500 tokens for system-level
  prompts in mobile agent apps.
- **Reusable.** A well-designed skill works for any user, not just
  the one who wrote it.

## Available Skills

| File | Purpose | Trigger keywords |
|---|---|---|
| `deep-research-framework.md` | Multi-source web research with source evaluation, quality gates, and synthesis | deep dive, research, market analysis, model comparison, fact-check 2+ sources |
| `memory-governance-framework.md` | Governance for memory operations (write/update/delete/AM patches, audit cycles) | memory operations, create file, update file, delete file, AM patch, memory audit, AM vs file disagreement |

## When to Add a New Skill

Create a new skill when:

- You keep using the same multi-step workflow across 3+ sessions
- The workflow has decision points the agent should make autonomously
- The workflow benefits from explicit anti-patterns and quality gates
- The workflow is too long to keep re-typing in every conversation

Do NOT create a skill when:

- The workflow fits in a one-line system-prompt addition
- The workflow is rarely used (<1/month)
- The workflow is highly personal and would not generalize
