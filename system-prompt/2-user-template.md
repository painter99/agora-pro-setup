# User Template

In Agora, switch to the **User** tab. This template defines the structure around each ordinary user message.

The User template is where the former Prefix/Suffix message envelope belongs in Agora 2.1. Keep exactly one structural **Prompt** item. The Prompt item represents the original user message and cannot be deleted or duplicated.

---

## Exact block order

### Block 1 — Text

Paste:

```text
<agora_user_message sent_date="
```

### Block 2 — Variable widget

Insert **Send Date** (`{sent_date}`).

### Block 3 — Text

Paste:

```text
" sent_time="
```

### Block 4 — Variable widget

Insert **Send Time** (`{sent_time}`).

### Block 5 — Text

Paste:

```text
">
```

Keep a newline after the closing `>` so the user message starts on its own line.

### Block 6 — Structural Prompt item

Keep Agora's single required **Prompt** item (`{prompt}`) here.

Do not replace it with manually typed `{prompt}` text. Do not add a second Prompt item.

### Block 7 — Text

Paste:

```text
</agora_user_message>
```

Keep a newline before the closing tag so it appears after the message body.

---

## Expected preview

```text
<agora_user_message sent_date="2026-05-09 Sat" sent_time="10:05:00">
[Prompt]
</agora_user_message>
```

The editor displays the structural item as `[Prompt]`; the provider request receives the original user-message content.

## Rules

- Do not place `{active_memory}` or `{skill_catalog}` in User. They belong in System.
- `{sent_date}` and `{sent_time}` describe the message being sent.
- `{date}` and `{time}` represent current clock values and are not needed for this envelope.
- Variables are resolved immediately before the outbound provider request, including relevant tool continuations and retries.
- Tool messages, Context Compact, and title generation may use dedicated application-owned formats.
