---
name: github-release-workflow
description: "Verified Git workflow from a constrained mobile sandbox and from a self-hosted build host: branches, GO rules, CI verification before merge (full mirrored log, not just the API conclusion), docs-only changes under a CI gate, CI efficiency rules, identity/deploy-key handling, a branch-cleanup gate, SSH troubleshooting, and Alpine/BusyBox gotchas."
license: MIT
---

# Skill: GitHub Release Workflow

## Catalog description
Verified Git workflow from a constrained mobile sandbox and from a self-hosted build host: branches, GO rules, CI verification before merge (full mirrored log, not just the API conclusion), docs-only changes under a CI gate, CI efficiency rules, identity/deploy-key handling, a branch-cleanup gate, SSH troubleshooting, and Alpine/BusyBox gotchas.

## Purpose
Reliable mobile-first Git workflow: safe commits, pushes, merges, and cleanup with minimal failures, including concrete gotchas of an Alpine/BusyBox sandbox. Tuned for a single developer driving everything from a phone through an AI agent: the remote CI is the only build feedback, so every run must be fast, cheap, and informative.

## Load when
- commit, push, merge, new branch, or cleanup;
- SSH/Git errors (host key, permission denied, missing repository, "detected dubious ownership", "Author identity unknown");
- git on a build host: which shell identity may touch the repository, per-repo deploy keys, single-branch clones;
- creating or adjusting a repository or its CI workflows;
- publishing content publicly (privacy check!).

## Do not load when
- Local edits without a commit;
- reading GitHub via web/API without any push need.

## Dependencies
- `tool-execution-contract` (safety layer). Context: Saved Memory holds account and key details — never the Skill file.

## Workflow

### Standard procedure (larger change)
```bash
cd /work/<repo>
git checkout -b <prefix>-YYYY-MM-DD   # or a thematic name
# edits via file_write / file_edit
git add -A
git diff --cached --check             # whitespace check
git commit -m "..."                   # identity: see "Identity and keys on a build host"
git push origin <branch>
# AFTER explicit GO from the user:
git checkout main && git merge --no-ff <branch> -m "Merge ..."
git push origin main
git merge-base --is-ancestor <branch> main \
  && git branch -d <branch> && git push origin --delete <branch>
```

### Identity and keys on a build host
- **The clone belongs to the user who works in it.** A durable background-job transport often runs commands as `root`, and git then refuses to operate on a repository owned by an unprivileged user ("detected dubious ownership"). Run git **as the owning identity** (typically the plain SSH device user); keep the job transport for long builds, image viewing and system administration. Do not paper over this with a global `safe.directory` exception.
- **A fresh clone has no `user.name`/`user.email`** → both `git commit` and `git merge` fail with "Author identity unknown". Solve it per command (`git -c user.name=… -c user.email=… commit …`) or repo-locally; never with a global identity shared between machines.
- **Per-repository deploy keys through SSH aliases**, not one account key: `~/.ssh/config` maps `Host github-<repo>` → its own `IdentityFile` + `IdentitiesOnly yes`. An account key with access to every repository is the first thing to retire.
- **Misleading warning:** `Warning: Identity file … not accessible` during a push does not mean failure — if the remote URL uses an alias, `~/.ssh/config` supplies the key and the push succeeds. Verify with `ssh -G <alias> | grep -i identityfile` instead of guessing.

### Branch state: where branches actually are
- A **single-branch clone** (`remote.origin.fetch = +refs/heads/main:…`) **never shows your own branch** as `origin/<branch>`. `git branch -a` in such a clone is not evidence about the remote.
- Read remote state with `git ls-remote --heads origin`; after fetching one branch, work through `FETCH_HEAD`.
- **Cleanup gate (mandatory before any deletion):**
  ```bash
  git fetch origin <branch>
  git merge-base --is-ancestor FETCH_HEAD main && echo "merged → safe to delete" || echo "NOT merged → keep and report"
  ```
  A branch that looks like post-merge leftovers may be unbacked work. Precedent: a feature branch with two commits that was not in `main` would have been deleted by an unconditional cleanup step.

### Trivial fixes (1–2 lines)
- Only with an explicit "commit to main" from the user — otherwise always use a branch.

### GO rules
1. **Always show diff stat before committing** — never push blind.
2. **GO from the user before pushing** — exception: explicit "send it" / "do the merge".
3. **`--no-ff` merges** — keep the branch visible in history.
4. **Cleanup after merge** — locally and on the remote, **but only after `git merge-base --is-ancestor` proves the merge** (see the cleanup gate above).
5. **Read repository state from the repository, not from memory** — a note saying "waiting for merge GO" is a hypothesis; `git log main` and `ls-remote` are evidence. Precedent: a merge that had already landed three hours earlier kept being reported as pending.
6. **CI verification before merge** — an API conclusion of "success" is NOT sufficient; required depth is defined in "CI verification before merge" below. Precedent: a real incident where `tee` without `pipefail` masked an assembleDebug failure, producing a falsely green run with an empty APK artifact.

### CI verification before merge (required depth)
| Run type | Required check |
|---|---|
| Run on a feature branch | API conclusion + JUnit summary (test counts) |
| **Merge run on main** | **Full mirrored log**: both `BUILD SUCCESSFUL` (unit tests and assembleDebug), JUnit XML — total count matches expectations, 0 failures / skipped / errors, 0 deprecation warnings and `e:`/javac errors |

- Read the full log via: `git fetch origin <log-branch> && git show origin/<log-branch>:<log-path>` (e.g. a `ci-logs` branch mirrored by the CI workflow).
- **Gotcha:** `raw.githubusercontent.com` may briefly serve a stale file (CDN cache) — verify via `git show` after fetch and check the file header (`# CI run N — commit <sha>`) matches the run being verified.
- Prerequisite: the CI must mirror full logs to a public branch; without such mirroring these rules cannot be followed — set it up first.

### Docs-only changes under a CI gate
Purely documentary edits (README, `*.md`, `docs/**`) do not change code, but in a repository with CI they still trigger a check run unless the workflow excludes doc paths.

- Repository with CI: put doc paths into `paths-ignore` in the workflow, otherwise the run starts anyway — and when it starts, verify `conclusion=success` like any other run. Repository without CI: nothing to do — there are no runs.
- Docs-only merge in a repository with CI: verify the run outcome for the merge head (`conclusion=success`, or a confirmed absence of a run only when `paths-ignore` covers the changed paths), plus the standard diff stat and local–remote sync. In a repository without CI: verify that Actions did not start a run for that commit (API / Actions UI — no run for the SHA).
- Beware mixed commits (docs + code): `paths-ignore` does not apply, full CI depth per the table above.
- `.github/workflows/*` are NOT docs — a workflow change always triggers CI.

### CI efficiency rules (when creating or tuning a workflow)
A mobile-only developer pays for every CI minute with waiting time.

1. **Concurrency with cancel-in-progress** — push-heavy iteration otherwise stacks parallel runs (every push starts its own run); a newer push should cancel the superseded run of the same branch:
   ```yaml
   concurrency:
     group: ${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true
   ```
2. **`timeout-minutes` on every job** — a hung job silently eats minutes; set an explicit ceiling.
3. **`paths-ignore` for docs** — see the section above.
4. **Shallow checkout is the default** — `actions/checkout` fetches `fetch-depth: 1`; a job that needs history or tags must set `fetch-depth: 0` explicitly.
5. **Use official build-tool actions with caching** — for Gradle/Android, `gradle/actions/setup-gradle` validates the wrapper and caches dependencies plus build outputs (community reports ~15x faster CI builds); it replaces a manual `chmod +x gradlew`.

### CI polling without a token
On public repositories, run statuses and conclusions are readable through the REST API without authentication (logs are not — they return 403):

```bash
wget -qO- "https://api.github.com/repos/<owner>/<repo>/actions/runs?per_page=3" \
  | grep -o '"status": *"[^"]*"\|"conclusion": *"[^"]*"'
```

Poll pattern: `for i in $(seq 1 18); do sleep 15; <check>; done` — the agent verifies CI itself instead of sending the user to the Actions tab.

### Backup ref before destructive operations
Before any force push, history rewrite, or non-standard branch deletion:

```bash
git push origin <branch>:refs/heads/backup/<branch>-<YYYY-MM-DD>
git ls-remote --exit-code --heads origin backup/<branch>-<YYYY-MM-DD>
```

Only proceed with the destructive step after the backup ref provably exists on the remote.

### SSH troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| Host key verification failed | GitHub not in known_hosts | `ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts` |
| Permission denied (publickey) | Key not registered on GitHub | `cat ~/.ssh/<key>.pub` -> Settings -> SSH keys |
| Could not resolve hostname <alias> | SSH alias without config | `GIT_SSH_COMMAND='ssh -F ~/.ssh/config-<name>' git push ...` |
| Repository does not exist | Typo in remote URL | `git remote -v` and correct |
| "detected dubious ownership" | Git runs as a different user than the clone owner | run git as the owning identity (not a global `safe.directory` exception) |
| "Author identity unknown" | No user.name/user.email in a fresh clone | `git -c user.name=… -c user.email=… commit …` |
| "Identity file … not accessible" warning, push still succeeds | The SSH alias supplied the key, not `-i` | `ssh -G <alias> | grep -i identityfile` |
| `git branch -a` misses a pushed branch | Single-branch fetch refspec | `git ls-remote --heads origin` |
| Author identity unknown | No user.name/user.email in a fresh clone | `git -c user.name=... -c user.email=... commit ...` (repo-local) |

### Sandbox gotchas (Alpine/BusyBox)
- **`grep` has no `--exclude-dir`** — use `python3` for complex searches.
- **`find` has no `-printf`** — use `-print` or python.
- **`curl` is not in Alpine** — use `wget`, `git ls-remote`, `ssh-keyscan`.
- **`git diff --cached <file>`** fails in busybox git — call it without a path, or without `--cached`.
- **`git add .` without `cd`/`workdir`** — fails with "not a git repository".
- **`file_edit` on lines with trailing spaces** — silent match failure; solve via python/sed.
- **The shell mangles quotes/backslashes** (python3 heredocs) — verify the result; prefer file_write/file_edit over heredocs.
- **A stale or corrupt local clone** — re-clone shallow into a fresh directory instead of repairing.
- **Pushes made with `GITHUB_TOKEN` do not trigger new workflow runs** (exceptions: `workflow_dispatch`, `repository_dispatch`) — CI-to-CI pushes are loop-free, but a bot push that should trigger CI needs a PAT.
- **GitHub e-mails the account owner when a workflow run fails** (default) — a free safety net for phone-only monitoring.
- **API rate limit 60 requests/h without a token** — batch status checks; statuses and artifacts of public repos are readable without auth.
- **Transient GitHub "Internal Server Error"** — retry; usually passes on the second attempt.

### Privacy check (before EVERY push to a public repo!)
- No family names, addresses, phone numbers, e-mails, business IDs, salary data.
- No sensitive domain-specific metadata that should stay internal.
- All public repo content: English, anonymized, generic.

## Forbidden behavior
- Pushing without GO unless explicit consent was given.
- Never pushing to `main` without GO or an explicit exception.
- Never pushing personal data into a public repo.
- Never deleting a branch before verifying the merge succeeded — with `merge-base --is-ancestor`, not with a feeling.
- Never treating `git branch -a` of a single-branch clone as proof about remote state.
- Never running git as root inside clones owned by an unprivileged service user.
- Never force pushing, rewriting history, or deleting a remote branch without a verified backup ref and explicit GO for the exact scope.

## Verification
- After push: `git log --oneline -3` + `git status --short --branch` (in sync with remote) + `git ls-remote --heads origin` for your own branches.
- After a merge: the merged content is provably on the remote (`git show main:<file>`, or the raw URL with a check that it is not a stale CDN copy).
- After merge: cleanup done, `git branch` clean, **CI run on main verified with the full mirrored log (see "CI verification before merge")**; for docs-only merges in a repo with CI, verified the run outcome (`conclusion=success`, or absence only under `paths-ignore`).
- Before push: privacy check passed (or the repository is private).

## Output contract
- What was performed (commit hash, branches, push status).
- Verification: local = remote sync.
- Any gotchas encountered and how they were resolved.

## Sources
v1.0 — distilled from hands-on mobile-first Git operations in a constrained Alpine/BusyBox sandbox; anonymized and generalized for public sharing.
v1.1 — added the CI verification gate before merge (full mirrored log for merge runs; an API conclusion alone is insufficient), including the CDN-cache gotcha of raw log reads.
v1.3 — added build-host reality: shell identity vs. repository ownership ("dubious ownership"), missing commit identity in fresh clones, per-repo deploy keys behind SSH aliases, single-branch clones hiding remote branches, and a mandatory `merge-base` gate before branch cleanup; anonymised 2026-10-12.
v1.2 — added docs-only changes under a CI gate, CI efficiency rules (concurrency + cancel-in-progress, job timeouts, paths-ignore, shallow checkout, Gradle caching), token-less CI polling, backup refs before destructive operations, and the GITHUB_TOKEN / notification / rate-limit gotchas. Cross-checked against GitHub Docs (workflow concurrency, triggering workflows) and gradle/actions docs, 2026-09-26.
