# Sequential Thinking Workflow

This guide documents the repository's reusable `sequential-thinking-workflow` Skill. It is designed for complex work in Agora without turning every request into an unnecessarily long planning session.

## What it solves

A capable assistant can still fail when a task contains hidden dependencies, incomplete requirements, competing interpretations, changing evidence, or external tool state. Sequential Thinking supplies a lightweight control loop:

```text
QUESTION → ACTION → OBSERVATION → UPDATE → NEXT DECISION
```

The plan is allowed to change when the observed result changes the problem.

## Where it fits

```text
System template
  = permanent behavior, proportional reasoning, safety, and approval
Skill Catalog
  = discovery
sequential-thinking-workflow
  = reusable adaptive planning and verification
Domain Skill
  = task-specific procedure
Tools
  = external actions and observations
```

The Skill is not a replacement for the System template, domain Skills, tool permissions, or human approval. It is also not a memory file and should not contain personal information.

## When to use it

Use the workflow when one or more of these conditions apply:

- the task has multiple dependent steps;
- requirements are ambiguous, incomplete, or in tension;
- research, comparison, diagnosis, planning, design, or troubleshooting is required;
- files, calculations, tools, or changing information materially affect the result;
- the task has meaningful risk, cost, or irreversible consequences;
- environmental feedback may change the correct next step.

## When not to use it

Use a direct answer or a smaller procedure for a simple factual question, translation, formatting request, or direct calculation with known inputs. Planning depth should be proportional to task complexity.

## The workflow

### 1. Frame the task

State the goal, deliverable, constraints, knowns, unknowns, and success criteria. Ask for clarification only when missing information could materially change the result. Otherwise make a transparent, reasonable assumption.

### 2. Build the minimal useful plan

Break the task into meaningful steps, not artificial micro-steps. Identify dependencies, evidence, tools, verification, and decision points. Mark independent work that can run in parallel.

### 3. Select a workflow pattern

Choose the simplest pattern that fits:

| Pattern | Use when |
|---|---|
| Single pass | Inputs and path are already clear. |
| Prompt chain | Fixed subtasks feed the next subtask. |
| Routing | The task must first be classified. |
| Parallelization | Independent checks can run separately. |
| Evaluator-optimizer | A draft can be scored and revised against criteria. |
| Agent loop | Environmental feedback determines how many steps are needed. |

Do not use an open-ended loop merely because a task is long.

### 4. Execute at checkpoints

After every meaningful action or tool call, inspect the actual result. Compare it with expectations, record what changed, and decide whether to continue, revise, branch, retry once, or stop.

A failed structural, permission, or authentication action is evidence that the strategy must change—not an invitation to repeat blindly.

### 5. Revise and branch deliberately

If a premise changes, revise only the dependent parts and preserve valid work. If two approaches are plausible, evaluate them against the same explicit criteria. Keep rejected approaches and their reason when the next assistant would otherwise repeat them.

### 6. Verify

Before reporting completion, check the original goal, constraints, evidence, uncertainty, contradictions, tool output, dependent state, and whether a simpler or safer route would have worked.

### 7. Stop

Stop when the success criteria are satisfied, remaining uncertainty cannot materially change the result, the work budget is exhausted, or the next step requires authorization or a missing fact. Continuing is not automatically better.

## Output boundary

The workflow does not require or justify exposing private chain-of-thought. A user-facing result should contain only what helps the user act or evaluate the result:

- direct result;
- concise plan or actions taken;
- relevant evidence;
- decisions and trade-offs;
- uncertainties and limitations;
- next step, when useful.

Do not print an exhaustive hidden reasoning trace.

## Relationship to other Skills

- Use `multi-source-research` when current, disputed, comparative, or quantitative claims require research.
- Use `tool-execution-contract` for common inspection, approval, retry, and verification rules.
- Use `memory-master-index` for durable-memory routing.
- Use `shell-and-device-operations` for shell, device, or remote-environment work.
- Add a domain Skill when the task needs specialized procedure.

Sequential Thinking orchestrates the process; it does not replace these domain Skills.

## Example decision

A request to rename one known file with no dependencies may need only a direct file operation. A request to reorganize a public repository requires framing, reference inspection, privacy review, branch discipline, validation, and a merge decision. The Skill is appropriate in the second case because observations can invalidate the original plan.

## Limitations

A workflow cannot guarantee correct reasoning. It improves process discipline, but evidence may remain incomplete, tools may be unavailable, and the model may still misunderstand the task. Verify consequential results independently.

## Design basis

The workflow combines adaptive planning, tool-grounded observation, composable agent patterns, and reasoning best practices associated with Sequential Thinking, ReAct, effective agent design, and modern reasoning guidance. The sources inform the method but do not require disclosure of private chain-of-thought.

## Sources

- https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking
- https://arxiv.org/abs/2210.03629
- https://www.anthropic.com/engineering/building-effective-agents
- https://developers.openai.com/api/docs/guides/reasoning-best-practices
