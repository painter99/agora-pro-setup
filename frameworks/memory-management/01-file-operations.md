# Memory File Operations — Write, Update, Delete, Naming, Proactive

> **Companion to:** `00-master-index.md`
> **Scope:** Operations on Saved Memory files (Archival tier). Does NOT cover Active Memory — see `02-am-anatomy.md` and `03-am-authority.md`.

---

## 1. Write Policy — When to Create a New Saved Memory File

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

### 1.1 Pre-write Verification (Agora `MemoryManager.kt`)

`create_memory_file` **throws if the file already exists** (not idempotent).
Before any `create_memory_file` call:

1. **Run `list_memory_files`** to confirm the name is free
2. **Run `read_memory_file`** (optional) to confirm no near-duplicate content
3. **If file exists** → use `edit_memory_file` (update) instead
4. **If name would conflict** → pick a different filename, do not overwrite

This prevents silent failure on already-existing files.

---

## 2. Update Policy — When to Edit an Existing File

**Edit an existing file when:**

| Trigger | Action |
|---|---|
| User provides new factual data about a covered topic | `edit_memory_file` (patch, not full rewrite) |
| Outdated info detected (date, status, config) | Update specific section |
| Contradiction between file and new evidence | Resolve + note change in file footer |
| File grown >3000 tokens (bloat risk) | Split or refactor; signal for review |

**Update protocol:**

1. **`read_memory_file` first** to confirm exact content + locate target
2. `edit_memory_file` with precise `old_string` → `new_string`
   - `old_string` must match exactly **once** — else throws
   - Use `""` as `new_string` to delete matched text
3. Preserve headers, structure, naming
4. Never overwrite without explicit user approval for PII or critical data (Rule 9)

### 2.1 Description vs Content (Agora-specific)

In Agora, **description is metadata stored in `memory_meta.json`**, not in the file content. The description is:

- Used for **search matching** (RAG)
- Shown in **UI** (Settings → Memory)
- **NOT visible to the model** when `read_memory_file` is called

Implication: when explaining what a file is to the model, **content is the source of truth** — description is for human and search only.

### 2.2 Patch Uniqueness Recovery

`edit_memory_file` fails when `old_string` matches **0 or >1 times**.
When this happens:

1. **Read** the file in full
2. **Locate** the actual unique match (with more context)
3. **Retry** with a more specific `old_string` (include surrounding context)
4. If the duplicate is unintended → fix it first via additional patch, then retry

---

## 3. Delete / Archive Policy — Forgetting

**Delete a file when:**

- User explicit request to forget ("Remove X")
- Topic fully obsolete and superseded by a newer file
- Information provably incorrect and irreparable

**Archive (rename with `_archived_` prefix) when:**

- Dormant for >6 months AND likely never referenced again
- Historical snapshot needed for context but not active work

**Never auto-delete.** All deletes require explicit user
confirmation (system prompt Rule 9: destructive ops need approval +
this framework's Confirmation Protocol — see `03-am-authority.md`).

---

## 4. Naming Conventions

| Rule | Reason |
|---|---|
| `snake_case.md` only | Clean for tool invocations |
| No spaces, no diacritics in filenames | Encoding safety |
| One topic per file | Strict specialization → easier triggers |
| Descriptive name > generic | `audiophile_journey.md` > `audio.md` |
| For frameworks: `<thing>-framework.md` or `<thing>/NN-name.md` | Clear hierarchy |
| **No `/`, `\`, `..` in filenames** | Agora `resolveFile()` sanitizes these as `_`; canonical-path check rejects path traversal |
| **No leading dot** (`.something.md`) | Avoid hidden files |

The `/`, `\`, `..` restriction is enforced by Agora's `resolveFile()` —
attempting to create `<dir>/<file>.md` will silently produce `<dir>_<file>.md`
or fail with `IllegalArgumentException: Invalid file name`.

---

## 5. Proactive Triggers — When the Agent Should Suggest Updates

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

### 5.1 Permission Gating (Agora-specific)

Before any memory tool call, verify that the **Agora Settings** permit it:

| Tool | Requires | Setting |
|---|---|---|
| `list_memory_files` | Always allowed | n/a |
| `read_memory_file` | `Access Saved Memories` ON | `Settings → Memory` |
| `create_memory_file` | `Access Saved Memories` ON | `Settings → Memory` |
| `edit_memory_file` | `Access Saved Memories` ON | `Settings → Memory` |
| `delete_memory_file` | `Access Saved Memories` ON | `Settings → Memory` |
| `update_active_memory` | `Access Active Memory` ON | `Settings → Memory` |

All permissions default to **OFF** (Agora User Manual, FAQ). If the
permission is OFF, the tool call will fail. **Propose to the user
to enable the permission** rather than treating it as a hard error.
