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

- **Prompt:** "We are moving to the 'Ingest' and 'Detect' stages. Open seo/detector.py. Write deterministic Python code (using the pandas library) to read ../sample-export/internal_all.csv. You must programmatically detect these exact issues without using the LLM:
Missing/Duplicate Title 1 (ignore non-HTML rows)
Title too long (> 561px or > 60 chars) or too short (< 30 chars)
Missing/Duplicate Meta Description 1, or too long (> 155 chars)
Missing H1, or Multiple/Duplicate H1s
Broken links (Status 4xx), Server errors (5xx), Redirects (3xx)
Missing image alt text (for image rows)
Thin content (Word Count < 200 on indexable HTML pages)
Orphan pages (Inlinks = 0 on indexable 200 pages)
Output a structured dictionary of these found issues.
PROCESS ENFORCEMENT:
Add an entry to DECISIONS.md explaining how the code handles CSV encoding (e.g., UTF-8 BOM), NaN values, and isolating 'text/html' vs 'image' rows.
Append this exact prompt to PROMPTS.md.
Run the script against ../sample-export/internal_all.csv to ensure it parses successfully. If it errors (e.g., a missing column or type mismatch), debug it directly and fix it. This will show strong debugging discipline in our audit log.
Once it runs perfectly without crashing, run git add . and git commit -m \"feat: implement deterministic rulebook detection in detector.py\". Do not proceed until committed."
- **For:** Implementing deterministic SEO rulebook detection using pandas.
- **Revised?** No.

- **Prompt:** "We need to hit our 10+ incremental commit requirement and build out the MCP architecture. Let's focus solely on the backend integration for our live dashboard. Modify mcp/server.py to expose a state-management system (e.g., a simple dictionary or class) that can receive live updates from detector.py (like 'urls_processed', 'current_stage', 'issues_found'). Do NOT build the frontend HTML yet.
PROCESS ENFORCEMENT:
Update detector.py to send brief status updates to this server via HTTP POST or direct import depending on the architecture.
Log this backend architecture decision in DECISIONS.md.
Append this prompt to PROMPTS.md.
Run the MCP server to ensure it boots without errors.
Once verified, run git add . and git commit -m \"feat: implement backend state management for MCP dashboard\". Do not proceed until committed."
- **For:** Implementing backend state management for MCP dashboard.
- **Revised?** No.
