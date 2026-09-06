# Skill: Shell and Device Operations

## Catalog description

Safe Local Sandbox, Conch, SSH, remote files, and durable job handling. Load when a command or device-file operation is required.

## Purpose

Agora shell is high-trust. The remote account's permissions define what the model can change.

## Load when

- a shell command or device-file operation is required;
- Conch, SSH, or Local Sandbox is involved;
- a durable `job_id` must be tracked;
- the target device is ambiguous.

## Do not load when

- answering without device tools;
- the needed text is already in context.

## Dependencies

`tool-execution-contract`. Use `04-tool-reference-card` if argument names are uncertain.

## Workflow

1. `list_shells` when more than one device exists or the target is unclear.
2. Identify **Local Sandbox**, **Conch**, or **SSH**.
3. Check confirmation policy, authentication, and secrets boundaries.
4. Inspect with `file_read` / `file_glob` / `file_grep` before edits.
5. Prefer a small reversible command.
6. For Conch: commands become durable jobs. A timeout returns `job_id` — it does **not** mean the job was killed. Use list/get/wait/stop; do not blindly rerun.
7. Verify exit status or job state **and** actual file/system state.
8. Stop on permission, authentication, or structural failure.

## GitHub is not a shell device

Do not add `github.com` as an Agora SSH/Conch device to "log into GitHub".

Correct chain:

```text
Agora → Local Sandbox or your Linux/Conch server → git + SSH key or HTTPS token → GitHub
```

If configuring Agora **SSH** toward a real Linux host:

```text
Host:     your server hostname or IP
Port:     22 (or the server's SSH port)
Username: the Linux account on that server
Password: only if that server uses password auth (prefer keys)
```

If you mistakenly thought GitHub SSH fields were:

```text
Host: github.com
User: git
```

that is Git transport, not an Agora shell login. GitHub does not provide general shell access.

## Forbidden behavior

- Exposing secrets in commands, remotes, or chat.
- Bypassing host-key verification.
- Rerunning an unknown durable job.
- Destructive commands without explicit approval.
- Claiming completion from a timeout alone.

## Verification

Confirm device, command or job status, and actual file state.

## Output contract

Device, exact operation, verified result, `job_id` when relevant, limitations.
