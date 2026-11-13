# MethodScript Function Reference: OS

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Contains various methods for interacting with the Operating System. Some of the functions deal with OS specific mechanisms.

1 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `get_pid()` -> int (throws UnsupportedOperationException) [restricted] - Returns the process id (pid) of the current process. In some implementations of Java, this cannot be relied on, and in those cases, an UnsupportedOperationException is thrown.
