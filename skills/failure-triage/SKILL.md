---
name: failure-triage
description: Use when a focused test, build, lint, type-check, or tool command fails during a task and the next repair is unclear.
---

Classify failure before expanding context.
- Preserve command, exit status, distinct error identifiers, target paths, and nearest relevant diagnostic context.
- Classify: introduced by current change, pre-existing, environment/tooling, dependency, flaky/external, or unknown.
- For introduced failures, trace only the named symbol, changed hunk, and immediate contract.
- For pre-existing or unrelated failures, record evidence and continue with the focused task unless it blocks validation.
- Retry only after a concrete repair or transient cause; never repeat an identical failing command for speculation.
- Escalate scope only when focused evidence cannot distinguish the class.
