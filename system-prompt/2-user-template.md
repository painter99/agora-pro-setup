# User Template

Use this as a minimal generic **User** template.

```text
<user_message>
<Prompt>
</user_message>
```

The `Prompt` item is Agora's required structural representation of the original user message. Keep exactly one `Prompt` item. Optional date or time variables may be placed around it only when the current Agora version exposes and requires them.

Do not use this template to duplicate the System template, Active Memory, or Skill Catalog. User-specific instructions belong in the user message or in the appropriate persistent layer.
