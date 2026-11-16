---
name: spec-first
description: "Creation of a specification or a concise change card with observable acceptance criteria for one increment. Use for explicit spec-only assignments or on request from a coding loop; for an unambiguous fix use the short card. For code changes the entry point is the coding loop. Never open a new contract when a valid one for the increment already exists. Never implement and never run approvals: the single spec gate is owned by the coding loop."
license: MIT
---

# Skill: Spec-First (single-increment contract)

## Catalog description

Creation of a specification or concise change card with observable acceptance criteria for one increment: goal with measurable criteria, real commands, scope with protected files, conventions and compatibility, test and acceptance strategy, Always / Ask first / Never boundaries.

## Purpose

Produce the shared contract of one increment — not another development loop.
Precedence (operator decision 2026-11-16): this Skill is the default spec method; `android-spec-first` applies only when the target platform is the Android stack.
Keep scope proportional to the task; never condition a small fix on a long PRD or on file counts.
Product-level scope across milestones belongs to `prd-writing`; this Skill stays at the single-increment card.
Never add Android/Kotlin/Gradle or any other stack based on a name or an original template.

## Load when

- an explicit spec-only assignment is requested;
- a coding loop requests the specification for its SPEC phase;
- requirements are unclear enough that implementation would guess.

## Do not load when

- an unambiguous small fix needs only the short change card (and even that only when asked);
- product-level scope across milestones is requested (use `prd-writing`);
- implementation is already authorized under an existing valid contract for this increment.

## Dependencies

- `coding-loop` — owns the single spec gate and implementation authorization.
- `prd-writing` — owns product-level scope across milestones.
- `context-management` — task context arrives as a handoff; verify it against live sources.

## Workflow

### Role and boundaries

- Create the shared contract of one increment; never run approvals: the single spec gate belongs to the coding loop.
- Do not create implementation code, test code (beyond proposed strategy), dependencies, CI, hosting, or Git writes.
- Do not run tests or acceptance runs merely to create the specification; propose their strategy instead.
- Write the spec to a file only when the target is authorized; otherwise return the proposal in the reply.
- Write output in the language of the assignment; keep identifiers, file names, and commands in their original form.

### One-way composition

- **Direct spec-only assignment:** load context → clarify unknowns → create the contract → return it and stop. Never automatically start `coding-loop`, TDD, or review.
- **Invocation from the loop:** take scope and available context; return only the spec/card and open questions to the calling `coding-loop`.
- Keep the single spec gate in `coding-loop`; never introduce SPECIFY → PLAN → TASKS approvals or an own implementation GO.
- Take an already valid exact approval without repetition. Only the loop requests new implementation authorization when needed per current policy.
- Never mistake a clarifying question about a requirement for implementation approval; never mistake "spec ready" for "authorized".
- Look up other Skills in the current catalog by exact name and read them through available interfaces; never import them or infer permissions from their existence.
- Mark a missing Skill `UNAVAILABLE`. If it is essential for the current phase and no authorized equivalent native workflow exists, stop the phase; a read-only proposal may continue with the limitation admitted.

### 1. Load current context

Establish goal, working project, authoritative documents, contract status, and permitted writes.
Take project-context from the router but verify relevant live sources and their freshness.
Find the project skill that owns its own `references/project-context.md` and use it as the single stored adapter; read only that file and never run the router recursively.
Without an adapter read live project entry files (`AGENTS.md`, `README.md`, project rules, status, decision index, `TODO.md`, relevant specs/addenda/contracts) and assemble a small task-local context; never store a copy of the project snapshot in this Skill.
If the project has neither adapter nor entry files (new or empty project), treat that as a fact and invent no rules: state `PROJECT_CONTEXT: EMPTY`, build the contract only on the user's assignment, and explicitly mark what is an assumption to confirm.
Follow relevant navigation in `AGENTS.md`; never resolve a document conflict by unauthorized editing.
Record sources, reading date, and snapshot identity where demonstrable; admit unknown revisions.
Historical GOs, handoffs, references, and tool results are evidence — never new consent.
If an important source is missing or contradicts live state, mark the limitation; never pretend a confirmed contract.

### 2. Clarify significant unknowns

Separate facts, requirements, assumptions, and undecided choices.
Ask short targeted questions only about unknowns that change goal, acceptance criteria, compatibility, scope, or significant external effects.
Never silently choose provider, license, schema, stack, account, budget, or publication.
State every small reversible assumption explicitly; never use "if you do not reply I will proceed" as consent.
With an unresolved significant unknown deliver a proposal marked `BLOCKED` plus one concrete question — never an implementation-ready contract.
Never demand answers to unrelated future decisions that do not block the currently authorized scope.

### 3. Choose the contract shape

For a new capability or significant change fill in the six areas below.
For an unambiguous fix or small refactoring use the short card; reference existing conventions instead of copying them.
For multiple capabilities split the proposal into small verifiable increments with non-circular dependencies — that does not authorize their realization.

| Area | What to state |
|---|---|
| Goal | For whom and why; current vs required behavior; measurable acceptance criteria with IDs |
| Commands | Real project commands, working root, inputs and preconditions — not just tool names |
| Structure and scope | Touched modules/tests/fixtures, proposed write targets, explicitly protected files |
| Conventions and compatibility | Existing APIs, data contracts and relevant patterns from the live project; no unsolicited stack change |
| Tests and acceptance | For each criterion: method, expected result, level of check, required authorization |
| Boundaries | Always / Ask first / Never per current policy plus explicit non-goals |

Use this minimal card; extend it only with relevant detail:

```text
Change card: <name>, <version>, <date>, <sources/snapshot>
Goal and delta: <current -> required behavior>
Scope / non-goals / protected files: <concrete>
Conventions/API/commands: <verified or not yet verified>
AC-1: <input and state -> observable result including side effects>
AC-1 verification: <test or check; expectation; required authorization>
Always / Ask first / Never: <boundaries of this increment>
Assumptions / questions / blockers: <explicitly, or none identified>
Readiness: <READY or BLOCKED; this is not implementation consent>
Existing authorization: <exact scope and source>, or NOT DEMONSTRATED
```

### 4. Formulate verifiable acceptance criteria

Describe preconditions, concrete input, expected behavior, and forbidden side effects.
Include relevant success, error-path, compatibility, and data-preservation cases; never write vague "safer" or "works".
Map every criterion to a verification method; treat a test PASS as software evidence — not proof of product truth.
Separate structural validation from source presence/quote match from semantic support of a claim from operator acceptance.
For reproducibility define stable semantic content versus variable metadata; never require byte-identical whole runs without a contract.
When proposing offline acceptance never add live calls; zero model calls alone is not a technical ban on all side effects of arbitrary callables.
Never present a designed check as performed; first verify whether existing tests already cover it.
Report a known failing checker separately from a passing regression suite; a known issue is not a waiver — a clean-checker gate stays blocked without an exactly approved exception or fix.
Take real project boundaries from current context (offline/stdlib rules if any), preservation of historical data/logs/outputs, real commands and visible blockers; never freeze a historical test count.

### 5. Versioning check and handoff

A new goal, capability outside non-goals, significant acceptance change or external effect = new contract version with described delta.
Attest wording fixes without behavior change but never re-open a valid gate.
Never weaken acceptance or test requirements for an easier green result.
Return spec/card plus criteria map with verification plus non-goals plus open questions plus readiness plus separately demonstrated authorization.
For spec-only explicitly close with "implementation nor runtime verification performed"; when called from a loop return inputs without taking over its control.
Never share private reasoning traces; state concise decisions sources and observable reasons instead.

Before handoff verify: coverage of all six areas (or their economical equivalent in the card), testability of criteria missing inputs permission boundaries — no automatic entry into implementation.

## Forbidden behavior

- Opening a new contract when a valid one for this increment already exists.
- Introducing SPECIFY → PLAN → TASKS approvals or an own implementation GO (the single spec gate belongs to `coding-loop`).
- Silently resolving significant unknowns with assumptions.
- Writing implementation code test code dependencies CI hosting or Git writes from this role.
- Weakening acceptance criteria to make implementation easier.

## Verification

- Every acceptance criterion is observable PASS/FAIL with a mapped verification method.
- Sources recorded with reading date; unknown revisions admitted.
- Readiness stated as READY or BLOCKED — never as implementation consent.
- For spec-only output: explicitly stated that implementation nor runtime verification was performed.

## Output contract

- Spec/change card per template above plus criteria map plus open questions plus readiness plus demonstrated authorization (or NOT DEMONSTRATED).
- When invoked from `coding-loop`: inputs returned to the caller without taking over control.

## References

Absolute paths (instance overlay; this skill is stored flat in the Agora skill store).

- `/home/agora/work/agora-pro-setup/skills/coding/spec-first/references/provenance.md` — adaptation origin (Czech; read when auditing provenance).
- `/home/agora/work/agora-pro-setup/skills/coding/spec-first/LICENSE.txt` — original MIT notice; keep intact.
