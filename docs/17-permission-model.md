# Permission Model

This document is the normative, unified permission and approval model for the
setup. It merges two earlier, partial descriptions:

- `docs/8-tools-and-safety.md` — the universal approval gate (what requires approval);
- `docs/16-multi-agent-system.md` — the capability-class vocabulary
  (Observe / Retrieve / Transform / Modify / External effect / Orchestrate),
  proposed there for a future native multi-agent runtime but directly usable
  for single-agent operation today.

`docs/8` remains valid: it states *which* actions require approval. This
document adds *how much* scrutiny each class of action receives.

## Design goal

A single agent must decide, for every action:

1. **which capability class** the action belongs to;
2. **which approval band** applies to that class in the current context;
3. **when to stop and ask** instead of proceeding.

## Capability classes

| Class | Meaning | Examples |
|---|---|---|
| **Observe** | Read current configuration, Skills, memory, conversations, tool availability | `list_skill_files`, `read_memory_file`, `list_shells` |
| **Retrieve** | Read external sources | `web_search`, `web_fetch`, conversation search, MCP read tools |
| **Transform** | Draft, summarize, analyze, calculate, generate proposals | writing a plan, refactoring text, computing a comparison |
| **Modify** | Edit Skills, memory, files, local configuration | `create/edit memory file`, sandbox `file_write`, shell `git commit` (local) |
| **External effect** | Reach beyond the user's own environment | push, publish, send, purchase, delete remote data, system-altering commands |
| **Orchestrate** | Create or change automation, delegate, schedule | `create_task`, `start_loop`, recursive Task creation |

## Approval bands

Three bands, deliberately coarse so they are usable mid-conversation:

| Band | Name | Policy |
|---|---|---|
| **A** | Autonomous | Act, then verify and report. No prior approval needed. |
| **B** | Verified consent | Show the exact action and scope; proceed on a positive reply in context. A general "help me with X" is not consent for a specific Modify/External action. |
| **C** | Explicit authorization | Require an unambiguous, current, scope-specific approval — ideally repeated back ("I will push branch X to origin; confirm"). |

## The matrix

| Class | Default band | Escalation to C |
|---|---|---|
| Observe | A | never (but respect access settings) |
| Retrieve | A | — |
| Transform | A | — |
| Modify | B; A only for clearly reversible, small-scope edits (e.g. new sandbox scratch file) | irreversible or large-scope modification; anything touching durable memory wholesale |
| External effect | C | always C; no automatic downgrade |
| Orchestrate | B for a proposal; C for actual creation | Tasks/Loops that run unattended or recur indefinitely are always C |

Band assignments are defaults, not permissions: an action can still be blocked
by application settings, tool availability, or the current confirmation policy.
Capability gating (`docs/15-capability-gating.md`) always applies first — a
class can be assigned only if the capability is verified as available.

## Stop conditions

Stop and request a decision regardless of band when:

- scope, reversibility, or ownership of the target is unclear;
- two sources conflict about the desired state;
- a prior attempt failed for a non-transient reason;
- the action affects legal, financial, employment, or safety matters.

## Relation to other documents

- `docs/8-tools-and-safety.md` — the approval gate this model refines.
- `docs/15-capability-gating.md` — verification of tool availability (precondition).
- `docs/16-multi-agent-system.md` — source of the class vocabulary; its native
  MAS runtime, when implemented, should map agent-profile permissions onto
  these classes and bands.
- `docs/18-domain-routing.md` — domains may assign stricter bands per class,
  never laxer ones than this model.

## Non-goals

This model does not introduce numeric risk tiers as runtime syntax, does not
assume the multi-agent runtime exists, and does not replace the application's
own confirmation settings — it sits above them as the agent-side decision rule.
