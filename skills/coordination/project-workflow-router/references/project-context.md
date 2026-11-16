# Project context adapter (template)

Replace this file per project. The router and the coding loop load it at the
INSPECT phase. All fields are placeholders — fill only what the project needs.

## Project identity

- name:
- repository path:
- entry docs (PRD / spec paths):

## Current gates and state

- active gates:
- state file path:
- pending operator decisions:

## Routing table

| Task type | Route |
|---|---|
| code change | coding-loop |
| spec-only | spec-first |
| test-only | python-tdd |
| review-only | code-review |

## Boundaries

- protected paths:
- approval gates that must not be bypassed:
