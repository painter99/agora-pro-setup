# 25 — MCP tool layer and stdio bridge (architecture pattern)

> A reusable pattern for adding a schema-validated tool layer to the build
> host: a private MCP server that exposes narrow, guarded operations, plus a
> bridge that makes the stdio-shaped MCP ecosystem usable from a phone
> client. Generic by design — personal specifics (hostnames, tailnet names,
> IPs, unit names, personal data) never belong in a public repository; they
> live in the operator's private memory and local config.

## 1. Purpose

docs/22 §6 describes the structured tool layer as an optional layer above the
shell; docs/23 stops at shell transports; docs/24 closes the notification and
gateway gaps. This document records what was learned once that layer was
actually built, exposed and operated:

1. **Routine operations deserve a schema.** A raw shell call is untyped: the
   agent composes a command string, quoting is a live risk, and the command
   can reach anything the user account can reach. A narrow tool with declared
   parameters moves validation server-side and shrinks the write surface to a
   single file.
2. **The MCP ecosystem is stdio-shaped; phone clients are not.** Most
   published MCP servers ship as npm or Python packages launched as local
   child processes. A mobile client cannot spawn a process, so a host-side
   bridge is the only way to reuse that ecosystem without waiting for a native
   stdio transport.

Division of labour observed in practice:

| Operation | Better fit | Why |
|---|---|---|
| Convert a document, OCR an image, read host state, append one calendar entry | **MCP tool** | fixed shape, schema-validated arguments, one call |
| Explore a repository, interpret a CI log, ad-hoc investigation | **shell** | unbounded shape; one command replaces five tools |
| Anything needing elevated privileges, git credentials or deletion | **shell + explicit approval** | the tool layer is deliberately given no such powers |

The tool layer does not replace the shell. It removes the repetitive,
error-prone part of it and shrinks the area an unattended call can damage.

## 2. Architecture

```text
┌────────────────────────────────────────────────────────────────┐
│ OPERATOR PHONE — MCP client in the assistant app               │
│   transport: Streamable HTTP                                   │
└──────────────────────────┬─────────────────────────────────────┘
                           │ HTTPS, private mesh network only
┌──────────────────────────▼─────────────────────────────────────┐
│ BUILD HOST                                                     │
│   mesh VPN proxy (path per server, no public port)             │
│     ├─ /mcp      → 127.0.0.1:8765  own server (Python SDK)     │
│     └─ /bridge   → 127.0.0.1:8767  stdio→HTTP bridge           │
│                       └─ child process: unmodified npm server  │
│   service user: no sudo, no credentials, one writable file     │
└────────────────────────────────────────────────────────────────┘
```

Rules of the pattern:

- Every server binds to **localhost only**; the mesh VPN proxy is the sole
  external path, and the host firewall opens nothing extra.
- **One path per server.** Paths are not multiplexed: one proxy path maps to
  exactly one localhost port.
- The service user owns no secrets: no repository keys, no sudo, no cloud
  credentials. Anything sensitive stays in the operator's private memory.
- Write-capable tools write to **one designated file** and validate before
  touching it.
- The bridge is infrastructure, not a fork: the upstream package runs
  unmodified, so updates are `npm update` plus a service restart.

## 3. Transport

The layer speaks one remote transport: **Streamable HTTP**. A client sends
`POST initialize`, receives an `mcp-session-id` header, and carries it on every
subsequent request. Three consequences are worth designing for:

1. **Session identity lives in a header, not in a URL.** Nothing identifying
   ends up in access logs, bookmarks or proxy history.
2. **Requests are ordinary POSTs.** A status line in the server journal is
   enough to debug the integration — there is no long-lived stream to interpret.
3. **Sessions expire.** A stateful server keeps history per session, so an idle
   session is eventually reaped and the next call opens a fresh one. Multi-step
   tools therefore accumulate history inside one working stretch; across
   stretches the conversation itself carries the state.

This section resolves the open question recorded in docs/22 §6: TLS issued by
the mesh VPN proxy makes trusted HTTPS available inside the private network,
so the tool layer needs **no auth headers and no self-signed certificates**.
Add a bearer token only when more devices or people join the network.

## 4. Own server (narrow tools)

A handful of decorated functions is the whole server: the schema comes from the
type hints and docstrings, and every guard lives in the same file as the tool it
protects. Keep the first batch to three or five tools — the operations you
actually repeat, not everything the host could theoretically do.

### 4.1 Install

```bash
python3 -m venv /home/<user>/mcp
/home/<user>/mcp/bin/pip install 'mcp<2'    # verify the current major upstream first
```

### 4.2 Tool shape and guards

```python
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("host-tools")

def _safe_path(p: str) -> str:
    real = os.path.realpath(p)
    if not real.startswith(HOME_ROOT + os.sep):   # single allowed root
        raise ValueError(f"path outside allowed root: {p}")
    return real

@mcp.tool()
def md_to_pdf(path: str, out: str = "") -> str:
    """Convert a Markdown file inside the allowed root to PDF."""
    ...
```

### 4.3 systemd unit (hardened)

```ini
# /etc/systemd/system/mcp-tools.service (excerpt)
[Service]
User=<user>
WorkingDirectory=/home/<user>
Environment=TMPDIR=/tmp
Environment=MCP_PORT=8765
Environment=MCP_TRANSPORT=streamable-http
ExecStart=/home/<user>/mcp/bin/python /home/<user>/mcp/server.py
Restart=on-failure
NoNewPrivileges=true
```

### 4.4 Gotchas

These cost real debugging time:

1. **Major-version renames in the SDK.** A new major release renamed the
   server class; a pinned install (`'mcp<2'`) kept the documented API working.
   Verify the upstream name before pinning, and re-check on each upgrade.
2. **DNS-rebinding protection returns `421 Invalid Host header`.** When the
   server binds to `127.0.0.1`, the SDK automatically allows only
   `localhost`/`127.0.0.1`. The VPN proxy forwards the *hostname* as `Host`.
   Note that a `host:*` wildcard matches `host:port` only — **not** a bare
   hostname — so the allowlist needs the bare name, the wildcard variant, and
   the matching origins with and without scheme. The protection stays on; only
   the list is corrected.
3. **Tool errors are results, not exceptions.** The protocol returns
   `isError=True` inside the result. A test client that expects a raised
   exception will report a working guard as a failure — and a broken guard as
   a pass. Assert on `isError`.
4. **Subprocess-spawning tools need a writable working directory.** Without
   `WorkingDirectory=` a hardened unit runs in `/` and document converters
   fail with `openTempFile: permission denied`. Set `TMPDIR` as well.
5. **Converters can be stricter than the CLI suggests.** Some require a
   non-empty document title; derive one from the content instead of relying on
   the caller to pass it.
6. **Verify the command you meant, not the flag you typed.** A health tool can
   look healthy while one section is silently wrong, because a short option was
   read as field selection instead of output format and the subcommand exited
   non-zero into a fallback string. Print the section, compare with the raw
   command run by hand.

## 5. Bridging stdio-only ecosystem servers

The published MCP ecosystem is overwhelmingly stdio-shaped: packages are launched as
child processes by a desktop client. A phone cannot do that, so the bridge turns
the child process into a remote endpoint and the client never notices the difference.

### 5.1 Install package and bridge

```bash
sudo apt-get install -y nodejs npm
mkdir -p /home/<user>/mcp-node && cd /home/<user>/mcp-node
npm install @modelcontextprotocol/server-sequential-thinking supergateway
```

### 5.2 Unit and proxy path

```ini
# /etc/systemd/system/mcp-bridge.service (excerpt)
[Service]
ExecStart=/home/<user>/mcp-node/node_modules/.bin/supergateway \
  --stdio "node /home/<user>/mcp-node/node_modules/@modelcontextprotocol/server-sequential-thinking/dist/index.js" \
  --outputTransport streamableHttp --port 8767 \
  --streamableHttpPath /bridge --stateful --sessionTimeout 1800000
```

```bash
tailscale serve --bg --set-path=/bridge http://127.0.0.1:8767/bridge
```

### 5.3 Gotchas

1. **The proxy path must appear in the target URL too.** Proxying
   `--set-path=/bridge` to `http://127.0.0.1:8767` (without the path) yields
   `404`; the target has to carry the same path the bridge listens on.
2. **Without `--bg`, adding a second path fails** with "listener already exists
   for port 443" — the first handler owns the port.
3. **Bridges often have no `--host` flag** and bind `*:PORT`. The firewall
   plus proxy-only exposure is what makes that acceptable; state this in the
   security model rather than assuming a loopback bind.
4. **`pkill -f "<pattern>"` can kill the calling shell** when the pattern is
   part of its own command line. Use a bracket pattern or resolve the PID from
   the listening socket first (same lesson as docs/23 §11).
5. **State lives per session.** A stateful bridge keeps one child process per
   session, so multi-step tools accumulate history; an idle timeout destroys
   the session and resets that history. Spawning per call instead would break
   every stateful server. Choose the session timeout with the client's usage
   pattern in mind.

The recipe generalises: a new ecosystem server is a package install, a new
port, a new path, and one more unit from the same template.

## 6. Client-side integration

- Add the server with transport type, URL and (optionally) custom headers,
  then enable tools **per tool**. Start read-only tools first.
- **Tool lists are snapshotted when a conversation is created.** After adding
  or enabling anything, open a *new* conversation; an existing one will keep
  the old tool set and look like a failed integration.
- **The server journal is ground truth.** `POST /mcp 200`, the request method
  names (`ListToolsRequest`, `CallToolRequest`) and the client address prove
  which transport the client actually used and whether a call landed. Never
  infer connectivity from a client UI state.
- Smoke-test order: `tools/list` → one read-only call → one narrow write call →
  **clean up the write** → one negative test (a path outside the allowed root,
  an impossible date) to prove the guards, not only the happy path.

## 7. Verification and measurement

| Check | Command / evidence | Pass condition |
|---|---|---|
| Service state | `systemctl is-active <unit>` | `active` and enabled |
| Proxy mapping | `tailscale serve status` | every path → its own port |
| Handshake | real MCP client against the **VPN URL**, not localhost | session id returned |
| Tool inventory | `tools/list` | expected names and schemas |
| Behaviour | `tools/call` per tool | real data, not a status string |
| Guards | `tools/call` with hostile input | result with `isError=True` |
| Client reach | server journal | request logged from the phone's address |
| Persistence | reboot, then repeat handshake | still reachable |

What the pilot still owes you is the **comparison against the shell**, and it
should be measured rather than asserted: for a fixed list of routine
operations, record prompt tokens per call, retry rounds until success, and
which layer was used. Aggregate after a couple of weeks and let the table
decide where the tool layer grows and where the shell stays.

One operational trap worth naming here, because it bit during verification:
a **durable background-job transport may execute commands as a different user
than the SSH device** (commonly root). Repository tooling then refuses to
operate on files owned by an unprivileged user ("detected dubious ownership"),
and a global configuration written under a different `$HOME` silently lands
somewhere else. Keep per-user work — git, edits, pushes — on the SSH identity
that owns those files, and reserve the job transport for long builds, image
viewing and system administration.

## 8. Security model

- **Least privilege.** The service user has no sudo, no shell history of
  value, no repository or provider keys. Each server is a separate unprivileged
  process with its own port.
- **Narrow write surface.** Exactly one designated file is writable, through
  validated arguments. Deletion is not exposed as a tool at all.
- **Network surface.** Localhost binds plus mesh-VPN proxy; the firewall opens
  no service ports. Reachability equals tailnet membership. A bearer token is
  added when devices beyond the operator's own join.
- **Third-party servers are a different trust class.** A remote MCP server sees
  the prompt content of every call routed to it and may have side effects.
  Prefer self-hosting in the private network; when adopting an ecosystem
  server, verify it exists upstream first — briefings in this project have
  contained plausible but non-existent server names.
- **No auto-discovery.** Only servers the operator explicitly added run.

## 9. Bootstrap order

1. Host bootstrapped and reachable as in docs/23; mesh VPN proxy and HTTPS
   certificates enabled as in docs/24 §2.2.
2. Python venv + SDK; write **three to five** tools covering the operations
   you actually repeat, each with its guard.
3. Negative tests for every guard before any client is involved.
4. systemd unit (unprivileged user, `WorkingDirectory`, restart policy), enable.
5. Proxy path for the server; verify with a real MCP client over the VPN URL.
6. Add the server in the client, enable chosen tools, **open a new
   conversation**, confirm from the server journal.
7. Only then add an ecosystem server through the bridge: package, own port, own
   path, own unit, same verification loop.
8. Start the measurement table (§7) and revisit scope from data.

## 10. Anti-patterns

- Treating the tool layer as a replacement for the shell, or refusing it
  because the shell "can do everything".
- Giving an MCP server sudo, repository keys or cloud credentials "for
  convenience".
- Exposing a generic `read_file(path)` / `run(command)` tool — that is the
  shell again, with a schema painted on top.
- Two servers on one proxy path, or one server split across two paths.
- Assuming a phone client can launch a stdio server.
- Believing a client is connected because the settings screen looks configured,
  instead of reading the server journal.
- Trusting tool output that "looks right" for one section while another section
  silently fell back to an error string.
- Verifying guards only with happy-path calls.
- Writing instance-specific hostnames, tailnet names or personal file paths into
  this public repository.

## 11. Cross-references

- **docs/22 §6** — the structured tool layer as an architectural option; §7 —
  why MCP comes after the shell bootstrap. The open question there (TLS and
  auth headers) is resolved in §3 of this document.
- **docs/23** — host bootstrap, phases 5–7 (toolchain, durable jobs, mesh VPN)
  and the gotcha list this document builds on.
- **docs/24** — notification layer and LLM gateway: the pattern for services
  that bind to localhost and are published through the same proxy, and the
  place where tool-driven jobs can publish their results.
- **docs/8** — tool safety and approval bands; **docs/17** — permission model
  the narrow-write rule follows; **docs/21** — retry discipline applied while
  debugging transports.
