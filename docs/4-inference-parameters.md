# Deep Dive: My Recommended Inference Parameters

Inference parameters control **how** the model generates tokens (sampling), not **what** the model knows. My settings are tuned for mobile Agora usage: deterministic enough to avoid hallucinations, creative enough for natural language, and cheap enough to keep streaming fast on a phone.

## My Default Sampling Config

| Parameter | Value | Why I use it |
| :--- | :--- | :--- |
| Thinking Budget | **2048 tok** | Enough headroom for multi-step planning without bloat. |
| Output Budget | **8192 tok** | Hard ceiling – prevents runaway responses on long tasks. |
| Temperature | **0.5–0.7** | Sweet spot: factual but not robotic. |
| TopP | **0.95** | Standard nucleus sampling, matches community best practice. |

> 💡 Per-model tweaks: GLM-5.3-Flash handles the lower bound (0.5)
> cleanly and benefits from tight output (it is verbose on AA).
> When I switch to GPT-5.6 Luna Pro for vision/PDF or a hard CLI pass,
> I nudge Temperature to 0.6 for slightly more descriptive captions.

## Where to set these in Agora

Agora exposes these under **Settings → Model Parameters** (inference settings, not part of the system prompt). Set them once per model and Agora remembers them.
```
