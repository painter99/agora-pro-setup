# 28 — Scheduled agent loops (pattern)

> A reusable pattern for unattended, scheduled agent work that actually closes
> the loop: isolated cron-driven tasks run the same episodic agent later
> (docs/16, docs/22 §4), each task does exactly one job, state lives in files
> between runs, results are delivered where the operator already looks, and
> every recommendation ends in a decision log with an explicit human decision.
> Generic by design — personal specifics (real paths, schedules tied to a
> person's day, model choices, domain data) never belong in a public
> repository; they live in the operator's private memory and task prompts.

## 1. Purpose

The platform pattern (docs/22) makes the agent episodic: wake → act → report →
sleep. Scheduled tasks are the same agent run later, under the same kernel and
gates — not a second agent (docs/0, design decision 6). What most setups miss
is not more automation but a **closed loop**. Scheduled work fails in three
recurring ways:

- **Reports nobody receives** — artifacts land on a host the operator does not
  sit at; the value of a finding is quality × probability it reaches the
  operator × probability it gets decided.
- **Stateless runs** — every run starts from scratch, re-reports known facts,
  re-proposes already-rejected ideas, and never notices trends.
- **Recommendations without decisions** — a stream of proposals with no
  tracked outcome becomes an unread newsletter.

The pattern answers with three loops: **delivery** (artifacts reach the
operator), **memory** (runs build on their predecessors), and **decisions**
(every recommendation is tracked to an explicit human outcome).

## 2. Topology

```text
            ┌────────────────────────────────────────────┐
            │  SCHEDULER (cron-driven tasks)             │
            │  isolation rule: one task = one job        │
            └───────────────┬────────────────────────────┘
                            │ wake: same agent, same kernel
┌───────────────────────────▼────────────────────────────┐
│  TASK AGENT                                            │
│  tools: shell + structured tool layer + read-only      │
│  memory/skills; NO injected active memory →            │
│  every rule the run must follow lives in the prompt    │
└──────────┬──────────────────────────┬──────────────────┘
           │ read-only inspection     │ writes (allowlist)
┌──────────▼───────────┐   ┌──────────▼──────────────────┐
│  HOST (read-only)    │   │  STATE DIRECTORY            │
│  services, listeners,│   │  rotation state, baseline,  │
│  packages, logs,     │   │  per-domain state, decision │
│  hardening audit     │   │  log, reports, dashboard    │
└──────────┬───────────┘   └──────────┬──────────────────┘
           │                          │ deliver
┌──────────▼──────────────────────────▼──────────────────┐
│  OPERATOR                                              │
│  bounded push + exchange outbox (docs/27) + dashboard  │
│  decision: approve / reject / defer → decision log     │
└────────────────────────────────────────────────────────┘
```

Rules of the topology:

- The scheduler wakes the agent; it never runs commands itself. Every action
  is a tool call by the agent, under the same permission model (docs/17).
- The task agent is **more restricted, not less**: it has no injected active
  memory and no automation tools, so it cannot silently extend its own scope.
- The host is inspected read-only by default; writes are an explicit
  allowlist per task (§7).

## 3. Task inventory (three instances)

The pattern is validated with three coexisting tasks; each is deliberately
narrow:

| # | Task | Cadence | Job | Writes | Pushes |
|---|---|---|---|---|---|
| 1 | Domain data sweep | daily | run a deterministic sweep script over external data sources, filter by the operator's standing criteria, summarize candidates | append to its report log | ≤ 1, only when candidates exist (silence = no news) |
| 2 | Documentation upkeep | daily | compare a shared tree's actual state with its README; write only on drift; prune own backups by age | one doc + own backup dir | none |
| 3 | Deep research rotation | weekly | full-stack security sweep (baseline + diff + hardening audit) and a Level 3 research pass on one rotating domain | state directory + delivery copies | ≤ 1 (+ structural watcher push, §10) |

Anti-pattern to avoid: a single "do-everything" task. Isolated jobs stay
debuggable, budgetable, and independently mutable — one prompt change never
breaks the other two.

## 4. State directory (the memory loop)

```text
<work-root>/deep-research/
├── rotation-state.txt        # line 1: next domain number; line 2: completed-run counter
├── baseline.md               # key = value snapshot of the whole stack
├── decisions.md              # decision log with statuses (§6)
├── state/<domain>.md         # cumulative per-domain state
├── reports/YYYY-MM-DD-<domain>.md   # full weekly reports (append-only by date)
└── dashboard.md              # rolling, always current, overwritten in full
```

- **Rotation state** names the next domain and counts completed runs. It
  advances **only after a successful run**; on error it stays, so the domain
  retries next week.
- **Per-domain state** carries the operator's verified versions (with
  verification dates), known issues, the fate of past recommendations, and
  trend notes. Each run reads it first — it is the difference between a
  continuum and a series of one-off essays.
- **The dashboard** is the operator's two-minute view: update date, next
  domain, top risks, hardening-index trend, recommendations waiting for a
  decision, a three-line summary of the last report. One stable file,
  overwritten each run.
- Plain files are the right size for a single-host, few-tasks setup; heavier
  memory services are an anti-pattern at this scale (§12).

## 5. Baseline + diff sweep

A snapshot alone shows state; a diff shows **change** — which is what an
operator needs to act on.

- First run writes the baseline and marks it "first observation" (no diff).
- Every later run compares against the baseline, reports **only deviations
  and persistent trends** (e.g. "update backlog grew for the third week in a
  row"), then updates the baseline.
- The sweep covers: failed services, expected service liveness, firewall
  state, listening ports against an expected list (unknown listener =
  finding), pending updates, disk and memory, size of the exchange tree,
  backup freshness, and recent error-level journal entries.
- A **hardening audit** (e.g. Lynis) adds a measurable security number: a
  hardening index plus warning/suggestion counts, trended in the dashboard.
  The audit is a read-only inspection — allowed inside the read-only
  discipline. Implementation notes: the auditor binary may live outside the
  user's PATH (invoke it via the privileged runner consistently), and its
  report file is typically root-readable only — read it through the same
  runner. A full audit takes well under a minute on a small headless host.

## 6. The decision log (the decision loop)

```text
| ID             | Date | Domain | Recommendation | Status   | Note |
| DR-YYYYMMDD-NN | ...  | ...    | ...            | PROPOSED | ...  |
```

- Statuses: `PROPOSED / APPROVED / REJECTED / DONE`. **Only the operator
  changes statuses** — through the interactive agent, never inside a task
  run. This is the autonomy model (docs/22 §4) applied to research output:
  a task proposes; a human disposes.
- The task agent adds `PROPOSED` entries with dated IDs and may update
  **notes** only.
- **No duplicates:** before proposing, the run checks the log; a repeat
  updates the existing entry's note (e.g. "re-confirmed by this week's
  evidence") instead of adding a row.
- **Superseded-by convention:** a newer recommendation that replaces an older
  one marks the older entry's note `superseded by <new ID>` — the log stays
  readable instead of accumulating contradictory open items.
- Every report opens with the log's status: what waits for a decision, what
  closed since the last run.
- **Meta-review every Nth run** (e.g. every 4th): the system audits itself
  with KPIs — completed vs. failed/skipped runs, counts by status, the ratio
  of realized recommendations — plus a verdict on report usefulness and
  whether the rotation still makes sense. Without this section, automation
  only grows; it never prunes itself.

## 7. Read-only discipline and the write allowlist

- Default is read-only. The prompt states an **explicit write allowlist**:
  the state directory, exactly one delivery copy per artifact, the task's own
  backup directory. Everything else — installs, upgrades, configuration,
  restarts, deletions, repository pushes, printing, outbound messages — is
  forbidden in task runs.
- Destructive operations are never allowlisted; they remain level-2
  proposals for an interactive session (docs/22 §4, docs/17).
- Where deletion is part of a task (backup retention), it is a **single exact
  command** scoped by directory, file-name pattern, and age (e.g.
  `find <backup-dir> -name '<exact-pattern>' -mtime +7 -delete`) — never a
  manual clean-out an agent improvises.
- Editing a durable document inside a task run follows the transactional
  pattern (docs/22 §5): timestamped backup first, precise patch second,
  read-back verification third.

## 8. Task-agent constraints (observed platform behavior)

A scheduled task runs the same agent, but the runtime differs from an
interactive session. Verified on the current app version:

- **No injected active memory.** The task agent does not see the operator's
  always-available context. Consequence: every rule the run must follow —
  scope, allowlist, output format, language rules — lives **in the task
  prompt**, self-contained. Durable context is read explicitly from memory
  and skill files when needed.
- **No automation tools.** The task agent cannot create tasks or loops — it
  cannot reproduce or extend the automation layer by itself.
- **Read access to memory and skills** works; the memory gate (docs/20)
  applies to any attempted write.
- **Web tools may be absent** in a task context. Fallback rule: perform the
  local sweep and dashboard update, report the limitation factually, and do
  **not** advance the rotation — the domain stays due for the next run.
- The tool-call budget applies as everywhere else (docs/21): no identical
  failed retries, adjust approach after two consecutive failures of one query
  type, exhaust a query type after three rounds.

## 9. Bounded research inside the loop

The weekly research pass runs at Level 3 (docs/7, `multi-source-research`):

- 3–7 sub-questions per domain: current versions vs. the operator's;
  newer tools and procedures; security advisories for the domain's
  components; concrete improvements to the operator's setup.
- Query diversification with a mandatory counter-evidence angle; source
  scoring; an evidence matrix; an explicit "what cannot be proven" section.
- Bounded iterations (e.g. ≤ 15 searches, ≤ 10 fetches, ≤ 20 tool rounds) —
  the report states its completeness instead of pretending it.
- The operator's local versions are verified **on the host** (package
  queries, version flags), never recalled from memory.
- The run reads its domain state and the decision log first: no repeated
  proposals, trends watched, open items tracked.

## 10. Delivery and the notification budget

- **Reports** are delivered through the exchange outbox (docs/27): a new
  file there triggers the watcher's structural neutral push (count + label,
  never file names or contents).
- **The dashboard** is delivered as a stable, overwritten file — the watcher
  pushes on *added* files, not on overwrites, so the dashboard refreshes
  silently.
- **The agent's own push is bounded** (≤ 1 per run): a short summary with the
  domain, top findings, and the report path; security findings raise the
  priority. The structural watcher push is counted in the budget — design
  for a known, small number of notifications per week.
- Alert fatigue is the failure mode of every monitoring system (docs/24): a
  push that says nothing new trains the operator to ignore pushes.

## 11. Failure handling

- **No silent failures.** Every failed step is reported factually; a task run
  never pretends partial work is complete.
- **Rotation never advances on error** — the domain retries next week.
- **Backups before edits**, retention pruning by the exact command (§7).
- **Language fidelity gate** before durable writes: a mechanical non-Latin
  script self-check plus a read-back (the `language-fidelity` Skill
  generalizes the check for non-English operators; the repo's English
  version lives in `skills/communication/`).
- Task-run output is one factual sentence per run: what changed, or "no
  change" — a run that explains too much is usually hiding a failure.

## 12. Anti-patterns

- One do-everything task instead of isolated jobs (§3).
- Stateless runs: reports written from scratch each time, known facts
  re-reported, rejected ideas re-proposed.
- Recommendations without IDs and statuses — a newsletter, not a loop.
- A task run changing decision statuses or "helpfully" implementing its own
  proposals.
- Advancing the rotation on a failed or degraded run.
- Unbounded pushes; a push per artifact instead of a budget.
- Letting the research task mutate the host "while it is there" — installs
  and upgrades are level-2 proposals, never task actions.
- Heavier state machinery (databases, memory services) for a single-host,
  few-tasks setup; plain files are the right size, and the bar for new
  infrastructure is a concrete requirement (docs/22 §2).
- Duplicating official or upstream documentation instead of referencing it.

## 13. Verification

Per run:

- artifacts exist and are fresh: dashboard update date, rotation state
  advanced exactly one step, decision log row(s) added, report dated today;
- delivery copies present in the outbox; push count within budget;
- the host shows **no unexpected mutations** — the mutation journal
  (docs/22 §5) records nothing from task runs.

Per period (meta-review):

- KPIs from §6; hardening-index trend; report usefulness verdict; rotation
  still matches the operator's actual stack.

## 14. Version coupling

The pattern depends only on stable capabilities: task scheduling with cron
semantics, shell and structured-tool access inside task runs, read-only
memory/skill access, the notification layer (docs/24), the exchange outbox
(docs/27), and an optional hardening auditor. On each major upstream release,
re-validate: the task agent's tool surface and injected context (§8 —
especially whether active memory becomes injected and whether automation
tools appear), prompt size limits for tasks, and the watcher's
added-vs-overwritten push semantics (§10).