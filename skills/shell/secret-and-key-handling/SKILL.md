---
name: secret-and-key-handling
description: "Secret and key handling for agents: secrets are generated and rotated only through scripts (CSPRNG, ssh-keygen), values are never displayed, outputs are limited to fingerprints; universal pattern for passwords, codes, tokens, and repository keys."
license: MIT
---

# Skill: secret-and-key-handling

## Catalog description
Secret and key handling for agents: secrets are generated and rotated only through scripts (CSPRNG, ssh-keygen), values are never displayed, outputs are limited to fingerprints; universal pattern for passwords, codes, tokens, and repository keys.

## Purpose
Keep secret values (passwords, codes, tokens, SSH keys) out of the agent's context window and out of chats and logs, while the agent still orchestrates them end to end: generation, rotation, application to targets, and delivery to the operator.

## Load when
- generating, rotating, or applying any password, code, key, or token;
- working with repository or deploy keys (GitHub and similar platforms);
- delivering credentials to the operator's devices through a file exchange;
- suspecting that a secret value leaked into a chat or log.

## Do not load when
- the work involves only public data (no secret in play);
- general infrastructure maintenance without touching secrets.

## Dependencies
- `tool-execution-contract` (verification and approval gates).
- `shell-and-device-operations` (device selection and shell execution discipline).

## Workflow
1. Classify the secret: a random password/code, a token, or an asymmetric key pair; identify its application target.
2. Generate or rotate only through installed scripts, never by writing the value out by hand — model text is not cryptographic entropy. Random material comes from the operating system CSPRNG (`/dev/urandom`); keys come from `ssh-keygen` (Ed25519).
3. Store the secret on a privileged path (root-owned, mode 600) that the agent's user cannot read, whenever the agent does not itself need the key for its tooling. Keys the agent actively uses (git, ssh) stay readable by those tools and are used, never displayed.
4. Apply the secret through a dedicated applier script that pushes the value into all its targets (live service, persistent configuration, operator delivery copy) and prints only fingerprints. Example shape: a console credential for a virtual machine is written to the running instance, the persistent domain configuration, and the delivery copy in one script run.
5. Deliver to the operator's phone through the exchange outbox with exactly one current version; superseded files are removed at rotation time.
6. Verify with fingerprints only (file hash prefixes, `ssh-keygen -lf`); the generator, verifier, and applier outputs must agree.
7. Report the operation: path, old and new fingerprint, where it was applied, how it was delivered — without ever printing the value.

Deploy and repository keys:
- one dedicated key per repository or service, Ed25519, comment convention `purpose-repo-date`;
- the private key is used only through tools that need it (git, ssh) and is never read, printed, or copied through chat;
- the public key is printable by definition and belongs on the platform (for example a GitHub deploy key) — the operator registers it;
- rotation means a new pair via script, the operator registering the new public key, and the old key being revoked on the platform;
- passphrase-less automation keys trade the passphrase for file permissions (mode 600, root-owned where possible); for higher-value repositories consider a passphrase plus an ssh-agent.

## Forbidden behavior
- Never generate a secret value by writing it out directly (no model-invented passwords, keys, or tokens).
- Never print, cat, echo, base64-encode, or otherwise display a secret value or a private key in chat, logs, or tool output.
- Never store secrets in a public repository, not even obfuscated.
- Never reuse one key across repositories or services.
- Never commit a script that contains a secret value; scripts carry logic, not material.
- Never treat a leaked value as tolerable — a confirmed leak into a chat or log means immediate rotation via the script plus an honest report.

## Verification
- Fingerprints from the generator, verifier, and applier match (for example, the persistent configuration equals the credential file).
- Delivery is confirmed by the exchange watcher (event and push), and exactly one current version exists in the outbox.
- The value itself never appeared in any tool output in the conversation.

## Output contract
Report: what was generated or rotated (path, old and new fingerprint), where it was applied, how it was delivered, and an explicit statement that no secret value appeared in any output.

## Limits
- This pattern is best-effort defense, not an absolute wall: an agent with unrestricted sudo can technically read privileged files; full separation requires narrowing sudoers to an allowlist (operator decision).
- A secret may be briefly visible in the process table during an applier call (root context) — negligible on a single-user host.
- The agent maintains the script code; scripts must never contain secret values.

## Related docs
- `docs/8-tools-and-safety.md` (safety layer around tool calls)
- `docs/30-instance-overlay.md` (instance-specific paths and names stay out of this repository)

## Sources
AWS Secrets Manager, "Use secrets safely with AI Coding Agents" (the agent orchestrates secret usage without seeing plaintext; "best-effort defense, not a security boundary"), 2026. Auth0, "Want AI Agents That Don't Spill Secrets? Don't Give Them Secrets", 2026. GitHub Docs, "Managing deploy keys" (per-repository Ed25519 keys, fingerprints), 2026. Operator rule carved 2026-11-03 after enabling console access to a virtual machine.