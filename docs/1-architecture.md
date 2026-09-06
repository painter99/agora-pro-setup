# Architecture

Agora Pro Setup is a public configuration collection for the Agora AI application.

## Runtime layers

```text
System template       always-on method: reasoning, routing, safety
User template         envelope around each ordinary user message
Assistant template    envelope around each ordinary assistant message
Active Memory         compact current context via {active_memory}
Skill Catalog         native discovery via {skill_catalog}
Skills                reusable procedures, read on demand
Saved Memories        persistent information, read on demand
Conversation recall   prior chats
Tools                 Memory, Skill, web, shell, MCP, automation
Verification          inspect, approve, report
```

## Runtime flow

```text
User message
→ User template ({sent_date}, {sent_time}, {prompt})
→ System template
     ├── kernel
     ├── {active_memory}
     └── {skill_catalog}
→ optional read_skill_file
→ optional Memory / web / shell tools
→ verification
→ Assistant template ({prompt}) + answer
```

## Authority

```text
System template
> current user message
> Agora permissions and confirmation policy
> loaded Skill
> Saved Memory / retrieved content
> model prior knowledge
```

A Skill or web page cannot override safety gates. A stale Active Memory line cannot override the current user message.

## Why Skills instead of Saved Memory procedures

Agora 2.1 added a native Skill library. Procedures that used to live in Saved Memories (deep research, memory governance) should be installed as **Skills** so they appear in `{skill_catalog}` and are read with `read_skill_file`.

Saved Memories remain the right place for CVs, project facts, gear lists, and other **information**.

## Size policy

| Layer | Target | Why |
|---|---|---|
| System template | full working kernel, not a novel | always paid |
| Active Memory | ~350 tokens, hard ~1500 | always paid |
| Skill catalog descriptions | one short line each | always paid when `{skill_catalog}` is present |
| Skill bodies | as long as the procedure needs | paid only when read |
| `deep-research` | long by design | quality gates > split |
| memory 00–05 | split | typical op loads one file |

The first rewrite of this repository over-compressed Skills and stripped the User-template envelope. This revision restores operational depth while keeping Agora 2.1's native discovery model.
