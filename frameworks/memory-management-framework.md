# Memory Management Framework for Agora

> **Active Memory entry to register this skill:**
> ```
> - `memory-management-framework.md` – Governance for memory
>   operations (write/update/delete/AM patches, audit cycles).
>   **Load when:** creating, updating, or deleting a memory
>   file, patching Active Memory, auditing memory, or when AM
>   and a Saved Memory disagree.
> ```
>
> Installation walkthrough → [`frameworks/README.md`](README.md).

> **Purpose:** Comprehensive governance for Active Memory (Core) and
> Saved Memories (Archival) in Agora. Defines when/how to write,
> update, delete, and patch memory.
> **Architecture basis:** Tiered memory model — Core (in-context AM)
> + Archival (file-based Saved Memories). Recall layer is implicit
> (conversations + search).
> **Scope:** Every memory operation by the AI agent should follow
> this framework autonomously; deviations must be justified.

---

## 1. Architecture Map

| Tier | Agora component | Lifetime | Cost per request | Update mechanism |
|---|---|---|---|---|
| **Core** (in-context) | Active Memory widget | Always injected in every prompt | Paid every turn (~tokens) | `update_active_memory` (patch only) |
| **Recall** | Conversation history (searchable) | Indefinite, search-indexed | Free to query | `search_conversations`, `read_conversation` |
| **Archival** | Saved Memories (file-based) | Indefinite, file-read on demand | Free unless loaded | `list_memory_files`, `create_memory_file`, `read_memory_file`, `edit_memory_file`, `delete_memory_file` |

**Critical asymmetry:** Core memory costs tokens every turn. Archival
is free until loaded. This asymmetry drives most of the rules below.

---

## 2. Write Policy — When to Create a New Saved Memory File

**Create a new file when ANY of these holds:**

| Trigger | Example |
|---|---|
| New persistent domain (>3 future references expected) | "Started a new hobby" → `<topic>_journey.md` |
| Static reference data with no natural AM home | CV, dormant tech stack, project history |
| Long-form structured content (>300 tokens) that would bloat AM | "Document all my Git repos with status" |
| User explicit request | "Save this for later" |
| Recurring conversation pattern in 3+ sessions | Repeatedly discussing the same setup without a file |

**Do NOT create a file when:**

- Topic fits in a single conversation → use Recall layer
- Topic already covered by existing file → update instead
- Topic is ephemeral (<1 week relevance) → AM or none
- Topic would duplicate dormant background → reference instead

**Decision rule:** Before creating, ask: *"Will this be referenced
in >2 distinct sessions, AND is it >200 tokens, AND does it not fit
cleanly in AM?"* If 3/3 yes → create file.

---

## 3. Update Policy — When to Edit an Existing File

**Edit an existing file when:**

| Trigger | Action |
|---|---|
| User provides new factual data about a covered topic | `edit_memory_file` (patch, not full rewrite) |
| Outdated info detected (date, status, config) | Update specific section |
| Contradiction between file and new evidence | Resolve + note change in file footer |
| File grown >3000 tokens (bloat risk) | Split or refactor; signal for review |

**Update protocol:**

1. `read_memory_file` first to confirm exact content
2. `edit_memory_file` with precise `old_string` → `new_string` (no
   full rewrites unless truly massive)
3. Preserve headers, structure, naming
4. Never overwrite without explicit user approval for PII or
   critical data (system prompt Rule 9)

---

## 4. Delete / Archive Policy — Forgetting

**Delete a file when:**

- User explicit request to forget ("Remove X")
- Topic fully obsolete and superseded by a newer file
- Information provably incorrect and irreparable

**Archive (rename with `_archived_` prefix) when:**

- Dormant for >6 months AND likely never referenced again
- Historical snapshot needed for context but not active work

**Never auto-delete.** All deletes require explicit user
confirmation (system prompt Rule 9: destructive ops need approval).

---

## 5. Active Memory Patching Rules

AM is the highest-cost tier. Patches must be **surgical and rare.**

**Patch AM when:**

| Trigger | Pattern |
|---|---|
| Identity change (age, location, job, status) | Update `### Who I Am` / `### Life Focus` |
| Behavior preference change | Update `### Communication Preferences` |
| New dormant background area | Add 1 line, reference file |
| New persistent topic with file | Add 1 line to Archive Index with trigger description |
| Remove obsolete anchor | Delete section (no zombies) |

**Hard constraints on AM patches:**

1. **NEVER replace full AM** unless reconstructing from a verified
   template (avoid the "I rewrote your identity" failure mode)
2. **NEVER add full file content to AM** — references only
   (Archival is the right home)
3. **NEVER add >50 tokens per patch** unless it is a structural fix
4. **NEVER add star/NEW/IMPORTANT markers** — they age out and
   become noise
5. **ALWAYS preserve hierarchy** — `###`, `####`, `-` levels

**Trigger description format for Archive Index entries:**

```
- `<file>.md` – <What it is>. **Load when:** <trigger keywords>.
```

---

## 5.5 Tool Reference Card (verified against Agora master, 2026-08-02)

This card mirrors Agora's actual tool definitions 1:1 — verified against
`MemoryToolProvider.kt`, `RagToolProvider.kt`, `ShellToolProvider.kt`,
`WebSearchToolProvider.kt`, and `ImageGenToolProvider.kt` in the official
Agora repository. **Use the exact tool names and argument keys below** —
invented names will silently fail (the model never sees a tool error,
just a no-op or "Unknown tool" response).

### Memory tools (`MemoryToolProvider`)

| Tool | Args (required* / optional) | When to use | DO NOT |
|---|---|---|---|
| `list_memory_files` | none | Audit; find file by trigger | n/a |
| `read_memory_file` | `name` OR `names[]` | Confirm before patch; batch load | Repeat without reason |
| `create_memory_file` | `name`*, `content`*, opt `description` | New persistent topic | Ephemeral data |
| `edit_memory_file` | `name`* + (`old_string`+`new_string` exact-match) **OR** `content` (full rewrite); opt `new_name`, opt `description` | Surgical fix | Use `content` unless >500 tok |
| `delete_memory_file` | `name`* | User explicit request | NEVER auto-delete (Rule 9) |
| `update_active_memory` | `content`*; opt `mode` (`patch`/`append`/`prepend`/`replace`), opt `old_string`/`new_string` (for patch) | Identity / status / index change | `mode="replace"` unless full reconstruction |

**`update_active_memory` modes** (canonical, in priority order):

1. **`patch`** — find `old_string` exactly once, replace with `new_string`. **Default-preferred** — directly enforces Failure Mode #1 prevention (AM hijack).
2. **`append`** — add `content` to end (e.g. new section header)
3. **`prepend`** — add `content` to beginning
4. **`replace`** — overwrite full AM. **Avoid unless reconstructing from verified template** (Failure Mode #1: AM hijack).

**`edit_memory_file` invariants** (enforced by Agora code):

- `content` and `old_string` are **mutually exclusive** (Error otherwise)
- `old_string` requires `new_string` (use `""` to delete matched text)
- `old_string` must match **exactly once** (else Error)
- At least one of `content`, `old_string`, `new_name`, `description` must be present

### Shell + File tools (`ShellToolProvider`)

| Tool | Args | When |
|---|---|---|
| `list_shells` | none | Server target ambiguous (>1 shell configured) |
| `execute_shell_command` | `command`*; opt `server`, `timeout_ms` (≤120 s fg / ≤86 400 s bg), `workdir`, `background` (Conch only) | Shell op on local sandbox or remote |
| `list_shell_jobs` / `get_shell_job` / `stop_shell_job` | Conch only | Durable background jobs |
| `file_read` | `path`*; opt `server`, `offset`, `limit` (default 1 MB) | Inspect before edit |
| `file_write` | `path`*, `content`*; opt `server` | New file / full overwrite |
| `file_edit` | `path`*, `old_string`*, `new_string`; opt `server`, `replace_all` | Surgical fix (replaces 1 by default; `replace_all=true` for many) |
| `file_glob` | `pattern`*; opt `server`, `path`, `depth` | Find files by glob |
| `file_grep` | `pattern`*; opt `server`, `path`, `glob` | Regex search |

`server` is required only when >1 shell device is configured; otherwise omit
(or use `"Local Sandbox"` for the on-device Alpine rootfs).

### RAG / conversation-history tools (`RagToolProvider`)

| Tool | Args | When |
|---|---|---|
| `search_conversations` | `query`*; opt `limit` (1–20, default 10) | Recall prior context (semantic + keyword) |
| `list_conversations` | opt `order` (`asc`/`desc`), `limit` (1–50), `offset` | Browse history |
| `read_conversation` | `conversation_id`*; opt `offset`, `limit` (1–100) | After `list_conversations` or `search_conversations` |

### Web tools (`WebSearchToolProvider`)

| Tool | Args | When |
|---|---|---|
| `web_search` | `query` | Fact verification; current info |
| `web_fetch` | URL | Primary-source deep read |

### Image generation (`ImageGenToolProvider`, BYOK)

| Tool | Args | When |
|---|---|---|
| `generate_image` | `prompt`; opt `size` | User asks for an image (BYOK key configured) |

---

## 6. Naming Conventions

| Rule | Reason |
|---|---|
| `snake_case.md` only | Clean for tool invocations |
| No spaces, no diacritics in filenames | Encoding safety |
| One topic per file | Strict specialization → easier triggers |
| Descriptive name > generic | `audiophile_journey.md` > `audio.md` |
| For frameworks: `<thing>-framework.md` | `deep-research-framework.md`, not `dr_prompt.md` |

---

## 7. Proactive Triggers — When the Agent Should Suggest Updates

The AI agent should propose a memory operation when:

| Situation | Suggested action |
|---|---|
| User says "I changed X to Y" | "Should I update `<file>.md` and/or AM?" |
| Conversation contains >5 distinct facts about a topic without existing file | "This looks like a candidate for a new memory file — create it?" |
| Contradiction detected between AM and existing file | "AM says X, but `<file>` says Y — how should we reconcile?" |
| AM mentions a file but file does not exist (or vice versa) | "Reference in AM points to a non-existent file — fix it?" |
| User asks "What do you know about me?" | Offer memory audit (read all + summarize) |
| 6+ months since last file edit | Suggest quarterly review |

**Rule:** Never execute proactive memory operations silently.
Always propose, get approval, then execute.

---

## 8. Audit Cycles

| Cadence | Trigger | Action |
|---|---|---|
| **Quarterly** | Every 90 days | Memory audit: list all files, check AM consistency, surface bloat |
| **Change-triggered** | Major life event (job, hobby pivot, project end) | Full AM rewrite with user approval |
| **Bloat-triggered** | AM >1800 tokens OR file >3000 tokens | Refactor or split |
| **User-initiated** | User asks for "memory audit" or similar | Full review, no auto-changes |

**Audit checklist:**

- [ ] AM age/contact info current?
- [ ] Dormant background still accurate?
- [ ] Archive Index — all files exist + descriptions accurate?
- [ ] Any file >3000 tokens (split candidate)?
- [ ] Any reference in AM pointing nowhere?
- [ ] Any file with content duplicating AM?

---

## 9. Contradiction Handling

When AM and a file disagree (or two files disagree):

1. **Surface both** to user with citations (do not pick a winner
   silently)
2. **Default to most recent** timestamp for ephemeral facts
3. **Default to user-stated** for identity facts (override even if
   file is old)
4. **Log the contradiction** in a methodology note of the relevant
   file (if major)
5. **Resolve via patch**, not overwrite

---

## 10. Failure Modes to Avoid

| Failure mode | Symptom | Prevention |
|---|---|---|
| **AM hijack** | Replace full AM with one new fact | Patch-only mode, never replace |
| **Zombie markers** | "⭐ NEW" from 30 days ago | Audit cycle removes stale markers |
| **Doubletalk** | Same fact in AM + file | One source of truth rule |
| **Phantom references** | AM cites file that does not exist | Audit + dry-run after every rename |
| **Bloated AM** | >1800 tokens, recall degrades | Progressive disclosure (file reads) |
| **Silent delete** | File disappears without trace | Always confirm, log in audit |
| **Overzealous proactive** | Agent writes to memory without permission | Default = propose, do not act |

---

## 11. Execution Contract

Before any memory operation, run this checklist:

```
1. ACKNOWLEDGE: What memory operation is needed
   (read / write / update / delete)?
2. SCOPE: Which file(s) and/or AM sections are affected?
3. RISK ASSESSMENT:
   - Read: zero risk
   - Write new file: medium risk (low if user requested)
   - Update existing: medium risk (need precise patch)
   - Delete: HIGH risk (always confirm)
   - AM patch: HIGH risk (identity-altering potential)
4. PROPOSE: Tell user what you intend to do (concise)
5. CONFIRM: Wait for approval on HIGH risk, proceed on LOW
6. EXECUTE: Use precise tool calls, exact old_string matches
7. VERIFY: Read back or summarize what changed
8. LOG: If change was structural (>50 tok), mention in next reply
```

---

## 12. Key Principles (Single-line)

1. **Core is precious, Archival is cheap** — bias toward files,
   away from AM
2. **Patch, never overwrite** — atomic, reversible
3. **Trigger descriptions over content dumps** — "**Load when:**"
   beats long summaries
4. **Propose, do not act** — on memory operations, especially AM
5. **Audit beats assumption** — verify references exist, dates
   current
6. **One source of truth per fact** — AM and file must agree
7. **Static vs Dynamic** — historical (CV, dormant stack) → file;
   current status → AM
