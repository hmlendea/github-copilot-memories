# MethodScript Function Reference: XGUI

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

This provides extremely limited gui control functions. This entire class is experimental, and will probably be removed at some point.

1 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `x_launch_browser(url)` -> void (throws IOException) [restricted] - Launches the desktop's default browser with the given url. On headless systems, this will throw an exception.
