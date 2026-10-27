# ADR-0001: Clean add-on layer; no upstream duplication

- Status: accepted (2026-10-06, operator GO)
- Supersedes: none

## Context

The Agora application documents its own behavior: official repository
documentation, the user manual, and in-app tool definitions. Copying that
content into this repository created two sources of truth that age at
different speeds, and readers could not tell which copy was current.

## Decision

This repository never duplicates upstream content; it links to it. Only
original architecture, governance, and procedures belong here. A duplication
audit (2026-10-06) compared headings of all repository documents against
upstream documentation, removed one upstream-derived reference document
(number retired, see ADR-0002), and slimmed four documents to their original
value.

## Consequences

- Documents stay small and do not rot against upstream changes.
- Readers need access to the upstream documentation for app behavior.
- A periodic duplication check is part of repository maintenance.
- Observed upstream behavior (what the app actually does) still overrides
  documentation, per the runtime-evidence principle.