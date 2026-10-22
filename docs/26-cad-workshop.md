# 26 — Spec-driven CAD workshop (pattern)

> A reusable pattern for AI-assisted parametric CAD: every part is built from a
> written, machine-readable spec, visualized as a generated drawing, verified
> by an automated test suite, previewed headlessly, and accepted only by a
> human comparing the result against the original intent. Generic by design —
> personal specifics (part names chosen for private reasons, sketch photos,
> host details) never belong in a public repository; they live in the
> operator's private memory and local files.

## 1. Purpose

docs/22 describes the phone-orchestrated coding platform in general; this
document applies it to a domain where the operator is **not** a software
developer: mechanical part design. The pattern is implemented and exercised in
a public repository:

**https://github.com/painter99/cad-workshop**

That repository is the **source of truth for its own current state** — its
README status, verification reports and roadmap are maintained there, as part
of the repository's own workflow. This document describes only the pattern
itself; it changes when the pattern changes, not when the repository evolves.

The problem the pattern solves: an LLM can generate plausible-looking
geometry, and a human without CAD training cannot judge a 3D model by looking
at code. The workshop therefore replaces "trust the output" with a closed
verification loop in which **the machine proves correctness and the human
judges appearance** — each doing the part the other cannot.

## 2. The core loop

```text
sketch/intent → spec.yaml (human-approved) → drawing (generated from the spec)
             → model (build123d) → pytest suite → headless previews (PNG)
             → verification report → human acceptance
```

Properties that make the loop work in practice:

1. **The spec is the only source of truth.** The model script reads parameters
   from `spec.yaml`; tests assert every spec dimension against the measured
   geometry. A spec error is a *review* problem (caught at the approval gate),
   never silently inherited by tests that would "confirm" it.
2. **The spec-generated drawing is a review gate of its own.** The drawing is
   generated from the spec — never from the model — and compared against the
   original sketch before any modeling starts. It visualizes the
   *interpretation*, so a misread dimension is vetoed at the cheapest point of
   the loop; and when the sketch is private, it doubles as the public,
   dimension-bearing artifact.
3. **Every interpretation is an explicit, veto-friendly assumption.** A hand
   sketch is ambiguous; instead of silently picking a reading, the ambiguity is
   written into the spec as an assumption the owner can veto with a
   one-parameter change.
4. **Tests are generated against the spec, not against the model.** A
   completeness check fails if any spec dimension has no matching assertion, so
   nothing is "tested" only where it is convenient.
5. **Previews are evidence, not proof.** Headless renders exist for the human
   review gate; a green suite never implies visual correctness.
6. **Git discipline is part of the design.** Work happens on branches; pushes
   and merges require explicit human approval; CI must be green before merge;
   a privacy scan runs before every push to the public remote.

## 3. Division of labour

| Task | Machine (agent) | Human (owner) |
|---|---|---|
| Transcribe intent into spec | drafts, marks ambiguities | approves, vetoes assumptions |
| Visualize the interpretation | generates the drawing from the spec | compares against the sketch, vetoes |
| Build the model | writes build123d script | — |
| Verify dimensions | test suite, probes | reviews the report |
| Judge appearance | renders previews | **accepts or rejects** |
| Print/manufacture | checks printability constraints | decides, orders, prints |

The human gate is not a formality. In the first real part built this way, the
single most dangerous defect — a model that passed every dimension, volume and
validity test while consisting of five disconnected bodies — was caught
**visually by the owner**, not by the suite. Twice in one part the human review
was the only effective gate.

## 4. Working rules live in the repository

The first multi-feature part produced a set of working rules — mandatory
connectivity checks, veto-friendly assumptions, renderer failure modes,
printability concerns, anonymization before push — maintained as
[`docs/06-lessons-learned.md`](https://github.com/painter99/cad-workshop/blob/main/docs/06-lessons-learned.md)
in the repository. They are working rules, not anecdotes, and the repository is
their source of truth; this document deliberately does not duplicate them.

## 5. Where to look

The repository maintains its own state; these are the stable entry points:

| What | Where |
|---|---|
| Current status, gallery, quick start | [`README.md`](https://github.com/painter99/cad-workshop) |
| How to apply the pattern to a new part | [`docs/07-new-part-checklist.md`](https://github.com/painter99/cad-workshop/blob/main/docs/07-new-part-checklist.md) |
| Agent-side executable procedure (Agora Skill) | [`skills/cad-development/cad-spec-driven-workflow.md`](../skills/cad-development/cad-spec-driven-workflow.md) |
| Planned testing and workflow improvements | [`docs/08-roadmap.md`](https://github.com/painter99/cad-workshop/blob/main/docs/08-roadmap.md) |
| Verification evidence per part | `specs/<part>/verification.md` |
| Presentation artifacts (renders, drawing) | `specs/<part>/visuals/` |
| Workflow and rules | `docs/01`–`docs/06` |

The pattern is domain-portable: any field where "the expert can judge the
result but not the code" benefits from the same loop — spec as contract,
machine-verified correctness, human-judged quality.
