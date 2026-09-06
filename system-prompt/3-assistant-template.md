# Assistant Template

In Agora, switch to the **Assistant** tab. This template defines the structure **around each ordinary assistant message**.

Keep **exactly one** structural **Prompt** item (`{prompt}`). Agora inserts the original assistant body there. Do not delete it. Do not add a second Prompt item.

---

## Recommended layout

Leave the Assistant template as **Prompt only**:

```text
[Prompt]
```

That is the correct default. The User template already wraps the human message with send date/time. Wrapping assistant output in extra XML is usually noise and can confuse later Context Compact / tool rounds.

---

## Optional additions

You may add text or variables **above or below** the Prompt item, for example `{current_model_id}`, if you have a specific reason. Most setups should not.

Do **not**:

- put `{active_memory}` or `{skill_catalog}` here;
- put `{sent_date}` / `{sent_time}` here unless you have a measured need;
- recreate Prefix/Suffix architecture on the assistant side.

Special paths (tool messages, Compact, title generation) ignore this template.
