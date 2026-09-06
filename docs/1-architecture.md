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
→ User template ({sent_date}, {sent_time}, {prompt})
→ System template ({active_memory}, {skill_catalog}, kernel)
→ relevant Skill read through `read_skill_file`
→ required Memory or external tools
→ result verification
→ Assistant template ({prompt})
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


## Reasoning placement

The System template contains the permanent reasoning levels, tool decision gate, research routing, approval gate, completion policy, and communication style. `docs/6-reasoning-framework.md` explains that runtime behavior; it does not replace the System template. Detailed research and memory procedures remain in Skills.
