# Active Memory — Anatomy, Content Rules & System Prompt Integration

> **Companion to:** `00-master-index.md` and `03-am-authority.md`
> **Scope:** What belongs in Active Memory, how much, in what order. Authority rules (who can change) → `03-am-authority.md`.

Active Memory is the highest-cost tier (paid every turn in tokens).
Every line must earn its place. This file codifies the rules that
keep AM healthy and prevent drift.

---

## 1. Anatomy — Required and Optional Sections

| Section | Purpose | Target lines | Owner |
|---|---|---|---|
| `> **Status (YYYY-MM-DD):**` | One-liner: current focus right now | 1 | Shared (passive date refresh OK) |
| `### Who I Am` | Name, age, location, contact | 3–5 | User only |
| `### Life Focus` | Priority, job, primary hobby anchor | 3–5 | User only |
| `### Communication Preferences` | Want / don't want / meta | 3–5 | User only |
| `### Archive Index (Saved Memories)` | 1 line per file with `**Load when:**` trigger | 1 per file | Shared (auto on create/delete) |
| `### Active Hobbies` *(optional)* | Anchor only; full detail in Saved Memory | 2–3 | User only |
| `### AI Models in Use` *(optional)* | Primary / Alternative / Avoid | 3–5 | User only |
| `### Dormant Background` *(optional)* | Past jobs, education; read-only on request | 3–5 | User only |

**Order matters.** Status blockquote on top (immediate read),
identity/communication anchors next (load-bearing context),
Archive Index last (look-up structure).

Agora stores AM as **plain text in `active_memory.md`** (Agora
`MemoryManager.kt`). The Settings UI shows a single multi-line text
field — no per-section structure. This means:

- AM must be **readable as Markdown** by both human and model
- Section headers must be **conventional** (`### Who I Am`) so the
  agent can reason about structure
- No exotic formatting (no tables inside AM unless necessary)

---

## 2. Quotas (Verified Against Agora Performance Cliff)

- **Total AM target:** ~350 tokens (matches `3-quality-am-example.md` compact pattern)
- **Total AM hard limit:** 1500 tokens (beyond this, recall and quality degrade — observed in mobile agent apps)
- **Per-patch budget:** ≤ 50 tokens, **unless structural fix** (rebuild from template, recovery from corruption)
- **Patches per session:** ≤ 1, **unless user explicitly requests multiple** in one message
- **Archive Index entries:** strictly 1 per file, must include `**Load when:**` trigger

---

## 3. Static vs Dynamic Rule (The Cardinal Allocation Rule)

| Tier | What goes there | Why |
|---|---|---|
| **Active Memory** | **Dynamic** facts: current status, active preferences, life focus, hobby anchors, communication style | "What I am doing right now" |
| **Saved Memories** | **Static** facts: CV, past jobs, completed courses, gear lists, static specs, project histories | "What I have done" |
| **Conversation Recall** | **Ephemeral** facts: what was discussed today, single-session decisions, work-in-progress notes | "What we talked about" |

If a fact could go in two tiers, **prefer the cheaper tier**.
Cost: Core > Archival (when loaded) > Recall (free).

---

## 4. Content Anti-Patterns (Do NOT Put These in AM)

| Anti-pattern | Example | Fix |
|---|---|---|
| **Session log** | "User mentioned X today at 14:30" | Push to Recall, not AM |
| **Spec dumps** | Tool definitions, framework rules copied into AM | Reference via Archive Index |
| **Status fragmentation** | 5 different `## Current` sections | Consolidate to 1 `> Status` blockquote |
| **Identity drift** | New sections added without `Who I Am` / `Life Focus` anchor | Add under existing anchor, don't create parallel section |
| **Archive Index bloat** | Entry without `**Load when:**` trigger | Patch trigger BEFORE adding new file |
| **Work-in-progress notes** | "TODO: discuss X tomorrow" | Saved Memory or session context |
| **Tool output dumps** | Copy-paste from `web_search` results into AM | AM has only what user decided to keep |
| **Doubletalk** | Same fact in both AM and a Saved Memory file | One source of truth — keep in file, reference only in AM |

---

## 5. AM ↔ System Prompt Integration (Agora-specific)

Active Memory is **injected into the system prompt** automatically
by Agora as the `<active_memory_context>` block. The AM is **not a
System Prompt** — it is a separate entity that gets injected alongside
the System Prompt at compile time.

**What this means architecturally:**

| Concern | System Prompt | Active Memory |
|---|---|---|
| **Who manages it** | User (template + block builder) | User + Agent (with permissions) |
| **When compiled** | Per-prompt compile | Per-prompt compile |
| **Variable substitution** | Yes (`{time}`, `{active_memory}`, `{sent_date}`) | No — AM is plain text, no variables |
| **Where it lives** | Agora System Prompt blocks | `active_memory.md` |
| **Token cost** | Fixed per-block | Per-token of AM content |
| **Tool access** | n/a | `update_active_memory` (if permission granted) |

**Practical implication:** if you want a **dynamic date in the
Status blockquote**, do **not** put it in AM. Instead, use the
`{sent_date}` or `{date}` variable in the System Prompt itself.

### 5.1 Variable Substitution (Keep in System Prompt)

| Variable | Expands to | Where to use |
|---|---|---|
| `{time}` | Current time (HH:mm:ss) | System Prompt (time-aware reasoning) |
| `{date}` | Current date (YYYY-MM-DD) | System Prompt (date-aware reasoning) |
| `{sent_date}` | Message sent date (YYYY-MM-DD) | Per-message context |
| `{sent_time}` | Message sent time (HH:mm) | Per-message context |
| `{active_memory}` | **Content of Active Memory** | System Prompt (rarely needed — AM is auto-injected) |
| `{model_id}` | Currently selected model ID | System Prompt (model-aware commands) |

**Do NOT try to use variables in AM.** AM is plain text and is
injected raw. If you need date awareness in AM, use the Status
block with a fixed date and refresh it via `update_active_memory`
when the context changes (see `03-am-authority.md` § Status refresh).

### 5.2 AM May Be Incomplete or Stale

Per Agora's `DefaultSystemPrompt.kt`:

> *"It may be incomplete or stale. If it conflicts with the current
> user message, the current user message wins. If it is empty, treat
> it as unavailable."*

This is **a feature, not a bug**. AM is a working memory, not a
database. It should be updated when genuinely needed, not on every
interaction. The user-message-wins rule means the agent should
**always trust the current message over outdated AM content**.
