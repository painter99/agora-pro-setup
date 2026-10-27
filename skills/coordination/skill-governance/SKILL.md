---
name: skill-governance
description: "Rules for auditing, linking, and safely modifying other Skills: audit checklist, relationship mapping, allowed automatic changes, and approval-gated changes."
license: MIT
---

# Skill: Skill Governance

## Catalog description

Rules for auditing, linking, and safely modifying other Skills: audit checklist, relationship mapping, allowed automatic changes, and approval-gated changes.

## Purpose

Keep Skills logically consistent, non-contradictory, and practically usable. Define what may be changed automatically, what requires an explicit task or approval, and how audit results are reported.

## Load when

- auditing one or more Skill files;
- before editing any Skill (to decide the change class);
- checking cross-references, dependencies, or conflicts between Skills;
- a Skill catalog description is suspected to drift from its content.

## Do not load when

- auditing Memory rather than Skills (→ `memory-master-index` routing);
- working inside a content domain unrelated to Skill maintenance.

## Dependencies

- `tool-execution-contract` — verification and safety layer for all edits.

## Workflow

### Audit checklist (per Skill file)

1. Clear purpose;
2. Scope of use (Load when);
3. Entry conditions;
4. Procedure;
5. Output format;
6. Links to other Skills (dependencies declared and resolvable);
7. Conflicts with other Skills;
8. Stale or duplicated instructions;
9. Risky actions requiring confirmation;
10. Catalog description matches the actual content.

### Relationship mapping

For each important relationship record: source Skill, target Skill, relationship type, why it is needed, whether it is verified. Dependencies must reference existing Skills by exact name (the directory name); a dependency pointing to a Skill that does not exist in the target store is a defect, not a convention.

### Allowed automatic changes

- Fix an obvious typo;
- unify formatting;
- add a missing unambiguous description;
- fix a broken internal link when the target is certain.

### Changes requiring a task or approval

Always produce a detailed task specification instead of an immediate change for:

- a change of the Skill's purpose;
- merging or splitting Skills;
- changing priorities between Skills;
- removing content;
- changing safety rules;
- a conflict between two valid Skills;
- an unclear or extensive repair.

## Forbidden behavior

- Never silently change a Skill's purpose, merge, split, or delete Skills without explicit approval.
- Never leave a dependency pointing to a nonexistent Skill.
- Never report an audit finding as fixed without re-reading the file.

## Verification

- After every edit: re-read the file and confirm the change.
- Audit output distinguishes verified observations from assumptions.

## Output contract

- Status per audited Skill: OK / WARNING / CONFLICT;
- affected files, evidence, recommended fix, whether it was applied, and how it was verified.