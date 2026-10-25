# Skill: Language Fidelity

## Catalog description

language-fidelity.md — keeps non-English user-facing output faithful to the target language: language lock, mechanical non-Latin-script self-check before persistent writes, escalation discipline, and thinking-token economy.

## Purpose

Prevent language degradation in user-facing output: a model instructed to reason in one language (typically English, for tokenizer efficiency) can leak foreign-script characters, foreign words, or malformed morphology into output written in the user's language. A documented production incident (October 2026) showed a primary model emitting CJK characters, French words, and broken word forms inside sentences of another language. This Skill adds a preventive self-check that catches script-level leakage before it is persisted, and states the honest limit of what mechanical detection can and cannot catch.

## Load when

- writing a persistent artifact: memory files, device files, calendar entries, tasks, commit messages;
- writing longer user-facing text in a non-English target language (documentation, README, reports, emails);
- the user corrected a language-fidelity defect (escalation trigger T3) or degradation repeats;
- planning token savings for routine tasks.

## Do not load when

- short conversational answers without a persistent write;
- the output is intentionally English (public repository docs, English README);
- a purely technical computation without prose.

## Dependencies

- `model-escalation-protocol.md` — T3 banner and escalation log.
- `tool-execution-contract.md` — tool-result verification rules.
- `memory-master-index.md` + `memory-file-operations.md` — persistent-write gate.

## Workflow

### 1. Language lock

- User-facing output in the user's target language only. Established technical anglicisms without a native equivalent are allowed.
- Internal reasoning stays in English. Measured evidence: English is the cheaper tokenization baseline (Mandarin measured at 1.76x English tokens on 2M translated sentences, 2026); reasoning tokens are billed as output, so the reasoning language is a direct cost item. Do not switch reasoning to the target language for "naturalness" — it costs more and does not improve quality.

### 2. Mechanical self-check before persistent writes (mandatory)

Before any persistent write containing target-language text, run a non-Latin-script detector on the exact text:

```bash
printf '%s' "<text>" | grep -cP '[\x{4E00}-\x{9FFF}\x{3400}-\x{4DBF}\x{0400}-\x{04FF}\x{0370}-\x{03FF}\x{1F00}-\x{1FFF}]'
```

- Output `0` = clean. The pattern covers CJK ideographs, Cyrillic, and Greek; diacritics of European target languages (for example Czech, Slovak, Polish) do not false-positive (verified 2026-10-25, GNU grep -P).
- Output ≥ 1 = finding; extract the exact characters (`grep -oP` with the same pattern), fix the text, re-run until clean.
- For files: `grep -cP '<same pattern>' <file>`.

### 3. Human/model review (second layer, honest limit)

Mechanical detection does **not** catch Latin-script foreign words ("quelque", "really") or malformed word forms. Before a persistent write, also read the text and check for: foreign words without technical justification, broken morphology, mid-sentence language switching. Fix findings before the write, not after.

### 4. On a finding in production

- Publish a corrected version of the output.
- Emit the T3 banner (accuracy category) and append a row to the escalation log per `model-escalation-protocol.md`.
- If the same degradation type repeats 3 times within 24 hours, recommend switching to a different model (T2 banner logic).

### 5. Thinking-token economy

- Routine tasks (research, calendar, routine shell, documentation): use the lowest reasoning effort the task definition supports.
- Visible plans and justifications: write in a Chain of Draft style (arXiv:2502.18600) — concise, information-dense steps of roughly five words or fewer; published results show large token reductions at comparable accuracy on standard benchmarks.
- Hard tasks (preventive trigger, multi-file refactors, irreversible actions): full reasoning effort — savings never at the cost of quality.
- Latent-space reasoning (Coconut, arXiv:2412.06769) is not applicable to API models: it requires retraining.

### 6. Periodic fidelity measurement (roughly every two weeks)

- Run a fidelity test set: 20–30 realistic prompts in the target language, check outputs with the detector plus review, record results in the model-evaluation memory.
- Optionally run a target-language benchmark suite if one exists for that language.

## Forbidden behavior

- Never claim a check was performed if the detector did not run and the text was not read.
- Never persist text with foreign-script characters or knowingly malformed forms.
- Never switch languages mid-sentence or use foreign phrases as style.
- Never move findings into Active Memory — they belong to the escalation log and Saved Memory.

## Verification

- After every persistent write: run the detector on the written content (not the draft) and re-read per the memory gate.
- After T3: confirm the log row exists (`tail -1 <escalation log>`).
- The detector pattern is verified (2026-10-25, GNU grep -P): diacritic-heavy target language text = 0 findings, CJK = caught and extractable.

## Output contract

- For persistent writes with target-language text: one report line — "language check: OK (detector 0 findings + review)" or "finding <what> → fixed, re-check OK".
- On T3: banner + log row + corrected output, per `model-escalation-protocol.md`.
- For savings recommendations: always separate measured facts (Chain of Draft, low reasoning effort) from estimates.