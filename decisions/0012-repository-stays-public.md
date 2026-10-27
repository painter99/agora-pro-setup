# ADR-0012: The repository remains public

- Status: accepted
- Date: 2026-10-27

## Context

The operator considered flipping this repository to private or to a
two-tier model (public sanitized copy plus private full copy). Motivations
were caution about public exposure of operational details and a general
privacy preference.

Considerations observed at decision time:

- The repository's purpose is a public reference architecture; visibility
  supports the sharing and feedback goals recorded in the project plan.
- Privacy discipline is already enforced as code: `scripts/privacy_scan.py`
  (identifier patterns, allowlisted generic values) runs before every commit
  and in CI, and the content rules forbid personal facts in the repository.
- Material that must stay private has a dedicated home: the instance overlay
  pattern (ADR-0009, `docs/30-instance-overlay.md`) keeps localized/personal
  instances separate from the public generic base.
- GitHub Actions is free for public repositories; a private repository would
  consume the limited free minutes quota (the check run takes well under a
  minute, so cost is not the deciding factor, but it removes one concern).
- The git history is already clean of personal data (a 2026-10 privacy
  incident was rewritten at the time).

## Decision

The repository remains public. Content that must stay private belongs to the
private instance layer (overlay), never into this repository. The privacy
scan and human review before every commit remain mandatory.

Revisit this decision only if a class of content emerges that cannot be
expressed in the generic base plus private overlay split.

## Consequences

- CI stays on the free tier; visibility and community feedback are preserved.
- The privacy scan, review discipline, and overlay pattern carry the privacy
  burden instead of repository visibility.
- A future flip to private remains possible at any time (settings change,
  reversible), so this decision is low-risk.