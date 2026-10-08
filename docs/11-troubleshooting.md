# Troubleshooting

## Skill does not load

Check Skill access, the saved file, short catalog description, exact flat name, `{skill_catalog}` in System, and whether the model actually called `read_skill_file`.

## Wrong memory layer is used

Facts and durable context belong in Memory. Reusable procedures belong in Skills. Check `memory-master-index` and do not route Skill CRUD through Memory tools.

## User dates are missing

Put the Send Date and Send Time widgets around the single Prompt block in **User**. Do not recreate Prefix/Suffix.

## Active Memory is missing

Place `{active_memory}` in **System** and check Access Active Memory. Custom templates do not receive hidden Active Memory text.

## Shell fails

Check selected device, authentication, host-key policy, confirmation setting, and durable `job_id`. Stop retrying structural or permission failures.

## Repeated failed tool calls

The model repeats a failed call with unchanged parameters, or loops on the same query type. The setup's retry discipline lives in `docs/21-tool-call-budget.md` and `tool-execution-contract`: never repeat an identical failed call, adjust after two consecutive failures, exhaust a query type after three failed rounds. If the model breaks this rule, tighten the System-template sentence — prompt-level enforcement is not guaranteed; a native per-generation budget would be (see `docs/16` §12).

## Unsupported research claim

Load `multi-source-research` for multi-source work, fetch pages rather than trusting snippets, surface conflicts, and state `LIMITED EVIDENCE` when appropriate.
