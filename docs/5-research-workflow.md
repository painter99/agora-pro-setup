# Deep research vs light verification

## Short answer

**Keep the original Deep Research framework.** The thin `multi-source-research` Skill from the first 2.1 rewrite was a summary, not a replacement.

| | Light verification | Deep research Skill |
|---|---|---|
| When | one fact, one official page, low stakes | 2+ sources, comparison, dispute, money/safety/technical decision |
| Loop | search → fetch → cite | triage → deep dive → synthesis + quality gates |
| Limits | a few targeted calls | explicit iteration bounds, escape hatch |
| Output | short conclusion + sources | full report template |

## What the original framework still does better

- ReAct loop with reflection
- source scoring table (authority, recency, specificity, cross-ref)
- chain of verification before logging a fact
- mandatory counter-query
- iteration bounds and escape hatch
- self-evaluation / quality gates
- contradiction surfacing instead of averaging sources
- structured report + source registry

Those are the pieces that actually change agent behavior. A 40-line "prefer primary sources" Skill does not.

## What 2.1 changes about *installation*

- Install as Skill `deep-research`, not Saved Memory.
- Discover via `{skill_catalog}`, load via `read_skill_file`.
- System template routes to it; it does not paste the whole loop into every request.
- Proportionality: do not fire the 20-iteration loop for "what time does the shop close".

## Planning / approval

Original text asked to present a plan and wait. Keep that for multi-phase or high-stakes research. For a small factual check, proceed. If Agora has no approval UI in that path, document the plan in the Methodology Note.
