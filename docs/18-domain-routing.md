# Domain Routing

How to add a new domain (work area, project type, hobby, family topic) to the
setup without creating a second agent. The architecture stays single-agent;
specialization lives in loaded context, not in identity.

## Principle

> One agent, many domains. A domain is a package of context and procedures the
> agent loads when a request belongs to that domain — nothing more.

## What a domain package contains

A domain is described by five layers. Most domains need only two or three.

| Layer | Where it lives | Content | Optional? |
|---|---|---|---|
| **Domain Skill(s)** | Saved Skills | Reusable procedure for the domain's recurring work (see `skills/skill-format.md`) | only if the domain has a repeatable procedure |
| **Active Memory block** | Active Memory | Compact current status, priorities, constraints (2–6 lines) | no — this is the routing anchor |
| **Saved Memory file(s)** | Saved Memory | Durable facts, decisions, references, history | when durable knowledge accumulates |
| **Permission overrides** | noted in the domain Skill | Stricter approval bands per class (see `docs/17-permission-model.md`); stricter only, never laxer | only if the domain carries elevated risk |
| **Catalog routing hints** | AM "Optional Saved Memory References" + Skill descriptions | Which file/Skill loads when | no |

## What must NOT go into a domain

- A second persona or "specialist agent" — the kernel stays one agent.
- Personal facts inside public Skills — personal content belongs in Memory.
- A copy of the System template or approval rules — they are global.
- Ephemeral session state — that belongs to the conversation, not to Memory.

## How to add a domain (procedure)

1. **Classify.** What type of work recurs here? Does it need a procedure (Skill)
   or only knowledge (Memory)? Decision rule from `docs/4-active-memory.md`:
   procedure → Skill; durable fact → Saved Memory; current status → AM.
2. **Write the Active Memory block.** Two to six lines: status, priorities,
   constraints. This is what makes the domain routable in ordinary conversation.
3. **Write the domain Skill** (if needed) using `skills/skill-format.md`.
   Declare dependencies (usually `tool-execution-contract.md`; add
   `multi-source-research.md` or `shell-and-device-operations.md` when relevant).
4. **Assign permission overrides** (if needed) as a small table in the Skill:
   capability class → stricter band, with one-line justification.
5. **Register references.** Add the Saved Memory files to the AM reference list
   with a "Load when" hint. Keep the catalog description concrete.
6. **Verify.** Ask a harmless in-domain question and confirm the right Skill
   gets loaded and the right Memory referenced; check that no other domain's
   content leaked into the answer.

## Worked example (fictional)

Domain: *Home brewing*.

- **AM block:**
  `### Home brewing — equipment: 20 l kettle, fermentation fridge; active
  batch: none; constraint: budget ~50 EUR/batch.`
- **Skill:** `brewing-batch-log.md` — procedure for planning and logging a
  batch; dependencies: none; permission overrides: none.
- **Saved Memory:** `brewing-recipes.md` (durable recipes), `brewing-history.md`
  (past batches, lessons).
- **Routing check:** "How long should the mash rest?" → kernel classifies as
  domain question → loads `brewing-batch-log.md` if procedure needed, otherwise
  answers from conversation + optional recipe reference. No new persona.

## Elevated-risk domain example

Domain: *Employment and career*.

- Permission overrides in the domain Skill:

  | Class | Default band (doc/17) | Domain band |
  |---|---|---|
  | External effect | C | C (unchanged) — any application, message, or publication |
  | Transform | A | B — drafts get explicit review before any further use |

- Justification: employment actions have durable external consequences; drafts
  shape decisions that are hard to reverse.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| One Skill per minor topic | Catalog bloat; routing noise | Merge into one domain Skill with a `Load when` section |
| Domain facts in the Skill body | Stale, private, duplicated | Facts → Saved Memory; procedure → Skill |
| Domain overrides that *loosen* bands | Breaks the global safety floor | Domains may only escalate |
| Separate "domain agent" prompt | Splits authority; duplicates rules | One kernel + loaded context |

## Relation to other documents

- `docs/4-active-memory.md` — the placement decision rule this extends.
- `docs/5-skills.md` — Skill model and families.
- `docs/13-memory-governance.md` — memory-layer governance for the package.
- `docs/17-permission-model.md` — bands that domain overrides may only tighten.
