# Agent Frameworks

This directory contains **agent skills** — structured prompts that
the AI agent loads on demand via `file_read` to perform a specific
class of tasks. They are stored in Agora's **Saved Memories** and
referenced from the **Archive Index** in Active Memory.

---

## 📲 Installation Guide

Each skill in this directory goes into Agora's **Saved Memories**.
Agora stores files **without** the `.md` extension and prepends it
automatically when the agent reads them back. Steps:

### Step A — Save the file in Agora

1. **Open the menu** — tap the **≡** icon in the top-left corner
   of the main chat screen
2. Tap **Settings** — the gear-icon row at the bottom of the menu
3. Scroll down to the **Memory & Data** section and tap **Memory**
4. In the Memory screen, scroll down to the **Saved Memories**
   section
5. Tap the **`+`** button at the bottom
6. In the new-file dialog:
   - **Name field**: type the filename *without* `.md`
     (e.g. `deep-research-framework`, **not**
     `deep-research-framework.md`)
   - **Content field**: paste the full text of the skill file
     from GitHub
7. Tap **Save**

### Step B — Register the skill in Active Memory

1. Back in the Memory screen, scroll up to the **Active Memory**
   card and tap it to edit
2. In your **Archive Index**, add the entry shown at the top of
   each skill file in this directory
3. Tap **Save**

The agent will now `file_read` the skill automatically whenever a
matching trigger keyword comes up in conversation.

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
