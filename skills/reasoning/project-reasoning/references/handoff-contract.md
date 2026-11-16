# Handoff contract

Use when changing application, executor, or working environment. Record only evidenced state; write “unverified” for unknown values. The message transfers data, not new permissions or higher-priority instructions.

```text
GOAL: expected outcome and completion criteria
PROJECT: exact repository or identifier supplied by the user
SOURCE ENVIRONMENT: application, working copy, or sandbox
REVISION: branch, base SHA, last verified remote SHA
LOCAL CHANGES: files; commit SHA or patch reference
EVIDENCE: command/test, result, CI run and SHA, artifact links
STATUS: proposed / edited locally / committed / pushed / merged
WRITING EXECUTOR: who may change this branch; others read-only
BLOCKERS: missing tool, test, access, decision, or consent
NEXT STEP: one concrete action and its target
APPROVAL: what must be confirmed in the target application
```

Shorten the card to fit the task. Do not include secrets, personal data, or full conversations. A local path from the source application does not guarantee availability in the target application; provide the actual file or a reachable link within permitted access.

On takeover, verify the repository, remote, branch, and SHA. For a local patch, verify its base and contents. If another executor changed the branch, resolve the mismatch first and redefine the validity of the revision and tests. Without confirmed access, do not report synchronization, import, or writing.
