# Two-agent bridge and the Manus-style working environment

This document has two halves that belong together.

- **Part 1 is a case study.** How a reference cloud agent product (Manus)
  actually works according to its own documentation, what independent users
  report about it, and how a two-agent setup — a coordinating agent and a
  coding agent working on the same repositories — reproduces the properties
  that make such a product feel like a personal working environment.
- **Part 2 is the operating contract.** The shared workflow record both agents
  read: division of labour, delegation policy, dispatch modes, the brief and
  report contract, where the shared skills live, and the decision log.

The generic dispatch contract lives in the skill `agora-goose-bridge`. The
public generic operating-procedure base is [`docs/35-two-agent-operating-procedure.md`](35-two-agent-operating-procedure.md);
each project's topology, commands, paths and approved deviations stay in its
private project adapter. Neither side copies the other: a change to the shared
contract changes this document and is refreshed into the project copies; a
change to the public base is reviewed against each adapter, and local details
remain private.

Status: case study and workflow record, updated 2026-11-17. This document is a
working agreement and a research record, not an authorization. The operator's
current instruction and each repository's `AGENTS.md` decide every approval.

---

# Part 1 — Case study: a Manus-style working environment, built locally

## 1.1 Why this case study exists

An operator asked for a personal working environment with the properties the
Manus workflow appears to have: context that survives a session, reusable
procedures, a research trail with sources, explicit human gates, and artifacts
that outlive the turn that produced them. The question behind the request was
not which product is best. It was: **which mechanisms actually create that
feeling, and which of them can be reproduced on a machine the operator owns.**

That question needs evidence about the reference product rather than memory of
it, and the evidence has to be separated by quality. Three bodies of material
were collected for this document:

1. the product's own documentation and help centre — primary, but vendor
   statements about what the product offers, not about how well it performs;
2. independent user reports from a public forum and a public news aggregator —
   anecdotal, and about real usage;
3. the project's own issue tracker — the only substantial public channel of the
   application this repository documents.

The result is deliberately bounded. Where the evidence is thin, this document
says so instead of filling the gap with a plausible story. Where a comment
carries a commercial interest, it is labelled as such and is not counted as
community opinion.

## 1.2 How the reference product actually works

All statements in this section come from the product's own documentation and
help centre, accessed 2026-11-17. They describe what the product offers. They
are not evidence of how reliably it delivers.

### The execution model

Manus is described as an autonomous general agent that takes a task and delivers
a result rather than answering a question. It runs in a sandbox environment — a
virtual computer with internet access, a persistent file system, the ability to
install software and create tools — and it can connect to the user's own
applications (mail, notes, chat, code hosting) through connectors. The
documentation's own framing is "a virtual colleague with its own computer".

A desktop application extends the same model to the user's own machine. The
agent gets access to a chosen folder, the terminal and the hardware; it can
work on files, run command-line tools and use local compute. Local actions are
governed by a permission mode with three levels: ask for approval on every
local action, approve safe actions automatically and ask only when a decision is
needed, or run everything without approval. In the two gated modes the agent
stays inside the task workspace, and network access, writes outside the
workspace and a change of working folder all require approval. Two limits are
worth stating explicitly, because they are easy to over-read: the permission
modes govern **local actions such as commands and file changes, not every read
the agent performs**, and the planning still happens in the vendor's cloud — the
desktop application is a remote agent with local reach, not a local model.

### Persistent workspaces (Projects)

A Project is a persistent workspace with a **master instruction** and a
**knowledge base** of files. Every new task created inside the project inherits
that configuration, which removes the repeated setup that makes recurring work
expensive. Instruction changes apply to the current task; file changes apply
only to tasks created afterwards, so earlier tasks keep the configuration they
were started with. Projects and tasks are private by default; an invited
collaborator sees the shared instruction and knowledge base but only the tasks
they created themselves.

### Reusable procedures (Skills)

Skills are file-system-based packages that encode a capability or a workflow:
an instruction file with optional scripts, references and templates. They are
loaded on demand rather than injected into every request, and the documentation
describes this as progressive disclosure. Four acquisition paths are documented:
ask the agent to package a successful interaction as a skill, upload a local
archive or folder, install from the curated official library, or import directly
from a public repository. A skill is invoked with a slash command. The
documentation also tells users to audit community skills before use, because
they can contain code and shell commands, and it gives the exact prompt to use
for that audit.

### Work that continues without the user (Automations)

Three kinds are documented:

| Kind | Starts when | Documented example |
|---|---|---|
| Schedule | a chosen time | a daily brief, a weekly report, recurring research |
| Triggered task | an event in a connected app | a pull request is opened, a refund is created, an invoice mail arrives |
| Advanced automation | a natural-language description | a routine that combines several sources, conditions and actions |

The triggered form is the interesting one for engineering work: the documented
example reacts to a pull request being opened, filters on the base branch and
draft status, summarises the change, identifies high-risk files, checks whether
the main behaviour is covered by tests, and posts a review only when there is a
clear actionable finding — otherwise it sends the summary to the user.

### Splitting work (Parallel Tasks and Wide Research)

**Parallel Tasks** lets a request be decomposed into separate tasks, each with
its own chat and its own result, all running at the same time. The task that
made the request stays in charge: it checks progress, reads the results and can
steer one task or all of them. A new task does not see the chat history of the
main task, so it must be given a self-contained brief. The documented best
practice is to start in a Project, because the Project carries the shared
context.

**Wide Research** is the same decomposition applied at scale. The main agent
analyses the request, splits it into independent sub-tasks, assigns each to a
dedicated agent with a fresh context window, and synthesises the results into
one output. The stated reason is a context-window effect: when many similar
items are processed sequentially, later items degrade as the context fills, and
the vendor cites a "fabrication threshold" around eight to ten items. The
architectural claim is that item two hundred fifty receives the same depth of
analysis as item one.

### Branching and running on your own key

A **Branch** takes any reply into a new task while keeping everything up to
that point, leaving the original task unchanged. **Flex** lets the agent run
with the user's own inference provider key: the user chooses the provider, the
model and the effort level, the provider bills the model usage, and the
platform credits cover the sandbox and the media features. The documented
providers include several large model houses and three inference partners.
The documentation is explicit that provider rate limits and quotas apply, that
quality and speed depend on the chosen model, and that the platform does not
guarantee third-party model performance.

### What it costs (vendor-stated)

From the help centre, updated during October and November 2026 and accessed
2026-11-17: a free plan with a daily credit refresh, one concurrent task and
two scheduled automations; two paid tiers starting at a monthly price with
monthly credit bundles, twenty concurrent tasks and twenty scheduled automations
each; and a team plan priced per seat. The credit rules page states that
consumption follows model tokens, virtual machines and third-party APIs, that
it varies with task complexity and duration, that completed tasks keep their
storage without further credit, and that a task failing for a technical reason
on the vendor's side is refunded. Daily credits are capped, are usable only in
the lightest agent mode, and monthly credits do not roll over. A separate page
states that **both** chat and agent modes consume credits, which makes older
statements about free chat stale.

Two cautions on these numbers: they are vendor statements on the access date,
not independent measurements, and the vendor itself points readers to the live
pricing page. A public forum comment from an earlier period complains about
price and limited credits; that is a dated impression without plan or usage
details and must not be merged into the current table.

## 1.3 What independent users report

### A public agent forum, read through a public archive

Direct requests to the forum platform were refused by its network policy during
this research, so the material was read through a public archive of public
posts. The archive query returned 120 records that resolve to **10 distinct
comment bodies across 4 threads** in one subreddit, with comment dates from
2026-11-07 to 2026-11-16; the archive's pagination repeated the same page set,
which is why the record count is larger than the distinct count. The four
threads ask four different questions: which agent to use for building agent
workflows, which tool keeps a research report updatable when its sources
change, which alternative to use when the job must end in real files, and how
a competing bot product is performing.

A thread about agent choice is also a marketing surface, so every distinct
comment is classified below. Five of the ten carry a referral link, an invite
link, a self-disclosure or an explicit commercial interest; four more are
opinions that recommend named products; one is a self-report with no commercial
link and no product recommendation.

| # | Thread (short) | Date | Class | What it says |
|---|---|---|---|---|
| 1 | alternatives for agent workflows | 2026-11-16 | opinion naming an alternative product | "Manus is solid for one-off web browsing tasks, but for ongoing repetitive tasks you might want to look at Squad." |
| 2 | alternatives for agent workflows | 2026-11-16 | self-promotion with a referral link | offers the author's own application as a Manus-like tool |
| 3 | alternatives for agent workflows | 2026-11-16 | opinion naming alternative products | "Manus is nice as a demo but the moment you need to customise a step you hit a wall, so I would rather own the workflow." |
| 4 | alternatives for agent workflows | 2026-11-16 | opinion with an invite link | splits the choice into the workflow builder and the agent between steps; names context retention, browser access, tool permissions and recovery as the deciding axes |
| 5 | alternatives for agent workflows | 2026-11-16 | promotion with disclosure | "the browser piece is where a lot of the manus feel comes from, since much of that list happens on sites you're logged into"; the author states they build a competing product and that they are biased |
| 6 | alternatives for agent workflows | 2026-11-16 | opinion naming alternative products | a terminal-based coding agent with a few tool servers covers most of it; "less polished than manus, but you can see every step it took and rerun it, which is the part I'd miss from anything hosted" |
| 7 | alternatives for agent workflows | 2026-11-16 | opinion naming alternative products | the choice is between something that works out of the box and a platform where the user builds and controls the workflow; lists several workflow tools |
| 8 | a thread about a competing bot product | 2026-11-13 | self-report, no commercial link | a business running many agents in sync, and having used the product "a lot with success for certain tasks" |
| 9 | research tools whose reports can be updated | 2026-11-07 | promotion with disclosure | "The claim ledger + page snapshot replies are the right shape"; "perplexity or manus will do the first report fine, the hard part is week 3 and that's the part to test" |
| 10 | alternatives when the job must end in files | 2026-11-07 | promotion with disclosure | "the scriptable checks reply above is the real answer whatever tool u use. \"done\" should mean the count and link scripts passed, not that the agent got tired"; ends with "still open the files yourself" |

Two comments point the same way, and it is worth quoting them exactly because
they are the reason this case study exists. Comment 3 calls the product "nice
as a demo" but says that the moment a step needs customising "you hit a wall,
so I would rather own the workflow". Comment 6 prefers a terminal-based agent
because there "you can see every step it took and rerun it". A third comment
makes a different point and is kept separate: comment 1 separates one-off
browsing from ongoing repetitive work and recommends another product for the
second case. These are three opinions in one subreddit over ten days. They are
not a measurement, and they are not a claim about what a hosted product can or
cannot do — they are the stated reasons why three people preferred something
else.

The three most useful design ideas in the sample come from **two separate
comments that each carry a commercial disclosure**, and they are recorded here
as proposals from interested parties, not as community consensus:

- comment 9 proposes a **claim ledger plus a snapshot diff** — the diff says
  something changed, the ledger says which downstream artifact the change
  breaks — and adds that the first report is easy while "the hard part is week
  3 and that's the part to test";
- comment 10 argues for **scriptable completion checks** instead of the agent's
  own word: "done" should mean the count and link checks passed, not that the
  agent got tired, and it ends with the human rule "still open the files
  yourself".

Both are useful design patterns, and both are also the kind of advice a vendor
with a product to sell would give. A reader should hold both facts at once,
and should not attribute the two proposals to one author: the archive does not
establish that they share one.

The sample's limits are worth stating plainly: one subreddit, four threads over
ten days, four different questions, and only one comment with no commercial
link and no product recommendation. It cannot support statements about the
community as a whole, and older threads were not reachable through the archive
during this research.

### A public news aggregator

The largest thread about the product in the sample is about its acquisition,
not its mechanics: a thread with several hundred points and a couple of
hundred comments. What it shows is attention and scepticism in equal measure —
much of the discussion is about the wording of the announcement rather than the
product — and one comment asks whether the product is simply a well-known model
plus browser automation inside a virtual machine. That question is the same
question the vendor's own engineering post answers directly: the product is an
agent framework built on top of frontier models rather than a trained
end-to-end agent, and the interesting engineering is in context management.

An earlier thread on the product's economics contains the specialisation
argument in its sharpest form: a commenter says they do not want an agent that
can kind of do several unrelated things, because for each of those things they
would rather have a program that does that one thing very well. That is the
same trade-off the two-agent setup below makes deliberately: narrow agents with
a written contract, not one agent that does everything adequately.

### The application's own issue tracker

The application this repository documents is distributed as an open-source
Android client that talks to the user's own model providers, with local
conversation storage, agent tools, memory, skills, scheduled tasks and remote
shell access. Its public community is thin and concentrated in the issue
tracker; the discussions endpoint is not available on the repository, and no
separate forum was found.

Repository activity on the access date: 617 stars, 121 forks and 107 open
issues. These are activity indicators, not user counts. The user-authored
threads that were read describe six concrete situations:

| Thread | What the user reports or asks for |
|---|---|
| local workspace request | per-session workspaces for code and files on the device |
| local model report | several small local models tested on one device class, with a hang during inference |
| provider image generation | an image endpoint that returns a job identifier instead of image data, with a proposed endpoint-level fix |
| spawned agent tool scope | a diagnostic run of a spawned agent, with the concern that workers get too broad a toolset; the author labels it a single self-reported run |
| project organisation | folders and scoped conversation search for topic-based work |
| conditional monitoring | a scheduled check that should notify only when a condition is met |

The useful convention visible across those threads is a reporting style:
provider, model, version and device details, plus an expected-versus-actual
description. That makes a report reproducible, and it is the same discipline
this repository's own check scripts impose.

What the tracker does **not** contain is any evidence of a large community
practice, a shared skill library, a common memory scheme, or a population-level
reliability picture. A thin community is a finding, not a gap to be filled with
assumptions.

## 1.4 What the evidence supports, and what it does not

Supported, with the source named:

- The reference product is **documented** to offer persistent project
  workspaces, reusable skills, scheduled and event-triggered routines, parallel
  decomposition, local execution with permission modes and a bring-your-own-key
  mode. This is a statement about the product's documented feature set.
- Two comments prefer **ownership over polish**: comment 3 calls customisation
  a wall and says the writer would rather own the workflow, and comment 6
  prefers a terminal-based agent because every step is visible and rerunnable.
  A third comment, comment 1, makes a narrower point — one-off browsing suits
  the product, ongoing repetitive work may not — and recommends another
  product for that case. Three comments in one subreddit over ten days are an
  anecdote, not a consensus, and none of them is evidence about what a hosted
  product can do.
- Two comments with a disclosed commercial interest proposed, separately, a
  **claim ledger with snapshot diffs** and the third week as the real test
  (comment 9), and **script-based completion checks** with the rule to open the
  files yourself (comment 10). Recorded as proposals from interested parties,
  not as community agreement.
- One self-report with no commercial link describes **many agents running in
  sync** for a business and successful use of the product for certain tasks.
  One report.
- The application's own issue tracker shows a **reporting convention** —
  provider, model, version, device, expected versus actual — and a set of
  feature interests around local workspaces, local inference, worker tool scope
  and topic organisation.

Not supported by the collected evidence, and therefore not asserted anywhere in
this document:

- where the reference product is "strongest" or "weakest", or any comparison
  of its performance with another product — the only sources that characterise
  performance are the vendor's own material and one hands-on comparison whose
  author calls his own exploration limited;
- a reliability rate, a success rate, or a defect rate for any product;
- a community consensus on which mechanism matters most, or how many users run
  recurring routines;
- that a hosted product cannot offer an owned, visible, rerunnable workflow —
  that is one commenter's stated reason for preferring a terminal-based agent,
  not a demonstrated limitation;
- the adoption or size of any skill library, scheduled-routine population or
  third-party ecosystem;
- any head-to-head comparison between the reference product and the
  application this repository documents;
- the number of active users of either product;
- the current price a particular user would pay, which the vendor itself
  resolves at the live pricing page;
- any claim that the local setup is more reliable, cheaper or better than the
  reference product. It is a different shape of thing, and the comparison has
  not been measured.

## 1.5 The two-agent workflow in this setup

The local answer to the same question is not a copy of the product. It is a
**control plane with two agents and a repository**: a coordinating agent that
talks to the operator, plans, dispatches, verifies and reports, and a coding
agent that executes inside an explicitly bounded scope and proposes. The
operator talks to the coordinating agent only; the coding agent never asks the
operator a question and never reads silence as approval.

The generic contract below is the one in the skill `agora-goose-bridge`. The
canonical operating procedure — the full task cycle, the service topology, the
record matrix and the stop rules — lives in the project repository, and this
document summarises it rather than replacing it.

### Roles

| Concern | Coordinating agent | Coding agent | Operator |
|---|---|---|---|
| Talking to the operator | yes | never | decides |
| Choosing mode, impact tier and scope | yes | no | — |
| Writing the brief | yes | no | — |
| Editing files inside the dispatched scope | only when the brief says so | yes, inside the scope | — |
| Running the validation commands | verifies | runs and reports | — |
| Recording the outcome | yes | no | — |
| Approving commits, pushes, merges | asks | never | approves |
| Confirming high-impact work | confirms within its delegated authority | asks in the brief | may confirm directly |

The last row has a boundary worth stating: a coordinator confirmation covers
work the coordinator is delegated to authorise. Where a repository rule, a
licence condition or a deployment policy requires the operator's own explicit
approval — publication, releases and tags, deletions, licence or decision
status, budget, hosting — the coordinator's confirmation is not a substitute,
and the dispatch stops until that approval exists.

### Dispatch modes

| Mode | Write access | Purpose | Expected return |
|---|---|---|---|
| `execute` | bounded by the brief | perform an agreed change and prove it with tests | changed files, commands run, test result |
| `ideate` | read-only | propose options, tools and next increments | proposal with options and trade-offs |
| `review` | read-only | check an artifact against a stated checklist | findings against the stated checklist |

An `ideate` or `review` dispatch that modified files is a failed dispatch. It is
reported as such, the files are inspected, and the mode is restored.

### Impact tiers

| Tier | Typical work | Who authorises it |
|---|---|---|
| low | web research about the project, options analysis, documentation, tests, refactors without behaviour change, small isolated fixes | the coding agent proceeds inside the brief |
| medium | new features inside an existing module, behaviour changes without new dependencies, changes to the web UI or the live path | the coding agent proceeds; the coordinating agent confirms the brief and verifies the result |
| high | schema or contract changes, the evidence ledger or the checker, licence or ADR status, budget, hosting or publication, deletions, anything touching historical data | explicit confirmation by the coordinating agent or the operator before the dispatch starts |

A dispatch states its tier and the source of its authorisation in the brief and
in the returned report. A dispatch that crosses into a higher tier stops and is
re-briefed. A high-impact increment is split into low and medium parts so the
groundwork can proceed while the confirmation is pending.

### The brief and the report contract

The brief is a file, never inline text with credentials. The canonical
template is authoritative and carries the full field list; the summary below is
not exhaustive. A brief states: mode, impact tier, authorisation source,
working directory, model route, budget, output file, goal, scope with its
protected and out-of-scope parts, constraints, acceptance criteria, permitted
tools, output contract, forbidden actions, stop conditions, the permitted file
list, and the validation to run. A field that does not apply is written as "not
applicable" with a reason, never silently dropped.

The returned report is data, not fact. Every load-bearing claim is verified
against the artifacts — the working tree, the diff, the test output, the
checker output — before it is used. The operator-facing report has three named
parts and never merges the two voices:

1. `Dispatched` — mode, scope, model route, impact tier, authorisation source,
   artifact locations.
2. `Returned` — the coding agent's own words, quoted or summarised without
   silent editing.
3. `Assessment` — what the coordinating agent verified, what it doubts, and the
   decision the operator still owes. The coding agent never writes this part.

### The task cycle

1. **Intake and route.** Read the request, the repository entry points and only
   the records the task needs. Take a fresh snapshot of the repository state.
   A previous brief, adapter, test result or recorded approval is evidence, not
   fresh authorisation.
2. **Choose the mode and the impact tier.** If the scope could reach a higher
   tier, split the safe groundwork from the gated work.
3. **Write the brief** from the shared template, with every field filled.
4. **Dispatch once.** Check for a running matching session first; never start a
   second one for the same task. The turn limit bounds the tool iterations and
   therefore the token spend. A monetary ceiling applies only where the
   configuration that enforces it has been verified; the operator's standing
   budget is the outer bound, and a dispatch that would exceed it is stopped
   before it starts, not measured afterwards.
5. **Verify the return** against the artifacts, not against the report text.
6. **Record** in the same authorised change as the work: changelog, status,
   progress, decision records. Never record progress for a proposal.
7. **Report to the operator** in the three named blocks, and ask only when a
   real operator decision is missing or when a dispatch has produced the
   evidence that frames the question.

### A first dispatch, concretely

A first dispatch in a fresh repository looks like this:

- **Brief file** — copy the canonical template
  `skills/coordination/agora-goose-bridge/templates/task-brief.txt` to a task
  file in the dispatch workspace and fill every field. For a documentation
  question the scope is one directory, the protected files are the whole
  repository, the mode is `ideate`, the impact tier is low, and the acceptance
  criteria are written as checks a reader can perform.
- **Command** — run the coding agent in the repository directory with the
  brief file as its input and a bounded turn count. The invocation has the
  shape `goose run --with-builtin developer --no-session --max-turns <n> -i
  <brief file>`, run from the repository directory, with the model route and
  the provider endpoint supplied through the environment and the credential
  kept out of the command line.
- **Verification** — read the returned report, then check the claim against
  the artifact: does the file exist, does the diff contain what the report
  says, does the check script still pass.
- **Record** — a proposal produces no change records: the changelog, the
  status line and the progress list are written in the same change as the
  **executed** work, never after the fact, and never for a proposal that has
  not been carried out.
- **Report** — the three blocks, with the artifact paths.

### Records and the operator card

| What happened | Where it is recorded | When |
|---|---|---|
| any change to code, docs, tests or configuration | the changelog | in the same commit as the change |
| current scope, evidence and acceptance limits | the project status record | in the same change, when the state moved |
| implementation progress and the next increments | the progress list | in the same change |
| a durable decision | a decision record or an open-question entry | when the decision is made, not later |
| a dispatch and its outcome | the brief file, the report and the transcript | during the dispatch |

The project procedure adopted on 2026-11-17 ends every dispatch with a
one-page card in a fixed shape: verified, proposed, blocked, decisions needed,
next action, artifact locations. A run that produced no card produced no
handoff. The card and the session checklist belong to the project procedure;
this document names them so the two records do not drift apart.

### Where the shared skills live

| Location | Content | Used by |
|---|---|---|
| shared skills repository, `skills/<family>/<name>/SKILL.md` | canonical text | both |
| project repository, `.agents/skills/<name>/SKILL.md` | project-scoped copy | coding agent inside that repository |
| agent home, `~/.agents/skills/<name>/SKILL.md` | globally available copy | coding agent in every session |
| agent skill store (flat namespace) | deployed copy | coordinating agent |

The coding agent discovers skills in the project directory and in the agent home
without further configuration; the standard requires one directory per skill, a
`SKILL.md` file with frontmatter, and a directory name equal to the skill name.
A project-scoped copy is a copy. Canonical text changes first, then the copies
are refreshed, then a drift check compares each deployed copy with the
canonical file.

## 1.6 Mapping: reference mechanism to local equivalent

| Reference mechanism | Equivalent here | Gap | Increment | Impact |
|---|---|---|---|---|
| persistent project workspace with a master instruction and knowledge base | project repository entry points, the project context adapter, the shared skill set | no maintained specification of the working environment itself | a versioned design record for the environment | medium |
| decision memo and decision log | decision records and an open-question list in the project repository | no accepted record for the working-state path, retention and memory boundaries | same increment | medium |
| evidence store with a validator | the project's evidence ledger and its checker | no manifest links a decision to its evidence and status | freeze manifest | high |
| checklist and acceptance scenarios | repository validation scripts, the project session checklist | one behaviour pilot covers four checks; the wider cross-agent behaviour is untested | behaviour pilot — **done 2026-11-17**, see below | low |
| reusable skills | canonical skills and their deployed copies | no inventory of source, copy, owner and last check | skill inventory and drift check | low |
| operator summary | the three-part dispatch report and the project operator card | the card is in the project procedure, not yet in the shared contract | session checklist and card — **in the project procedure since 2026-11-17** | low |
| frozen evaluation package | a draft manifest with unfilled items | not frozen | freeze manifest | high |
| scheduled and triggered routines | scheduled tasks in the application, plus the dispatch cycle as a manual routine | no unattended trigger path for the two-agent seam | automation design | medium |

The increments are ordered so that the cheap, low-impact ones close first and
the high-impact ones wait for the operator's decisions.

The behaviour pilot is the one that is already closed, and it is the reason to
run one: a read-only dispatch carried three deliberately untrue statements and
one unfilled brief field, and asked the coding agent to check them. The observed
result was the point of the exercise — the agent refuted the stale claim with
repository commands, refused an approval that no record supported, reported an
unreadable file as unreadable instead of substituting another source, and named
the missing field. A seam that has not been tested is an assumption.

## 1.7 Where the local setup differs, and why that is not a defect

| Dimension | Reference product | Local setup | Consequence |
|---|---|---|---|
| Execution | hosted sandbox, with a desktop app that can run on the user's machine | the operator's own machine and repositories, with a local gateway to model providers | the repositories, the skills and the runtime live on the operator's machine; the prompts and the content still travel to the configured inference provider, so "local" describes where state and execution live, not where inference happens. The application can also run a model on the device, but the described setup does not use that path |
| Cost model | credits, refreshed daily or monthly, with the vendor billing the sandbox | the operator's own provider account and a local proxy, with spend ceilings on the live path where the configuration enforces them | spend is visible to the operator rather than governed by a plan, and the ceiling is a property of a configuration that has to be verified, not a property of the system |
| Structure | one agent with many modes | two agents with a written contract between them | every task has an owner, a scope, a tier and a verification step; the cost is one extra hop |
| Recurrence | scheduled and triggered routines inside the product | scheduled tasks in the application, plus a manual dispatch cycle | the two-agent seam has no unattended trigger path yet; that is a known gap, not a solved one |
| Verification | the agent's own report and the user's inspection of the files | the same, plus a repository checker and a required verification step before any claim | "done" is never the agent's word alone |
| Customisation | the product's own feature set | the repository, the skills and the local tooling are all editable | one commenter calls customisation a wall (comment 3). Editability is a deliberate local design choice, not a measured advantage over any product |

## 1.8 Guidance for power users

Derived from the evidence above and from the operating contract in Part 2. The
first four points come from the design ideas in the forum sample, including the
one proposed by an interested commenter; the rest follow from the local
contract.

1. **Own the workflow.** One commenter in the sample says that the moment a
   step needs customising they hit a wall, and that they would rather own the
   workflow. For this setup, keep the procedure in files you can edit.
2. **Make every step visible and rerunnable.** Another commenter prefers a
   terminal-based agent because there every step is visible and rerunnable.
   Where auditability matters, prefer a trace you can replay.
3. **Let the checks decide, not the agent.** Counts, links and checks are
   necessary evidence that a step did what it should. Passing checks is not
   acceptance: acceptance also needs the requester's judgement. The agent's
   confidence is not evidence at all.
4. **Keep a claim ledger.** One row per assertion, with its source, its
   passage, its date and its status. A validator checks the shape; a human
   checks the truth.
5. **Test the third week, not the first run.** The first report is the easy
   part; recurring work is where a setup proves itself.
6. **Open the files yourself.** The deliverable is the file, not the summary of
   the file.
7. **Split recurring work into a project-like context.** Shared instructions
   and shared files, inherited by every new task, beat re-explaining.
8. **Package a successful procedure once, reuse it everywhere.** A skill is a
   procedure with a file format, not a paragraph in a prompt.
9. **Give the browser the right session, and audit what it can do.** One
   interested commenter attributes much of the product's feel to the browser
   running inside the user's own logged-in accounts; if that holds, it is also
   where the risk lives. Treat it as a hypothesis to test, not a finding.
10. **Keep the human gate where it costs the most.** Schema, contracts, the
    evidence store, licences, budget, publication, deletions and historical
    data are operator decisions. Where a repository rule requires the
    operator's own approval, a coordinator confirmation does not replace it.
11. **Treat community threads as marketing surfaces.** Classify replies before
    counting them; a recommendation with a referral link or a disclosure is not
    a consensus.
12. **Write the session down.** Context that lives only in a chat window dies
    with the window. Records, not recall, are what makes an environment
    personal.

## 1.9 Open questions

- Can a follow-up with a larger, accessible forum sample establish how many
  independent users describe a recurring routine with the same shape as the
  one documented here?
- What is the actual failure distribution of a two-agent seam under repeated
  use, and which failure mode appears first?
- Which of the twelve guidance points above is load-bearing in practice, and
  which are folklore?
- Can the unattended trigger path for the seam be built without weakening the
  human gate?
- What does a mature skill library look like when it is maintained rather than
  collected, and how does drift get caught early?

## 1.10 Source registry

Every source was accessed on 2026-11-17. Quality is scored on authority,
recency, specificity and independence; an anecdotal user report stays weak
evidence even when it is independent, and a comment with a commercial interest
is not an independent user report at all.

| # | Source | URL | Date | Supports | Quality |
|---|---|---|---|---|---|
| S1 | Manus documentation index | https://manus.im/docs/llms.txt | accessed 2026-11-17 | the product's own feature map | 5/5/4/1 |
| S2 | Manus — welcome and execution model | https://manus.im/docs/introduction/welcome | accessed 2026-11-17 | sandbox, persistence, connectors | 5/5/4/1 |
| S3 | Manus — Projects | https://manus.im/docs/features/projects | accessed 2026-11-17 | master instruction, knowledge base, inheritance rules | 5/5/5/1 |
| S4 | Manus — Skills | https://manus.im/docs/features/skills | accessed 2026-11-17 | skill packages, progressive disclosure, acquisition paths, auditing | 5/5/5/1 |
| S5 | Manus — Automations | https://manus.im/docs/automations | accessed 2026-11-17 | schedule, triggered task, advanced automation | 5/5/5/1 |
| S6 | Manus — Parallel Tasks | https://manus.im/docs/features/parallel-tasks | accessed 2026-11-17 | decomposition, self-contained briefs, main-task control | 5/5/5/1 |
| S7 | Manus — Wide Research | https://manus.im/docs/features/wide-research | accessed 2026-11-17 | parallel per-item agents, context-window argument | 5/4/5/1 |
| S8 | Manus — desktop application | https://manus.im/docs/features/desktop | accessed 2026-11-17 | local execution, permission modes, workspace rules | 5/5/5/1 |
| S9 | Manus — running with your own key | https://manus.im/docs/models/manus-flex | accessed 2026-11-17 | provider choice, effort level, cost split, provider limits | 5/4/5/1 |
| S10 | Manus help centre — membership pricing | https://help.manus.im/en/articles/11711111-what-is-the-current-membership-pricing-for-manus | updated 2026-11 | plan structure, credits, concurrency, scheduled automations | 5/5/5/1 |
| S11 | Manus help centre — credit rules | https://help.manus.im/en/articles/11711097-what-are-the-rules-for-credits-consumption-and-how-can-i-obtain-them | updated 2026-11 | what consumes credits, refunds, expiry | 5/5/5/1 |
| S12 | Manus help centre — Wide Research | https://help.manus.im/en/articles/11960169-what-is-wide-research | updated 2026-09 | subtask cap, automatic triggering, paid-only | 5/4/4/1 |
| S13 | Manus help centre — sharing and using skills | https://help.manus.im/en/articles/14753565-how-to-share-and-use-skills-in-manus | updated 2026-10 | skill packaging and portability | 5/4/4/1 |
| S14 | Manus help centre — chat and agent modes | https://help.manus.im/en/articles/17768086-what-are-the-differences-between-chat-mode-and-agent-mode | updated 2026-10 | mode boundary, both modes consume credits | 5/5/4/1 |
| S15 | Manus engineering blog — context engineering | https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus | 2025-07-18 | action/observation loop, context growth, external memory | 5/3/5/1 |
| S16 | Hands-on comparison of two autonomous agents | https://www.alpsencer.com/blog/2025/manus-vs-devin/ | 2025-03, updated 2026-08 | observed task examples, mistakes found, the author's own limits | 3/3/4/5 |
| S17 | Public news aggregator thread on the product's acquisition | https://news.ycombinator.com/item?id=46426534 | 2025-12-29 | community attention, scepticism, the "model plus browser" question | 3/3/3/5 |
| S18 | Public news aggregator thread on the product's economics | https://news.ycombinator.com/item?id=43307713 | 2025-03 | the specialisation argument | 3/3/3/5 |
| S19 | Public agent forum thread — alternatives for building agent workflows | https://reddit.com/r/AI_Agents/comments/1xxbxr1/what_are_some_good_alternatives_to_manus_for/ | 2026-11-16 | comments 1–7 of the classification table in 1.3 | 2/5/3/4 |
| S20 | Public agent forum thread — research tools whose reports can be updated | https://reddit.com/r/AI_Agents/comments/1xq8yu5/what_ai_research_tool_actually_makes_it_easy_to/ | 2026-11-07 | comment 9 of the classification table | 2/5/3/3 |
| S21 | Public agent forum thread — alternatives when the job must end in files | https://reddit.com/r/AI_Agents/comments/1xofraq/whats_the_closest_manus_alternative_when_the_job/ | 2026-11-05 | comment 10 of the classification table | 2/5/3/3 |
| S22 | Public agent forum thread — a competing product | https://reddit.com/r/AI_Agents/comments/1xpurfh/how_good_are_the_new_grok_bots_really/ | 2026-11-07 | comment 8 of the classification table | 2/5/3/4 |
| S23 | Public archive of public forum posts | https://arctic-shift.photon-reddit.com/api/comments/search | accessed 2026-11-17 | the comment bodies behind S19–S22, read because direct requests to the forum platform were refused | 3/5/3/4 |
| S24 | Application repository and readme | https://github.com/newo-ether/Agora | accessed 2026-11-17 | product identity, feature set, distribution channels | 5/5/4/1 |
| S25 | Application release notes, latest observed release | https://github.com/newo-ether/Agora/releases/tag/v2.2.0 | 2026-10-31 | version, licence change, agent-related features | 5/5/4/1 |
| S26 | Application user manual | https://newo-ether.github.io/Agora/ | accessed 2026-11-17 | memory, skills, automation, shell and privacy behaviour | 5/5/4/1 |
| S27 | Application issue tracker — six user-authored threads | https://github.com/newo-ether/Agora/issues | 2026-08 to 2026-11 | local workspaces, local inference, provider compatibility, worker tool scope, project organisation, conditional monitoring | 3/5/3/4 |

Access notes, recorded because they affect how the evidence was obtained: the
forum platform refused direct requests during this research, so the forum
material was read through a public archive of public posts (S23); the archive
query returned 120 records that resolve to 10 distinct comment bodies across
4 threads, because its pagination repeated the same page set — the distinct
count is the one used in the text; five of the ten comments carry a referral
link, an invite link, a self-disclosure or an explicit commercial interest, and
four more recommend named products; every comment is marked with its class in
the classification table, and the findings drawn from it name the comments they
rest on; the
application's discussions endpoint was not available; the search engines
returned interstitials or unusable results for targeted queries.

---

# Part 2 — The operating contract

The shared workflow record between two agents that work on the same
repositories:

- the **coordinating agent** plans, dispatches, verifies and talks to the
  operator;
- the **coding agent** executes, proposes and reviews inside an explicitly
  bounded scope.

This part is the single place both sides read to learn the current agreement.
The generic dispatch contract lives in the skill `agora-goose-bridge`; the
project-specific operating procedure lives in the project repository. This
document records what was decided and when.

## Division of labour

| Concern | Coordinating agent | Coding agent |
|---|---|---|
| Talking to the operator | yes | no |
| Planning and dispatching | yes | no |
| Editing files inside a dispatched scope | only when the dispatch says so | yes, inside the scope |
| Proposing options and trade-offs | assesses them | writes them |
| Approvals, pushes, merges | asks the operator, never decides alone | never |
| Verification of returned work | yes | reports its own observations |

## Delegation policy

The coding agent is the default route for project work. The operator is asked
only after a dispatch, or for decisions that are genuinely the operator's. The
coordinating agent is the intermediary: the operator talks to it, and the coding
agent never asks the operator directly.

| Tier | Typical work | Who authorises it |
|---|---|---|
| low | web research about the project, options analysis, documentation, tests, refactors without behaviour change, small isolated fixes | the coding agent proceeds inside the brief |
| medium | new features inside an existing module, behaviour changes without new dependencies, changes to the web UI or the live path | the coding agent proceeds; the coordinating agent confirms the brief and verifies the result |
| high | schema or contract changes, the evidence ledger or the checker, licence or ADR status, budget, hosting or publication, deletions, anything touching historical data | explicit confirmation by the coordinating agent or the operator before the dispatch starts |

A dispatch states its tier and the source of its authorisation in the brief and
in the returned report. A dispatch that crosses into a higher tier stops and is
re-briefed. A high-impact increment may be split into low and medium parts so
the groundwork can proceed while the confirmation is pending.

## Dispatch modes

| Mode | Write access | Purpose |
|---|---|---|
| `execute` | bounded by the brief | perform an agreed change and prove it with tests |
| `ideate` | read-only | propose options, tools and next increments |
| `review` | read-only | check an artifact against a stated checklist |

An `ideate` or `review` dispatch that modified files is a failed dispatch. It is
reported as such, the files are inspected, and the mode is restored.

## Model routing and delegated subagents

The coding agent runs on a route chosen per dispatch. Which route is legal for which phase — and
which routes exist at all — is decided by the operator-approved role policy of the instance; this
document and the bridge Skill carry the procedure, not the route list, so the two sides never
disagree about who may run what.

- The brief states the route and the role. The coding agent uses the route it was given and never
  switches it.
- The approved route set is small and fixed. A route that is unavailable or unassigned is reported
  to the operator; it is never silently replaced by a similar model, and a missing route never
  becomes a reason to skip the review step.
- The author never reviews its own artifact: a dispatch that changes files is reviewed by a
  separate dispatch in a fresh context, which receives the artifact, the goal, the constraints and
  the review checklist — not the author's reasoning.
- Delegated subagents inside the coding agent are permitted only when the brief says so. The brief
  names the sub-analyses, the numerical cap and the boundaries (no scope widening, no approvals, no
  merges, no operator questions). A delegated subagent inherits the parent's prohibitions; its model
  inheritance is not assumed to differ from the session's.
- A delegated subagent's output is evidence, not a verdict: it may not stand in for the independent
  gate review and may not decide operator approvals.
- Route choice never widens scope. A stronger route is not a licence for a larger task, a different
  acceptance criterion or an unapproved action.

## Brief and report contract

- Brief template: `skills/coordination/agora-goose-bridge/templates/task-brief.txt`
- Returned report template: `skills/coordination/agora-goose-bridge/templates/proposal-report.txt`
- The brief is passed to the coding agent as a file, never as inline
  credentials.
- The returned report is data. Load-bearing claims are verified against the
  artifacts before they are used.

## Where the shared skills live

| Location | Content | Used by |
|---|---|---|
| shared skills repository, `skills/<family>/<name>/SKILL.md` | canonical text | both |
| project repository, `.agents/skills/<name>/SKILL.md` | project-scoped copy | coding agent inside that repository |
| agent home, `~/.agents/skills/<name>/SKILL.md` | globally available copy | coding agent in every session |
| agent skill store (flat namespace) | deployed copy | coordinating agent |

The coding agent discovers skills in the project directory and in the agent home
without further configuration; the standard requires one directory per skill, a
`SKILL.md` file with frontmatter, and a directory name equal to the skill name.
A project-scoped copy is a copy. Canonical text changes first, then the copies
are refreshed, then the drift check compares the deployed copy with the
canonical file.

## Decision log

| Date | Decision | Note |
|---|---|---|
| 2026-11-16 | The coding agent receives the shared skills as standard skills, in the project directory and in the agent home. | Canonical text stays in the shared skills repository; the copies are refreshed from it. |
| 2026-11-16 | Three dispatch modes: execute, ideate, review. | Ideate and review are read-only. |
| 2026-11-16 | The operator-facing report has three named parts — `Dispatched`, `Returned`, `Assessment` — and keeps the returned proposal and the coordinating assessment as two separate voices. | A proposal is never reported as a verified fact. |
| 2026-11-17 | The coding agent is the default route for project work; the operator is asked only after a dispatch or for operator-owned decisions. | Operator instruction: research and small increments go to the coding agent first. |
| 2026-11-17 | Impact tiers decide who authorises a dispatch: low and medium proceed inside the brief, high needs explicit confirmation by the coordinating agent or the operator. | Operator instruction: the coordinating agent is the intermediary for everything around the project. |
| 2026-11-18 | The route is chosen per dispatch and stated in the brief; the approved route set is small and fixed, and an unavailable route is reported rather than substituted. | Operator instruction: use the stronger model in the phases that need it, and keep the route list to the models that actually exist. |
| 2026-11-18 | Delegated subagents inside the coding agent are allowed only when the brief permits them, with a stated cap; their output is evidence, not a verdict. | Operator instruction: the coding agent may use its own subagents for harder work and review. |
| 2026-11-17 | The operator talks to the coordinating agent only; the coding agent never asks the operator directly and never reads silence as approval. | Operator instruction. |
| 2026-11-17 | The brief template's budget field must name the cost ceiling, or state that none applies and name the outer bound that does. | A behaviour pilot found the field under-specified in a real brief. |
| 2026-11-17 | This document becomes the case study of the two-agent working environment as well as the workflow record; the case study is Part 1, the contract is Part 2. | Operator instruction: study the reference product and the community, describe how the local workflow works and how the two correspond. |
| 2026-11-17 | Publish a generic operating-procedure base in `docs/35`; keep each project's topology, commands, paths, and approved deviations in its private adapter. The public base is adaptation guidance, not a duplicate of the Skill contract. | Operator chose the logically stable public/private split: reusable procedure is public, instance-specific overlay remains private. When the public base changes, compare each adapter with the new base and update it deliberately; do not silently assume local policy changed. This qualifies the earlier project-procedure placement decision. |

## Where the project-specific procedure lives

The shared skill keeps the generic dispatch contract: the brief and report
templates, the dispatch modes and the delegation policy with impact tiers. The
public generic operating-procedure base is
[`docs/35-two-agent-operating-procedure.md`](35-two-agent-operating-procedure.md).
Each project's topology, commands, paths, record locations and approved
deviations belong in its private adapter, not in the shared Skill or public
base. Neither side copies the other: contract changes are refreshed into
project copies; changes to the public base are checked against each adapter;
private project details remain in the project repository. The adapter's
revision and drift handling are defined locally, following the decision logged
above.

## Rules that always apply

- No credential, key or personal datum travels in a brief, a task file or a
  report.
- No push, merge, release or publication happens on a proposal alone; the
  operator approves each of them explicitly.
- Two agents never write to the same file in the same round.
- When the operator changes a decision mid-flight, the dispatch stops and is
  re-briefed.
- A returned report is never presented as a verified fact.
