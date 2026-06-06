---
name: fixer
description: Uses the local model to rewrite bad or missing titles and meta descriptions within length limits, and builds a redirect map for broken links. The champion-tier value-add.
---

# Fixer sub-agent

Turn detected problems into ready-to-use fixes. This is where the model earns its place.

## Implementation Details
- **Architecture**: Implemented as a Python class `Fixer` in `seo/fixer.py`.
- **LLM Integration**: Communicates with local Ollama API (`gemma4:31b-cloud`) using `requests`.
- **Validation Loop (Champion Tier)**:
  - For titles and meta descriptions, the fixer uses a `while` loop.
  - If the LLM returns a title > 60 characters or a meta description > 155 characters, the result is rejected.
  - The prompt is refined to be more explicit about the length constraint, and the model is called again.
  - Max retry limit is set to 5 attempts to prevent infinite loops.
- **Redirect Suggestions**: Analyzes the URL slug of 4xx pages to suggest a logical target URL.

## Workflow
1. For pages flagged `missing_title`, `title_too_long`, `missing_meta_description`, etc.:
   - Request optimized rewrite.
   - Validate length in Python.
   - Retry if too long.
   - Collect `{url, old, new}`.
2. For `broken_link` (4xx) pages:
   - Request logical redirect target based on slug.
   - Collect `{from, to, reason}`.
3. Final results are pushed to the MCP server via `seo_set_fixes`.

Keep each rewrite a small, separate model call so context stays tight and quota stays low.
Never feed the whole crawl to the model — only the one page you are fixing.
