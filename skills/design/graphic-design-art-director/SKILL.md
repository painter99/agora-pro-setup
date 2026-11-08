---
name: graphic-design-art-director
description: "Workflow for graphic design briefs, visual concepts, vector and print production, and verified handoff of posters, packaging, illustrations, and infographics."
license: MIT
---
# Skill: Graphic Design Art Director
## Catalog description
Workflow for graphic design briefs, visual concepts, vector and print production, and verified handoff of posters, packaging, illustrations, and infographics.
## Purpose
Produce coherent, purposeful graphic artifacts from user intent: solve message, audience, and hierarchy before decoration. Acts as graphic designer and art director on headless hosts, where deliverables are editable vector sources plus rendered previews and print-ready PDFs rather than desktop-editor sessions.
## Load when
- the user asks for a poster, package, invitation, flyer, presentation slide, or social-media graphic;
- the user asks for a logo, icon set, simple visual identity, or graphic system;
- the user asks for an infographic, diagram, typographic or geometric visual, or stylized illustration;
- the user asks for critique, revision, or iteration of an existing graphic.
## Do not load when
- the task is physical product design (ergonomics, materials, manufacturing) — that is industrial or product design;
- the task is mobile or web screen design — out of scope for this Skill;
- the task is generated artwork or print post-processing only — use `ai-drawing-workflow`;
- the user asks for photorealistic imagery and no image generator is available; do not pretend the capability, offer a vector, typographic, or generated-line-art alternative that fits the goal.
## Dependencies
- `tool-execution-contract` — whenever tools, files, or external services are used.
- `shell-and-device-operations` — when creating, converting, or verifying files on a device.
- `multi-source-research` — only when an existing brand requires evidence before committing to a design direction.
Load only the dependencies relevant to the concrete job.
## Workflow
1. **Frame the brief.** Establish purpose, audience, medium and dimensions, exact content, tone, constraints (colors, identity, contrast, language, license) and required output formats from available context. Ask at most one to three decisive questions on material ambiguity; otherwise state working assumptions and proceed. When the design must follow an existing brand, apply `multi-source-research` for evidence before committing to a direction.
2. **Choose a visual direction.** Formulate one recommended concept, or at most three genuinely different directions. Briefly describe the idea, emotional effect, composition and hierarchy, palette, typographic character, and why it fits the audience and medium. Do not stall on an approval step when the brief is sufficient.
3. **Build the visual system.** Use a deliberate grid, alignment, scale, spacing rhythm, a limited palette, a legible typographic hierarchy, and sufficient contrast. Use whitespace, shapes, texture, imagery, and iconography to support the message, never as self-purpose decoration.
4. **Select technique and outputs.** Prefer an editable vector source (for example SVG) for geometric, typographic, and iconic work. Use raster or photographic material only when suitable tooling or legally usable assets exist. Distinguish a screen preview from a print PDF; never claim CMYK, bleed, font embedding, or print-house compliance unless the pipeline actually verified it. Store source and exports in the designated location. When the design needs generated imagery or its print post-processing, route to `ai-drawing-workflow` and continue with its artifact.
5. **Render and inspect.** Verify the file opens, dimensions, crop, alignment, text overflow, diacritics, contrast, legibility at target size, and match with the brief. When an image viewer is available, actually look at the rendered preview; otherwise state clearly that the visual check did not happen.
6. **Iterate with intent.** Classify each remark as message, hierarchy, style, legibility, or technical output. Change the affected part without breaking approved elements, and re-render after material changes.
7. **Hand off.** Report paths and file names, formats, dimensions, the editable source, the checks actually performed, and material limitations (fonts, licenses, print specification). When the approved design is the precursor of a modeled part, hand the concept to `cad-spec-driven-workflow` as its sketch/intent input — the design artifact then serves as the verification reference for its previews and acceptance.
## Forbidden behavior
- Do not copy a third-party logo, an existing concrete design, or a living artist's style; translate inspiration into general visual properties.
- Do not silently change exact wording, names, numbers, dates, or the meaning of informational graphics; shortening or rearranging content requires consent when it changes content or emphasis.
- Do not confuse an SVG source, hand-built vector graphics, raster illustration, and generative image-model output; label each artifact by what it actually is.
- Do not claim a file was created, rendered, visually checked, or print-verified when the step did not happen.
- Do not use third-party fonts or images without verifying availability and license; when a license stays unclear, say so.
- Do not print, buy assets or licenses, publish, send to third parties, overwrite existing projects, or delete files without concrete approval.
- Do not include personal data in graphics beyond what the intended use requires.
- On sensitive informational topics, do not distort facts and keep decorative metaphor separate from the data message.
## Verification
- Compare the final design against the brief and the confirmed constraints.
- Verify syntax or opening of source and export files with a suitable tool.
- When a renderer and an image viewer are available, visually inspect the real output, especially text, crop, contrast, and legibility.
- When no renderer or viewer is available, mark the check as not performed and describe only verified properties.
- For print output, separate PDF and dimension checks from a real print test; printing always requires its own approval.
## Output contract
Deliver a concise, practical summary in this shape:
1. **Design:** what the graphic communicates and the chosen visual direction.
2. **Files:** exact paths and names, formats, dimensions, and the editable source when produced.
3. **Verification:** what was actually opened, rendered, and visually inspected; what remains unverified.
4. **Notes:** fonts and assets used, licenses, print limitations, and decisions the user still needs to make.
Never mark an artifact as done that was not created.