---
name: skill-mirror-check
description: "Verifies that deployed local Skills match the repository source of truth: fresh read of every Skill, diff against the repo, classified findings (content drift / expected overlay / cosmetic), report and escalation on drift."
license: MIT
---

# Skill: Skill Mirror Check

## Catalog description
Verifies that deployed local Skills match the repository source of truth: fresh read of every Skill, diff against the repo, classified findings (content drift / expected overlay / cosmetic), report and escalation on drift.

## Purpose

The repository is the source of truth for Skill texts; the local store is the deployed instance. Silent divergence between the two causes a specific failure: behavior observed on the instance gets attributed to the repository text, and the repository gets "fixed" for problems that never existed in it. This check makes divergence visible and classified before anything is edited.

## Load when

- after importing repository Skill versions into the local instance;
- when instance behavior contradicts the repository Skill text — suspect local drift first, before editing the repository;
- the weekly mirror-check task runs;
- on request ("proveď mirror check" / "verify the skill mirror").

## Do not load when

- ordinary domain work with no skill-content question;
- editing a Skill — that is skill-governance territory; this check is read-only.

## Dependencies

- `tool-execution-contract` — verification and safety layer for all tool operations.
- `skill-governance` — what counts as a Skill defect and which changes need approval.
- `shell-and-device-operations` — shell execution for the diff step.

## Expected overlays (allowed differences)

| Skill | Overlay sections (local filled, repo placeholders) | Basis |
|---|---|---|
| `agora-coordinator` | Capability Configuration table | docs/30-instance-overlay.md |
| `model-escalation-protocol` | Model stack table (§1), Static routing table (§6) | docs/30-instance-overlay.md |

A difference confined to these sections is expected, not drift. A repository file containing personal data is a privacy defect (skill-governance), never an overlay.

## Workflow

1. `list_skill_files` → the current local catalog; map every local Skill to its repository path `skills/<family>/<name>/SKILL.md`.
2. Coverage check: a local Skill without a repository counterpart, or a repository Skill without a local counterpart, is a finding.
3. For every Skill: fresh `read_skill_file`, write the returned content verbatim into `/home/agora/tmp/mirror-check/<name>.md`, and `diff` it against the repository file.
4. Classify every difference:
   - **CONTENT DRIFT** — different words or sections outside the overlay areas → blocking finding. Do not auto-fix.
   - **EXPECTED OVERLAY** — differences confined to the overlay table → OK.
   - **COSMETIC** — trailing newline at end of file, a missing/extra blank line after a heading, whitespace-only → non-blocking; list for optional normalization.
5. A difference that disappears when the read is repeated is a transcription artifact, not drift — re-read before reporting drift, and state the verification method either way.
6. Report per Skill: IDENTICAL / OVERLAY-ONLY / COSMETIC / DRIFT, with diff evidence for anything not identical.
7. On drift, determine the direction before any repair:
   - Repository clearly the newer truth (a recent repository change was never imported) → repair = re-import the repository version into the local store; this proceeds on the operator's standing authorization (2026-10-28) and is recorded in the report with diff evidence.
   - Local version genuinely newer (content that exists only locally and belongs in the repository) → do not import; propose a repository port through the standard branch workflow (GO per github-release-workflow).
   - Ambiguous direction → report the diff and wait for the operator.
   No repair is ever silent: every applied repair is recorded in the report with its evidence and authorization basis.
8. Persist the dated report under `/home/agora/logs/skill-mirror-check/` and send exactly one notification with the summary (higher priority when drift was found).

## Forbidden behavior

- Never edit, create, or delete a Skill (local or repository) as part of this check — read-only; fixes go through the skill-governance gates.
- Never classify an overlay difference as drift, or drift as overlay.
- Never claim mirror integrity for a Skill whose diff did not actually run.
- Never write personal data into the repository.

## Verification

- Every catalog Skill has a diff result — a skipped read is a finding, not a gap in the report.
- Diff evidence is quoted for every non-identical result.
- The report file exists and matches the pushed summary.

## Output contract

- Summary line: `N/N identical-or-expected, M cosmetic, K drift` + report path.
- Per-Skill table with classification.
- For drift: the exact diff, the proposed remedy, and which approval gate it needs.