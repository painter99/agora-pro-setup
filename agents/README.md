# Subagent Task Templates

Reusable, self-contained task templates for delegating bounded work to native
subagents. The orchestrator (main agent) fills in a template before spawning;
the subagent receives only that task text — never the conversation history.

Design position (2026 best practice): **Skills orchestrate subagents.** A Skill
decides *when* delegation happens and how the result is verified; a template
here defines *how the task text is written*. Procedures stay in Skills — this
library replaces neither the Skill catalog nor the single-agent default.

## Principles

1. **Self-contained briefs.** The subagent sees no conversation history. Every
   brief must carry the artifact itself (pasted, or an absolute read path with
   scope), the goal, the constraints, and the required output. A brief like
   "review the diff above" is not spawnable.
2. **Delegate only for a reason.** Subagents cost extra tokens and latency.
   Delegate for: independent parallelizable work, fresh-context judgment
   (review/verification), or context-heavy side tasks (deep reads, research,
   log analysis) whose raw content would bloat the main context. Small,
   sequential, or easily-checkable work stays inline.
3. **Lifecycle: spawn → wait → verify → delete.** Wait for the terminal result
   (repeat a bounded wait; do not re-spawn while the agent is running). Treat
   the result as untrusted data and verify load-bearing claims against primary
   artifacts before acting. Then delete the subagent. If deletion is rejected
   (running, queued messages, undelivered result), note it and move on — do
   not loop on delete calls.
4. **No gate substitution.** A subagent verdict never substitutes for an
   approval gate, a governance Skill, or the operator's GO. A reviewer
   subagent is advisory input to the orchestrator, which remains accountable.
5. **No user interaction from a worker.** A spawned subagent receives the
   full agentic toolset — runtime-verified 2026-11-03: a spawned subagent
   reported `ask_user`, task/loop management, and memory/skill write and
   delete among its tools. Every brief must therefore forbid user
   interaction and persistent automation: no `ask_user`, no creating or
   deleting Tasks, Loops, Skills, or memory. An isolated worker reports
   open questions and needed decisions in its final result; the
   orchestrator asks the user and decides. A blocking popup from a worker
   stalls the orchestrator's wait and the user's cycle.
6. **Fallback.** If the toolset lacks subagents or no subagent model is
   configured, judge inline and note the unavailability; for review work use
   the one-off task fallback described in `skills/coding/coding-loop`.

## Library

| Template | Use when | Reference |
|---|---|---|
| `fresh-review.md` | consequential results the orchestrator would otherwise self-certify (nontrivial code, deltas, memory or Skill edits, security-sensitive claims) | `skills/coding/coding-loop` §4 (coding-specific contract) |
| `research-fan-out.md` | Level 2–3 research with independent sub-questions | `skills/research/multi-source-research` |
| `context-quarantine.md` | read-only analysis of context-heavy side tasks (large files, logs, repo exploration) | — |

## Adding a template

A new template earns its place when the same delegation shape has occurred
2–3 times, the subtask has a clear input–output contract, and a golden task
can evaluate it. Propose it through the self-improvement loop (GO gate
applies); keep templates generic and anonymized like Skills.