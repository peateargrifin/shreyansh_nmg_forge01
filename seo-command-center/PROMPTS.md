# PROMPTS.md — my key prompts log

Keep the handful of prompts that actually moved the build. Not every message — the ones that
mattered: the system/sub-agent prompts, the ones you iterated on, the "this finally worked"
moment. This shows how you direct an AI, which is graded (challenge brief section 08).

Format per entry:
- **Prompt** (paste it)
- **For:** what you were trying to do
- **Revised?** did you have to change it, and why

---

## My prompts

- **Prompt:** "Update CLAUDE.md to explicitly state: We must NEVER use the LLM to parse raw CSV rows—all detection must be done with deterministic Python code. We are aiming for the Champion tier, which requires a strict validation loop on LLM output (e.g., checking title lengths in code before accepting them) and outputting fix CSV files. We must strictly follow the output contract in ../report.schema.json. Update PROMPTS.md with this request. Ensure .claude/settings.json and the audit hooks are active. Once you have updated CLAUDE.md, commit the changes with: 'chore: establish strict grading constraints and champion tier goals in project memory and CRITICAL PROCESS CHECK: Ensure that .claude/audit.jsonl is actively recording our steps via the hooks. Also, add this prompt to PROMPTS.md, and log any data parsing choices (like handling CSV encoding or empty values) in DECISIONS.md."
- **For:** Establishing strict grading constraints and project goals in memory.
- **Revised?** No.
