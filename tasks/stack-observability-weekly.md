# Task: weekly stack observability and deep research

> Card of a live scheduled task — **not the verbatim prompt**. Operator-specific
> details are genericized into fill-in placeholders; see the
> [task cards README](README.md).

## Purpose

A weekly closed-loop observability pass over the whole agent stack:
(a) a health and security sweep with baseline+diff and a hardening audit,
(b) Level-3 deep research on one domain from a rotation, (c) updates of the
dashboard, per-domain state, and the decision log, (d) delivery of the report
and dashboard to the operator. The system is read-only except the state
directory and delivery copies. Every recommendation is a proposal awaiting
operator approval.

## Schedule

Weekly (Tuesday night).

## State directory

`rotation-state` (next domain, completed runs), `baseline` (key/value
snapshot), `decisions` (decision log), per-domain state files, dated reports, a
rolling dashboard.

## Reads

- the deep-research framework and capability map from memory
- the research workflow Skill and the language-fidelity Skill
- the state directory itself (never re-propose what is already logged)

## Workflow

1. Pick the next domain from the rotation state.
2. Sweep the whole stack (failed units, listeners, firewall, hardening index,
   pending upgrades, disk/RAM, error journal); compare against the baseline and
   report only deviations and persistent trends; then refresh the baseline.
3. Deep research on the domain: 3–7 sub-questions (current versions vs ours,
   newer alternatives, recent advisories, concrete improvements), query
   diversification, source scoring, evidence matrix, explicit "what cannot be
   proven", bounded tool budget. Local versions are verified on the machine,
   never from memory.
4. Write the report: decision-log status first (what awaits approval, what
   closed since the last run), executive summary, key findings, sweep
   deviations and trends, evidence matrix, unprovable items, ranked
   recommendations with new decision-log IDs, source registry, methodology
   note, next domain.
5. Update the per-domain state file; rewrite the dashboard (date, next domain,
   top risks, hardening index + trend, recommendations awaiting approval,
   summary of the last report, the skills-health graph from the weekly
   retrospective, and the repo-graph snapshot from the weekly repository
   sync — both local log files; a missing file is reported as no data yet).
6. Append new decision-log entries as proposals only; never change existing
   statuses (operator-only); mark superseded chains in notes.
7. Copy the report and dashboard to the operator's delivery directory; send
   exactly one notification (high priority on security findings).

## Meta-review

Every 4th completed run adds a KPI section: run completion ratio,
decision-log status counts, realization ratio, self-improvement eval KPIs from
the local eval log, and a quality/cost review of the loop itself.

## Hard rules

- Read-only on the system except: the state directory, the two delivery copies,
  one notification. No installs, upgrades, configuration changes, restarts,
  deletion, git push, printing, e-mail, or task management.
- Decision-log statuses are changed only by the operator.
- Without web tools: sweep + dashboard only, do not advance the rotation,
  report the limitation.
- Never fabricate sources or URLs; uncertainty is marked; superlatives only
  with a direct comparison.
- The live report is written in the operator's language with a mechanical
  script-leak check before every write.
- On error, do not advance the rotation.

## Delivery and notifications

- Report + dashboard copied to the operator's delivery directory; exactly one
  notification (high priority on security findings); the delivery watcher may
  add its own neutral confirmation of the new file.

## Failure behavior

Every failed step is reported factually; nothing fails silently.

## Verification

State files updated, delivery copies present, notification count ≤ 1, rotation
advanced only on success.