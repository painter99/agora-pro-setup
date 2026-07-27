# Deep Dive: My Core Reasoning Framework

Why does an AI agent need a complex system prompt? By default, Large Language Models are "greedy predictors"—they want to generate the next token as fast as possible. This leads to hallucinations, missed prerequisites, and premature execution.

My framework forces the LLM into a **systematic planning cycle** before taking any action.

## Key Rules Explained

### Rule 1: Logical Dependencies & Constraints
* "Analyze intended action against rules, prerequisites, and order of operations."
* **Why I use it:** On my mobile device, I often give incomplete commands in a random order. Rule 1 forces the agent to reorder operations logically before executing.

### Rule 3: Abductive Reasoning
* "Look beyond immediate or obvious causes."
* **Why I use it:** When a tool call fails (e.g., a file isn't found), standard LLMs repeat the same failed command. Abductive reasoning forces my agent to hypothesize: *"Did the file path change? Do I lack permissions? Let me list the directory first."*

### Rule 6: Absolute Grounding & Zero-Trust
* "Treat your internal knowledge as unreliable."
* **Why I use it:** LLMs suffer from overconfidence. When I ask about a technical specification, they guess. Rule 6 strips away their self-confidence and forces them to use `web_search` or `file_read` before giving me an answer.

### Rule 9: Inhibition & Human-in-the-Loop
* "Halt and wait for user approval before any destructive action."
* **Why I use it:** Safety. When I am connected to local files or a remote shell server from my phone, I ensure my agent never executes `rm -rf`, overwrites a critical file, or sends API requests without my explicit consent.
```
