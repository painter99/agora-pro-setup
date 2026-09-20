# Memory Governance Gate

Architectural remediation for a real failure mode: the System template became a
**benevolent router** and the model stopped following the memory-management
framework, because the framework lives only in Skills and the Skill Catalog is
discovery, not execution.

## Version analysis (what the repository history shows)

| Version | Commits | Memory enforcement | Outcome |
|---|---|---|---|
| v1 — monolithic framework | `f23fbf7` (2026-07-27), `f1991eb` (07-30) | "Block 7 memory hint": governance reference + write policy inside the System tab | Worked, but the kernel carried framework detail |
| v2 — split + HARD GATE | `6bf57f9` (08-02), `d31ca3e`, `7e3f1dc` (08-30), `594f6b4` (09-04) | Kernel-level **HARD GATE**: before any memory tool call, first `read_memory_file` on the master index; end-of-task attestation line | Enforcement was reliable; kernel text grew long |
| v3 — compact router | `ba62243` (09-05), `896a28c` → reverted by `9721786` (09-06), `ef43753`, `7da5d42` (09-06) | Gate removed from the kernel; memory rules relocated into `skills/memory-governance/`; kernel says only "use memory tools when appropriate" | Compact and clean, but **the gate no longer fires**: nothing forces the model to load the framework before writing |

The v3 refactor was right about *placement* (procedures belong in Skills) and
wrong about *enforcement* (a rule that must always apply cannot live only behind
an optional catalog lookup).

## Root cause

1. **Discovery ≠ execution.** `{skill_catalog}` shows names and descriptions. A
   Skill body only influences behavior if the model chooses to read it.
2. **Benevolent phrasing.** "Use memory tools for persistent information when
   appropriate" grants discretion at exactly the point where discretion causes
   drift (wrong layer, duplicate facts, silent AM replacement, unindexed files).
3. **No post-write verification requirement in the kernel.** The invariants exist
   in `docs/13` and in the governance Skills, but nothing in the always-injected
   layer requires them.
4. **No attestation.** Without a required end-of-task line, a skipped gate is
   invisible to the user.

## Remediation: kernel-owned gate, Skill-owned procedure

Split the concern by layer instead of choosing one:

| Layer | Owns | Why |
|---|---|---|
| System template (kernel) | **the trigger and the obligation**: which tool calls are gated, that the routing Skill must be read first, that writes must be verified, that the gate must be attested | always injected; cannot be skipped |
| `memory-master-index.md` | **the decision guide**: which layer, which specialized Skill | procedure detail, loaded on demand |
| `active-memory-design.md`, `active-memory-authority.md`, `memory-file-operations.md`, `memory-audits.md` | **the specialized procedures** | progressive disclosure |
| `tool-execution-contract.md` | inspection, approval, retry, verification | shared safety floor |
| `docs/17-permission-model.md` | memory writes = **Modify** class, band B/C | normative approval bands |
| `docs/19-memory-tool-reference.md` | tool names/arguments (reference, not a Skill) | static facts out of the catalog |

This is defense in depth: the kernel guarantees the gate fires; the Skills keep
the kernel small; the docs keep the rules auditable.

## The gate (normative text)

The kernel carries a compact version — roughly 100 words, not the v2 wall of
text:

```text
Memory writes are gated. Before any create_memory_file, edit_memory_file,
delete_memory_file, or update_active_memory call, read memory-master-index.md
and the governance Skill it routes to (Active Memory: active-memory-design.md +
active-memory-authority.md; Saved Memory: memory-file-operations.md). Choose the
layer first: durable fact -> Saved Memory, reusable procedure -> Skill, current
status -> Active Memory, transient -> no write. Prefer a unique patch over
replacement; deletion and full replacement require explicit approval for the
exact scope. After the write, re-read the result and check dependent references,
including the Active Memory Archive Index. If memory tools are unavailable, say
so instead of simulating a write. When this gate applied, end the task with one
line stating that it was loaded and followed.
```

Design constraints honored:

- **Compact:** one paragraph; the decision detail stays in Skills.
- **Capability-gated** (`docs/15`): degrades to an honest statement when memory
  tools are disabled, never a simulated write.
- **Permission-consistent** (`docs/17`): Modify class, band B for ordinary
  patches, band C for deletion/full replacement.
- **Observable:** the attestation line makes a skipped gate visible to the user.
- **Index-coupled:** every new Saved Memory file must be reachable from the
  Active Memory Archive Index, otherwise it is invisible to future sessions.

## What was deliberately NOT restored

- The v2 "internal knowledge is UNRELIABLE" wall and the nine-rule reasoning
  framework: superseded by `skills/reasoning/sequential-thinking-workflow.md` and
  `docs/6`.
- The deep-research HARD GATE: `multi-source-research.md` plus the kernel's
  research-routing sentence are sufficient; research is not a write operation and
  carries no drift risk.
- Block/widget assembly instructions: Agora 2.1 uses System/User/Assistant
  templates (`docs/3`), not the old tab-block layout.

## Verification

After changing the System template, confirm by behavior, not by reading:

1. Ask for a durable fact to be remembered; check that the response shows a
   `read_memory_file`/`read_skill_file` call on the router **before** the write.
2. Check the attestation line is present.
3. Check the write landed in the correct layer and that the Archive Index was
   updated.
4. Ask a transient question; confirm **no** memory write happens (the gate must
   not create write pressure).

## Related docs

`docs/0-overview.md`, `docs/3-system-user-assistant-templates.md`,
`docs/4-active-memory.md`, `docs/13-memory-governance.md`,
`docs/15-capability-gating.md`, `docs/17-permission-model.md`,
`docs/19-memory-tool-reference.md`.
