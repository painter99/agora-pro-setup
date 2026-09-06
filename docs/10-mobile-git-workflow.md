# Mobile-first Git workflow

End-to-end Git from a phone through Agora + a sandbox or SSH host. No laptop required.

## Pipeline

```text
[ Agora on phone ]
        ↓
System + User templates + Active Memory + Skill Catalog
        ↓
[ Model + tools ]
        ↓
Local Sandbox or your Linux/Conch host
        ↓
git over SSH (ed25519) or HTTPS + PAT
        ↓
[ GitHub ]
```

GitHub is **not** an Agora Shell device.

## Safe sequence

1. Inspect the repo (`git status`, `git log`).
2. Create a branch. Never commit first on `main`.
3. Small logical change.
4. `git diff --stat` (and the diff) before commit.
5. Commit.
6. **Explicit GO** before every push.
7. Merge to `main` only after a second explicit GO.

## Bootstrap notes (Alpine sandbox)

```text
apk update && apk add git openssh
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
# paste .pub into GitHub → Settings → SSH keys
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts
```

Use a dedicated key when possible. Do not paste private keys into chat.

## Recoveries

| Symptom | Likely cause | Fix |
|---|---|---|
| Host key verification failed | missing `known_hosts` | `ssh-keyscan` |
| Permission denied (publickey) | key not on GitHub | add `.pub`, retry |
| Repository not found | wrong URL or access | `git ls-remote` |
| HTTPS username prompt | no credential helper | SSH remote, or PAT via helper — never embed token in URL committed to git |

Pushing is an external publish. Treat it as high-trust.
