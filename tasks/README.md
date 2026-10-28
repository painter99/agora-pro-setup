# Task Cards

Documented instances of the scheduled-task pattern from
[`docs/28-update-observability.md`](../docs/28-update-observability.md). Tasks
currently running in this setup: daily maintenance tasks, weekly loop tasks
(stack observability + research, self-improvement retrospective, repository
sync, skill mirror check), and a quarterly replication dry-run.

## What these files are — and are not

- Each card documents one live scheduled task: purpose, cadence, workflow
  shape, hard rules, delivery and notification budget, failure behavior.
- **Cards are not the original prompts.** The deployed prompts contain
  operator-specific details — local paths, personal criteria, notification
  topics, output language — that are intentionally genericized here into
  fill-in placeholders. The structure and the hard rules are faithful; the
  specifics are not.
- Task mechanics themselves (how tasks are scheduled, which tools a task agent
  receives) are an application feature and are not documented here; the
  upstream documentation owns that.
- Card names are generic and operator-neutral; live instances may carry
  operator-specific names.

## Card format

Every card uses the same sections: **Purpose, Schedule, Reads, Workflow, Hard
rules, Delivery and notifications, Failure behavior, Verification** — plus a
**Meta-review** section where the instance defines one.

## Maintenance

- Cards are repository content like any other: English, anonymized, generic,
  maintained by the weekly repository-sync task.
- A new task gets a card when it is created; a materially changed prompt gets a
  card update in the same weekly sync; a retired task's card is removed by a
  normal commit — git history remains the archive of variants.