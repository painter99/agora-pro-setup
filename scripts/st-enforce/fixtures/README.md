# Fixtures

Status: **UNVERIFIED** — these fixtures are synthetic test data, not captures
of a real goose stream. They mimic the goose 1.59.2 stream-json schema (see
the smoke corpus in the workspace where they were authored); no fixture here
has been validated against a recorded live goose session.

Events use the goose 1.59.2 stream-json schema: assistant messages carry
content items of type toolRequest (id + toolCall.value.name/arguments), user
messages carry toolResponse (id + toolResult.status/value), and the final
assistant message carries text content. `{ST_CANARY}` is a test placeholder
that the fake goose binary in `test_st_goose.py` substitutes with a real
token.

Files:

- `protocol-template.md` — template of the per-run protocol text the wrapper
  injects (`{MIN_THOUGHTS}` and `{ST_CANARY}` are placeholders).
- `stream-pass.jsonl` — stream that satisfies canary + minimum-thoughts checks.
- `stream-fail-noskill.jsonl` — stream that never calls `load_skill`.
- `stream-fail-short.jsonl` — stream with fewer thoughts than required.
