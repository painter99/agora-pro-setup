# Deep Dive: My Core Reasoning Framework

LLMs are "greedy predictors"—they want to generate the next token as fast as possible. This leads to hallucinations, missed prerequisites, and premature execution. My framework forces the LLM into **systematic planning** before any action—turning it from a chatbot into a methodical engineer.

## Key Rules (and why I have each one)

### Rule 1 – Logical Dependencies & Reverse Engineering
*"Plan backward from the goal: identify prerequisites and order of operations."*
**Why I have it:** On mobile I often give incomplete commands in random order. Rule 1 forces the agent to look at the goal, map dependencies backwards, and reorder operations logically before running the first tool.

### Rule 3 – Abduction & Critical Thinking
*"Look for the most logical root cause—not just the obvious error."*
**Why I have it:** When a tool call fails (e.g., file not found), a standard LLM just repeats the same failed command. This rule forces a hypothesis (*"Did the path change? Missing permissions?"*) and a critical challenge of its own assumptions.

### Rule 5 – Information Exhaustion (Zero Laziness)
*"NEVER ask the user for information you can retrieve yourself."*
**Why I have it:** Writing long explanations on a phone is frustrating. This rule explicitly forbids laziness. If the answer is in Active Memory, a previous conversation, or on the web, the agent must actively trace it itself.

### Rule 6 – Absolute Grounding (Zero-Trust of Own Memory)
*"Internal knowledge is UNRELIABLE. Verify."*
**Why I have it:** LLMs suffer from overconfidence. When I ask for a tech spec, they guess. Rule 6 strips away that overconfidence and forces a web_search or file_read first.

### Rule 8 – Intelligent Persistence & Structural Halt
*"On structure/auth errors (Permission denied), DO NOT REPEAT, DO NOT HALLUCINATE a fix; change strategy and wait."*
**Why I have it:** *"Halts are features."* Lesson learned from a mobile Git/SSH workflow session. When the agent hits a hard wall (missing credentials), I don't want it to spam the server with guessed passwords. I want it to stop, explain the root cause, and wait.

### Rule 9 – Inhibition, Safety & Tone
*"Halt and require consent before any destructive action. Keep final responses concise, without robotic filler phrases."*
**Why I have it:** Both safety and UX. On mobile I don't want the agent to run rm -rf or overwrite a critical file without my knowledge. The ban on filler phrases (*"Understood"*, *"Here is the information"*) saves screen space.
