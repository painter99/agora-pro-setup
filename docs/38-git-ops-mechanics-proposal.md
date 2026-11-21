# Controlled Git Operations for Coding Agents

> **Status: PROPOSAL / DRAFT — not adopted, not implemented, and grants no authority.**
> All implementation, credential, account, repository-setting, commit, push, and merge changes require their own authorization. Design claims marked **UNVERIFIED** require testing before reliance.

## 1. Problem statement

A coding agent may hold working credentials that allow it to push changes. If the agent also has unrestricted `sudo` on the same host, process wrappers, hidden credentials, filesystem permissions, and local audit files are not security boundaries: the agent may be able to bypass them or obtain equivalent host access. This must be stated plainly.

The goal is to separate change preparation from authoritative Git operations. A controlled path should limit what can be committed or published, bind each operation to an exact reviewed snapshot and authorization, and leave evidence for a separate controller to verify. It cannot make an untrusted host administrator harmless or prove that a change is correct.

**Current-state note: UNVERIFIED.** This proposal does not assert any repository's present permissions, credential exposure, host isolation, branch rules, or service availability.

## 2. Threat model: controls and limits

- **Compromised or mistaken coding agent:** broker allowlists, immutable snapshots, per-operation authorization, and server-side branch rules can restrict official remote mutations. They do not prevent local edits or commits in an agent-writable copy.
- **Unrestricted host administrator or shared privileged account:** a wrapper, local token file, lock, or log can be bypassed by an actor with equivalent privileges. Isolation is required for a security boundary; its effectiveness must be tested.
- **Forged, stale, replayed, or overbroad request:** signed, short-lived, one-time grants bound to exact operation data reduce these risks. They do not replace authorization or prevent abuse by a compromised trusted signer.
- **Concurrent changes and time-of-check/time-of-use races:** immutable snapshots, expected object IDs, atomic token consumption, and server-side compare-and-swap (CAS) checks reduce races. Local locks alone cannot stop external actors.
- **Malicious repository content or tests:** parse inputs as data, constrain configuration and environment, and never run untrusted hooks or tests with broker privileges. A model review or scanner cannot guarantee detection of every malicious change or secret.
- **Privileged platform or account bypass:** branch rules add an independent layer only if they cover all relevant identities and have no unintended bypass. They do not prevent local changes, publication elsewhere, data disclosure, or authorized administrator bypass.
- **Audit tampering:** hash chaining and externally anchored checkpoints make alteration more detectable, not impossible. A privileged operator may still defeat controls without an independently protected anchor.

## 3. Recommended architecture

### Roles and separation

1. The coding agent prepares a change in an isolated workspace and submits a typed request; it has no usable credentials for official remote refs.
2. A controller observes, verifies, authorizes within an explicit grant, and can stop new requests. It does not invent the owner's approval.
3. A fresh-context pre-operation gate examines the exact operation package and returns a strict `PASS` or `FAIL` result.
4. A separate qualified reviewer performs any review required by the project's role policy. Gate `PASS` is an additional check, not qualified review and not permission to act.
5. An isolated broker, running under a minimally privileged identity, alone performs final authorized Git operations and records their outcomes.

### Isolation and broker boundary

The agent runtime must not have host-root access, broker credentials, broker sockets or writable approval/audit stores, inherited signing material, alternate write credentials, or network access to Git hosting except where explicitly necessary. The broker uses a separate trust boundary and repository/object store. These are design requirements, not claims about an existing deployment; escape paths and alternate credentials must be tested.

If genuine isolation is absent, operate in **advisory mode**: generate manifests and review results without remote mutation. Keep automatic remote operations disabled until isolation is demonstrated. A local wrapper on a shared privileged host is process discipline, not enforcement.

### Per-operation gate

Start a new, non-restored gate context for each `commit`, `push`, or `merge`. Supply only the versioned manifest, approved brief and scope, complete relevant change and object IDs, protected-path rules, and evidence of deterministic checks. Exclude credentials and author reasoning. Treat repository text and prompts as untrusted data. Missing, truncated, oversized, stale, or incomplete evidence means `FAIL`/stop.

The gate reports schema version, operation ID, manifest digest, snapshot IDs, scope, coverage, checks, evidence, blockers, context identity, and time. Any timeout, invalid schema, unclear coverage, route failure, or snapshot change is `FAIL`. A model verdict does not prove absence of defects or secrets.

- **Commit:** inspect the exact staged tree, parent, file set and metadata, message, and authorized identity.
- **Push:** inspect the full commit range and objects against the expected remote ref and old object ID; disallow force and history rewrite. Define explicit behavior for missing or unexpected remote refs.
- **Merge:** inspect the exact pull request, source head, target base, merge base, resulting tree, merge method, checks, and conflicts. Re-run review if either head or base changes. If the platform cannot enforce the required head/base conditions atomically, do not automate merge.

The gate is not a replacement for mandatory independent, qualified review. It is also not authorization: a valid owner-approved grant is separately required for each operation unless a narrowly bounded delegation is explicitly approved.

### One-time signed authorization

A trusted authorization service—not the gate model—validates the owner's approval, required qualified review, gate result, deterministic checks, and immutable snapshot before issuing a short-lived signed grant. Bind it to repository identifier, operation and nonce, exact target, expected old and new object IDs, manifest and brief digests, required evidence, method, actor, issue time, and expiry. Do not put credentials in the grant.

The broker verifies the signature and live state, atomically reserves and consumes the grant before mutation, and rejects replay, expiry, revocation, scope mismatch, changed refs, or missing evidence. An uncertain outcome never permits token reuse: stop and reconcile first. A grant cannot protect against compromise of its signer or broker host.

### Controller and audit

The controller verifies scope and authorization, watches gate and broker states, checks the resulting remote state independently, and stops new work on uncertainty. A stopped agent job may not stop an in-flight broker request or remote transaction; query and reconcile those separately.

Maintain an append-only event record for request, denial, intent, result, and reconciliation. Include event and operation IDs; actor; repository and target; before/expected/after object IDs; manifest, brief, review, grant and runner-evidence digests; outcome and exit status; UTC time; sequence; and previous/current event hashes. Never record bearer tokens or unintended private diffs. Persist and sync `intent` before mutation and `result` after. Anchor periodic signed checkpoints in a separate administrative domain. Hash chaining alone cannot prevent privileged deletion or rewriting of the entire log.

## 4. Advisory-first operating policy

Begin with advisory-only manifests, gate outputs, and audit events on synthetic or isolated test data. Do not enable automatic remote operations until isolation, authorization, replay prevention, audit durability, and platform controls pass documented negative and positive tests. A failure, missing evidence, audit error, timeout, or unknown in-flight state closes the broker to new mutations.

Every commit, push, and merge is a distinct operation with its own snapshot and authorization. A request for a sequence of operations is not authority for all steps unless an explicit grant names them. A successful push or merge may not be safely reversible; never imply rollback is guaranteed.

## 5. Repository-owner checklist (Git hosting)

- [ ] Inventory every write/admin identity, application, deploy credential, and bypass path; identify the broker identity and revocation owner.
- [ ] Protect the primary branch with pull-request-only changes and required checks tied to trusted sources and the exact commit.
- [ ] Require current source/target revisions and rerun checks after changes; require qualified or human review where supported and appropriate.
- [ ] Prohibit force pushes and branch deletion; apply protections to administrators where possible and minimize or disable bypass.
- [ ] Review protected tags and other important branches separately; choose merge methods based on actual project requirements.
- [ ] Verify plan/tier support, application permissions, and rules for every relevant identity. These platform details are **UNVERIFIED** until checked on the actual account.
- [ ] Test on a disposable branch or repository: direct and force push denial, missing/stale checks, stale head/base, bypass behavior, and successful approved pull-request merge.
- [ ] Keep gate `PASS` separate from hosting-platform reviewer approval; a model verdict is not a platform review.

## 6. Reversible migration sequence

1. **Document current state, no changes.** Inventory identities, credentials without reading secret values, sudo, network paths, repository rules, and active work. Record unknowns. Revert by simply retaining the existing process; do not claim it is fenced.
2. **Build an isolated test broker without production credentials.** Test forged grants, replay, scope escape, changed refs, configuration injection, symlinks, concurrency, audit failure, and interruption. Disable or remove the test service to return to the prior state.
3. **Prove isolation and advisory mode.** Demonstrate the agent cannot reach broker secrets, host privilege, official refs, or alternate remote-write routes. If any test fails, remain advisory-only; turn off the test deployment to revert.
4. **Separately authorize repository protection and broker identity changes.** Apply rules and provision/revoke credentials only under explicit approval and a documented rollback plan. Do not restore agent write access as a silent fallback. Until old access is revoked and tested, report that fencing is incomplete.
5. **Run shadow operation reviews.** Exercise synthetic commit, push, and merge packages without mutation; verify fresh gate contexts, required qualified reviews, digests, one-time consumption, and durable audit.
6. **Pilot only after independent qualified review and exact approval.** Use one isolated commit, then separately authorized topic-branch push, then separately authorized pull-request merge. Verify each result and stop before the next. Remote publication is not fully reversible.
7. **Adopt gradually.** Expand only after evidence is reviewed. Keep advisory fallback available; any rollback that changes credentials or branch protections requires fresh approval and must not re-enable an unsafe route by default.

## 7. Proposed follow-on artifacts

- Skill outline: `goose-git-ops` request workflow, boundaries, manifest fields, stop/reconcile behavior, and misuse tests.
- Wrapper/broker interface specification: typed `request`, `inspect`, and `cancel`; trusted internal `execute`; no generic shell or arbitrary Git arguments.
- Reviewer checklist template: snapshot identity, operation scope, completeness, protected paths, evidence, risks, blockers, and strict `PASS`/`FAIL`.
- Ledger schema: versioned request/decision/intent/result/reconciliation events with hashes, sequence, and external checkpoint references.
- Implementation, deployment, repository changes, and policy changes remain separate proposals requiring review and explicit authorization.

**Status: DRAFT, unreviewed, and unimplemented.** Validate every platform capability and isolation assumption before treating this proposal as operational guidance.
