# Skill: Shell and Device Operations

## Catalog description

Safe selection, execution, and verification of Agora shell and device-file operations.

## Purpose

Govern Local Sandbox, Conch, SSH, remote files, and durable shell jobs.

## Load when

- a shell command or device-file operation is required;
- a remote device, Conch job, SSH connection, or sandbox is involved;
- command scope or verification is unclear.

## Do not load when

- answering without device tools;
- editing repository text already available in the current context.

## Dependencies

`tool-execution-contract.md`. Use the current shell tool documentation and configured device policy.

## Workflow

1. Use `list_shells` when the target device is ambiguous.
2. Identify Local Sandbox, Conch, or SSH and the exact scope.
3. Check confirmation policy, permissions, authentication, and secrets boundaries.
4. Inspect files with read, glob, or grep before editing.
5. Prefer a small reversible operation.
6. For Conch, track the exact `job_id`; a timeout does not mean the job was killed.
7. Verify exit status, job state, file contents, and dependent references.
8. Stop on permission, authentication, or structural failure.

## Forbidden behavior

Do not expose secrets, bypass host-key verification, rerun an unknown durable job, run destructive commands without approval, or claim completion from a timeout alone.

## Verification

Confirm the target device, command result or durable job status, and actual file state.

## Output contract

Report device, exact operation, verified result, job identifier when relevant, and limitations.
