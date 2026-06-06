# DECISIONS.md — decision & learnings log

A short running note of the real choices you made: what you tried, what failed and why, what
you changed. This is your engineering judgement on the record — it is what separates a builder
from a button-presser, and it is graded (challenge brief section 08).

Append a 1–2 line entry whenever you make a real decision or hit/fix a wall. Add a timestamp.

Format:
`[HH:MM] <decision or problem> → <what you did and why>`

---

## My log
- `[2026-06-06 10:00]` Chose `utf-8-sig` encoding for CSV loading in `detector.py` → handles potential UTF-8 BOM from Screaming Frog exports.
- `[2026-06-06 10:00]` Implemented `.strip()` and `or ""` for empty CSV values → ensures deterministic checks against empty strings without `NoneType` errors.
- `[2026-06-06 10:00]` Used `_int` and `_float` helpers with try-except defaults → prevents crash on malformed numeric cells in SF exports.
- `[2026-06-06 10:15]` Switched to `pandas` for `detector.py` → better handling of NaN values via `.fillna('')` and more efficient filtering of large CSVs.
- `[2026-06-06 10:15]` Row Isolation Strategy: Used `Content Type` column to separate `text/html` for page-level checks and image-specific types (e.g., `image/jpeg`, `image/png`) for alt-text checks.
- `[2026-06-06 10:15]` NaN Handling: Applied `.fillna('')` to all columns during ingest to avoid `NaN` comparisons failing and to treat empty cells consistently as empty strings.
