# Audit Cycles, Contradictions, Failure Modes & Execution Contract

> **Companion to:** `00-master-index.md`
> **Scope:** Recurring audits, contradiction handling between AM and files, known failure modes, execution checklist.

---

## 1. Audit Cycles

| Cadence | Trigger | Action |
|---|---|---|
| **Quarterly** | Every 90 days | Memory audit: list all files, check AM consistency, surface bloat |
| **Change-triggered** | Major life event (job, hobby pivot, project end) | Full AM rewrite with user approval |
| **Bloat-triggered** | AM >1500 tokens OR file >3000 tokens | Refactor or split |
| **User-initiated** | User asks for "memory audit" or similar | Full review, no auto-changes |

**Audit checklist:**

- [ ] AM age/contact info current?
- [ ] Dormant background still accurate?
- [ ] Archive Index — all files exist + descriptions accurate?
- [ ] Any file >3000 tokens (split candidate)?
- [ ] Any reference in AM pointing nowhere?
- [ ] Any file with content duplicating AM?
- [ ] All Archive Index entries have `**Load when:**` trigger?
- [ ] All file filenames follow Naming Conventions (no `/`, `\`, `..`)?

---

## 2. Contradiction Handling

When AM and a file disagree (or two files disagree):

1. **Surface both** to user with citations (do not pick a winner silently)
2. **Default to most recent** timestamp for ephemeral facts
3. **Default to user-stated** for identity facts (override even if file is old)
4. **Log the contradiction** in a methodology note of the relevant file (if major)
5. **Resolve via patch**, not overwrite

If `Access Active Memory` is OFF and the agent cannot read AM, treat
this as a "contradiction source unknown" and ask the user.

---

## 3. Failure Modes to Avoid

| Failure mode | Symptom | Prevention |
|---|---|---|
| **AM hijack** | Replace full AM with one new fact | Patch-only mode, never replace (except Recovery) |
| **Zombie markers** | "⭐ NEW" from 30 days ago | Audit cycle removes stale markers |
| **Doubletalk** | Same fact in AM + file | One source of truth rule |
| **Phantom references** | AM cites file that does not exist | Audit + dry-run after every rename |
| **Bloated AM** | >1500 tokens, recall degrades | Progressive disclosure (file reads) |
| **Silent delete** | File disappears without trace | Always confirm + log in audit |
| **Overzealous proactive** | Agent writes to memory without permission | Default = propose, do not act |
| **Patch uniqueness explosion** | `old_string` matches >1 times | Read first, use longer context |
| **Permission misread** | Tool call fails silently | Check `Settings → Memory` permissions before calling |
| **Stateless UI assumption** | Treats AM as if it has a GUI structure | AM is plain text — headers are conventions, not enforced |

---

## 4. Execution Contract (Before Any Memory Operation)

Before any memory operation, run this checklist:

```
1. ACKNOWLEDGE: What memory operation is needed
   (read / write / update / delete / AM-patch)?
2. SCOPE: Which file(s) and/or AM sections are affected?
3. RISK ASSESSMENT:
   - Read: zero risk
   - Write new file: medium risk (low if user requested)
   - Update existing (patch): medium risk (reversible)
   - Update existing (full content): HIGH risk (need confirmation)
   - Rename: HIGH risk (need confirmation)
   - Delete: HIGH risk (always confirm)
   - AM patch (targeted): HIGH risk (identity-altering potential)
   - AM replace: VERY HIGH risk (recovery only)
4. PROPOSE: Tell user what you intend to do (concise)
5. CONFIRM: Wait for approval on HIGH risk, proceed on LOW
6. EXECUTE: Use precise tool calls, exact old_string matches
   - `old_string` must match exactly once — else fails
   - For AM: verify `Access Active Memory` is ON first
7. VERIFY: Read back or summarize what changed
8. LOG: If change was structural (>50 tok), mention in next reply
```

### 4.1 Risk Matrix Summary

| Op | Risk | Confirmation |
|---|---|---|
| `read_memory_file` | None | None |
| `list_memory_files` | None | None |
| `create_memory_file` | Low | Standard proposal |
| `edit_memory_file` (patch) | Medium | Standard proposal (reversible) |
| `edit_memory_file` (full content) | High | Explicit user GO |
| `edit_memory_file` (rename) | High | Explicit user GO |
| `delete_memory_file` | Very High | Explicit user GO + verbal confirmation |
| `update_active_memory` (patch) | High | Standard proposal |
| `update_active_memory` (replace) | Very High | Explicit user GO + diff summary |
| AM change to identity/preferences | Very High | Explicit user GO, even for "small" changes |

---

## 5. Token Economics (Why Modular Split Matters)

Before the refactor, `memory-management-framework.md` was a single
437-line file. Loading it for any memory operation cost ~1300 tokens
of context. After the refactor (modular split):

- **File operation** (read/write/delete) → load `01-file-operations.md` (~350 tok)
- **AM content decision** → load `02-am-anatomy.md` (~300 tok)
- **AM authority decision** → load `03-am-authority.md` (~350 tok)
- **Tool verification** → load `04-tool-reference-card.md` (~300 tok)
- **Audit / failure** → load `05-audit-failure-modes.md` (~250 tok)
- **Unsure** → load `00-master-index.md` (~250 tok) + follow links

Net saving: ~50 % tokens per typical memory operation.
