# ADR-0010: CI lint gate enabled

- Status: accepted (2026-10-27, operator GO after Level-2 research)
- Supersedes: ADR-0005 (the CI-deferral aspect only; validation-as-code stands)

## Context

ADR-0005 deferred continuous integration because the repository is
docs-only. Research (2026-10-27, Level 2) showed: lint/link checks in CI are
standard practice for documentation repositories; Actions usage is free for
public repositories on standard hosted runners; the safe pattern is the
`pull_request` event with a least-privilege read-only token (never
`pull_request_target`), no secrets, and no third-party actions beyond
`actions/checkout`.

## Decision

Enable a minimal check workflow (`.github/workflows/check.yml`): on every
push to `main` and on pull requests, run `scripts/check.sh` (the same gate
as local commits). Least privilege (`permissions: contents: read`),
concurrency with cancel-in-progress, 5-minute timeout, no secrets.

## Consequences

- Enforcement no longer depends on discipline alone (ADR-0005 caveat
  resolved).
- The autonomous weekly repository sync now also gets its pushes checked;
  a red run is a drift signal, not a silent failure.
- Cost: zero (public repository); runtime: seconds.
- The workflow file is outside the sync task's write scope (`.github/` is
  excluded by its prompt), so CI configuration changes stay under operator
  GO.