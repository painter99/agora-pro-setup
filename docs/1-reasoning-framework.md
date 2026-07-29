# Deep Dive: My Core Reasoning Framework

LLMs are "greedy predictors"—they want to generate the next token as fast as possible. This leads to hallucinations, missed prerequisites, and premature execution. My framework forces the LLM into **systematic planning** before any action—turning it from a chatbot into a methodical engineer.

## Key Rules (and why I have each one)

### Rule 1 – Logical Dependencies & Reverse Engineering
*"Plan backward from the goal: identify prerequisites and order of operations."*
**Why I have it:** On mobile I often give incomplete commands in random order. Rule 1 forces the agent to look at the goal, map dependencies backwards, and reorder operations logically before running the first tool.

### Rule 3 – Abduction & Critical Thinking
*"Look for the most logical root cause—not just the obvious error. Question your assumptions."*
**Why I have it:** When a tool call fails (e.g., file not found), a standard LLM just repeats the same failed command. This rule forces a hypothesis (*"Did the path change? Missing permissions?"*) and a critical challenge of its own assumptions before retrying.

### Rule 5 – Information Exhaustion (Zero Laziness)
*"NEVER ask the user for information you can retrieve yourself."*
**Why I have it:** Writing long explanations on a phone is frustrating. This rule explicitly forbids laziness. If the answer is in Active Memory, a previous conversation, or on the web, the agent must actively trace it itself.

### Rule 6 – Absolute Grounding (Zero-Trust of Own Memory) + Conflict Surfacing
*"Internal knowledge is UNRELIABLE. Verify via trustworthy primary sources. When sources conflict, surface the contradiction—do not smooth it over."*
**Why I have it:** LLMs suffer from overconfidence *and* from consensus bias (sycophancy): when two sources disagree, they tend to average them out into one "nice" answer. Rule 6 strips away that overconfidence by forcing verification via primary sources, and explicitly forbids smoothing over conflicts—both citations must be presented.

### Rule 8 – Intelligent Persistence & Structural Halt
*"On structure/auth errors (Permission denied), DO NOT REPEAT, DO NOT HALLUCINATE a fix; change strategy and wait."*
**Why I have it:** *"Halts are features."* Lesson learned from a mobile Git/SSH workflow session. When the agent hits a hard wall (missing credentials), I don't want it to spam the server with guessed passwords. I want it to stop, explain the root cause, and wait.

### Rule 9 – Inhibition, Safety, Language & Tone
*"Halt and require consent before any destructive action. Match the user's language. Keep final responses concise, without robotic filler phrases. For research tasks, explicitly state any limitations."*
**Why I have it:** Safety, UX, and intellectual honesty. On mobile I don't want the agent to run rm -rf or overwrite a critical file without my knowledge. The ban on filler phrases (*"Understood"*, *"Here is the information"*) saves screen space. Matching the user's language avoids awkward bilingual outputs. Stating limitations explicitly prevents the agent from pretending certainty when scope, time, or source availability constrained the answer.
