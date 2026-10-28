# 28 — Stack update observability (pattern)

> A reusable pattern for keeping a personal agent stack observable: how
> current, patched, hardened, and stable it is; what drifts; and what the
> surrounding ecosystem offers next — measured on a schedule, diffed against
> a baseline, delivered to the operator, and closed by explicit decisions.
> The vehicle — scheduled tasks — is a capability of the agent application
> itself and is documented in the application's official manual; this
> repository does not duplicate it (see the duplication rule in the README).
> Generic by design — personal specifics (real paths, schedules, model
> choices, domain data) never belong in a public repository. A validated
> working instance with day-zero measurements is shown in §8.

## 1. Purpose

The platform pattern (docs/22) makes the agent episodic: wake → act → report →
sleep. An episodic agent sees nothing between wake-ups, so the state of the
stack is whatever the last observation said. The question this pattern
answers continuously is:

> How current, patched, hardened, and stable is the stack — and what should
> change next?

"Update observability" is deliberately broader than patch monitoring. Five
dimensions are measured (§2): currency, patch state, hardening, drift, and
ecosystem movement. And measurement alone is not observability — a number
nobody receives and a recommendation nobody decides are noise. The pattern
therefore closes three loops:

- **Delivery loop** — artifacts land where the operator already looks
  (exchange outbox, docs/27; notification layer, docs/24) plus a rolling
  dashboard.
- **Memory loop** — every run reads what its predecessors wrote and builds on
  it; trends become visible instead of being re-measured from scratch.
- **Decision loop** — every recommendation gets an identity and a tracked
  outcome; the operator's decision is the only thing that closes it.

The vehicle: scheduled tasks run the same episodic agent later, under the
same kernel and gates — not a second agent (docs/0, design decision 6).
Their configuration belongs to the application's official documentation;
§7 lists only the constraints this pattern itself adds.

## 2. What is observed (the measured inventory)

| Dimension | Metric | Source | Cadence |
|---|---|---|---|
| Currency | versions of core components vs. upstream latest | package/version queries on the host; upstream release feeds | weekly |
| Patch state | pending updates (total + security-origin subset) | package-manager simulation on the host | weekly |
| Hardening | audit index + warning/suggestion counts (e.g. Lynis) | read-only hardening audit | weekly |
| Drift | listening ports vs. expected list; service liveness vs. expected set; firewall state; disk/memory; handover-tree size | host inspection | weekly (the health check bridges the gaps — docs/24) |
| Ecosystem movement | new versions, tools, procedures, advisories per domain | bounded Level 3 research (docs/7) | weekly, one domain per run (rotation) |
| Delivery freshness | backup ages, dashboard update date | state directory | weekly |

Why each dimension earns its weekly cost:

- **Currency** — an unpatched known vulnerability is the cheapest attack on
  the stack; falling behind upstream also makes every future upgrade
  costlier.
- **Patch state** — security-origin updates are the time-critical subset; a
  growing backlog is a trend to catch early, not an event.
- **Hardening** — one comparable number per week turns security posture from
  a feeling into a trend; warnings are the actionable subset, suggestions
  the backlog.
- **Drift** — silent configuration change is how outages and exposures
  happen; the expected-state comparison turns "something changed" into a
  finding with severity.
- **Ecosystem movement** — a self-hosted stack does not rot by breaking but
  by falling behind; the research leg is the only defense against doing
  things the way they were done years ago.
- **Delivery freshness** — observability that is not delivered is invisible;
  stale backups or a stale dashboard mean the loop itself is degrading.

The research leg runs at Level 3 (docs/7); the full procedure — query
diversification with counter-evidence, source scoring, the evidence matrix,
bounded iterations, and the mandatory "what cannot be proven" section —
lives in the `multi-source-research` Skill
(`skills/research/multi-source-research/SKILL.md`), which the weekly run reads
before researching. Referencing the Skill here keeps the chain complete:
this document says *what* is observed and *why*, docs/7 defines the levels,
and the Skill carries the procedure.

Design rule: every metric is either **measured on the host** (never recalled
from memory) or **sourced with citations** (research leg). A metric that
cannot be measured or sourced honestly is dropped, not estimated.

## 3. Baseline + diff discipline

A snapshot shows state; a diff shows change — and change is what an operator
acts on.

- The first run writes a baseline (`key = value` form) and marks it "first
  observation"; no diff is claimed.
- Every later run compares against the baseline, reports **only deviations
  and persistent trends** ("update backlog grew for the third week in a
  row"), then updates the baseline.
- Slow drift — a growing backlog, shrinking disk, a new listener — surfaces
  as a trend long before it becomes an incident.
- The hardening audit adds a measurable security number: an index plus
  warning/suggestion counts, trended in the dashboard. The audit is a
  read-only inspection. Implementation notes: the auditor binary may live
  outside the user's PATH (invoke it consistently through the privileged
  runner) and its report file is typically root-readable only; a full audit
  takes well under a minute on a small headless host.

## 4. The measurement store (state directory)

```text
<work-root>/deep-research/
├── rotation-state.txt        # line 1: next domain; line 2: completed-run counter
├── baseline.md               # key = value snapshot of the whole stack
├── decisions.md              # decision log with statuses (§5)
├── state/<domain>.md         # cumulative per-domain state
├── reports/YYYY-MM-DD-<domain>.md   # full reports, append-only by date
└── dashboard.md              # rolling, always current, overwritten in full
```

- **Rotation state** advances only after a successful run; on error it stays
  and the domain retries next time.
- **Per-domain state** carries verified versions (with verification dates),
  known issues, the fate of past recommendations, and trend notes.
- **The dashboard** is the operator's two-minute view: update date, next
  domain, top risks, hardening-index trend, recommendations awaiting a
  decision, a three-line summary of the last report.
- Plain files are the right size for a single-host, few-tasks setup; heavier
  state machinery is an anti-pattern at this scale (§10).

## 5. The decision log (closing the loop)

```text
| ID             | Date | Domain | Recommendation | Status   | Note |
| DR-YYYYMMDD-NN | ...  | ...    | ...            | PROPOSED | ...  |
```

- Statuses: `PROPOSED / APPROVED / REJECTED / DONE`. **Only the operator
  changes them** — through the interactive agent, never inside an unattended
  run (autonomy model, docs/22 §4; permission model, docs/17).
- The unattended run adds `PROPOSED` entries with dated IDs and may update
  **notes** only.
- **No duplicates:** before proposing, the run checks the log; a repeat
  updates the existing note ("re-confirmed by this week's evidence") instead
  of adding a row.
- **Superseded-by convention:** a newer recommendation that replaces an older
  one marks the older note `superseded by <new ID>` — the log stays readable
  instead of accumulating contradictory open items.
- Every report opens with the log's status: what awaits a decision, what
  closed since the last run.
- **Meta-review every Nth run** (e.g. every 4th): the observer observes
  itself — completed vs. failed/skipped runs, counts by status, the ratio of
  realized recommendations, plus a verdict on report usefulness and whether
  the rotation still matches the operator's actual stack. Without this,
  automation only grows; it never prunes itself.

## 6. Delivery and the notification budget

- **Reports** go through the exchange outbox (docs/27); a new file there
  triggers the watcher's structural neutral push (count + label, never file
  names or contents).
- **The dashboard** is delivered as a stable, overwritten file — the watcher
  pushes on *added* files, not overwrites, so it refreshes silently.
- **The agent's own push is bounded** (≤ 1 per run): domain, top findings,
  report path; security findings raise the priority. The structural watcher
  push counts toward the budget — design for a known, small number of
  notifications per week.
- Alert fatigue is the failure mode of every monitoring system (docs/24): a
  push that says nothing new trains the operator to ignore pushes.
- **Run metadata** — each report records its duration, token usage where the
  application exposes it, and failed or skipped steps. The meta-review reads
  failure counts as a lite error budget: two failed runs of the same task
  within a rolling month trigger a review of the task itself, not just
  another retry of its domain.

## 7. The vehicle: constraints this pattern adds

Scheduled tasks are an application capability — their mechanics belong to the
official documentation and are not duplicated here. What the pattern itself
contributes on top:

- **One task = one job.** Isolated, independently mutable jobs (a daily data
  sweep, a daily documentation upkeep, a weekly research rotation) instead of
  a do-everything task.
- **Read-only default with an explicit write allowlist** per task: the state
  directory, exactly one delivery copy per artifact, the task's own backup
  directory. Installs, upgrades, configuration, restarts, deletions,
  repository pushes, printing, outbound messages — never in an unattended
  run. Deletion where genuinely needed (backup retention) is a single exact
  command scoped by directory, name pattern, and age.
- **Rules live in the prompt.** An unattended run receives no injected
  active memory (observed behavior, version-dependent — §12): every rule the
  run must follow is stated in the task prompt, self-contained; durable
  context is read explicitly from memory and skill files. The memory gate
  (docs/20) still applies to any attempted write.
- **Capability fallback.** If web tools are unavailable in the run context,
  the run performs the local sweep and dashboard update, reports the
  limitation, and does **not** advance the rotation.
- **Tool budget applies** as everywhere (docs/21).
- **Instance documentation.** The live tasks that run this pattern are
  documented as genericized task cards in [`tasks/`](../tasks/README.md) —
  cards, not verbatim prompts; operator-specific details stay out of the
  repository.

## 8. A working instance (validated)

The pattern runs on a single-host setup with three coexisting tasks (§7):
a daily external-data sweep, a daily documentation upkeep, and a weekly
research rotation over ten domains. The measurement store as deployed:

```text
<work-root>/deep-research/
├── rotation-state.txt        # "1" / "0" — ten domains queued, none completed
├── decisions.md              # seeded with the operator's founding decisions
├── state/  reports/          # filled by the first runs
└── dashboard.md              # written by the first run
```

Day-zero measurement (single headless host):

| Metric | Day-zero value | Reading |
|---|---|---|
| Hardening audit (read-only) | index 65 · 0 warnings · 49 suggestions | ~23 s wall time — the weekly security-trend leg costs less than half a minute; suggestions are the improvement backlog the loop works through |

The decision log as seeded — founding decisions with outcomes, including an
honest rejection:

```text
| DR-20261026-01 | platform/sweep | adopt the hardening audit into the weekly sweep | DONE     | installed and verified same day |
| DR-20261026-02 | meta-review    | KPIs in the periodic meta-review                | DONE     | part of the weekly prompt |
| DR-20261026-03 | decision log   | superseded-by convention                        | DONE     | part of the weekly prompt |
| DR-20261026-04 | agent memory   | heavier memory services (vector store)          | REJECTED | file state suffices at this scale; revisit at ~10 tasks |
```

And the dashboard skeleton the first run produces:

```text
# Stack observability — dashboard (YYYY-MM-DD)
Next domain: 1 — platform/OS
Top risks: (from the last sweep)
Hardening index: 65 — trend: first observation
Awaiting decision: —
Last report: <path> — three-line summary
```

## 9. Failure handling

- **No silent failures** — every failed step is reported factually; partial
  work is never presented as complete.
- **Rotation never advances on error.**
- **Backups before edits** of any durable document; read-back verification
  after (transactional pattern, docs/22 §5).
- **Language fidelity gate** before durable writes: a mechanical non-Latin
  script self-check plus a read-back
  (`skills/communication/language-fidelity/SKILL.md`).
- Run output is one factual sentence: what changed, or "no change".

## 10. Anti-patterns

- Monitoring without delivery: measurements that stay on the host.
- Stateless runs: re-measured facts, re-proposed rejected ideas, invisible
  trends.
- Recommendations without IDs and statuses — a newsletter, not a loop.
- An unattended run changing decision statuses or implementing its own
  proposals.
- Advancing the rotation on a failed or degraded run.
- Unbounded pushes; alert fatigue.
- Letting the observation task mutate the host "while it is there".
- Duplicating the application's own task/scheduling documentation instead of
  referencing it (the repository's duplication rule).
- Heavier state machinery (databases, memory services) for a single-host,
  few-tasks setup.

## 11. Verification

Per run:

- artifacts exist and are fresh: dashboard date, rotation advanced exactly
  one step, decision log row(s) added, report dated today;
- delivery copies present in the outbox; push count within budget;
- the host shows **no unexpected mutations** — the mutation journal
  (docs/22 §5) records nothing from observation runs.

Per period (meta-review):

- KPIs from §5; hardening-index trend; report usefulness verdict; rotation
  still matches the actual stack; where a self-improvement loop exists
  (docs/29), also its eval KPIs (run count, average score, regressions),
  read-only from the SIL eval log;
- task-run failure rate as a lite error budget (§6): a rising trend triggers
  a review of the task itself, not just another retry of its domain.

## 12. Version coupling

The pattern depends only on stable capabilities: scheduled execution of the
same agent (cron semantics), shell and structured-tool access in unattended
runs, read-only memory/skill access, the notification layer (docs/24), the
exchange outbox (docs/27), and an optional hardening auditor. On each major
upstream release, re-validate: the unattended run's tool surface and injected
context (§7 — especially whether active memory becomes injected), prompt size
limits, and the watcher's added-vs-overwritten push semantics (§6).