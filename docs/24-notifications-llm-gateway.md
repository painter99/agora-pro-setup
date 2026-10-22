# 24 — Notification layer and LLM gateway (architecture pattern)

> A reusable pattern for completing the episodic agent loop on a build host:
> a self-hosted notification service so the operator's phone knows when the
> agent needs attention, and a local LLM gateway so agents can call cloud
> models without ever seeing API keys. Generic by design — personal specifics
> (hostnames, tailnet names, IPs, key material) never belong in a public
> repository; they live in the operator's private memory and local config.

## 1. Purpose

The phone-orchestrated platform (docs/22) leaves two gaps once the host is
operational:

1. **Operator awareness.** The agent is episodic — it observes only when it
   looks. A background job that finishes, fails, or waits for approval is
   invisible until the operator opens the app. A notification layer closes
   the loop: the host pushes a short message to the phone.
2. **Credential hygiene.** Agents that call cloud LLM APIs directly must
   carry provider keys in their environment. A local gateway inverts this:
   keys live in one root-owned config, agents authenticate with a local
   master key, and the gateway injects provider credentials server-side.

Both services run on the build host, bind to localhost only, and are exposed
exclusively through the mesh VPN's HTTPS proxy (docs/22 §6).

## 2. Notification layer (ntfy pattern)

```text
┌──────────────────────────────┐
│  BUILD HOST                  │
│  ├─ agent / job / timer      │──► curl POST ──► ntfy (127.0.0.1:2586)
│  └─ health-check timer       │                   │ upstream relay
└──────────────────────────────┘                   ▼ (optional)
                                        push relay (APNs / FCM)
                                                   │
┌──────────────────────────────────────────────────▼─┐
│  OPERATOR PHONE — ntfy app, subscribed via         │
│  https://<host>.<tailnet>.ts.net/<topic>           │
└────────────────────────────────────────────────────┘
```

Rules of the pattern:

- The ntfy server binds to **localhost only**; the phone reaches it through
  the mesh VPN HTTPS proxy, never through an open port.
- **Topic names are bearer credentials.** Without server-side auth, whoever
  knows the topic name can publish to it. Use an unguessable random string
  (e.g. 24 hex chars), never a dictionary word; rotate it if it leaks.
- Notifications carry **neutral content only** (job names, counts, states).
  Sensitive details stay in the app or private memory — anything routed
  through an upstream relay leaves the tailnet.
- The upstream relay (`upstream-base-url`) is optional and must be verified,
  not assumed: publish a test message and poll the upstream topic to confirm
  it actually forwards — a misconfigured relay fails silently. The simpler
  default is no relay at all: the phone subscribes directly via the tailnet
  URL, and the app's instant-delivery option covers Doze.
- Every durable alert source is wired as a systemd timer or a job-completion
  hook, not as an ad-hoc manual call.

### 2.1 Server setup (Debian)

```bash
sudo apt-get install -y ntfy          # in Debian repos since trixie
sudo tee /etc/ntfy/server.yml <<'EOF'
base_url: "https://<host>.<tailnet>.ts.net"
listen-http: "127.0.0.1:2586"
behind-proxy: true
cache-file: "/var/cache/ntfy/cache.db"
EOF
# Optional: upstream relay to the public ntfy.sh for instant delivery.
# Add it only after verifying it actually forwards (publish a test, poll
# the upstream topic) — a silent relay failure means no delivery at all.
#   upstream-base-url: "https://ntfy.sh"
sudo mkdir -p /var/cache/ntfy && sudo chown _ntfy:_ntfy /var/cache/ntfy
sudo systemctl enable --now ntfy
curl -s http://127.0.0.1:2586/v1/health   # {"healthy":true}
```

### 2.2 HTTPS exposure via mesh VPN proxy

```bash
# one-time: enable Serve + HTTPS certificates for the tailnet in the
# vendor admin console (the CLI prints the exact URL when it is missing)
sudo tailscale serve --bg http://127.0.0.1:2586
curl -s https://<host>.<tailnet>.ts.net/v1/health   # {"healthy":true}
```

The phone subscribes to topic `<topic>` on that URL in the ntfy app — with
the app's instant-delivery (Doze) option enabled, alerts arrive without
per-subscription polling delays.

### 2.3 Publishing from agents and jobs

```bash
curl -s -H "Title: <source>" -d "<neutral message>" \
  http://127.0.0.1:2586/<topic>
```

Typical wiring: background-job completion hooks, scheduled sweeps
("N new items"), and agent approval requests ("waiting for GO").

### 2.4 Health-check timer (minimal monitoring)

A one-shot systemd service plus a timer (e.g. every 15 minutes) checks core
services, VPN link, disk and RAM thresholds, and publishes a high-priority
alert on failure only. A `--test` flag sends a test notification for
verification during bootstrap.

## 3. LLM gateway (LiteLLM pattern)

```text
┌──────────────────────────────┐     ┌───────────────────────────────┐
│  AGENT / TOOL ON THE HOST    │     │  LLM GATEWAY (127.0.0.1:4000) │
│  auth: local master key      │────►│  auth check, routing, logging │
└──────────────────────────────┘     │  injects provider API keys    │
                                     └───────────────┬───────────────┘
                                                     │ HTTPS (keys only here)
                                     ┌───────────────▼───────────────┐
                                     │  LLM PROVIDERS (cloud)        │
                                     └───────────────────────────────┘
```

Rules of the pattern:

- **Agents never see provider keys.** They authenticate to the gateway with
  a local master key stored in a `600` root-owned env file; the gateway
  holds the provider credentials.
- The gateway binds to **localhost only** — it is consumed by tools running
  on the host (extraction pipelines, MCP wrappers, scripts). Expose it
  through the VPN proxy only if remote clients genuinely need it.
- All calls route through one OpenAI-compatible endpoint, which gives
  per-project spend tracking, rate limiting, and provider fallback for free.
- Model onboarding is additive: append one `model_list` entry per provider
  key; nothing else changes.

### 3.1 Setup (Debian, Python 3.12+)

```bash
sudo python3 -m venv /opt/litellm
sudo /opt/litellm/bin/pip install 'litellm[proxy]'
sudo useradd -r -s /usr/sbin/nologin litellm
sudo mkdir -p /etc/litellm
# generate: LITELLM_MASTER_KEY=sk-<random 32 bytes>  ->  /etc/litellm/env (600)
# /etc/litellm/config.yaml (600):
#   model_list: []                      # filled per provider key
#   general_settings:
#     master_key: os.environ/LITELLM_MASTER_KEY
#   litellm_settings:
#     drop_params: true
```

### 3.2 systemd unit (hardened)

```ini
[Service]
User=litellm
Group=litellm
EnvironmentFile=/etc/litellm/env
ExecStart=/opt/litellm/bin/litellm --config /etc/litellm/config.yaml \
  --host 127.0.0.1 --port 4000
Restart=on-failure
NoNewPrivileges=true
ProtectHome=true
```

### 3.3 Verification

```bash
systemctl is-active litellm                     # active
curl -s http://127.0.0.1:4000/health/liveliness # I'm alive!
curl -s -H "Authorization: Bearer $MASTER_KEY" \
  http://127.0.0.1:4000/v1/models               # {"data":[...]}
```

## 4. Security model

- **Least privilege:** each service runs as its own dedicated system user
  (`_ntfy`, `litellm`) with no shell; secrets are `600` and owned by the
  service user, never world-readable, never committed.
- **Network surface:** both services bind to localhost; the only external
  path is the mesh VPN HTTPS proxy, which is reachable solely from the
  tailnet.
- **Neutral content rule:** notification bodies and titles never contain
  personal or project-sensitive details; the phone app and private memory
  are the places for context.
- **Auditability:** gateway requests are logged centrally; health checks and
  job hooks produce a journal trail per event.

## 5. Bootstrap order

1. Install and configure ntfy (localhost) → verify `/v1/health`.
2. Enable tailnet Serve/HTTPS in the vendor console → `tailscale serve` →
   verify from the host via the public tailnet URL.
3. Install the ntfy app on the phone, subscribe to the topic, send a test
   and confirm delivery end-to-end (including the upstream topic, if the
   optional relay is used).
4. Wire health-check timer and job hooks.
5. Install the LLM gateway, generate the master key, verify liveness and
   auth with an empty model list.
6. Add provider models/keys one by one; verify each with a minimal call.

## 6. Anti-patterns

- Exposing ntfy or the gateway on a public port "temporarily".
- Putting provider keys into agent environments because "it is easier".
- Sensitive content in notification bodies (it transits the push relay).
- Manual-only notifications — unwired jobs stay silent until they fail.
- Skipping the empty-model-list verification: auth must be proven to work
  before any real key is added.