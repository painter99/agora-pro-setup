# Provenance — mobile-spec-first

## Origin and license

English methodological derivative of the Agora skill `android-spec-first`. Source read: `skills/android-development/android-spec-first/SKILL.md` in the `agora-pro-setup` repository, revision per the build contract `552034846217c035ce802aad276fb826d0aaedf4`; read date 2026-11-14. Preserve the upstream MIT notice; [LICENSE.txt](../LICENSE.txt) is an unchanged copy of the Agora repository license.

The original skill states v1.0 and a methodological adaptation from `addyosmani/agent-skills/skills/spec-driven-development`. This is information inherited from its Sources section, not external verification performed here or direct copying from that additional upstream source.

## Adaptation differences

Preserve assumptions-first, the six specification areas, observable acceptance criteria, and protection of non-goals. Replace Android/Kotlin/Gradle specifics with a general method derived from the current project. Add a short card for unambiguous changes, a direct spec-only path, distinction between readiness and authorization, and task-local loading of live materials without a recursive router.

Remove its own IMPLEMENT phases and four approval gates, automatic routing to Android TDD/review, and implicit consent by silence. Leave the single spec gate to `mobile-coding-loop`; this skill provides the contract shape and does not take over control, implementation, or permissions. Distinguish software evidence, semantic support, and operator acceptance.

## Project material and limitations

Read the local `aipt-tdd-coding-loop-navrh.md` proposal and the complete `skill-build-contract.md` from the `agora-manus-adaptation` directory, as well as the live AIPT `AGENTS.md`, `README.md`, `docs/principles.md`, `docs/project-status.md`, `docs/decisions/effective-index.md`, `docs/milestone-3-spec.md`, `contracts/offline-replay-v1.md`, and `TODO.md`; read on 2026-11-14. The context proposal and build contract cite AIPT revision `04772f3cdee2a0fe8e6560e8ee1799fed8ac44cb`; this is not a newly verified remote state here.

AIPT serves only as project material for requirements and an acceptance-criteria example. Do not copy its code or data; this derivative's MIT license does not license AIPT or change its missing license. Do not retain a project snapshot here: the only stored adapter belongs in `aipt-project-workflow/references/project-context.md`; always verify relevant live sources when using it.

Use `skill-creator` and its workflow/output-patterns for initialization, structure, and output. Distinguish structural checking from use of the skill; design scenarios in SKILL.md remain **NOT PERFORMED**. Do not claim import, installation, runtime correctness, or AIPT implementation performed.
