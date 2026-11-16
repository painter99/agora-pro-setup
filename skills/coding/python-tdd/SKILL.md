---
name: python-tdd
description: "Test-driven development for Python logic with stdlib unittest: RED-GREEN-REFACTOR for new behavior, the Prove-It pattern for bug fixes, characterization testing before refactoring. Hermetic fixture discipline, assertion selection by contract invariants, concrete test evidence, and bounded fix rounds."
license: MIT
---

# Skill: Python TDD

## Catalog description

Test-driven development for Python logic with stdlib unittest: RED-GREEN-REFACTOR for new behavior, the Prove-It pattern for bug fixes, characterization testing before refactoring. Hermetic fixture discipline, assertion selection by contract invariants, concrete test evidence, and bounded fix rounds.

## Purpose

Supply the testing method for an existing Python project — not another controlling loop. Hold the flow: context → baseline → choice of test path → small authorized step → verification → evidence.

The method is language-independent; the commands and libraries in this Skill are Python. For another stack use its native runner with the same flow and the same evidence discipline.

## Load when

- implementing new Python behavior inside the coding loop's TEST/INCREMENT phase;
- fixing a bug (Prove-It pattern);
- refactoring with characterization tests;
- an explicit test-only task is requested.

## Do not load when

- the task is pure documentation, a non-Python frontend, or configuration without logic;
- spec approval, final review, product acceptance, or a done claim is requested (owned by `coding-loop` and its review method);
- the project prescribes a different test method — hand over to that method, never force a migration.

## Dependencies

- `coding-loop` — owns the single spec gate, fix-round budget, review, and acceptance; work inside its phase during implementation.
- `code-review` — review consumes the test evidence produced here; this Skill never creates a second review or acceptance loop.

## Workflow

### Role and boundaries

- During implementation work inside the corresponding `coding-loop` phase; leave the single spec gate to that Skill. Never re-open a valid approval and never call the loop back.
- For direct test-only work perform only approved tests/diagnostics; a failure never becomes permission to modify product code. Refactoring or a fix happens only within its authorized scope.
- Never take over spec approvals, final review, product acceptance, or a "done" conclusion. Never confuse a development coding loop with a production research loop.
- Never create a project, infrastructure, CI, or a new stack. Respect the live project policy (e.g. stdlib-only), its rules, and existing test tooling. Never introduce pytest, coverage tooling, or other new dependencies merely for TDD. This Skill supplies the method with stdlib unittest; if another test method is prescribed, hand over to the corresponding available Skill.
- Never grant permissions, workers, or model routes. Never perform Git writes, imports, publication, or live/paid acceptance as a side effect of testing.
- Write output in the language of the assignment; keep identifiers, file names, and commands in their original form.

### 1. Load context and real conventions

1. Take the task-local project-context from the router and verify its age against live project documents and touched files. Read handoffs, old GOs, and tool results as evidence — never as new authorization.
2. On direct use, find the project skill in the current catalog that owns its own `references/project-context.md` and read only that file; never run the router recursively and never copy the adapter here.
3. If no project skill is available, state its name as `UNAVAILABLE`. Read live project entry files and assemble a small task-local context: rules, scope, contract, real commands, protected inputs, known gates (`AGENTS.md`, `README.md`, status, decision index, `TODO.md`, relevant specs); follow needed links per task. In an empty project there are no entry files: state `PROJECT_CONTEXT: EMPTY`, take the user's assignment as the only source, mark derived rules as assumptions, and propose the test method before running anything.
4. Look up further methods in the current catalog by exact name too — no absolute installation paths, no cross-package links. If a method is essential for the phase and unavailable without an authorized equivalent native workflow, stop the phase; a read-only proposal may continue with the limitation admitted. Report unavailable review as `UNREVIEWED`.
5. Verify working root, interpreter, test discovery, test IDs, neighboring tests, and existing fixture/mocking conventions. Never infer commands from a skill name or a historical original.
6. Before editing clarify the observable contract, permitted files, and immutable inputs. Hand a missing source, permission, or significant scope change to the phase owner; never bypass a gate.

### 2. Establish the baseline

Run targeted existing tests and relevant project checks in the authorized environment. Verify the current full baseline per policy before concluding anything about a new change; a historical test count is not permanent proof.

Use the following stdlib shapes only after confirming they match the project; replace placeholder test IDs with real ones:

```sh
python3 -m unittest tests.test_module.TestCase.test_behavior
python3 -m unittest discover -s tests -t .
python3 -W error::ResourceWarning -m unittest discover -s tests -t .
```

Record separately: targeted tests, full suite, strict resource run, and any separate canonical checker the project requires. Never suppress checker output just because a regression test passes.

Admit a known defect from context with its exact location, finding code, and exit statuses. A regression may correctly pass while checking a preserved defect while the canonical checker fails. A known defect is not a waiver and not a new behavioral RED; a clean-checker gate stays blocked without an explicit scoped exception or authorized correction.

### 3. Choose one test path

| Task | Procedure and required evidence |
|---|---|
| New behavior | Write a test of the observable contract → observe a relevant behavioral RED → minimal implementation → GREEN → refactor with tests still green. |
| Bugfix — Prove-It | Reproduce the real problem → test on the faulty snapshot FAILs for the right reason → minimal fix → same test PASSes → regression suite. |
| Refactoring | First characterization of current intended behavior → capture baseline results → change structure in small steps → preserve contract and suite. An immediate GREEN is valid evidence. |
| Test-only | Check coverage and add/run approved tests. Document failures; propose product fixes only. |

- Attest RED with a concrete assertion and the expected/observed behavior delta. A broken import, typo in a test ID, missing library, or environment permission fault is not a reproduced behavioral failure.
- For rejection of invalid input also check side effects: return/exit status, outputs not created, inputs unchanged. Never limit the test to "it threw some exception".
- If a new-behavior test passes immediately, check whether the behavior already exists and whether the assertion actually discriminates the contract. State truthfully "RED not observed"; never manufacture an artificial defect or fake history.
- Mark characterization of known faulty behavior as preservation of the defect, not acceptance of it; keep the expected fix separate from this contract.
- Reach GREEN by fixing the implementation within permitted scope — never by deleting a test, lowering acceptance, hiding a finding, or hand-editing a generated report instead of the renderer.

### 4. Keep tests hermetic

- Use `unittest.TestCase`, `unittest.mock`, local fixtures, and `tempfile.TemporaryDirectory` per existing conventions; never call networks/models, real accounts, or production services — including real sockets on localhost.
- Read original fixtures, snapshots, historical data, logs, and reports without modification. For tampering/append/traversal/symlink/bad-hash tests first create a copy in an isolated temp directory and modify only the copy. Add new test fixtures only in authorized scope; label synthetic provenance explicitly.
- Separate inputs from runtime output. For a fresh-output contract create an existing temp parent and a not-yet-existing child outside the checkout; never pass an already-existing root `TemporaryDirectory` as fresh output. Give each run a different path; never overwrite historical outputs.
- Patch objects where the tested module looks them up; mocks return realistic data and controlled errors. Prefer dependency injection; never cover your own test oracle with a global I/O mock.
- Isolate time randomness env and working directory only where they affect the contract. Restore changes via context manager or `addCleanup`; close files processes and mocks even on FAIL. Never use suite order host clock or sleep as an oracle.
- Test the result and relevant absence of side effects. For I/O fault injection verify actually confirmed writes audit trail and incomplete/error outcome; never mark unwritten evidence or a failed export as success.
- Distinguish a proven offline entry point from a mocked ban on one specific call from OS network isolation. Zero `model_calls` does not prove absence of all side effects; an arbitrary injected Python callable is not automatically a network sandbox.

### 5. Select assertions by invariants

Derive coverage from the contract and risk — never from a rigid test-pyramid ratio or raw test counts. Do not copy an existing suite; add missing observable boundaries.

The following invariants come from a data-product origin. In another project replace them with the invariants of its contract; the structure stays:

- Accept evidence only after confirmed storage or explicitly selected reuse; verify identical references across ledger manifest and selected report views.
- For invalid inputs verify controlled rejection of hash mismatch traversal/symlink duplicate IDs/JSON keys and bad paths only where the current contract requires it; never invent a new schema.
- Preserve original statuses and unknown usage/terms. A replay must never turn `unverified` into `verified`, a missing datum into a documented zero, or a synthetic fixture into live research output.
- Separate structural validation from source presence and quote match from semantic support of claims from operator acceptance. A test PASS is software evidence — not truth proof or a research-quality metric.
- Compare deterministic semantic content of MD/HTML and completeness of selected evidence; keep quotes as safely rendered data. Fresh run IDs and runtime metadata may differ: without defined normalization never claim byte-identical whole bundles.

Design scenarios — **NOT PERFORMED**: on a fixture copy change an input hash and verify rejection before output creation; inject failure of a second write and verify only the first confirmed evidence in all views plus an incomplete outcome. First compare against the existing contract and coverage; this is neither a found-bug claim nor consent to run anything.

### 6. Verify bound attempts hand over evidence

After each small step rerun the same targeted test related modules and the full suite; use resource/checker runs per policy. After a refactor re-verify the touched contract. Never present unrun checks as PASS.

After two failed fix rounds change hypothesis or diagnostic method. Allow at most three failed rounds per problem; after the third stop honestly and hand over results and the needed decision. A permission/missing-source blocker stops earlier — never consume further rounds.

Hand over a concise test record — never new product ledger fields:

- **Context:** goal path (TDD/Prove-It/characterization/test-only) scope date initial and final snapshot (revision plus diff/hash of touched files for uncommitted edits).
- **Targeted proof:** exact test IDs command cwd/interpreter observed FAIL reason and exit status on the initial snapshot; same test exit status and summary after the change. For characterization state immediate GREEN; without a run state NOT PERFORMED.
- **Regression and gates:** actual count/result of the full suite resource run and canonical checker separately known findings input integrity and mock/isolation boundaries. Report a missing result as unverified — never as an estimate.
- **Change and handoff:** tests/implementation changed in permitted scope refactor remaining risks count of failed rounds and next needed decision. Store logs only in permitted locations; never put credentials private data or hidden reasoning traces into shared evidence.

Hand the phase owner the final contract snapshot and tests for `code-review` if policy requires it; never create a second review/acceptance loop here. A behavioral change after review invalidates relevant review coverage and requires fresh review per approved policy/budget. An advisory checker is never reviewer of record. Report implemented/tested separately from `UNREVIEWED` authorized offline acceptance operator acceptance and Git state; never derive any of these from PASS or `complete`.

## Forbidden behavior

- Weakening deleting skipping or specializing an assertion to force PASS.
- Manufacturing an artificial RED by damaging code or faking history.
- Calling networks models real accounts or production services from tests.
- Overwriting historical outputs fixtures logs or reports.
- Editing checkers CI or acceptance criteria for cosmetic green.
- Treating a test PASS as proof of research truth or product acceptance.

## Verification

- RED (or immediate-GREEN for characterization) observed and recorded with exact IDs commands and exit statuses.
- Full suite resource run and canonical checker reported separately with actual results.
- Fix rounds within cap (max 3 per problem); exhausted budget reported honestly.
- Evidence record complete per the four-part structure above.

## Output contract

- Concise test record: context targeted proof regression/gates change-and-handoff.
- Failures documented with proposed (not performed) product fixes for test-only work.
- Explicit NOT PERFORMED / UNVERIFIED / UNAVAILABLE markers instead of assumed results.

## References

The reference material is part of this skill in the sections below:

- [Origin and license boundary](#origin-and-license-boundary)

The original MIT notice remains in [LICENSE.txt](LICENSE.txt).

## Origin and license boundary

### Direct methodological source

Derive this English skill from `agora-pro-setup`, file `skills/android-development/android-dev-tdd/SKILL.md`, revision `552034846217c035ce802aad276fb826d0aaedf4`. The source file was read in full locally on 2026-11-14; take the source revision identifier from the binding build contract, not as a claim of a new Git verification.

Preserve the upstream MIT notice and the complete license text unchanged in `LICENSE.txt`. The license covers this methodological derivative, not third-party project code or data.

The original skill states its own adaptation from `addyosmani/agent-skills/skills/test-driven-development` (RED–GREEN–REFACTOR, Prove-It, test pyramid, and the named rule). Present this secondary attribution as information inherited from upstream; the secondary source was not separately read or verified for this task.

### Adaptation — 2026-11-14

- Preserve tests-first, behavioral bug reproduction, minimal fix, regression, and fixture-first approach.
- Replace Android/Kotlin/Compose/Gradle conventions with stdlib Python `unittest`, `unittest.mock`, and temporary directories; do not adopt tools or percentage-based test pyramids.
- Correct “Tests are proof” to concrete software evidence separated from truth, source support, and operator acceptance.
- Add immediately-green characterization, a test-only boundary, fixture-copy integrity, exact snapshot/FAIL/PASS records, known checker blockers, and a fix-round limit.
- Preserve one-way composition: the testing method sits inside the coding loop, without its own spec gate, callback to the router, Git writes, or live acceptance.

### Project material, not copied software

Read the local `agora-manus-adaptation/aipt-tdd-coding-loop-navrh.md` proposal and its `skill-build-contract.md` on 2026-11-14. As context, load the live AIPT `AGENTS.md`, `README.md`, `docs/principles.md`, `docs/project-status.md`, `docs/decisions/effective-index.md`, `docs/milestone-3-spec.md`, `contracts/offline-replay-v1.md`, and `TODO.md` (accessed 2026-11-14). The build contract and proposal cite project revision `04772f3cdee2a0fe8e6560e8ee1799fed8ac44cb`; it was not independently verified with a Git command for this task.

Do not copy AIPT code, fixtures, or historical data; do not infer a reuse license from this skill or change the project's missing license. Keep the only stored AIPT adapter at `aipt-project-workflow/references/project-context.md`; here retain only the general testing method and instructions for loading live context. Treat dated material neither as permanent runtime evidence nor as new permission.

Distinguish structural package validation from use of the skill, import, test/runtime correctness, review, and product acceptance. Mark the design scenarios in SKILL.md as **NOT PERFORMED**; their inclusion is not execution or authorization to implement.

### Clarification after user audit — 2026-11-14

Limit the stdlib-only policy to AIPT according to its current rules; other Python projects follow their existing conventions and tooling. Preserve this skill's method using stdlib `unittest`, the ban on adding new dependencies solely for TDD, and handoff of a different prescribed method without forcing migration. This change updates instructions; it is not a runtime test, import, or project-code change.
