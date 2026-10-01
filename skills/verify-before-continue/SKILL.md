---
name: verify-before-continue
description: Use for multi-step code changes. Validate each substantive edit with the cheapest focused check; stop on failure.
---
After each substantive edit:
- Run the cheapest focused check that can falsify it.
- Failure: repair and rerun before further edits.
- Final: run appropriate broader checks for the touched surface.
- Report command and outcome; omit passing noise.
Stop when acceptance criteria pass; no adjacent work.
