# ADR-0018: Worker capability scope lives in the brief until the runtime provides per-spawn scoping

- Status: accepted (2026-11-05, operator GO)
- Supersedes: none

## Context

Subagents in the application (verified in source, tag v2.2.0) receive a
fixed toolset: only `agent_*` tools and conversation recall are
runtime-excluded from a worker run; `ask_user`, task/loop management, and
memory/skill writes are inherited from the parent context. `agent_spawn`
takes only `name`, `model_id`, and `task` — no per-spawn tool or skill
scoping exists. Workers do receive the skill catalog in their context
whenever `access_skills` is on, and skill read/write access is governed by
global toggles only.

Orchestrator–worker patterns therefore cannot rely on runtime enforcement
for anything beyond delegation and recall isolation. Mainstream frameworks
implement the missing layer as per-agent configuration over a shared store:
the Claude Agent SDK subagent definition carries per-agent tools, a skill
preload list, and a memory-source selector; the OpenAI Agents SDK packages
model, instructions, and tools per agent. None implements a separate skill
namespace for workers.

## Decision

- Worker capability scoping lives in the **brief**: every subagent brief
  declares its skill scope (default none), forbids user interaction and
  persistent automation, and defines the output contract (agents/ README
  principles 5 and 7).
- The **shared skill catalog stays the single source of truth**; workers get
  scoped access to it through the brief, never a separate worker namespace.
- Skill write tools are forbidden to workers regardless of future runtime
  capabilities; the instruction layer is governed in the main thread.
- Escalation of worker questions to the user belongs to the orchestrator
  (routed-question pattern proposed upstream); approval gates always
  escalate to the operator.

## Consequences

- Brief-level enforcement is prompt-level: probable, not guaranteed (the
  same trade as ADR-0004). Runtime-verified boundaries (no `agent_*`, no
  conversation recall for workers) do not depend on it.
- When the runtime gains per-spawn scoping, the brief's skill list maps 1:1
  to the runtime parameter; templates need no structural change.
- No second catalog exists to drift; the mirror check continues to cover
  the shared catalog.
