# Saved Memories Guide (The Archive)

Saved Memories are persistent files that my agent **does not read automatically** until it realizes (based on the Archive Index in my Active Memory) that it actually needs them for the current task.

### My Best Practices for Archive Files
1. **No spaces in filenames:** I always use `snake_case.md` (e.g., `project_alpha.md`). It is much easier for the AI to invoke tools with clean filenames.
2. **Strict Specialization:** I never mix unrelated topics in one file. I create one file for my CV, one for a specific hobby, and one for a specific coding project.
3. **Static vs. Dynamic Data:** 
   - I put historical milestones (e.g., past jobs, completed courses, static specs) here.
   - I keep my *current* state (what I am doing *today*) in my Active Memory.
4. **Use Markdown:** I format the inside of these files using clean Markdown (`## Headers`, `- bullet points`). LLMs parse Markdown natively with near-perfect accuracy.
```
