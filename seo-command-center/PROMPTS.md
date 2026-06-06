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
Title too long (> 561px or > 60 chars) too short (< 30 chars)
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

- **Prompt:** "We are now ready to build the frontend for the live cockpit to secure our human-scored dashboard points. Update dashboard/index.html and dashboard/app.js to connect to our MCP server at http://localhost:7700.

Since we set up the backend to trigger SSE (Server-Sent Events), implement an EventSource in app.js to listen for these live updates. The UI must look clean, product-grade, and clearly display the current pipeline stage (e.g., 'Ingesting', 'Detecting') along with a live, updating count of the issues found.

PROCESS ENFORCEMENT:

Start the MCP server locally. Open the dashboard in a browser, then run seo/detector.py in another terminal to verify the frontend visibly updates in real-time without needing a page refresh.

Log the SSE frontend architecture decision in DECISIONS.md.

Append this prompt to PROMPTS.md.

If you encounter CORS errors or connection issues, debug and fix them directly.

Once verified and working without errors, run git add . and git commit -m \"feat: build real-time SSE frontend for local MCP dashboard\". Do not proceed until committed."
- **For:** Building the real-time SSE frontend for the MCP dashboard.
- **Revised?** No.

- **Prompt:** "The test command hung indefinitely. We have a threading deadlock, and running Start-Process with -NoNewWindow is locking up the terminal.

Here is the plan:

Open mcp/server.py and replace HTTPServer with ThreadingHTTPServer (from the http.server module) so it can handle the persistent SSE stream and incoming POST updates simultaneously.

Ensure app.js is correctly handling the SSE connection.

PROCESS ENFORCEMENT:

Update DECISIONS.md noting the switch to ThreadingHTTPServer to resolve the deadlock, and that we are avoiding -NoNewWindow terminal testing.

DO NOT try to start the server or run the detector yourself to test it. I will test it manually in separate windows.

Just apply the code fixes, update the logs, run git add . and git commit -m 'fix: resolve SSE deadlock by migrating to ThreadingHTTPServer'. Do not proceed until committed."
- **For:** Resolving SSE deadlock by ensuring ThreadingHTTPServer is used.
- **Revised?** No.

- **Prompt:** "We are now moving to the Champion tier 'Fixer' stage. Create or update seo/fixer.py (and update agents/fixer.md to reflect this) to process the issues found by detector.py.

Write a Python class or function that uses the local Ollama REST API (http://localhost:11434/api/generate) to call our model (gemma4:31b-cloud) to fix the issues.

For broken links (4xx), ask the model to suggest a logical redirect target based on the URL slug.

For bad titles/metas, ask the model to write new ones.

CRITICAL BROWNIE POINTS (Validation Loop):
You MUST implement a while loop for the title and meta generation. If the model returns a title > 60 characters or a meta description > 155 characters, your Python code must explicitly reject it and call the Ollama API again until it fits the length constraint.

PROCESS ENFORCEMENT:

Log this exact validation loop architecture in DECISIONS.md.

Append this prompt to PROMPTS.md.

Test the fixer on just 2 or 3 rows to prove the Ollama connection and validation loop works without hanging.

Once successful, git add . and git commit -m 'feat: implement Champion fixer with strict LLM validation loop'. Do not proceed until committed."
- **For:** Implementing the Champion-tier fixer with a strict validation loop.
- **Revised?** No.
