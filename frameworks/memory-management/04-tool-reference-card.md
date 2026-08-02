# Tool Reference Card — Verified Against Agora Master

> **Companion to:** `00-master-index.md`
> **Scope:** Tool names, arguments, and Agora-specific patterns. Verified against Agora master (`MemoryManager.kt`, `ShellToolProvider`, `WebSearchToolProvider`, `ImageGenToolProvider`, `SettingsMemoryPage.kt`).

This card mirrors Agora's actual tool definitions 1:1.
**Use the exact tool names and argument keys below** —
invented names will silently fail (the model never sees a tool error,
just a no-op or "Unknown tool" response).

---

## 1. Memory Tools (`MemoryToolProvider`)

| Tool | Args (required* / optional) | When to use | DO NOT |
|---|---|---|---|
| `list_memory_files` | none | Audit; find file by trigger; pre-create check | n/a |
| `read_memory_file` | `name` OR `names[]` | Confirm before patch; batch load | Repeat without reason |
| `create_memory_file` | `name`*, `content`*, opt `description` | New persistent topic | Ephemeral data; existing file (use `edit`) |
| `edit_memory_file` | `name`* + (`old_string`+`new_string` exact-match) **OR** `content` (full rewrite); opt `new_name`, opt `description`, opt `old_string`+`new_string` | Surgical fix | Use `content` unless >500 tok |
| `delete_memory_file` | `name`* | User explicit request | NEVER auto-delete (Rule 9 + Confirmation Protocol) |
| `update_active_memory` | `content`*; opt `mode` (`patch`/`append`/`prepend`/`replace`), opt `old_string`/`new_string` (for patch) | Identity / status / index change | `mode="replace"` unless full reconstruction |

### 1.1 `update_active_memory` Modes (Canonical Priority)

1. **`patch`** — find `old_string` exactly once, replace with `new_string`. **Default-preferred** — enforces AM hijack prevention.
2. **`append`** — add `content` to end (e.g. new section header)
3. **`prepend`** — add `content` to beginning
4. **`replace`** — overwrite full AM. **Avoid unless reconstructing from verified template** (Recovery Protocol).

### 1.2 `edit_memory_file` / `update_active_memory` Invariants

Both share the same semantics (Agora `MemoryManager.kt`):

- `content` and `old_string` are **mutually exclusive** (Error otherwise)
- `old_string` requires `new_string` (use `""` to delete matched text)
- `old_string` must match **exactly once** (else Error)
- At least one of `content`, `old_string`, `new_name`, `description` must be present

### 1.3 `description` Semantics

`description` is stored in `memory_meta.json` (Agora), NOT in the file.
It is used for:
- **Search matching** (RAG / keyword search)
- **UI display** (Settings → Memory → Saved Memories list)

The model **does not see the description** when calling `read_memory_file`.
Content is the source of truth for the model.

---

## 2. Shell + File Tools (`ShellToolProvider`)

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

---

## 3. RAG / Conversation-History Tools (`RagToolProvider`)

| Tool | Args | When |
|---|---|---|
| `search_conversations` | `query`*; opt `limit` (1–20, default 10) | Recall prior context (semantic + keyword) |
| `list_conversations` | opt `order` (`asc`/`desc`), `limit` (1–50), `offset` | Browse history |
| `read_conversation` | `conversation_id`*; opt `offset`, `limit` (1–100) | After `list_conversations` or `search_conversations` |

---

## 4. Web Tools (`WebSearchToolProvider`)

| Tool | Args | When |
|---|---|---|
| `web_search` | `query` | Fact verification; current info |
| `web_fetch` | URL | Primary-source deep read |

Default provider: **DuckDuckGo Lite** (no API key required). For higher
reliability, configure Brave, Serper, Tavily, or SearXNG.

---

## 5. Image Generation (`ImageGenToolProvider`, BYOK)

| Tool | Args | When |
|---|---|---|
| `generate_image` | `prompt`; opt `size` | User asks for an image (BYOK key configured) |

---

## 6. Concurrency & Atomicity (Agora-specific)

All public methods in `MemoryManager.kt` are **`@Synchronized`**:

- Multiple conversations touching memory **do not race**
- Concurrent `update_active_memory` calls are serialized
- Meta writes use **atomic temp-file + rename** to prevent torn JSON

**Practical implication:** the agent **does not need to coordinate**
memory operations between conversations. Tool calls are safe.

---

## 7. Tool Card UX (In-Chat Cards)

When the agent uses a memory tool, Agora shows an inline card:

| Tool | Card text |
|---|---|
| `list_memory_files` | "Looked through N saved memories" |
| `read_memory_file` | "Read [memory name]" |
| `create_memory_file` | "Saved [memory name]" |
| `edit_memory_file` | "Updated [memory name]" |
| `delete_memory_file` | "Removed [memory name]" |
| `update_active_memory` | "Updated active memory" |

The user can tap the card to inspect the actual content. **Always
be honest about what changed** — never minimize or hide the scope.
