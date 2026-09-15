# Architecture Overview

One-page map of the whole setup: why the layers exist, which documents and
Skills implement each, and where a new piece belongs. This document explains
*why* the architecture is shaped this way; `README.md` lists *what* the
repository contains and *how* to install it.

## The layers

```text
┌──────────────────────────────────────────────────────────────┐
│ 1. Kernel — System template                                  │
│    permanent behavior, routing, safety, approval gate        │
├──────────────────────────────────────────────────────────────┤
│ 2. State handoff — Compact template                          │
│    survives long conversations without drift                 │
├──────────────────────────────────────────────────────────────┤
│ 3. Skills — procedures loaded on demand                      │
│    how to work; no personal facts                            │
├──────────────────────────────────────────────────────────────┤
│ 4. Memory — Active (current context) + Saved (durable facts) │
├──────────────────────────────────────────────────────────────┤
│ 5. Domains — packages of 3 + 4 for life areas                │
├──────────────────────────────────────────────────────────────┤
│ 6. Automation — Tasks/Loops run the same agent later         │
├──────────────────────────────────────────────────────────────┤
│ 7. Future: native multi-agent runtime (doc/16, proposal)     │
└──────────────────────────────────────────────────────────────┘
```

Cross-cutting: **capability gating** (verify tools at runtime) and the
**permission model** (classes × approval bands) apply to every layer.

## Design decisions

1. **Single-agent first.** One kernel with loaded context beats many
   "specialist agents": one authority, one safety floor, no duplication.
   Specialization lives in Skills and domain packages (`docs/18`).
2. **Progressive disclosure.** The kernel stays compact; Skills load only when
   relevant. Catalog discovery ≠ Skill loading ≠ execution.
3. **Instructions ≠ information.** Procedures are Skills; facts are Memory;
   current status is Active Memory. Mixing them is the main source of drift.
4. **Runtime evidence wins.** Settings screens and documentation prove nothing;
   a capability exists only when a tool call proves it (`docs/15`).
5. **Permission floor.** Every layer may tighten approval bands, never loosen
   them (`docs/17`).
6. **Automation is not a second agent.** A Task or Loop is the same agent run
   later, under the same kernel and gates (`docs/16` phases it as future work).

## Document map

| Layer / concern | Docs | Skills |
|---|---|---|
| Kernel & templates | `docs/3` | — |
| Reasoning & routing | `docs/6`, `docs/14` | `sequential-thinking-workflow` |
| Compact / state handoff | `docs/12` | — |
| Skills model | `docs/5` | `skill-format.md` (authoring guide) |
| Memory layers | `docs/4`, `docs/13` | `memory-master-index` + governance family |
| Tools & safety | `docs/8`, `docs/9` | `tool-execution-contract`, `shell-and-device-operations` |
| Research | `docs/7` | `multi-source-research` |
| Capability gating | `docs/15` | implemented in `agora-coordinator` |
| Permission model (normative) | `docs/17` | — |
| Domain routing | `docs/18` | — |
| Coordination & audits | `docs/11` | `agora-coordinator` |
| Multi-agent (future) | `docs/16` — proposal for the Agora application | — |
| Models | `docs/10` | — |

## Decision tree: where does new content belong?

```text
New content
├─ A rule the agent must follow in EVERY conversation?
│   → System template (keep it short)
├─ A repeatable procedure?
│   → Skill (follow skills/skill-format.md)
├─ A durable fact, decision, or reference?
│   → Saved Memory
├─ Current status / priority / constraint?
│   → Active Memory (2–6 lines)
├─ Recurring work in a specific life area?
│   → Domain package (docs/18)
├─ Should happen later, unattended?
│   → Task/Loop proposal — creation needs explicit approval (docs/17, Orchestrate)
└─ A future application capability, not usable today?
    → document as proposal (like docs/16), never assume it at runtime
```

## Where to start reading

- Installing: `docs/2-installation.md`, then `README.md`.
- Understanding the agent's behavior: this page, then `docs/6`.
- Extending with a new domain: `docs/18`.
- Governing memory: `docs/13`.
