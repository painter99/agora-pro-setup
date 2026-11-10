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
- `process-design` — script safety gate for agent-written scripts (see Forbidden behavior).
- `self-improvement-loop` — step 7 handoff: recurring fix patterns become deltas instead of instance-only fixes.

## Workflow

### 1. Spec gate
Before writing code, state the specification: inputs, outputs, constraints, and what "done" means in observable terms. If the spec cannot say what done and failed look like, stop and get it from the user. Every behavior in the spec needs a test path — a mechanism (an override, a fixture) or an explicit deferral with a reason — and the spec must cover malformed inputs (missing or wrong header, empty input). A small task may hold the spec in the reply; a recurring or multi-step task gets it written down first.

### 2. Implement in small increments
Prefer the smallest change that moves toward the spec. One increment is one verifiable step. Reward hacking concentrates in large single-shot implementations — the measured gap grows with the size of the change — so a large change needs an explicit reason.

### 3. Test
Run the tests and read the report; an exit code is not evidence, the test output is. Tests are artifacts under review, not judges: never weaken, skip, or delete an assertion to make a run pass; never edit the test suite or CI configuration to fit the implementation without stating the reason and getting approval. If no test exists for the change, write the smallest test that would catch the bug or the regression.

### 4. Second-agent review

Before declaring a non-trivial change done, obtain qualified review in a separate fresh context. Supply the specification, final diff, final contents of touched files, relevant tests, and acceptance criteria — not the implementation reasoning or author conversation. The reviewer checks specification compliance, test adequacy, hard-coded behavior, weakened assertions, and scope violations.

**Reviewer mechanics (Agora).** Use an available, approved subagent mechanism under the kernel's role, permission, spawn-budget, and concurrency rules. Verify exact tool names against the live schema. A Loop or self-review in the author conversation is not independent review. If no qualified fresh-context reviewer is available, or the approved budget is exhausted, stop and report the work as unreviewed. Do not use scheduled Tasks, Loops, providers, or direct APIs as a review fallback or budget bypass. A trivial change may use self-review with deterministic evidence; mandatory review for non-trivial changes is not waived.

**Freshness and lifecycle.** Immediately before reviewer dispatch, inspect the live artifacts and verify that the supplied final contents and diff match them. Record the reviewed revision or content hashes. Treat the supplied review inputs as immutable. Wait for the terminal result; a timeout permits another wait, not a duplicate spawn. Verify the verdict and follow the kernel's worker lifecycle policy.

If the target changes after dispatch, the verdict does not cover the changed target. Record the mismatch, preserve useful findings as provisional, and obtain required review of the updated artifact in a separate fresh context within the remaining approved budget. Do not resume a previously briefed reviewer and label it fresh.

**Reviewer prompt contract.**

```text
Role: Qualified fresh-context reviewer; you did not produce this artifact.
Goal: Assess the supplied artifact against the specification and acceptance criteria.
Inputs: Specification, final diff, final touched-file contents, relevant tests,
        and reviewed revision or content hashes.
Checks: Correctness; test adequacy; hard-coded passing behavior;
        weakened or skipped assertions; out-of-scope changes.
Output: Final message with finding, severity, evidence, and suggested fix;
        overall verdict PASS / PASS-with-notes / FAIL.
Permissions: Read only the explicitly supplied or allowlisted artifacts.
Prohibitions: No artifact edits, publication, spawning, ask_user, persistent
              automation, memory or Skill writes, or secret/credential access.
Stop: Missing, unreadable, inconsistent, or stale inputs — report the gap;
      do not invent findings or expand access.
```

The coordinator verifies the verdict, resolves findings, and records remaining limitations. A review pass covers only the inspected artifact state.

### 5. Bounded fix loop
Fix rounds follow the tool-call budget: after two consecutive failed rounds on the same problem, change the approach; after three failed rounds, stop, report honestly what fails and what was tried, and hand back to the user. Never iterate silently past the cap. Fix-round review policy: fixes for minor findings need re-tests and a fix-diff artifact; fixes that change behavior or the spec need a fresh re-review with a new fresh-context reviewer using an available approved subagent mechanism; if unavailable, report the updated work as unreviewed.

### 6. Acceptance against reality
The final gate is acceptance on real input, not green tests: run the change on the actual data or environment it targets (or a faithful copy) and show the observable result. Nothing is done until this gate passes — never report completion without it. Verify with an independent second method (checksum, grep, a second tool); a mismatch between two methods is a loud report, not a silent choice.

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