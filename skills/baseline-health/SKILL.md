---
name: baseline-health
description: Use before changing code when test, build, lint, or type-check baseline status is unknown and pre-existing failures could cause rework.
---

Establish the smallest useful baseline.
- Identify the focused check for the intended file, project, or behaviour.
- Run it before editing when inexpensive and available.
- Passing baseline: record command and continue.
- Failing baseline: capture distinct failures, determine whether they touch the target surface, and state baseline status before editing.
- No focused check: state baseline unknown; do not run a broad suite solely for orientation.
- Never repair unrelated baseline failures unless requested.
