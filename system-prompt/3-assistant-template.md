# Assistant Template

Use this as a minimal generic **Assistant** template.

```text
<Prompt>
```

The `Prompt` item is Agora's required structural representation of the original assistant message. Keep exactly one `Prompt` item. Do not add a second wrapper that attempts to recreate the former Prefix/Suffix architecture.

Special generation paths such as tool messages, Context Compact, and title generation may use their own application-owned formats.
