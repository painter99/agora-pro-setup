# Troubleshooting

## Skill never loads

- Skill access enabled?
- File exists under Skills (not Memories)?
- Catalog description present and specific?
- `{skill_catalog}` actually in the **System** template?
- Did the model call `read_skill_file`?
- Flat name match (`deep-research` vs `deep-research.md` vs folder path)?

## Too many Skills load

Shorten descriptions. Remove "anything related".

## Memory ops go to the wrong store

Procedures → Skills. Facts → Memories. If the agent writes a workflow into Saved Memory, point it at `00-master-index` and this distinction.

## User envelope missing dates

You are still thinking in Prefix/Suffix. Put `{sent_date}` / `{sent_time}` around `{prompt}` in the **User** tab. Assistant tab stays Prompt-only.

## Variables empty

Spelling, placement, access toggle, Agora version. Disabled Skill access ⇒ empty `{skill_catalog}`.

## Shell / GitHub confusion

`github.com` is not Conch. Fill Conch only if you run a Conch server. For Git: sandbox or your Linux host, then `git` + SSH key.

## Unexpected memory writes

Authority Skill (`03-am-authority`), confirmation matrix, whether the user actually asked to remember.

## Active Memory too large

Move long-form to Saved Memory. Keep status, preferences, Archive Index. Never paste `deep-research` into AM.

## Unsupported claims

Route to `deep-research` when 2+ sources matter. Fetch pages. Surface conflicts. State LIMITED EVIDENCE.
