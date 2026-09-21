# Skill: GitHub Release Workflow

## Catalog description

Verified Git workflow from a constrained mobile sandbox: branches, GO rules, CI verification before merge (full mirrored log, not just the API conclusion), SSH troubleshooting, and Alpine/BusyBox gotchas.

## Purpose

Reliable mobile-first Git workflow: safe commits, pushes, merges, and cleanup with minimal failures, including concrete gotchas of an Alpine/BusyBox sandbox.

## Load when

- commit, push, merge, new branch, or cleanup;
- SSH/Git errors (host key, permission denied, missing repository);
- creating or adjusting a repository;
- publishing content publicly (privacy check!).

## Do not load when

- Local edits without a commit;
- reading GitHub via web/API without any push need.

## Dependencies

- `tool-execution-contract.md` (safety layer). Context: Saved Memory holds account and key details — never the Skill file.

## Workflow

### Standard procedure (larger change)
```bash
cd <workdir>/<repo>
git checkout -b <prefix>-YYYY-MM-DD   # or a thematic name
# edits via file_write / file_edit
git add -A
git diff --cached --check             # whitespace check
git commit -m "..."
git push origin <branch>
# AFTER explicit GO from the user:
git checkout main && git merge --no-ff <branch> -m "Merge ..."
git push origin main
git branch -d <branch> && git push origin --delete <branch>
```

### Trivial fixes (1–2 lines)
- Only with an explicit "commit to main" from the user — otherwise always use a branch.

### GO rules
1. **Always show diff stat before committing** — never push blind.
2. **GO from the user before pushing** — exception: explicit "send it" / "do the merge".
3. **`--no-ff` merges** — keep the branch visible in history.
4. **Cleanup after merge** — locally and on the remote.
5. **CI verification before merge** — an API conclusion of "success" is NOT sufficient; required depth is defined in "CI verification before merge" below. Precedent: a real incident where `tee` without `pipefail` masked an assembleDebug failure, producing a falsely green run with an empty APK artifact.

### CI verification before merge (required depth)
| Run type | Required check |
|---|---|
| Run on a feature branch | API conclusion + JUnit summary (test counts) |
| **Merge run on main** | **Full mirrored log**: both `BUILD SUCCESSFUL` (unit tests and assembleDebug), JUnit XML — total count matches expectations, 0 failures / skipped / errors, 0 deprecation warnings and `e:`/javac errors |

- Read the full log via: `git fetch origin <log-branch> && git show origin/<log-branch>:<log-path>` (e.g. a `ci-logs` branch mirrored by the CI workflow).
- **Gotcha:** `raw.githubusercontent.com` may briefly serve a stale file (CDN cache) — verify via `git show` after fetch and check the file header (`# CI run N — commit <sha>`) matches the run being verified.
- Prerequisite: the CI must mirror full logs to a public branch; without such mirroring these rules cannot be followed — set it up first.

### SSH troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| Host key verification failed | GitHub not in known_hosts | `ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts` |
| Permission denied (publickey) | Key not registered on GitHub | `cat ~/.ssh/<key>.pub` -> Settings -> SSH keys |
| Could not resolve hostname <alias> | SSH alias without config | `GIT_SSH_COMMAND='ssh -F ~/.ssh/config-<name>' git push ...` |
| Repository does not exist | Typo in remote URL | `git remote -v` and correct it |
| Author identity unknown | No user.name/user.email in a fresh clone | `git -c user.name=... -c user.email=... commit ...` (repo-local) |

### Sandbox gotchas (Alpine/BusyBox)
- **`grep` has no `--exclude-dir`** — use `python3` for complex searches.
- **`find` has no `-printf`** — use `-print` or python.
- **`curl` is not in Alpine** — use `wget`, `git ls-remote`, `ssh-keyscan`.
- **`git diff --cached <file>`** fails in busybox git — call it without a path, or without `--cached`.
- **`git add .` without `cd`/`workdir`** — fails with "not a git repository".
- **`file_edit` on lines with trailing spaces** — silent match failure; solve via python/sed.
- **A stale or corrupt local clone** — re-clone shallow into a fresh directory instead of repairing.

### Privacy check (before EVERY push to a public repo!)
- No family names, addresses, phone numbers, e-mails, business IDs, salary data.
- No sensitive domain-specific metadata that should stay internal.
- All public repo content: English, anonymized, generic.

## Forbidden behavior

- Pushing without GO unless explicit consent was given.
- Never pushing to `main` without GO or an explicit exception.
- Never pushing personal data into a public repo.
- Never deleting a branch before verifying the merge succeeded.

## Verification

- After push: `git log --oneline -3` + `git status --short --branch` (in sync with remote).
- After merge: cleanup done, `git branch` clean, **CI run on main verified with the full mirrored log (see "CI verification before merge")**.
- Before push: privacy check passed (or the repository is private).

## Output contract

- What was performed (commit hash, branches, push status).
- Verification: local = remote sync.
- Any gotchas encountered and how they were resolved.

## Sources

v1.0 — distilled from hands-on mobile-first Git operations in a constrained Alpine/BusyBox sandbox; anonymized and generalized for public sharing.
v1.1 — added the CI verification gate before merge (full mirrored log for merge runs; an API conclusion alone is insufficient), including the CDN-cache gotcha of raw log reads.
