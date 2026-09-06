# Installation

## 1. System template

Open **Settings → System Prompts**. Use [`system-prompt/1-system-template.md`](../system-prompt/1-system-template.md).

Required widgets in System:

```text
{active_memory}
{skill_catalog}
```

Place them where the file shows `<active_memory>` / `<skill_catalog>` wrappers.

## 2. User template

Use [`system-prompt/2-user-template.md`](../system-prompt/2-user-template.md).

Keep **one** Prompt item. Wrap it:

```text
<agora_user_message sent_date="{sent_date}" sent_time="{sent_time}">
{prompt}
</agora_user_message>
```

This is the current replacement for Prefix + Suffix.

## 3. Assistant template

Use [`system-prompt/3-assistant-template.md`](../system-prompt/3-assistant-template.md).

Default: **Prompt only**. Do not copy the user XML wrapper here.

## 4. Active Memory

Copy [`active-memory/1-active-memory-template.md`](../active-memory/1-active-memory-template.md). Keep it short. Archive Index lists **Saved Memories**, not Skills.

## 5. Skills

Settings → Skills. Import from `skills/` using **flat** names (see [`skills/README.md`](../skills/README.md)). Add short descriptions.

Start with memory 00–05 + `deep-research` + `tool-execution-contract` + `shell-and-devices`.

## 6. Permissions

Review separately:

- Access Active Memory
- Access Saved Memories
- Allow skill access
- Web search
- Conversation search
- Shell (still needs a configured device)
- MCP / automation if used

Defaults vary by Agora version. Do not assume a tool exists because this repo mentions it.

## 7. Test

- Ordinary question (no tools)
- Question that should load `deep-research`
- "Remember this durable fact" (memory Skill path)
- Blocked delete
- `list_shells` only if a device exists

Inspect each tool card. Do not treat a successful prompt save as proof of routing.
