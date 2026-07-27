# 📱 Agora App – My Pro Setup for Autonomous AI Agents

Welcome to my personal configuration guide for [**Agora**](https://github.com/newo-ether/Agora) (the premier open-source AI agent app on F-Droid). 

Executing complex workflows on a mobile device—like analyzing server logs, conducting multi-step web research, or managing projects—requires more than just a simple chatbot. It requires a **truly autonomous AI agent** that plans, uses tools, and operates with zero hallucinations.

I built this repository to share my battle-tested setup. It natively utilizes Agora's UI block system and is optimized specifically for token efficiency, fast mobile streaming, and high-reliability tool-calling.

---

## 🗺️ Repository Map & Architecture

```text
               +-----------------------------------+
               |         MY AGORA SETUP            |
               +-----------------------------------+
                                 |
         +-----------------------+-----------------------+
         |                                               |
[ 🛠️ System Configuration ]                     [ 🧠 Memory System ]
 ├── system-prompt/                              ├── memory-management/
 │    ├── 1-system-tab-blocks.md                  │    ├── 1-active-memory-template.md
 │    ├── 2-prefix-tab-blocks.md                  │    └── 2-saved-memories-guide.md
 │    └── 3-suffix-tab-blocks.md                  
         |                                               |
         +-----------------------+-----------------------+
                                 |
                     [ 📚 Deep Dive Docs ]
                      ├── docs/1-reasoning-framework.md
                      ├── docs/2-benchmarks-and-models.md
                      ├── docs/3-troubleshooting.md
                      └── docs/4-inference-parameters.md
```

---

## 💡 Real-World Example: Why You Need This

To understand the difference between a standard "chatbot" and this
**Autonomous Agent Setup**, here is a real situation I handled
directly from my phone while returning from a short vacation abroad:

**The Situation:** I was traveling on an international express train
from one EU country to another, and had a very tight transfer window
— under 5 minutes — for my next regional connection at a border
station. I needed to know whether the regional train would wait for
me in case of a delay, and what my realistic backup options were if
I missed it.

**How My Agent Handled It (MiniMax M3):**
1. **Zero Hallucination & Nuance:** Instead of guessing, it
   autonomously executed multiple verification calls in seconds. It
   checked the current timetable and connection rules across
   operators, explicitly noting that the connection was **not
   contractually guaranteed** in the official schedule — while
   accurately pointing out that onboard staff or dispatch often
   request regional trains to hold for delayed international
   services in practice. Both facts delivered in one answer.
2. **Context Awareness:** When I corrected my departure time
   mid-conversation, the agent instantly recalculated my exact
   timeline and upcoming milestones along the route — border
   crossing, transfer point, final destination — without breaking
   flow.
3. **Problem Solving:** When I asked what my fallback would be if
   the connection didn't hold, it laid out the exact local backup
   (a regional train about 1 hour 15 minutes later), provided
   realistic arrival times, and advised me to use the local
   national rail app for live tracking upon arrival at the transfer
   station.

I got a complete, verified logistical rescue plan while sitting on
a moving international train. **This is what a mobile AI Dev-Ops
& Life assistant looks like.**

---

## 🚀 Quick Start (4 Steps)

1. **Configure Prompt Blocks:** Open Agora → Edit System Prompt. Follow my exact block-by-block layout in [`system-prompt/1-system-tab-blocks.md`](system-prompt/1-system-tab-blocks.md).
2. **Setup Time-Awareness:** Configure the Prefix and Suffix tabs using [`system-prompt/2-prefix-tab-blocks.md`](system-prompt/2-prefix-tab-blocks.md) and [`system-prompt/3-suffix-tab-blocks.md`](system-prompt/3-suffix-tab-blocks.md).
3. **Set Up Your Workbench:** Fill in your Active Memory using my template in [`memory-management/1-active-memory-template.md`](memory-management/1-active-memory-template.md).
4. **Tune Inference Parameters:** Set sampling values in Agora's model settings — see my recommended config in [`docs/4-inference-parameters.md`](docs/4-inference-parameters.md).

---

## ⚖️ My Dual-Model Strategy & A/B Testing

For optimal results in Agora, I use a **Dual-Model Strategy**. Depending on the task, I switch between these two top-tier models to get the best balance of speed, cost, and specialized capabilities.

```text
+-------------------------------------------------------------------------+
|                         MY RECOMMENDED SETUP                            |
+------------------------------------+------------------------------------+
|   🥇 MiniMax M3 (Primary Engine)   |  🥈 Qwen 3.7 Plus (A/B & Vision)  |
|   • Daily workhorse & general chat |  • Multimodal / Screenshot analysis|
|   • Lightning fast (80 tok/s)      |  • Terminal & CLI heavy tasks      |
|   • ~25% cheaper API cost          |  • A/B testing reference model     |
+------------------------------------+------------------------------------+
```

### Verified Benchmark Comparison

| Metric / Feature | 🥇 MiniMax M3 (My Primary) | 🥈 Qwen 3.7 Plus (My Alternative) | Winner / Advantage |
| :--- | :--- | :--- | :--- |
| **MCP Atlas (Tool Use)** | **74.2%** | 73.2% | **MiniMax M3** (+1.0%) |
| **Output Speed** | **~80 tok/s** | ~54 tok/s | **MiniMax M3** (+48% faster) |
| **Time To First Token** | **1.62s** | 2.87s | **MiniMax M3** (77% faster TTFT) |
| **Average Pricing (1M)** | **$0.24 in / $0.96 out** | $0.32 in / $1.28 out | **MiniMax M3** (~25% cheaper) |
| **SWE-Bench Verified** | **80.5%** | 77.7% | **MiniMax M3** (+2.8%) |
| **Terminal-Bench 2.0** | 66.0% | **70.3%** | **Qwen 3.7 Plus** (+4.3%) |
| **Vision & Image Input** | Basic | **Native Multi-image & Video** | **Qwen 3.7 Plus** (Vision Specialist) |
| **Large Context Decode** | **Ultra-fast (MSA)** | Standard Attention | **MiniMax M3** (15x faster on large context) |
| **Licensing** | **Open-Weight** | Proprietary API | **MiniMax M3** (Self-hostable) |

### ⚙️ My Default Sampling Config

| Thinking Budget | Output Budget | Temperature | TopP |
| :---: | :---: | :---: | :---: |
| 2048 tok | 8192 tok | 0.5–0.7 | 0.95 |

*(Full reasoning per parameter → [`docs/4-inference-parameters.md`](docs/4-inference-parameters.md))*

---

### When I use which in Agora:

* **I use MiniMax M3 for 90% of my daily tasks:** It is significantly faster on my phone, cheaper, handles long context decode effortlessly via MiniMax Sparse Attention (MSA), and delivers exceptional multilingual performance.
* **I switch to Qwen 3.7 Plus when:** I need to feed screenshots or UI mockups to my agent, or when I am executing complex CLI/Terminal workflows. *Note: Qwen 3.7 Plus uses standard attention, so processing very large context windows feels noticeably slower than MiniMax M3.*

*(Read my complete deep-dive on why I chose these two models in [`docs/2-benchmarks-and-models.md`](docs/2-benchmarks-and-models.md)).*
