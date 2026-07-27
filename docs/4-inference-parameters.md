# Deep Dive: My Recommended Inference Parameters

Inference parameters control **how** the model generates tokens (sampling),
not **what** the model knows. My settings are tuned for mobile Agora usage:
deterministic enough to avoid hallucinations, creative enough for natural
language, and cheap enough to keep streaming fast on a phone.

## My Default Sampling Config

| Parameter        | Value        | Why I use it                                              |
| :---             | :---         | :---                                                     |
| Thinking Budget  | **2048 tok** | Enough headroom for multi-step planning without bloat.   |
| Output Budget    | **8192 tok** | Hard ceiling – prevents runaway responses on long tasks. |
| Temperature      | **0.5–0.7**  | Sweet spot: factual but not robotic.                     |
| TopP             | **0.95**     | Standard nucleus sampling, matches community best practice. |

> 💡 Per-model tweaks: MiniMax M3 handles the lower bound (0.5)
> cleanly. When I switch to Qwen 3.7 Plus for vision tasks,
> I nudge Temperature to 0.6 for slightly more descriptive image captions.

## Where to set these in Agora
Agora exposes these under **Settings → Model Parameters**
(inference settings, not part of the system prompt). Set them once
per model and Agora remembers them.
```
