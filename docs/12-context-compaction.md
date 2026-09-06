# Context Compaction

This document explains how Agora's Context Compact works, how the recommended Compact prompt in `system-prompt/4-compact-template.md` relates to it, and why that prompt deviates from the compaction prompts used by other tools.

## How Agora implements Compact

Per Agora's official documentation (`docs/en/context.md` in the Agora repository):

- Compact summarizes older context into a durable **Compact capsule** while keeping recent messages verbatim. Original messages are never deleted; deleting a capsule only removes the summary boundary.
- **Automatic compact** runs before a send would overflow the active token budget. The trigger is application-level and cannot be changed by the prompt.
- **Recent messages to keep** (0–20) preserves a verbatim recent suffix after the Compact boundary. Setting this above 0 is recommended — it is the single most effective mitigation for post-compaction behavioral drift, and it is handled by the app, not the prompt.
- **Compact model** can be a different (smaller, faster) model than the conversation model. Because the compactor does not receive `{active_memory}`, `{skill_catalog}`, or Skill bodies, its instructions must live entirely in the **Compact prompt** setting.
- Compact capsules can be **recompacted**. Chained compactions are therefore a normal case, not an edge case.

## Why the recommended prompt is stricter than industry stock prompts

Public research on production compaction (Claude Code, Codex CLI, OpenCode, Amp; summarized in the survey "Context Compaction Research" by badlogic) shows that stock compaction prompts are short and cover only the happy path: completed work, current state, next steps, constraints. Four documented failure modes are left unaddressed:

| Failure mode | Evidence | Countermeasure in the recommended prompt |
|---|---|---|
| Prompt injection via transcript content | Not addressed by any stock prompt | Provenance rules: transcript instructions are content to summarize, never instructions to follow |
| Cumulative drift across repeated compactions — uncertainty hardening into "confirmed facts" | Documented quality loss with multiple compactions (Claude Code user reports; Codex warns users in-product) | Prior-handoff content keeps its stated uncertainty; never upgraded to confirmed fact |
| Fabricated next steps — the compactor invents a "clear next step" when none was agreed | Common compactor failure; Codex template asks for "clear next steps" with no guard | If no next step was agreed, the handoff must say so |
| Misattributed provenance (assistant proposals recorded as user decisions; app control text recorded as user intent) | Not addressed by stock prompts | Explicit provenance and control-text rules, including Agora's `<context_summary>` wrappers and synthetic continuation text |

Two additional rules come from general compactor reliability, not from any specific tool:

- **Rejected approaches with the rejection reason** — prevents the next assistant from repeating a path the user already declined. The reason matters more than the rejection itself.
- **Fidelity of numbers** — units, thresholds, dates, and versions are kept verbatim; disputed values are marked unresolved instead of silently picking one reading.

## Agora-specific adaptations

- The verbatim recent suffix is **not** requested from the model, because Agora already provides it via "Recent messages to keep". Configure the app setting instead of adding prompt text.
- The compaction trigger threshold is not controllable via the prompt; it is app-level. No prompt text attempts to influence it.
- Environment and tool state (sandbox files, running Conch jobs, configuration changes) is explicitly preserved because Agora's agentic tools create external state the next assistant must account for.

## Practical settings

1. **Settings → Context → Compact prompt**: paste `system-prompt/4-compact-template.md` verbatim.
2. **Recent messages to keep**: set 10–20 for long agentic sessions; 0 defeats the verbatim-suffix protection.
3. **Compact model**: a smaller model works, but verify rule compliance (Provenance, Fidelity) on a realistic test conversation before trusting it — long strict prompts are the first thing a weak model drops.
4. **Review capsules**: Compact output is a generated summary. Review important facts in the capsule before relying on them, as Agora's manual advises.

## Limitations

A prompt cannot guarantee correct behavior. Chained compactions lose information even with careful prompts. Test this configuration with realistic but non-sensitive scenarios before consequential use, and prefer re-running Compact with a larger "Recent messages to keep" value when summary quality drops.
