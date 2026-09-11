# Multi-Agent System for Agora

> Status: proposal for discussion and future implementation
> Scope: native Agora architecture, not a requirement for the current app

## 1. Purpose

Agora already provides the main building blocks for agentic workflows: a model, tools, Skills, memory, web and search, MCP, shell access, Tasks, Loops, and local or remote execution. This document proposes an optional **Multi-Agent System (MAS) layer** that users could configure after installation.

The goal is not to make every conversation multi-agent. The goal is to let a user compose a small, inspectable team of specialized agents when a single agent, prompt, or tool set is no longer sufficient.

The default installation should remain useful as a single agent. MAS should be an opt-in capability with clear boundaries, visible execution, and graceful degradation when a tool or model is unavailable.

## 2. Design principles

1. **Single-agent first.** Use one agent when one agent with clear tools and instructions is sufficient.
2. **Skills are reusable capability definitions.** A Skill may describe a role, procedure, tool policy, or output contract; it is not automatically a running agent.
3. **Agents are configured runtimes.** An agent combines instructions, a model, tools, Skills, memory scope, permissions, and an output contract.
4. **One owner of the user-facing answer.** A manager or supervisor remains responsible for synthesis unless the user explicitly chooses a handoff.
5. **Read before write.** A worker must inspect state before changing it and verify every consequential result.
6. **Least privilege.** Each agent receives only the tools, memory, repositories, and permissions it needs.
7. **Human approval at boundaries.** Publishing, deletion, purchases, messages, credentials, system changes, and recurring automation require explicit approval.
8. **Runtime evidence wins.** Documentation and configuration may describe a capability, but only an observed runtime result proves that it is available in a particular run.
9. **Observable execution.** The UI should show which agent ran, which tools were used, what was returned, and where approval or failure occurred.
10. **Bounded autonomy.** Every run has limits for turns, depth, time, cost, tool calls, and delegation.

## 3. Terminology

| Term | Meaning |
|---|---|
| **Skill** | Reusable Markdown or structured instructions, procedure, policy, or output contract. |
| **Agent profile** | User-configured definition combining model, instructions, Skills, tools, memory scope, and permissions. |
| **Worker** | An agent invoked for a bounded subtask. |
| **Manager** | An agent that keeps ownership of the user conversation and calls workers as tools. |
| **Supervisor** | A coordinator that decomposes a complex request, delegates work, monitors results, and synthesizes an answer. |
| **Handoff** | Transfer of conversational ownership to another agent. |
| **Run** | One bounded execution with an input, state, tool calls, results, and terminal outcome. |
| **Team** | A saved or dynamically assembled set of agent profiles and routing rules. |
| **Task** | A scheduled or manually triggered automation. It is not automatically equivalent to an agent or a Skill. |

## 4. Recommended default architecture

```text
User
  |
  v
Agora conversation
  |
  v
MAS Router / Supervisor
  |-- direct answer by primary agent
  |-- manager calls bounded worker agents
  |-- optional handoff to a specialist
  |-- optional Task or Loop proposal
  |
  +--> Agent Registry / Team definition
  |       +--> agent profiles
  |       +--> Skill references
  |       +--> tool and permission scopes
  |       +--> model selection and limits
  |
  +--> Context and state layer
  |       +--> conversation branch
  |       +--> Active Memory
  |       +--> selected Saved Memories
  |       +--> run state and audit trail
  |
  +--> Tool layer
          +--> data and retrieval tools
          +--> action tools
          +--> orchestration tools
          +--> MCP and external services
```

This is a logical architecture. In an initial implementation, several components may remain inside the existing generation pipeline rather than becoming independent services.

## 5. Two orchestration modes

### 5.1 Manager mode — recommended default

The primary agent remains responsible for the conversation and final answer. Specialist agents are exposed as bounded capabilities, similar to tools.

Use this mode when:

- the user expects one coherent answer;
- specialists provide research, checking, classification, or transformation;
- the manager must enforce a common policy and approval gate;
- worker output should be synthesized rather than shown as a separate conversation.

Example:

```text
Primary Agora agent
  -> calls Memory auditor
  -> calls Repository researcher
  -> calls Capability diagnostician
  -> verifies reports
  -> gives one final answer
```

### 5.2 Handoff mode — optional

The current agent transfers conversational ownership to a specialist.

Use this mode when:

- the specialist should directly continue the conversation;
- the branch has a genuinely different policy or tool set;
- the user can see and accept the change of active agent.

Handoffs should preserve only the necessary context and should record the source agent, target agent, reason, and transferred state.

## 6. Dynamic team assembly

A supervisor may assemble a team per run from installed Skills and saved agent profiles. It must not silently create unrestricted autonomous agents.

Suggested flow:

```text
1. Classify the request.
2. Decide whether a single agent is sufficient.
3. Identify the minimum required capabilities.
4. Select compatible agent profiles and Skills.
5. Compute the combined tool, memory, and approval scope.
6. Present or record the execution plan when the run is complex.
7. Run workers sequentially or in parallel within limits.
8. Validate worker results and resolve conflicts.
9. Synthesize the final answer.
10. Stop, report, and persist only approved state changes.
```

Dynamic assembly should use a **capability registry**, not only free-text Skill names. A registry entry should include:

```yaml
id: agora-maintenance
kind: agent-profile
purpose: Audit and repair the local Agora setup
skills:
  - tool-execution-contract
  - skill-governance
  - memory-audits
tools:
  - list_skill_files
  - read_skill_file
  - list_memory_files
  - read_memory_file
  - web_fetch
permissions:
  memory_write: deny
  repository_write: deny
  task_write: approval-required
limits:
  max_turns: 12
  max_delegation_depth: 1
```

The exact format is illustrative. A future native implementation could use a typed schema rather than YAML.

## 7. Built-in profiles after installation

A useful default installation could include profiles that are disabled until needed:

| Profile | Default role | Default write scope |
|---|---|---|
| **General Assistant** | Direct conversation and ordinary tool use | No external write without approval |
| **Coordinator** | Routes requests, assembles bounded teams, synthesizes reports | No direct write by default |
| **Maintenance** | Audits setup, Skills, memory references, and runtime capabilities | Small reversible repair only, if enabled |
| **Researcher** | Current web and repository research with source verification | Read-only |
| **Memory Steward** | Routes and audits Active/Saved Memory | Write only after read and approval policy |
| **Capability Diagnostician** | Verifies tools, MCP, Tasks, models, and generation-path limits | Read-only |
| **Task Planner** | Produces bounded Task specifications and checks schedules | Task write requires approval |
| **Reviewer** | Evaluates claims, conflicts, safety, and completion evidence | Read-only |

The user should be able to disable, duplicate, edit, or replace these profiles.

## 8. Tasks and automation

Tasks are a powerful future orchestration surface, but task creation must be treated as an external side effect.

A safe native design should distinguish:

- **task proposal** — an agent describes a task but does not create it;
- **task creation** — creates a stored automation after user approval;
- **task execution** — runs with a snapshot of its profile, Skills, tools, and permissions;
- **task supervision** — reports progress, failures, and approval requests;
- **task cancellation** — stops future runs and active work according to explicit policy.

A Task must not be allowed to recursively create more Tasks by default. If self-scheduling or task creation is ever supported, it needs:

- a dedicated capability and permission;
- maximum delegation depth;
- maximum number of child Tasks;
- expiration or review date;
- loop detection;
- audit log;
- user-visible approval;
- a kill switch.

A scheduled Task must store or reference a versioned snapshot so that a later Skill or prompt edit does not silently change an existing automation. The UI should show whether the Task uses the current profile or a pinned revision.

## 9. Permission model

Permissions should be attached to an agent profile and narrowed further for each run.

Suggested capability classes:

- **Observe:** read current configuration, Skills, memory, conversations, and tool availability.
- **Retrieve:** web, repository, search, RAG, and external read-only sources.
- **Transform:** draft, summarize, analyze, calculate, or generate a proposal.
- **Modify:** edit Skills, memory, files, or local configuration.
- **External effect:** send, publish, purchase, delete, schedule, or change an external system.
- **Orchestrate:** call other agents, create Tasks, hand off, or start a Loop.

Default policy:

```text
Observe and retrieve: allowed when configured.
Transform: allowed within run limits.
Modify: read-before-write and policy-gated.
External effect: explicit user approval.
Orchestrate: bounded; Task creation and recursive delegation require approval.
```

## 10. Context and memory isolation

Workers should not automatically receive the complete conversation, Active Memory, or all Saved Memories. The supervisor should pass a minimal context package:

```text
- user request and relevant constraints;
- required facts from Active Memory;
- selected Saved Memory references or excerpts;
- task objective and expected output;
- permitted tools and approval state;
- confidentiality and retention policy.
```

The system should record what context was passed to each worker. Sensitive memory should be excluded unless required for the task.

## 11. Failure handling and verification

Every worker result should have a typed outcome:

```text
COMPLETED
PARTIAL
BLOCKED — approval required
UNAVAILABLE — capability missing
FAILED — tool or provider error
CONFLICT — outputs disagree
CANCELLED — limit or user stop
```

The supervisor must not treat a worker response as proof that an action happened. It should verify the underlying tool result or durable state before reporting success.

Runs should stop on:

- approval requirement;
- unavailable required capability;
- maximum turns, depth, time, cost, or tool calls;
- repeated failures without new evidence;
- contradictory results that require user judgment;
- user cancellation.

## 12. User interface requirements

A usable MAS feature needs more than a prompt field. The UI should provide:

1. **Team builder** — select profiles, Skills, models, tools, and memory scopes.
2. **Agent registry** — inspect purpose, version, dependencies, permissions, and status.
3. **Run plan** — show selected agents and expected sequence before complex execution.
4. **Live trace** — show agent, tool, input/output boundary, duration, and result status.
5. **Approval cards** — approve or reject specific actions, not vague future autonomy.
6. **Context inspector** — show which memory and conversation context was passed.
7. **Budget controls** — turns, time, tokens, cost, parallel workers, and delegation depth.
8. **Versioning** — pin or update profiles, Skills, prompts, and Task snapshots.
9. **Test mode** — dry-run read-only execution before enabling writes or automation.
10. **Kill switch** — stop the run, team, or scheduled Task.

## 13. Evaluation and observability

MAS should ship with evaluation support rather than relying on anecdotal success.

Minimum metrics:

- final task success;
- correct routing rate;
- unnecessary delegation rate;
- tool-call accuracy;
- verification compliance;
- approval bypass attempts;
- latency and token/cost budget;
- worker failure and retry rate;
- disagreement and conflict rate;
- user correction rate.

A built-in test suite could include:

- direct question that should not delegate;
- memory question where Active Memory already contains the answer;
- repository architecture question;
- read-only audit;
- attempted write without approval;
- unavailable-tool scenario;
- conflicting worker reports;
- recursive Task creation attempt;
- cancellation during a worker run.

## 14. Incremental implementation path

### Phase 0 — current Agora

- one primary agent;
- native Skills and tools;
- manual Task specifications;
- explicit approval and runtime capability checks.

### Phase 1 — inspectable profiles

- saved agent profiles;
- tool and memory scopes;
- profile versioning;
- dry-run mode;
- run trace and permission display.

### Phase 2 — manager mode

- a primary agent can invoke a profile as a bounded worker;
- structured worker input/output;
- result verification and synthesis;
- parallel workers with budgets.

### Phase 3 — supervised Tasks

- agent proposes Tasks;
- user approves creation;
- Task runs use pinned profile and Skill snapshots;
- progress and failure reporting;
- cancellation and kill switch.

### Phase 4 — optional dynamic MAS

- per-run team assembly from the registry;
- policy-based routing;
- optional handoffs;
- bounded nested orchestration;
- evaluation and performance dashboard.

## 15. Relevance to the current setup

The current `agora-pro-setup` architecture already provides useful foundations:

- System template as permanent routing and safety kernel;
- Active Memory as compact current context;
- Saved Memory as durable information;
- Skill Catalog and on-demand Skill loading;
- capability gating based on observed runtime results;
- tool execution contracts and verification;
- coordinator repository awareness;
- sequential thinking for complex work.

The next practical step does not require pretending that Skills are already independent agents. We can define the contracts and profiles now, test them as one-agent routing, and leave the native MAS runtime as a future Agora feature.

## 16. Open questions for Agora

1. Should an agent profile be stored inside an Agora archive and synced with conversations?
2. Are Skills immutable references, versioned snapshots, or live files during a run?
3. Should the manager see raw worker transcripts or only structured reports?
4. How should provider/model selection work across workers?
5. Can local models and remote providers participate in the same team?
6. What is the approval UX for Task creation and external effects?
7. How are secrets isolated between profiles and MCP servers?
8. What happens when a Task runs with a different toolset than ordinary chat?
9. How are costs and context budgets divided among workers?
10. Can users export and share a team definition without sharing personal memory or credentials?

## 17. Non-goals

This proposal does not require:

- autonomous unrestricted agents;
- hidden background work;
- automatic sharing of all user memory;
- direct repository writes;
- a new agent protocol before the basic profile and permission model is clear;
- replacing the current single-agent experience.

## References

- Agora application: https://github.com/newo-ether/Agora
- Agora setup architecture: https://github.com/painter99/agora-pro-setup
- Anthropic, Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- OpenAI, Orchestration and handoffs: https://developers.openai.com/api/docs/guides/agents/orchestration
- Model Context Protocol architecture: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
