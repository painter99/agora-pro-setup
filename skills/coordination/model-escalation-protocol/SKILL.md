---
name: model-escalation-protocol
description: "model-escalation-protocol.md — tripwire protocol for agentic work: objective failure triggers, escalation banner, mandatory re-frame, model-switch recommendation, append-only log, and a static routing table tuned from log data."
license: MIT
---

# Skill: Model Escalation Protocol

## Catalog description

model-escalation-protocol.md — tripwire protocol for agentic work: objective failure triggers, escalation banner, mandatory re-frame, model-switch recommendation, append-only log, and a static routing table tuned from log data.

## Purpose

Shorten the time between "the model went off track" and "the user knows". Unreliable self-detection of failure is compensated by countable, objective signals visible to both the model and the user. The protocol does not make the model smarter — it prevents loops of futile attempts and enforces truthful claims about performed actions.

## Load when

- working agentically with tools (shell, files, MCP, git, CI) and the task has multiple steps;
- hitting a repeated error, a contradiction, or a user's factual correction;
- the task contains an irreversible action, a multi-file refactor, or 3+ mutually dependent unknowns;
- deciding which model suffices, or writing the escalation log.

## Do not load when

- a simple single-step query without tools;
- pure conversation or coaching without actions.

## Dependencies

- `sequential-thinking-workflow` — the re-frame method; this Skill decides when to run it.
- `tool-execution-contract` — tool-result verification rules (T4 is built on it).
- `memory-master-index` + `active-memory-authority` — T3/T5 memory writes.

## Workflow

### 1. Model stack table (template — fill in per your model stack)

| Slot | Model | Status |
|---|---|---|
| Primary (most tasks) | `<your primary model>` | |
| Conversation / specialized texts | `<your secondary model>` | |
| Hard tasks / escalation | `<your strongest model>` or **unfilled** | |

Keep this table current. Escalation recommendations must match it; if the escalation slot is unfilled, the banner says so and leaves the choice to the user.

### 2. Objective triggers

| ID | Signal | Required reaction |
|---|---|---|
| **T1** | 2+ failed tool calls of the same type/query | **Change the approach** (different query, anchor, or tool) + `sequentialthinking` min. 3 steps **before** the next attempt. Repeating an identical call is forbidden. |
| **T2** | 3+ failed rounds on the same subtask | Banner `⚠️ ESCALATION` + recommend **switching to a stronger model**; stop further attempts. |
| **T3** | User corrected a factual claim | Banner (accuracy category) + re-verify with a tool + log row. |
| **T4** | Claim of a completed action without a tool result | Forbidden. If found in your own draft: fix, replace with "not performed", banner. |
| **T5** | Contradiction between two of your claims in the same conversation | Banner, resolve explicitly (which holds and why), log. |
| **T6** | Stagnation: 4+ rounds without new evidence or reduced unknowns | `sequentialthinking` re-frame; then either a new plan or T2. |
| **T7** | **Preventive:** 3+ mutually dependent unknowns, OR an irreversible action, OR a multi-file refactor, OR money/publication/career | `sequentialthinking` **BEFORE** the first action. |
| **T8** | Scope creep (doing what the user did not ask for) | Stop, confirm the task definition, continue only after confirmation. |

### 3. Reaction ladder (always in order, not flat)

1. `sequentialthinking` re-frame (why it fails, hypotheses, what to verify more cheaply)
2. Different approach: different tool / anchor / smaller step / direct state check
3. Banner + recommendation to switch to a stronger model (see the stack table)
4. Hand back to the user with an honest status: what holds, what does not, what is needed

### 4. Banner format (exactly one block, max 4 lines)

```text
⚠️ ESCALATION [T2]
Signal: 3x the same error at <what exactly>
Tried: <a, b, c>
Recommendation: switch to a stronger model (task type: <e.g. multi-file refactor>) — escalation slot status per stack table
```

Noise rules: max 1 banner per trigger per round; never repeat a banner for the same situation; a banner is written only when a trigger condition is met. Never claim a model name as your own state (a model reliably does not know which model it is) — the recommendation says "switch to a stronger model", not "I am <model>".

### 5. Escalation log (append-only)

On every banner, append one row on the build host via shell:

```bash
mkdir -p /home/agora/logs
printf '%s,unknown-model,%s,%s,%s,"%s"\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "<task_type>" "<T-id>" "<resolved|switched|handback>" "<what>" \
  >> /home/agora/logs/escalations.csv
```

Columns: `date,model,task_type,trigger,outcome,notes`. Keep `model` as `unknown-model` unless the system prompt provides it — do not guess. Write `notes` without commas: quoted CSV still splits on commas under `awk -F,` (verified 2026-10-12, 7 fields instead of 6). The log is a dead letter box until a routing table is derived from it (below).

### 6. Static routing table (seed — tune from log data after ~2 weeks)

| Task type | Model |
|---|---|
| Research, documents, calendar, MCP routines, shell diagnostics, routine agent work | `<primary model>` |
| Multi-file coding, git/CI debugging, refactors, security-sensitive operations, irreversible actions, long horizons | `<strongest model>` or the escalation slot |
| Anything where banner T2 already fired | A stronger model than the one currently running |

### 7. Verification cadence

- After banner T1/T2: a changed approach or an explicit handback must follow — never another identical attempt.
- Confirm the log row landed: `tail -1 /home/agora/logs/escalations.csv`.
- Every ~2 weeks: aggregate by `task_type`/`trigger` (`awk -F,`) → update the routing table and record it in the model-evaluation memory.

## Forbidden behavior

- Never repeat an identical failed tool call without changing the approach.
- Never claim an action was performed without an observed tool result.
- Never overwrite the model name in your own text unless the system prompt provided it.
- Never use the banner as politeness or decoration; false alarms destroy the protocol's credibility.
- Never write escalations into Active Memory — they belong to the log and Saved Memory.

## Verification

- After banner T1/T2, the next action is a changed approach or an explicit handback.
- Log row confirmed by `tail -1` after every banner.
- Routing table updated from log aggregation at the stated cadence.

## Output contract

- On a trigger: banner in the fixed format + one log row + a justified next action from the ladder.
- At the end of a run where escalation fired: one summary line (which trigger, what outcome).