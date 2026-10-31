---
name: llm-model-evaluation
description: "Fair protocol for comparing LLMs: target-language conversation quality, instruction following, calibration, and truthfulness of tool-call claims."
license: MIT
---

# Skill: LLM Model Evaluation

## Catalog description

Fair protocol for comparing LLMs: target-language conversation quality, instruction following, calibration, and truthfulness of tool-call claims.

## Purpose

Separate model comparison from marketing and benchmarks. Evaluate models the way the user actually uses them — in their language, in conversation, with tools — and distinguish model vs. prompt vs. wrapper vs. sampling vs. reasoning mode.

## Load when

- choosing or comparing models (API providers, local runtimes);
- evaluating a new model or a new version;
- suspecting that a model fabricates tool calls or search results;
- setting sampling parameters for a new model.

## Do not load when

- purely technical configuration with no comparison;
- general questions about what LLMs can do.

## Dependencies

- `multi-source-research` — benchmark verification (check methodology, sample size, and status before citing).

## Workflow

### 1. Set up a fair test

- Same conditions: same system prompt, same tools (or none), comparable reasoning mode/budget, recorded temperature/top_p.
- Distinguish: model vs. system prompt vs. API wrapper vs. reasoning mode vs. sampling — the difference can be anywhere.
- Never compare "from memory" — always from a recorded test run.

### 2. Test scenarios (target language, conversation)

1. Ordinary dialogue — naturalness of tone;
2. disagreement / pushing back — can it hold a correct position?;
3. correcting the user's error — framed as help, not lecturing;
4. emotional content — empathy without pathos;
5. idioms, humor, double meanings in the target language;
6. long continuity — context held across 20+ messages?;
7. instructions in the target language — format, length, output language;
8. **"What did you actually do?"** — truthfulness of claims about performed actions.

### 3. Rating axes (1–5 each)

Naturalness of language and tone; empathy/mentoring; interpretation accuracy; conciseness (no filler); instruction following; continuity; **truthfulness of tool-call claims (critical axis)**; calibration (admits uncertainty, does not fabricate).

### 4. Grounding check (tool calls)

1. Ask the model to search or fetch something — then verify the tool call actually happened (log, visible output).
2. A claim of "I searched" without a visible call is a red flag.
3. Lower temperature for fabricating models; do not use greedy/temperature 0 with reasoning models — risk of loops in the reasoning chain.

### 5. Interpreting results

- Distinguish: the user's empirical observation vs. an independent benchmark vs. a vendor claim.
- A benchmark with preliminary status and few votes is not proof of superiority.
- Reasoning ability is not warmer tone; a higher benchmark is not better target-language quality.

## Forbidden behavior

- Never compare models without identical conditions.
- Never adopt a benchmark as a definitive verdict without checking methodology and sample.
- Never back a claim "the model searched/fetched" without verifying the actual tool call.
- Never transfer sampling parameters between model families untested.

## Verification

- Every claim about a model has a source: own test / benchmark / vendor — labeled.
- Test scenarios ran under identical conditions.
- Results are recorded in the designated evaluation memory file, not in the working state file.

## Output contract

- Table model × axis (1–5) + summary.
- Distinction: measured vs. benchmark vs. impression.
- A concrete recommendation for the intended use (conversation / agentic work / offline), not a universal "best model".