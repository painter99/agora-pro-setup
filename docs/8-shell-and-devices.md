# Shell and devices

Agora may expose:

- **Local Sandbox** (F-Droid Alpine)
- **Conch** (HTTP job server + remote files)
- **SSH** (a real Linux host)

Plus remote read/write/edit/glob/grep/`view_image` depending on device type.

## Conch fields (Settings → Shell)

These are **not** GitHub fields.

| Field | Meaning |
|---|---|
| Server URL | your Conch server, `https://…` |
| API Key | Conch API key (not a GitHub token) |
| Name / Description | labels for you |

If you do not run Conch, do not fill this form. Use Local Sandbox or SSH to a machine you control.

## SSH fields toward a Linux host

```text
Host:     hostname or IP of YOUR server
Port:     22 (or custom)
Username: Linux user on that server
Auth:     key or password for THAT server
```

Not `github.com` / `git`. GitHub SSH is Git transport and does not give a general shell.

## Durable jobs

A Conch timeout returns `job_id` without killing the job. Track it. Do not rerun blindly.

Details: Skill [`shell-and-devices.md`](../skills/shell/shell-and-devices.md).
