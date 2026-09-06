# Reasoning and Routing Framework

This document explains how the repository's reasoning policy is implemented by the current Agora 2.1 prompt architecture. It is documentation, not a second runtime prompt.

## Runtime placement

The permanent method lives in the **System** template:

```text
System
├── reasoning policy and core principles
├── {active_memory}
├── Active Memory interpretation rules
├── {skill_catalog}
├── Skill interpretation and authority rules
├── web / conversation / Memory / shell tool policy
├── approval gate
├── completion policy
└── communication style
```

The **User** template supplies the ordinary-message envelope:

```text
<agora_user_message sent_date="{sent_date}" sent_time="{sent_time}">
{prompt}
</agora_user_message>
```

The **Assistant** template normally contains only its single structural `{prompt}` item. It does not duplicate the User envelope, Active Memory, or Skill Catalog.

## Routing sequence

```text
1. Read the current user message.
2. Select proportional reasoning depth.
3. Decide whether Memory, conversation recall, web, shell, or another tool materially helps.
4. Use {skill_catalog} to discover a relevant Skill.
5. Read the Skill body before applying it.
6. Follow its workflow without overriding System, user, permission, or approval rules.
7. Inspect tool output and verify the result.
8. Answer with facts, estimates, assumptions, recommendations, and limitations separated where useful.
```

The Skill Catalog is discovery. `read_skill_file` is loading. The Skill body is execution guidance. Tool-result inspection is verification. These are separate stages.

## Adaptive reasoning levels

| Level | Appropriate for | Typical runtime behavior |
|---|---|---|
| **0 — Direct** | conversation, translation, rewriting, formatting | answer without unnecessary planning or tools |
| **1 — Checked** | non-trivial self-contained task | identify assumptions and perform a consistency check |
| **2 — Multi-step** | tools, calculations, dependencies, file work | plan prerequisites, execute in order, verify intermediate results |
| **3 — Research** | current, technical, comparative, quantitative, unfamiliar, disputed | read `multi-source-research`, gather evidence, surface conflicts |
| **4 — High risk** | destructive, secret-accessing, irreversible, system-altering, consequential | state exact scope and risk; obtain approval before execution |

## What the System template does not do

It does not contain the complete research loop, memory CRUD manual, or shell-job manual. Those procedures belong in Skills and are loaded only when relevant. The System template provides the routing and safety gates that make progressive disclosure reliable.

## Research routing

For a small factual check, use proportional verification. For multi-source or consequential work, read `multi-source-research` and follow its levels, query diversification, mini-ReAct cycle, source scoring, counter-evidence, bounded iterations, escape hatch, and quality gate.

## Memory routing

Active Memory is current context. Saved Memories are durable information. Memory-governance Skills describe placement, patching, authority, and audits. Do not store a reusable procedure as personal Memory merely because both are Markdown files.

## Tool and safety routing

Before a tool call, identify the exact operation, target, device, permission, and approval requirement. After it, inspect the actual result. A tool call is not evidence of success by itself. Structural, authentication, and permission failures are stop conditions, not invitations to guess.

## Final quality check

Before a non-trivial answer, the System policy asks whether the goal was understood, constraints were met, evidence is sufficient, uncertainty is visible, alternatives were considered, and the response is complete without filler. This is the practical meaning of the repository's reasoning framework.
