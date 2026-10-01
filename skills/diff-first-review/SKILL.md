---
name: diff-first-review
description: Use when reviewing a change, pull request, patch, or diff for defects, regressions, risks, or missing tests.
---

Review the change surface before repository history.
- Start with changed-file names, diff statistics, then relevant hunks.
- Trace only changed symbols to their definitions, callers, contracts, and focused tests.
- Read unchanged files only when a hunk exposes a concrete dependency, invariant, or compatibility risk.
- Prioritise correctness, security, behavioural regression, and missing tests; ignore unrelated style.
- Report findings as `path:line - severity: issue`; explain impact and smallest remedy.
- No finding: state this and name residual test gaps or uncertainty.
