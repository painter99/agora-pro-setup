# System, User, and Assistant Templates

Agora 2.1 uses **System / User / Assistant**, not the former **System / Prefix / Suffix** arrangement.

## System

System is the complete provider-visible system message. It contains the compact kernel, `{active_memory}`, `{skill_catalog}`, and the permanent safety/tool policy.

## User

User wraps every ordinary user message. In this repository's recommended setup it contains:

```text
<agora_user_message sent_date="{sent_date}" sent_time="{sent_time}">
{prompt}
</agora_user_message>
```

The editor represents `{prompt}` as one immovable **Prompt** block. Build the wrapper from Text and Send Date/Send Time widgets; do not type a second Prompt block.

## Assistant

Assistant contains exactly one immovable **Prompt** block. It should normally remain Prompt-only. The user-message envelope must not be copied around assistant output.

## Variables

Current variables include `{time}`, `{date}`, `{sent_time}`, `{sent_date}`, `{active_memory}`, `{skill_catalog}`, `{current_model_id}`, and `{message_model_id}`. `{model_id}` is a legacy alias.

Variables are resolved immediately before outbound provider requests, including relevant tool continuations and retries. Agora does not append hidden memory or Skill text to a custom System template.
