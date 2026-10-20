# 26 — Spec-driven CAD workshop (applied pattern)

> A reusable pattern for AI-assisted parametric CAD: every part is built from a
> written, machine-readable spec, verified by an automated test suite, previewed
> headlessly, and accepted only by a human comparing the preview against the
> original intent. Generic by design — personal specifics (part names chosen for
> private reasons, sketch photos, host details) never belong in a public
> repository; they live in the operator's private memory and local files.

## 1. Purpose

docs/22 describes the phone-orchestrated coding platform in general; this
document applies it to a domain where the operator is **not** a software
developer: mechanical part design. The working repository is public and can be
studied as a live example:

**https://github.com/painter99/cad-workshop**

The problem it solves: an LLM can generate plausible-looking geometry, and a
human without CAD training cannot judge a 3D model by looking at code. The
workshop therefore replaces "trust the output" with a closed verification loop
in which **the machine proves correctness and the human judges appearance** —
each doing the part the other cannot.

## 2. The core loop

```text
sketch/intent → spec.yaml (human-approved) → model (build123d) → pytest suite
             → headless previews (PNG) → verification report → human acceptance
```

Properties that make the loop work in practice:

1. **The spec is the only source of truth.** The model script reads parameters
   from `spec.yaml`; tests assert every spec dimension against the measured
   geometry. A spec error is a *review* problem (caught at the approval gate),
   never silently inherited by tests that would "confirm" it.
2. **Every interpretation is an explicit, veto-friendly assumption.** A hand
   sketch is ambiguous; instead of silently picking a reading, the ambiguity is
   written into the spec as an assumption the owner can veto with a
   one-parameter change.
3. **Tests are generated against the spec, not against the model.** A
   completeness check fails if any spec dimension has no matching assertion, so
   nothing is "tested" only where it is convenient.
4. **Previews are evidence, not proof.** Headless renders exist for the human
   review gate; a green suite never implies visual correctness.
5. **Git discipline is part of the design.** Work happens on branches; pushes
   and merges require explicit human approval; CI must be green before merge;
   a privacy scan runs before every push to the public remote.

## 3. Division of labour

| Task | Machine (agent) | Human (owner) |
|---|---|---|
| Transcribe intent into spec | drafts, marks ambiguities | approves, vetoes assumptions |
| Build the model | writes build123d script | — |
| Verify dimensions | test suite, probes | reviews the report |
| Judge appearance | renders previews | **accepts or rejects** |
| Print/manufacture | checks printability constraints | decides, orders, prints |

The human gate is not a formality. In the first real part built this way, the
single most dangerous defect — a model that passed every dimension, volume and
validity test while consisting of five disconnected bodies — was caught
**visually by the owner**, not by the suite. Twice in one part the human review
was the only effective gate.

## 4. What the first multi-feature part taught

Condensed from the workshop's `docs/06-lessons-learned.md` (full text in the
repository):

1. **Per-feature tests cannot see feature-to-feature disconnection.** A
   mandatory connectivity check (`body_count == 1`) and a preview-vs-sketch
   comparison before the final build are now workflow steps, not best
   practices.
2. **Assumed dimensions are the biggest error source.** Surface ambiguity at
   the approval gate as veto-friendly assumptions; iterate on the spec, not on
   the geometry — correction rounds then cost one parameter change and a
   re-run of the suite, not re-modeling.
3. **Model the function, not the shape.** A "cheaper" rib layout was rejected
   because rib height defines resting depth of the item the part holds.
4. **Know your renderer's failure modes.** A preview renderer can lie
   (depth-sorting artifacts); judge geometry from reliable views plus measured
   probes, and treat presentation rendering as a separate task.
5. **Printability is a spec-level concern.** Bridging spans, rib orientation
   and hole shrinkage on FDM (~0.1–0.2 mm) belong in the verification report,
   next to the geometric checks.
6. **Anonymization before the first public push** keeps the public history
   clean; a privacy scan is a workflow step, not a later cleanup.

## 5. Status and outlook

- The loop is proven end-to-end on a reference part and a first real part
  (six-pocket organizer with ribbed pocket floors), both with full
  verification reports and owner acceptance recorded in the repository.
- Open work: a presentation-quality headless renderer (the automated preview
  renderer is deliberately minimal), and generated dimensioned drawings
  derived from the spec — so that the public repository shows professional
  artifacts only, while raw hand sketches stay private.
- The pattern is domain-portable: any field where "the expert can judge the
  result but not the code" benefits from the same loop — spec as contract,
  machine-verified correctness, human-judged quality.
