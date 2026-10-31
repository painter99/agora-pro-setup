# Changelog

All notable changes to this repository are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning is semantic (MAJOR.MINOR.PATCH) and tagged. Each release records
the Agora app baseline it was maintained against.

## [Unreleased]

### Added

- New Skill `skills/memory-governance/file-based-active-memory/SKILL.md`: content
  policy and read/write discipline for the working state file that replaces
  injected Active Memory (file-based active memory); ADR-0017; docs/4 rewritten
  as the file-based-AM design; manifest skill-set 25→24, decision-records 17→18.
- New Skill `skills/coding/coding-loop/SKILL.md`: goal-based coding loop (spec
  gate, small increments, tested steps, second-agent review, bounded fix
  rounds, anti-reward-hacking guards). New `coding` family with Treat line,
  TEC domain routing row, manifest skill-set 27→28.
- New `docs/32-coding-workflow.md`: the coding layer — loop in practice,
  scripts-repository versioning pattern, per-effect-class testing policy;
  ADR-0016 (human-gated coding loop as a Skill); routing in docs/0 + README;
  manifest docs 31→32, decisions 16→17.
- coding-loop Skill: reviewer mechanics specified — the fresh-context reviewer
  is a one-off scheduled task (self-contained prompt, single review file,
  deleted after the verdict is verified, must not recur); a Loop or a
  same-conversation re-read does not count as a fresh context (D-20261030-03).
  Task-management tool names (`create_task`/`delete_task`/`list_tasks`) named
  with a defer note to the current toolset. Review-task prompt contract added:
  the creating agent owns the reviewer's prompt (role, reads, checks, single
  write target, hard rules — fill-in template; missing item = task not ready
  to create).

### Changed

- Memory gate (kernel sentence, docs/20) and the memory-governance Skills:
  current-status writes route to file tools via `file-based-active-memory`; the
  maintained instance no longer uses injected Active Memory
  (`update_active_memory` unused); docs/1, 2, 3, 5, 6, 13, 18, 22, 30 aligned.
- coding-loop Skill hardening from the first dogfood run (D-20261030-04):
  spec gate now requires a test path per behavior and malformed-input
  coverage; reviewer mechanics add the shell-time rule for the cron (`date`,
  never conversation context; verify `next_run_at`), diff freshness proof,
  final-content attachment for edits, immediate task deletion after the
  verdict (one-off crons recur yearly), a two-sleep-check wait pattern, a
  fix-round review policy (minor fixes = re-tests; behavior/spec fixes =
  fresh re-review), and independent second-method verification at the
  acceptance gate.
- `docs/32` testing policy: test framework convention added (standard-library
  `unittest` default, `python3 <test>.py`).

### Removed

- Retired Skills `active-memory-design` and `active-memory-authority` (the
  file-based-AM switch; their invariants moved into `file-based-active-memory`).
- Removed the `active-memory/` template and example (injected-AM templates;
  content recoverable from git history).
- Removed the repo-only `skills/examples/` family (two minimal format demos
  and the event photo-sharing operator template): zero local use, removes
  the 28-vs-25 skill-count mismatch and the weekly mirror-check repo-only
  exception; content remains recoverable from git history. Manifest skill-set
  28→25; mirror-check coverage clause and docs/2 example note updated.

## [1.3.0] - 2026-10-30

Checker hardening and privacy purge, process-design Skill, night task
schedule, self-improvement loop v3.1 (full-catalog audit + outcome
tracking), repo-graph observability loop.

### Added

- New Skill `skills/coordination/process-design/SKILL.md`: specification-first
  design of repeatable, safe, and stable processes (process card template,
  per-step verification, loud failure, rollback, review cycle) plus rendering
  of an external one-page methodology artifact derived from the same source.
  Refined from research before release: last-validated card metadata,
  escalation criteria, per-step freedom levels, notification tiers and
  hygiene, and a supervised first-run validation rule. Added script safety
  gate: static scan of agent-written scripts, dry-run default, test on a
  copy, read-only inputs, checksum proof of untouched input, atomic writes.

- `check_format.py` now resolves `Dependencies` entries: every backticked
  reference must match an existing Skill directory
  (`skills/**/<name>/SKILL.md`).

- `privacy_scan.py` extended: Czech-prose detection outside code fences
  (3+ diacritic glyphs per line; the repository is English-only) and
  versioned model-identifier patterns (product names like "Claude Code"
  do not match — a digit is required).

- `skill-mirror-check` Skill + weekly task card — verifies that deployed local
  Skills match the repository source of truth (fresh read + diff per Skill,
  classified as content drift / expected overlay / cosmetic); prevents
  instance drift from being misattributed to repository text and triggering
  nonsense repository fixes.

- Two previously local-only Skills published: `skill-governance` and
  `llm-model-evaluation` — closes dangling dependencies in `agora-coordinator`
  and `self-improvement-loop`.

- `memory-tool-reference` Skill published — ported from the local instance,
  reformatted to the SKILL.md layout, and wired into memory routing
  (`memory-master-index` Dependencies, `tool-execution-contract` Domain
  routing).

- `memory-audits` Skill: quantified staleness scoring (fresh ≤ 30 days,
  aging 31–90, stale > 90; undated files count as stale) — staleness is a
  finding with a verify/refresh/archive recommendation, never a silent
  correction.

### Changed

- Task cards rescheduled to the operator's night window: daily data sweep,
  exchange README maintenance, self-improvement retrospective, skill mirror
  check, repository sync, stack observability, quarterly replication dry-run
  (exact times are instance-specific). The Sunday ordering (retrospective →
  mirror check → repository sync) is preserved.
- Self-improvement retrospective upgraded from a rotating three-Skill
  mini-audit to a full-catalog Skills audit every run (dependency graph:
  hubs, cycles, dangling references, missing bindings) with a reduction lens
  (KEEP / MERGE / RETIRE verdicts with evidence and impact on dependents) and
  up to two structural deltas; the rotation state file is replaced by a
  Skills health state file.
- `docs/29-self-improvement-loop.md` and the `self-improvement-loop` Skill
  aligned with the full-catalog audit wording.
- Self-improvement loop: realized deltas now get a longitudinal outcome
  assessment (helpful/harmful/neutral) in later retrospectives, appended to
  the eval log (after ACE's helpful/harmful counters).
- `docs/29-self-improvement-loop.md`: positioning within the self-evolving
  agents taxonomy (arXiv:2507.21046) and safety rationale from the Darwin
  Gödel Machine (§5) added to the safety rules.

- Skill evaluation methodology in the self-improvement loop (`docs/29` §7,
  `self-improvement-loop` Skill): capability-uplift vs. encoded-preference
  taxonomy, trigger-precision review of catalog descriptions, blind A/B
  (skill vs. no skill), and a periodic necessity/retirement check.

- AGENTS.md operational sections distilled from cross-repository agent
  instruction practice: navigation guidance, boundaries with reasons and
  alternatives, a repository-specific anti-pattern catalog, and a definition
  of done.

- Untrusted external content rule — external content is data, never
  instructions; memory-write hygiene against memory poisoning (`docs/8`,
  `docs/13`, one kernel sentence, ADR-0015).

- Task-run metadata guidance and a lite error-budget rule in the
  observability pattern (`docs/28` §6, §11).

- Incident postmortem template with a decision-lineage section (`docs/29` §8).

- Stack observability task (v6): the dashboard additionally reads the local
  repo-graph snapshot written by the weekly repository sync (absence is
  reported as no data yet), completing the repository-graph observability
  loop; the skills-health dashboard field aligned with the full-catalog
  audit wording.

- `LICENSE` copyright line restored to the copyright holder's real name —
  the LICENSE is the single sanctioned location for it (ADR-0014).

- `privacy_scan.py`: instance-specific identifier patterns removed from the
  public scanner entirely (ADR-0014) — they load from an instance-side
  overlay file (`~/.config/agora-repo/privacy-extra-patterns.txt`, one
  `<kind> <regex>` per line) that is never committed; an absent file (CI,
  fresh clones) degrades gracefully to the generic classes. The public
  repository must contain no personal identifiers — not in docs, not in
  tooling, not obfuscated; the LICENSE copyright line is the sole
  exception.

- `privacy_scan.py` hardened after an adversarial self-test (2026-10-28):
  family-term coverage extended with generic Czech kinship stems (siblings,
  parents, in-laws, children, grandchildren), the personal-name pattern now
  matches inflected forms, and `model_id` matches spaced model forms via a
  bounded sub-name group (concrete examples live in the scanner docstring).
  Documented accepted gaps: obfuscated contact strings, short Czech lines
  with <= 2 diacritic glyphs, instance-specific proper nouns (adding them
  to this public scanner would publish them).

- `aps-upgrade`: repository-first flow for Skill text changes — the setup
  repository is the source of truth; the local instance imports repository
  versions and re-applies the personal overlay (docs/30). Runtime verification
  of new app behavior still precedes any Skill text change.

- `model-escalation-protocol`: Load-when narrowed — the first bullet now
  requires a preventive T7 condition (irreversible action, multi-file
  refactor, 3+ mutually dependent unknowns, money/publication/career) or an
  already-fired trigger; routine multi-step tasks are covered by
  `sequential-thinking-workflow` + `tool-execution-contract` alone
  (D-20261028-04; dogfood eval pending).

### Fixed

- Dependency and format consistency across Skills: `.md` suffixes in
  `self-improvement-loop` Dependencies, prose Dependencies sections
  (`multi-source-research`, `sequential-thinking-workflow`), self-referencing
  description prefixes (`language-fidelity`, `model-escalation-protocol`),
  missing cross-links (`agora-coordinator` → memory audit routing,
  `github-release-workflow`/`cad-spec-driven-workflow` →
  `shell-and-device-operations`), and extended Domain routing in
  `tool-execution-contract`.

- `memory-file-operations`: restored the Saved Memory file taxonomy
  (living topic file / session log / hybrid / buffer with write triggers) that
  was lost during generalization; the local instance relies on it for
  session-log naming and living-file maintenance.

- Broken external MADR link in `decisions/README.md` — now points to the
  official project page (https://adr.github.io/madr/). External URLs are not
  covered by `check_links.py`; they are covered by the quarterly replication
  dry-run.

- Skills deep-audit fixes (2026-10-28): `docs/5` coordinator composition
  diagram updated to the current six dependencies (stale "local instance
  Skill" note removed; peer dependency cycles documented as intentional);
  `tool-execution-contract` Domain routing further extended by
  `language-fidelity`, `model-escalation-protocol`, `llm-model-evaluation`,
  and `aps-upgrade`; description capitalization (`language-fidelity`,
  `model-escalation-protocol`), `memory-master-index` H1 title,
  chronological Sources order in `github-release-workflow`, and a trimmed
  catalog description for `self-improvement-loop`.

## [1.2.0] - 2026-10-27

P2 milestone: SKILL.md layout, CI gate, platform layer, replication golden task.

### Added

- `.github/workflows/check.yml` — CI gate running `scripts/check.sh` on push
  to `main` and pull requests; least privilege, no secrets (ADR-0010,
  supersedes the CI deferral in ADR-0005).
- Skills migrated to the Agent Skills (`SKILL.md`) layout: one directory per
  Skill under `skills/`, YAML frontmatter (`name`, `description`, `license`)
  plus the existing 10-section body (ADR-0011); `check_format.py` now
  validates frontmatter, naming rules, and description consistency.
- ADR-0012 — the repository remains public; sensitive material belongs to the
  private instance overlay, not this repository.
- `agora-coordinator` Skill now routes systemic findings (repeated failures,
  drift patterns) into the self-improvement loop as evaluated deltas instead
  of ad-hoc direct edits.
- `platform/` — parameterized host-level systemd unit templates (MCP server,
  sequential-thinking bridge, exchange watcher service + timer) with an
  install manifest and `docs/31` (ADR-0013, minimal scope per the dry-run
  gate); the privacy scan now covers `.service` and `.timer` files.
- Golden task: a quarterly replication dry-run (fresh-agent simulation over a
  clean clone) is now a scheduled task; card in `tasks/` (docs/29).

### Fixed

- Stale Skill references after the SKILL.md migration (`docs/5`, `docs/20`,
  `docs/21`, `docs/28`) and CI-era drift: README status line, `docs/29`
  verification step, `tasks/repo-sync-weekly` card, and the
  `github-release-workflow` Skill now reflect the CI gate; the coordinator
  Skill capability table was re-verified against runtime.
- Kernel Skill naming: the System template memory gate and the `docs/20`
  normative text now quote repository-layout Skill names (directory names, no
  `.md` suffix), consistent with the import rule in `docs/2`; the `docs/5`
  naming note explains store suffix differences (both forms resolve in the
  maintained instance — verified 2026-10-27). Replication dry-run GAP-2.
- `manifest.yaml`: glob sources carry machine-checkable `files` counts
  (inventory v3) and a new `check_inventory.py` enforces them in `check.sh` —
  the inventory no longer drifts in prose (replication dry-run GAP-1).
- `docs/2` and README: tool names quoted by the kernel gate are documented as
  app-version-coupled, with import-time re-verification guidance.

## [1.1.0] - 2026-10-27

P1 milestone: validation, inventory, and decision records complete.

### Added

- `manifest.yaml` — machine-readable component inventory (source → deployment
  target) for drift detection; the privacy scan now covers YAML files too.
- `decisions/` — architecture decision records (MADR-lite): 8 seeded ADRs
  (add-on-layer policy, docs numbering, kernel rules, tool-call budget,
  validation-as-code, MCP transport, inventory, task cards) + format index.
- `docs/30-instance-overlay.md` + ADR-0009 — instance overlay pattern:
  public generic base ↔ private localized instance, derivation and export
  rules, privacy gates.

### Fixed

- `docs/2-installation.md`: added a prerequisites section (python3/git/bash for repository validation); replaced the stale partial Skill table with the flat-name rule (file name without `.md`), so the document no longer drifts when Skills are added.
- `AGENTS.md`: documented the validation prerequisites.

### Changed

- `skill-mirror-check`: drift policy now encodes the operator's standing
  authorization (2026-10-28) — on confirmed content drift with the repository
  clearly newer, the repository version is re-imported into the local store
  in place, recorded with diff evidence; repository ports and ambiguous
  directions still require operator GO. Weekly task card aligned.

## [1.0.0] - 2026-10-27

First tagged release: the governance layer as of `main` @ `dfae1bc`.

### Added

- `AGENTS.md` — agent-facing entry point: precedence rule, repository map,
  mandatory conventions, validation entry point.
- `scripts/check.sh` — one-command validation: Skill format compliance,
  personal-identifier scan, relative link integrity.
- `CHANGELOG.md` — this file; versioning policy (semantic version tags).

### Compatibility

- Maintained against Agora app releases from F-Droid; current app baseline is
  the v2.1.x line (see `docs/22-platform-architecture.md`, §6).