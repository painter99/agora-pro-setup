# Instance Overlay

Pattern for running a private, personalized instance on top of this public,
generic repository. The repository is the reusable governance layer; the
instance is the live setup that actually runs.

## The two layers

| | Base (this repository) | Instance (private) |
|---|---|---|
| Language | English | any, typically localized |
| Personal data | none (anonymized, scanned) | present, by design |
| Storage | public git repository | app stores, private memory, host |
| Validation | `scripts/check.sh` | instance-level tests and dogfood |
| Change flow | branch → checks → GO → merge | import diff → functional test |

## What flows in each direction

**Base → instance (imports).** Skills, prompt templates, and patterns
(`docs/`) are imported into the instance. An import
may be localized and may gain instance-only hooks (for example an extra
kernel sentence), but keeps the derivable shape of the base file so future
updates can be diffed.

**Instance → base (exports).** Only generalized patterns: strip personal
context, translate to English, run the privacy scan and checks, then ship
through the standard branch-and-GO flow. Live task prompts are never exported
verbatim (ADR-0008).

**Never exported:** personal facts, names, schedules, hardware models,
network details, ports, credentials, live prompts, the working state file and
its path (ADR-0017).

## Derivation and precedence

- Instance files derived from base files keep the same section structure;
  a base update is applied by diffing, not by re-deriving from scratch.
- Runtime precedence: observed instance reality wins over stale base
  documentation — the same precedence rule the repository states for agents.
- When instance practice evolves a better pattern, generalizing it back to
  the base is a deliberate step (privacy scan + GO), after which both layers
  carry it.

## Maintenance

- Base updates reach the instance through a review pass (import diff plus a
  functional test), never silently.
- The instance keeps a private record of what was imported and when — the
  instance-side counterpart of `manifest.yaml`.
- Drift between layers is checked in the maintenance pass: instance inventory
  versus base manifest.

## Verification

- Export: privacy scan with 0 findings and `check.sh` exit 0 before push.
- Import: diff review plus a functional test on the instance.
- Ongoing: layer comparison in the scheduled maintenance pass.