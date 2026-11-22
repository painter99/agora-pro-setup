# Growth justification template

Every new Skill (`skills/**/SKILL.md`) and every new numbered doc
(`docs/<number>-*.md`) needs a justification file in `skills/justifications/`,
enforced by `scripts/check_growth.py`:

- New Skill: `skills/justifications/<skill-dir-name>.md`
- New doc: `skills/justifications/docs-justification-<number>.md`
  (the ambiguous `docs-<number>.md` form is rejected: it collides with the
  skill-justification namespace)

Copy the matching block below into the new file, keep every field label
exactly as written, and keep the value on the same line as the label. Values
may be prose or the explicit word `UNKNOWN` (empty fields fail the check).
One justification per Skill or doc; the checker enforces the 1:1 match and a
budget of at most one new Skill and one new doc per changeset. The checker
verifies presence, not truth: review assesses the content.

## Skill justification fields

```text
Problem: <what problem the new Skill solves>
Trigger / anti-trigger: <when to load it, and when not to>
Existing alternatives and overlap: <existing Skills or docs that nearly cover it, and the delta>
Evidence / usage: <observed need, or UNKNOWN>
Why a skill extension is insufficient: <why an existing Skill cannot simply gain a section>
Safety / dependencies: <permission, safety or dependency considerations>
Eval: <how correctness of the Skill is verified>
Owner: <role or team accountable for maintaining the Skill>
```

## New-doc justification fields

```text
Owner: <role or team accountable for the doc>
Overlap / alternatives: <existing docs that nearly cover it, and the delta>
Why an existing doc cannot hold it: <why no current numbered doc can host the content>
Links: <related docs and Skills this doc must stay consistent with>
Maintenance owner: <role or team that keeps the doc current>
Expected reader: <audience the doc is written for>
```
