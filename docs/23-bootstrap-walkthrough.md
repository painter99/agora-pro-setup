# 23 — Bootstrap walkthrough: from bare laptop to agent-operated build host

> Companion to docs/22. Where docs/22 defines the architecture pattern, this
> document records the concrete, ordered instantiation of that pattern as it was
> executed on a real host — step by step, with the commands that were actually
> run and the verification used at each step. Generic by design: interface
> names, addresses and credentials appear as placeholders; personal specifics
> (hardware models, network names, passwords, project names) stay in the
> operator's private memory, never in this repository.

## 1. Scope and assumptions

- Host: an idle x86_64 machine (laptop or mini-desktop), ~16 GB RAM, local disk.
- OS: current stable Debian, installed from the netinst image, **headless**
  (no desktop environment), SSH server selected in the installer.
- Orchestrator: the Agora app on the operator's phone (local sandbox + shell
  devices). The agent never touches the host directly; every action is a tool
  call relayed by the app (docs/22 §1).
- End state of this walkthrough: host boots unattended, network persists across
  reboots, SSH server runs, baseline packages installed, agent access verified,
  toolchain and first build verified, durable-jobs transport active, remote
  access via mesh VPN.

## 2. Phase overview

| Phase | What happens | Who executes | Verified by |
|---|---|---|---|
| 0 | OS install (netinst, headless) | operator | login prompt on console |
| 1 | firmware: auto-power-on | operator | host returns after power loss |
| 2 | network: recovery + persistence | operator at console | lease + ping + **reboot test** |
| 3 | baseline packages + ergonomics | operator at console | package list, lid behavior |
| 4 | agent access (SSH device) | operator in app UI | first remote command |
| 5 | toolchain (JDK, SDK) | agent over SSH | version outputs |
| 6 | jobs transport (Conch) | agent + app UI | durable job + image view |
| 7 | remote access (mesh VPN) | operator in browser + app UI | tailnet ping, both transports |

Every phase below is documented as executed and verified — the walkthrough
records verified reality, not intentions.

The division of labor is the point of the pattern: the operator does only what
physically requires a human — installing, firmware, the first network
recovery, approvals in UIs. Everything after the first SSH connection is the
agent's work.

## 3. Phase 0 — OS install

**Executed by:** operator at the console.

- Netinst USB; tasksel selection: **SSH server + standard system utilities
  only**. No desktop environment — the agent "sees" through rendered artifacts
  and shell outputs, not through a GUI (docs/22 §3).
- Hostname and unprivileged user of the operator's choice; root account locked
  (administration happens via `sudo` from the user).
- Whole-disk guided partitioning (ESP + ext4 root + swap) is sufficient for a
  stateless build host; `noatime` tuning is applied later.

Lessons:

- `sudo` asks for the **user's** password, not root's.
- A keyboard-layout mismatch (e.g. national vs US layout) changes typed
  characters — when a "correct" password is rejected at the console, suspect
  the layout before anything else.

## 4. Phase 1 — firmware

**Executed by:** operator in the firmware setup.

- Enable **auto-power-on** (firmware labels vary by vendor; one common label is
  "Power On with AC Attach"). A headless host must return by itself after a
  power cut — this is what makes the "no uptime guarantees" model workable.
- Leave Secure Boot enabled; current stable Debian supports it.
- Nothing else is changed in firmware.

## 5. Phase 2 — network (the realistic part)

**Executed by:** operator at the console (guided step by step); the agent
verifies over SSH as soon as it exists.

### 5.1 What actually broke after the first reboot

The installer had configured the network **for the interface used during
installation** (often Wi-Fi). On the installed system:

- the wired NIC had **no stanza at all** → it stayed administratively DOWN;
- the DHCP client (`dhcpcd`) was present as a binary, but nothing started it:
  Debian's dhcpcd ships **no systemd unit** (`systemctl is-enabled dhcpcd` →
  `not-found` is normal, not an error) — boot networking belongs to ifupdown;
- DNS resolution failed (`Temporary failure resolving`), so apt fetches failed.

Diagnosis (three read-only commands):

```
ip -br a
ip route
cat /etc/resolv.conf
```

Reading the interfaces file settled the diagnosis:

```
sudo cat /etc/network/interfaces
```

### 5.2 One-time manual recovery (at the console)

```
sudo ip link set <wired-iface> up
sudo dhcpcd <wired-iface>
ping -c3 deb.debian.org
```

`dhcpcd` obtains a lease, adds routes and writes `resolv.conf` — the host is
online. This state is **not persistent**; it exists only until reboot.

### 5.3 Persistence via ifupdown

Boot-time networking is configured in `/etc/network/interfaces`. Both
transports can coexist; the operator's preference decides the default:

```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

# Wi-Fi (operator's preferred transport)
auto <wifi-iface>
iface <wifi-iface> inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

# Wired ethernet (backup; primary whenever the cable is plugged)
auto <wired-iface>
iface <wired-iface> inet dhcp
```

Wi-Fi credentials: if the passphrase contains **special characters** (quotes,
spaces), do not inline it as `wpa-ssid`/`wpa-psk` — generate a hashed config
instead. The hash is immune to escaping problems and leaves no plaintext:

```
read -s -p "Wi-Fi passphrase: " PSK && echo
wpa_passphrase "<SSID>" "$PSK" | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null
sudo sed -i '/#psk=/d' /etc/wpa_supplicant/wpa_supplicant.conf
sudo chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf
unset PSK
```

Notes:

- `auto` (not `allow-hotplug`) is the deterministic choice for fixed internal
  NICs; dhcpcd waits for carrier, so a cable plugged in later still gets a
  lease.
- **The reboot test is the only real verification** of persistence: reboot,
  log in, then `ip -br a` + `ping -c3 deb.debian.org`.
- Optional but recommended: a DHCP reservation in the router for a stable
  address; a mesh VPN (docs/22 §3) later removes IP dependence entirely.

## 6. Phase 3 — baseline packages and host ergonomics

**Executed by:** operator at the console.

Package batch (docs/22 §3 baseline; GUI tools stay on-demand):

```
sudo apt update && sudo apt install -y \
  curl git tmux unzip jq ufw smartmontools openssh-client python3-venv \
  wpasupplicant
```

(`wpasupplicant` only when Wi-Fi is used; it is also required for the
`wpa-conf` stanza above.)

Lid switch — a laptop host must not suspend when the lid closes:

```
sudo mkdir -p /etc/systemd/logind.conf.d
printf '[Login]\nHandleLidSwitch=ignore\n' | sudo tee \
  /etc/systemd/logind.conf.d/lid-ignore.conf
sudo systemctl reload systemd-logind
```

Hardware verification (read-only; results are recorded privately, not in this
repository):

```
lscpu | grep -E 'Model name|^CPU\(s\)'
lspci | grep -iE 'vga|3d|network'
```

## 7. Phase 4 — agent access (the handover moment)

**Executed by:** operator in the app UI; the agent verifies.

In the app: **Settings → Shell Devices → SSH** with host, port, user and
password (key-only hardening is a later step; docs/22 §3 auth row). Then the
first verification command, executed by the agent over SSH:

```
hostname && whoami && uname -a && nproc && free -h | head -2 && df -h / | tail -1
```

Expected: the chosen hostname, the unprivileged user, the expected kernel,
thread count, RAM and free disk. From this moment the operator does not touch
the console anymore — the agent works over SSH, and the physical bootstrap
chicken-and-egg (docs/22 §7) is resolved: the console was needed only until SSH
worked.

## 8. Phase 5 — toolchain and first build

**Executed by:** the agent over SSH.

JDK from the distro (version chosen against the project's Android Gradle
plugin):

```
sudo apt install -y openjdk-21-jdk-headless
java -version && javac -version
```

Android SDK under `/opt/android-sdk`:

```
sudo mkdir -p /opt/android-sdk/cmdline-tools
wget -P /tmp https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
sudo unzip -q /tmp/commandlinetools-linux-11076708_latest.zip -d /opt/android-sdk/cmdline-tools
sudo mv /opt/android-sdk/cmdline-tools/cmdline-tools /opt/android-sdk/cmdline-tools/latest
```

**Ownership gotcha:** a directory created with `sudo` is root-owned; the SDK
manager then fails with `Failed to read or create install properties file`
(exit code 1). On a single-user agent host the clean model is a user-owned
SDK:

```
sudo chown -R <user>:<user> /opt/android-sdk
```

Licenses and packages — a long step, run it in `tmux` and poll the log:

```
tmux new-session -d -s sdk \
  'yes | /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager \
   "platforms;android-35" "build-tools;35.0.0" "platform-tools" \
   > /tmp/sdk.log 2>&1'
tail -5 /tmp/sdk.log        # poll until done
```

Project and build configuration:

```
git clone --depth 20 https://github.com/<org>/<project>.git ~/work/<project>
cd ~/work/<project>
echo "sdk.dir=/opt/android-sdk" > local.properties
printf 'org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g\norg.gradle.parallel=true\norg.gradle.caching=true\n' > ~/.gradle/gradle.properties
```

**Wrapper gotcha:** the Gradle wrapper's default network timeout (10 s) is too
aggressive on slower links — the distribution download fails with
`SocketTimeoutException`. Add `networkTimeout=60000` to
`gradle/wrapper/gradle-wrapper.properties` (supported since Gradle 8).

The full unit-test suite runs inside `tmux`:

```
tmux new-session -d -s build \
  './gradlew testDebugUnitTest > /tmp/build.log 2>&1'
```

Verification reads the JUnit XML results from the module's build directory
(`app/build/test-results/testDebugUnitTest/`) and sums `tests`, `failures`,
`errors` and `skipped` — the totals must match the project's CI baseline.

Measured on this host: the cold run (wrapper download + all dependencies +
compile + full suite) took ≈ 6 minutes wall; a warm no-op rerun takes ≈ 1 s
(daemon + caches). The agent now runs tests and reads failures without any CI
round trip.

## 9. Phase 6 — durable jobs transport (Conch)

**Executed by:** the agent over SSH; the final device entry by the operator in
the app UI.

Conch (docs/22 §3, §6) is a single static binary serving shell execution with
durable background jobs and image retrieval. Install in **system mode**
(machine-wide systemd service — runs at boot without any user login; the
user-mode variant would need lingering on a headless host):

```
wget -qO /tmp/conch-install.sh \
  https://raw.githubusercontent.com/newo-ether/conch/main/scripts/install.sh
# inspect the script, then:
sudo bash /tmp/conch-install.sh --mode system -y \
  --api-key "$(head -c 32 /dev/urandom | base64 -w0)"
```

Gotchas:

- Without a TTY the installer hangs on its confirmation prompt — `-y` skips
  prompts. A hung run is killed by PID (not by a name pattern) and re-run; an
  existing installation is detected and upgraded in place, and override flags
  are refused during an upgrade.
- Configuration lives in `/etc/conch/env` (root-only, mode 600); the **server
  public key** for the app's end-to-end encryption is printed by the service at
  startup — read it from the journal: `journalctl -u conch`.

App side: Settings → Shell Devices → Conch with the server URL — **the URL
must include the scheme** (`http://<host>:14216`; a bare host:port is
rejected) — plus the API key and the server public key.

Verified capabilities on this host: foreground commands; a durable background
job (start → job id → wait → result, surviving client disconnects); and image
viewing — a PNG generated server-side and read through the image tool, which
gives the agent its "eyes" for rendered artifacts (docs/22 §3 "How the agent
sees").

## 10. Phase 7 — remote access (mesh VPN)

**Executed by:** the agent over SSH; approvals by the operator in the browser
and app UI.

Tailscale on the host (the official installer adds the apt repository):

```
wget -qO /tmp/ts-install.sh https://tailscale.com/install.sh
sudo bash /tmp/ts-install.sh
tmux new-session -d -s tsup 'sudo tailscale up > /tmp/ts-up.log 2>&1'
cat /tmp/ts-up.log        # contains the authentication URL
```

The printed `https://login.tailscale.com/a/…` URL is opened in **any** browser
— the operator approves the device from the phone; no console needed. The
phone client installs from F-Droid or the vendor's GitHub releases (no Play
services required) and logs into the same account.

Android VPN settings for a split-tunnel tailnet:

- **Always-on VPN: on** — the client reconnects itself after reboots and
  network changes.
- **"Block connections without VPN": off** — lockdown mode forces all traffic
  into the tunnel; without an exit node, internet-bound traffic is dropped and
  the phone loses connectivity. The kill switch only fits full-tunnel use
  (exit node), which is not this pattern.

Firewall — the default-deny policy would block tailnet traffic to the host;
allow the agent ports on the tailnet interface:

```
sudo ufw allow in on tailscale0 to any port 22 proto tcp
sudo ufw allow in on tailscale0 to any port 14216 proto tcp
```

Devices receive stable CGNAT-range addresses (`100.x.y.z`); the same address
works on the LAN and from anywhere, so the app's shell devices are switched to
the tailnet address once. Verified on this host: a direct (non-relayed)
connection between phone and host, and both transports answering over the
tailnet from mobile data.

## 11. Gotchas learned on this host

- The installer's stanza covers **only the install-time interface** — check
  both NICs after the first boot, not just the one that worked in the
  installer.
- A minimal target system may lack the package that services installer-written
  options (e.g. WPA integration) — a stanza can be syntactically present and
  still dead until the package is installed.
- `dhcpcd` without a systemd unit is normal on Debian; persistence lives in
  ifupdown, not in a service.
- The raw console has no clipboard: minimize manual typing, prefer single
  commands, and enter secrets through `read -s` so they stay out of shell
  history.
- Reading root-owned files needs `sudo` — `cat: Permission denied` is not a
  failure state, just a reminder.
- Verify every mutation by reading the file back (`sudo cat …`) before moving
  on; a typo in a heredoc is otherwise discovered only at the next reboot.

## 12. Cross-references

- Architecture, rationale and the generic baseline: **docs/22** (§3 baseline,
  §5 state contract, §7 bootstrap sequence).