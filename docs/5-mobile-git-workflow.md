# Deep Dive: Mobile-First Git Workflow

The end-to-end pipeline I use to **commit and push to GitHub entirely from my phone**, with no laptop in sight. It pairs the Agora mobile app with an AI agent that has access to a sandboxed shell.

## Why this workflow exists

"GitHub mobile app" and "cloud IDE" workflows break down when you need to:

- Bootstrap SSH keys from a cold sandbox.
- Install packages on an unfamiliar distro (Alpine ≠ Ubuntu).
- Coordinate 10+ file writes with sane commit hygiene.
- Get a human-readable diff before any push.

The AI-agent-and-sandbox approach replaces all of that with a chat conversation.

## Pipeline at a glance

```text
[ Agora App on Phone ]
        ↓
user message (+ timestamps + Active Memory)
        ↓
[ AI Agent (GLM-5.3-Flash / GPT-5.6 Luna Pro) ]
        ↓
shell calls
        ↓
[ Local Alpine Sandbox ]
        ↓
git over SSH (ed25519)
        ↓
[ GitHub ]
```

## Verified steps (July 2026)

### 1. Sandbox bootstrap

`apk update && apk add git openssh` — on Alpine this installs `git 2.47.3` and `openssh 9.9_p2` in ~10s.

### 2. SSH key + config

`ssh-keygen -t ed25519 -C "pavel@agora-sandbox" -f ~/.ssh/id_ed25519 -N ""`

Paste the output of `cat ~/.ssh/id_ed25519.pub` into **GitHub → Settings → SSH keys**.

`~/.ssh/config`:

```text
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

Permissions: `chmod 600 ~/.ssh/config`.

### 3. Trust GitHub's host key (avoid "Host key verification failed")

`ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts`

### 4. Test clone

`git clone git@github.com:<user>/<repo>.git /tmp/repo` — first run will fail with `Permission denied (publickey)` until the key is on GitHub. Re-run after pasting.

### 5. Branch first — never `main` directly

`cd /tmp/repo && git checkout -b edit-YYYY-MM-DD`

### 6. Batch writes

A good agent supports many file operation calls per turn. Use `file_write` for new files and full overwrites; use `file_edit` (exact `old_string` + `new_string` match) for surgical fixes to existing files. One logical change per commit, many files per commit.

### 7. Commit + push branch (NOT `main` yet)

`git add . && git commit -m "..." && git push -u origin edit-YYYY-MM-DD`

### 8. Merge + push `main` (only after explicit "GO")

`git checkout main && git merge --no-ff edit-YYYY-MM-DD -m "..." && git push origin main`

## Safety rules I never skip

1. **Always branch first.** Never commit directly to `main`.
2. **Always show diff before push.** `git diff --stat` is non-negotiable.
3. **Always wait for explicit "GO".** The agent must halt before every push.
4. **Use `--no-ff` on merge.** Preserves the feature branch in history.
5. **Delete the branch after merge** (optional): `git push origin --delete edit-YYYY-MM-DD`.

## What breaks (and how I recover)

| Symptom | Cause | Fix |
|---|---|---|
| `Host key verification failed` | GitHub key not in `known_hosts` | Run `ssh-keyscan` (Step 3) |
| `Permission denied (publickey)` | Key not on GitHub account | Paste `cat ~/.ssh/id_ed25519.pub` into Settings → SSH keys, retry |
| `Repository not found` | Wrong repo or no access | `git ls-remote` the SSH URL first |
| Push hangs on timeout | DNS/firewall blocks `github.com:22` | Test with `ssh -T git@github.com` |
```
