# Shell and Device Operations

Agora may expose Local Sandbox, Conch, SSH, and device-file tools depending on build and configuration.

## Device selection

Use `list_shells` when the target is ambiguous. Do not assume Local Sandbox is the intended device.

## Conch and SSH

How Conch durable jobs and SSH transport behave — job lifecycle, encryption, host-key pinning — is defined by the application and documented in the official user manual. This repository adds only operating rules on top: treat both shell types as high-trust capabilities, inspect/wait/stop/acknowledge the exact job, and never blindly rerun an unknown job.

## Safe sequence

1. Inspect target and current state.
2. Use the smallest reversible command.
3. Obtain approval for destructive or high-trust actions.
4. Read command result or job status.
5. Verify actual file/system state.
6. Report device, status, and limitations.
