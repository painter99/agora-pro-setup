# ADR-0016: Coding layer — human-gated loop as a Skill

- Status: accepted (2026-10-30, operator GO)
- Supersedes: none

## Context

The stack gains a coding layer: the agent implements code, the operator sets
the frame and verifies. Field research (2026) shows that "tests green" is an
unreliable correctness signal for larger changes (reward hacking grows with
code size), and that production coding harnesses run hand-rolled, deterministic
loops rather than general frameworks. The stack already has the verification
culture (GO gates, tool-call budget per ADR-0004, script safety gate in
`process-design`); what was missing is the loop itself, its measurement, and
the versioning home for personal scripts.

## Decision

1. The coding loop is a Skill (`coding-loop`), not a new tool or framework:
   spec gate → small increments → tests as reviewable artifacts → second-agent
   review → bounded fix rounds → acceptance against reality.
2. The loop is human-gated: no autonomous fix iterations past the tool-call
   budget, no auto-merge, no unattended pushes to shared branches.
3. Coding work is measured by coding golden tasks in the instance eval corpus
   (docs/29); recurring fix patterns become Skill deltas through the
   self-improvement loop.
4. Personal scripts version in a private instance repository mirroring the
   live paths; employer code never enters it.
5. The pattern is documented in docs/32; instance values stay in the overlay
   (ADR-0009, docs/30).

## Consequences

- New Skill family `coding/`; domain routing row in the tool execution
  contract.
- Golden tasks and the scripts repository are instance-layer artifacts; the
  repository carries only the pattern.
- No new tooling or CI beyond the existing checks; the loop's enforcement is
  prompt-level (like ADR-0004), backed by the approval gate.