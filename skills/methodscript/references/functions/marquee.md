# MethodScript Function Reference: Marquee

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

2 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `marquee([marqueeName], text, stringWidth, delayTime, callback)` -> void (throws CastException) [restricted] - Sets up a marquee, which will automatically split up a given string for you, and call the callback. The split string will automatically wrap, handle buffering spaces, and scroll through the text.
- `marquee_stop(marqueeName)` -> void [restricted] - Stops a named marquee.
