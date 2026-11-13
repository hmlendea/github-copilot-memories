# MethodScript Function Reference: TaskHandling

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

2 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `tm_get_tasks()` -> array [restricted] - Returns an array of currently running tasks. See more...
- `tm_kill_task(taskType, id)` -> void (throws CastException) [restricted] - Attempts to kill the specified task. The taskType and id will be listed with the task in the task manager. If the task is already finished, doesn't exist, or already in the process of finishing, nothi...
