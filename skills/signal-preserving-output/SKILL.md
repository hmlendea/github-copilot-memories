---
name: signal-preserving-output
description: Use when builds, tests, linters, logs, Git commands, or other terminal operations may return verbose output.
---

Minimise returned output without hiding evidence.
- Narrow execution to the affected project, test, file, path, or revision first.
- Prefer native quiet, summary, count, name-only, or structured-output options that preserve exit status, warnings, errors, and failing identifiers.
- Success: retain command, exit status, and concise native summary.
- Failure: retain every distinct failure identifier plus sufficient diagnostic context; deduplicate repeated noise only.
- Never filter interactive commands or conceal prompts.
- If filtering could alter interpretation, return unfiltered relevant output.
