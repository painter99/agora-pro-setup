# Skill: aps-upgrade

## Catalog description
Procedure for adapting a setup repository and local Skills to a released Agora version: trigger validation, changelog check, local dogfood, repo port, tag.

## Purpose
Perform the upgrade only after an official Agora release, reliably and verifiably: no speculative edits beforehand, runtime verification of new tools, synchronization of the local Skills with the repository version, and a safe merge workflow. The Skill is version-agnostic; the concrete tasks and state for one version live in an upgrade-plan Saved Memory file (`aps-vX.Y-upgrade-plan.md`).

## Load when
- an upstream watch detects a released Agora version (release/tag/APK, not only commits on master);
- the user asks to upgrade the repository or adapt Skills to a new Agora version;
- a new Agora version has just been installed on the device;
- an `aps-v*-upgrade-plan.md` file should be started, updated, or completed.

## Do not load when
- a routine watch check with no release (reporting upstream news only);
- repository changes unrelated to an Agora version;
- the question "what's new" carries no intent to upgrade.

## Dependencies
- `github-release-workflow.md` — branches, GO rules, merge, CI verification, privacy scan.
- `agora-coordinator.md` — capability gating (switch rule), runtime tool verification.
- `tool-execution-contract.md` — safety layer.
- Context (Saved Memory): the setup-repository state file (watch results, repository rules) and the current `aps-vX.Y-upgrade-plan.md`.

## Workflow
1. **Trigger validation:** confirm the version is actually released (releases page + tag + APK asset). Commits on master are not a release.
2. **Plan:** read the current `aps-vX.Y-upgrade-plan.md`. Check the official changelog against the plan and record deltas (new facts, cancelled assumptions).
3. **Local dogfood (before touching the repository):**
   - install the APK (the user's physical action);
   - verify every new tool at runtime with a real tool call; enable a capability only with the verification date (switch rule);
   - update the local Skills to the verified behavior (including the capability table in `agora-coordinator.md`);
   - use the setup for a few days: memory gate, Active Memory behavior, Compact.
4. **Repository port:** short topic branches as planned (English, anonymized). Each branch: branch → diff stat → GO → push → `--no-ff` merge → cleanup; format-check script; privacy scan. No long-lived staging branch.
5. **Wrap-up:** tag (for example `agora-2.2-compatible`), compatibility line in the README, update the watch record and the plan status (completed @ SHA).
6. **Next version:** after completion, create the next version's plan by cloning the structure; the old plan remains as history.

## Forbidden behavior
- No Skill or repository edits before an official release.
- Never enable a capability without runtime verification and a date.
- No renumbering of docs (retired numbers stay retired; new documents take the next free number).
- No copying of upstream content into the repository (link, do not duplicate).
- Do not change repository Skills without GO; push to main only through an approved merge.
- Do not delete local or repository Skills without an explicit GO for the exact scope.

## Hard limits
- Max 4 topic branches per upgrade in one run (more = split across runs).
- 1 GO per branch; merge only after the approved diff stat.
- Runtime tool verification: max 3 attempts, then report the tool as unavailable.

## Verification
- Every runtime claim has an observed tool result and a verification date.
- Every branch: diff stat before push; after merge, remote sync (`ls-remote`).
- Format-check (`skill-format.md`) passed for all changed Skills; privacy scan clean.
- The tag exists; watch record and plan updated; no dangling references.

## Output contract
- What changed in the new version (facts with changelog/commit references).
- What was runtime-verified (tool, date, result) and what was not.
- Branches performed, commits, merge SHA, and how each was verified.
- Plan status (phase, open items) and recommended next steps.

## Repository / context awareness
- The upstream Agora repository is the application environment; the app defines behavior — the app wins.
- The setup repository is this architecture and governance layer on top of the app.
- Local Skills are the dogfood instance; repository versions are English and anonymized. Order: local first, then port to the repository.