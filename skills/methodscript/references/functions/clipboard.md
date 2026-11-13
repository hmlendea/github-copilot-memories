# MethodScript Function Reference: Clipboard

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Provides functions for managing the system clipboard

2 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `get_clipboard([flavor])` -> string (throws FormatException; InsufficientPermissionException; UnsupportedOperationException) [restricted] - Returns the contents of the system clipboard. Can only be used in cmdline mode. Flavor defaults to null, and is currently unused. Only strings are currently supported.
- `set_clipboard(value, [flavor])` -> void (throws InsufficientPermissionException; UnsupportedOperationException) [restricted] - Sets the contents of the system clipboard, to the given value. Can only be used in cmdline mode. Flavor defaults to null, and is currently unused. Only strings are currently supported.
