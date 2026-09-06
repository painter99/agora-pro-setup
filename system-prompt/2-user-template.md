# User Template

In Agora, switch to the **User** tab. This template defines the structure **around each ordinary user message**.

Keep **exactly one** structural **Prompt** item (`{prompt}`). You may add text and variables above or below it. This replaces the former Prefix + Suffix tabs.

The layout below matches a working Agora 2.1 User template: wrap the message in XML and stamp `{sent_date}` / `{sent_time}`.

---

## Block order

### Block 1 — Text

```text
<agora_user_message sent_date="
```

### Block 2 — Variable widget

Click `+` and insert **Send Date** (`{sent_date}`).

### Block 3 — Text

```text
" sent_time="
```

### Block 4 — Variable widget

Click `+` and insert **Send Time** (`{sent_time}`).

### Block 5 — Text

```text
">
```

Include a trailing newline so the original message does not stick to the opening tag.

### Block 6 — Prompt (required, immovable)

The structural **Prompt** item. Agora inserts the original user message here. Do not delete it. Do not add a second Prompt item.

### Block 7 — Text

```text
</agora_user_message>
```

Include a leading newline so the closing tag does not stick to the message.

---

## Preview (what the model should see)

```text
<agora_user_message sent_date="2026-05-09 Sat" sent_time="10:05:00">
[Prompt]
</agora_user_message>
```

`{sent_date}` and `{sent_time}` are resolved immediately before each outbound provider request, including tool continuations. Editor previews use example values.

---

## Rules

- Do **not** put `{active_memory}` or `{skill_catalog}` in the User template. Those belong in **System**.
- Do **not** recreate Prefix/Suffix tabs. The User template is the current place for this wrapper.
- `{date}` / `{time}` are clock-now values. `{sent_date}` / `{sent_time}` are the timestamp of **this message**. Prefer send-time for user-message envelopes.
- Tool messages, Context Compact, and title generation use Agora's own formats and ignore this template.
