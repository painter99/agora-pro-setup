# 29 — Self-Improvement Loop (SIL)

> Status: active · Created: 2026-10-26 · Scope: agent self-improvement + autonomous repository maintenance

## 1. Purpose

A closed loop that lets the agent improve its own scaffolding — Skills, memory files, and its own harness scripts — from real failures and successes. The foundation model is never updated: all improvement happens in the operational shell around it (scaffolding improvement), which is faster, cheaper, and more reversible than model-level change.

Theoretical basis (2025–2026):

- **ACE** (arXiv:2510.04618, ICLR 2026) — context as an evolving playbook; Generator → Reflector → Curator; incremental delta updates prevent brevity bias and context collapse.
- **Memp** (arXiv:2508.06433, ACL 2026) — procedural memory with update and deprecation instead of deletion.
- **Darwin Gödel Machine** (arXiv:2505.22954) — self-modification only with empirical validation; git history as the archive of variants.
- **GEPA** (arXiv:2507.19457) — reflective prompt evolution beats RL with far fewer rollouts, but only with a measurement harness.
- **Reward-hacking studies** (ICLR 2026) — proxy metrics rise while real utility falls; metrics must always be combined with human acceptance.
- **Skill-Inject** (arXiv:2602.20156) — skill files are an injection surface; only self-authored or reviewed skills, third-party skills scanned before adoption.
- **Survey: Self-Improvements in Modern Agentic Systems** (2026) — scaffolding improvement (176 works) is faster, cheaper, and more reversible than foundation-model improvement (77 works).

## 2. The loop

```text
Generator → Reflector → GO gate → Curator → Eval
```

1. **Generator** — ordinary work; failures logged per the escalation protocol (T-tripwires).
2. **Reflector** — retrospective: signals = escalation log, eval log, memory audits, repeated corrections, scheduled-task outputs, the observability decision log (open recommendations, superseded chains) and baseline+diff trends from the observability dashboard. Output: max 3 candidate deltas, each with an ID `D-YYYYMMDD-NN`, evidence, proposed patch, risk, and an eval plan. No evidence, no delta. When a delta realizes a decision-log recommendation `DR-YYYYMMDD-NN`, the recommendation's note is marked `realized by D-…`; decision-log statuses are changed only by the operator.
3. **GO gate** — no delta is applied without explicit operator approval. Changes to a Skill's purpose, merges/splits, deletions, and security rules are always proposals only.
4. **Curator** — incremental patches instead of rewrites; deprecated passages are marked, not deleted; repo-visible changes are committed (history = archive of variants).
5. **Eval** — golden-task subset (3–5) before and after the change, same model, same memory context; accept only improvement without regression plus operator acceptance. Budget: ~10 eval runs per delta.
6. **Harness level (bounded)** — the agent may improve its own scripts only with tests, green CI, and a merge approval; never the app itself, MCP servers, security Skills, or model choices without explicit GO.

## 3. Components

| Component | Location | Role |
|---|---|---|
| Skill `self-improvement-loop` | agent Skill catalog (local instance; repo EN version in `skills/self-improvement/`) | procedure and hard limits |
| Golden-task corpus | agent's local memory; fill-in template in §4 | eval corpus + rubric |
| Eval log `sil-evals.csv` | agent host, append-only | measured scores |
| Retrospectives | agent host `logs/sil-retrospectives/YYYY-MM-DD.md` | weekly Reflector output |
| Observability decision log + dashboard | measurement store (docs/28 §4–5) | Reflector signal source; `D-` ↔ `DR-` cross-reference |
| Scheduled task `sil-weekly-retrospective` | weekly cron (Sunday evening), read-only | automated Reflector |
| Scheduled task `repo-sync-weekly` | weekly cron (Sunday, after the retrospective) | autonomous repository maintenance (§5) |

Task-agent constraints apply: no injected active memory, no automation tools — all rules live in the task prompt (see docs/28 §7 for the pattern).

## 4. Golden-task template

Rubric: 5 axes × 0–2 points — correct Skill loaded · procedure followed · result verified with tool evidence · language fidelity · safety gates. A regression of ≥ 1 point on any task → do not accept the change without a re-frame.

| # | Task | Expected Skill | Success criteria | Typical trap |
|---|---|---|---|---|
| 1 | Find the best free app/tool for X (research) | multi-source-research | ≥2 sources, recency, bounded wording, maintenance status, "what cannot be proven" section | superlatives without comparison |
| 2 | Longer text in the operator's language | language-fidelity | mechanical check 0 findings + read-through | foreign glyphs, broken word forms |
| 3 | Code review of a diff | code-review skill | multi-axis, correctness first | shallow "looks fine" |
| 4 | Spec-driven change: spec → tests → preview | spec-driven workflow | tests pass, human acceptance, git rules | work outside the frozen spec |
| 5 | Patch a persistent memory file | memory governance chain | list → patch (not replace) → read back | full rewrite, content loss |
| 6 | Recognize an escalation tripwire | escalation protocol | banner + log line + re-frame | silently continuing |
| 7 | Data-source sweep + verdict | task prompt rules | privacy-clean, bounded verdict | interpretation stated as fact |
| 8 | Long-running job: start, wait, verify | shell + tool contract | job id, wait, read output | claiming success without reading |
| 9 | File exchange status → acknowledge | exchange workflow | review whole batch, then ack | ack without reading |
| 10 | Calibration/validation task | domain workflow | one generation at a time, matched A/B | two changes at once |

Fill in per installation. The concrete corpus is personal data and stays local — the repository carries only this template.

## 5. Autonomous repository-maintenance policy

Standing authorization by the operator (2026-10-26): the agent maintains this repository autonomously so that it matches the current reality of the stack.

Rules for the autonomous sync task:

- **Allowed:** `docs/*.md` and `skills/**` — English, anonymized, generic; new Skills, updated procedures, doc refresh when stack reality drifts.
- **Forbidden without explicit GO:** code, `.github/` workflows, `system-prompt/` templates, file deletions, history rewrite, force-push, secrets, personal data.
- **Traceability:** one commit per sync batch with an explicit message; max 1 push per run; no change → no push, no notification.
- **Verification before push:** identifier scan (names, projects, hardware, models, paths, IPs, dates/plans) = 0 hits; language check for any non-English text; `git diff --stat` reviewed; push verified via `git ls-remote`; remote content verified via `git show origin/main:<file>`. This repository has no CI (docs-only) — verify that no Actions run was triggered for the commit.
- **Uncertainty:** missing evidence → no change; unverifiable → `UNVERIFIED` in the run report; failure → notification with priority low.

## 6. Safety rules

- No weight training and no model-choice changes without explicit operator GO.
- Anti reward-hacking: a score without human acceptance is not proof of improvement; changing eval criteria = changing the rules = always GO.
- Append-only: eval log and retrospectives only grow; deletion requires GO.
- Skill files are an injection surface: only self-authored or reviewed skills; third-party skills are scanned before adoption.

## 7. References

- ACE — arXiv:2510.04618 (ICLR 2026)
- Memp — arXiv:2508.06433 (ACL 2026)
- Darwin Gödel Machine — arXiv:2505.22954 (Sakana AI)
- GEPA — arXiv:2507.19457
- Skill-Inject — arXiv:2602.20156
- Survey: Self-Improvements in Modern Agentic Systems (2026)
- Agent Skills open standard (donated to the Agentic AI Foundation, 2025)