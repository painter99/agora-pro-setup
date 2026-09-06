# System, User, and Assistant Templates

Current Agora uses three ordered templates rather than the former System/Prefix/Suffix arrangement.

## System

Defines the complete provider-visible system message. It may contain text blocks and predefined variables such as `{active_memory}` and `{skill_catalog}`.

## User

Defines ordinary user messages and must contain exactly one structural `Prompt` item. Optional text or variables may surround it.

## Assistant

Defines ordinary assistant messages and must contain exactly one structural `Prompt` item.

## Important behavior

Variables are resolved immediately before outbound provider requests, including relevant continuations and retries. The selected structured System template owns the system prompt; Agora does not silently append hidden memory or Skill text.

Special paths such as tool messages, Context Compact, and title generation may have dedicated formats.

## Migration rule

Do not reproduce the former Prefix/Suffix XML wrapper as the current installation. Use the templates in `system-prompt/`.
