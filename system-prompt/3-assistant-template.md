# Assistant Template

In Agora, switch to the **Assistant** tab. This template defines the structure around each ordinary assistant message.

The Assistant template must contain exactly one structural **Prompt** item. The Prompt item represents the original assistant message and cannot be deleted or duplicated.

---

## Exact block order

### Block 1 — Structural Prompt item

Keep Agora's built-in **Prompt** item (`{prompt}`) as the only block.

The resulting assistant template is:

```text
[Prompt]
```

## Why Assistant stays Prompt-only

The timestamped `<agora_user_message>` envelope belongs to the User template because it describes the user's submitted message. It must not be copied around assistant output.

Keeping Assistant Prompt-only also avoids adding artificial XML or metadata to ordinary assistant messages and leaves Agora's dedicated formats free to handle tool messages, Context Compact, and title generation.

## Optional additions

Text or variables may be placed above or below Prompt only for a deliberate, tested use case. Do not add `{active_memory}`, `{skill_catalog}`, or the User XML envelope here.
