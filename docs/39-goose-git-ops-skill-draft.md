---
name: goose-git-ops
description: Request authorized Git operations through a controlled broker; never treat a review result as permission.
---

# goose-git-ops

> **Adopted 2026-11-21 (ADR-0022).** The live Skill is [`skills/shell/goose-git-ops`](../skills/shell/goose-git-ops/SKILL.md); this draft is retained as the draft of record. Advisory mode only until the broker infrastructure is verified.

## Purpose

Prepare changes and request a narrowly scoped Git operation through the project's controller and broker. The skill describes a workflow; it does not provide credentials, authorize an operation, or prove that a broker is secure.

## Security limitation

If you have unrestricted `sudo` or equivalent access to the host that holds the Git credentials, local wrappers, filesystem permissions, tokens, locks, and logs are not security boundaries. You may be able to bypass them. In that situation this skill is process discipline only. Do not claim that Git operations are technically fenced. Keep automatic remote operations off and use advisory mode until real isolation has been independently demonstrated.

## Required roles

- **Agent (you):** prepare a change and submit an operation request with a manifest. Do not self-authorize.
- **Controller:** verify owner authorization and scope, observe the gate and broker, and stop work on uncertainty.
- **Fresh gate context:** review the exact operation package and return structured `PASS` or `FAIL`.
- **Qualified reviewer:** provide any separate independent review required by project policy. Gate `PASS` never replaces this review.
- **Broker:** in an isolated, minimally privileged environment, execute only the exact approved operation and record its result.

## Workflow

### 1. Check the route before preparing a request

- Confirm that the project explicitly enables this controlled path and that it is not advisory-only.
- Identify the permitted operation type: `commit`, `push`, or `merge`.
- Check that you have an explicit, current authorization for that exact operation and scope. If missing or ambiguous, stop and ask the controller through the established project process; do not infer approval from a task request, prior approval, gate result, or earlier operation.
- Do not continue if isolation, required review, audit availability, or broker state is unknown.

### 2. Prepare an immutable operation package

Prepare the proposed change in the authorized workspace. Do not include secrets. Create a versioned manifest that identifies at least:

- unique operation ID, repository identifier, operation type, and actor;
- target branch/ref or pull request and intended method;
- exact expected old and new object IDs, parent/base/head as applicable;
- snapshot and complete relevant object/diff inventory;
- approved brief and scope, with digests;
- required deterministic checks and their evidence, command/result, exit status, and snapshot ID;
- required qualified-review record, if applicable;
- expected outcome, expiry, and any project-specific constraints.

For a commit, identify the exact tree and parent. For a push, include the full commit range and expected remote ref state; never request force or history rewrite. For a merge, identify the exact pull request, source head and target base, resulting tree, required checks, and merge method. Incomplete, stale, truncated, or ambiguous data is a stop condition.

Do not rely on a mutable shared worktree after submission. If any relevant object, ref, manifest, check, approval, or base/head changes, request a fresh review and authorization.

### 3. Submit the request; do not execute it yourself

Send the manifest and referenced immutable snapshot through the approved request interface. The request is a proposal, not an instruction to run arbitrary Git commands. Use only typed broker operations exposed for this project; never submit shell strings, arbitrary arguments, alternate remotes, or unapproved refs.

Wait for the controller and fresh gate. A valid gate result must identify the operation, manifest digest, snapshots, scope, coverage, checks, evidence, blockers, context, and time. Only exact `PASS` is a positive gate outcome; timeout, malformed result, incomplete coverage, or changed snapshot is `FAIL`/stop. `PASS` is not owner authorization and does not let you act beyond the approved scope.

The authorization service and broker—not you and not the gate model—must validate approval, required qualified review, checks, signature, expiry, revocation state, and exact snapshot. Do not create, copy, edit, or reuse an authorization token. One grant is for one bound operation and must not be replayed.

### 4. Wait for broker execution and verification

After the controller confirms that all independent requirements are satisfied, wait for the broker's operation result. Do not run a parallel commit, push, merge, or retry. A timeout or lost response means the state is unknown, not that the operation failed. Do not resubmit: ask the controller to inspect the same operation and reconcile its audit record and remote state.

The controller must verify the resulting repository or pull-request state independently and report the exact outcome. A successful remote operation may not be safely reversible. Do not attempt a rollback or cleanup without a new explicit authorization.

## The agent must NEVER

- Read, copy, print, transmit, or search for private keys, passwords, tokens, credential stores, or broker signing material.
- Push directly, merge directly, or use an alternate identity, remote, API, shell, or credential path to bypass the broker.
- Treat gate `PASS`, a test result, a prior grant, or a general request as authorization.
- Expand the approved repository, operation, ref, commit range, pull request, method, or snapshot.
- Force push, rewrite history, change protected refs, or retry an uncertain operation.
- Modify a submitted manifest, review, audit record, or authorization token to make it pass validation.
- Run untrusted repository hooks or tests with broker privileges or ask the broker to execute arbitrary commands.
- Claim isolation, successful execution, clean audit, or remote state without controller-verified evidence.

## Stop and report

Stop requesting mutations and notify the controller when authorization is absent or unclear; the gate fails or is unavailable; evidence or snapshot is incomplete or changed; the broker or audit is unavailable; a credential path or privilege boundary is uncertain; results conflict; or an operation's outcome is unknown. Report the operation ID and observable error only; never include secrets. Do not start a duplicate job. The controller must invalidate pending grants, inspect any in-flight broker job, and reconcile before further action.

## Status and limitations

This draft assumes a controller, fresh-context gate, authorization service, isolated broker, immutable snapshot store, and durable audit path exist and have been tested. Their availability and security are **UNVERIFIED**. Until independently proven, use advisory mode only. This skill is not a security boundary and does not replace project rules, owner approval, independent qualified review, or platform protections.
