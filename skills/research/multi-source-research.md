# Skill: Multi-Source Research

## Catalog description

Proportional research workflow with query diversification, source scoring, verification, counter-evidence, and bounded iterations.

## Purpose

Provide a reusable research procedure for current, technical, comparative, quantitative, unfamiliar, or disputed questions. It is intentionally stronger than a generic “use primary sources” reminder, but shorter and more adaptable than a maximal research framework.

## Load when

- current or externally verifiable facts materially affect the answer;
- prices, availability, specifications, laws, statistics, rankings, or recommendations are involved;
- a comparison, investigation, or fact-check needs more than one source;
- sources may conflict or the cost of error is meaningful.

## Do not load when

- translating, rewriting, formatting, or brainstorming;
- answering from facts supplied by the user when verification is not requested;
- performing a direct calculation from known inputs;
- a small, low-risk check needs only one clearly authoritative source.

## Dependencies

Use available `web_search` and `web_fetch` tools. Use conversation or Memory tools only when they materially clarify the question. Do not assume any tool is available; follow the current Agora tool set and permissions.

## Proportionality: choose the research level

### Level 1 — Light verification

Use for one narrow, low-risk claim. Search or fetch a suitable authoritative source, check its date and scope, and cite it. If the source is inaccessible or ambiguous, label the limitation.

### Level 2 — Multi-source check

Use for a comparison, recommendation, technical claim, or claim where one source is not enough. Use at least two relevant sources when possible, preferably including a primary source and an independent or contrasting source.

### Level 3 — Deep research

Use for broad, consequential, disputed, or multi-part questions. Run the full workflow below, including a plan, source scoring, counter-evidence, bounded iterations, and a final quality gate.

Do not run Level 3 merely because the user used the words “deep dive.” Match depth to scope and consequence.

## Workflow

### Phase 0 — Scope and plan

1. Restate the decision or factual question in one sentence.
2. Identify the scope, date boundary, geography, and intended use.
3. Split the question into 3–7 sub-questions when it is genuinely multi-part.
4. Choose Level 1, 2, or 3 and state why.
5. For substantial or high-impact Level 3 research, present a concise plan when an approval mechanism is available. For a small check, proceed proportionally.

### Phase 1 — Triage and query diversification

For each important sub-question, create different query angles:

- factual or definitional;
- primary-source or official;
- comparative or analytical;
- counter-evidence, criticism, or limitations.

Do not repeat a query that produced no new information. Search local context, Memory, or prior conversations first when relevant; do not search externally for facts already established and sufficient.

### Phase 2 — Source collection and deep dive

1. Fetch the most relevant sources instead of relying on snippets.
2. Prefer official documentation, standards, legislation, academic work, original data, manufacturers, and reputable institutions according to the topic.
3. Record the source name, URL, publication/update date, claim supported, and access date.
4. Compare source scope, method, definitions, incentives, and recency.
5. Seek at least one independent or opposing source for important conclusions.
6. Never fetch the same URL repeatedly without a reason.

### Phase 3 — Evidence notes and mini-ReAct loop

For every meaningful iteration, keep the compact cycle:

```text
QUESTION → ACTION → OBSERVATION → REFLECTION → UPDATE
```

- **Question:** Which uncertainty or sub-question is being resolved?
- **Action:** Which search or fetch addresses it?
- **Observation:** What does the source actually say?
- **Reflection:** Is it relevant, authoritative, current, corroborated, or contradicted?
- **Update:** What changes in the working conclusion, gap list, or next query?

Do not expose private chain-of-thought. Report only concise evidence and reasoning summaries when useful.

### Phase 4 — Source evaluation

Score important sources from 1–5:

| Axis | 5 | 1 |
|---|---|---|
| Authority | primary or highly relevant expert source | anonymous, unrelated, or weak source |
| Recency | current for the question | materially outdated |
| Specificity | reproducible data, named method, clear scope | vague assertion |
| Independence | independent corroboration or contrasting evidence | dependent repetition or unverified claim |

Use scores to guide confidence, not to manufacture mathematical certainty. Mark a claim `LIMITED EVIDENCE`, `DISPUTED`, or `UNVERIFIED` when appropriate.

### Phase 5 — Chain of verification

Before presenting an important factual claim, check:

```text
□ Is the claim directly supported by a fetched source?
□ Is the source relevant to the exact scope and date?
□ Is there corroboration, or is a single-source fallback explicitly justified?
□ Are numbers attributed with date and methodology?
□ Did I search for contradictory evidence when the claim matters?
□ Did I separate source fact from my calculation or interpretation?
```

If a check fails, weaken the wording, identify the gap, or continue researching. Never fill the gap with an unsupported guess.

### Phase 6 — Contradiction and failure handling

- Surface meaningful source conflicts; do not average them into a false consensus.
- Prefer the newest reliable source for time-sensitive facts, but explain why.
- Prefer primary evidence over commentary when methods and scope are comparable.
- If only one credible source exists, state `SINGLE-SOURCE — LIMITED CONFIDENCE`.
- If search returns nothing, rephrase or narrow the query once or twice.
- If fetching fails, try a relevant alternative source rather than repeating indefinitely.
- If access remains insufficient, report `INSUFFICIENT ACCESS`.

### Phase 7 — Bounded iterations and escape hatch

Use proportional bounds:

| Level | Suggested search/fetch budget | Stop condition |
|---|---:|---|
| 1 | 1–3 total calls | claim verified or limitation clear |
| 2 | up to 8 total calls | key claims corroborated or gaps explicit |
| 3 | up to 15 searches, 10 fetches, 20 total tool iterations | sub-questions answered, budget reached, or no new information |

For Level 3, if two consecutive iterations produce no new evidence or five iterations remain stuck, stop adding tools and reconceptualize the sub-question. Re-run only the affected phase. Report the boundary instead of pretending completeness.

## Output contract

### Level 1–2

```markdown
## Conclusion
## Evidence
## Uncertainty and limitations
## Sources
```

### Level 3

```markdown
# [Title]

> Date: YYYY-MM-DD | Sources: N | Confidence: HIGH/MEDIUM/LOW

## Executive Summary
## Key Findings
## Analysis and Synthesis
## Contradictions and Limitations
## Recommendations / Next Steps
## Source Registry
| # | Source | URL | Date | Relevance / score |
|---|---|---|---|---|
## Methodology Note
```

Always distinguish sourced facts, calculations, estimates, assumptions, interpretations, and recommendations.

## Quality gate

Before finalizing Level 2 or 3 research, check:

- [ ] The requested scope was answered.
- [ ] Important claims have appropriate evidence.
- [ ] Source types and vendor claims are labeled honestly.
- [ ] Counter-evidence and contradictions were not hidden.
- [ ] Confidence matches evidence quality.
- [ ] The result is actionable without pretending certainty.
- [ ] The report states what remains unknown.

If the result fails materially, revise once or mark it `DRAFT — NEEDS HUMAN REVIEW`.

## Forbidden behavior

- Fabricated citations, URLs, quotes, statistics, or tool results.
- Treating snippets as proof.
- Treating a vendor claim as an independent benchmark.
- Repeating failed searches without changing strategy.
- Unlimited research without an escape hatch.
- Presenting a recommendation stronger than the evidence.
- Claiming to have used this Skill before reading it.
