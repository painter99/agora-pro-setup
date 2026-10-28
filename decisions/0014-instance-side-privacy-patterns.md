# ADR-0014: Instance-side privacy patterns

- Status: accepted (2026-10-28, operator GO)
- Supersedes: none (corrects the implicit P0 choice of embedding personal
  identifier literals in the scanner)

## Context

The privacy scanner originally carried the instance's personal identifier
patterns (owner name forms, a family place) as regex literals. Tooling files
are public repository content like any other: a scanner whose purpose is
privacy protection must not itself publish the identifiers it protects.
The operator requires that no personal identifier remain in the public
repository — not in documentation, not in tooling, not obfuscated. The
single sanctioned exception is the `LICENSE` copyright line, which must
name the copyright holder (standard open-source practice).

## Decision

- The public scanner contains only generic pattern classes: contacts, paths,
  IP addresses, generic Czech kinship/prose heuristics, and model
  identifiers.
- Instance-specific identifier patterns live in an instance-side overlay
  file, `~/.config/agora-repo/privacy-extra-patterns.txt` (one
  `<kind> <regex>` per line, `#` comments), loaded by the scanner when
  present. An absent file (CI, fresh clones) degrades gracefully to the
  generic classes.
- The overlay file belongs to the instance overlay (docs/30); it is never
  committed, copied into the repository, or published.
- The `LICENSE` copyright line is the only repository location where the
  owner's real name appears; the scanner does not scan the LICENSE.

## Consequences

- Detection of personal identifiers on the maintained instance is unchanged;
  CI and fresh clones detect only the generic classes — human review, the
  operator GO gate, and the instance-side maintenance grep remain the
  primary gates for identifier classes not covered publicly.
- History note: past revisions of the scanner and the LICENSE copyright
  line contained personal literals; the scanner history is purged (see
  CHANGELOG). Absolute erasure from third-party caches or forks cannot be
  guaranteed.