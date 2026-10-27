# ADR-0002: Document numbering is immutable; retired numbers are not reused

- Status: accepted (2026-10-06, operator GO)
- Supersedes: none

## Context

Renumbering documents breaks cross-references in other documents, Skills, and
external links, and makes historical discussions hard to follow.

## Decision

Never renumber existing documents. When a document is removed, its number is
retired and stays unused (number 19 is retired); new documents take the next
free number (next: 30). When content moves, cross-references are updated in
the same change.

## Consequences

- References remain stable across time.
- Number gaps are intentional and must not be "fixed".
- The link checker and the component inventory verify that references stay
  resolvable.