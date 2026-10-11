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
  reboots, SSH server runs, baseline packages installed, agent access verified.

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

Phases 0–4 are documented below as executed. Phases 5–6 are appended to this
document only after they are executed and verified — the walkthrough records
verified reality, not intentions.

## 3. Phase 0 — OS install

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

- Enable **auto-power-on** (firmware labels vary by vendor; one common label is
  "Power On with AC Attach"). A headless host must return by itself after a
  power cut — this is what makes the "no uptime guarantees" model workable.
- Leave Secure Boot enabled; current stable Debian supports it.
- Nothing else is changed in firmware.

## 5. Phase 2 — network (the realistic part)

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

## 8. Phases 5–6 — toolchain and jobs transport (to be appended)

The remaining phases follow docs/22 §3 and §6 and will be appended here as
executed and verified:

- **Phase 5 — toolchain:** distro JDK (verified against the project's Android
  Gradle plugin), Android SDK under `/opt`, project clone over HTTPS (public
  repositories; deploy keys are only for push), Gradle heap sized to real RAM,
  long builds run inside `tmux` and polled in batches.
- **Phase 6 — jobs transport:** Conch as a single static binary + systemd unit
  + API key, reachable from the LAN/VPN only; adds durable background jobs and
  image viewing (docs/22 §3 "How the agent sees").

## 9. Gotchas learned on this host

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

## 10. Cross-references

- Architecture, rationale and the generic baseline: **docs/22** (§3 baseline,
  §5 state contract, §7 bootstrap sequence).