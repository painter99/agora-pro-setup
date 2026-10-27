# AGENTS.md

Standing instructions for AI coding agents working in this repository.
`README.md` is written for humans; this file is the agent-facing entry point.
It follows the cross-tool [AGENTS.md](https://agents.md) convention.

## Precedence rule (read first)

If any instruction in this file, in `docs/`, or in any Skill conflicts with the
observed state of the repository (actual files, actual `scripts/check.sh`
results, actual git history), verify the observed state first and prefer it;
report the conflict instead of silently following either source. Stale
instructions are a known failure mode for coding agents; this repository is
maintained against observed reality (see `docs/28-update-observability.md`).

## What this repository is

A documentation-and-governance layer for the
[Agora](https://github.com/newo-ether/Agora) application: prompt templates,
Active Memory guidance, Skills, operational documentation, and task cards.
There is no build and no CI. Content changes are Markdown-only; `scripts/`
contains validation tooling only.

Start reading at `docs/0-overview.md` (architecture map) and `README.md`
(what the repository contains and how to install it).

## Repository map

- `docs/` — numbered architecture documents; `docs/0-overview.md` is the map.
- `skills/` — Skills (reusable procedures); format defined in
  `skills/skill-format.md`.
- `system-prompt/` — System, User, Assistant, and Compact template guidance.
- `active-memory/` — generic Active Memory template and example.
- `tasks/` — task cards (genericized descriptions, not verbatim prompts).
- `scripts/` — validation checks; run before every commit.
- `CHANGELOG.md` — release history and versioning policy.

## Mandatory conventions

1. **Language and privacy.** All repository content is English, anonymized,
   and generic: no personal names, projects, hardware models, networks, ports,
   schedules, or family context. Personal context belongs to a private memory
   layer, never to this public repository.
2. **Validate before committing.** Run `./scripts/check.sh` and require exit
   code 0. The script checks Skill format compliance, personal-identifier
   patterns, and relative link integrity.
3. **Skill format.** Every file under `skills/` (except `README.md`,
   `skill-format.md`, and `skill-catalog.md`) must carry the 10 required
   sections from `skills/skill-format.md`, in the documented order.
4. **Docs numbering.** Never renumber existing documents. A retired document
   keeps its number unused (19 is retired); new documents take the next free
   number. Update cross-references when moving or retiring content.
5. **No upstream duplication.** Do not copy content that exists in the
   official Agora repository or user manual; link to it instead. This
   repository is a clean add-on layer.
6. **Branch workflow.** Work on a topic branch (`<topic>-YYYYMMDD`), commit
   with a clear message, show the diff stat, and wait for explicit operator
   approval before pushing or merging. Merges to `main` are `--no-ff`; branch
   cleanup only after `git merge-base --is-ancestor` verification.

## Validation

```bash
./scripts/check.sh
```

Requires python3, git, and bash.

- `check_format.py` — Skill section structure: 10 required sections in order,
  code fences excluded from matching.
- `privacy_scan.py` — personal-identifier pattern scan over all Markdown
  (emails, phone numbers, IPv4 addresses, home paths, family terms, names).
  Findings require human review; allowlisted generic values are documented in
  the script.
- `check_links.py` — relative Markdown links resolve to existing files.

If you add a new convention that can be checked mechanically, extend
`scripts/` instead of documenting it only.

## Last verified

2026-10-27 against `main` @ `dfae1bc`. If this file is older than recent
merges, re-verify its claims (file map, checks, conventions) before relying
on them.