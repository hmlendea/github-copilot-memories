---
name: verify-before-continue
description: Apply to all multi-step code changes. Run checks after each step; do not proceed on failure.
---
After each change run: tests, linter, type-check. If any fail, fix before the next step.
Stop when all checks pass — do not add unrequested work.
