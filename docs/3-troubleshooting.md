# Deep Dive: Troubleshooting & Mobile UX

## Common Issues & Solutions I've Found

### 1. The Agent Is Guessing Instead of Searching
* **Cause:** My prompt was too vague, or the LLM defaulted to its internal weights out of overconfidence.
* **Solution:** I simply remind the agent of **Rule 6**: *"Apply Rule 6: Verify this claim using web_search before answering."*

### 2. Startup Latency Is Too High
* **Cause:** My Active Memory became bloated, or I was forcing the agent to read a large saved file at startup via a tool call.
* **Solution:** I move static historical data into `Saved Memories` and keep my `Active Memory` under 30 lines. I rely entirely on the **Archive Index** pattern to tell the agent where to find things.
```
