# Skill: Android Spec-First Development

## Catalog description

Spec-first development for Android/Kotlin apps: PRD as source of truth, gated workflow with human validation, scope-creep defense.

## Purpose

No code without an approved specification. The spec (PRD) is the shared source of truth between the human validator and the AI implementer. Code without a spec is guessing.

## Load when

- New project, new feature, or significant change is requested;
- requirements are unclear, ambiguous, or a rough idea;
- a change spans more than one file;
- implementation would take more than 30 minutes.

## Do not load when

- one-line fixes, typos, or changes with unambiguous requirements.

## Dependencies

`android-dev-tdd.md` (testing strategy comes from the spec), `android-code-review.md` (spec = correctness yardstick).

## Workflow

### Gated phases

```
SPECIFY -> PLAN -> TASKS -> IMPLEMENT
   |         |        |         |
   v         v        v         v
 human approval at every gate
```

**Never advance to the next phase without human validation.**

### Phase 0: Scope check

One request = one capability? Go straight to SPECIFY. Multiple capabilities? Build a **capability map** first:

```markdown
| Module id      | Responsibility            | Depends on |
|----------------|---------------------------|------------|
| data-source-a  | parser for source A       | -          |
| data-source-b  | client for source B       | -          |
| fallback       | primary-source selection  | data-*     |
| widget         | home-screen widget        | fallback   |
```

- Kebab-case IDs; do not rename mid-project.
- Arrows point one way; no cycles (a cycle collapses into one module).

### Phase 1: SPECIFY

1. **State assumptions UP FRONT, before writing the spec:**

```
ASSUMPTIONS:
1. Phase 1 = personal APK, no Play Store
2. min SDK 26, target 35+
3. UI language: user's locale
-> Correct me now, or I will proceed on this basis.
```

Never fill in ambiguous requirements silently. An unstated assumption is the most dangerous form of misunderstanding.

2. The spec must cover six areas:
   - **Objective** — what, why, who the user is, what success looks like (acceptance criteria!).
   - **Commands** — full runnable commands (`./gradlew assembleDebug`, `./gradlew testDebugUnitTest`), not just tool names.
   - **Project structure** — where source, tests, and fixtures live.
   - **Code style** — one real Kotlin snippet beats three paragraphs of prose.
   - **Testing strategy** — framework, test locations, which level covers which concern (see `android-dev-tdd.md`).
   - **Boundaries** (three layers):
     - **Always:** tests before commit, naming conventions, validate inputs at the system boundary.
     - **Ask first:** Room schema change, new dependency, build config change.
     - **Never:** secrets in the repo, deleting failing tests without approval, scope creep beyond the approved PRD.

### Phase 2: PLAN and Phase 3: TASKS

Break the work into small, verifiable tasks with acceptance criteria and dependencies. Each task: one thing, testable, committable.

### Phase 4: IMPLEMENT

One task at a time, TDD (`android-dev-tdd.md`), review after each (`android-code-review.md`).

## Scope-creep defense

A new capability outside the approved spec = **a new spec version**, not "a small addition". Non-goals are binding.

## Anti-rationalization table

| Excuse | Reality |
|---|---|
| "It's obvious, we don't need a spec" | What is obvious to the AI is not obvious to the human — and vice versa |
| "I'll fill in details during implementation" | A detail added in flight is an unapproved decision |
| "It's just a small extra feature" | A small extra feature is scope creep |
| "The human won't review it anyway" | The human is the validator; without them the spec is not approved |

## Verification

- Each gate has explicit human approval recorded.
- Implementation tasks map 1:1 to approved tasks.
- No changes outside spec scope without a new spec version.

## Forbidden behavior

- Writing feature code before the spec is approved.
- Silently resolving ambiguity with assumptions.
- Deleting failing tests or expanding scope without approval.

## Sources

v1.0 — adapted from `addyosmani/agent-skills/skills/spec-driven-development` (gated workflow, capability map, assumptions-first, six spec areas, boundaries); translated and adjusted for a Kotlin/Gradle/Compose workflow. Not a verbatim copy.
