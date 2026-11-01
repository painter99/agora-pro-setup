---
name: ai-drawing-workflow
description: "Repeatable pipeline for AI-generated print-ready artwork on CPU-only hosts: distilled diffusion generation, line-art or pencil-sketch post-processing, A-series 300 dpi outputs, and mandatory visual verification."
license: MIT
---
# Skill: AI Drawing Workflow
## Catalog description
Repeatable pipeline for AI-generated print-ready artwork on CPU-only hosts: distilled diffusion generation, line-art or pencil-sketch post-processing, A-series 300 dpi outputs, and mandatory visual verification.
## Purpose
Turn "draw me a picture of X" into a reproducible, verified artifact on hardware without a usable GPU: generation with a CPU-friendly distilled diffusion engine, deterministic post-processing into clean black-and-white line art or a grayscale pencil sketch, print-ready A-series raster, vector, and PDF outputs, and honest quality gates. Records engine quirks (command-line frontends that generate but never save, few-step models without usable negative prompts) in this Skill and in the delivery README, so repeats do not rediscover them.
## Load when
- the user asks to draw or generate an illustration, coloring page, or pencil sketch on the host;
- a black-and-white print-ready version (A4 or A3 at 300 dpi) is required;
- prompts of a generation pipeline need iterative tuning for visual quality;
- a new model, engine, or post-processing tool is being considered for adoption — apply `multi-source-research` before adopting it.
## Do not load when
- the task is a CAD or technical part drawing — use `cad-spec-driven-workflow`;
- the task is routine photo editing achievable with image tools and no generation;
- the task is pure vector or typographic design without generated imagery — use `graphic-design-art-director`.
## Dependencies
- `tool-execution-contract` — verification and retry discipline for every step.
- `shell-and-device-operations` — detached background jobs and file handling on the host.
## Workflow
1. **Write a task list.** Create a small JSON task list; per task: prompt, output path, seed, step count, pixel size, model id, mode (`lineart` or `sketch`), and threshold. First iteration: two variants of the subject (sketch plus coloring page) with different seeds. Distilled few-step models have no usable negative prompt, so describe everything positively and in detail, starting from the matching template below. When the artwork is part of a larger design (poster, layout, identity), consult `graphic-design-art-director` for the brief and composition first; for a standalone picture request this Skill alone suffices.
   - Coloring page template: "A black and white coloring book page of a friendly SUBJECT in side profile. Bold clean vector-style outlines with uniform thick line weight, large clearly separated regions, closed outlines suitable for coloring, pure white background, black line art only, no shading, no gradients, no crosshatching, no background objects, generous white margins."
   - Pencil sketch template: "A realistic graphite pencil sketch of a single SUBJECT in side profile, illustrated for a children's storybook. Gentle expression with a small bright round eye, soft cross-hatching shading on belly, legs, and tail underside, clean pure white paper background with no gray wash, no scenery, generous white margins, monochrome black and white."
   - These are example framings; adapt subject, pose, and shading regions to the task. Coloring pages must forbid shading in the prompt; sketches require it.
2. **Generate through a saving wrapper.** Run the engine via a library-level wrapper that stores each image plus a JSON sidecar (model, seed, steps, latency); engine command-line frontends may generate successfully yet save nothing, so verify files on disk instead of trusting exit codes. Load the model once per batch, run as a detached background job, and poll the log for saved and done markers. Never run two large model instances in parallel on a RAM-limited host.
3. **Post-process per mode.**
   - `lineart` (coloring page): grayscale, contrast level, threshold, morphological close and dilate to solidify lines, vectorize with binary color mode and spline fitting plus a speckle filter, place the vector on the target canvas preserving aspect ratio, then render raster and PDF at target size.
   - `sketch` (pencil look): grayscale with a level stretch that whitens the paper while preserving graphite tones, center on the target canvas at target dpi, then render raster and PDF; keep grayscale — thresholding destroys pencil shading.
   - Thresholds are tuned per engine contrast; weak one-step models crumble under aggressive thresholds, so lower the threshold or fall back to `sketch` mode.
4. **Verify visually, always.** Look at every final render. Run an independent fresh-context critique (aesthetics, audience fit, print cleanliness, anatomy) that returns a print-or-fix verdict per artifact. Never report done without looking.
5. **Iterate from the failure-mode table in this step.** Re-run only affected tasks with cured prompts and, when needed, a new seed.

   | Failure mode | Prompt cure |
   |---|---|
   | hooked or detached tiny arms | tiny two-fingered arms held close to the chest with clearly drawn claws |
   | teeth as scattered islands | clearly separated triangular teeth inside the open mouth |
   | dark ring around the eye | small bright round eye with a highlight |
   | gray wash across the paper | clean pure white paper background with no gray wash |
   | scary expression for young children | gentle non-scary expression, friendly storybook mood |
6. **Deliver with metadata.** Copy finals plus a README (model, seeds, date, license, observed engine quirks, print hints) into the agreed handoff directory; archive superseded versions in a subfolder instead of overwriting. A concept image meant for later 3D realization goes to `cad-spec-driven-workflow` as its sketch/intent input, ideally after a design pass via `graphic-design-art-director`.
## Forbidden behavior
- Do not claim an image was generated, saved, viewed, or print-verified without evidence (file listing, dimensions, inspected render).
- Do not install GPU drivers, system packages, or kernel modules to accelerate generation without explicit approval; CPU and integrated-GPU paths are the default.
- Do not run two heavy model instances concurrently on a RAM-limited host.
- Do not ship AI-rendered text as final artwork text; set text vectorially with licensed fonts instead.
- Do not deliver generated output without checking the model license for the intended use (personal versus commercial).
- Do not overwrite previous delivery versions; archive them.
## Verification
- A dimensions check confirms the target canvas size and dpi metadata on final rasters.
- The PDF opens and reports one page at the target physical size.
- Every final was viewed by the agent and critiqued independently; verdicts are recorded.
- The delivery directory listing confirms file names and sizes.
- The generation model's license is recorded in the delivery README.
## Output contract
1. **Artifacts:** paths, formats, and dimensions of finals and of vector or editable sources.
2. **Generation record:** model, steps, seeds, and latency per task.
3. **Verification:** what was viewed, critique verdicts, and what remains unverified.
4. **Notes:** license constraints, print recommendations, and next-iteration ideas.
## Hard limits
- One background generation job at a time; batch tasks inside a single model load.
- At most two critique-and-fix rounds per artifact before asking the user for direction.
- At most three seeds or variants per concept; beyond that, involve the user.