---
name: prd-writing
description: "Creation and maintenance of a Product Requirements Document for a product, app, or major feature: goals with success metrics, binding non-goals, user stories, requirements with fact status, milestones with acceptance criteria, decision log, and versioning."
license: MIT
---

# Skill: PRD writing

## Catalog description
Creation and maintenance of a Product Requirements Document for a product, app, or major feature: goals with success metrics, binding non-goals, user stories, requirements with fact status, milestones with acceptance criteria, decision log, and versioning.

## Purpose
Own the product level of truth: what is being built, for whom, what is excluded, which milestones lead there, and how completion is recognized. The PRD governs scope and acceptance; implementation follows it, not the other way around.

Origin: ported from the Manus skill `prd-writing` (2026-11-15), which itself derives from the PRD template distilled from three real PRDs (a weather-station widget app, an audio analysis app, and a job-search app). The Manus original ships `scripts/prd_check.py`; that script was deliberately NOT ported (platform-specific control mechanism) — the manual Quality gate below replaces it.

## Load when
- a new product, app, or major feature is being specified;
- an existing PRD is adopted, updated, versioned, or extended with a milestone or scope change;
- an executor handover is being prepared;
- a PRD is audited against this standard.

## Do not load when
- a small fix or single increment needs only a change card (`coding-loop` spec gate);
- the task is documentation without product scope;
- translating or formatting.

## Dependencies
- `context-management` — the handover distillate travels as a worker brief.
- `skill-governance` — changes to this Skill itself go through governance.

## Workflow
1. **Gather inputs.** Product, audience, platform, existing documents, non-goals. Ask only about choices that change scope, audience, or external effect.
2. **Verify facts.** Only live-verified facts belong in the PRD — URL fetched, measurement taken, behavior observed. Mark `LIVE-VERIFIED YYYY-MM-DD`; everything else is an `ASSUMPTION` and goes to open questions if it affects scope.
3. **Write the draft** from the Template below, version `v0.1`, status `draft`. Requirements in tables, not prose.
4. **Check** against the Quality gate below; fix or name the gap in open questions.
5. **GO gate.** Request explicit approval and record it in the decision log with date and source. The approval covers the document, not implementation.
6. **Maintain as a living document.** At every milestone update status, evidence, and changelog. A scope or non-goals change means a new version, never a silent edit.
7. **Hand over** to an executor via `context-management` using the Handover distillate below — never the full PRD.

## Three authority tiers

| Tier | Owner | May | May not |
|---|---|---|---|
| PRD | user as product owner | change scope, non-goals, milestones; version | authorize implementation |
| Change card | `coding-loop` via its spec gate | translate the current milestone into one increment | change PRD non-goals or scope |
| Implementation | executor | perform the approved increment | decide about the product |

A PRD GO approves the document and direction. An implementation GO is issued by the coding loop for a specific increment. Confusing the two is the most common PRD failure.

A milestone closes only with evidence: review or merge hash, test count and result, acceptance reference. A "done" claim without proof stays IN PROGRESS.

The PRD does not live in chat. It is a file in the project — default `PRD.md` at the root, else per project convention (`docs/prd.md`). One product, one file. It may exist before the first line of code.

## Forbidden behavior
- Never treat a PRD GO as implementation authorization.
- Never change scope or non-goals without a version bump and changelog entry.
- Never write unverified facts as certain; mark `LIVE-VERIFIED` vs `ASSUMPTION`.
- Never hand over the full PRD history or decision log to an executor agent.
- Never leave a template section empty; write "Not relevant for this version" with a reason.

## Verification
- Re-read the saved PRD file after writing; header version matches the changelog.
- The Quality gate passes before any GO request.
- Milestone closure carries evidence (merge hash, test count and result, acceptance reference); otherwise status stays IN PROGRESS.

## Output contract
- The PRD file (or the draft in the reply when writing is not yet authorized).
- Decision log entries with date and source; open questions with statuses.
- A handover distillate when an executor is briefed.

## Template

```markdown
# PRD: <product name>
Version: v0.1 | Date: YYYY-MM-DD | Status: draft | Author: <name> | Platform: <...> | Repo: <link or "outside Git">

## 1. Executive Summary
Value proposition: <what it does that nothing else does>. Scope of v0.1: <one to three sentences>.

## 2. Goals
| ID | Goal | Success metric |
|----|------|----------------|
| G1 | <...> | <measurable value and how it is measured> |

## 3. Non-goals (binding)
| ID | Excluded | Reason |
|----|----------|--------|
| N1 | <what does not exist in this version> | <why> |

## 4. Personas
| Persona | Need | Share | Context |
|---------|------|-------|---------|
| <...> | <...> | <% or "only"> | <...> |

## 5. User stories
| ID | Priority | Story | Phase |
|----|----------|-------|-------|
| US-001 | Must | As <who> I want <what> so that <why> | M1 |

## 6. Functional requirements
| ID | Description | Verification | Fact status |
|----|-------------|--------------|-------------|
| F1 | <...> | <how it is verified> | LIVE-VERIFIED YYYY-MM-DD / ASSUMPTION |

## 7. Non-functional requirements
| ID | Area | Target (measurable) |
|----|------|----------------------|
| NF1 | performance | <e.g., first useful result ≤ 2 s on reference device> |

## 8. Architecture and stack
<diagram or component list; data model; decisions the implementer must not bypass>

> ⚠️ Do not use <X>: <reason> (verified YYYY-MM-DD)

## 9. Phases and milestones
- M1.1 — <acceptance criterion> [ ] — status: OPEN

## 10. Release and versioning
<SemVer rule; what the first functional release means>

## 11. Risks
| ID | Risk | P | I | Mitigation |
|----|------|---|---|------------|
| R1 | <...> | medium | high | <...> |

## 12. Open questions
| ID | Question | Status |
|----|----------|--------|
| Q1 | <...> | OPEN |

## 13. Decision log
| Date | Decision | Source |
|------|----------|--------|

## Changes
- v0.1 — YYYY-MM-DD — first draft
```

## Writing rules
- Requirements in tables; every goal has a measurable success metric ("better UX" is not a metric).
- Priorities Must / Should / Could; acceptance criteria objectively checkable (yes/no, number, threshold).
- Non-goals are more binding than goals — each exclusion has a reason.
- Every risk has probability, impact, mitigation; every open question has status and date; every decision has date and source.
- Identifiers and code names in English.
- Mark facts: "live-verified on X" or "assumption".
- Normative decisions are recorded inline in the affected section AND in the decision log.

## Quality gate (manual — replaces the unported Manus script)
Before GO: header version matches changelog; all sections present or explicitly marked "Not relevant"; no duplicate IDs (G/N/US/F/NF/M/Q/R); no placeholder text left; every goal has a metric; every acceptance criterion checkable; open questions have statuses; decision log entries have dates and sources.

## Handover distillate for an executor agent
Extract only: Executive Summary; Personas; Goals; Non-goals; User stories; Functional + non-functional requirements; acceptance criteria of the current phase; OPEN questions only. Do NOT hand over history or the decision log.

## Anti-patterns
1. Goals without a success metric.
2. Vague acceptance criteria ("works fast").
3. Missing non-goals.
4. Scope change without a version bump.
5. Unverified facts written as certain.
6. Decisions without date or source.
7. A frozen PRD that never updates.
8. Unlabeled implementation detail inside the PRD.
9. Implementation without the GO gate.
10. Open questions without status.
