# System, User, and Assistant templates

Agora 2.1 replaced **System / Prefix / Suffix** with **System / User / Assistant**.

## What the tabs mean

| Tab | Owns |
|---|---|
| **System** | Entire provider-visible system message |
| **User** | Structure around each ordinary **user** message |
| **Assistant** | Structure around each ordinary **assistant** message |

User and Assistant each have exactly one structural **Prompt** item (`{prompt}`). It cannot be deleted or duplicated. Text and variables go above or below it.

## Variables

Current variables include:

```text
{time} {date}
{sent_time} {sent_date}
{active_memory}
{skill_catalog}
{current_model_id} {message_model_id}
```

`{model_id}` remains a legacy alias of `{current_model_id}`.

`{sent_date}` / `{sent_time}` stamp **that message**. `{date}` / `{time}` are clock-now. For the user envelope, prefer send-time.

Variables resolve immediately before each outbound provider request (including tool continuations). Empty or disabled variables resolve to empty strings. Agora does not append hidden memory or Skill text.

## Recommended mapping from the old Prefix/Suffix setup

Old Prefix+Suffix XML:

```text
<agora_user_message sent_date="…"> … </agora_user_message>
```

Now lives entirely in the **User** tab, around `{prompt}`.

The **Assistant** tab should stay Prompt-only unless you have a measured reason otherwise.

## Do not

- Put `{skill_catalog}` only in User/Assistant — the model needs it on the System message.
- Leave `{active_memory}` out of System because "Agora used to auto-inject" — custom templates must place the variable.
- Recreate Prefix/Suffix as if those tabs still exist.
