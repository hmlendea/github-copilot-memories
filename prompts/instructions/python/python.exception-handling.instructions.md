---
description: "Use when writing or editing Python code. Covers exception handling."
applyTo: "**/*.py"
---
## Python

### Error Handling

- Guard clauses at top of functions for missing configuration or preconditions.
- `try/except Exception as exception:` wrapping all external I/O calls (HTTP, file, socket).
- Check response status code before parsing the body: `if response.status_code == 200:`.
- Use `.get("key", default)` for safe dict access on JSON responses.
