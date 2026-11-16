# Provenance and scope of adaptation

Created 2026-11-14 as an English Manus derivative of `mobile-code-review`.

## Licensed source basis

- Repository: `painter99/agora-pro-setup`.
- Source: `skills/android-development/android-code-review/SKILL.md`.
- Revision recorded in the build contract: `552034846217c035ce802aad276fb826d0aaedf4`.
- The local source was read; the revision was not re-verified over the network or with Git operations.
- Preserve the upstream MIT notice; the complete license text remains unchanged in [LICENSE.txt](../LICENSE.txt).
- The upstream skill itself states that it was adapted from `addyosmani/agent-skills/skills/code-review-and-quality` (v1.0, not a verbatim copy). This is inherited provenance information; that additional source was not independently retrieved or verified.

## Project and methodological materials

Read `skill-build-contract.md`, `aipt-tdd-coding-loop-navrh.md`, `skill-creator/SKILL.md`, and its workflow/output patterns. Specific review examples and boundaries are set by these materials; do not create new project policy.

AIPT materials read 2026-11-14: `AGENTS.md`, `README.md`, `docs/principles.md`, `docs/project-status.md`, `docs/decisions/effective-index.md`, `docs/milestone-3-spec.md`, `contracts/offline-replay-v1.md`, `TODO.md`. The proposal/build contract cite revision `04772f3cdee2a0fe8e6560e8ee1799fed8ac44cb`; this build did not independently re-verify it. Each future use must verify the live state.

AIPT serves only as project context, not as a license for copied code. Do not copy its code, data, history, or complete adapter; this derivative does not change AIPT's missing license. The only stored project adapter belongs in `aipt-project-workflow/references/project-context.md`, outside this package.

## Main changes from the original

Preserve the five axes, the code-health improvement standard, the size assessment, and concrete structural remedies. Remove Android/Kotlin/Compose specifics, fixed dependencies, and the automatic merge gate. Introduce read-only review of the final snapshot without edits, test side effects, delegation, or permission acquisition; retain the single spec gate in the coding loop.

Distinguish a qualified fresh-context reviewer, an advisory checker, and `UNREVIEWED`; tie the conclusion to the complete touched-file set, diff, test evidence, and snapshot identity. Do not treat missing coverage as “clean.” For AIPT, add evidence fidelity, reproducibility, and privacy; four distinct evidence/acceptance boundaries; and exact determinism of semantic content without false byte-identity claims for the entire bundle.

Use one-way composition according to exact catalog names, without recursively running the router, hard-coded model routes, or installation-conditional paths. Do not claim import, runtime verification, product acceptance, or new permissions. The license applies to this derivative; preserve its notice upon further distribution.
