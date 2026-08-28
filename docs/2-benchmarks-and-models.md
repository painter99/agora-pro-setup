# Deep Dive: My Model Selection Strategy

Choosing the right model for Agora isn't about raw general benchmark scores (like MMLU). For me, it's entirely about **Agentic Tool Calling Stability**, mobile streaming latency, and cost-efficiency.

## The Benchmark That Matters: Artificial Analysis

**MCP Atlas is not published** for GLM-5.3-Flash or GPT-5.6 Luna Pro, so I do not invent a score. The independent source I use is the **Artificial Analysis Intelligence Index** (agentic work, terminal use, coding, science, long context) plus measured **output speed**, **TTFT**, and **list price**.

### Verified Benchmark Data

Read 2026-08-28 from Artificial Analysis model pages. Terminal-Bench / DeepSWE are **vendor launch numbers** (Z.ai vs OpenAI) — mixed sources, not a head-to-head lab run. Luna Pro = GPT-5.6 Luna with `reasoning.mode=pro`; AA reports **Luna (max)** as the independent proxy.

| Metric / Feature | 🥇 GLM-5.3-Flash (Primary) | 🥈 GPT-5.6 Luna Pro (Alternative) |
| :--- | :--- | :--- |
| **AA Intelligence Index** | **57** | 52 (Luna max) |
| **Output Speed** | ~50 tok/s (AA median) | **~126 tok/s** (AA Luna max) |
| **Time To First Chunk** | ~1.5 s (Z.ai, AA providers) | ~0.86 s (Luna non-reasoning, AA) |
| **List Pricing (1M)** | **$0.15 in / $0.50 out** | $0.20 in / $1.20 out |
| **Cost per AA Index task** | $0.09 | **$0.05** (Luna max) |
| **Terminal-Bench 2.1** | 84.3 (Z.ai) | 84.7 (OpenAI Luna) |
| **DeepSWE v1.1** | 63.4 (Z.ai) | 67.2 (OpenAI Luna) |
| **Context Window** | 1M | 1.05M |
| **Input modalities** | Text, image, **video** | Text, image, PDF |
| **Licensing** | **MIT open-weight** | Proprietary |

Sources: [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash), [AA GPT-5.6 Luna](https://artificialanalysis.ai/models/gpt-5-6-luna), [OpenRouter Luna Pro](https://openrouter.ai/openai/gpt-5.6-luna-pro) ($0.20 / $1.20). GLM list price is $0.15 / $0.50; a 50% Z.ai promo runs through 2026-09-09 — I quote **list**, not the discount.

---

## My Dual-Model Architecture

I stopped looking for one "perfect" model and instead use these two interchangeably depending on my current task:

### 1. My Primary Workhorse: GLM-5.3-Flash

GLM-5.3-Flash (Z.ai, Aug 2026; formerly the Ox Alpha stealth listing) is my overall winner for daily mobile agentic workflows. Independent Intelligence Index **57** at **$0.15 / $0.50** per 1M tokens is the price/performance pair I actually feel on a phone bill. 320B total / 18B active MoE, MIT weights, 1M context, native image **and video**.

Caveat I do not hide: AA calls it **notably slow** (~50 tok/s median) and somewhat verbose. Fast third-party hosts exist (Databricks ~267 tok/s on AA's provider page), but I plan around the median, not the peak.

### 2. My A/B Testing & Speed Partner: GPT-5.6 Luna Pro

GPT-5.6 Luna Pro is the same Luna weights with OpenAI `reasoning.mode=pro`. AA Luna (max) sits at Intelligence Index **52** but **~126 tok/s** — about 2.5× the GLM median — and **$0.05 per AA task** because it burns fewer tokens. I switch to it when streaming feel matters, when I need PDF/image in the OpenAI stack, or when I want a higher-compute pass on a hard terminal/debug job.

Caveat: Pro thinking raises time-to-first-**answer** (OpenRouter P50 latency on Pro is tens of seconds). Non-reasoning Luna is the snappy one (~0.86 s TTFT).
```
