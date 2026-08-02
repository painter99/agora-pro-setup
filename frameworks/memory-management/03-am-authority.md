# Active Memory — Authority Model, Hard Rules, Recovery & Confirmation

> **Companion to:** `00-master-index.md` and `02-am-anatomy.md`
> **Scope:** Who can change AM, decision flow, hard rules, recovery, confirmation. Content rules (what belongs) → `02-am-anatomy.md`.

The cardinal problem this file prevents: **agent drift** — the agent
makes AM changes that were never authorized, fragmenting identity
and preferences over time. Authority must be explicit.

---

## 1. Three Roles, Three Scopes

| Role | May change | Must not change |
|---|---|---|
| **User explicit** | Anything in AM (full authority) | — |
| **Agent proactive** | Archive Index only: add entry on `create_memory_file`, remove entry on `delete_memory_file`, refresh `Status` date when conversation context makes it stale | Identity, preferences, life focus, hobby anchor, communication style, AI model choices, dormant background |
| **Agent passive** | Date refresh in `> Status (YYYY-MM-DD):`, fix obvious typo if `old_string` is unambiguous, add missing `**Load when:**` trigger to existing Archive Index entry | Substantive content, identity claims, preferences, anchors |

---

## 2. Decision Flow Before Any AM Patch

```
1. Is the change user-explicit?
   YES → proceed (any scope)
   NO ↓
2. Is the change to Archive Index (add/remove entry) or Status date?
   YES → proceed (agent proactive)
   NO ↓
3. Is the change a date refresh, typo fix, or missing trigger?
   YES → proceed (agent passive)
   NO ↓
4. STOP. Propose the change to user; await approval.
```

---

## 3. Hard Rules (Override Any Agent Inclination)

1. **AM is sacred.** Identity, communication preferences, life focus, and hobby anchors are **user-only**. Agent must propose, never act.
2. **Archive Index is shared.** Entries appear automatically when files are created/deleted. No manual scrubbing.
3. **`Status` blockquote is dated.** Format `> **Status (YYYY-MM-DD):**` is required. Agent may refresh the date when conversation context makes status stale (e.g., user says "I just started learning Python" — update Status from "researching audio gear" to "learning Python" with today's date).
4. **No full replace without template.** `mode="replace"` is permitted **only** when the agent has a verified template in hand (e.g., from `1-active-memory-template.md`) and the AM is demonstrably corrupted beyond patch recovery.
5. **Conflicts defer to user message.** Per Agora `DefaultSystemPrompt.kt`: *"If [active memory] conflicts with the current user message, the current user message wins."* When in doubt, do not patch — ask.
6. **Permission required.** Before any `update_active_memory` call, verify `Access Active Memory` is ON in `Settings → Memory`. Otherwise the call fails; propose enabling the permission rather than retrying.
7. **Patch uniqueness.** `update_active_memory` with `mode="patch"` fails when `old_string` matches 0 or >1 times. Always read AM first to confirm the target string is unique.

---

## 4. Recovery Protocol (When AM Is Broken)

If AM appears corrupt, fragmented, or has grown beyond 1500 tokens:

1. **Read** current AM in full (the system injects it as `<active_memory_context>`; surface it for analysis).
2. **Compare** with `1-active-memory-template.md` and `3-quality-am-example.md` (Saved Memories). Identify drifted sections, orphaned content, anti-pattern violations.
3. **Categorize** drift:
   - Zombie markers, typos, date drift → patch
   - Duplicated facts (doubletalk) → delete from AM, ensure Saved Memory file has them
   - Bloated sections → split into Saved Memory file, replace with anchor
   - Identity drift → patch back to user-stated facts; flag for user confirmation
4. **Propose** recovery plan with diff summary (no silent rebuild).
5. **Wait** for user approval.
6. **Execute** with `mode="replace"` ONLY after explicit user GO. New content sourced from template + user-confirmed facts.
7. **Verify** post-rebuild: total token count, hierarchy integrity, no orphaned sections.

**Recovery is the one case where `mode="replace"` is appropriate.**

### 4.1 Patch-Failure Sub-Recovery

When a `mode="patch"` call fails because `old_string` matches >1 times:

1. **Read** AM to find the duplicates
2. **Patch** out the unintended duplicate first (with more context in `old_string`)
3. **Retry** the original patch
4. **If duplicates are intentional** (e.g., list of choices) → use a longer `old_string` with surrounding context to make it unique

---

## 5. Confirmation Protocol (Agora-specific)

Agora's `SettingsMemoryPage.kt` requires user confirmation for
destructive operations via UI dialog. The chat-side equivalent is
the agent's responsibility:

| Operation | Confirmation needed? | Confirmation type |
|---|---|---|
| `read_memory_file` | No | n/a |
| `list_memory_files` | No | n/a |
| `create_memory_file` | No (low risk) | Standard proposal |
| `edit_memory_file` (patch) | No (reversible) | Standard proposal |
| `edit_memory_file` (full content) | **Yes** | Explicit user GO |
| `edit_memory_file` (rename) | **Yes** | Explicit user GO |
| `delete_memory_file` | **Yes (always)** | Explicit user GO + confirmation in conversation |
| `update_active_memory` (patch/append) | No (reversible) | Standard proposal |
| `update_active_memory` (replace) | **Yes (always)** | Explicit user GO + diff summary |
| Any AM change to identity / preferences / life focus | **Yes (always)** | Explicit user GO, even for "small" changes |

**"Standard proposal"** = include the operation in your next-response
plan and proceed if the user does not object within the same turn.
**"Explicit user GO"** = wait for the user to confirm before calling
the tool.

### 5.1 Sensitive Data

Before saving sensitive personal data (PII, financial, legal, medical):
- **Ask** the user explicitly
- **Confirm** the scope of what should be saved
- **Never** infer sensitive data from conversation and save silently

This is consistent with Agora's `DefaultSystemPrompt.kt`:
*"Ask before saving sensitive personal data, long-term preferences,
or deleting/replacing existing memory."*

---

## 6. Standing Instructions vs AM

Per Agora User Manual, AM is suitable for **"standing instructions
that apply to all conversations"** — e.g., "always respond in Czech",
"prefer A/B/C options", "verify facts with sources". These ARE AM
content (Communication Preferences section), not System Prompt
content, because they are user-level and may change over time.

**Rule of thumb:** if the instruction is **user-specific and may
change** (preferences, current focus) → AM. If the instruction is
**about the agent's reasoning process** (tool mandates, reasoning
rules, anti-hallucination) → System Prompt.
