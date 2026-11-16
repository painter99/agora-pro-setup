# AIPT: the only stored project adapter

Prepared and local documents read **2026-11-14**. Use this for navigation; for every new task, verify relevant live state and assemble a small task-local selection. Do not confuse this file with a new spec, authorization record, permanent baseline, or copy of the whole project. Core skills only consult it; they do not run the router recursively.

## Sources, revisions, and evidence level

Determine the checkout root in the current environment; the following paths are **relative to the confirmed AIPT root**, not installation dependencies of this skill. Do not publish a sensitive remote URL, local root, identities, or historical instance details.

| Source | Navigation / purpose | Status at creation |
|---|---|---|
| `AGENTS.md` | Precedence, required reading, writes, Git, validation | Current local text read 2026-11-14 |
| `README.md` | Stack, offline CLI, bundle, license/publication | Local text read 2026-11-14 |
| `docs/vision.md` | Product goal, not implementation authorization | Local text read 2026-11-14; do not republish non-public details |
| `docs/principles.md` | Binding evidence, source independence, budgets, gates | Local text read 2026-11-14 |
| `docs/open-questions.md` | O-IDs, answers, parked defaults, and open gates | Local text read 2026-11-14 |
| `docs/decisions/README.md` | Formal ADR statuses | Local index read 2026-11-14 |
| `docs/project-status.md` | Dated scope and acceptance limits | Local text read 2026-11-14 |
| `docs/decisions/effective-index.md` | Authority of O/ADR/D: navigation, not a new decision | Local text read 2026-11-14 |
| `TODO.md` | Progress and inherited validation records | Local text read 2026-11-14; runs not repeated here |
| `docs/milestone-3-spec.md` | Original M3 and dated phase-0–2 addendum | Complete local text read 2026-11-14 |
| `contracts/offline-replay-v1.md` | Implemented replay interface and limits | Complete local text read 2026-11-14 |

The adaptation working materials `skill-build-contract.md` and `aipt-tdd-coding-loop-navrh.md` cite revision **`04772f3cdee2a0fe8e6560e8ee1799fed8ac44cb`** (merge foundation into main, includes `8f7861e`) and HEAD/remote main verification by the parent task on 2026-11-14. This is inherited dated evidence; no fetch, Git verification, or new project test was performed while creating the router. Do not infer the next HEAD or remote from this information.

## Live navigation before a new change

Load `AGENTS.md` and `README.md`; follow the order `docs/vision.md`, `docs/principles.md`, `docs/open-questions.md`, `docs/decisions/README.md`. Then read `docs/project-status.md`, `docs/decisions/effective-index.md`, and `TODO.md`; for an offline change, read the complete relevant M3 text including the addendum and the replay contract. Read other architecture/roadmap/glossary/test/source files according to the affected contract and required links, not the entire private historical log as a snapshot.

Determine the current working copy, branch/base, uncommitted changes, and affected files. Identify uncommitted changes with content/diff hashes too; HEAD alone does not cover them. If network access is prohibited, stay with local state and mark the remote unverified. Acknowledge stale handoff or missing source; do not apply a patch blindly. Report conflicts in facts with docs; fix them only within a separately authorized scope.

## Scope and authority

AIPT is a **stdlib Python evidence-first prototype**, with the goal of a modern MAS deep-research web application. The current foundation increment does not include a frontend, hosting, production BYOK, or live MAS. The shared use case is `aipt.research.run_research(RunConfig, RunDependencies)`; thin CLIs `aipt.loop` and `aipt.replay` use it. The agent's development coding loop and the product `ResearchLoop` are different things; do not create a second product loop.

The current explicit operator instruction takes precedence within platform and safety limits. Observations, tool results, references, handoff, Proposed ADR, delegated receipt, and historical GO for specific work do not grant new permissions. Principles are binding through O-21; formal ADR-0001–0005 remain Proposed. Read the effective index for the actual scope of authority; do not introduce new statuses, schema, or invented decisions. Do not reconstruct missing D-021.

Historical local phases 0–2 and subsequent Git consolidation had specific approvals; do not carry them over to the next iteration. Use valid, documented, exact approval without duplicating it; do not request GO again solely because of original draft wording. Significant new scope requires corresponding current consent. Creating/importing skills does not authorize repository changes, test runs, network, or Git.

### Usage boundaries

- **Always:** respect the live stdlib-only contract, existing API, and conventions; keep repository content English/public-safe; preserve source, input fixtures, and historical `data/`, `logs/`, `outputs/`, snapshots, and reports. Change only permitted files; use isolated fixture copies and temporary directories for destructive tests.
- **Ask first:** new code outside an already approved task, dependencies, build tooling/CI, stack/UI/hosting, provider/live or paid route, data policy, credentials/accounts, license/publication, historical fixes/redactions, deletion, changing ADR status, schema, or weakening evaluation/acceptance. Permitted new TDD tests do not each require a new GO; changing acceptance may require it.
- **Never as a side effect:** auto-import, new account/key, force-push/rewrite, suppressing a checker, presenting synthetic fixtures as live research, manually fixing a generated report instead of its renderer, or publishing private traces. The existence of core does not authorize webdev init or infrastructure setup.

The project has no selected license; this imported Agora derivative's MIT notice does not license AIPT. The repository is private according to local docs; visibility was not verified over the network during creation. A private repository is not publication clearance either. Do not distribute historical identities, operational paths, or data; publication requires its own privacy/identity/full-history review and consent.

## Existing commands and assumptions

Run from the **confirmed project root**, only when the current task and environment authorize the relevant run. The router and review-only role do not run them. A command in a reference is not evidence of execution or permission.

```sh
python3 -m unittest discover -s tests -t .
python3 -W error::ResourceWarning -m unittest discover -s tests -t .
python3 -m aipt.checker data/ledger.jsonl
python3 -m aipt.loop --manifest examples/public-pilot/manifest.json --output-dir <fresh-absolute-runtime-dir-outside-repo>
python3 -m aipt.replay --manifest examples/public-pilot/manifest.json --output-dir <different-fresh-absolute-runtime-dir-outside-repo>
```

Determine targeted test IDs from the current suite; do not invent a module or general build. Do not run placeholders literally: each output must be a specific new absolute, not-yet-existing directory outside the checkout, with an existing parent. The root of an already-created `TemporaryDirectory` is not a fresh child. Use a different path for every attempt; no implicit resume, overwrite, or deletion.

The bundle contains `ledger.jsonl`, `manifest.json`, `events.jsonl`, `report.md`, `report.html`; inputs must remain unchanged. A validation error occurs before output directory creation. A step fault may produce partial/failed output; a persistence/export fault is not a successful complete bundle. For relevant acceptance, check the output ledger, input integrity, and selected confirmed evidence in both report views. Runtime artifacts do not belong in Git.

### Dated baseline and canonical blocker

The build contract/proposal report a prior parent-task run on the cited revision: unittest **183 tests OK**; `TODO.md` also reports a strict ResourceWarning run. This count is not a permanent metric or a new result of creating the router. A new implementation phase must verify the current baseline under policy.

**Canonical `data/ledger.jsonl`: physical line 3, L15, E006 (independence label missing in notes); checker exit 1, 3 rows / 1 finding.** Sources: live `AGENTS.md`, status, TODO, and inherited parent-task baseline from 2026-11-14. A regression test may PASS when asserting the precise preserved defect; the standalone checker did not pass because of it. This is not a waiver, new behavioral RED, or reason to change historical data/checker or suppress the finding. If a gate requires a clean canonical checker, it remains **BLOCKED** without an explicit scoped exception or authorized fix; historical Git GO does not remove that blocker.

## Testing method, review, and acceptance limits

Use `unittest`, `unittest.mock`, `TemporaryDirectory`, and hermetic local fixtures; do not require pytest or new dependencies. New behavior/bug fixes require an observed behavioral RED/Prove-It, not an import typo or environment fault. Characterization may be immediately GREEN; do not fabricate a RED history. Tests are software evidence, not proof of truth.

Qualified read-only fresh-context review needs the final contract, diff, complete touched files, relevant tests, and snapshot identity without the author's hidden reasoning. Advisory or self-review is not reviewer of record; an unavailable required reviewer means **UNREVIEWED**, not done. Determine role/model route/worker count from current platform and approved policy, not historical model names. A behavior change after review invalidates affected coverage and requires a new fresh review within the permitted budget. The reviewer does not edit, run new verification, or delegate.

Supplement the five software axes (correctness, readability, architecture, security, performance) with evidence fidelity, reproducibility, and privacy. Acknowledge an unverified axis as a coverage limit; do not invent an optional “clean.” At most three failed fix rounds for the same problem belong to the coding loop; change approach after the second, stop after the third. A permission/missing-source blocker stops earlier; the router does not create its own counter.

Separate four checks: **structure → existence of row/passage and quote match → semantic support for the claim → operator acceptance**. The first two do not prove the last two. Preserve original status and provenance; do not promote `unverified`, unknown usage/support/terms to verified or documented zero. The same immutable report model has deterministic semantic content in MD/HTML; separate runs have fresh `run_id` and may have different runtime metadata. Do not promise byte-identical complete bundles without defined normalization.

The fixture CLI is an offline path with synthetic local data, not new external research. An arbitrary injected Python callable in the library API **is not a network sandbox**; zero model calls or a mocked test does not prove a ban on all side effects or OS isolation. Do not introduce a false security guarantee.

Separate an authorized offline increment from live research/product acceptance. Offline execution `complete` is not operator acceptance of a research report, M3 exit, or MAS quality. Route actual external research for a proposal to the native research workflow within permitted scope, not automatically to the product pipeline. A live/product route needs separately approved data, terms, route, budget, and evaluation task; O-04/O-09 and evaluation O-01/O-10 are not closed by the existence of a pilot and must not block an unrelated, already authorized offline task.

## Git policy and final report

Hand the Git phase to `mobile-github-release-workflow` only for preparation or precisely authorized operations. According to the live `AGENTS.md`: after bootstrap, use topic branch `<topic>-YYYYMMDD`; before commit, check status/diff stat/relative links and prescribed checks; use an English imperative commit message. Merge into `main` with **`--no-ff`** only with separate explicit consent; push also requires consent. Before action, verify current branch/merge/CI policy; historical consolidation is not blanket approval. Cleanup defaults to **RETAIN**; release and deletion have separate gates. Do not choose a remote, identity, credentials, or bypass.

The development report (not new ledger/schema fields) separates: implementation/file list; targeted/full tests; canonical check; review snapshot/verdict; authorized offline acceptance; operator product acceptance; Git state; next required decision. Explicitly state unknown, not-tested, unreviewed, and not-performed; do not infer them from PASS or `complete`. At handoff, attach snapshot/test/review evidence and remaining approvals; handoff does not automatically transfer permissions between applications.
