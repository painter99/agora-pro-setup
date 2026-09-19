# Skill: Android Development — TDD and the Prove-It Pattern

## Catalog description

TDD development of Android/Kotlin app logic: red-green-refactor, the Prove-It pattern for bug fixes, test pyramid with Gradle tooling.

## Purpose

Develop Android/Kotlin app logic (parsers, repositories, fallback logic, unit conversions) tests-first. Tests are proof — "it seems to work" is not done.

## Load when

- Writing new logic (parser, repository, fallback selector, unit conversion);
- fixing a bug (use the Prove-It pattern);
- changing the behavior of existing code.

## Do not load when

- pure configuration, documentation, static content, or layouts without logic.

## Dependencies

`android-spec-first.md` (spec defines the testing strategy), `android-code-review.md` (review checks that Prove-It was followed).

## Workflow

### 1. Discover tooling FIRST (never assume)

- Build: `./gradlew` (the wrapper wins over any global Gradle).
- All tests: `./gradlew testDebugUnitTest` (or `./gradlew :app:test`).
- Single test: `./gradlew test --tests "ClassName.methodName"`.
- Before the first test, check existing conventions: where tests live, how they are named, what neighboring tests use.

### 2. TDD cycle

```
RED      -> GREEN       -> REFACTOR
test      minimum code   cleanup, tests
FAILS     to pass        still PASS
```

- **RED**: the test must fail. A test that passes immediately proves nothing.
- **GREEN**: the minimum code to break the test. Do not over-engineer.
- **REFACTOR**: clean up with green tests after every step.

### 3. Test pyramid (Kotlin/Compose)

| Level | Share | Tool | Example |
|---|---|---|---|
| Unit (pure logic) | ~80 % | JUnit + kotlin.test | text/JSON parsers, fallback logic |
| Integration | ~15 % | Robolectric / instrumented | Room DAO, Retrofit service |
| E2E/UI | ~5 % | Compose UI test | widget render, main screen |

**Priority for offline apps:** parsers and repositories are pure logic -> unit tests with fixture files under `test/resources`. NEVER call the network in tests — fixtures first.

### 4. Prove-It Pattern (bug fixes)

```
Bug report -> test reproducing the bug -> FAIL (bug confirmed)
-> fix -> test PASS -> full suite (no regressions)
```

## Beyoncé rule

"If you liked it, you should have put a test on it." If something broke and there was no test for it, that is on us — not on "infrastructure changes".

## Anti-rationalization table

| Excuse | Reality |
|---|---|
| "It's just a small change" | Small changes break things as often as large ones |
| "The test would be complicated" | A complicated test is a signal the tested code has a design problem |
| "I verified it manually" | Manual verification cannot be repeated; a test can |
| "I'll add tests later" | Later = never. RED-GREEN now |

## Verification

- New tests were observed failing (RED) before the fix, then passing (GREEN).
- The full suite passes before commit.
- Bug fixes ship together with their regression test.

## Forbidden behavior

- Committing logic without tests.
- Writing a fix before a failing test reproduces the bug.
- Calling the network in unit tests.

## Sources

v1.0 — adapted from `addyosmani/agent-skills/skills/test-driven-development` (red-green-refactor, Prove-It, test pyramid, Beyoncé rule); translated and adjusted for Kotlin/Gradle/Compose. Not a verbatim copy.
