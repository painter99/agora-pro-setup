---
name: self-improvement-loop
description: "Closed self-improvement loop for agents: retrospective → delta proposal → human GO gate → incremental patch → eval on golden tasks; anti reward-hacking rules; based on ACE, Memp, and DGM (2025–2026). Load when: after a session or task with a lesson, when proposing a change to an existing Skill, or in a weekly retrospective run."
license: MIT
---

# Skill: Self-Improvement Loop (SIL)

## Catalog description

Closed self-improvement loop for agents: retrospective → delta proposal → human GO gate → incremental patch → eval on golden tasks; anti reward-hacking rules; based on ACE, Memp, and DGM (2025–2026). Load when: after a session or task with a lesson, when proposing a change to an existing Skill, or in a weekly retrospective run.

## Purpose

Improve the agent's own scaffolding (Skills, memory files, own harness scripts) from real failures and successes — without model training, without auto-merge, with measurable verification of every change. The foundation model is never updated.

## Load when

- a session or scheduled task with a teachable outcome has finished (failures, repeated corrections, a new verified procedure);
- the operator asks for a retrospective or an improvement proposal;
- a change to an existing Skill or to the operating rules is being proposed;
- the weekly retrospective task runs.

## Do not load when

- a one-off task with nothing to learn from;
- an acute incident — apply the escalation protocol first, this loop after;
- the operator explicitly does not want changes.

## Dependencies

- `model-escalation-protocol`
- `memory-audits`
- `skill-governance.md`
- `memory-master-index`
- `memory-file-operations`
- `llm-model-evaluation.md`
- `tool-execution-contract`

## Workflow

1. **Generator** — ordinary work; failures logged per the escalation protocol.
2. **Reflector** — collect signals (escalation log, eval log, memory audits, repeated corrections, scheduled-task outputs, the observability decision log with its open recommendations and superseded chains, baseline+diff trends from the observability dashboard); output: max 3 candidate deltas, each as `| id | what | evidence | proposed patch | risk | eval plan |`. No evidence, no delta. A delta carries an ID `D-YYYYMMDD-NN`; when it realizes a decision-log recommendation `DR-YYYYMMDD-NN`, the recommendation's note is marked `realized by D-…`. Decision-log statuses are changed only by the operator — the loop reads and proposes, never closes them.
3. **GO gate** — no delta is applied without explicit operator approval; purpose changes, merges/splits, deletions, and security rules are always proposals only.
4. **Curator** — patch instead of replace; preserve details (prevents context collapse); mark deprecated passages instead of deleting; commit repo-visible changes (history = archive of variants).
5. **Eval** — golden-task subset (3–5) before and after, same model and memory context; accept only improvement without regression plus operator acceptance; budget ~10 runs per delta.
6. **Harness level (bounded)** — the agent may improve its own scripts only with tests, green CI, and a merge approval; never the app itself, MCP servers, security Skills, or model choices without explicit GO.

## Forbidden behavior

- Apply a delta without the GO gate.
- Optimize toward a proxy metric without human acceptance.
- Rewrite a whole Skill or context when a patch suffices.
- Train weights or change model choices without explicit GO.
- Hide failed evals.

## Verification

- After every applied delta: read the result back (Skill and memory), language check per the language-fidelity Skill, eval result appended to the eval log.

## Output contract

- Retrospective: table of candidate deltas + recommended order.
- After GO: report — file and patch, commit, eval scores before/after, language check result.

## Related docs

- `docs/29-self-improvement-loop.md` — SIL pattern, golden-task corpus template, autonomous repository-maintenance policy (§5).
- `docs/28-update-observability.md` — decision log and dashboard signals consumed by the Reflector; SIL KPIs in the meta-review.