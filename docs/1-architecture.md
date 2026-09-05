# Architecture

Agora Pro Setup is a public configuration collection for the Agora AI application.

## Runtime layers

```text
System template       permanent routing, authority, and safety
User template         ordinary user-message structure
Assistant template    ordinary assistant-message structure
Active Memory         compact current context via {active_memory}
Skill Catalog         native Skill discovery via {skill_catalog}
Skills                reusable procedures read on demand
Saved Memories        persistent information and references
Tools                 capability execution and external effects
Verification          inspection, approval, and result reporting
```

## Runtime flow

```text
User message
→ System template
→ Active Memory and Skill Catalog projection
→ relevant Skill read through tools
→ required Memory or external tools
→ result verification
→ response
```

## Core distinctions

- A System template is not Active Memory.
- Active Memory is not Saved Memory.
- A Skill is not a Saved Memory.
- Skill discovery is not Skill execution.
- Tool invocation is not verified success.
- Repository organization is not the same as Agora's internal storage.

The permanent prompt should be a compact router and safety layer, not a complete manual.
