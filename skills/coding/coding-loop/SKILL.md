---
name: coding-loop
description: "Goal-based coding loop for agent-driven implementation: spec gate, small increments, tested steps, second-agent review, bounded fix rounds, and anti-reward-hacking guards before any done claim."
license: MIT
---

# Skill: coding-loop

## Catalog description
Goal-based coding loop for agent-driven implementation: spec gate, small increments, tested steps, second-agent review, bounded fix rounds, and anti-reward-hacking guards before any done claim.

## Purpose
Run coding tasks as a closed loop with a deterministic stop condition instead of an open-ended "write code until it looks done". The agent writes the code; the loop enforces verification: tests, a fresh-context review, and acceptance against reality. Field evidence (2026) shows that "tests green" alone is an unreliable correctness signal — reward hacking grows measurably with the size of the change — so this loop treats tests as reviewable artifacts, not as proof.

## Load when
- implementing a coding task from a specification or a user request;
- fixing a reported bug (reproduce → fix → verify);
- refactoring with an existing test suite as the safety net;
- writing automation scripts for the operator's own environment.

## Do not load when
- only reviewing code (Android/Kotlin diffs have `android-code-review`);
- the task already runs inside a domain workflow with its own loop (`android-spec-first`, `cad-spec-driven-workflow`);
- the request is not about code (research, writing, memory operations).

## Dependencies
- `tool-execution-contract` — retry discipline, tool-call budget, verification of every step.

## Workflow

### 1. Spec gate
Before writing code, state the specification: inputs, outputs, constraints, and what "done" means in observable terms. If the spec cannot say what done and failed look like, stop and get it from the user. A small task may hold the spec in the reply; a recurring or multi-step task gets it written down first.

### 2. Implement in small increments
Prefer the smallest change that moves toward the spec. One increment is one verifiable step. Reward hacking concentrates in large single-shot implementations — the measured gap grows with the size of the change — so a large change needs an explicit reason.

### 3. Test
Run the tests and read the report; an exit code is not evidence, the test output is. Tests are artifacts under review, not judges: never weaken, skip, or delete an assertion to make a run pass; never edit the test suite or CI configuration to fit the implementation without stating the reason and getting approval. If no test exists for the change, write the smallest test that would catch the bug or the regression.

### 4. Second-agent review
Before declaring done, have the diff reviewed in a fresh context — a new conversation or a task agent that reads the spec and the diff but not the implementation reasoning. The reviewer checks: does the code do what the spec says, do the tests actually test it, is anything hard-coded to pass? Fix review findings like any other failure.

### 5. Bounded fix loop
Fix rounds follow the tool-call budget: after two consecutive failed rounds on the same problem, change the approach; after three failed rounds, stop, report honestly what fails and what was tried, and hand back to the user. Never iterate silently past the cap.

### 6. Acceptance against reality
The final gate is acceptance on real input, not green tests: run the change on the actual data or environment it targets (or a faithful copy) and show the observable result. Nothing is done until this gate passes — never report completion without it.

### 7. Encode what was learned
Recurring fix patterns, review comments, and user corrections become system rules: propose a delta to the relevant Skill or a project rules file through the self-improvement loop instead of fixing only the instance. Fixes that never reach the ruleset will repeat.

## Hard limits
- Maximum 3 fix rounds per problem (then honest handback).
- Second-agent review is mandatory for every non-trivial change.
- No done claim without: test evidence + review pass + acceptance against reality.

## Anti-reward-hacking guards
- Tests and test configuration are reviewable artifacts; changes to them require justification and approval.
- Small increments by default.
- Never modify evaluation scripts, CI workflows, or checkers to make results look better.
- Report failures with the same prominence as successes.

## Forbidden behavior
- Never report a coding task as done based on "tests green" alone.
- Never weaken, skip, delete, or special-case an assertion to force a pass.
- Never iterate past the fix-round budget without reporting.
- Never skip the second-agent review on non-trivial changes.
- Never run an unscanned agent-written script on real data (script safety gate in `process-design`).
- Never put secrets or personal data into code, tests, or commit messages.

## Verification
- Test evidence: the actual test report (counts, failures), not a paraphrase.
- Review: fresh-context verdict recorded; findings resolved or explicitly deferred with a reason.
- Acceptance: observable result on real input (output, checksum, or state diff).
- Budget: fix rounds within cap; exhausted rounds reported honestly.

## Output contract
- The diff or file list with what changed and why.
- Test evidence and the review verdict.
- The acceptance result against real input.
- If not done: what fails, what was tried, and the handback question.

## Related docs
- `docs/29-self-improvement-loop.md` — the loop that turns recurring fix patterns into rules and Skills.
- `docs/28-update-observability.md` — measuring scheduled agent work that runs code.