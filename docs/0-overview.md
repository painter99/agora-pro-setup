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
│ 4. Memory — file-based AM (current) + Saved (durable facts)  │
├──────────────────────────────────────────────────────────────┤
│ 5. Domains — packages of 3 + 4 for life areas                │
├──────────────────────────────────────────────────────────────┤
│ 6. Automation — Tasks/Loops run the same agent later         │
├──────────────────────────────────────────────────────────────┤
│ 7. Multi-agent: Subagents partial; profiles open (docs/16)  │
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
   current status is the file-based AM working state file. Mixing them is the
   main source of drift.
4. **Runtime evidence wins.** Settings screens and documentation prove nothing;
   a capability exists only when a tool call proves it (`docs/15`).
5. **Permission floor.** Every layer may tighten approval bands, never loosen
   them (`docs/17`).
6. **Automation is not a second agent.** A Task or Loop is the same agent run
   later, under the same kernel and gates (`docs/16` phases the remaining
   proposed capabilities as future work; native subagents are partially
   delivered).

## Document map

| Layer / concern | Docs | Skills |
|---|---|---|
| Kernel & templates | `docs/3` | — |
| Reasoning & routing | `docs/6`, `docs/14` | `sequential-thinking-workflow` |
| Compact / state handoff | `docs/12` | — |
| Skills model | `docs/5` | `skill-format.md` (authoring guide) |
| Memory layers | `docs/4`, `docs/13` | `memory-master-index` + governance family |
| Tools & safety | `docs/8`, `docs/9`, `docs/21` | `tool-execution-contract`, `shell-and-device-operations` |
| Research | `docs/7` | `multi-source-research` |
| Capability gating | `docs/15` | implemented in `agora-coordinator` |
| Permission model (normative) | `docs/17` | — |
| Memory gate (kernel enforcement) | `docs/20` | `memory-master-index` + governance family |
| Domain routing | `docs/18` | — |
| Coordination & audits | `docs/11` | `agora-coordinator` |
| Multi-agent | `docs/16` — native Subagents partially delivered; remaining MAS features, including profiles, remain proposals | — |
| Stack update observability | `docs/28` | — |
| Self-improvement loop | `docs/29` | `self-improvement-loop` |
| Decision records | `decisions/` (index: `decisions/README.md`) | — |
| Instance overlay | `docs/30` | — |
| Platform layer (host units) | `docs/31` | — |
| Coding workflow | `docs/32` | `coding-loop` |
| Programming agent roles | `docs/33` | — |
| Two-agent bridge (coordination ↔ coding agent) and the case study of the two-agent working environment | `docs/34` | `agora-goose-bridge` |
| Generic two-agent operating-procedure adaptation guide | `docs/35` | — |
| Coordination and optional external research architecture | `docs/36` — preservation draft, not operating policy | — |
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
│   → file-based AM (working state file, 2–6 lines)
├─ Recurring work in a specific life area?
│   → Domain package (docs/18)
├─ An architectural decision worth recording?
│   → ADR in decisions/ (format: decisions/README.md)
├─ Should happen later, unattended?
│   → Task/Loop proposal — creation needs explicit approval (docs/17, Orchestrate)
└─ A future application capability, not usable today?
    → document as proposal (like the open features in docs/16), never assume it at runtime
```

## Where to start reading

- Installing: `docs/2-installation.md`, then `README.md`.
- Understanding the agent's behavior: this page, then `docs/6`.
- Extending with a new domain: `docs/18`.
- Governing memory: `docs/13`.
- Tool-call retry discipline and budget: `docs/21`.
- Dispatch spend discipline and spend observability: `docs/37`.
- Stack update observability: `docs/28`.
- Agent self-improvement and autonomous repository maintenance: `docs/29`.
- Why the architecture is the way it is: `decisions/` (decision records).
- Adapting this setup to another person or language: `docs/30`.
- Host-level services (MCP servers, exchange watcher): `docs/31`, with the
  host walkthrough in `docs/23`.
- Coding tasks (the agent writes code): `docs/32`.
- Who does what in programming projects (roles, delegation, merge GO):
  `docs/33`.
- Adopting the generic two-agent operating process: `docs/35`; use the shared
  Skill and `docs/34` for the binding dispatch contract, and keep local details
  in a private project adapter.
- Proposed coordination and external research architecture: `docs/36` (draft,
  not independently reviewed after revision or deployed).

## Stack layers and owners

The stack has four layers: **Agora** (the governed agent application),
**Goose** (the second, coding-side agent, bridged by `docs/34`), and two
optional, unverified components: **Manus** (external research, `docs/36`
draft) and **Obsidian** (private operator vault, last row below). This
section is an owner index, not a second authority: every linked document
remains the sole owner of its facts. Private (instance-side) owners are
named only as generic classes — this repository never holds live prompts,
schedules, instance paths or private records. "Optional" means the
component is not part of the verified setup; nothing here implies
deployment or new runtime behavior.

| Artifact class | Canonical owner | Public / private boundary | Derivation / verification |
|---|---|---|---|
| Architecture, boundaries, data flows | [docs/0-overview.md](0-overview.md) (this map) plus each domain doc for its own facts ([docs/17](17-permission-model.md), [docs/28](28-update-observability.md), [docs/29](29-self-improvement-loop.md), [docs/30](30-instance-overlay.md), [docs/33](33-programming-agent-roles.md), [docs/34](34-agora-goose-bridge.md), [docs/37](37-spend-observability.md)); approved decisions in [decisions/README.md](../decisions/README.md) | Generic and public; instance-specific component facts live in the private instance overlay, described generically by [docs/30](30-instance-overlay.md) | [README.md](../README.md) and [AGENTS.md](../AGENTS.md) are audience-specific navigation indexes — update when an owner changes; verify targets and sample claims, not only links |
| Role and permission policy | `system-prompt/` templates, [docs/17](17-permission-model.md), [docs/33](33-programming-agent-roles.md), Part 2 of [docs/34](34-agora-goose-bridge.md) (binding bridge contract); Skill [agora-goose-bridge](../skills/coordination/agora-goose-bridge/SKILL.md) implements the workflow | Part 1 of [docs/34](34-agora-goose-bridge.md) is a dated case study, not policy; actual instance restrictions may tighten but never loosen these floors | [README.md](../README.md), [AGENTS.md](../AGENTS.md) and this document navigate only; none creates a competing role policy |
| Skills | `skills/<family>/<name>/SKILL.md`; format [skills/skill-format.md](../skills/skill-format.md); catalog [skills/skill-catalog.md](../skills/skill-catalog.md); inventory [manifest.yaml](../manifest.yaml) | Deployed Skill stores and Goose copies are deployment observations, not alternative policy owners | Catalog entries derive from each Skill's frontmatter description; verify against a fresh complete store export (name, bytes, direction); mismatches are reported, not blindly overwritten; any repair follows the authorized repo-to-store repair rule of the [skill-mirror-check](../skills/coordination/skill-mirror-check/SKILL.md) mirror policy |
| Tasks (automation) | `tasks/*.md` generic reference cards ([tasks/README.md](../tasks/README.md)); automation model [docs/16](16-multi-agent-system.md) | Live task prompts, permissions and schedules are private runtime state; the live original stays authority until any verified cutover — none is assumed | Private run briefs and configurations, where they exist, derive clause-by-clause from securely captured live prompts and are reviewed before use; a live scheduler read proves current state, a snapshot only a past state |
| Spend | [docs/37](37-spend-observability.md) (generic policy) | Observed budgets, gateway usage and dispatch ledgers are private instance records | Bounded private rollups with time window and provenance; token counts do not prove cost |
| Run evidence and memory | Governance is public: [docs/4](4-active-memory.md), [docs/13](13-memory-governance.md), [docs/20](20-memory-gate.md), [docs/29](29-self-improvement-loop.md); content is private | Original reports, gateway logs, working state and Saved Memory files each own their own observed facts | Dated summaries cite immutable source identity and status; a derived summary never becomes the primary record |
| Two-agent bridge (Goose) | Part 2 of [docs/34](34-agora-goose-bridge.md) with Skill [agora-goose-bridge](../skills/coordination/agora-goose-bridge/SKILL.md); generic adaptation guide [docs/35](35-two-agent-operating-procedure.md) | Dispatch and review records are private runtime evidence; local details live in a private project adapter | Briefs and reports follow the binding contract; the shared Skill templates never override it |
| External research (Manus) — optional, unverified | [docs/36](36-coordination-architecture-proposal.md) is a preservation draft, explicitly not operating policy | Any approved public-data use registry and access records are private | Whether anything derives from this layer is unknown/unverified; no new external dispatch is implied by this map |
| Operator vault (Obsidian) — optional, unverified | No owner here: any such view is derived, never authority; exchange transport is [docs/27](27-file-exchange.md) | A view is a sanitized export of private approved sources; vault edits are annotations only and cannot update sources or execute tasks | A derived view carries source identifiers, generation timestamp and an explicit derived marker, and is regenerated from its owners; delivery is not verified viewing |
