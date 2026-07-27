# Deep Dive: My Model Selection Strategy

Choosing the right model for Agora isn't about raw general benchmark scores (like MMLU). For me, it's entirely about **Agentic Tool Calling Stability**, mobile streaming latency, and cost-efficiency.

## The Benchmark That Matters: MCP Atlas
Developed by Scale AI, **MCP Atlas** (Model Context Protocol Atlas) tests an AI's ability to discover APIs, chain tools, recover from execution errors, and complete multi-step tasks over long horizons.

### Verified Benchmark Data (Independent Sources)

| Metric / Feature | 🥇 MiniMax M3 (Primary) | 🥈 Qwen 3.7 Plus (Alternative) |
| :--- | :--- | :--- |
| **MCP Atlas (Tool Use)** | **74.2%** (#13) | 73.2% (#16) |
| **Output Speed** | **~80 tok/s** | ~54 tok/s |
| **Time To First Token** | **1.62s** | 2.87s |
| **Average Pricing (1M)** | **$0.24 in / $0.96 out** | $0.32 in / $1.28 out |
| **SWE-Bench Verified** | **80.5%** | 77.7% |
| **Terminal-Bench 2.0** | 66.0% | **70.3%** |
| **Large Context Decode** | **Ultra-fast (MSA)** | Standard Attention |
| **Licensing** | **Open-Weight** | Proprietary |

---

## My Dual-Model Architecture

I stopped looking for one "perfect" model and instead use these two interchangeably depending on my current task:

### 1. My Primary Workhorse: MiniMax M3
MiniMax M3 is my overall winner for daily mobile agentic workflows. It is ~48% faster than Qwen 3.7 Plus, has a 77% faster TTFT, and costs about 25% less. Its MiniMax Sparse Attention (MSA) architecture is the real game-changer—it allows the model to decode 1M token contexts up to 15x faster than standard attention models. When I load massive memory files, M3 doesn't stutter.

### 2. My A/B Testing & Vision Partner: Qwen 3.7 Plus
Qwen 3.7 Plus is my ideal companion model. It excels in Terminal/CLI benchmarks (70.3% on Terminal-Bench 2.0) and features native multimodal capabilities (image and video analysis). I switch to Qwen 3.7 Plus specifically when I need my agent to inspect screenshots, debug mobile UI mockups, or perform heavy terminal automations.
```
