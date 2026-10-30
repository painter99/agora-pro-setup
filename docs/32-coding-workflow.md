# docs/32 — Coding workflow

The coding layer of this setup: how the agent writes and verifies code, how the
work is measured, and where the resulting scripts live. The operator sets the
frame and verifies; the agent implements. No autonomous fix loops and no
auto-merge — every layer here is human-gated (ADR-0016).

## Components

| Component | Where | Role |
|---|---|---|
| Coding loop | Skill `coding-loop` | goal-based loop: spec gate → small increments → tests → second-agent review → bounded fix rounds → acceptance against reality |
| Eval corpus | instance golden tasks | coding golden tasks (script from spec, bugfix with reproduction, behavior-preserving refactor) scored on the SIL scale |
| Scripts repository | private instance repo | versioned mirror of personal scripts; live paths keep running, the repo holds history |
| Rule encoding | `docs/29` | recurring fix patterns and review comments become Skill deltas through the self-improvement loop |

## The loop in practice

1. **Spec gate.** The task states inputs, outputs, constraints, and an
   observable "done". No spec, no code.
2. **Small increments.** One increment is one verifiable step; large
   single-shot changes need an explicit reason (the reward-hacking gap grows
   with change size).
3. **Tests as reviewable artifacts.** The test report is evidence; assertions
   are never weakened to force a pass; test-suite or CI edits require
   justification and approval.
4. **Second-agent review.** Non-trivial diffs are reviewed in a fresh context
   (a new conversation or a task agent) that sees the spec and the diff, not
   the implementation reasoning.
5. **Bounded fix rounds.** Two consecutive failed rounds on one problem →
   change the approach; three → honest report and handback (tool-call budget,
   `docs/21`).
6. **Acceptance against reality.** The final gate is the observable result on
   real input (or a faithful copy), shown to the operator. "Tests green" alone
   is never done.

## Scripts repository (versioning pattern)

Personal (non-employer) scripts live in a private repository that mirrors the
live paths:

- Live scripts stay on their working paths (timers and tasks keep running);
  the repository is the versioning source of truth.
- Change procedure: edit the live file → copy into the repo → byte-compare
  (`cmp`) → commit → push. The agent commits on every change it makes.
- Excluded by design: employer code (goes to the employer's system only),
  projects with their own repositories, `.bak` backups (git history replaces
  them), secrets and tokens, data and reports.
- Secret scan before every push (token/password/secret/api-key/bearer
  patterns); findings are reviewed manually.

## Testing policy

Copy verification (`cmp`) proves the repository matches the live file; it does
not prove the script works. Each script is tested according to its effect
class:

| Effect class | Examples | Test |
|---|---|---|
| Read-only, no side effects | holiday check, source availability test | run directly; record exit code and output |
| Read-only with notifications | health check | run via `bash`; expect the alert path to fire |
| Sends notifications or mutates state | morning brief, calendar reminders, exchange watcher, daily data sweep | do not run casually; test on a copy or in dry-run when a change is made (script safety gate in `process-design`) |
| Heavy local models | transcription, TTS | not tested casually; exercised by their own workflows |

Test evidence belongs in the commit message or the change report.

## Boundaries

- The loop is human-gated: no autonomous fix iterations past the budget, no
  auto-merge, no unattended pushes to shared branches.
- Employer code never enters personal repositories (standing rule).
- Golden tasks and instance-specific values stay in the instance layer
  (`docs/30`); the repository documents the pattern.

## Related

- `docs/29` — self-improvement loop (rule encoding)
- `docs/28` — measuring scheduled agent work
- `docs/21` — tool-call budget (fix-round cap)
- `docs/30` — instance overlay (golden tasks, scripts repo)
- `docs/26` — domain workflow example: spec-driven CAD