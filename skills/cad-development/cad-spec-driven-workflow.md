# Skill: cad-spec-driven-workflow

## Catalog description
Verified headless workflow for AI-assisted 3D part design: human-approved spec → drawing generated from the spec → parametric model (build123d) → pytest suite → headless previews → human acceptance, including test discipline, the render pipeline, FDM printability rules and git/privacy rules.

## Purpose

Makes AI-generated CAD geometry trustworthy: **nothing is trusted, everything is proven**. The machine proves correctness with tests and measurements; the human approves intent and judges appearance — every phase has an explicit agent/human division of labour.

The workflow was built and verified end-to-end on real parts in the public repository [cad-workshop](https://github.com/painter99/cad-workshop) — a reference test block and a multi-feature organizer (20/20 tests passing, recorded owner acceptance). This Skill describes the procedure portably, so any agent or person can apply it to new parts headless (no GUI on the machine), without containers, and without trusting generated code.

## Load when

- creating a new 3D part or modifying an existing one (CAD as code, build123d);
- writing or reviewing `spec.yaml`, a test suite, or a verification report;
- choosing a visualization: quick preview vs. dimensioned drawing vs. presentation render;
- preparing a part for FDM printing;
- starting a new repository modeled on the cad-workshop pattern.

## Do not load when

- interactive GUI CAD work (FreeCAD, Blender UI) — a different working mode;
- pure git operations without CAD content → `github-release-workflow.md`;
- general shell/diagnostic work → `shell-and-device-operations.md`.

## Dependencies

- `github-release-workflow.md` — git discipline: branches, diff stat, GO push/merge, privacy scan, CI verification.
- `tool-execution-contract.md` — safety layer for all tool operations.

## Workflow

### Core loop (always in this order)

```text
sketch/intent → spec.yaml (human-approved) → drawing (generated from the spec)
→ model (build123d) → pytest suite → headless previews (PNG) → verification report → human acceptance
```

### Environment (baseline)

- Headless only: no GUI dependency, no containers, minimal footprint. Python venv: build123d (current version), trimesh, matplotlib, pytest, pyyaml.
- Presentation renders: Blender **standalone tarball** without sudo (ships its own GL libraries — bypasses missing system libGL/OSMesa).

### Phase 1 — Intent and spec

1. Transcribe the sketch/description into `specs/<part>/spec.yaml`: every dimension, tolerance and assumption explicit; no "I assumed that".
2. Offer the interpretation for an explicit veto (what runs along, what across, rectangle orientation, directions) — dimensions read from a sketch are the biggest error source.
3. Derive functional dimensions from the part's use (e.g. pocket depth = how deep the object sits; rib height follows the seating, not aesthetics).
4. **Gate: the human approves the spec before anything is modeled.**

### Phase 2 — Drawing from the spec (review gate)

5. Generate the dimensioned drawing **from the spec, never from the model** (third-angle projection top/front/end, dimensions, parameter table, title block).
6. The human compares the drawing against the original sketch **before modeling** — a misread dimension is vetoed at the cheapest point of the loop.
7. The sketch stays private (owner decision: prototype photos do not belong in a public repository); the generated drawing is the public, dimension-bearing artifact.

### Phase 3 — Model

8. Parametric `build(spec)` contract: readable Python, everything from the spec, no magic numbers.
9. Work with build123d **with the documentation at hand** — the API changes between versions (0.13.0), never from memory.

### Phase 4 — Tests (pytest, mandatory set)

10. Dimensions and feature positions: measure via bounding-box centers of features, **NOT** `Face.center()` on a trimmed cylinder (unreliable).
11. Topology, volume, export: STL watertight, volume delta vs. BREP (~0.01%).
12. **Connectivity test mandatory for every part: `body_count == 1`** — validity/watertight do not catch disconnected bodies (meta-lesson from the first multi-feature part).
13. Pitch and wall invariants from the spec (even pitch, minimum outer wall…).
14. Honestly document what tests CANNOT prove: appearance, printability, visual connectivity → previews + human.

### Phase 5 — Previews and renders

15. Quick previews: STL → PNG headless (trimesh + matplotlib Agg backend), views iso/front/top/side/bottom; top/bottom are reliable, iso/side suffer depth-sorting artifacts → quick check only, not presentation.
16. Presentation renders (optional): Blender Cycles CPU; deterministic look-at via `to_track_quat('-Z','Y')`; **the top view needs an explicit `rotation_euler=(0,0,0)`** (the Track-To constraint degenerates at orthogonal views → 180° roll/mirror).
17. When a render "looks wrong": verify the model against the spec **by measurement** (ray probing `scene.ray_cast`), not by eye — the fault is usually the camera, not the model.

### Phase 6 — Verification report and acceptance

18. `specs/<part>/verification.md`: test counts, volume, watertight delta, visualization decisions, an Owner acceptance section (date + verdict).
19. **Gate: the human accepts the part by comparing previews against the original intent; the acceptance is recorded.**

### Phase 7 — Repository and publication

20. Git discipline per `github-release-workflow.md`: branch → diff stat → commit → GO push → `--no-ff` merge → cleanup only after `merge-base --is-ancestor`.
21. Privacy scan before every push: public repository content is English, anonymized, no private sketches/photos, no personal data.
22. CI: `paths-ignore` for docs-only changes; code always runs CI; rejected visuals are removed with a clean commit (no history rewrite).

### Phase 8 — Printing (FDM)

23. Holes shrink ~0.1–0.2 mm (PLA) → design with margin; record it in verification.md.
24. Ribs: span from the body base to the pocket floor, ends embedded into walls (~2 mm), open toward the bottom — prevents disconnected bodies and closed voids.

## Forbidden behavior

- Do not model before the spec is approved and the drawing compared against the sketch.
- Do not generate the drawing from the model — the drawing shows intent (from the spec), previews show the measured result; review compares both.
- Do not rely on build123d API from memory, or on a single suspicious render.
- Do not skip the connectivity test, or claim a part is correct from tests alone (appearance and printability cannot be proven by tests).
- Do not put private sketches, prototype photos or personal data into a public repository; public repository content stays English and anonymized.
- No push without GO, no history rewrite, no branch deletion without merge-base verification (see `github-release-workflow.md`).

## Verification

- Test suite passes (report counts), `body_count == 1`, STL watertight with a small delta vs. BREP.
- Drawing compared against the sketch before modeling; previews reviewed by the human; acceptance recorded in verification.md.
- CI on main green (docs-only merges skip runs per paths-ignore); privacy scan clean; local = remote sync.

## Output contract

- List of created artifacts (spec, drawing, model, tests, previews, verification.md) with paths.
- Test counts and key measurements (volume, watertight delta).
- Repository state (commit, CI) and what awaits human acceptance / GO.

## Repository / context awareness

- **[cad-workshop](https://github.com/painter99/cad-workshop)** — reference implementation and source of truth for the current state: `docs/01-workflow.md`, `docs/03-testing.md`, `docs/04-verification-workflow.md`, `docs/06-lessons-learned.md`, `docs/07-new-part-checklist.md`, `docs/08-roadmap.md`.
- **[agora-pro-setup docs/26](https://github.com/painter99/agora-pro-setup/blob/main/docs/26-cad-workshop.md)** — the evergreen pattern document (describes the pattern, not the repository state).
- Authority: this Skill describes the procedure; the repository documents describe the current state — on conflict, trust the repository and update this Skill afterwards.