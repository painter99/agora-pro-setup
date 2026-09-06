# Shell and Device Operations

Agora can expose a Local Sandbox, Conch remote shell, SSH devices, and related remote file operations depending on build and configuration.

## Device selection

Use `list_shells` when the target is ambiguous. Do not assume that the Local Sandbox is the intended device. Confirm the device, account, permissions, and command scope.

## Conch

Conch commands may become durable jobs. A bounded wait can return a `job_id` without killing the job. Do not rerun an unknown job. Inspect, wait, stop, or acknowledge the exact job as appropriate.

## SSH

Verify host, user, authentication, and host-key policy. Do not bypass host-key verification or expose private keys.

## Safe workflow

1. Inspect the target.
2. Use a minimal reversible command.
3. Require approval for destructive or high-trust actions.
4. Read the command result or job status.
5. Verify actual file and system state.
6. Report the device and limitations.

Shell capabilities are high-trust capabilities. The remote account's permissions determine what the model can change.
