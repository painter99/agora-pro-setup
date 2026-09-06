# 🎯 Agora Skills

This directory contains **reusable instruction files** for Agora's native **Saved Skills** library (Agora 2.1+).

They are **not** Saved Memories. Memories hold information. Skills hold procedures.

---

## How Skills work

When **Allow skill access** is enabled:

1. Agora builds a compact catalog of each Skill's **name + short description**.
2. That catalog is injected only if the System template contains `{skill_catalog}`.
3. The model reads a relevant body with `read_skill_file`.
4. Skill bodies are **not** stuffed into every request.

There is **no Active Skill**. Do not create `active_skill.md` or an active-Skill toggle.

The internal `Load when` section inside a Skill is documentation and post-read validation. It cannot be the first discovery mechanism — the catalog is.

---

## 📲 Installation

1. Agora → **Settings → Memory & Data → Skills**
2. Enable Skill access if you want the catalog and Skill tools.
3. **Add** → import Markdown or paste.
4. **Name** (flat, no folders, usually without `.md`): `deep-research`
5. **Description** (short — this is what `{skill_catalog}` shows)
6. Save.

Repeat per file. Repository folders are for humans only.

### Suggested catalog descriptions

| Install as | Description |
|---|---|
| `00-master-index` | Routes memory operations. Load when remember/forget/save/update/audit. |
| `01-file-operations` | Saved Memory file CRUD, naming, proactive suggestions. |
| `02-am-anatomy` | What belongs in Active Memory and what must stay out. |
| `03-am-authority` | Who may change Active Memory; recovery and confirmation. |
| `04-tool-reference-card` | Exact Agora tool names, including Skill tools. |
| `05-audit-failure-modes` | Memory audits, contradictions, failure modes. |
| `deep-research` | Multi-source research with source scoring and quality gates. |
| `tool-execution-contract` | Shared inspect / approve / verify rules for tools. |
| `shell-and-devices` | Local Sandbox, Conch, SSH, durable jobs. |

---

## Design rules

- One Skill = one class of task.
- Catalog descriptions must be concrete. "Anything related" causes over-loading.
- Do not duplicate the entire System template inside a Skill.
- Declare dependencies by **flat Skill name**.
- Keep `deep-research` as one file (accepted length trade-off).
- Keep memory governance **split** (00–05) so typical operations load ~one file.

---

## Available Skills

| Path in this repo | Agora Skill name |
|---|---|
| `research/deep-research.md` | `deep-research` |
| `tool-execution-contract.md` | `tool-execution-contract` |
| `shell/shell-and-devices.md` | `shell-and-devices` |
| `memory-management/00-master-index.md` | `00-master-index` |
| `memory-management/01-file-operations.md` | `01-file-operations` |
| `memory-management/02-am-anatomy.md` | `02-am-anatomy` |
| `memory-management/03-am-authority.md` | `03-am-authority` |
| `memory-management/04-tool-reference-card.md` | `04-tool-reference-card` |
| `memory-management/05-audit-failure-modes.md` | `05-audit-failure-modes` |
| `examples/example-project-skill.md` | optional |
| `examples/example-learning-skill.md` | optional |

`skill-format.md` is documentation for authors, not a runtime Skill.
