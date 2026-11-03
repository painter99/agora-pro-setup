# Context-Quarantine Subagent Template

Read-only analysis of a context-heavy side task: reading a large file,
exploring a repository, scanning logs, or digesting a long document — work
whose raw content would clutter the main context with material that is
referenced once and never again.

## Task template

```text
Read-only analysis task. You receive only this task text.

Target: <absolute path(s), or exact locations and scope to read>
Question: <what to find, decide, or summarize — self-contained>
Limits: <what to ignore; any length or count bound>

Output: a compact summary (at most <N> words), the key evidence excerpts with
file and line pointers, and an explicit list of what you did not check.
Do not modify anything. Do not call ask_user or any user-interaction,
automation, or memory/skill create-or-delete tool; list missing inputs in
the "did not check" section instead of asking.
```

## Orchestration rules

- Quarantine subagents never get write tasks; their only output is the report.
- Verify pointers before citing them as fact: read the referenced lines in
  the main loop when the summary feeds a decision.
- The summary, not the raw content, is the only thing that enters the main
  context — that is the point of the pattern.
- Delete the subagent after its result is processed (wait first; if deletion
  is rejected, note it and move on).