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
There is no build. Content changes are Markdown-only; `scripts/` contains
validation tooling, and CI runs the same checks on every push (see Validation).

Start reading at `docs/0-overview.md` (architecture map) and `README.md`
(what the repository contains and how to install it).

## Repository map

- `docs/` — numbered architecture documents; `docs/0-overview.md` is the map.
- `skills/` — Skills (reusable procedures), one directory per Skill with a
  `SKILL.md` inside; format defined in `skills/skill-format.md`.
- `system-prompt/` — System, User, Assistant, and Compact template guidance.
- `active-memory/` — generic Active Memory template and example.
- `tasks/` — task cards (genericized descriptions, not verbatim prompts).
- `platform/` — parameterized host-level systemd unit templates + install
  manifest (`docs/31`); placeholders only, no host-specific values.
- `scripts/` — validation checks; run before every commit.
- `manifest.yaml` — component inventory: every deployable component, its
  source, and its deployment target.
- `decisions/` — architecture decision records; index in `decisions/README.md`.
- `CHANGELOG.md` — release history and versioning policy.

## Navigating this repository

- Start at `docs/0-overview.md` (architecture map) and this file. `manifest.yaml` is the component inventory; `decisions/README.md` records why things are the way they are.
- Search with `grep -rn` (or `rg`) instead of reading directories file by file; list with `ls` or `find` before assuming a path exists.
- Read a document in full before editing it; patch anchors must match exactly once.
- Do not use web search for repository-internal questions — read the repository. Web search is for upstream (Agora application) behavior and external standards.

## Mandatory conventions

1. **Language and privacy.** All repository content is English, anonymized,
   and generic: no personal names, projects, hardware models, networks, ports,
   schedules, or family context. Personal context belongs to a private memory
   layer, never to this public repository. Sole exception: the `LICENSE`
   copyright line names the copyright holder (ADR-0014) — the privacy scan
   does not scan the LICENSE, and instance-specific identifier patterns
   live only in the instance overlay, never in repository files.
2. **Validate before committing.** Run `./scripts/check.sh` and require exit
   code 0. The script checks Skill format compliance, personal-identifier
   patterns, and relative link integrity.
3. **Skill format.** Every Skill lives at `skills/<family>/<skill-name>/SKILL.md`
   (Agent Skills layout): YAML frontmatter (`name` matching the directory,
   `description` mirroring the Catalog description, `license: MIT`) plus the
   10 required sections from `skills/skill-format.md` in the documented order.
   Author docs (`README.md`, `skill-format.md`, `skill-catalog.md`) are not
   Skills.
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
7. **Inventory.** `manifest.yaml` lists every deployable component with its
   source and deployment target. When a component is added or removed, update
   the inventory in the same change.
8. **Decision records.** Record architectural decisions as ADRs in
   `decisions/` (format in `decisions/README.md`): one decision, one file;
   never deleted — superseded ADRs keep their Status line pointing to the
   successor.

## Boundaries

Do not modify — each with its reason and what to do instead:

- `docs/` numbering — numbers are immutable; a retired number (19) stays retired. Add new documents under the next free number and update cross-references.
- `decisions/` — ADRs are recorded by the operator through the interactive agent; an autonomous task or unrequested run proposes changes in its report instead of committing them.
- `LICENSE` — the copyright line is the sole sanctioned location for the owner's real name (ADR-0014); never "correct" it to an anonymized value.
- `platform/` — templates carry placeholders only; real host values live in the instance overlay, never here.
- `.github/workflows/` — CI pipeline changes need operator review; propose them, do not push.

Requires explicit operator approval:

- changes to `system-prompt/` templates (kernel rules are always-applicable text);
- changes to `scripts/` checkers (validation-as-code is the enforcement layer);
- creating tags or releases;
- any push outside the topic-branch → `--no-ff` merge flow.

## Repository anti-patterns

Specific failure modes observed in this repository — not general advice:

- Prose file counts in `manifest.yaml` — they drift; use glob sources with a machine-checked `files:` count.
- A soft gate before commit — chaining `check.sh` with `;` instead of `&&` lets a failed check commit anyway. Hard-`&&` the gate before every commit.
- Editing on `main` directly — a forgotten `checkout -b` puts work on the wrong branch; make `checkout -b` the first command of every new unit of work.
- Rewriting only backticked `name.md` reference forms after a layout change — path-style and unbackticked references stay stale; sweep all reference styles.
- Retiring a document by renumbering the others — cross-references break; retire the number instead.
- Fixing the frontmatter `description` but not the Catalog description body (or vice versa) — the format check enforces their equality; change both in the same edit.
- Operator schedule values in repository content — clock times (HH:MM), cron
  fields, or weekday+time combinations reveal how the instance is operated.
  Genericize to relative windows ("night window, exact time instance-specific");
  the privacy scan flags `schedule_time` and `cron_schedule` outside code
  fences.

## Validation

```bash
./scripts/check.sh
```

Requires python3, git, and bash. Continuous integration runs the same checks
on every push to `main` and on pull requests (`.github/workflows/check.yml`).

- `check_format.py` — Skill section structure: 10 required sections in order,
  code fences excluded from matching.
- `privacy_scan.py` — personal-identifier pattern scan over all Markdown
  (emails, phone numbers, IPv4 addresses, home paths, family terms, names).
  Findings require human review; allowlisted generic values are documented in
  the script.
- `check_links.py` — relative Markdown links resolve to existing files.
- `check_inventory.py` — component inventory: every `manifest.yaml` source
  resolves and glob file counts match the tree.

If you add a new convention that can be checked mechanically, extend
`scripts/` instead of documenting it only.

## Definition of done

A change in this repository is done when:

- `./scripts/check.sh` exits 0 (hard `&&` before the commit);
- the diff is minimal — only what the task requires; unrelated improvements are reported, not bundled;
- affected cross-references, routing rows, and the component inventory (`manifest.yaml`) are updated in the same change;
- `CHANGELOG.md` carries an entry for user-visible changes;
- the branch is merged `--no-ff`, the run on `main` is verified `success`, and the branch is cleaned up after `merge-base --is-ancestor`;
- findings outside the task scope are reported — not silently fixed, not silently dropped.

## Last verified

2026-10-30 against the post-v1.3.0 `main` state. If this file is
older than recent merges, re-verify its claims (file map, checks, conventions)
before relying on them.