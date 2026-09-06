# Skill: Memory Master Index

## Catalog description

Routes Active Memory and Saved Memory operations. Load when remember/forget/save/update/audit, or AM vs file disagreement.

> Install this file into Agora **Saved Skills** (flat name, no directories).
> The body below is the operational contract. `Memory Master Index` in the Skill Catalog should stay short.

---

# Memory Management Framework — Master Index

> **Purpose:** Comprehensive governance for memory operations in Agora.
> **Architecture:** Tiered model — Core (in-context AM) + Recall (conversations) + Archival (Saved Memories).
> **Scope:** Every memory operation follows this framework autonomously; deviations must be justified.

This is the **master index** — it does not contain rules itself.
Read the specialized file that matches your operation. When in doubt,
read the **Decision Guide** below.

---

## 🚦 Quick Decision Guide — Which File Should I Read?

| If you are about to... | Read this file first |
|---|---|
| Create a new Saved Memory file | `01-file-operations` (Skill) (Write Policy) |
| Update an existing Saved Memory file | `01-file-operations` (Skill) (Update Policy) |
| Delete or archive a Saved Memory file | `01-file-operations` (Skill) (Delete Policy) |
| Choose a filename or naming convention | `01-file-operations` (Skill) (Naming) |
| Suggest a memory operation proactively | `01-file-operations` (Skill) (Proactive Triggers) |
| Decide what to put in Active Memory | `02-am-anatomy` (Skill) (Anatomy + Quotas) |
| Write or update Active Memory content | `02-am-anatomy` (Skill) + `03-am-authority` (Skill) |
| Recover Active Memory from drift / corruption | `03-am-authority` (Skill) (Recovery Protocol) |
| Verify if a tool call is correct | `04-tool-reference-card` (Skill) |
| Audit memory or resolve contradictions | `05-audit-failure-modes` (Skill) |
| Unsure about anything | Read this file — then follow the link |

---

## 📂 Architecture Map

| Tier | Agora component | Lifetime | Cost per request | Update mechanism |
|---|---|---|---|---|
| **Core** (in-context) | Active Memory widget | Always injected in every prompt | Paid every turn (~tokens) | `update_active_memory` (patch only) |
| **Recall** | Conversation history (searchable) | Indefinite, search-indexed | Free to query | `search_conversations`, `read_conversation` |
| **Archival** | Saved Memories (file-based) | Indefinite, file-read on demand | Free unless loaded | `list_memory_files`, `read_memory_file`, `create_memory_file`, `edit_memory_file`, `delete_memory_file` |

**Critical asymmetry:** Core memory costs tokens every turn. Archival
is free until loaded. This asymmetry drives most of the rules below.

---

## 📚 Specialized Files

| # | File | Purpose | Lines |
|---|---|---|---|
| 01 | `01-file-operations` (Skill) | Write / Update / Delete / Naming / Proactive triggers for Saved Memories | ~120 |
| 02 | `02-am-anatomy` (Skill) | Active Memory structure, quotas, content anti-patterns, AM ↔ System Prompt integration | ~90 |
| 03 | `03-am-authority` (Skill) | Who can change AM, hard rules, recovery protocol, confirmation protocol | ~100 |
| 04 | `04-tool-reference-card` (Skill) | Tool reference 1:1 with Agora (memory, file, shell, RAG, web, image) | ~90 |
| 05 | `05-audit-failure-modes` (Skill) | Audit cycles, contradiction handling, failure modes, execution contract | ~70 |

---

## 🔑 Key Principles (Single-line — keep these in mind)

1. **Core is precious, Archival is cheap** — bias toward files, away from AM
2. **Patch, never overwrite** — atomic, reversible
3. **Trigger descriptions over content dumps** — `**Load when:**` beats long summaries
4. **Propose, do not act** — on memory operations, especially AM
5. **Audit beats assumption** — verify references exist, dates current
6. **One source of truth per fact** — AM and file must agree
7. **Static vs Dynamic** — historical (CV, dormant stack) → file; current status → AM
8. **Permissions default to off** — verify `Access Active Memory` + `Access Saved Memories` are ON before any memory tool call (`Settings → Memory`)
9. **AM may be incomplete or stale** — auto-refresh is OK when context warrants, never silently
10. **User-message-wins** — if AM conflicts with current user message, the user message wins (Agora `DefaultSystemPrompt.kt` literal)

---

## ⚡ Performance Notes

- **Token budget:** Total AM target ~350 tokens, hard limit 1500 tokens (Agora performance cliff)
- **Per-patch budget:** ≤ 50 tokens, unless structural fix or recovery
- **Patches per session:** ≤ 1, unless user explicitly requests multiple
- **Skill loading:** Read only the specialized file you need — saves ~60 % tokens vs. reading one big file

---

## 🔗 Cross-References

| If you need to... | Also see |
|---|---|
| Verify a tool name and its arguments | `04-tool-reference-card` (Skill) |
| Check AM quotas before patching | `02-am-anatomy` (Skill) § Quotas |
| Resolve a contradiction between AM and a file | `05-audit-failure-modes` (Skill) § Contradiction Handling |
| Decide whether to delete or archive | `01-file-operations` (Skill) § Delete / Archive Policy |
| Understand the AM authority model | `03-am-authority` (Skill) § Three Roles |

---

## 🛠 Partner AM Archive Index Entry

This Skill lives in Agora **Saved Skills**. Do not also store it as a Saved Memory.
Saved Memories hold *information*. This file holds *procedure*.

If you still keep a Memory Archive Index, it should list information files, not this Skill.
Optional Active Memory reminder:


```
- `00-master-index` – Master index for memory
  governance. **Load when:** user asks about memory operations,
  create/update/delete file, AM patches, audit, or AM vs file
  disagreement. For specialized sub-files (anatomy, authority,
  tools, audit), see cross-references inside.
```
