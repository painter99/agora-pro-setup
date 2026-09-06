# Shell and Device Operations

Agora may expose Local Sandbox, Conch, SSH, and device-file tools depending on build and configuration.

## Device selection

Use `list_shells` when the target is ambiguous. Do not assume Local Sandbox is the intended device.

## Conch

Conch commands may become durable jobs. A bounded wait can return a `job_id` without killing the process. Inspect, wait, stop, or acknowledge the exact job; never blindly rerun an unknown job.

## SSH

SSH settings describe a real Linux host: host, port, Linux username, and authentication for that host. GitHub's `github.com` / `git` endpoint is Git transport, not a general Agora shell device.

## Safe sequence

1. Inspect target and current state.
2. Use the smallest reversible command.
3. Obtain approval for destructive or high-trust actions.
4. Read command result or job status.
5. Verify actual file/system state.
6. Report device, status, and limitations.
