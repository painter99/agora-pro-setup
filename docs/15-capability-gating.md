# Capability Gating

A pattern for agents operating in environments where tool availability cannot be assumed from settings, changelogs, or past runs.

## The problem

Agora provisions tools per generation path. Different paths can receive different toolsets even with identical settings:

- an ordinary conversation generation may have the full toolset;
- a Task-run generation may receive a restricted subset (for example, automation or memory-read tools absent);
- MCP availability is per server and per tool;
- a Skill catalog freezes at generation start — edits made during a run are not visible until a fresh generation.

A settings screen therefore proves nothing about a specific run. An agent that assumes capabilities from any of these sources can claim actions it never performed, or perform writes it cannot inspect.

## The pattern

1. **Bootstrap detection** — at the start of every run, verify tool availability with real read-only calls, never from declarations. Distinguish "I can see the tool" from "I called the tool and observed the result".
2. **Recorded state** — keep a Capability Configuration table inside the coordinating Skill. Each row: capability, verified state, verification date. Fill it only from observed tool results. The recorded state also includes the agent's repository awareness: which reference repositories define its architecture and environment, and what role each one plays.
3. **Switch rule** — enable a capability only after practical verification (for example, a Run now test with a real tool call), never from release notes. Record the date of verification.
4. **Graceful degradation** — if a tool is missing, mark that area UNAVAILABLE, claim no actions in it, and continue with what is available. A missing tool is a fact to report, not an error to hide.

## The write-only trap

A restricted toolset can include write access without read access — for example, an Active Memory update tool present while memory-read tools are absent. An agent in this state could overwrite memory it cannot inspect.

Rule: **never write without a prior read.** If the read tool is unavailable, the write tool must be treated as unavailable too, regardless of what the settings screen says.

## Practical verification

- Use read-only operations for diagnostics (list operations, harmless reads).
- Verify a scheduled path with a Run now execution before trusting its schedule.
- After editing a Skill or memory file, verify the change in a fresh generation (the catalog and admitted context freeze at generation start).
- When read-back verification is technically impossible, state the actual verification method used (for example, a successful tool return) instead of claiming read-back verification.

## Where this is implemented

- [`skills/coordination/agora-coordinator.md`](../skills/coordination/agora-coordinator.md) — the coordinator Skill contains a Capability Configuration table and the switch rule as part of its workflow, plus a Repository Awareness section defining the two reference repositories (setup architecture and application environment).
- [`tool-execution-contract.md`](../skills/tool-execution-contract.md) — the underlying safety layer: inspect before acting, verify after acting, never claim success without evidence.

## Related documentation

- `docs/5-skills.md` — Skill discovery and the coordination family.
- `docs/8-tools-and-safety.md` — tool safety and approval gates.
- `docs/13-memory-governance.md` — memory-layer architecture and routing.
