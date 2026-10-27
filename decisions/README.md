# Decision Records

Architecture decision records (ADRs) for this repository, in a light
[MADR](https://adr.github.io/madr/)-inspired format.

## Format

One decision, one file: `NNNN-kebab-title.md`.

```markdown
# ADR-NNNN: <title>

- Status: accepted | superseded (date, operator GO)
- Supersedes: ADR-XXXX or none

## Context
Why this decision was needed.

## Decision
What was decided, in normative wording.

## Consequences
What this makes easier, harder, or mandatory.
```

Superseded ADRs are never deleted; their Status line points to the successor.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-clean-add-on-layer-no-upstream-duplication.md) | Clean add-on layer; no upstream duplication | accepted 2026-10-06 |
| [0002](0002-docs-numbering-immutable.md) | Document numbering is immutable; retired numbers are not reused | accepted 2026-10-06 |
| [0003](0003-always-applicable-rules-live-in-the-kernel.md) | Always-applicable rules live in the kernel, not only in Skills | accepted 2026-10-20 |
| [0004](0004-tool-call-budget-prompt-level.md) | Tool-call budget is enforced at prompt level | accepted 2026-10-08 |
| [0005](0005-validation-as-code-ci-deferred.md) | Validation lives in the repository as code; CI deferred | accepted 2026-10-27 |
| [0006](0006-single-streamable-http-endpoint.md) | One Streamable HTTP endpoint per MCP server; SSE retired | accepted 2026-10-25 |
| [0007](0007-component-inventory-drift-anchor.md) | Component inventory is the drift anchor | accepted 2026-10-27 |
| [0008](0008-task-cards-not-verbatim-prompts.md) | Scheduled tasks are documented as cards, not verbatim prompts | accepted 2026-10-27 |
| [0009](0009-instance-overlay.md) | Instance overlay — public generic base, private localized instance | accepted 2026-10-27 |
| [0010](0010-ci-lint-gate-enabled.md) | CI lint gate enabled (supersedes the CI-deferral in ADR-0005) | accepted 2026-10-27 |
| [0011](0011-agent-skills-skill-md-layout.md) | Skills use the Agent Skills (SKILL.md) layout | accepted 2026-10-27 |
| [0012](0012-repository-stays-public.md) | The repository remains public | accepted 2026-10-27 |
| [0013](0013-platform-layer-minimal-scope.md) | Platform layer — minimal scope (unit templates, no bootstrap script) | accepted 2026-10-27 |